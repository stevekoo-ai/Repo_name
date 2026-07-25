"""Conflict Resolver (Master Instruction 15.6).

Category priority: liquidity_survival > macro_risk > industry_cycle >
investment_opportunity > travel_discretionary (config/rules.yaml
`conflict_resolver_priority`). Two concrete rules from 15.6 are applied
directly: a live liquidity need (housing funds, confirmed trip) suppresses
an "확대"(increase) investment action, and an unfavorable FX read never
cancels a confirmed trip — generators.from_fx_and_travel already turns
that into a split-conversion action rather than a hold, so here we just
make sure it doesn't get crowded out.
"""
from __future__ import annotations

from core.config import rules_config


def category_rank(category: str) -> int:
    order = rules_config()["conflict_resolver_priority"]
    return order.index(category) if category in order else len(order)


def resolve_conflicts(candidates: list[dict]) -> list[dict]:
    liquidity_active = any(c["category"] == "liquidity_survival" for c in candidates)

    for c in candidates:
        if liquidity_active and c["category"] == "investment_opportunity" and "확대" in c["title"]:
            c["conflict_note"] = (
                "유동성 우선 원칙(15.6) 적용 — 청약/필수자금 확보가 우선이며, "
                "공격적 매수 확대는 해당 자금 목표 달성 후 재검토한다."
            )
            c["factors"]["portfolio_impact"] = max(0, c["factors"]["portfolio_impact"] - 20)
        c["category_rank"] = category_rank(c["category"])

    return candidates
