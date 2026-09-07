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

import time
from datetime import datetime
from statistics import median
from typing import Any

import requests

from core.config import api_config, get_api_key
from core.logger import log_event
from . import base
from .kr_regions import (
    CAPITAL_AREA_EXTRA, HIGHLIGHT_REGION, NATIONWIDE_EXTRA, REGION_TIERS,
    SEOUL_DISTRICTS, TIER_LABELS, all_regions as _all_regions, probe_regions,
)

_HISTORY_MONTHS_BACKFILL = 4  # first-run backfill depth once normalized history exists it's just 1
# 2026-09-07: connect 8초는 너무 짧았다. 같은 GitHub Actions 러너에서
# scripts/api_probe.py가 timeout=20으로 4종 전부 성공한 직후, 이 수집기들은
# 전부 "connect timeout=8"로 죽었다 — 즉 apis.data.go.kr이 막힌 게 아니라
# 8초 안에 TCP 핸드셰이크가 안 끝나는 것뿐이었다. requests는 (연결, 응답)
# 튜플을 받으므로 연결에 넉넉히 주고 응답은 따로 제한한다.
_TIMEOUT_SECONDS = (15, 30)
_PAGE_SIZE = 1000  # a single sigungu-month practically never exceeds this many apartment deals

# SEOUL_DISTRICTS/CAPITAL_AREA_EXTRA/NATIONWIDE_EXTRA/REGION_TIERS/TIER_LABELS/HIGHLIGHT_REGION/
# _all_regions live in collectors/kr_regions.py, shared with molit_rent.py/molit_villa.py/
# molit_officetel.py — re-imported here (rather than just used internally) so existing callers
# that reach in via `molit.SEOUL_DISTRICTS` etc. (engine/real_estate/market_trend.py, tests)
# keep working unchanged.


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
    base.raise_for_status(resp)
    # 형식(JSON/XML)에 상관없이 파싱 — collectors/base.py의 파서 주석 참고.
    # 2026-09-07 이전엔 여기서 resp.json()만 부르다 XML 응답에 깨졌고,
    # 그 실패가 인증 오류로 오진돼 한 달간 조용히 수집이 멈춰 있었다.
    return base.parse_data_go_kr_items(resp, "MOLIT 아파트매매")


def _probe_with_detail(lawd_cd: str, deal_ymd: str, api_key: str,
                        attempts: int = 2, backoff_seconds: float = 1.5) -> tuple[list[dict] | None, str | None]:
    """Like base.retry(_fetch_region_month), but also returns the last exception's message —
    base.retry() only logs it and returns None, which is enough for every other collector but
    not here (see the caller's comment on why the exact error text matters for MOLIT)."""
    last_error: str | None = None
    for attempt in range(1, attempts + 1):
        try:
            return _fetch_region_month(lawd_cd, deal_ymd, api_key), None
        except Exception as exc:  # collectors must never crash the pipeline
            last_error = str(exc)
            log_event("collector.fetch_failed", level="warning",
                      label=f"molit:probe:{lawd_cd}", attempt=attempt, error=last_error)
            if attempt < attempts:
                time.sleep(backoff_seconds * attempt)
    return None, last_error


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

    # 2026-09-07: 예전엔 all_regions[0](종로구) 한 곳만 찔러보고 실패하면 55개
    # 지역을 통째로 포기했다. 한 지역의 일시적 connect timeout이 그날 수집
    # 전체를 날리는 구조 — 실제로 그렇게 됐다(같은 러너에서 강남구는 정상
    # 응답하는데 종로구 타임아웃 하나로 전량 skip). 서킷브레이커의 목적은
    # "소스가 진짜 죽었을 때 CI를 오래 붙잡지 않는 것"이지 "한 번 삐끗하면
    # 포기하는 것"이 아니므로, 서로 다른 지역 몇 곳이 **모두** 실패할 때만
    # 소스가 죽었다고 판정한다.
    probe_rows = probe_error = None
    for probe_region in probe_regions(all_regions):
        probe_rows, probe_error = _probe_with_detail(
            probe_region["code"], target_months[-1], api_key)
        if probe_rows is not None:
            break
    if probe_rows is None:
        # A single try=1 probe never survived a transient blip (GitHub Actions runner IPs have
        # been observed to intermittently, not permanently, fail to reach apis.data.go.kr — same
        # pattern as KOSIS/ECOS). One extra attempt costs a few seconds and materially improves
        # the odds of a real network hiccup not tripping the breaker; a true block still fails
        # fast within ~10s either way, which is what the circuit breaker exists to bound.
        #
        # The captured exception is surfaced in `note` (not just the log) because this failure
        # has at least two very different root causes that need different fixes: a genuine
        # network/timeout issue vs. data.go.kr returning an auth/service error (e.g. this key is
        # approved for a different data.go.kr product — 한국부동산원 vs 국토교통부_아파트매매
        # 실거래 상세자료 require *separate* 활용신청 approval even under the same 인증키). Those
        # look identical as a bare "probe call failed" but very different once the actual
        # response/exception text is visible.
        note = f"MOLIT unreachable (probe call failed after retry): {probe_error} — skipped remaining regions to avoid a long CI stall"
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
