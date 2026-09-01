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
from engine.real_estate import officetel_trend, rent_trend, villa_trend
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

    # Position & exposure model (Section 0). Deliberately computed BEFORE and
    # independently of every collector: it reads config/portfolio.yaml only, so
    # it stays valid on days when the whole macro layer is carried forward.
    # See engine/exposure/model.py for why this layer exists.
    try:
        from engine.exposure.model import build_exposure_model
        payload["exposure"] = build_exposure_model()
        log_event("exposure_model.computed",
                  semi_pct=round(payload["exposure"].semi_pct, 1),
                  deployable=payload["exposure"].deployable_cash)
    except Exception as exc:
        log_event("exposure_model.failed", error=str(exc), level="warning")
        payload["exposure"] = None

    # Add interest rate analysis
    rate_analysis = _rate_analysis_section()
    payload["rate_analysis"] = rate_analysis

    # Add comprehensive crisis index
    cci_analysis = _cci_section()
    payload["cci_analysis"] = cci_analysis

    # Add real estate transaction price trend (서울/수도권/전국) — 아파트 매매/전월세/
    # 연립다세대 매매/오피스텔 매매 4종. 각 collector는 별도 data.go.kr 활용신청이 필요해
    # 승인 전까지는 개별적으로 "pending"일 수 있다 (7.9 — 소스 없다고 파이프라인이 막히지 않음).
    payload["real_estate"] = real_estate_trend.compute_real_estate_trend()
    payload["real_estate_rent"] = rent_trend.compute_rent_trend()
    payload["real_estate_villa"] = villa_trend.compute_villa_trend()
    payload["real_estate_officetel"] = officetel_trend.compute_officetel_trend()

    # Add daily dashboard history integration
    payload["daily_history_summary"] = _daily_history_summary(month_key)

    # Add decision engines (Phase 2 integration)
    from engine.exporters.sk_hynix_decision import compute_sk_hynix_decision
    from engine.exporters.real_estate_decision import compute_real_estate_decision

    try:
        payload["sk_hynix_decision"] = compute_sk_hynix_decision(payload)
        log_event("sk_hynix_decision.computed", signal=payload["sk_hynix_decision"].signal,
                  confidence=payload["sk_hynix_decision"].confidence)
    except Exception as exc:
        log_event("sk_hynix_decision.failed", error=str(exc), level="warning")
        payload["sk_hynix_decision"] = None

    # HBM Cycle Score — 외국인수급·보유율 2축 자동채점 (hbm-cycle-score.md "1.").
    # Context/evidence only, never a second buy/sell instruction (R4 in
    # reconciliation.py: 포지션 지시는 단일 출처) — sk_hynix_decision above
    # remains the only module allowed to say HOLD/BUY/SELL. The other 4 axes
    # (ASP·엔비디아&CoWoS·공급확대·고객재고) are qualitative judgment calls
    # this cron pipeline can't reproduce; they stay in the wiki (Phase 4).
    try:
        from scripts.hbm_cycle_score import score_foreign_flow_axis, score_foreign_holding_axis

        payload["hbm_cycle_score"] = {
            "ticker": "000660",
            "foreign_flow": score_foreign_flow_axis("000660"),
            "foreign_holding": score_foreign_holding_axis("000660"),
        }
        log_event("hbm_cycle_score.computed",
                  flow=payload["hbm_cycle_score"]["foreign_flow"]["score"],
                  holding=payload["hbm_cycle_score"]["foreign_holding"]["score"])
    except Exception as exc:
        log_event("hbm_cycle_score.failed", error=str(exc), level="warning")
        payload["hbm_cycle_score"] = None

    # 하이퍼스케일러 CapEx 실측 + SK Hynix 오늘의 실측 데이터 (SEC EDGAR + KIS,
    # 이미 매일/주간 수집되던 CSV를 처음으로 PEOS 쪽에서도 읽는다). 전부
    # 정보/근거용 — 어느 것도 새 매매 지시를 만들지 않는다(R4).
    try:
        from scripts.capex_periphery import read_hyperscaler_capex, read_ai_periphery
        from scripts.investor_flow import (
            read_latest_price_snapshot, read_ticker_rows, summarize_flows,
            credit_balance_streak, read_latest_short_sale, read_latest_adr,
        )

        payload["hyperscaler_capex"] = read_hyperscaler_capex()
        payload["ai_periphery"] = read_ai_periphery()

        flow_rows = read_ticker_rows("000660")
        payload["sk_hynix_live"] = {
            "price_snapshot": read_latest_price_snapshot("000660"),
            "flow_summary": summarize_flows(flow_rows) if flow_rows else None,
            "flow_latest_date": flow_rows[-1]["date"] if flow_rows else None,
            "credit_balance": credit_balance_streak("000660"),
            "short_sale": read_latest_short_sale("000660"),
            "adr": read_latest_adr("SKHY"),
        }
        log_event("sk_hynix_live_data.loaded",
                  capex_tickers=list(payload["hyperscaler_capex"].keys()) if payload["hyperscaler_capex"] else [],
                  has_price_snapshot=payload["sk_hynix_live"]["price_snapshot"] is not None)
    except Exception as exc:
        log_event("sk_hynix_live_data.failed", error=str(exc), level="warning")
        payload["hyperscaler_capex"] = None
        payload["ai_periphery"] = None
        payload["sk_hynix_live"] = None

    try:
        payload["real_estate_decision"] = compute_real_estate_decision(payload)
        log_event("real_estate_decision.computed", signal=payload["real_estate_decision"].signal,
                  confidence=payload["real_estate_decision"].confidence)
    except Exception as exc:
        log_event("real_estate_decision.failed", error=str(exc), level="warning")
        payload["real_estate_decision"] = None

    # Record daily signal (Phase 3c: Signal Persistence)
    try:
        from engine.report.signal_recorder import record_daily_signal

        sk_signal = payload["sk_hynix_decision"].signal if payload.get("sk_hynix_decision") else "HOLD"
        sk_confidence = payload["sk_hynix_decision"].confidence if payload.get("sk_hynix_decision") else 50.0
        re_signal = payload["real_estate_decision"].signal if payload.get("real_estate_decision") else "WAIT"
        re_confidence = payload["real_estate_decision"].confidence if payload.get("real_estate_decision") else 50.0

        today = date.today().isoformat()
        record_daily_signal(
            date=today,
            sk_hynix_signal=sk_signal,
            sk_hynix_confidence=sk_confidence,
            real_estate_signal=re_signal,
            real_estate_confidence=re_confidence,
            notes=f"Recorded from PEOS pipeline ({month_key})"
        )
        log_event("daily_signal.recorded", date=today, sk_signal=sk_signal, re_signal=re_signal)
    except Exception as exc:
        log_event("daily_signal.failed", error=str(exc), level="warning")

    # Add rolling aggregation (Phase 3c: Signal Trending)
    try:
        from engine.report.signal_recorder import load_signals
        from engine.report.rolling_aggregator import aggregate_signals_by_period, compare_periods

        # Load signals from past 90 days
        signals = load_signals()

        # Aggregate into periods
        if signals:
            monthly_periods = aggregate_signals_by_period(signals, "month")
            quarterly_periods = aggregate_signals_by_period(signals, "quarter")

            # Build rolling windows dict
            rolling_windows = {
                "status": "ok",
                "signals_count": len(signals),
                "monthly": {
                    "current": monthly_periods[-1].__dict__ if monthly_periods else None,
                    "previous": monthly_periods[-2].__dict__ if len(monthly_periods) > 1 else None,
                    "comparison": (
                        compare_periods(monthly_periods[-1], monthly_periods[-2])
                        if len(monthly_periods) > 1 else (None, None)
                    ),
                },
                "quarterly": {
                    "current": quarterly_periods[-1].__dict__ if quarterly_periods else None,
                    "previous": quarterly_periods[-2].__dict__ if len(quarterly_periods) > 1 else None,
                    "comparison": (
                        compare_periods(quarterly_periods[-1], quarterly_periods[-2])
                        if len(quarterly_periods) > 1 else (None, None)
                    ),
                },
                "ytd": {
                    "current": quarterly_periods[-1].__dict__ if quarterly_periods and len(quarterly_periods) >= 4 else None,
                }
            }
            payload["rolling_windows"] = rolling_windows
            log_event("rolling_windows.computed", signals_count=len(signals),
                      monthly_count=len(monthly_periods), quarterly_count=len(quarterly_periods))
        else:
            payload["rolling_windows"] = {"status": "no_signals", "note": "신호 데이터 없음"}
            log_event("rolling_windows.skipped", reason="no_signals")

    except Exception as exc:
        log_event("rolling_windows.failed", error=str(exc), level="warning")
        payload["rolling_windows"] = {"status": "error", "error": str(exc)}

    # Add 12-week macro indicator analysis (Layer 0 supporting evidence)
    try:
        from engine.report.weekly_analysis import generate_weekly_analysis

        weekly_result = generate_weekly_analysis()
        payload["weekly_analysis"] = {
            "analysis_date": weekly_result.analysis_date,
            "period_start": weekly_result.period_start,
            "period_end": weekly_result.period_end,
            "indicators": {
                name: {
                    "label": analysis.label,
                    "unit": analysis.unit,
                    "current_value": analysis.current_value,
                    "value_12w_ago": analysis.value_12w_ago,
                    "pct_change": analysis.pct_change,
                    "abs_change": analysis.abs_change,
                    "trend": analysis.trend,
                    "latest_date": analysis.latest_date,
                    "data_points": analysis.data_points,
                }
                for name, analysis in weekly_result.indicators.items()
            }
        }
        log_event("weekly_analysis.computed", analysis_date=weekly_result.analysis_date,
                  indicator_count=len(weekly_result.indicators))
    except Exception as exc:
        log_event("weekly_analysis.failed", error=str(exc), level="warning")
        payload["weekly_analysis"] = {"status": "error", "error": str(exc)}

    # Add data center construction vs opposition raw data (HBM Cycle Score
    # "고객재고" axis supporting reference — intentionally NOT scored, see
    # data/manual_inputs/data_center_construction.yaml header for why).
    try:
        from collectors import manual as manual_collectors

        dc_payload = manual_collectors.fetch_data_center_construction()
        payload["data_center_construction"] = dc_payload  # None -> markdown section self-skips
        if dc_payload:
            log_event("data_center_construction.loaded", updated_at=dc_payload.get("updated_at"))
    except Exception as exc:
        log_event("data_center_construction.failed", error=str(exc), level="warning")
        payload["data_center_construction"] = None

    # 위키 판단형 지식 브리지 (Phase 4, 2026-08-27) — HBM Cycle Score 정성축,
    # 9체크포인트, 찐반등 4대 신호, 트럼프 트래커 등은 WebSearch·애널리스트
    # 리포트 해석이 필요해 이 LLM-미사용 cron 파이프라인이 재현할 수 없다.
    # data/wiki_digest/*.yaml(위키가 유일한 원천, 이 파일들은 그 압축 요약을
    # 미러링할 뿐)을 읽어 리포트에 노출 — 원문은 위키로 링크.
    try:
        from engine.report.wiki_digest import load_wiki_digests

        payload["wiki_digests"] = load_wiki_digests()
        log_event("wiki_digests.loaded", count=len(payload["wiki_digests"]),
                  stale_count=sum(1 for d in payload["wiki_digests"] if d["is_stale"]))
    except Exception as exc:
        log_event("wiki_digests.failed", error=str(exc), level="warning")
        payload["wiki_digests"] = []

    # Cross-engine reconciliation. Runs LAST so it can see every engine's output,
    # and emits one stance instead of letting modules contradict each other in
    # front of the reader. See engine/report/reconciliation.py for the rules.
    try:
        from engine.report.reconciliation import reconcile
        payload["reconciliation"] = reconcile(payload)
        log_event("reconciliation.computed",
                  conflicts=len(payload["reconciliation"].conflicts),
                  tradeable=payload["reconciliation"].tradeable)
    except Exception as exc:
        log_event("reconciliation.failed", error=str(exc), level="warning")
        payload["reconciliation"] = None


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
        # Series dropped for age. Present so the report can distinguish "not collected"
        # from "collected and happens to be blank" — see engine/rate_analysis/scoring.py.
        "stale_series": getattr(rate_score_detail, "stale_series", []),
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
            "copper_gold_ratio": (round(cci_detail.copper_gold_ratio, 4)
                                  if cci_detail.copper_gold_ratio is not None else None),
            "k_emp_yoy": round(cci_detail.k_emp_yoy, 0) if cci_detail.k_emp_yoy else None,
            # Needed to tell "no data" apart from a real reading: score_semiconductor_cycle()
            # returns 0 both when the series is missing and when the cycle is healthy, so the
            # score alone cannot be narrated honestly. None here means genuinely uncollected.
            "semi_cycle_index": (round(cci_detail.semi_cycle_index, 4)
                                 if cci_detail.semi_cycle_index is not None else None),
        },
        # 2026-09-01 신설 — 사용자 지적: "데이터 신선도가 표시가 없네! 특히
        # 몇점이고 판단만 하는 항목은 믿을 수가 없네!". 모듈별 PRIMARY/FALLBACK/
        # NO_DATA + 참조 시리즈 + 며칠 지난 데이터인지 그대로 통과시킨다.
        "data_quality": cci_detail.data_quality,
        "sk_hynix_action": sk_hynix_action,
        "interpretation": {
            "GREEN": "Systemic expansion. Capital injection favored. Aggressive growth positioning optimal.",
            "YELLOW": "Momentum deceleration. Capital hedging recommended. Tactical positioning advised.",
            "RED": "Systemic invalidation. Capital evacuation urgent. Defensive/short positioning required.",
        },
    }


def _daily_history_summary(month_key: str) -> dict:
    """일일 대시보드 이력 데이터를 월간 리포트에 통합 (지난 30일 최신 5개 기록).

    peos_daily_history.csv에서 해당 월의 마지막 기록들을 읽어 일일 변화 추이를 제공한다.
    """
    import csv
    from pathlib import Path

    history_file = Path("data/peos_daily_history.csv")
    if not history_file.exists():
        return {"status": "unavailable", "note": "일일 이력 데이터 없음"}

    try:
        records = []
        with open(history_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                run_date = row.get("run_date", "")
                if run_date.startswith(month_key):
                    records.append(row)

        if not records:
            return {"status": "unavailable", "note": f"{month_key} 월간 일일 이력 없음"}

        # 마지막 5개 기록만 사용
        records = records[-5:]

        # 첫 기록과 마지막 기록의 변화 계산
        first = records[0]
        last = records[-1]

        def safe_float(v):
            if not v or v == '':
                return None
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        return {
            "status": "ok",
            "month": month_key,
            "daily_records": [
                {
                    "date": r.get("run_date"),
                    "kr_regime": r.get("kr_regime"),
                    "kr_score": safe_float(r.get("kr_raw_score")),
                    "kr_confidence": safe_float(r.get("kr_confidence")),
                    "us_regime": r.get("us_regime"),
                    "us_score": safe_float(r.get("us_raw_score")),
                    "us_confidence": safe_float(r.get("us_confidence")),
                    "investment_env_score": safe_float(r.get("investment_environment_score")),
                    "semiconductor_score": safe_float(r.get("semiconductor_score")),
                    "bond_score": safe_float(r.get("bond_score")),
                }
                for r in records
            ],
            "trend_summary": {
                "kr_regime_stable": first.get("kr_regime") == last.get("kr_regime"),
                "kr_confidence_change": safe_float(last.get("kr_confidence")) - safe_float(first.get("kr_confidence")) if safe_float(first.get("kr_confidence")) and safe_float(last.get("kr_confidence")) else None,
                "us_regime_stable": first.get("us_regime") == last.get("us_regime"),
                "us_confidence_change": safe_float(last.get("us_confidence")) - safe_float(first.get("us_confidence")) if safe_float(first.get("us_confidence")) and safe_float(last.get("us_confidence")) else None,
                "investment_env_trend": (safe_float(last.get("investment_environment_score")) or 0) - (safe_float(first.get("investment_environment_score")) or 0),
                "semiconductor_trend": (safe_float(last.get("semiconductor_score")) or 0) - (safe_float(first.get("semiconductor_score")) or 0),
            }
        }
    except Exception as e:
        return {"status": "error", "note": f"일일 이력 읽기 오류: {str(e)}"}
