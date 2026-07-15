"""Macro Engine orchestrator (Master Instruction 11.2 execution order).

    Data Collection -> Normalization -> Indicator Calculation -> Trend
    Detection -> Rule Engine -> Score Engine -> Confidence Calculation ->
    Risk Detection -> Scenario Analysis(*) -> AI Report Payload

Runs the US Macro Core first, then KR Core-10, then compares them — per the
user's explicit request to read the "big picture" (US regime) before
judging whether Korea is riding that wave or diverging from it, rather than
scoring Korea in isolation. The KR block ('macro') remains the one that
drives personal/asset decisions downstream; US ('macro_us') and the
comparison are context, not a second decision engine.

(*) Scenario analysis lives in engine/report/scenario.py since it also
needs domain-engine outputs, not just macro.
"""
from __future__ import annotations

from datetime import date

from core.logger import log_event
from core.models import IndicatorReading
from . import change_detection, comparison, confidence, indicators, indicators_us, regime, regime_us, score, snapshot, us_clock


def _readings_payload(readings: dict[str, IndicatorReading]) -> dict:
    return {
        key: {
            "value": r.value,
            "score": r.score,
            "weight": r.weight,
            "status": r.status.value,
            "label": r.label,
            "source": r.source,
            "fields": r.detail.get("fields", {}),
            "note": r.detail.get("note"),
        }
        for key, r in readings.items()
    }


def _run_market(
    *, readings: dict[str, IndicatorReading], history: list[dict], snapshot_key: str,
    determine_regime_fn, change_detect_fn, previous_snapshot: dict | None,
) -> dict:
    scores = score.compute_scores(readings)
    band_key, band_label = score.score_band(scores["raw_score"])
    regime_result = determine_regime_fn(readings, scores["raw_score"], history)
    confidence_result = confidence.compute_confidence(
        readings, scores["raw_score"],
        previous_raw_score=(previous_snapshot or {}).get(snapshot_key, {}).get("scores", {}).get("raw_score"),
    )
    changes = change_detect_fn(readings, previous_snapshot)

    return {
        "regime": regime_result["regime"],
        "previous_regime": regime_result["previous_regime"],
        "transition": regime_result["transition"],
        "score_band": band_key,
        "score_band_label": band_label,
        "scores": scores,
        "confidence": confidence_result,
        "warning_active": regime_result["warning_active"],
        "warnings_kr": regime_result["warnings_kr"],
        "downgrade_signals": regime_result["downgrade_signals"],
        "upgrade_signals": regime_result["upgrade_signals"],
        "changes": changes,
        "readings": _readings_payload(readings),
    }


def run_macro_engine(month_key: str | None = None) -> dict:
    month_key = month_key or f"{date.today().year:04d}-{date.today().month:02d}"

    history = snapshot.load_history(limit=6, before_month=month_key)
    previous_snapshot = history[-1] if history else None

    us_readings = indicators_us.build_us_core_readings()
    us_macro = _run_market(
        readings=us_readings, history=history, snapshot_key="macro_us",
        determine_regime_fn=regime_us.determine_regime_us,
        change_detect_fn=change_detection.detect_changes_us,
        previous_snapshot=previous_snapshot,
    )

    kr_readings = indicators.build_core10_readings()
    kr_macro = _run_market(
        readings=kr_readings, history=history, snapshot_key="macro",
        determine_regime_fn=regime.determine_regime,
        change_detect_fn=change_detection.detect_changes,
        previous_snapshot=previous_snapshot,
    )
    kr_macro["us_investment_clock"] = us_clock.get_investment_clock_context()

    kr_us_comparison = comparison.compare_kr_us(kr_macro, us_macro)

    payload = {
        "macro": kr_macro,
        "macro_us": us_macro,
        "kr_us_comparison": kr_us_comparison,
    }

    snapshot.save_snapshot(payload, month_key=month_key)
    log_event("macro_engine.completed", month=month_key,
              regime=kr_macro["regime"], raw_score=kr_macro["scores"]["raw_score"],
              confidence=kr_macro["confidence"]["confidence"],
              us_regime=us_macro["regime"], us_raw_score=us_macro["scores"]["raw_score"])
    return payload
