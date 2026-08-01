"""국토교통부 아파트 전월세 실거래가 공개시스템 collector.

collectors/molit.py(아파트 매매)와 지역군·수집 파이프라인 구조는 같지만, 매매와 달리 한
거래가 전세(보증금만) 또는 월세(보증금+월세)로 갈린다 — 두 유형을 하나로 뭉개면 시세
신호가 흐려지므로 별도 계열로 분리해 저장한다. monthlyRent가 0(또는 빈 값)인 거래를 전세로
분류한다.

거래 단위 dealAmount 대신 deposit(보증금)/monthlyRent(월세) 필드를 쓰는 것만 매매 API와
다르고, excluUseAr(전용면적) 등 나머지 필드명은 국토부 실거래가 API 계열 공통 스키마를
그대로 따른다는 전제다. base_url은 data.go.kr Swagger 문서로 아직 실측 확인되지 않은
값이다(config/api.yaml 참고) — 서비스ID가 다르면 SERVICE_ACCESS_DENIED_ERROR가 아니라
404로 나타나므로, 활용신청 승인 후 첫 실행에서 그 구분으로 원인을 좁히면 된다.
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
from .molit import _trailing_deal_months

_HISTORY_MONTHS_BACKFILL = 4
_TIMEOUT_SECONDS = 8
_PAGE_SIZE = 1000

SOURCE = "molit_rent"
SERIES_PREFIX = "molit_rent"


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
            f"MOLIT rent (전월세) returned non-JSON response (likely a service/auth error): "
            f"{base.redact_url(resp.text[:300])}"
        )
    header = payload.get("response", {}).get("header", {})
    if header.get("resultCode") not in (None, "00", "000"):
        raise RuntimeError(f"MOLIT rent (전월세) error response: {header.get('resultMsg')}")
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


def _amount_per_pyeong(row: dict[str, Any], amount_field: str) -> float | None:
    """One transaction's <amount_field>(만원)/전용면적(㎡) -> 원/3.3㎡(평)."""
    try:
        amount_manwon = float(str(row[amount_field]).replace(",", "").strip())
        area_m2 = float(row["excluUseAr"])
    except (KeyError, ValueError, TypeError):
        return None
    if area_m2 <= 0:
        return None
    pyeong = area_m2 / 3.3058
    return (amount_manwon * 10_000) / pyeong


def _is_jeonse(row: dict[str, Any]) -> bool:
    """monthlyRent가 0(또는 빈 값)이면 전세, 그 외에는 월세."""
    try:
        rent = float(str(row.get("monthlyRent", "0") or "0").replace(",", "").strip())
    except (ValueError, TypeError):
        return False
    return rent == 0


def _split_prices(rows: list[dict[str, Any]]) -> dict[str, list[float]]:
    """한 지역·월 거래 목록을 전세 보증금/월세 보증금/월세 월세액(모두 평당)으로 나눈다.
    월세 거래는 보증금·월세 둘 다 파싱 성공한 것만 카운트해 두 계열의 거래량을 일치시킨다."""
    jeonse_deposit: list[float] = []
    wolse_deposit: list[float] = []
    wolse_rent: list[float] = []
    for row in rows:
        if _is_jeonse(row):
            price = _amount_per_pyeong(row, "deposit")
            if price is not None:
                jeonse_deposit.append(price)
        else:
            deposit_price = _amount_per_pyeong(row, "deposit")
            rent_price = _amount_per_pyeong(row, "monthlyRent")
            if deposit_price is not None and rent_price is not None:
                wolse_deposit.append(deposit_price)
                wolse_rent.append(rent_price)
    return {
        "jeonse_deposit_pyeong": jeonse_deposit,
        "wolse_deposit_pyeong": wolse_deposit,
        "wolse_rent_pyeong": wolse_rent,
    }


def fetch_and_store() -> dict[str, Any]:
    """Fetch every configured region for the needed trailing months, persist per-district
    (전세만), per-tier, and highlight normalized series for both 전세/월세, and return a
    coverage summary."""
    api_key = get_api_key(SOURCE)
    if not api_key:
        note = "DATA_GO_KR_KEY not set — register a free key at data.go.kr (아파트 전월세 실거래가 자료)"
        log_event("collector.molit_rent_skipped", level="warning", note=note)
        return {"status": "pending", "note": note, "regions_total": len(all_regions())}

    regions = all_regions()
    thinnest_history = min(
        (len(base.read_normalized(f"{SERIES_PREFIX}_jeonse_{tier}_price_pyeong")) for tier in REGION_TIERS),
        default=0,
    )
    months_needed = _HISTORY_MONTHS_BACKFILL if thinnest_history < 2 else 1
    target_months = _trailing_deal_months(months_needed)

    probe_region = regions[0]
    probe_rows, probe_error = _probe_with_detail(probe_region["code"], target_months[-1], api_key)
    if probe_rows is None:
        note = f"MOLIT rent (전월세) unreachable (probe call failed after retry): {probe_error} — skipped remaining regions to avoid a long CI stall"
        log_event("collector.molit_rent_circuit_breaker_tripped", level="warning", note=note)
        return {"status": "source_error", "note": note, "regions_total": len(regions), "regions_covered": 0}

    # month -> region_code -> {"jeonse_deposit_pyeong": [...], "wolse_deposit_pyeong": [...], "wolse_rent_pyeong": [...]}
    month_region_splits: dict[str, dict[str, dict[str, list[float]]]] = {}
    regions_covered: set[str] = set()
    for deal_ymd in target_months:
        region_splits: dict[str, dict[str, list[float]]] = {}
        for region in regions:
            rows = base.retry(
                lambda r=region: _fetch_region_month(r["code"], deal_ymd, api_key),
                label=f"{SOURCE}:{region['code']}:{deal_ymd}", attempts=2, backoff_seconds=1.0,
            )
            if not rows:
                continue
            split = _split_prices(rows)
            if any(split.values()):
                region_splits[region["code"]] = split
                regions_covered.add(region["code"])
        month_region_splits[deal_ymd] = region_splits

    # Per-district series (Seoul only, 전세 보증금만 — 매매의 top-movers 랭킹과 동일한 용도).
    # Naming (`{PREFIX}_jeonse_district_{code}_price_pyeong`) matches the generic
    # engine.real_estate.market_trend._district_movers(series_prefix=f"{PREFIX}_jeonse")
    # convention (series_prefix + "_district_" + code + "_price_pyeong") so 전세 trend reuses
    # the same reader as 매매, instead of a jeonse-specific engine function.
    for deal_ymd, region_splits in month_region_splits.items():
        month_date = f"{deal_ymd[0:4]}-{deal_ymd[4:6]}-01"
        for region in SEOUL_DISTRICTS:
            prices = region_splits.get(region["code"], {}).get("jeonse_deposit_pyeong")
            if prices:
                base.append_normalized(f"{SERIES_PREFIX}_jeonse_district_{region['code']}_price_pyeong",
                                        [{"date": month_date, "value": median(prices)}])

    # Highlight region series (용인 기흥구) — 전세/월세 둘 다. 전세 쪽은 마찬가지로
    # {PREFIX}_jeonse_highlight_price_pyeong 이름으로 맞춰 market_trend._highlight_region 재사용.
    for deal_ymd, region_splits in month_region_splits.items():
        split = region_splits.get(HIGHLIGHT_REGION["code"])
        if not split:
            continue
        month_date = f"{deal_ymd[0:4]}-{deal_ymd[4:6]}-01"
        if split["jeonse_deposit_pyeong"]:
            base.append_normalized(f"{SERIES_PREFIX}_jeonse_highlight_price_pyeong",
                                    [{"date": month_date, "value": median(split["jeonse_deposit_pyeong"])}])
            base.append_normalized(f"{SERIES_PREFIX}_jeonse_highlight_volume",
                                    [{"date": month_date, "value": float(len(split["jeonse_deposit_pyeong"]))}])
        if split["wolse_deposit_pyeong"]:
            base.append_normalized(f"{SERIES_PREFIX}_wolse_highlight_deposit_pyeong",
                                    [{"date": month_date, "value": median(split["wolse_deposit_pyeong"])}])
            base.append_normalized(f"{SERIES_PREFIX}_wolse_highlight_rent_pyeong",
                                    [{"date": month_date, "value": median(split["wolse_rent_pyeong"])}])
            base.append_normalized(f"{SERIES_PREFIX}_wolse_highlight_volume",
                                    [{"date": month_date, "value": float(len(split["wolse_deposit_pyeong"]))}])

    # Tier aggregates — pooled (not median-of-medians) across every region in the tier.
    for tier, tier_regions in REGION_TIERS.items():
        codes = {r["code"] for r in tier_regions}
        for deal_ymd in target_months:
            region_splits = month_region_splits.get(deal_ymd, {})
            pooled_jeonse = [p for code in codes for p in region_splits.get(code, {}).get("jeonse_deposit_pyeong", [])]
            pooled_wolse_deposit = [p for code in codes for p in region_splits.get(code, {}).get("wolse_deposit_pyeong", [])]
            pooled_wolse_rent = [p for code in codes for p in region_splits.get(code, {}).get("wolse_rent_pyeong", [])]
            if not pooled_jeonse and not pooled_wolse_deposit:
                continue
            month_date = f"{deal_ymd[0:4]}-{deal_ymd[4:6]}-01"
            coverage = sum(1 for code in codes if region_splits.get(code))
            if pooled_jeonse:
                base.append_normalized(f"{SERIES_PREFIX}_jeonse_{tier}_price_pyeong",
                                        [{"date": month_date, "value": median(pooled_jeonse)}])
                base.append_normalized(f"{SERIES_PREFIX}_jeonse_{tier}_volume",
                                        [{"date": month_date, "value": float(len(pooled_jeonse))}])
            if pooled_wolse_deposit:
                base.append_normalized(f"{SERIES_PREFIX}_wolse_{tier}_deposit_pyeong",
                                        [{"date": month_date, "value": median(pooled_wolse_deposit)}])
                base.append_normalized(f"{SERIES_PREFIX}_wolse_{tier}_rent_pyeong",
                                        [{"date": month_date, "value": median(pooled_wolse_rent)}])
                base.append_normalized(f"{SERIES_PREFIX}_wolse_{tier}_volume",
                                        [{"date": month_date, "value": float(len(pooled_wolse_deposit))}])
            base.write_raw(SOURCE, f"{tier}_{deal_ymd}", {
                "deal_ymd": deal_ymd,
                "median_jeonse_deposit_pyeong": median(pooled_jeonse) if pooled_jeonse else None,
                "jeonse_count": len(pooled_jeonse),
                "median_wolse_deposit_pyeong": median(pooled_wolse_deposit) if pooled_wolse_deposit else None,
                "median_wolse_rent_pyeong": median(pooled_wolse_rent) if pooled_wolse_rent else None,
                "wolse_count": len(pooled_wolse_deposit),
                "regions_covered": coverage, "regions_total": len(codes),
            })

    log_event("collector.molit_rent_completed", regions_covered=len(regions_covered), regions_total=len(regions),
               months_fetched=target_months)
    return {
        "status": "ok" if regions_covered else "source_error",
        "regions_covered": len(regions_covered), "regions_total": len(regions),
        "months_fetched": target_months,
    }
