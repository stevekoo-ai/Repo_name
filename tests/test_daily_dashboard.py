"""docs/peos-daily.html generator (engine/report/daily_dashboard.py)."""
from __future__ import annotations

import json
import re

import pandas as pd
import pytest

from engine.report import daily_dashboard
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


def _extract_data_json(html_doc: str) -> dict:
    match = re.search(r"var PEOS_DAILY_DATA = (\{.*\});", html_doc)
    assert match, "PEOS_DAILY_DATA payload not found in rendered dashboard"
    return json.loads(match.group(1))


def test_indicator_chart_prefers_deep_raw_history_over_short_daily_rows(_history_csv, monkeypatch):
    """A raw source series (e.g. 10 years of GDP prints) should back the kr_gdp chart instead
    of the 2-row daily_history.csv fixture, once normalized data exists for it — this is what
    makes the 1개월/6개월/1년 period buttons show something other than the same 2 points."""
    deep_df = pd.DataFrame({
        "date": ["2016-01-01", "2020-01-01", "2026-07-15"],
        "value": [0.5, -1.2, 1.9],
    })

    def _fake_read_normalized(series_id):
        if series_id == "ecos_gdp_growth_qoq":
            return deep_df
        return pd.DataFrame(columns=["date", "value"])

    monkeypatch.setattr(daily_dashboard.collector_base, "read_normalized", _fake_read_normalized)

    html_doc = render_daily_dashboard(history_path=_history_csv)
    data = _extract_data_json(html_doc)

    gdp_series = data["series"]["kr_gdp"]
    assert gdp_series["dates"] == ["2016-01-01", "2020-01-01", "2026-07-15"]
    assert gdp_series["values"] == [0.5, -1.2, 1.9]
    assert "원시 데이터 기준" in html_doc


def test_indicator_chart_falls_back_to_daily_history_when_no_raw_series(_history_csv, monkeypatch):
    """Without normalized data for an indicator, its chart should still use the short
    daily_history.csv values (old behavior) rather than going blank."""
    monkeypatch.setattr(
        daily_dashboard.collector_base, "read_normalized",
        lambda series_id: pd.DataFrame(columns=["date", "value"]),
    )

    html_doc = render_daily_dashboard(history_path=_history_csv)
    data = _extract_data_json(html_doc)

    gdp_series = data["series"]["kr_gdp"]
    assert gdp_series["dates"] == ["2026-07-14", "2026-07-15"]
    assert gdp_series["values"] == [1.8, 1.9]
    assert "PEOS 계산값" in html_doc


def test_each_series_carries_its_own_dates_for_the_js_filter(_history_csv, monkeypatch):
    """The old implementation shared one global `dates` array across every chart, which is
    only correct if every series has the same cadence. Deep raw series (monthly/quarterly)
    and the daily PEOS history (one row/day) don't, so each chart_id's data must carry its
    own dates array rather than reusing a shared one."""
    deep_df = pd.DataFrame({"date": ["2016-01-01", "2020-01-01"], "value": [0.5, -1.2]})
    monkeypatch.setattr(
        daily_dashboard.collector_base, "read_normalized",
        lambda series_id: deep_df if series_id == "ecos_gdp_growth_qoq" else pd.DataFrame(columns=["date", "value"]),
    )

    html_doc = render_daily_dashboard(history_path=_history_csv)
    data = _extract_data_json(html_doc)

    assert data["series"]["kr_gdp"]["dates"] != data["series"]["kr_raw_score"]["dates"]
