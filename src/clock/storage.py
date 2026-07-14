"""Persist the full historical reading table into data/history.csv.

The model recomputes every historical month's reading from FRED's currently
published series on every run (cheap — it's a few hundred rows of pandas
math, not the network fetch). So instead of appending one row per day, we
just overwrite history.csv with the freshly computed full table each time,
stamping a `last_updated` column for transparency. This is what backfills
decades of history the first time this runs, and keeps every row in sync
with the latest data revisions afterwards.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

COLUMNS = [
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
    "last_updated",
]


def write_full_history(history_path: str | Path, full_history: pd.DataFrame, run_date: pd.Timestamp) -> pd.DataFrame:
    history_path = Path(history_path)
    df = full_history.copy()
    df["data_asof"] = pd.to_datetime(df["data_asof"]).dt.date.astype(str)
    df["last_updated"] = run_date.date().isoformat()
    df = df[COLUMNS].sort_values("data_asof").reset_index(drop=True)

    history_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(history_path, index=False)
    return df
