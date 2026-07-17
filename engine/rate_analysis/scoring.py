"""Interest rate scoring engine — evaluates US/KR yield dynamics and portfolio impact.

Implements 100-point scoring system:
  - Absolute Rate Level (30pts): Position of US 10Y and KR 10Y
  - Trend Analysis (30pts): Rate momentum over 1M and 3M windows
  - Yield Spread (25pts): US-KR differential vs 200~250bp target range
  - Market Signals (15pts): Yield curve inversion, financial conditions tightness

Score interpretation:
  - 85~100: Extreme easing (strong accommodation)
  - 70~85: Easing cycle
  - 55~70: Neutral to moderately accommodative (current: 68)
  - 40~55: Tightening cycle
  - 0~40: Extreme tightening (strong restriction)
"""
from __future__ import annotations

from datetime import timedelta
from dataclasses import dataclass
from typing import Optional

from collectors import fred, ecos
from core.models import DataPoint, DataStatus
from collectors import base as collector_base


@dataclass
class RateScoreDetail:
    """Detailed breakdown of rate scoring."""
    absolute_rate_score: int  # 0~30
    trend_score: int  # 0~30
    spread_score: int  # 0~25
    market_signal_score: int  # 0~15
    total_score: int  # 0~100

    us_10y: Optional[float] = None  # Current US 10Y Treasury rate
    kr_10y: Optional[float] = None  # Current KR 10Y Government Bond rate
    spread: Optional[float] = None  # US 10Y - KR 10Y (in basis points)
    trend_1m: Optional[float] = None  # 1-month rate change (in bp)
    trend_3m: Optional[float] = None  # 3-month trend
    us_10y_2y_spread: Optional[float] = None  # Yield curve (recession signal)


def _get_latest_rate(series_key: str, window_days: int = 1) -> Optional[float]:
    """Fetch latest rate from normalized data."""
    df = collector_base.read_normalized(f"fred_{series_key}" if "us_" in series_key else f"ecos_{series_key}")
    if df.empty:
        return None
    latest = df.sort_values("date").iloc[-1]
    return float(latest["value"]) if latest["value"] is not None else None


def _calculate_rate_change(series_key: str, days: int = 30) -> Optional[float]:
    """Calculate rate change over N days (in basis points)."""
    prefix = "fred_" if "us_" in series_key else "ecos_"
    df = collector_base.read_normalized(f"{prefix}{series_key}")
    if df.empty or len(df) < 2:
        return None

    df = df.sort_values("date")
    current = float(df.iloc[-1]["value"])

    # Find point N days ago (read_normalized returns "date" as datetime.date objects)
    target_date = df.iloc[-1]["date"] - timedelta(days=days)
    past_df = df[df["date"] <= target_date]

    if past_df.empty:
        return None

    past = float(past_df.iloc[-1]["value"])
    return (current - past) * 100  # Convert to basis points


def score_absolute_rates(us_10y: Optional[float], kr_10y: Optional[float]) -> int:
    """Score absolute rate levels (0~30 points).

    US 10Y scoring (0~15):
      4.5%+: 30pts, 3.5-4.5%: 25pts, 2.5-3.5%: 20pts, 1.5-2.5%: 15pts (baseline),
      0.5-1.5%: 10pts, <0.5%: 0pts

    KR 10Y scoring (0~15):
      3.5%+: 30pts, 3.0-3.5%: 25pts, 2.5-3.0%: 20pts, 2.0-2.5%: 15pts (baseline),
      1.5-2.0%: 10pts, <1.5%: 0pts
    """
    us_score = 0
    kr_score = 0

    # US 10Y scoring
    if us_10y is not None:
        if us_10y >= 4.5:
            us_score = 30
        elif us_10y >= 3.5:
            us_score = 25
        elif us_10y >= 2.5:
            us_score = 20
        elif us_10y >= 1.5:
            us_score = 15
        elif us_10y >= 0.5:
            us_score = 10
        else:
            us_score = 0

    # KR 10Y scoring
    if kr_10y is not None:
        if kr_10y >= 3.5:
            kr_score = 30
        elif kr_10y >= 3.0:
            kr_score = 25
        elif kr_10y >= 2.5:
            kr_score = 20
        elif kr_10y >= 2.0:
            kr_score = 15
        elif kr_10y >= 1.5:
            kr_score = 10
        else:
            kr_score = 0

    # Average of both
    if us_10y is not None and kr_10y is not None:
        return (us_score + kr_score) // 2
    elif us_10y is not None:
        return us_score
    elif kr_10y is not None:
        return kr_score
    else:
        return 0


def score_trend(us_1m_change: Optional[float], kr_1m_change: Optional[float],
                us_3m_trend: str, kr_3m_trend: str) -> int:
    """Score rate trend (0~30 points).

    1-month changes (0~15pts):
      - Similar movement: +5pts
      - One rising, one falling: -5pts penalty

    3-month trend (0~15pts):
      - Both rising (tightening): 10pts
      - Both falling (easing): 10pts
      - Mixed: 5pts
    """
    trend_1m_score = 0
    trend_3m_score = 0

    # 1-month trend scoring
    if us_1m_change is not None and kr_1m_change is not None:
        # Both rising
        if us_1m_change > 0 and kr_1m_change > 0:
            trend_1m_score = 5
        # Both falling
        elif us_1m_change < 0 and kr_1m_change < 0:
            trend_1m_score = 5
        # Opposite directions (divergence)
        else:
            trend_1m_score = -5

        # Add magnitude bonus
        if abs(us_1m_change) > 50 or abs(kr_1m_change) > 50:
            trend_1m_score += 5

        trend_1m_score = max(0, trend_1m_score)

    # 3-month trend scoring
    us_rising = us_3m_trend == "up"
    kr_rising = kr_3m_trend == "up"

    if us_rising == kr_rising:  # Same direction
        trend_3m_score = 10
    else:
        trend_3m_score = 5

    return trend_1m_score + trend_3m_score


def score_spread(spread_bp: Optional[float], spread_1m_change: Optional[float]) -> int:
    """Score US-KR yield spread (0~25 points).

    Absolute spread (0~15pts) — target: 200~250bp:
      <100bp: 0pts (KR too high), 100-150bp: 5pts, 150-200bp: 10pts,
      200-250bp: 15pts (ideal), 250-300bp: 15pts, 300-350bp: 10pts, >350bp: 5pts

    Spread momentum (0~10pts):
      Widening (expansion): +5pts (defensive)
      Narrowing (contraction): +5pts (risk-on)
      Stable (±10bp): +3pts (safe)
    """
    abs_score = 0
    momentum_score = 0

    # Absolute spread scoring
    if spread_bp is not None:
        if spread_bp < 100:
            abs_score = 0
        elif spread_bp < 150:
            abs_score = 5
        elif spread_bp < 200:
            abs_score = 10
        elif spread_bp <= 250:
            abs_score = 15
        elif spread_bp <= 300:
            abs_score = 15
        elif spread_bp <= 350:
            abs_score = 10
        else:
            abs_score = 5

    # Momentum scoring
    if spread_1m_change is not None:
        if -10 <= spread_1m_change <= 10:
            momentum_score = 3
        elif spread_1m_change > 0:
            momentum_score = min(10, 5 + (spread_1m_change // 25))  # Widening is defensive
        else:
            momentum_score = min(10, 5 + (abs(spread_1m_change) // 25))  # Narrowing is risk-on

    return abs_score + momentum_score


def score_market_signals(us_10y_2y_spread: Optional[float], inflation_signal: str = "normal") -> int:
    """Score market signals (0~15 points).

    US Yield Curve (0~10pts):
      Positive (>0): 10pts (normal), -0.25~0: 8pts (caution), -0.25~-0.5: 5pts (warning),
      <-0.5: 0pts (recession risk)

    Financial Conditions (0~5pts):
      Easing: 5pts, Neutral: 3pts, Tightening: 1pt
    """
    curve_score = 0
    condition_score = 0

    # Yield curve inversion signal
    if us_10y_2y_spread is not None:
        if us_10y_2y_spread > 0:
            curve_score = 10
        elif us_10y_2y_spread >= -0.25:
            curve_score = 8
        elif us_10y_2y_spread >= -0.5:
            curve_score = 5
        else:
            curve_score = 0

    # Financial conditions (simplified: based on rate level)
    if inflation_signal == "high":
        condition_score = 1  # Tightening
    elif inflation_signal == "moderate":
        condition_score = 3  # Neutral
    else:
        condition_score = 5  # Easing

    return curve_score + condition_score


def calculate_rate_score() -> RateScoreDetail:
    """Calculate comprehensive interest rate score (0~100 points).

    Fetches latest rates from FRED/ECOS collectors, computes trends,
    and returns detailed scoring breakdown.
    """
    # Fetch latest rates
    us_10y = _get_latest_rate("us_10y_treasury")
    kr_10y = _get_latest_rate("kr_10y_yield")
    us_2y = _get_latest_rate("us_2y_treasury")
    us_10y_2y = _get_latest_rate("us_yield_curve_10y2y")

    # Calculate changes
    us_1m_change = _calculate_rate_change("us_10y_treasury", days=30)
    kr_1m_change = _calculate_rate_change("kr_10y_yield", days=30)
    us_3m_change = _calculate_rate_change("us_10y_treasury", days=90)
    kr_3m_change = _calculate_rate_change("kr_10y_yield", days=90)

    # Calculate spread
    spread_bp = None
    spread_1m_change = None
    if us_10y is not None and kr_10y is not None:
        spread_bp = (us_10y - kr_10y) * 100

        # Calculate spread change
        us_1m = _calculate_rate_change("us_10y_treasury", days=30) or 0
        kr_1m = _calculate_rate_change("kr_10y_yield", days=30) or 0
        spread_1m_change = us_1m - kr_1m

    # Determine trends
    us_3m_trend = "up" if us_3m_change and us_3m_change > 0 else "down"
    kr_3m_trend = "up" if kr_3m_change and kr_3m_change > 0 else "down"

    # Calculate component scores
    abs_score = score_absolute_rates(us_10y, kr_10y)
    trend_score = score_trend(us_1m_change, kr_1m_change, us_3m_trend, kr_3m_trend)
    spread_score = score_spread(spread_bp, spread_1m_change)
    signal_score = score_market_signals(us_10y_2y)

    # Total score
    total = abs_score + trend_score + spread_score + signal_score

    return RateScoreDetail(
        absolute_rate_score=abs_score,
        trend_score=trend_score,
        spread_score=spread_score,
        market_signal_score=signal_score,
        total_score=min(100, total),  # Cap at 100
        us_10y=us_10y,
        kr_10y=kr_10y,
        spread=spread_bp,
        trend_1m=us_1m_change,
        trend_3m=us_3m_change,
        us_10y_2y_spread=us_10y_2y,
    )


def portfolio_recommendation(score: int) -> dict:
    """Generate portfolio allocation recommendation based on rate score.

    Score ranges:
      85~100: Extreme easing → Stocks 70% + Bonds 20% + Cash 10%
      70~85: Easing → Stocks 60% + Bonds 25% + Cash 15%
      55~70: Neutral → Stocks 50% + Bonds 30% + Cash 20% (current: 68)
      40~55: Tightening → Stocks 40% + Bonds 35% + Cash 25%
      0~40: Extreme tightening → Stocks 30% + Bonds 40% + Cash 30%
    """
    if score >= 85:
        return {
            "stocks": 70, "bonds": 20, "cash": 10,
            "condition": "Extreme easing — aggressive growth",
            "rebalance_trigger": 65,
        }
    elif score >= 70:
        return {
            "stocks": 60, "bonds": 25, "cash": 15,
            "condition": "Easing cycle — growth focused",
            "rebalance_trigger": 50,
        }
    elif score >= 55:
        return {
            "stocks": 50, "bonds": 30, "cash": 20,
            "condition": "Neutral to moderately accommodative — balanced",
            "rebalance_trigger": 40,
        }
    elif score >= 40:
        return {
            "stocks": 40, "bonds": 35, "cash": 25,
            "condition": "Tightening cycle — defensive",
            "rebalance_trigger": 30,
        }
    else:
        return {
            "stocks": 30, "bonds": 40, "cash": 30,
            "condition": "Extreme tightening — highly defensive",
            "rebalance_trigger": 55,
        }


def sk_hynix_outlook(score: int, spread_bp: Optional[float]) -> dict:
    """Generate SK Hynix outlook based on rate environment.

    Positive factors: Dollar strength (higher rates), AI demand
    Negative factors: Semiconductor cycle downturn, competition
    """
    outlook_3m = 50  # Base case: 50% probability of gains
    outlook_6m = 50
    outlook_12m = 55

    # Rate environment adjustment
    if score >= 75:  # Easing → Risk-on, good for tech
        outlook_3m += 15
        outlook_6m += 10
        outlook_12m += 5
    elif score >= 60:  # Neutral to accommodative
        outlook_3m += 10
        outlook_6m += 5
        outlook_12m += 5
    elif score <= 45:  # Tightening or recession risk
        outlook_3m -= 15
        outlook_6m -= 10
        outlook_12m -= 5

    # Spread adjustment (USD strength proxy)
    if spread_bp is not None:
        if spread_bp > 250:  # Wide spread = strong dollar = positive for SK Hynix exports
            outlook_3m += 5
            outlook_6m += 3
        elif spread_bp < 150:  # Narrow spread = weak dollar = negative
            outlook_3m -= 5
            outlook_6m -= 3

    outlook_3m = max(20, min(80, outlook_3m))  # Bound between 20~80%
    outlook_6m = max(20, min(80, outlook_6m))
    outlook_12m = max(20, min(80, outlook_12m))

    return {
        "3m_probability": outlook_3m,
        "6m_probability": outlook_6m,
        "12m_probability": outlook_12m,
        "rationale": _generate_hynix_rationale(score, spread_bp),
    }


def _generate_hynix_rationale(score: int, spread_bp: Optional[float]) -> str:
    """Generate text explanation of SK Hynix outlook."""
    if score >= 75:
        rate_factor = "Rate easing supports AI semiconductor demand"
    elif score >= 60:
        rate_factor = "Neutral rate environment maintains AI momentum"
    elif score >= 45:
        rate_factor = "Tightening rates pressure valuation multiples"
    else:
        rate_factor = "Extreme tightening threatens semiconductor cycle"

    if spread_bp is not None:
        if spread_bp > 250:
            spread_factor = "Wide US-KR spread (strong dollar) supports export competitiveness"
        elif spread_bp > 150:
            spread_factor = "Moderate spread maintains export margin"
        else:
            spread_factor = "Narrow spread (weak dollar) pressures export margins"
    else:
        spread_factor = "Spread data unavailable"

    return f"{rate_factor}. {spread_factor}."
