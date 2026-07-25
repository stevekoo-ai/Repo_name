"""Shared numeric / date helpers used across collectors, indicators and engines."""
from __future__ import annotations

from datetime import date
from typing import Sequence

from .models import TrendPoint

TREND_WINDOWS_MONTHS = {
    "1m": 1,
    "3m": 3,
    "6m": 6,
    "12m": 12,
    "3y": 36,
    "5y": 60,
}


def safe_div(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def pct_change(current: float | None, previous: float | None) -> float | None:
    """Percent change, e.g. YoY / MoM growth rates. Returns None if inputs are missing."""
    if current is None or previous in (None, 0):
        return None
    return (current - previous) / abs(previous) * 100


def direction_of(change: float | None, flat_band: float = 0.0) -> str | None:
    if change is None:
        return None
    if change > flat_band:
        return "up"
    if change < -flat_band:
        return "down"
    return "flat"


def compute_trend(series: Sequence[tuple[date, float]], as_of_index: int = -1) -> dict[str, TrendPoint]:
    """Compute the 1M/3M/6M/12M/3Y/5Y trend set (9.3) for a monthly series.

    `series` must be sorted ascending by date and contain (date, value) tuples.
    Missing history for a window simply yields TrendPoint(change=None).
    """
    if not series:
        return {}
    series = list(series)
    idx = as_of_index if as_of_index >= 0 else len(series) + as_of_index
    current_value = series[idx][1]

    trends: dict[str, TrendPoint] = {}
    for window, months_back in TREND_WINDOWS_MONTHS.items():
        prior_idx = idx - months_back
        if prior_idx < 0:
            trends[window] = TrendPoint(window=window, change=None)
            continue
        prior_value = series[prior_idx][1]
        change = pct_change(current_value, prior_value)
        trends[window] = TrendPoint(window=window, change=change, direction=direction_of(change))
    return trends


def moving_average(values: Sequence[float | None], periods: int) -> float | None:
    clean = [v for v in values[-periods:] if v is not None]
    if not clean:
        return None
    return sum(clean) / len(clean)


def month_key(d: date) -> str:
    return f"{d.year:04d}-{d.month:02d}"


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
