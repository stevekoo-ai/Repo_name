"""Shared rate/liquidity sub-scores reused by the Investment and Bond engines
(Master Instruction 13.4, 13.6) so the two engines agree on what "rates are
easing" means instead of each re-deriving it.

Both functions return (score_0_100 | None, detail_dict). None means the
underlying series isn't available yet (Pending) — callers must not treat
None as 0/unfavorable.
"""
from __future__ import annotations

from collectors import base as collector_base
from core.utils import clamp

_THREE_MONTH_ROWS = 63  # ~3 trading months of daily ECOS data


def rate_direction_score() -> tuple[float | None, dict]:
    """0-100, higher = rates easing over the last ~3 months (favorable for bonds/liquidity, 13.6)."""
    latest, prior = collector_base.series_change_over_rows("ecos_kr_3y_yield", _THREE_MONTH_ROWS)
    if latest is None:
        return None, {}
    change_bp = (latest - prior) * 100
    score = clamp(50 - change_bp / 2, 0.0, 100.0)  # -100bp -> 100 (very favorable), +100bp -> 0
    return score, {"kr_3y_yield_change_bp_3m": round(change_bp, 1)}


def real_rate_score(base_rate: float | None, cpi_yoy: float | None) -> tuple[float | None, dict]:
    """0-100, higher real policy rate = more attractive for bond buyers (13.6)."""
    if base_rate is None or cpi_yoy is None:
        return None, {}
    real_rate = base_rate - cpi_yoy
    score = clamp(50 + real_rate * 25, 0.0, 100.0)  # 0% real -> 50, +2% -> 100, -2% -> 0
    return score, {"real_rate_pct": round(real_rate, 2)}


def macro_score_normalized(macro_payload: dict) -> float | None:
    """Rescale the Core-10 raw score (-10..+10) to 0-100. Shared by Investment and Bond engines."""
    scores = macro_payload.get("scores", {})
    if not scores.get("scored_count"):
        return None
    return clamp((scores["raw_score"] + 10) / 20 * 100, 0.0, 100.0)
