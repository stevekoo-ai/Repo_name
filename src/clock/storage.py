"""Accumulate daily clock readings into data/history.csv.

Economic indicators here are monthly, so a run's `data_asof` (the latest
data month) will repeat across many daily `run_date`s until a new release
lands. We keep one row per run for a full audit trail, but the report /
charts dedupe on `data_asof` so the trend lines show real economic
history rather than a flat, revisit-heavy line.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .model import ClockReading

COLUMNS = [
    "run_date",
    "data_asof",
    "growth_value",
    "growth_change_3m",
    "growth_signal",
    "inflation_yoy",
    "inflation_change_3m",
    "inflation_signal",
    "phase",
    "asset",
    "core_cpi_yoy",
    "yield_curve_10y2y",
    "unemployment_rate",
]


def reading_to_row(reading: ClockReading, run_date: pd.Timestamp) -> dict:
    as_of = max(reading.growth.as_of, reading.inflation.as_of)
    return {
        "run_date": run_date.date().isoformat(),
        "data_asof": as_of.date().isoformat(),
        "growth_value": reading.growth.value,
        "growth_change_3m": reading.growth.change,
        "growth_signal": reading.growth.label,
        "inflation_yoy": reading.inflation.value,
        "inflation_change_3m": reading.inflation.change,
        "inflation_signal": reading.inflation.label,
        "phase": reading.phase["name"],
        "asset": reading.phase["asset"],
        "core_cpi_yoy": reading.context.get("core_cpi_yoy"),
        "yield_curve_10y2y": reading.context.get("yield_curve_10y2y"),
        "unemployment_rate": reading.context.get("unemployment_rate"),
    }


def append_history(history_path: str | Path, row: dict) -> pd.DataFrame:
    history_path = Path(history_path)
    if history_path.exists() and history_path.stat().st_size > 0:
        df = pd.read_csv(history_path)
    else:
        df = pd.DataFrame(columns=COLUMNS)

    # One row per run_date: replace if we already ran today, else append.
    df = df[df["run_date"] != row["run_date"]]
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df = df.sort_values("run_date").reset_index(drop=True)

    history_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(history_path, index=False)
    return df
