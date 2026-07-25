"""Action Engine orchestrator (Master Instruction 15).

Collects candidates from every domain engine's output, scores each with
the 15.3 Action Priority Score formula, resolves cross-category conflicts
(15.6), and returns a ranked, human-readable action list — the page every
other engine ultimately exists to feed (2.2 절대 원칙 5: 모든 출력은
행동으로 끝나야 한다).
"""
from __future__ import annotations

from core.config import rules_config
from core.logger import log_event
from engine.scoring.weighted import weighted_sum_0_100
from . import conflict, generators


def priority_grade(score: float) -> int:
    """15.4 grade bands — same 85/70/55/40 thresholds used throughout PEOS."""
    if score >= 85:
        return 5
    if score >= 70:
        return 4
    if score >= 55:
        return 3
    if score >= 40:
        return 2
    return 1


GRADE_LABEL_KR = {
    5: "★★★★★ 반드시 확인 / 반드시 실행",
    4: "★★★★☆ 검토 필요",
    3: "★★★☆☆ 관찰 필요",
    2: "★★☆☆☆ 참고",
    1: "보류",
}


def build_action_plan(macro_payload: dict, semiconductor: dict, investment: dict, bond: dict,
                       fx: dict, housing: dict, travel: dict, calendar_events: list[dict]) -> list[dict]:
    weights = rules_config()["action_priority"]

    candidates: list[dict] = []
    candidates += generators.from_macro_warnings(macro_payload)
    candidates += generators.from_semiconductor(semiconductor)
    candidates += generators.from_investment(investment)
    candidates += generators.from_bond(bond)
    candidates += generators.from_fx_and_travel(fx, travel)
    candidates += generators.from_housing(housing)
    candidates += generators.from_calendar(calendar_events)

    candidates = conflict.resolve_conflicts(candidates)

    actions = []
    for c in candidates:
        score, breakdown = weighted_sum_0_100(c["factors"], weights)
        grade = priority_grade(score)
        actions.append({
            "priority": grade,
            "priority_label": GRADE_LABEL_KR[grade],
            "priority_score": round(score, 1),
            "title": c["title"],
            "reason": c["reason"],
            "invalid_condition": c["invalid_condition"],
            "recheck": c["recheck"],
            "category": c["category"],
            "conflict_note": c.get("conflict_note"),
        })

    actions.sort(key=lambda a: (-a["priority_score"], conflict.category_rank(a["category"])))
    log_event("action_engine.completed", action_count=len(actions))
    return actions
