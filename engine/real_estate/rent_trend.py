"""아파트 전월세 실거래가 트렌드 — collectors/molit_rent.py 집계 결과를 읽어 계산.

매매(engine/real_estate/market_trend.py)와 구조는 같지만 전세/월세 두 계열을 같이 다룬다:
전세는 매매와 동일하게 평당 보증금 하나만 추적하면 되지만, 월세는 평당 보증금과 평당
월세액 두 숫자가 같이 있어야 시세를 읽을 수 있어 별도 헬퍼(_wolse_tier_trend)로 뽑았다.
"""
from __future__ import annotations

from collectors import base as collector_base
from collectors import kr_regions, molit_rent
from .market_trend import _district_movers, _highlight_region, _pct_change, _tier_trend

_MANWON = 10_000
_PREFIX = molit_rent.SERIES_PREFIX


_JEONSE_PREFIX = f"{_PREFIX}_jeonse"
_WOLSE_PREFIX = f"{_PREFIX}_wolse"


def _jeonse_tier_trend(tier: str) -> dict:
    return _tier_trend(tier, series_prefix=_JEONSE_PREFIX)


def _wolse_tier_trend(tier: str) -> dict:
    deposit_df = collector_base.read_normalized(f"{_WOLSE_PREFIX}_{tier}_deposit_pyeong")
    if deposit_df.empty:
        return {"data_status": "pending", "tier": tier, "label": kr_regions.TIER_LABELS[tier]}
    deposit_df = deposit_df.sort_values("date").reset_index(drop=True)
    rent_df = collector_base.read_normalized(f"{_WOLSE_PREFIX}_{tier}_rent_pyeong").sort_values("date").reset_index(drop=True)
    volume_df = collector_base.read_normalized(f"{_WOLSE_PREFIX}_{tier}_volume").sort_values("date").reset_index(drop=True)

    latest_deposit = float(deposit_df.iloc[-1]["value"])
    prior_deposit = float(deposit_df.iloc[-2]["value"]) if len(deposit_df) >= 2 else None
    latest_rent = float(rent_df.iloc[-1]["value"]) if not rent_df.empty else None
    prior_rent = float(rent_df.iloc[-2]["value"]) if len(rent_df) >= 2 else None
    latest_volume = float(volume_df.iloc[-1]["value"]) if not volume_df.empty else None

    deposit_mom = _pct_change(latest_deposit, prior_deposit)
    rent_mom = _pct_change(latest_rent, prior_rent)

    return {
        "data_status": "ok",
        "tier": tier,
        "label": kr_regions.TIER_LABELS[tier],
        "reference_month": str(deposit_df.iloc[-1]["date"])[:7],
        "deposit_per_pyeong_manwon": round(latest_deposit / _MANWON, 0),
        "deposit_mom_change_pct": round(deposit_mom, 2) if deposit_mom is not None else None,
        "rent_per_pyeong_manwon": round(latest_rent / _MANWON, 1) if latest_rent is not None else None,
        "rent_mom_change_pct": round(rent_mom, 2) if rent_mom is not None else None,
        "transaction_count": int(latest_volume) if latest_volume is not None else None,
    }


def compute_rent_trend() -> dict:
    """Main entry point — triggers the MOLIT 전월세 fetch, then reads back accumulated
    normalized history to build the report-ready jeonse/wolse trend payload."""
    fetch_summary = molit_rent.fetch_and_store()

    return {
        "fetch_status": fetch_summary["status"],
        "fetch_note": fetch_summary.get("note"),
        "regions_covered": fetch_summary.get("regions_covered"),
        "regions_total": fetch_summary.get("regions_total"),
        "jeonse_tiers": {tier: _jeonse_tier_trend(tier) for tier in kr_regions.REGION_TIERS},
        "wolse_tiers": {tier: _wolse_tier_trend(tier) for tier in kr_regions.REGION_TIERS},
        "jeonse_highlight": _highlight_region(series_prefix=_JEONSE_PREFIX),
        "seoul_jeonse_district_movers": _district_movers(series_prefix=_JEONSE_PREFIX),
    }
