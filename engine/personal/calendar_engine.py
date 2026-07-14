"""Economic Calendar Engine (Master Instruction 13.12, 16.12).

    priority = 0.30*user_relevance + 0.25*market_impact + 0.20*industry_impact
             + 0.15*time_urgency + 0.10*portfolio_impact

Only 3 importance tiers are used for calendar events (vs. the 5-tier scale
used elsewhere) per 13.12's explicit ★★★★★/★★★★☆/★★★☆☆ output grades.
"""
from __future__ import annotations

from datetime import date, datetime

from collectors import manual
from core.config import rules_config
from core.utils import clamp
from engine.scoring.weighted import log_score, weighted_sum_0_100


def _time_urgency(event_date: str) -> float:
    days_until = (datetime.fromisoformat(event_date).date() - date.today()).days
    return clamp(100 - days_until * 2.5, 0.0, 100.0)


def _importance_tier(score: float) -> int:
    if score >= 80:
        return 5
    if score >= 60:
        return 4
    return 3


def compute_calendar(horizon_days: int = 45) -> list[dict]:
    weights = rules_config()["calendar_priority"]
    events = manual.fetch_calendar_events()
    today = date.today()

    results = []
    for ev in events:
        event_date = datetime.fromisoformat(ev["date"]).date()
        days_until = (event_date - today).days
        if days_until < 0 or days_until > horizon_days:
            continue

        factors = {
            "user_relevance": ev.get("user_relevance"),
            "market_impact": ev.get("market_impact"),
            "industry_impact": ev.get("industry_impact"),
            "time_urgency": _time_urgency(ev["date"]),
            "portfolio_impact": ev.get("portfolio_impact"),
        }
        score, breakdown = weighted_sum_0_100(factors, weights)
        priority_score = round(score, 1) if breakdown else None
        log_score("calendar", ev["name"], score, breakdown)

        tier = _importance_tier(priority_score) if priority_score is not None else 3
        results.append({
            "name": ev["name"],
            "date": ev["date"],
            "category": ev.get("category"),
            "days_until": days_until,
            "priority_score": priority_score,
            "importance_tier": tier,
            "importance_label": "★" * tier + "☆" * (5 - tier),
        })

    return sorted(results, key=lambda r: (-r["priority_score"] if r["priority_score"] is not None else 0, r["days_until"]))
