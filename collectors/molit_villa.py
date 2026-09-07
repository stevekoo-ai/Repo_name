"""국토교통부 연립다세대(빌라) 매매 실거래가 공개시스템 collector.

collectors/molit.py(아파트 매매)와 지역군·수집 파이프라인 구조가 동일하다 — 차이는 데이터
소스(연립다세대 매매 실거래가 자료, data ID 15126472대) 하나뿐이라 그 모듈을 거의 그대로
복제했다. 응답 필드명(dealAmount/excluUseAr 등)은 국토부 실거래가 API 계열이 매물 유형과
무관하게 공유하는 스키마라 collectors/molit.py의 _price_per_pyeong 파싱 로직도 그대로 적용된다.

base_url은 data.go.kr Swagger 문서로 아직 실측 확인되지 않은 값이다(config/api.yaml 참고) —
서비스ID가 다르면 SERVICE_ACCESS_DENIED_ERROR가 아니라 404로 나타나므로, 활용신청 승인 후
첫 실행에서 그 구분으로 원인을 좁히면 된다.
"""
from __future__ import annotations

import time
from datetime import datetime
from statistics import median
from typing import Any

import requests

from core.config import api_config, get_api_key
from core.logger import log_event
from . import base
from .kr_regions import HIGHLIGHT_REGION, REGION_TIERS, SEOUL_DISTRICTS, TIER_LABELS, all_regions, probe_regions
from .molit import _price_per_pyeong, _trailing_deal_months

_HISTORY_MONTHS_BACKFILL = 4
# 2026-09-07: connect 8초는 너무 짧았다. 같은 GitHub Actions 러너에서
# scripts/api_probe.py가 timeout=20으로 4종 전부 성공한 직후, 이 수집기들은
# 전부 "connect timeout=8"로 죽었다 — 즉 apis.data.go.kr이 막힌 게 아니라
# 8초 안에 TCP 핸드셰이크가 안 끝나는 것뿐이었다. requests는 (연결, 응답)
# 튜플을 받으므로 연결에 넉넉히 주고 응답은 따로 제한한다.
_TIMEOUT_SECONDS = (15, 30)
_PAGE_SIZE = 1000

SOURCE = "molit_villa"
SERIES_PREFIX = "molit_villa"


def _fetch_region_month(lawd_cd: str, deal_ymd: str, api_key: str) -> list[dict[str, Any]]:
    base_url = api_config()["sources"][SOURCE]["base_url"]
    params = {
        "serviceKey": api_key, "LAWD_CD": lawd_cd, "DEAL_YMD": deal_ymd,
        "pageNo": 1, "numOfRows": _PAGE_SIZE, "type": "json",
    }
    resp = requests.get(base_url, params=params, timeout=_TIMEOUT_SECONDS)
    base.raise_for_status(resp)
    # 형식(JSON/XML)에 상관없이 파싱 — collectors/base.py의 파서 주석 참고.
    # 2026-09-07 이전엔 여기서 resp.json()만 부르다 XML 응답에 깨졌고,
    # 그 실패가 인증 오류로 오진돼 한 달간 조용히 수집이 멈춰 있었다.
    return base.parse_data_go_kr_items(resp, "MOLIT 연립다세대")


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
        note = "DATA_GO_KR_KEY not set — register a free key at data.go.kr (연립다세대 매매 실거래가 자료)"
        log_event("collector.molit_villa_skipped", level="warning", note=note)
        return {"status": "pending", "note": note, "regions_total": len(all_regions())}

    regions = all_regions()
    thinnest_history = min(
        (len(base.read_normalized(f"{SERIES_PREFIX}_{tier}_price_pyeong")) for tier in REGION_TIERS),
        default=0,
    )
    months_needed = _HISTORY_MONTHS_BACKFILL if thinnest_history < 2 else 1
    target_months = _trailing_deal_months(months_needed)

    # 2026-09-07: 예전엔 all_regions[0](종로구) 한 곳만 찔러보고 실패하면 55개
    # 지역을 통째로 포기했다. 한 지역의 일시적 connect timeout이 그날 수집
    # 전체를 날리는 구조 — 실제로 그렇게 됐다(같은 러너에서 강남구는 정상
    # 응답하는데 종로구 타임아웃 하나로 전량 skip). 서킷브레이커의 목적은
    # "소스가 진짜 죽었을 때 CI를 오래 붙잡지 않는 것"이지 "한 번 삐끗하면
    # 포기하는 것"이 아니므로, 서로 다른 지역 몇 곳이 **모두** 실패할 때만
    # 소스가 죽었다고 판정한다.
    probe_rows = probe_error = None
    for probe_region in probe_regions(regions):
        probe_rows, probe_error = _probe_with_detail(
            probe_region["code"], target_months[-1], api_key)
        if probe_rows is not None:
            break
    if probe_rows is None:
        note = f"MOLIT villa (연립다세대) unreachable (probe call failed after retry): {probe_error} — skipped remaining regions to avoid a long CI stall"
        log_event("collector.molit_villa_circuit_breaker_tripped", level="warning", note=note)
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

    log_event("collector.molit_villa_completed", regions_covered=len(regions_covered), regions_total=len(regions),
               months_fetched=target_months)
    return {
        "status": "ok" if regions_covered else "source_error",
        "regions_covered": len(regions_covered), "regions_total": len(regions),
        "months_fetched": target_months,
    }
