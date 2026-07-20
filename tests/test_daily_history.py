"""Daily history accumulation (engine/report/daily_history.py) — the CSV
that backs docs/peos-daily.html's multi-timeframe trend view."""
from __future__ import annotations

import pandas as pd
import pytest

from engine.report import daily_history


@pytest.fixture(autouse=True)
def _isolated_path(tmp_path, monkeypatch):
    monkeypatch.setattr(daily_history, "DAILY_HISTORY_PATH", tmp_path / "peos_daily_history.csv")
    yield


def _payload(run_month_score=1, kr_regime="Recovery", us_regime="Recession"):
    return {
        "macro": {"regime": kr_regime, "score": run_month_score, "confidence": 80.0},
        "macro_us": {"regime": us_regime, "score": -2, "confidence": 75.0},
        "personal": {
            "investment_environment_score": 70.1, "semiconductor_score": 79.6,
            "bond_score": 40.0, "fx_score": 32.9, "housing_readiness_score": 60.4,
        },
        "macro_dashboard": [
            {"key": "gdp", "current": 1.8}, {"key": "cpi", "current": None},
        ],
        "us_macro_dashboard": [
            {"key": "gdp", "current": 2.9}, {"key": "unemployment", "current": 4.1},
        ],
    }


def test_build_daily_row_flattens_indicators_with_market_prefix():
    row = daily_history.build_daily_row(_payload(), run_date="2026-07-15")
    assert row["run_date"] == "2026-07-15"
    assert row["kr_regime"] == "Recovery"
    assert row["us_regime"] == "Recession"
    assert row["kr_gdp"] == 1.8
    assert row["kr_cpi"] is None
    assert row["us_gdp"] == 2.9
    assert row["us_unemployment"] == 4.1
    assert row["investment_environment_score"] == 70.1


def test_append_daily_history_writes_and_accumulates():
    path = daily_history.append_daily_history(_payload(kr_regime="Recovery"), run_date="2026-07-14")
    daily_history.append_daily_history(_payload(kr_regime="Early Expansion"), run_date="2026-07-15")

    df = pd.read_csv(path)
    assert list(df["run_date"]) == ["2026-07-14", "2026-07-15"]
    assert list(df["kr_regime"]) == ["Recovery", "Early Expansion"]


def test_append_daily_history_dedupes_same_day_keeping_latest():
    daily_history.append_daily_history(_payload(kr_regime="Recovery"), run_date="2026-07-15")
    path = daily_history.append_daily_history(_payload(kr_regime="Expansion"), run_date="2026-07-15")

    df = pd.read_csv(path)
    assert len(df) == 1
    assert df.iloc[0]["kr_regime"] == "Expansion"
