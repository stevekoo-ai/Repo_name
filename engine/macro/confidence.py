"""Macro confidence score (Master Instruction 11.11).

    Confidence = 0.30*freshness + 0.25*source_quality
               + 0.25*indicator_consistency + 0.20*trend_stability

The instruction specifies the four weights but not each sub-factor's exact
formula ("각 하위 요인은 0~100으로 표준화"), so the definitions below are a
documented, deterministic heuristic — calibrate the weights in
config/rules.yaml `confidence.weights`; the sub-factor formulas themselves
are intentionally simple and named so they're easy to audit/replace.
"""
from __future__ import annotations

from core.config import rules_config
from core.models import DataStatus, IndicatorReading
from core.utils import clamp

# Fallback reliability grade (1-5) by source label, used when a reading's
# collector didn't surface reliability_grade explicitly (7.2 grades).
SOURCE_RELIABILITY_GRADE = {
    "한국은행 ECOS": 5,
    "통계청 KOSIS": 5,
    "FRED": 5,
    "산업통상자원부 (수동 입력)": 5,
    "기업 IR / TrendForce / 산업 리서치 (수동 입력)": 3,
}


def _freshness(readings: dict[str, IndicatorReading]) -> float:
    if not readings:
        return 0.0
    ok = sum(1 for r in readings.values() if r.status == DataStatus.OK)
    return ok / len(readings) * 100


def _source_quality(readings: dict[str, IndicatorReading]) -> float:
    scored = [r for r in readings.values() if r.status == DataStatus.OK]
    if not scored:
        return 0.0
    grades = [SOURCE_RELIABILITY_GRADE.get(r.source, 4) for r in scored]
    return sum(grades) / len(grades) / 5 * 100


def _indicator_consistency(readings: dict[str, IndicatorReading], raw_score: float) -> float:
    scored = [r for r in readings.values() if r.score is not None]
    if not scored:
        return 0.0
    majority_sign = 1 if raw_score > 0 else (-1 if raw_score < 0 else 0)
    agree = sum(1 for r in scored if (r.score == 0) or (majority_sign == 0) or (r.score == majority_sign))
    return agree / len(scored) * 100


def _trend_stability(raw_score: float, previous_raw_score: float | None) -> float:
    if previous_raw_score is None:
        return 70.0  # no history yet — neutral default, not a guess about direction
    delta = abs(raw_score - previous_raw_score)
    return clamp(100 - delta * 10, 0.0, 100.0)


def compute_confidence(readings: dict[str, IndicatorReading], raw_score: float,
                        previous_raw_score: float | None) -> dict:
    weights = rules_config()["confidence"]["weights"]
    freshness = _freshness(readings)
    source_quality = _source_quality(readings)
    consistency = _indicator_consistency(readings, raw_score)
    stability = _trend_stability(raw_score, previous_raw_score)

    confidence = (
        weights["data_freshness"] * freshness
        + weights["source_quality"] * source_quality
        + weights["indicator_consistency"] * consistency
        + weights["trend_stability"] * stability
    )
    return {
        "confidence": round(clamp(confidence, 0.0, 100.0), 1),
        "components": {
            "data_freshness": round(freshness, 1),
            "source_quality": round(source_quality, 1),
            "indicator_consistency": round(consistency, 1),
            "trend_stability": round(stability, 1),
        },
    }
