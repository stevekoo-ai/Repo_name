"""Bond Engine (Master Instruction 13.6).

    Bond Score = 0.40*rate_direction + 0.25*real_rate_attractiveness
               + 0.20*inflation_slowdown_signal + 0.15*growth_slowdown_signal
"""
from __future__ import annotations

from core.config import rules_config
from engine.scoring.weighted import log_score, weighted_sum_0_100
from . import market_conditions


def _inflation_slowdown_score(macro_payload: dict) -> float | None:
    changes = macro_payload.get("changes", [])
    cpi_improve = any(c["indicator"] == "cpi" and c["direction"] == "improve" for c in changes)
    ppi_improve = any(c["indicator"] == "ppi" and c["direction"] == "improve" for c in changes)
    if cpi_improve and ppi_improve:
        return 90.0
    if cpi_improve or ppi_improve:
        return 65.0

    downgrade_signals = macro_payload.get("downgrade_signals", [])
    if "cpi_reaccelerating" in downgrade_signals or "ppi_sustained_high" in downgrade_signals:
        return 20.0
    return None  # no clear signal either way — Pending, not a guessed neutral


def compute_bond_score(macro_payload: dict, base_rate: float | None, cpi_yoy: float | None) -> dict:
    weights = rules_config()["bond"]

    rate_score, rate_detail = market_conditions.rate_direction_score()
    real_score, real_detail = market_conditions.real_rate_score(base_rate, cpi_yoy)
    inflation_score = _inflation_slowdown_score(macro_payload)
    macro_norm = market_conditions.macro_score_normalized(macro_payload)
    growth_slowdown_score = (100 - macro_norm) if macro_norm is not None else None

    factors = {
        "rate_direction": rate_score,
        "real_rate_attractiveness": real_score,
        "inflation_slowdown_signal": inflation_score,
        "growth_slowdown_signal": growth_slowdown_score,
    }
    score, breakdown = weighted_sum_0_100(factors, weights)
    bond_score = round(score, 1) if breakdown else None
    log_score("bond", "bond_score", score, breakdown)

    return {
        "bond_score": bond_score,
        "factors": {k: (round(v, 1) if v is not None else None) for k, v in factors.items()},
        "detail": {**rate_detail, **real_detail},
        "data_status": "ok" if bond_score is not None else "pending",
    }
