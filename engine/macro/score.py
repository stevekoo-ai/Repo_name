"""Macro scoring (Master Instruction 11.5, 11.6).

Two numbers come out of the Core-10 readings:
  - raw_score: simple Σ(indicator_score), range -10..+10 — used for the
    11.6 band lookup, per the instruction to keep the original band scale
    for the MVP rather than re-deriving bands for a weighted scale.
  - weighted_score: Σ(indicator_score × weight) per 11.5 — carried through
    as an auxiliary, more nuanced signal for confidence/regime/report use.
"""
from __future__ import annotations

from core.config import thresholds_config
from core.models import IndicatorReading


def compute_scores(readings: dict[str, IndicatorReading]) -> dict:
    scored = {k: r for k, r in readings.items() if r.score is not None}
    raw_score = sum(r.score for r in scored.values())
    weighted_score = sum(r.weighted_score() for r in scored.values())
    total = len(readings)
    return {
        "raw_score": raw_score,
        "weighted_score": round(weighted_score, 3),
        "scored_count": len(scored),
        "total_count": total,
        "coverage_pct": round(len(scored) / total * 100, 1) if total else 0.0,
    }


def score_band(raw_score: float) -> tuple[str, str]:
    """11.6 band lookup. Returns (band_key, korean_label)."""
    for key, spec in thresholds_config()["score_bands"].items():
        if spec["min"] <= raw_score <= spec["max"]:
            return key, spec["label_kr"]
    return "unclassified", "미분류"
