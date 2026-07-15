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


def _momentum_series(df: pd.DataFrame, lookback: int = LOOKBACK_MONTHS) -> pd.DataFrame:
    """date/value/change/label for every row where a `lookback`-period-earlier value exists.

    This is the vectorized form of the "rising if higher than N periods ago"
    rule, used both for the single latest Signal and for backfilling every
    historical month at once.
    """
    df = df.sort_values("date").reset_index(drop=True)
    out = df.copy()
    out["change"] = out["value"] - out["value"].shift(lookback)
    out = out.dropna(subset=["change"]).reset_index(drop=True)
    out["label"] = out["change"].apply(lambda c: "rising" if c > 0 else "falling")
    return out[["date", "value", "change", "label"]]


def _yoy(df: pd.DataFrame) -> pd.DataFrame:
    """Convert a monthly level series to a year-over-year % change series."""
    df = df.sort_values("date").reset_index(drop=True)
    out = df.copy()
    out["value"] = out["value"].pct_change(periods=12) * 100
    return out.dropna(subset=["value"]).reset_index(drop=True)


def _select_growth_frame(series: dict[str, pd.DataFrame]) -> pd.DataFrame:
    if "growth_primary" in series and len(series["growth_primary"]) > LOOKBACK_MONTHS:
        return series["growth_primary"][["date", "value"]]
    return _yoy(series["growth_fallback"])


def _signal_from_momentum(momentum: pd.DataFrame) -> Signal:
    if momentum.empty:
        raise ValueError("not enough history to compute momentum")
    last = momentum.iloc[-1]
    return Signal(label=last["label"], value=float(last["value"]), change=float(last["change"]), as_of=last["date"])


def compute_growth_signal(series: dict[str, pd.DataFrame]) -> Signal:
    return _signal_from_momentum(_momentum_series(_select_growth_frame(series)))


def compute_inflation_signal(series: dict[str, pd.DataFrame]) -> Signal:
    return _signal_from_momentum(_momentum_series(_yoy(series["inflation_primary"])))


def build_full_history(series: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Compute a growth/inflation/phase reading for every historical month.

    Uses the currently-published (revised) FRED series, not real-time
    vintages, so a month's *retrospective* reading here can differ slightly
    from what the model would have said if run live back then (data
    revisions). Good enough for spotting the historical pattern of phases.
    """
    growth = _momentum_series(_select_growth_frame(series)).rename(
        columns={"value": "growth_value", "change": "growth_change_3m", "label": "growth_signal"}
    )
    inflation = _momentum_series(_yoy(series["inflation_primary"])).rename(
        columns={"value": "inflation_yoy", "change": "inflation_change_3m", "label": "inflation_signal"}
    )

    full = pd.merge(growth, inflation, on="date", how="inner").sort_values("date").reset_index(drop=True)
    full["phase"] = full.apply(lambda r: PHASES[(r["growth_signal"], r["inflation_signal"])]["name"], axis=1)
    full["asset"] = full.apply(lambda r: PHASES[(r["growth_signal"], r["inflation_signal"])]["asset"], axis=1)

    if "inflation_confirm" in series and len(series["inflation_confirm"]) > 12:
        core = _yoy(series["inflation_confirm"]).rename(columns={"value": "core_cpi_yoy"})[["date", "core_cpi_yoy"]]
        full = pd.merge_asof(full, core.sort_values("date"), on="date", direction="backward")
    else:
        full["core_cpi_yoy"] = None

    if "context_yield_curve" in series and not series["context_yield_curve"].empty:
        yc = series["context_yield_curve"].rename(columns={"value": "yield_curve_10y2y"}).sort_values("date")
        full = pd.merge_asof(full, yc, on="date", direction="backward")
    else:
        full["yield_curve_10y2y"] = None

    if "context_unemployment" in series and not series["context_unemployment"].empty:
        ur = series["context_unemployment"].rename(columns={"value": "unemployment_rate"}).sort_values("date")
        full = pd.merge_asof(full, ur, on="date", direction="backward")
    else:
        full["unemployment_rate"] = None

    return full.rename(columns={"date": "data_asof"})


def read_clock(series: dict[str, pd.DataFrame]) -> ClockReading:
    full = build_full_history(series)
    if full.empty:
        raise ValueError("not enough overlapping history to compute a reading")
    last = full.iloc[-1]

    growth = Signal(label=last["growth_signal"], value=float(last["growth_value"]),
                     change=float(last["growth_change_3m"]), as_of=last["data_asof"])
    inflation = Signal(label=last["inflation_signal"], value=float(last["inflation_yoy"]),
                        change=float(last["inflation_change_3m"]), as_of=last["data_asof"])
    phase = PHASES[(growth.label, inflation.label)]

    context = {}
    for key in ("core_cpi_yoy", "yield_curve_10y2y", "unemployment_rate"):
        if pd.notna(last.get(key)):
            context[key] = float(last[key])

    return ClockReading(growth=growth, inflation=inflation, phase=phase, context=context)
