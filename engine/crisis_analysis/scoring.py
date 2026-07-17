"""Comprehensive Crisis Index (CCI) scoring engine — 9 modules consolidated.

Modules A-I evaluate global macro state and output 0-100 score:
- 0-30 (GREEN): Expansion, capital injection
- 31-55 (YELLOW): Deceleration, capital hedging
- 56-100 (RED): Systemic breakdown, capital evacuation
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from collectors import base as collector_base
from collectors import fred, ecos, kosis
from core.logger import log_event


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


def _get_latest(series_id: str, days_back: int = 1) -> Optional[float]:
    """Fetch latest value from normalized collector data."""
    df = collector_base.read_normalized(series_id)
    if df.empty:
        return None
    latest = df.sort_values("date").iloc[-1]
    return float(latest["value"]) if latest["value"] is not None else None


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

    Returns: (score, ma3, min_12m)
    """
    ur_data = fred.fetch_series("us_unemployment")
    if ur_data.value is None:
        return 0, None, None

    ma3 = _moving_avg("fred_us_unemployment", window=3)
    min_12m = _min_window("fred_us_unemployment", months=12)

    if ma3 is None or min_12m is None:
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

    Returns: (score, ratio)
    """
    # Fallback: use synthetic copper/gold proxies or return 0 if unavailable
    # In real environment would fetch from Yahoo Finance
    ratio = None

    # For now, return neutral score if data unavailable
    return 0, ratio


def score_credit_oas() -> tuple[int, Optional[float]]:
    """Module E: High-Yield Bond OAS (credit crunch & liquidity).

    Returns: (score, hy_oas_percent)
    """
    hy_oas_data = fred.fetch_series("hy_oas")
    if hy_oas_data.value is None:
        return 0, None

    hy_oas = hy_oas_data.value
    if hy_oas >= 6.5:
        score = 15
    elif hy_oas >= 4.5:
        score = 5
    else:
        score = 0

    return score, hy_oas


def score_buffett() -> tuple[int, Optional[float]]:
    """Module F: Buffett Indicator (macro valuation).

    Returns: (score, buffett_ratio)
    """
    # TMC and GDP would need specialized data sources
    # For now, return neutral if unavailable
    return 0, None


def score_rule_of_20() -> tuple[int, Optional[float]]:
    """Module G: Rule of 20 (PER + CPI inflation adjustment).

    Returns: (score, rule20_value)
    """
    # PER_M would need market data; CPI from FRED
    cpi = _get_latest("fred_us_cpi")
    if cpi is None:
        return 0, None

    # Without PER data, use CPI as proxy for inflation component
    rule20 = cpi  # Simplified

    score = 5 if rule20 > 20 else 0
    return score, rule20


def score_k_sahm() -> tuple[int, Optional[float]]:
    """Module H: K-Sahm Rule (domestic South Korea employment crisis).

    Returns: (score, k_emp_yoy)
    """
    k_emp_data = kosis.fetch_series("k_employed_yoy")
    if k_emp_data.value is None:
        return 0, None

    k_emp = k_emp_data.value

    # Check if 3+ consecutive months of weak job growth
    history = _get_series_window("kosis_k_employed_yoy", 90)
    weak_months = sum(1 for v in history[:3] if v < 100000)

    score = 5 if weak_months >= 3 else 0
    return score, k_emp


def score_semiconductor_cycle() -> tuple[int, Optional[float]]:
    """Module I: Semiconductor Inventory Cycle (restocking vs decumulation).

    Returns: (score, cycle_index)
    """
    ship = _get_latest("kosis_semiconductor_shipment_index")
    inv = _get_latest("kosis_semiconductor_inventory_index")

    if ship is None or inv is None:
        return 0, None

    # Simplified: cycle index = shipment_change - inventory_change
    ship_history = _get_series_window("kosis_semiconductor_shipment_index", 60)
    inv_history = _get_series_window("kosis_semiconductor_inventory_index", 60)

    ship_change = (ship_history[0] - ship_history[-1]) / ship_history[-1] if ship_history else 0
    inv_change = (inv_history[0] - inv_history[-1]) / inv_history[-1] if inv_history else 0

    cycle_index = ship_change - inv_change

    # Inventory rising + shipments falling = overstock risk (RED)
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
