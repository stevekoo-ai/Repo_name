"""Structured report payload builder (Master Instruction 20).

Runs the full pipeline (Macro -> Personal/Domain -> Action -> Scenario)
and assembles one JSON-serializable dict that both the Markdown renderer
(engine/report/markdown.py) and any future PDF/Excel exporter consume —
scoring logic and narrative rendering stay fully separate (24.1).
"""
from __future__ import annotations

from datetime import date

from core.config import thresholds_config
from core.logger import log_event
from core.models import DataStatus
from engine.action import engine as action_engine
from engine.macro import engine as macro_engine
from engine.macro import snapshot as macro_snapshot
from engine.personal import mapping
from . import scenario as scenario_mod

INDICATOR_ORDER = [
    "gdp", "industrial_production", "retail_sales", "exports", "semiconductor_exports",
    "current_account", "cpi", "ppi", "unemployment", "us_global",
]

TREND_ARROWS = {1: "▲", 0: "→", -1: "▼"}


def _report_readiness(coverage_pct: float, core10_complete: bool) -> str:
    cfg = thresholds_config()["report_readiness"]
    if core10_complete and cfg["final_report_requires_core10_complete"]:
        return "final"
    if coverage_pct >= cfg["draft_report_min_coverage_pct"]:
        return "draft"
    return "insufficient"


def _macro_dashboard(macro: dict, previous_macro: dict | None) -> list[dict]:
    rows = []
    prev_readings = (previous_macro or {}).get("readings", {})
    for key in INDICATOR_ORDER:
        r = macro["readings"].get(key, {})
        prev = prev_readings.get(key, {})
        rows.append({
            "indicator": r.get("label", key),
            "current": r.get("value"),
            "previous": prev.get("value"),
            "trend": TREND_ARROWS.get(r.get("score"), "N/A") if r.get("status") == "ok" else "N/A",
            "score": r.get("score"),
            "status": r.get("status"),
            "source": r.get("source"),
        })
    return rows


def _executive_brief(macro: dict, personal: dict, actions: list[dict]) -> dict:
    asset_summary = {k: v["stars"] for k, v in personal["asset_impact"].items()}
    top_events = [f"{e['name']} ({e['date']})" for e in personal["calendar"][:5]]
    top_action = actions[0] if actions else None

    diagnosis = (
        f"{macro['regime']} 국면(총점 {macro['scores']['raw_score']}, "
        f"신뢰도 {macro['confidence']['confidence']}점) — "
        f"반도체 {personal['semiconductor'].get('status_label_kr', '미분류')}"
    )

    return {
        "one_line_diagnosis": diagnosis,
        "asset_summary": asset_summary,
        "top_events": top_events,
        "final_suggestion": top_action["title"] if top_action else "핵심 지표 확보 후 재평가가 필요합니다.",
    }


def _appendix(macro: dict) -> dict:
    sources = sorted({
        r.get("source") for r in macro["readings"].values() if r.get("source")
    })
    return {
        "sources": sources,
        "glossary": {
            "Regime": "경기 국면 — Recovery/Early Expansion/Expansion/Late Expansion/Slowdown/Recession 순환.",
            "Confidence": "판정 신뢰도(0-100) — 데이터 최신성/출처 품질/지표 일관성/추세 안정성 가중합.",
            "Investment Environment Score": "거시+반도체+유동성+리스크를 종합한 투자 환경 점수(0-100).",
        },
        "previous_month_regime": macro.get("previous_regime"),
    }


def build_report_payload(month_key: str | None = None) -> dict:
    month_key = month_key or f"{date.today().year:04d}-{date.today().month:02d}"

    macro_result = macro_engine.run_macro_engine(month_key=month_key)
    macro = macro_result["macro"]
    previous_snapshot = macro_snapshot.previous_snapshot(before_month=month_key)
    previous_macro = (previous_snapshot or {}).get("macro")

    personal = mapping.run_personal_mapping(macro)
    actions = action_engine.build_action_plan(
        macro, personal["semiconductor"], personal["investment"], personal["bond"],
        personal["fx"], personal["housing"], personal["travel"], personal["calendar"],
    )
    scenarios = scenario_mod.compute_scenarios(macro, personal["semiconductor"], personal["investment"])

    core10_complete = all(
        r.get("status") == DataStatus.OK.value for r in macro["readings"].values()
    )
    readiness = _report_readiness(macro["scores"]["coverage_pct"], core10_complete)

    payload = {
        "report_month": month_key,
        "report_readiness": readiness,
        "macro": {
            "regime": macro["regime"],
            "previous_regime": macro["previous_regime"],
            "transition": macro["transition"],
            "score": macro["scores"]["raw_score"],
            "weighted_score": macro["scores"]["weighted_score"],
            "score_band": macro["score_band"],
            "score_band_label": macro["score_band_label"],
            "confidence": macro["confidence"]["confidence"],
            "confidence_components": macro["confidence"]["components"],
            "warnings": macro["warnings_kr"],
            "changes": macro["changes"],
            "us_investment_clock": macro["us_investment_clock"],
        },
        "macro_dashboard": _macro_dashboard(macro, previous_macro),
        "personal": {
            "investment_environment_score": personal["investment"].get("investment_environment_score"),
            "investment_biases": personal["investment"].get("biases"),
            "semiconductor_score": personal["semiconductor"].get("semiconductor_score"),
            "semiconductor_band": personal["semiconductor"].get("status_label_kr"),
            "bond_score": personal["bond"].get("bond_score"),
            "fx_score": personal["fx"].get("fx_score"),
            "housing_readiness_score": (
                round(sum(n["readiness_score"] for n in personal["housing"]["notices"] if n.get("readiness_score") is not None)
                      / max(1, len([n for n in personal["housing"]["notices"] if n.get("readiness_score") is not None])), 1)
                if personal["housing"].get("notices") else None
            ),
            "etf_fit": personal["etf_fit"],
        },
        "assets": personal["asset_impact"],
        "housing": personal["housing"],
        "travel": personal["travel"],
        "scenarios": scenarios,
        "actions": actions,
        "calendar": personal["calendar"],
        "personal_executive_brief": _executive_brief(macro, personal, actions),
        "appendix": _appendix(macro),
    }

    log_event("report_payload.built", month=month_key, readiness=readiness, action_count=len(actions))
    return payload
