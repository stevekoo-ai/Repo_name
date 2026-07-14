"""FX Engine (Master Instruction 13.7).

    FX Score = 0.35*usdkrw_trend + 0.25*dollar_index_trend
             + 0.25*kr_us_rate_differential + 0.15*us_rate_direction

FX Score here reads as "환전 유리도": how favorable *now* is to convert KRW
into foreign currency for an upcoming trip/travel (won relatively strong,
policy backdrop not pointing toward further won weakness). Trip/travel
readiness engines (13.10/13.11) consume this score directly.
"""
from __future__ import annotations

from collectors import base as collector_base
from core.config import rules_config
from core.utils import clamp
from engine.scoring.weighted import log_score, weighted_sum_0_100

_THREE_MONTH_ROWS_DAILY = 63
_THREE_MONTHS_MONTHLY = 3


def _favorability_from_pct_change(series_id: str, offset_rows: int, sensitivity: float = 5.0) -> tuple[float | None, float | None]:
    """Won-favorability score from a daily series' % change over `offset_rows` rows.
    Rising value (KRW weakening / DXY up) reduces favorability."""
    latest, prior = collector_base.series_change_over_rows(series_id, offset_rows)
    if latest is None or prior == 0:
        return None, None
    pct_change = (latest - prior) / abs(prior) * 100
    score = clamp(50 - pct_change * sensitivity, 0.0, 100.0)
    return score, round(pct_change, 2)


def _rate_differential_score() -> tuple[float | None, float | None]:
    kr_df = collector_base.read_normalized("ecos_base_rate")
    us_df = collector_base.read_normalized("fred_us_fed_funds_rate")
    if kr_df.empty or us_df.empty:
        return None, None
    kr_rate = kr_df.sort_values("date")["value"].iloc[-1]
    us_rate = us_df.sort_values("date")["value"].iloc[-1]
    differential = kr_rate - us_rate
    score = clamp(50 + differential * 20, 0.0, 100.0)  # more negative differential -> less favorable
    return score, round(differential, 2)


def _us_rate_direction_score() -> tuple[float | None, float | None]:
    latest, prior = collector_base.series_change_over_rows("fred_us_fed_funds_rate", _THREE_MONTHS_MONTHLY)
    if latest is None:
        return None, None
    change_bp = (latest - prior) * 100
    score = clamp(50 - change_bp / 2, 0.0, 100.0)  # US cutting -> favorable for KRW
    return score, round(change_bp, 1)


def compute_fx_score() -> dict:
    weights = rules_config()["fx"]

    usdkrw_score, usdkrw_pct = _favorability_from_pct_change("ecos_usdkrw", _THREE_MONTH_ROWS_DAILY)
    dxy_score, dxy_pct = _favorability_from_pct_change("fred_us_dollar_index", _THREE_MONTH_ROWS_DAILY)
    differential_score, differential = _rate_differential_score()
    us_rate_score, us_rate_bp = _us_rate_direction_score()

    factors = {
        "usdkrw_trend": usdkrw_score,
        "dollar_index_trend": dxy_score,
        "kr_us_rate_differential": differential_score,
        "us_rate_direction": us_rate_score,
    }
    score, breakdown = weighted_sum_0_100(factors, weights)
    fx_score = round(score, 1) if breakdown else None
    log_score("fx", "fx_score", score, breakdown)

    return {
        "fx_score": fx_score,
        "factors": {k: (round(v, 1) if v is not None else None) for k, v in factors.items()},
        "detail": {
            "usdkrw_change_pct_3m": usdkrw_pct,
            "dollar_index_change_pct_3m": dxy_pct,
            "kr_us_rate_differential_pct": differential,
            "us_fed_funds_change_bp_3m": us_rate_bp,
        },
        "data_status": "ok" if fx_score is not None else "pending",
    }
