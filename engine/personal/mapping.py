"""Personal Economic Engine orchestrator (Master Instruction 13).

    Macro Result + Domain Scores + User Profile + User Assets + User Goals
    -> Personal Meaning Mapping -> Domain Recommendation -> Unified Action Plan

This module runs every domain engine (13.4-13.12) against the macro
payload and assembles the `personal` section of the report payload;
engine/action/engine.py then turns all of it into the Action Plan.
"""
from __future__ import annotations

from collectors import base as collector_base
from engine.semiconductor import score as semiconductor_score
from . import bond, calendar_engine, fx, housing, investment, portfolio_impact, travel


def _latest(series_id: str) -> float | None:
    df = collector_base.read_normalized(series_id)
    if df.empty:
        return None
    return float(df.sort_values("date")["value"].iloc[-1])


def run_personal_mapping(macro_payload: dict) -> dict:
    readings = macro_payload.get("readings", {})
    semi_exports_yoy = readings.get("semiconductor_exports", {}).get("fields", {}).get("yoy")
    cpi_yoy = readings.get("cpi", {}).get("fields", {}).get("yoy")

    semiconductor = semiconductor_score.compute_semiconductor_score(semi_exports_yoy)

    inv = investment.compute_investment_environment(macro_payload, semiconductor)
    etf_fit = investment.compute_etf_fit(
        inv["factors"]["macro_score_normalized"],
        semiconductor.get("semiconductor_score"),
        inv["factors"]["liquidity_rate_condition"],
        inv["factors"]["risk_penalty_inverse"],
    )

    base_rate = _latest("ecos_base_rate")
    bd = bond.compute_bond_score(macro_payload, base_rate=base_rate, cpi_yoy=cpi_yoy)

    fxr = fx.compute_fx_score()
    hs = housing.compute_housing_readiness()
    tr = travel.compute_travel_readiness(fxr.get("fx_score"))
    cal = calendar_engine.compute_calendar()
    asset_impact = portfolio_impact.compute_asset_impact(inv, semiconductor, bd, fxr, hs, etf_fit)

    return {
        "semiconductor": semiconductor,
        "investment": inv,
        "etf_fit": etf_fit,
        "bond": bd,
        "fx": fxr,
        "housing": hs,
        "travel": tr,
        "calendar": cal,
        "asset_impact": asset_impact,
    }
