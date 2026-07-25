"""US regime detection — same state machine as engine/macro/regime.py
(11.7-11.10's downgrade/warning/upgrade signal-count rules), but every
signal is computed from US series only, so KR data-source issues (KOSIS/
ECOS intermittent access) never affect it. Shares the transition logic via
regime.run_state_machine; only signal computation, config section
(config/rules.yaml `regime_us`), and snapshot key ("macro_us") differ.
"""
from __future__ import annotations

from core.config import rules_config, thresholds_config
from core.models import IndicatorReading
from . import indicators as kr_indicators
from . import regime

SIGNAL_LABELS_US = {
    "retail_sales_slump": "미국 소매판매 급락",
    "industrial_production_decline_2m": "미국 산업생산 2개월 연속 감소",
    "cpi_reaccelerating": "미국 CPI 재가속",
    "ppi_sustained_high": "미국 PPI 고압 지속",
    "yield_curve_inversion_deepening": "미국 장단기 금리 역전 심화",
    "trade_balance_widening": "미국 무역적자 확대",
    "gdp_contraction": "미국 GDP 위축",
    "gdp_negative": "미국 GDP 마이너스 성장",
    "retail_sales_negative": "미국 소매판매 감소 전환",
    "unemployment_surge": "미국 실업률 급등",
    "yield_curve_inverted": "미국 장단기 금리 역전",
    "trade_balance_wide_deficit": "미국 무역적자 확대 지속",
}


def _compute_signals_us(readings: dict[str, IndicatorReading]) -> dict[str, bool]:
    t = thresholds_config()["regime_signals_us"]
    s: dict[str, bool] = {}

    retail_mom_hist = regime.recent_pct_changes("fred_us_retail_sales", 1, 2)
    s["retail_sales_slump"] = (
        len(retail_mom_hist) == 2 and (retail_mom_hist[0] - retail_mom_hist[1]) >= t["retail_sales_slump_mom_drop_pp"]
    )
    retail_mom = regime.field_value(readings, "retail_sales", "mom")
    s["retail_sales_negative"] = retail_mom is not None and retail_mom < 0
    s["retail_sales_strong"] = retail_mom is not None and retail_mom >= t["retail_sales_strong_mom"]

    ip_mom_hist = regime.recent_pct_changes("fred_us_industrial_production", 1, t["ip_consecutive_decline_months"])
    s["industrial_production_decline_2m"] = (
        len(ip_mom_hist) == t["ip_consecutive_decline_months"] and all(v < 0 for v in ip_mom_hist)
    )
    ip_mom = regime.field_value(readings, "industrial_production", "mom")
    s["industrial_production_strong"] = ip_mom is not None and ip_mom >= t["industrial_production_strong_mom"]

    cpi_yoy_hist = regime.recent_pct_changes("fred_us_cpi", 12, 2)
    s["cpi_reaccelerating"] = len(cpi_yoy_hist) == 2 and (cpi_yoy_hist[1] - cpi_yoy_hist[0]) >= t["cpi_reaccelerating_pp"]
    cpi_yoy = regime.field_value(readings, "cpi", "yoy")
    lo, hi = t["cpi_stable_range"]
    s["cpi_stable"] = cpi_yoy is not None and lo <= cpi_yoy <= hi

    ppi_yoy_hist = regime.recent_pct_changes("fred_us_ppi", 12, t["ppi_sustained_months"])
    s["ppi_sustained_high"] = (
        len(ppi_yoy_hist) == t["ppi_sustained_months"] and all(v >= t["ppi_sustained_high_threshold"] for v in ppi_yoy_hist)
    )
    ppi_yoy_hist2 = regime.recent_pct_changes("fred_us_ppi", 12, 2)
    s["ppi_easing"] = len(ppi_yoy_hist2) == 2 and (ppi_yoy_hist2[0] - ppi_yoy_hist2[1]) >= t["ppi_easing_drop_pp"]

    yc_bp_3m = regime.bp_change_row_offset("fred_us_yield_curve_10y2y", 63)
    yc_spread = regime.field_value(readings, "yield_curve", "spread")
    s["yield_curve_inversion_deepening"] = yc_bp_3m is not None and yc_bp_3m <= t["yield_curve_inversion_deepening_bp"]
    s["yield_curve_inverted"] = yc_spread is not None and yc_spread < 0
    s["yield_curve_steepening"] = yc_bp_3m is not None and yc_bp_3m > 0 and yc_spread is not None and yc_spread >= 0

    avg_now = kr_indicators.series_moving_average("fred_us_trade_balance", 3)
    avg_prior = kr_indicators.series_moving_average("fred_us_trade_balance", 3, offset=3)
    widening = False
    if avg_now is not None and avg_prior is not None and avg_prior < 0:
        widening_pct = (avg_prior - avg_now) / abs(avg_prior) * 100  # deficit got bigger (more negative)
        widening = widening_pct >= t["trade_balance_widening_3m_pct"]
    s["trade_balance_widening"] = widening
    trade_avg3 = regime.field_value(readings, "trade_balance", "avg_3m")
    s["trade_balance_wide_deficit"] = trade_avg3 is not None and trade_avg3 <= t["trade_balance_wide_deficit"]

    unemployment_change = regime.field_value(readings, "unemployment", "avg_3m_change")
    s["unemployment_surge"] = unemployment_change is not None and unemployment_change >= t["unemployment_surge_pp"]
    s["unemployment_improving"] = unemployment_change is not None and unemployment_change <= t["unemployment_improving_pp"]

    gdp_qoq = regime.field_value(readings, "gdp", "qoq")
    s["gdp_negative"] = gdp_qoq is not None and gdp_qoq < 0
    s["gdp_contraction"] = gdp_qoq is not None and gdp_qoq < 0
    s["gdp_strong"] = gdp_qoq is not None and gdp_qoq >= t["gdp_strong_qoq"]

    return s


def determine_regime_us(readings: dict[str, IndicatorReading], raw_score: float, history: list[dict]) -> dict:
    cfg = rules_config()["regime_us"]
    signals = _compute_signals_us(readings)
    return regime.run_state_machine(cfg, signals, raw_score, history, "macro_us", readings,
                                     SIGNAL_LABELS_US, ("retail_sales", "industrial_production"))
