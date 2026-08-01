"""국토교통부 오피스텔 매매 실거래가 공개시스템 collector.

collectors/molit.py(아파트 매매)/molit_villa.py(연립다세대 매매)와 지역군·수집 파이프라인
구조가 동일하다 — 차이는 데이터 소스(오피스텔 매매 실거래가 자료)뿐이라 그 모듈들을 거의
그대로 복제했다. 응답 필드명(dealAmount/excluUseAr 등)은 국토부 실거래가 API 계열이 매물
유형과 무관하게 공유하는 스키마라 collectors/molit.py의 _price_per_pyeong 파싱 로직도
그대로 적용된다.

base_url은 data.go.kr Swagger 문서로 아직 실측 확인되지 않은 값이다(config/api.yaml 참고) —
서비스ID가 다르면 SERVICE_ACCESS_DENIED_ERROR가 아니라 404로 나타나므로, 활용신청 승인 후
첫 실행에서 그 구분으로 원인을 좁히면 된다.
"""
from __future__ import annotations

import time
from statistics import median
from typing import Any

import requests

from core.config import api_config, get_api_key
from core.logger import log_event
from . import base
from .kr_regions import HIGHLIGHT_REGION, REGION_TIERS, SEOUL_DISTRICTS, all_regions
from .molit import _price_per_pyeong, _trailing_deal_months

_HISTORY_MONTHS_BACKFILL = 4
_TIMEOUT_SECONDS = 8
_PAGE_SIZE = 1000

SOURCE = "molit_officetel"
SERIES_PREFIX = "molit_officetel"


def _fetch_region_month(lawd_cd: str, deal_ymd: str, api_key: str) -> list[dict[str, Any]]:
    base_url = api_config()["sources"][SOURCE]["base_url"]
    params = {
        "serviceKey": api_key, "LAWD_CD": lawd_cd, "DEAL_YMD": deal_ymd,
        "pageNo": 1, "numOfRows": _PAGE_SIZE, "type": "json",
    }
    resp = requests.get(base_url, params=params, timeout=_TIMEOUT_SECONDS)
    base.raise_for_status(resp)
    try:
        payload = resp.json()
    except ValueError:
        raise RuntimeError(
            f"MOLIT officetel (오피스텔) returned non-JSON response (likely a service/auth error): "
            f"{base.redact_url(resp.text[:300])}"
        )
    header = payload.get("response", {}).get("header", {})
    if header.get("resultCode") not in (None, "00", "000"):
        raise RuntimeError(f"MOLIT officetel (오피스텔) error response: {header.get('resultMsg')}")
    items = payload.get("response", {}).get("body", {}).get("items")
    if not items:
        return []
    rows = items.get("item", []) if isinstance(items, dict) else items
    return rows if isinstance(rows, list) else [rows]


def _probe_with_detail(lawd_cd: str, deal_ymd: str, api_key: str,
                        attempts: int = 2, backoff_seconds: float = 1.5) -> tuple[list[dict] | None, str | None]:
    last_error: str | None = None
    for attempt in range(1, attempts + 1):
        try:
            return _fetch_region_month(lawd_cd, deal_ymd, api_key), None
        except Exception as exc:  # collectors must never crash the pipeline
            last_error = str(exc)
            log_event("collector.fetch_failed", level="warning",
                      label=f"{SOURCE}:probe:{lawd_cd}", attempt=attempt, error=last_error)
            if attempt < attempts:
                time.sleep(backoff_seconds * attempt)
    return None, last_error


def fetch_and_store() -> dict[str, Any]:
    """Fetch every configured region for the needed trailing months, persist per-district,
    per-tier, and highlight normalized series, and return a coverage summary."""
    api_key = get_api_key(SOURCE)
    if not api_key:
        note = "DATA_GO_KR_KEY not set — register a free key at data.go.kr (오피스텔 매매 실거래가 자료)"
        log_event("collector.molit_officetel_skipped", level="warning", note=note)
        return {"status": "pending", "note": note, "regions_total": len(all_regions())}

    regions = all_regions()
    thinnest_history = min(
        (len(base.read_normalized(f"{SERIES_PREFIX}_{tier}_price_pyeong")) for tier in REGION_TIERS),
        default=0,
    )
    months_needed = _HISTORY_MONTHS_BACKFILL if thinnest_history < 2 else 1
    target_months = _trailing_deal_months(months_needed)

    probe_region = regions[0]
    probe_rows, probe_error = _probe_with_detail(probe_region["code"], target_months[-1], api_key)
    if probe_rows is None:
        note = f"MOLIT officetel (오피스텔) unreachable (probe call failed after retry): {probe_error} — skipped remaining regions to avoid a long CI stall"
        log_event("collector.molit_officetel_circuit_breaker_tripped", level="warning", note=note)
        return {"status": "source_error", "note": note, "regions_total": len(regions), "regions_covered": 0}

    month_region_prices: dict[str, dict[str, list[float]]] = {}
    regions_covered: set[str] = set()
    for deal_ymd in target_months:
        region_prices: dict[str, list[float]] = {}
        for region in regions:
            rows = base.retry(
                lambda r=region: _fetch_region_month(r["code"], deal_ymd, api_key),
                label=f"{SOURCE}:{region['code']}:{deal_ymd}", attempts=2, backoff_seconds=1.0,
            )
            if not rows:
                continue
            prices = [p for p in (_price_per_pyeong(r) for r in rows) if p is not None]
            if prices:
                region_prices[region["code"]] = prices
                regions_covered.add(region["code"])
        month_region_prices[deal_ymd] = region_prices

    for deal_ymd, region_prices in month_region_prices.items():
        month_date = f"{deal_ymd[0:4]}-{deal_ymd[4:6]}-01"
        for region in SEOUL_DISTRICTS:
            prices = region_prices.get(region["code"])
            if prices:
                base.append_normalized(f"{SERIES_PREFIX}_district_{region['code']}_price_pyeong",
                                        [{"date": month_date, "value": median(prices)}])

    for deal_ymd, region_prices in month_region_prices.items():
        prices = region_prices.get(HIGHLIGHT_REGION["code"])
        if not prices:
            continue
        month_date = f"{deal_ymd[0:4]}-{deal_ymd[4:6]}-01"
        base.append_normalized(f"{SERIES_PREFIX}_highlight_price_pyeong", [{"date": month_date, "value": median(prices)}])
        base.append_normalized(f"{SERIES_PREFIX}_highlight_volume", [{"date": month_date, "value": float(len(prices))}])

    for tier, tier_regions in REGION_TIERS.items():
        codes = {r["code"] for r in tier_regions}
        for deal_ymd in target_months:
            region_prices = month_region_prices.get(deal_ymd, {})
            pooled = [p for code in codes for p in region_prices.get(code, [])]
            if not pooled:
                continue
            month_date = f"{deal_ymd[0:4]}-{deal_ymd[4:6]}-01"
            coverage = sum(1 for code in codes if region_prices.get(code))
            base.append_normalized(f"{SERIES_PREFIX}_{tier}_price_pyeong", [{"date": month_date, "value": median(pooled)}])
            base.append_normalized(f"{SERIES_PREFIX}_{tier}_volume", [{"date": month_date, "value": float(len(pooled))}])
            base.write_raw(SOURCE, f"{tier}_{deal_ymd}", {
                "deal_ymd": deal_ymd, "median_price_pyeong": median(pooled), "transaction_count": len(pooled),
                "regions_covered": coverage, "regions_total": len(codes),
            })

    log_event("collector.molit_officetel_completed", regions_covered=len(regions_covered), regions_total=len(regions),
               months_fetched=target_months)
    return {
        "status": "ok" if regions_covered else "source_error",
        "regions_covered": len(regions_covered), "regions_total": len(regions),
        "months_fetched": target_months,
    }
