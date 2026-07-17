"""Structured report payload builder (Master Instruction 20).

Runs the full pipeline (Macro -> Personal/Domain -> Action -> Scenario)
and assembles one JSON-serializable dict that both the Markdown renderer
(engine/report/markdown.py) and any future PDF/Excel exporter consume —
scoring logic and narrative rendering stay fully separate (24.1).
"""
from __future__ import annotations

from datetime import date

from collectors import base as collector_base
from core.config import report_config, thresholds_config
from core.logger import log_event
from core.models import DataStatus
from engine.action import engine as action_engine
from engine.macro import engine as macro_engine
from engine.macro import snapshot as macro_snapshot
from engine.personal import mapping
from engine.rate_analysis import scoring as rate_scoring
from engine.crisis_analysis import scoring as cci_scoring
from engine.real_estate import market_trend as real_estate_trend
from . import discussion as discussion_mod
from . import scenario as scenario_mod

INDICATOR_ORDER = [
    "gdp", "industrial_production", "retail_sales", "exports", "semiconductor_exports",
    "current_account", "cpi", "ppi", "unemployment", "us_global",
]

# Which normalized-tier series (collectors/base.py) backs each Core-10 indicator's
# raw value, for trend sparklines and a previous-period fallback that doesn't
# depend on a prior monthly PEOS snapshot existing (engine/macro/indicators.py
# is the source of truth for these series ids — kept in sync manually since it's
# a display-only concern, not a scoring one). us_global has no single backing
# series (it's a composite of several FRED series) so it's left out of both.
SERIES_FOR_INDICATOR = {
    "gdp": "ecos_gdp_growth_qoq",
    "industrial_production": "kosis_industrial_production_index",
    "retail_sales": "kosis_retail_sales_index",
    "exports": "motie_total_exports_yoy",
    "semiconductor_exports": "motie_semiconductor_exports_yoy",
    "current_account": "ecos_current_account",
    "cpi": "kosis_cpi_index",
    "ppi": "ecos_ppi_yoy_level",
    "unemployment": "kosis_unemployment_rate",
}

# engine/macro/indicators.py falls back to an OECD-via-FRED mirror when the
# matching KOSIS series is unreachable — when that happens the fresh data
# lives under this series id instead, so the sparkline should look here too.
FALLBACK_SERIES_FOR_INDICATOR = {
    "industrial_production": "fred_kr_industrial_production_oecd",
    "retail_sales": "fred_kr_retail_sales_mom_oecd",
    "cpi": "fred_kr_cpi_oecd",
    "unemployment": "fred_kr_unemployment_oecd",
}

US_INDICATOR_ORDER = [
    "gdp", "industrial_production", "retail_sales", "cpi", "ppi", "unemployment",
    "trade_balance", "yield_curve",
]

US_SERIES_FOR_INDICATOR = {
    "gdp": "fred_us_gdp_qoq",
    "industrial_production": "fred_us_industrial_production",
    "retail_sales": "fred_us_retail_sales",
    "cpi": "fred_us_cpi",
    "ppi": "fred_us_ppi",
    "unemployment": "fred_us_unemployment",
    "trade_balance": "fred_us_trade_balance",
    "yield_curve": "fred_us_yield_curve_10y2y",
}

TREND_ARROWS = {1: "▲", 0: "→", -1: "▼"}


def _series_history_and_prev(series_id: str, years: int) -> tuple[list[dict], float | None]:
    """Long-window history for a sparkline, plus the value one period back —
    read straight from the raw normalized series so both are available on day
    one, before a second monthly PEOS snapshot exists to diff against."""
    df = collector_base.read_normalized(series_id)
    if df.empty:
        return [], None
    df = df.sort_values("date")
    cutoff = date.today().replace(year=date.today().year - years)
    hist_df = df[df["date"] >= cutoff]
    history = [{"date": str(row.date), "value": float(row.value)} for row in hist_df.itertuples()
               if row.value == row.value]  # drop NaN
    prev_value = float(df["value"].iloc[-2]) if len(df) >= 2 else None
    return history, prev_value


def _report_readiness(coverage_pct: float, core10_complete: bool) -> str:
    cfg = thresholds_config()["report_readiness"]
    if core10_complete and cfg["final_report_requires_core10_complete"]:
        return "final"
    if coverage_pct >= cfg["draft_report_min_coverage_pct"]:
        return "draft"
    return "insufficient"


def _macro_dashboard(macro: dict, previous_macro: dict | None, indicator_order: list[str] | None = None,
                      series_for_indicator: dict[str, str] | None = None) -> list[dict]:
    indicator_order = indicator_order if indicator_order is not None else INDICATOR_ORDER
    series_for_indicator = series_for_indicator if series_for_indicator is not None else SERIES_FOR_INDICATOR
    years = report_config().get("trend_history_years", 10)
    rows = []
    prev_readings = (previous_macro or {}).get("readings", {})
    for key in indicator_order:
        r = macro["readings"].get(key, {})
        prev = prev_readings.get(key, {})

        series_id = series_for_indicator.get(key)
        history: list[dict] = []
        series_prev_value = None
        if series_id:
            history, series_prev_value = _series_history_and_prev(series_id, years)
        if not history and key in FALLBACK_SERIES_FOR_INDICATOR:
            history, series_prev_value = _series_history_and_prev(FALLBACK_SERIES_FOR_INDICATOR[key], years)

        previous_value = prev.get("value")
        previous_source = "snapshot" if previous_value is not None else None
        if previous_value is None and series_prev_value is not None:
            previous_value = series_prev_value
            previous_source = "series_history"

        rows.append({
            "key": key,
            "indicator": r.get("label", key),
            "current": r.get("value"),
            "previous": previous_value,
            "previous_source": previous_source,
            "trend": TREND_ARROWS.get(r.get("score"), "N/A") if r.get("status") in ("ok", "stale") else "N/A",
            "score": r.get("score"),
            "status": r.get("status"),
            "source": r.get("source"),
            "history": history,
            "history_years": years,
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
    macro_us = macro_result["macro_us"]
    kr_us_comparison = macro_result["kr_us_comparison"]
    previous_snapshot = macro_snapshot.previous_snapshot(before_month=month_key)
    previous_macro = (previous_snapshot or {}).get("macro")
    previous_macro_us = (previous_snapshot or {}).get("macro_us")

    personal = mapping.run_personal_mapping(macro)
    actions = action_engine.build_action_plan(
        macro, personal["semiconductor"], personal["investment"], personal["bond"],
        personal["fx"], personal["housing"], personal["travel"], personal["calendar"],
    )
    scenarios = scenario_mod.compute_scenarios(macro, personal["semiconductor"], personal["investment"])
    discussion_points = discussion_mod.generate_discussion_points(personal)

    core10_complete = all(
        r.get("status") == DataStatus.OK.value for r in macro["readings"].values()
    )
    readiness = _report_readiness(macro["scores"]["coverage_pct"], core10_complete)

    payload = {
        "report_month": month_key,
        "report_readiness": readiness,
        "macro_us": {
            "regime": macro_us["regime"],
            "previous_regime": macro_us["previous_regime"],
            "transition": macro_us["transition"],
            "score": macro_us["scores"]["raw_score"],
            "weighted_score": macro_us["scores"]["weighted_score"],
            "score_band": macro_us["score_band"],
            "score_band_label": macro_us["score_band_label"],
            "confidence": macro_us["confidence"]["confidence"],
            "warnings": macro_us["warnings_kr"],
            "changes": macro_us["changes"],
        },
        "us_macro_dashboard": _macro_dashboard(macro_us, previous_macro_us, US_INDICATOR_ORDER, US_SERIES_FOR_INDICATOR),
        "kr_us_comparison": kr_us_comparison,
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
        "discussion_points": discussion_points,
        "calendar": personal["calendar"],
        "personal_executive_brief": _executive_brief(macro, personal, actions),
        "appendix": _appendix(macro),
    }

    # Add interest rate analysis
    rate_analysis = _rate_analysis_section()
    payload["rate_analysis"] = rate_analysis

    # Add comprehensive crisis index
    cci_analysis = _cci_section()
    payload["cci_analysis"] = cci_analysis

    # Add real estate transaction price trend (서울/수도권/전국)
    payload["real_estate"] = real_estate_trend.compute_real_estate_trend()

    log_event("report_payload.built", month=month_key, readiness=readiness, action_count=len(actions))
    return payload


def _rate_analysis_section() -> dict:
    """Generate interest rate analysis section (US/KR yield comparison and portfolio impact)."""
    rate_score_detail = rate_scoring.calculate_rate_score()
    portfolio_rec = rate_scoring.portfolio_recommendation(rate_score_detail.total_score)
    sk_hynix_rec = rate_scoring.sk_hynix_outlook(rate_score_detail.total_score, rate_score_detail.spread)

    return {
        "total_score": rate_score_detail.total_score,
        "score_components": {
            "absolute_rates": rate_score_detail.absolute_rate_score,
            "trend_analysis": rate_score_detail.trend_score,
            "spread": rate_score_detail.spread_score,
            "market_signals": rate_score_detail.market_signal_score,
        },
        "current_rates": {
            "us_10y": round(rate_score_detail.us_10y, 2) if rate_score_detail.us_10y else None,
            "kr_10y": round(rate_score_detail.kr_10y, 2) if rate_score_detail.kr_10y else None,
            "spread_bp": round(rate_score_detail.spread, 0) if rate_score_detail.spread else None,
        },
        "trends": {
            "us_10y_1m_change_bp": round(rate_score_detail.trend_1m, 1) if rate_score_detail.trend_1m else None,
            "us_10y_3m_trend": "up" if rate_score_detail.trend_3m and rate_score_detail.trend_3m > 0 else "down",
        },
        "market_signal": {
            "us_10y_2y_spread": round(rate_score_detail.us_10y_2y_spread, 2) if rate_score_detail.us_10y_2y_spread else None,
            "yield_curve_status": "normal" if rate_score_detail.us_10y_2y_spread and rate_score_detail.us_10y_2y_spread > 0 else "inverted",
        },
        "portfolio_recommendation": {
            "stocks": portfolio_rec["stocks"],
            "bonds": portfolio_rec["bonds"],
            "cash": portfolio_rec["cash"],
            "condition": portfolio_rec["condition"],
            "rebalance_trigger": portfolio_rec["rebalance_trigger"],
        },
        "sk_hynix_outlook": {
            "3m_upside_probability": sk_hynix_rec["3m_probability"],
            "6m_upside_probability": sk_hynix_rec["6m_probability"],
            "12m_upside_probability": sk_hynix_rec["12m_probability"],
            "rationale": sk_hynix_rec["rationale"],
        },
    }


def _cci_section() -> dict:
    """Generate Comprehensive Crisis Index analysis section."""
    cci_detail = cci_scoring.calculate_cci()
    sk_hynix_action = cci_scoring.get_sk_hynix_action(cci_detail)

    return {
        "total_score": cci_detail.total_score,
        "state": cci_detail.state,
        "score_components": {
            "sahm": cci_detail.sahm_score,
            "yield_curve": cci_detail.yield_curve_score,
            "harvey": cci_detail.harvey_score,
            "copper_gold": cci_detail.copper_gold_score,
            "credit_oas": cci_detail.credit_score,
            "buffett": cci_detail.buffett_score,
            "rule_of_20": cci_detail.rule20_score,
            "k_sahm": cci_detail.k_sahm_score,
            "semiconductor": cci_detail.semiconductor_score,
        },
        "raw_values": {
            "ur_ma3": round(cci_detail.ur_ma3, 2) if cci_detail.ur_ma3 else None,
            "ur_min_12m": round(cci_detail.ur_min_12m, 2) if cci_detail.ur_min_12m else None,
            "spread_10y2y": round(cci_detail.spread_10y2y, 3) if cci_detail.spread_10y2y else None,
            "spread_10y3m": round(cci_detail.spread_10y3m, 3) if cci_detail.spread_10y3m else None,
            "hy_oas": round(cci_detail.hy_oas, 2) if cci_detail.hy_oas else None,
            "k_emp_yoy": round(cci_detail.k_emp_yoy, 0) if cci_detail.k_emp_yoy else None,
        },
        "sk_hynix_action": sk_hynix_action,
        "interpretation": {
            "GREEN": "Systemic expansion. Capital injection favored. Aggressive growth positioning optimal.",
            "YELLOW": "Momentum deceleration. Capital hedging recommended. Tactical positioning advised.",
            "RED": "Systemic invalidation. Capital evacuation urgent. Defensive/short positioning required.",
        },
    }
