"""Merrill Lynch Investment Clock phase logic.

Two axes:
  - Growth momentum: rising or falling, from an output-gap-style proxy
    (OECD Composite Leading Indicator for the US; industrial production
    YoY as a fallback if the CLI series is unavailable).
  - Inflation momentum: rising or falling, from CPI YoY acceleration.

Momentum is measured as a 3-month change: if the indicator today is higher
than it was 3 months ago, momentum is "rising", otherwise "falling". This is
the standard operationalization used in Merrill Lynch / sell-side writeups
of the clock (see references in README).

Four phases, clockwise:
  12 o'clock  Reflation    growth falling, inflation falling   -> Bonds
   3 o'clock  Recovery     growth rising,  inflation falling   -> Equities
   6 o'clock  Overheat     growth rising,  inflation rising    -> Commodities
   9 o'clock  Stagflation  growth falling, inflation rising    -> Cash
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

PHASES = {
    ("falling", "falling"): {
        "name": "Reflation",
        "name_kr": "리플레이션(경기침체/저물가)",
        "asset": "Bonds",
        "asset_kr": "채권",
        "hour": 12,
        "color": "#4C72B0",
    },
    ("rising", "falling"): {
        "name": "Recovery",
        "name_kr": "회복",
        "asset": "Equities",
        "asset_kr": "주식",
        "hour": 3,
        "color": "#55A868",
    },
    ("rising", "rising"): {
        "name": "Overheat",
        "name_kr": "과열",
        "asset": "Commodities",
        "asset_kr": "원자재",
        "hour": 6,
        "color": "#C44E52",
    },
    ("falling", "rising"): {
        "name": "Stagflation",
        "name_kr": "스태그플레이션",
        "asset": "Cash",
        "asset_kr": "현금",
        "hour": 9,
        "color": "#8172B2",
    },
}

LOOKBACK_MONTHS = 3


@dataclass
class Signal:
    label: str  # "rising" or "falling"
    value: float
    change: float
    as_of: pd.Timestamp


@dataclass
class ClockReading:
    growth: Signal
    inflation: Signal
    phase: dict
    context: dict


def _momentum_signal(df: pd.DataFrame, lookback: int = LOOKBACK_MONTHS) -> Signal:
    """Rising if the latest value exceeds the value `lookback` periods earlier."""
    df = df.sort_values("date").reset_index(drop=True)
    if len(df) <= lookback:
        raise ValueError("not enough history to compute momentum")
    latest = df.iloc[-1]
    prior = df.iloc[-1 - lookback]
    change = latest["value"] - prior["value"]
    label = "rising" if change > 0 else "falling"
    return Signal(label=label, value=float(latest["value"]), change=float(change), as_of=latest["date"])


def _yoy(df: pd.DataFrame) -> pd.DataFrame:
    """Convert a monthly level series to a year-over-year % change series."""
    df = df.sort_values("date").reset_index(drop=True)
    out = df.copy()
    out["value"] = out["value"].pct_change(periods=12) * 100
    return out.dropna(subset=["value"]).reset_index(drop=True)


def compute_growth_signal(series: dict[str, pd.DataFrame]) -> Signal:
    if "growth_primary" in series and len(series["growth_primary"]) > LOOKBACK_MONTHS:
        return _momentum_signal(series["growth_primary"])
    return _momentum_signal(_yoy(series["growth_fallback"]))


def compute_inflation_signal(series: dict[str, pd.DataFrame]) -> Signal:
    cpi_yoy = _yoy(series["inflation_primary"])
    return _momentum_signal(cpi_yoy)


def read_clock(series: dict[str, pd.DataFrame]) -> ClockReading:
    growth = compute_growth_signal(series)
    inflation = compute_inflation_signal(series)
    phase = PHASES[(growth.label, inflation.label)]

    context = {}
    if "context_yield_curve" in series and not series["context_yield_curve"].empty:
        context["yield_curve_10y2y"] = float(series["context_yield_curve"].sort_values("date").iloc[-1]["value"])
    if "context_unemployment" in series and not series["context_unemployment"].empty:
        context["unemployment_rate"] = float(series["context_unemployment"].sort_values("date").iloc[-1]["value"])
    if "inflation_confirm" in series and len(series["inflation_confirm"]) > 12:
        core_yoy = _yoy(series["inflation_confirm"])
        context["core_cpi_yoy"] = float(core_yoy.iloc[-1]["value"])

    return ClockReading(growth=growth, inflation=inflation, phase=phase, context=context)
