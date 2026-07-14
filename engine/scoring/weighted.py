"""Generic weighted-sum scoring, reused by every domain engine (12.4-13.12, 15.3).

Every domain score in the Master Instruction has the same shape: a
dict of named sub-factors in some bounded range, combined with weights
from config/rules.yaml that sum to 1.0. Centralizing the combination
logic here means each domain engine only supplies factor values, not
its own arithmetic.
"""
from __future__ import annotations

from core.logger import log_event
from core.utils import clamp


def weighted_sum(factors: dict[str, float | None], weights: dict[str, float],
                  missing_policy: str = "renormalize") -> tuple[float, dict[str, float]]:
    """Combine sub-factors into one score using the configured weights.

    Factors that are None (Pending data) are excluded; remaining weights
    are renormalized to sum to 1 (missing_policy="renormalize") so a single
    missing input doesn't silently zero out the composite — the caller
    still sees which factors were actually used via the returned breakdown.
    """
    usable = {k: v for k, v in factors.items() if v is not None and k in weights}
    if not usable:
        return 0.0, {}

    if missing_policy == "renormalize":
        total_weight = sum(weights[k] for k in usable)
        if total_weight <= 0:
            return 0.0, {}
        norm_weights = {k: weights[k] / total_weight for k in usable}
    else:
        norm_weights = {k: weights[k] for k in usable}

    breakdown = {k: usable[k] * norm_weights[k] for k in usable}
    score = sum(breakdown.values())
    return score, breakdown


def weighted_sum_0_100(factors_0_100: dict[str, float | None], weights: dict[str, float]) -> tuple[float, dict[str, float]]:
    """Same as weighted_sum but clamps the final composite into [0, 100] (12.3, 13.4-13.8 all use 0-100 scores)."""
    score, breakdown = weighted_sum(factors_0_100, weights)
    return clamp(score, 0.0, 100.0), breakdown


def log_score(engine: str, target: str, score: float, breakdown: dict[str, float]) -> None:
    log_event("score.computed", engine=engine, target=target, score=round(score, 2),
               breakdown={k: round(v, 2) for k, v in breakdown.items()})
