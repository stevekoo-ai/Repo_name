"""국토교통부 아파트매매 실거래가 공개시스템 collector.

서울(25개 자치구 전역) / 수도권(서울+경기+인천 주요 대도시) / 전국(대표 도시 표본)
3단 지역군 실거래가 트렌드를 만들기 위한 데이터 소스. 개인 청약 타겟(용인 플랫폼시티,
config/user.yaml housing.priority_regions)과 가장 가까운 용인 기흥구는 별도 series로도
쌓아 리포트에서 하이라이트한다.

Requires a free 공공데이터포털(data.go.kr) "아파트매매 실거래 상세자료" 일반 인증키
(DATA_GO_KR_KEY — data.go.kr issues one general-purpose "Decoding" key per
account that's shared across every service you're approved for, not one key
per API, hence the generic env var name). Without one, every region returns
Pending — no guessing (7.9).

MOLIT's raw feed is per-transaction (no ready-made index), so this module
aggregates each region's monthly transactions into summary points (median
가격/평, 거래건수) before writing to the normalized store — one row per
(series, month), matching the (date, value) shape every other collector uses.

Circuit breaker: ECOS/KOSIS calls from this pipeline's GitHub Actions runner
were observed (see collectors/kosis.py) to hang on a connect timeout against
every Korean-government-hosted endpoint, not just fail fast — that turned a
~15-series fetch into an 8-minute pipeline stall. MOLIT goes through the
unified data.go.kr gateway (apis.data.go.kr) rather than an agency's own
domain, so it may not share that restriction, but with ~55 configured
regions x up to 4 backfill months the worst case (every call timing out) would
be over an hour. To bound that, the very first call is a "probe": if it fails
outright, the whole fetch aborts immediately instead of repeating the same
failure 200+ more times.
"""
from __future__ import annotations

from datetime import datetime
from statistics import median
from typing import Any

import requests

from core.config import api_config, get_api_key
from core.logger import log_event
from . import base

_HISTORY_MONTHS_BACKFILL = 4  # first-run backfill depth once normalized history exists it's just 1
_TIMEOUT_SECONDS = 8  # kept short deliberately — see module docstring on the circuit breaker
_PAGE_SIZE = 1000  # a single sigungu-month practically never exceeds this many apartment deals

# 법정동코드(5자리 시군구 코드, 행정표준코드관리시스템 code.go.kr 기준). MOLIT가 특정
# 지역에서 계속 빈 배열만 돌려준다면 구·시 통합/신설로 코드가 바뀌었을 가능성이 있으니
# 그 지역만 code.go.kr에서 재확인하면 된다 — 나머지 지역 집계에는 영향 없음.
SEOUL_DISTRICTS: list[dict[str, str]] = [
    {"name": "종로구", "code": "11110"}, {"name": "중구", "code": "11140"},
    {"name": "용산구", "code": "11170"}, {"name": "성동구", "code": "11200"},
    {"name": "광진구", "code": "11215"}, {"name": "동대문구", "code": "11230"},
    {"name": "중랑구", "code": "11260"}, {"name": "성북구", "code": "11290"},
    {"name": "강북구", "code": "11305"}, {"name": "도봉구", "code": "11320"},
    {"name": "노원구", "code": "11350"}, {"name": "은평구", "code": "11380"},
    {"name": "서대문구", "code": "11410"}, {"name": "마포구", "code": "11440"},
    {"name": "양천구", "code": "11470"}, {"name": "강서구", "code": "11500"},
    {"name": "구로구", "code": "11530"}, {"name": "금천구", "code": "11545"},
    {"name": "영등포구", "code": "11560"}, {"name": "동작구", "code": "11590"},
    {"name": "관악구", "code": "11620"}, {"name": "서초구", "code": "11650"},
    {"name": "강남구", "code": "11680"}, {"name": "송파구", "code": "11710"},
    {"name": "강동구", "code": "11740"},
]

# 서울 제외, 수도권(경기·인천) 주요 대도시 — 33개 경기 시군 전체 대신 인구 상위권 위주로
# 추려 호출 수를 관리한다. 용인 기흥구는 사용자 청약 타겟(플랫폼시티) 인근이라 하이라이트.
CAPITAL_AREA_EXTRA: list[dict[str, str]] = [
    {"name": "인천 미추홀구", "code": "28177"}, {"name": "인천 연수구", "code": "28185"},
    {"name": "인천 남동구", "code": "28200"}, {"name": "인천 부평구", "code": "28237"},
    {"name": "인천 계양구", "code": "28245"}, {"name": "인천 서구", "code": "28260"},
    {"name": "수원 영통구", "code": "41117"}, {"name": "성남 분당구", "code": "41135"},
    {"name": "안양 동안구", "code": "41173"}, {"name": "부천시", "code": "41190"},
    {"name": "안산 단원구", "code": "41273"}, {"name": "고양 일산동구", "code": "41285"},
    {"name": "남양주시", "code": "41360"}, {"name": "시흥시", "code": "41390"},
    {"name": "하남시", "code": "41450"},
    {"name": "용인 기흥구", "code": "41463", "highlight": "용인 플랫폼시티 인근 — 청약 타겟 지역"},
    {"name": "화성시", "code": "41590"}, {"name": "김포시", "code": "41570"},
]

# 수도권 제외, 8개 특·광역시 + 주요 도청소재지 대표 도시 1곳씩 — 전국 250여개 시군구
# 전량 조회는 호출량이 과도해 대표 표본으로 대체한 것. "전국" 수치는 전수조사가 아닌
# 대표 도시 표본 기준 추정치임을 리포트에도 명시한다.
NATIONWIDE_EXTRA: list[dict[str, str]] = [
    {"name": "부산 해운대구", "code": "26350"}, {"name": "대구 수성구", "code": "27260"},
    {"name": "광주 서구", "code": "29140"}, {"name": "대전 서구", "code": "30170"},
    {"name": "울산 남구", "code": "31140"}, {"name": "세종시", "code": "36110"},
    {"name": "청주 흥덕구", "code": "43113"}, {"name": "천안 서북구", "code": "44133"},
    {"name": "전주 완산구", "code": "45111"}, {"name": "포항 남구", "code": "47111"},
    {"name": "창원 성산구", "code": "48123"}, {"name": "제주시", "code": "50110"},
]

REGION_TIERS: dict[str, list[dict[str, str]]] = {
    "seoul": SEOUL_DISTRICTS,
    "capital_area": SEOUL_DISTRICTS + CAPITAL_AREA_EXTRA,
    "nationwide": SEOUL_DISTRICTS + CAPITAL_AREA_EXTRA + NATIONWIDE_EXTRA,
}

TIER_LABELS = {"seoul": "서울", "capital_area": "수도권", "nationwide": "전국(대표표본)"}

HIGHLIGHT_REGION = next(r for r in CAPITAL_AREA_EXTRA if r.get("highlight"))


def _all_regions() -> list[dict[str, str]]:
    """Every configured region, deduplicated by code (capital_area/nationwide reuse seoul)."""
    seen: dict[str, dict[str, str]] = {}
    for region in REGION_TIERS["nationwide"]:
        seen.setdefault(region["code"], region)
    return list(seen.values())


def _trailing_deal_months(n: int) -> list[str]:
    """Last n YYYYMM strings, oldest first, starting from last month — MOLIT registrations
    lag the contract date by up to ~30 days, so the current month is rarely useful yet."""
    today = datetime.utcnow()
    y, m = today.year, today.month
    months = []
    for _ in range(n):
        m -= 1
        if m == 0:
            m, y = 12, y - 1
        months.append(f"{y:04d}{m:02d}")
    return list(reversed(months))


def _fetch_region_month(lawd_cd: str, deal_ymd: str, api_key: str) -> list[dict[str, Any]]:
    base_url = api_config()["sources"]["molit"]["base_url"]
    params = {
        "serviceKey": api_key, "LAWD_CD": lawd_cd, "DEAL_YMD": deal_ymd,
        "pageNo": 1, "numOfRows": _PAGE_SIZE, "type": "json",
    }
    resp = requests.get(base_url, params=params, timeout=_TIMEOUT_SECONDS)
    resp.raise_for_status()
    payload = resp.json()
    header = payload.get("response", {}).get("header", {})
    if header.get("resultCode") not in (None, "00", "000"):
        raise RuntimeError(f"MOLIT error response: {header.get('resultMsg')}")
    items = payload.get("response", {}).get("body", {}).get("items")
    if not items:
        return []
    rows = items.get("item", []) if isinstance(items, dict) else items
    return rows if isinstance(rows, list) else [rows]


def _price_per_pyeong(row: dict[str, Any]) -> float | None:
    """One transaction's 거래금액(만원)/전용면적(㎡) -> 원/3.3㎡(평)."""
    try:
        amount_manwon = float(str(row["dealAmount"]).replace(",", "").strip())
        area_m2 = float(row["excluUseAr"])
    except (KeyError, ValueError, TypeError):
        return None
    if area_m2 <= 0:
        return None
    pyeong = area_m2 / 3.3058
    return (amount_manwon * 10_000) / pyeong


def fetch_and_store() -> dict[str, Any]:
    """Fetch every configured region for the needed trailing months, persist per-district,
    per-tier, and highlight normalized series, and return a coverage summary.

    Idempotent-ish per (region, month): re-running the same month just overwrites that
    date's row in each normalized CSV (append_normalized dedupes by date).
    """
    api_key = get_api_key("molit")
    if not api_key:
        note = "DATA_GO_KR_KEY not set — register a free key at data.go.kr (아파트매매 실거래 상세자료)"
        log_event("collector.molit_skipped", level="warning", note=note)
        return {"status": "pending", "note": note, "regions_total": len(_all_regions())}

    all_regions = _all_regions()
    thinnest_history = min(
        (len(base.read_normalized(f"molit_{tier}_price_pyeong")) for tier in REGION_TIERS),
        default=0,
    )
    months_needed = _HISTORY_MONTHS_BACKFILL if thinnest_history < 2 else 1
    target_months = _trailing_deal_months(months_needed)

    probe_region = all_regions[0]
    probe_rows = base.retry(
        lambda: _fetch_region_month(probe_region["code"], target_months[-1], api_key),
        label=f"molit:probe:{probe_region['code']}", attempts=1, backoff_seconds=0,
    )
    if probe_rows is None:
        note = "MOLIT unreachable (probe call failed) — skipped remaining regions to avoid a long CI stall"
        log_event("collector.molit_circuit_breaker_tripped", level="warning", note=note)
        return {"status": "source_error", "note": note, "regions_total": len(all_regions), "regions_covered": 0}

    # month -> {region_code: [price_per_pyeong, ...]}
    month_region_prices: dict[str, dict[str, list[float]]] = {}
    regions_covered: set[str] = set()
    for deal_ymd in target_months:
        region_prices: dict[str, list[float]] = {}
        for region in all_regions:
            rows = base.retry(
                lambda r=region: _fetch_region_month(r["code"], deal_ymd, api_key),
                label=f"molit:{region['code']}:{deal_ymd}", attempts=2, backoff_seconds=1.0,
            )
            if not rows:
                continue
            prices = [p for p in (_price_per_pyeong(r) for r in rows) if p is not None]
            if prices:
                region_prices[region["code"]] = prices
                regions_covered.add(region["code"])
        month_region_prices[deal_ymd] = region_prices

    # Per-district series (Seoul only) — powers the top-movers ranking in the report.
    for deal_ymd, region_prices in month_region_prices.items():
        month_date = f"{deal_ymd[0:4]}-{deal_ymd[4:6]}-01"
        for region in SEOUL_DISTRICTS:
            prices = region_prices.get(region["code"])
            if prices:
                base.append_normalized(f"molit_district_{region['code']}_price_pyeong",
                                        [{"date": month_date, "value": median(prices)}])

    # Highlight region series (용인 기흥구).
    for deal_ymd, region_prices in month_region_prices.items():
        prices = region_prices.get(HIGHLIGHT_REGION["code"])
        if not prices:
            continue
        month_date = f"{deal_ymd[0:4]}-{deal_ymd[4:6]}-01"
        base.append_normalized("molit_highlight_price_pyeong", [{"date": month_date, "value": median(prices)}])
        base.append_normalized("molit_highlight_volume", [{"date": month_date, "value": float(len(prices))}])

    # Tier aggregates — pooled (not median-of-medians) across every region in the tier.
    for tier, regions in REGION_TIERS.items():
        codes = {r["code"] for r in regions}
        for deal_ymd in target_months:
            region_prices = month_region_prices.get(deal_ymd, {})
            pooled = [p for code in codes for p in region_prices.get(code, [])]
            if not pooled:
                continue
            month_date = f"{deal_ymd[0:4]}-{deal_ymd[4:6]}-01"
            coverage = sum(1 for code in codes if region_prices.get(code))
            base.append_normalized(f"molit_{tier}_price_pyeong", [{"date": month_date, "value": median(pooled)}])
            base.append_normalized(f"molit_{tier}_volume", [{"date": month_date, "value": float(len(pooled))}])
            base.write_raw("molit", f"{tier}_{deal_ymd}", {
                "deal_ymd": deal_ymd, "median_price_pyeong": median(pooled), "transaction_count": len(pooled),
                "regions_covered": coverage, "regions_total": len(codes),
            })

    log_event("collector.molit_completed", regions_covered=len(regions_covered), regions_total=len(all_regions),
               months_fetched=target_months)
    return {
        "status": "ok" if regions_covered else "source_error",
        "regions_covered": len(regions_covered), "regions_total": len(all_regions),
        "months_fetched": target_months,
    }
