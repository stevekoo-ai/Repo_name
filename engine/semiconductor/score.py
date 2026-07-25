"""Semiconductor Engine (Master Instruction 12).

Combines the manual signal snapshot (data/manual_inputs/semiconductor.yaml,
7.3 exception policy) with the official 반도체 수출 YoY indicator into
Memory Cycle / AI Infrastructure / Semiconductor composite scores (12.4).
"""
from __future__ import annotations

from collectors import manual
from core.config import rules_config, thresholds_config
from core.models import DataStatus
from core.utils import clamp
from engine.scoring.weighted import log_score, weighted_sum_0_100


def _signal_to_100(x: float | None) -> float | None:
    """Manual signals are analyst-normalized to [-1, 1]; rescale to [0, 100]."""
    if x is None:
        return None
    return clamp((x + 1) / 2 * 100, 0.0, 100.0)


def _yoy_to_100(yoy: float | None, center: float = 0.0, scale: float = 1.5) -> float | None:
    """Heuristic YoY% -> 0-100 rescaling: 0% YoY -> 50, +/-33pp -> +/-50 from center."""
    if yoy is None:
        return None
    return clamp(50 + (yoy - center) * scale, 0.0, 100.0)


def status_band(score_0_100: float) -> str:
    """Bands are matched by `min` only (highest qualifying min wins) so a
    continuous float score never falls into a gap between two integer-
    boundaried YAML bands (e.g. 79.6 between "positive" max:79 and
    "strong_positive" min:80)."""
    bands = thresholds_config()["semiconductor_bands"]
    ranked = sorted(bands.items(), key=lambda kv: kv[1]["min"], reverse=True)
    for key, spec in ranked:
        if score_0_100 >= spec["min"]:
            return key
    return "unclassified"


STATUS_LABEL_KR = {
    "strong_positive": "강한 긍정",
    "positive": "긍정",
    "neutral_plus": "중립+",
    "cautious": "주의",
    "weak_risk": "약세/위험",
    "unclassified": "미분류",
}


def compute_semiconductor_score(semiconductor_exports_yoy: float | None) -> dict:
    weights = rules_config()["semiconductor"]
    signals = manual.get_semiconductor_signal_dict() or {}

    memory_factors = {
        "dram_price_trend": _signal_to_100(signals.get("dram_price_trend")),
        "nand_price_trend": _signal_to_100(signals.get("nand_price_trend")),
        "semiconductor_exports": _yoy_to_100(semiconductor_exports_yoy),
        "guidance_signal": _signal_to_100(signals.get("guidance_signal")),
        "inventory_supply_signal": _signal_to_100(signals.get("inventory_supply_signal")),
    }
    memory_cycle_score, memory_breakdown = weighted_sum_0_100(memory_factors, weights["memory_cycle_score"])

    ai_factors = {
        "ai_leader_earnings": _signal_to_100(signals.get("ai_leader_earnings")),
        "gpu_shipment": _signal_to_100(signals.get("gpu_shipment")),
        "ai_server_shipment": _signal_to_100(signals.get("ai_server_shipment")),
        "csp_capex": _signal_to_100(signals.get("csp_capex")),
        "hbm_signal": _signal_to_100(signals.get("hbm_signal")),
    }
    ai_infra_score, ai_breakdown = weighted_sum_0_100(ai_factors, weights["ai_infrastructure_score"])

    composite_factors = {
        "memory_cycle_score": memory_cycle_score if memory_breakdown else None,
        "ai_infrastructure_score": ai_infra_score if ai_breakdown else None,
        "kr_semiconductor_export_trend": _yoy_to_100(semiconductor_exports_yoy),
    }
    semiconductor_score, semi_breakdown = weighted_sum_0_100(composite_factors, weights["semiconductor_score"])

    band = status_band(semiconductor_score) if semi_breakdown else "unclassified"
    log_score("semiconductor", "semiconductor_score", semiconductor_score, semi_breakdown)

    return {
        "memory_cycle_score": round(memory_cycle_score, 1) if memory_breakdown else None,
        "ai_infrastructure_score": round(ai_infra_score, 1) if ai_breakdown else None,
        "semiconductor_score": round(semiconductor_score, 1) if semi_breakdown else None,
        "status_band": band,
        "status_label_kr": STATUS_LABEL_KR.get(band, band),
        "breakdown": {
            "memory_cycle": {k: round(v, 1) for k, v in memory_breakdown.items()},
            "ai_infrastructure": {k: round(v, 1) for k, v in ai_breakdown.items()},
            "semiconductor": {k: round(v, 1) for k, v in semi_breakdown.items()},
        },
        "data_status": "ok" if semi_breakdown else "pending",
    }
