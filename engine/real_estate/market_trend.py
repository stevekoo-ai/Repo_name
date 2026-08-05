"""부동산 실거래가 트렌드 분석.

MOLIT 실거래가는 개별 거래 원자료라 사전 계산된 지수가 없다 — collectors/molit.py가
지역군별/구별 월 중위 가격(원/평)·거래건수로 집계해 정규화 저장소에 쌓아두면, 여기서는
그 누적 이력만 읽어 전월 대비(MoM)·3개월 추세·거래량 변화·시장 온도를 계산한다.
"""
from __future__ import annotations

from collectors import base as collector_base
from collectors import kr_regions, molit

_MANWON = 10_000


def _pct_change(current: float | None, prior: float | None) -> float | None:
    if current is None or prior is None or prior == 0:
        return None
    return (current - prior) / prior * 100


def _price_and_volume(price_series_id: str, volume_series_id: str) -> dict:
    price_df = collector_base.read_normalized(price_series_id)
    if price_df.empty:
        return {"data_status": "pending"}

    price_df = price_df.sort_values("date").reset_index(drop=True)
    volume_df = collector_base.read_normalized(volume_series_id)
    volume_df = volume_df.sort_values("date").reset_index(drop=True) if not volume_df.empty else volume_df

    latest_price = float(price_df.iloc[-1]["value"])
    prior_1m_price = float(price_df.iloc[-2]["value"]) if len(price_df) >= 2 else None
    prior_3m_price = float(price_df.iloc[-4]["value"]) if len(price_df) >= 4 else None

    latest_volume = float(volume_df.iloc[-1]["value"]) if not volume_df.empty else None
    prior_volume = float(volume_df.iloc[-2]["value"]) if len(volume_df) >= 2 else None

    mom_pct = _pct_change(latest_price, prior_1m_price)
    trend_3m_pct = _pct_change(latest_price, prior_3m_price)
    volume_mom_pct = _pct_change(latest_volume, prior_volume)

    return {
        "data_status": "ok",
        "reference_month": str(price_df.iloc[-1]["date"])[:7],
        "price_per_pyeong_manwon": round(latest_price / _MANWON, 0),
        "mom_change_pct": round(mom_pct, 2) if mom_pct is not None else None,
        "trend_3m_pct": round(trend_3m_pct, 2) if trend_3m_pct is not None else None,
        "transaction_count": int(latest_volume) if latest_volume is not None else None,
        "volume_mom_change_pct": round(volume_mom_pct, 1) if volume_mom_pct is not None else None,
        "market_heat": _market_heat(mom_pct, volume_mom_pct),
    }


def _market_heat(mom_pct: float | None, volume_mom_pct: float | None) -> str:
    """Heuristic 3-band read, not a scored indicator: price momentum plus whether
    volume is confirming it. 데이터 부족 시 판단 보류."""
    if mom_pct is None:
        return "데이터 부족"
    if mom_pct >= 1.0 and (volume_mom_pct is None or volume_mom_pct >= 0):
        return "과열"
    if mom_pct <= -1.0:
        return "냉각"
    return "보합"


def _tier_trend(tier: str, series_prefix: str = "molit", tier_labels: dict | None = None) -> dict:
    labels = tier_labels if tier_labels is not None else kr_regions.TIER_LABELS
    result = _price_and_volume(f"{series_prefix}_{tier}_price_pyeong", f"{series_prefix}_{tier}_volume")
    result["tier"] = tier
    result["label"] = labels[tier]
    return result


def _highlight_region(series_prefix: str = "molit", highlight_region: dict | None = None) -> dict:
    region = highlight_region if highlight_region is not None else kr_regions.HIGHLIGHT_REGION
    result = _price_and_volume(f"{series_prefix}_highlight_price_pyeong", f"{series_prefix}_highlight_volume")
    result["region_name"] = region["name"]
    result["note"] = region.get("highlight")
    return result


def _district_movers(limit: int = 3, series_prefix: str = "molit", seoul_districts: list | None = None) -> dict:
    """서울 25개 자치구 중 최근월 평당가 MoM 상승률 상위/하위 지역."""
    districts = seoul_districts if seoul_districts is not None else kr_regions.SEOUL_DISTRICTS
    rows = []
    for region in districts:
        df = collector_base.read_normalized(f"{series_prefix}_district_{region['code']}_price_pyeong")
        if df.empty or len(df) < 2:
            continue
        df = df.sort_values("date").reset_index(drop=True)
        latest = float(df.iloc[-1]["value"])
        prior = float(df.iloc[-2]["value"])
        mom_pct = _pct_change(latest, prior)
        if mom_pct is None:
            continue
        rows.append({
            "name": region["name"],
            "price_per_pyeong_manwon": round(latest / _MANWON, 0),
            "mom_change_pct": round(mom_pct, 2),
        })

    if not rows:
        return {"data_status": "pending", "gainers": [], "decliners": []}

    ranked = sorted(rows, key=lambda r: r["mom_change_pct"], reverse=True)
    return {
        "data_status": "ok",
        "gainers": ranked[:limit],
        "decliners": list(reversed(ranked[-limit:])) if len(ranked) > limit else [],
    }


def compute_sale_trend(fetch_and_store_fn, series_prefix: str) -> dict:
    """Generic 매매 trend builder shared by 아파트(molit)/연립다세대(molit_villa)/오피스텔
    (molit_officetel) — they differ only in which collector fetches the data and which
    normalized-series prefix it wrote to; region tiers/labels are shared (collectors/kr_regions.py)."""
    fetch_summary = fetch_and_store_fn()

    return {
        "fetch_status": fetch_summary["status"],
        "fetch_note": fetch_summary.get("note"),
        "regions_covered": fetch_summary.get("regions_covered"),
        "regions_total": fetch_summary.get("regions_total"),
        "tiers": {tier: _tier_trend(tier, series_prefix=series_prefix) for tier in kr_regions.REGION_TIERS},
        "highlight": _highlight_region(series_prefix=series_prefix),
        "seoul_district_movers": _district_movers(series_prefix=series_prefix),
    }


def compute_real_estate_trend() -> dict:
    """Main entry point — triggers the MOLIT(아파트 매매) fetch, then reads back accumulated
    normalized history to build the report-ready trend payload."""
    return compute_sale_trend(molit.fetch_and_store, "molit")
