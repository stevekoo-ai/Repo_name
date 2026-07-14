"""Macro Engine orchestrator (Master Instruction 11.2 execution order).

    Data Collection -> Normalization -> Indicator Calculation -> Trend
    Detection -> Rule Engine -> Score Engine -> Confidence Calculation ->
    Risk Detection -> Scenario Analysis(*) -> AI Report Payload

(*) Scenario analysis lives in engine/report/scenario.py since it also
needs domain-engine outputs, not just macro.
"""
from __future__ import annotations

from datetime import date

from core.logger import log_event
from . import change_detection, confidence, indicators, regime, score, snapshot, us_clock


def run_macro_engine(month_key: str | None = None) -> dict:
    month_key = month_key or f"{date.today().year:04d}-{date.today().month:02d}"

    readings = indicators.build_core10_readings()
    scores = score.compute_scores(readings)
    band_key, band_label = score.score_band(scores["raw_score"])

    history = snapshot.load_history(limit=6, before_month=month_key)
    previous_snapshot = history[-1] if history else None

    regime_result = regime.determine_regime(readings, scores["raw_score"], history)
    confidence_result = confidence.compute_confidence(
        readings, scores["raw_score"],
        previous_raw_score=(previous_snapshot or {}).get("macro", {}).get("scores", {}).get("raw_score"),
    )
    changes = change_detection.detect_changes(readings, previous_snapshot)
    investment_clock = us_clock.get_investment_clock_context()

    readings_payload = {
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

    payload = {
        "macro": {
            "regime": regime_result["regime"],
            "previous_regime": regime_result["previous_regime"],
            "transition": regime_result["transition"],
            "score_band": band_key,
            "score_band_label": band_label,
            "scores": scores,
            "confidence": confidence_result,
            "warnings_kr": regime_result["warnings_kr"],
            "downgrade_signals": regime_result["downgrade_signals"],
            "upgrade_signals": regime_result["upgrade_signals"],
            "changes": changes,
            "us_investment_clock": investment_clock,
            "readings": readings_payload,
        }
    }

    snapshot.save_snapshot(payload, month_key=month_key)
    log_event("macro_engine.completed", month=month_key, regime=regime_result["regime"],
              raw_score=scores["raw_score"], confidence=confidence_result["confidence"])
    return payload
