"""Travel / Trip Engine (Master Instruction 13.10, 13.11).

    Trip Readiness Score (business) = 0.40*fx_favorability + 0.35*cost_risk_inverse
        + 0.25*lead_time_readiness
    Travel Timing Score (leisure)   = 0.50*fx_favorability + 0.30*season_favorability
        + 0.20*airfare_hotel_trend
"""
from __future__ import annotations

from datetime import date, datetime

from collectors import manual
from core.config import rules_config
from core.utils import clamp
from engine.scoring.weighted import log_score, weighted_sum_0_100

_PEAK_SEASON_MONTHS = {7, 8, 12, 1}  # heuristic: summer + year-end/new-year peak travel windows


def _lead_time_readiness(departure_date: str | None) -> float | None:
    if not departure_date:
        return None
    days_until = (datetime.fromisoformat(departure_date).date() - date.today()).days
    if days_until < 0:
        return None
    if days_until >= 60:
        return 80.0   # plenty of time to plan/exchange in tranches
    if days_until >= 21:
        return 60.0
    return 35.0        # short notice — less room to time the exchange


def _season_favorability(departure_date: str | None) -> float | None:
    if not departure_date:
        return None
    month = datetime.fromisoformat(departure_date).date().month
    return 35.0 if month in _PEAK_SEASON_MONTHS else 70.0  # off-peak -> cheaper/less crowded


def _cost_trend_score(signal: float | None) -> float | None:
    if signal is None:
        return None
    return clamp((signal + 1) / 2 * 100, 0.0, 100.0)


def _score_trip(trip: dict, fx_score: float | None) -> dict:
    is_business = trip.get("type") == "business"
    weights = rules_config()["travel"]["trip_readiness" if is_business else "travel_timing"]
    cost_score = _cost_trend_score(trip.get("cost_trend_signal"))

    if is_business:
        factors = {
            "fx_favorability": fx_score,
            "cost_risk_inverse": cost_score,
            "lead_time_readiness": _lead_time_readiness(trip.get("departure_date")),
        }
    else:
        factors = {
            "fx_favorability": fx_score,
            "season_favorability": _season_favorability(trip.get("departure_date")),
            "airfare_hotel_trend": cost_score,
        }

    score, breakdown = weighted_sum_0_100(factors, weights)
    trip_score = round(score, 1) if breakdown else None
    log_score("travel", trip.get("name", "trip"), score, breakdown)

    return {
        "name": trip.get("name"),
        "type": trip.get("type"),
        "destination_country": trip.get("destination_country"),
        "departure_date": trip.get("departure_date"),
        "score_kind": "trip_readiness" if is_business else "travel_timing",
        "score": trip_score,
        "factors": {k: (round(v, 1) if v is not None else None) for k, v in factors.items()},
        "data_status": "ok" if trip_score is not None else "pending",
    }


def compute_travel_readiness(fx_score: float | None) -> dict:
    trips = manual.fetch_trips()
    if not trips:
        return {"trips": [], "data_status": "pending", "note": "data/manual_inputs/trips.yaml 에 일정 없음"}
    scored = [_score_trip(t, fx_score) for t in trips]
    return {"trips": scored, "data_status": "ok"}
