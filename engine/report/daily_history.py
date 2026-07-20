"""Daily history accumulation for docs/peos-daily.html (the multi-timeframe
trend dashboard — 오늘/1주일/1개월/6개월/1년/전체 — from opening the same page
every day). One row per calendar day in data/peos_daily_history.csv, covering
every KR/US Core-10/Core-Macro indicator value plus the composite scores.
This is a different thing from the monthly report's 10-year sparklines,
which track each *raw source series* — this tracks PEOS's own computed
regime/scores day over day, which isn't captured anywhere else.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
DAILY_HISTORY_PATH = REPO_ROOT / "data" / "peos_daily_history.csv"


def _indicator_values(dashboard_rows: list[dict], prefix: str) -> dict[str, float | None]:
    return {f"{prefix}_{row['key']}": row.get("current") for row in dashboard_rows}


def build_daily_row(payload: dict, run_date: str | None = None) -> dict:
    run_date = run_date or date.today().isoformat()
    macro, macro_us, p = payload["macro"], payload["macro_us"], payload["personal"]

    row = {
        "run_date": run_date,
        "kr_regime": macro["regime"],
        "kr_raw_score": macro["score"],
        "kr_confidence": macro["confidence"],
        "us_regime": macro_us["regime"],
        "us_raw_score": macro_us["score"],
        "us_confidence": macro_us["confidence"],
        "investment_environment_score": p.get("investment_environment_score"),
        "semiconductor_score": p.get("semiconductor_score"),
        "bond_score": p.get("bond_score"),
        "fx_score": p.get("fx_score"),
        "housing_readiness_score": p.get("housing_readiness_score"),
    }
    row.update(_indicator_values(payload["macro_dashboard"], "kr"))
    row.update(_indicator_values(payload["us_macro_dashboard"], "us"))
    return row


def load_history_json(history_path: Path | None = None) -> dict:
    """Read the accumulated daily history into the plain-dict shape the
    report's client-side period-toggle JS expects (html.py's
    _section_period_trends): dates, per-metric numeric series, and the two
    categorical regime series kept separate since they're not chartable as
    lines but drive the period judgment summary (dominant regime, change
    count)."""
    history_path = history_path or DAILY_HISTORY_PATH
    if not history_path.exists() or history_path.stat().st_size == 0:
        return {"dates": [], "series": {}, "regimes": {"kr_regime": [], "us_regime": []}}

    df = pd.read_csv(history_path).sort_values("run_date").reset_index(drop=True)
    dates = df["run_date"].tolist()
    numeric_cols = [c for c in df.columns if c not in ("run_date", "kr_regime", "us_regime")]
    series = {col: [None if pd.isna(v) else float(v) for v in df[col]] for col in numeric_cols}
    regimes = {
        "kr_regime": [None if pd.isna(v) else str(v) for v in df["kr_regime"]] if "kr_regime" in df else [],
        "us_regime": [None if pd.isna(v) else str(v) for v in df["us_regime"]] if "us_regime" in df else [],
    }
    return {"dates": dates, "series": series, "regimes": regimes}


def append_daily_history(payload: dict, run_date: str | None = None) -> Path:
    row = build_daily_row(payload, run_date)
    DAILY_HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    new_df = pd.DataFrame([row])
    if DAILY_HISTORY_PATH.exists() and DAILY_HISTORY_PATH.stat().st_size > 0:
        existing = pd.read_csv(DAILY_HISTORY_PATH)
        combined = pd.concat([existing, new_df], ignore_index=True)
    else:
        combined = new_df

    combined = (
        combined.drop_duplicates(subset=["run_date"], keep="last")
        .sort_values("run_date")
        .reset_index(drop=True)
    )
    combined.to_csv(DAILY_HISTORY_PATH, index=False)
    return DAILY_HISTORY_PATH
