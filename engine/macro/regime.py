"""Regime detection (Master Instruction 11.7-11.10).

State machine over the cycle Recovery -> Early Expansion -> Expansion ->
Late Expansion -> Slowdown -> Recession -> Recovery. Movement is driven by
three signal-count rules, evaluated every run against config/thresholds.yaml
`regime_signals` magnitudes and config/rules.yaml `regime` structure:

  - downgrade: >=2 of 7 negative signals -> demote one stage (11.8)
  - warning:   >=1 of 6 risk signals -> Warning flag, no forced demotion (11.9)
  - upgrade:   >=3 of 7 positive signals -> promote one stage (11.10)

If neither threshold fires, the explicit "2 consecutive months of
improving score + co-improving exports/production" persistence rule
(11.7's Early Expansion -> Expansion example) is checked. Other 11.7
examples (Expansion -> Late Expansion via strength + inflation pressure;
Expansion -> Slowdown via falling score + worsening breadth) are already
covered by the generic downgrade/warning signal set above, since their
triggers (cpi_reaccelerating, ppi_sustained_high, export/production
weakness) are members of it.
"""
from __future__ import annotations

from collectors import base as collector_base
from core.config import rules_config, thresholds_config
from core.models import IndicatorReading
from . import score as score_mod

SIGNAL_LABELS_KR = {
    "export_slump": "수출 급락",
    "semiconductor_export_slump": "반도체 수출 급락",
    "industrial_production_decline_2m": "산업생산 2개월 연속 감소",
    "cpi_reaccelerating": "CPI 재가속",
    "ppi_sustained_high": "PPI 고압 지속",
    "fx_surge": "환율 급등",
    "rates_rising": "금리 상승",
    "exports_negative": "수출 감소 전환",
    "semiconductor_exports_negative": "반도체 수출 감소 전환",
    "unemployment_surge": "실업률 급등",
    "current_account_deficit": "경상수지 적자",
    "us_employment_cooling": "미국 고용 급랭",
    "yield_curve_inversion_deepening": "장단기 금리 역전 심화",
}


def field_value(readings: dict[str, IndicatorReading], indicator: str, field: str):
    if indicator not in readings:
        return None
    return readings[indicator].detail.get("fields", {}).get(field)


def recent_values(series_id: str, n: int) -> list[float]:
    df = collector_base.read_normalized(series_id)
    if df.empty:
        return []
    return df.sort_values("date")["value"].tail(n).tolist()


def recent_pct_changes(series_id: str, periods: int, n: int) -> list[float]:
    df = collector_base.read_normalized(series_id)
    if df.empty:
        return []
    s = df.sort_values("date")["value"].pct_change(periods=periods) * 100
    return s.dropna().tail(n).tolist()


def bp_change_row_offset(series_id: str, offset_rows: int) -> float | None:
    """Approximate N-row-ago change in percentage-point terms, converted to bp (x100)."""
    latest, prior = collector_base.series_change_over_rows(series_id, offset_rows)
    if latest is None:
        return None
    return (latest - prior) * 100


def _compute_signals(readings: dict[str, IndicatorReading]) -> dict[str, bool]:
    t = thresholds_config()["regime_signals"]
    s: dict[str, bool] = {}

    exports_yoy = field_value(readings, "exports", "yoy")
    semi_yoy = field_value(readings, "semiconductor_exports", "yoy")
    s["exports_negative"] = exports_yoy is not None and exports_yoy < 0
    s["semiconductor_exports_negative"] = semi_yoy is not None and semi_yoy < 0
    s["exports_strong"] = exports_yoy is not None and exports_yoy >= t["exports_strong_yoy"]
    s["semiconductor_strong"] = semi_yoy is not None and semi_yoy >= t["semiconductor_strong_yoy"]

    exp_hist = recent_values("motie_total_exports_yoy", 2)
    s["export_slump"] = len(exp_hist) == 2 and (exp_hist[0] - exp_hist[1]) >= t["export_slump_yoy_drop_pp"]
    semi_hist = recent_values("motie_semiconductor_exports_yoy", 2)
    s["semiconductor_export_slump"] = (
        len(semi_hist) == 2 and (semi_hist[0] - semi_hist[1]) >= t["semiconductor_export_slump_yoy_drop_pp"]
    )

    ip_mom_hist = recent_pct_changes("kosis_industrial_production_index", 1, t["ip_consecutive_decline_months"])
    s["industrial_production_decline_2m"] = (
        len(ip_mom_hist) == t["ip_consecutive_decline_months"] and all(v < 0 for v in ip_mom_hist)
    )

    cpi_yoy_hist = recent_pct_changes("kosis_cpi_index", 12, 2)
    s["cpi_reaccelerating"] = len(cpi_yoy_hist) == 2 and (cpi_yoy_hist[1] - cpi_yoy_hist[0]) >= t["cpi_reaccelerating_pp"]
    cpi_yoy = field_value(readings, "cpi", "yoy")
    lo, hi = t["cpi_stable_range"]
    s["cpi_stable"] = cpi_yoy is not None and lo <= cpi_yoy <= hi

    ppi_yoy_hist = recent_pct_changes("ecos_ppi_yoy_level", 12, t["ppi_sustained_months"])
    s["ppi_sustained_high"] = (
        len(ppi_yoy_hist) == t["ppi_sustained_months"] and all(v >= t["ppi_sustained_high_threshold"] for v in ppi_yoy_hist)
    )
    ppi_yoy_hist2 = recent_pct_changes("ecos_ppi_yoy_level", 12, 2)
    s["ppi_easing"] = len(ppi_yoy_hist2) == 2 and (ppi_yoy_hist2[0] - ppi_yoy_hist2[1]) >= t["ppi_easing_drop_pp"]

    fx_mom = recent_pct_changes("ecos_usdkrw", 1, 1)
    s["fx_surge"] = bool(fx_mom) and fx_mom[-1] >= t["fx_surge_mom_pct"]

    rate_bp_3m = bp_change_row_offset("ecos_kr_3y_yield", 63)
    s["rates_rising"] = rate_bp_3m is not None and rate_bp_3m >= t["rates_rising_bp_3m"]
    s["rates_easing"] = rate_bp_3m is not None and rate_bp_3m <= t["rates_easing_bp_3m"]

    yc_bp_3m = bp_change_row_offset("fred_us_yield_curve_10y2y", 63)
    s["yield_curve_inversion_deepening"] = yc_bp_3m is not None and yc_bp_3m <= t["yield_curve_inversion_deepening_bp"]

    unemployment_change = field_value(readings, "unemployment", "avg_3m_change")
    s["unemployment_surge"] = unemployment_change is not None and unemployment_change >= t["unemployment_surge_pp"]

    current_account_avg = field_value(readings, "current_account", "avg_3m")
    s["current_account_deficit"] = current_account_avg is not None and current_account_avg < 0

    us_global_val = readings["us_global"].value if "us_global" in readings else None
    s["us_employment_cooling"] = us_global_val is not None and us_global_val <= t["us_employment_cooling_composite"]
    s["us_employment_improving"] = us_global_val is not None and us_global_val >= t["us_employment_improving_composite"]

    gdp_qoq = field_value(readings, "gdp", "qoq")
    s["gdp_strong"] = gdp_qoq is not None and gdp_qoq >= t["gdp_strong_qoq"]

    return s


def _persistence_upgrade(current_regime: str, history: list[dict], raw_score: float,
                          readings: dict[str, IndicatorReading], history_key: str,
                          breadth_indicators: tuple[str, str]) -> str | None:
    """11.7 example: Early Expansion -> Expansion when score improves 2 months running
    and two breadth indicators (exports/production for KR, retail_sales/production
    for US) co-improve."""
    if current_regime != "Early Expansion" or len(history) < 1:
        return None
    prev = history[-1]
    prev_score = prev.get(history_key, {}).get("scores", {}).get("raw_score")
    if prev_score is None or raw_score <= prev_score:
        return None
    if len(history) >= 2:
        prev_prev_score = history[-2].get(history_key, {}).get("scores", {}).get("raw_score")
        if prev_prev_score is not None and prev_score <= prev_prev_score:
            return None
    breadth_a, breadth_b = breadth_indicators
    a_ok = (readings.get(breadth_a).score or -1) >= 0 if breadth_a in readings else False
    b_ok = (readings.get(breadth_b).score or -1) >= 0 if breadth_b in readings else False
    if a_ok and b_ok:
        return "Expansion"
    return None


def run_state_machine(cfg: dict, signals: dict[str, bool], raw_score: float, history: list[dict],
                       history_key: str, readings: dict[str, IndicatorReading],
                       label_map: dict[str, str], breadth_indicators: tuple[str, str]) -> dict:
    """Shared cycle/downgrade/warning/upgrade state machine (11.7-11.10) —
    used by both the KR and US regime engines. Only the signal source, config
    section, and snapshot key differ between markets; the transition logic
    itself (and its "cycle[] is chronological, not a goodness scale" reading
    of 상향/강등) is identical, so it's kept in one place rather than
    duplicated per market."""
    cycle: list[str] = cfg["cycle"]

    downgrade_hits = [k for k in cfg["downgrade"]["signals"] if signals.get(k)]
    warning_hits = [k for k in cfg["warning"]["signals"] if signals.get(k)]
    upgrade_hits = [k for k in cfg["upgrade"]["signals"] if signals.get(k)]

    band_key, _ = score_mod.score_band(raw_score)
    seed_regime = cfg["score_band_seed"].get(band_key, cycle[0])
    previous_regime = (
        history[-1][history_key]["regime"]
        if history and history[-1].get(history_key, {}).get("regime")
        else seed_regime
    )
    idx = cycle.index(previous_regime) if previous_regime in cycle else 0

    # cycle[] is chronological, not a linear "goodness" scale (Late Expansion is
    # a later stage than Expansion, not a strictly worse one). Downgrade always
    # steps forward (toward Slowdown/Recession); upgrade always steps backward
    # (toward Recovery/Early Expansion, i.e. away from late-cycle risk). This is
    # a deliberate, symmetric reading of 11.7-11.10's "1단계 상향/강등" language.
    transition = None
    if len(downgrade_hits) >= cfg["downgrade"]["trigger_count"]:
        idx = min(idx + 1, len(cycle) - 1)
        transition = "downgrade"
    elif len(upgrade_hits) >= cfg["upgrade"]["trigger_count"]:
        idx = max(idx - 1, 0)
        transition = "upgrade"
    else:
        promoted = _persistence_upgrade(previous_regime, history, raw_score, readings, history_key, breadth_indicators)
        if promoted:
            idx = cycle.index(promoted)
            transition = "persistence"

    new_regime = cycle[idx]
    warning_active = len(warning_hits) >= cfg["warning"]["trigger_count"]

    return {
        "regime": new_regime,
        "previous_regime": previous_regime,
        "transition": transition,
        "score_band": band_key,
        "downgrade_signals": downgrade_hits,
        "warning_signals": warning_hits,
        "upgrade_signals": upgrade_hits,
        "warning_active": warning_active,
        "warnings_kr": [label_map.get(k, k) for k in warning_hits] if warning_active else [],
        "all_signals": signals,
    }


def determine_regime(readings: dict[str, IndicatorReading], raw_score: float, history: list[dict]) -> dict:
    cfg = rules_config()["regime"]
    signals = _compute_signals(readings)
    return run_state_machine(cfg, signals, raw_score, history, "macro", readings,
                              SIGNAL_LABELS_KR, ("exports", "industrial_production"))
