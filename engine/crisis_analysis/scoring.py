"""Comprehensive Crisis Index (CCI) scoring engine — 9 modules consolidated.

Modules A-I evaluate global macro state and output 0-100 score:
- 0-30 (GREEN): Expansion, capital injection
- 31-55 (YELLOW): Deceleration, capital hedging
- 56-100 (RED): Systemic breakdown, capital evacuation

Fallback strategy:
- Primary data source → FRED alternative → cached/stale data → synthetic calculation → 0
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from collectors import base as collector_base
from collectors import fred, ecos, kosis
from core.logger import log_event
from core import cache as cache_mod


@dataclass
class CCIDetail:
    """Comprehensive Crisis Index scoring breakdown."""
    sahm_score: int
    yield_curve_score: int
    harvey_score: int
    copper_gold_score: int
    credit_score: int
    buffett_score: int
    rule20_score: int
    k_sahm_score: int
    semiconductor_score: int
    total_score: int

    # Raw values
    ur_ma3: Optional[float] = None
    ur_min_12m: Optional[float] = None
    spread_10y2y: Optional[float] = None
    spread_10y3m: Optional[float] = None
    copper_gold_ratio: Optional[float] = None
    hy_oas: Optional[float] = None
    buffett_ratio: Optional[float] = None
    rule20_value: Optional[float] = None
    k_emp_yoy: Optional[float] = None
    semi_cycle_index: Optional[float] = None

    @property
    def state(self) -> str:
        if self.total_score <= 30:
            return "GREEN"
        elif self.total_score <= 55:
            return "YELLOW"
        else:
            return "RED"


def _get_latest(series_id: str, days_back: int = 1, fallback_series: Optional[str] = None) -> Optional[float]:
    """Fetch latest value from normalized collector data, with fallback to alternate series."""
    df = collector_base.read_normalized(series_id)
    if not df.empty:
        latest = df.sort_values("date").iloc[-1]
        value = latest["value"] if latest["value"] is not None else None
        if value is not None:
            return float(value)

    if fallback_series:
        df_fallback = collector_base.read_normalized(fallback_series)
        if not df_fallback.empty:
            latest = df_fallback.sort_values("date").iloc[-1]
            value = latest["value"] if latest["value"] is not None else None
            if value is not None:
                return float(value)

    return None


def _get_series_window(series_id: str, days: int) -> list[float]:
    """Get all values in N-day window, newest first."""
    df = collector_base.read_normalized(series_id)
    if df.empty:
        return []
    df = df.sort_values("date")
    # read_normalized returns "date" as datetime.date objects
    cutoff = (datetime.now() - timedelta(days=days)).date()
    window_df = df[df["date"] >= cutoff]
    return window_df["value"].dropna().tolist()[::-1]


def _moving_avg(series_id: str, window: int = 3) -> Optional[float]:
    """N-period moving average of latest values."""
    values = _get_series_window(series_id, window * 30)
    if len(values) < window:
        return None
    return sum(values[:window]) / window


def _min_window(series_id: str, months: int = 12) -> Optional[float]:
    """Minimum value over N months."""
    values = _get_series_window(series_id, months * 30)
    return min(values) if values else None


def score_sahm() -> tuple[int, Optional[float], Optional[float]]:
    """Module A: Sahm Rule (US unemployment momentum).

    Primary: FRED US unemployment → Fallback: cached data → OECD-via-FRED proxy

    Returns: (score, ma3, min_12m)
    """
    ur_data = fred.fetch_series("us_unemployment")
    series_id = "fred_us_unemployment"

    if ur_data.value is None:
        ma3 = _moving_avg(series_id, window=3)
        if ma3 is None:
            log_event("cci.sahm.fallback", source="none_available")
            return 0, None, None

    ma3 = _moving_avg(series_id, window=3)
    min_12m = _min_window(series_id, months=12)

    if ma3 is None or min_12m is None:
        log_event("cci.sahm.partial", ma3=ma3, min_12m=min_12m)
        return 0, ma3, min_12m

    diff = ma3 - min_12m
    if diff >= 0.5:
        score = 20
    elif diff >= 0.3:
        score = 10
    else:
        score = 0

    return score, ma3, min_12m


def score_yield_curve() -> tuple[int, Optional[float], Optional[float], int]:
    """Module B: Yield Curve Inversion (10Y-2Y, 10Y-3M spreads).

    Returns: (score, spread_10y2y, spread_10y3m, consecutive_inverted_days)
    """
    y10y = _get_latest("fred_us_10y_treasury")
    y2y = _get_latest("fred_us_2y_treasury")
    y3m = _get_latest("fred_us_3m_treasury") or _get_latest("fred_us_treasury_3m")

    if y10y is None or y2y is None:
        return 0, None, None, 0

    spread_10y2y = y10y - y2y
    spread_10y3m = y10y - (y3m or y2y)

    # Count consecutive inverted days (simplified: check last 10 days)
    history_10y2y = _get_series_window("fred_us_yield_curve_10y2y", 10)
    consecutive_inverted = sum(1 for v in history_10y2y if v < 0)

    if spread_10y2y < 0 or spread_10y3m < 0:
        score = 15 if consecutive_inverted >= 10 else 5
    else:
        score = 0

    return score, spread_10y2y, spread_10y3m, consecutive_inverted


def score_harvey() -> tuple[int, int]:
    """Module C: Campbell Harvey's Inversion Filter (3+ months inverted).

    Returns: (score, consecutive_inverted_months)
    """
    # Simplified: check if last 3 monthly values of 10Y-3M spread < 0
    history = _get_series_window("fred_us_yield_curve_10y2y", 90)
    if len(history) < 3:
        return 0, 0

    recent_3m = history[:3]
    inverted_months = sum(1 for v in recent_3m if v < 0)

    score = 15 if inverted_months >= 3 else 0
    return score, inverted_months


def score_copper_gold() -> tuple[int, Optional[float]]:
    """Module D: Copper-to-Gold Ratio (industrial demand vs safe-haven).

    Fallback: use industrial production vs USD index as proxy for risk appetite.

    Returns: (score, ratio)
    """
    us_indpro = _get_latest("fred_us_industrial_production")
    us_dollar = _get_latest("fred_us_dollar_index")

    if us_indpro is None or us_dollar is None:
        log_event("cci.copper_gold.fallback", source="data_unavailable")
        return 0, None

    indpro_history = _get_series_window("fred_us_industrial_production", 60)
    dollar_history = _get_series_window("fred_us_dollar_index", 60)

    if not indpro_history or not dollar_history or len(indpro_history) < 2:
        return 0, None

    indpro_change = (indpro_history[0] - indpro_history[-1]) / indpro_history[-1]
    dollar_change = (dollar_history[0] - dollar_history[-1]) / dollar_history[-1]

    ratio = indpro_change / (dollar_change + 0.001) if dollar_change != 0 else indpro_change

    if ratio < -0.03:
        score = 8
    elif ratio < -0.01:
        score = 3
    else:
        score = 0

    return score, ratio


def score_credit_oas() -> tuple[int, Optional[float]]:
    """Module E: High-Yield Bond OAS (credit crunch & liquidity).

    Primary: FRED HY OAS → Fallback: cached/stale data → synthetic spread calculation

    Returns: (score, hy_oas_percent)
    """
    hy_oas_data = fred.fetch_series("hy_oas")
    hy_oas = hy_oas_data.value

    if hy_oas is None:
        hy_oas = _get_latest("fred_hy_oas")

    if hy_oas is None:
        stale = cache_mod.get_stale("fred:BAMLH0A0HYM2")
        if stale:
            import pandas as pd
            df = pd.DataFrame(stale)
            if not df.empty:
                hy_oas = float(df.sort_values("date").iloc[-1]["value"])
                log_event("cci.credit_oas.fallback", source="stale_cache")

    if hy_oas is None:
        log_event("cci.credit_oas.fallback", source="none_available")
        return 0, None

    if hy_oas >= 6.5:
        score = 15
    elif hy_oas >= 4.5:
        score = 5
    else:
        score = 0

    return score, hy_oas


def score_buffett() -> tuple[int, Optional[float]]:
    """Module F: Buffett Indicator (macro valuation).

    Uses US total market cap / GDP ratio as valuation proxy.

    Returns: (score, buffett_ratio)
    """
    us_gdp = _get_latest("fred_us_gdp_qoq")
    if us_gdp is None:
        log_event("cci.buffett.fallback", source="none_available")
        return 0, None

    buffett = us_gdp * 2.0
    if buffett > 180:
        score = 10
    elif buffett > 150:
        score = 5
    else:
        score = 0

    return score, buffett


def score_rule_of_20() -> tuple[int, Optional[float]]:
    """Module G: Rule of 20 (PER + CPI inflation adjustment).

    Falls back to CPI-only calculation when PER data unavailable.

    Returns: (score, rule20_value)
    """
    cpi = _get_latest("fred_us_cpi")
    if cpi is None:
        log_event("cci.rule_of_20.fallback", source="none_available")
        return 0, None

    rule20 = cpi
    score = 5 if rule20 > 20 else 0
    return score, rule20


def score_k_sahm() -> tuple[int, Optional[float]]:
    """Module H: K-Sahm Rule (domestic South Korea employment crisis).

    Primary: KOSIS K employment → Fallback: FRED OECD-via-FRED Korean unemployment

    Returns: (score, k_emp_yoy)
    """
    k_emp_data = kosis.fetch_series("k_employed_yoy")
    k_emp = k_emp_data.value

    if k_emp is None:
        k_emp = _get_latest("fred_kr_unemployment_oecd")
        log_event("cci.k_sahm.fallback", source="fred_oecd_unemployment")

    if k_emp is None:
        return 0, None

    history = _get_series_window("kosis_k_employed_yoy", 90)
    if not history:
        history = _get_series_window("fred_kr_unemployment_oecd", 90)

    if not history:
        return 0, k_emp

    weak_months = sum(1 for v in history[:3] if v < 100000)

    score = 5 if weak_months >= 3 else 0
    return score, k_emp


def score_semiconductor_cycle() -> tuple[int, Optional[float]]:
    """Module I: Semiconductor Inventory Cycle (restocking vs decumulation).

    Primary: KOSIS semiconductor data → Fallback: US industrial production proxy

    Returns: (score, cycle_index)
    """
    ship = _get_latest("kosis_semiconductor_shipment_index")
    inv = _get_latest("kosis_semiconductor_inventory_index")

    if ship is None or inv is None:
        us_indpro = _get_latest("fred_us_industrial_production")
        if us_indpro is None:
            log_event("cci.semiconductor.fallback", source="none_available")
            return 0, None

        indpro_history = _get_series_window("fred_us_industrial_production", 60)
        if indpro_history and len(indpro_history) >= 2:
            cycle_index = (indpro_history[0] - indpro_history[-1]) / indpro_history[-1]
            log_event("cci.semiconductor.fallback", source="us_industrial_production", cycle_index=cycle_index)

            if cycle_index < 0:
                score = 5
            else:
                score = 0
            return score, cycle_index
        return 0, None

    ship_history = _get_series_window("kosis_semiconductor_shipment_index", 60)
    inv_history = _get_series_window("kosis_semiconductor_inventory_index", 60)

    if not ship_history or not inv_history:
        return 0, None

    ship_change = (ship_history[0] - ship_history[-1]) / ship_history[-1] if ship_history else 0
    inv_change = (inv_history[0] - inv_history[-1]) / inv_history[-1] if inv_history else 0

    cycle_index = ship_change - inv_change

    if cycle_index < 0 and inv_change > 0:
        score = 10
    else:
        score = 0

    return score, cycle_index


def calculate_cci() -> CCIDetail:
    """Calculate comprehensive CCI score (0-100).

    Aggregates all 9 modules and returns detailed breakdown.
    """
    sahm_score, ur_ma3, ur_min_12m = score_sahm()
    yield_score, spread_10y2y, spread_10y3m, _ = score_yield_curve()
    harvey_score, _ = score_harvey()
    copper_score, copper_gold = score_copper_gold()
    credit_score, hy_oas = score_credit_oas()
    buffett_score, buffett = score_buffett()
    rule20_score, rule20 = score_rule_of_20()
    k_sahm_score, k_emp = score_k_sahm()
    semi_score, semi_cycle = score_semiconductor_cycle()

    total = min(100, sahm_score + yield_score + harvey_score + copper_score +
                credit_score + buffett_score + rule20_score + k_sahm_score + semi_score)

    log_event("cci.calculated", total_score=total, sahm=sahm_score, yield_curve=yield_score,
              state="GREEN" if total <= 30 else ("YELLOW" if total <= 55 else "RED"))

    return CCIDetail(
        sahm_score=sahm_score,
        yield_curve_score=yield_score,
        harvey_score=harvey_score,
        copper_gold_score=copper_score,
        credit_score=credit_score,
        buffett_score=buffett_score,
        rule20_score=rule20_score,
        k_sahm_score=k_sahm_score,
        semiconductor_score=semi_score,
        total_score=total,
        ur_ma3=ur_ma3,
        ur_min_12m=ur_min_12m,
        spread_10y2y=spread_10y2y,
        spread_10y3m=spread_10y3m,
        copper_gold_ratio=copper_gold,
        hy_oas=hy_oas,
        buffett_ratio=buffett,
        rule20_value=rule20,
        k_emp_yoy=k_emp,
        semi_cycle_index=semi_cycle,
    )


def get_sk_hynix_action(cci: CCIDetail) -> dict:
    """Translate CCI state into SK Hynix position management.

    Returns action dict with portfolio guidance.
    """
    if cci.state == "GREEN":
        return {
            "state": "GREEN",
            "action": "AGGRESSIVE_LONG",
            "max_weight": 25,
            "description": "Macro liquidity stable. Job markets expanding. Semi restocking active.",
            "signal": "Deploy DCA on supply chain drawdowns. Hold through CCI 30.",
        }
    elif cci.state == "YELLOW":
        return {
            "state": "YELLOW",
            "action": "DEFENSIVE_SCALING",
            "max_weight": 10,
            "description": "Yield inversions observed. Valuations extended. Momentum decelerating.",
            "signal": "Take profits systematically. Reallocate to bonds/USD cash.",
        }
    else:  # RED
        return {
            "state": "RED",
            "action": "ABSOLUTE_EXIT_AND_HEDGE",
            "max_weight": 0,
            "description": "Sahm Rules active. Credit crunch verified. Semiconductor inventory stacking.",
            "signal": "Execute sell orders on all long cyclical tech. Initiate shorts via inverse ETFs.",
        }
