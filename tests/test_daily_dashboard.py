"""docs/peos-daily.html generator (engine/report/daily_dashboard.py)."""
from __future__ import annotations

import pandas as pd
import pytest

from engine.report.daily_dashboard import render_daily_dashboard


@pytest.fixture
def _history_csv(tmp_path):
    df = pd.DataFrame([
        {
            "run_date": "2026-07-14", "kr_regime": "Recovery", "kr_raw_score": 1, "kr_confidence": 80.0,
            "us_regime": "Expansion", "us_raw_score": 2, "us_confidence": 75.0,
            "investment_environment_score": 65.0, "semiconductor_score": 79.6,
            "bond_score": 40.0, "fx_score": 32.9, "housing_readiness_score": 60.4,
            "kr_gdp": 1.8, "kr_cpi": None, "us_gdp": 2.9, "us_unemployment": 4.1,
        },
        {
            "run_date": "2026-07-15", "kr_regime": "Early Expansion", "kr_raw_score": 2, "kr_confidence": 82.0,
            "us_regime": "Recession", "us_raw_score": -1, "us_confidence": 70.0,
            "investment_environment_score": 70.1, "semiconductor_score": 80.1,
            "bond_score": 41.0, "fx_score": 30.0, "housing_readiness_score": 60.4,
            "kr_gdp": 1.9, "kr_cpi": 2.5, "us_gdp": -0.5, "us_unemployment": 4.4,
        },
    ])
    path = tmp_path / "peos_daily_history.csv"
    df.to_csv(path, index=False)
    return path


def test_render_daily_dashboard_smoke(_history_csv):
    html_doc = render_daily_dashboard(history_path=_history_csv)

    assert html_doc.startswith("<!doctype html>")
    assert html_doc.count("<section") == html_doc.count("</section>")
    assert "PEOS Daily Dashboard" in html_doc
    assert "period-toggle" in html_doc
    # regime changed between the two rows -> should show up in the history table
    assert "Early Expansion" in html_doc
    assert "Recession" in html_doc


def test_render_daily_dashboard_handles_missing_history_file(tmp_path):
    html_doc = render_daily_dashboard(history_path=tmp_path / "does_not_exist.csv")
    assert html_doc.startswith("<!doctype html>")
    assert "국면 변경 이력" in html_doc
