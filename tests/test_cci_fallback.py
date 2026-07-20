"""Test CCI fallback logic: when primary data is missing, use alternatives or cached data."""
from __future__ import annotations

import pandas as pd
import pytest

from core.models import DataPoint, DataStatus
from engine.crisis_analysis import scoring as cci_scoring


@pytest.fixture(autouse=True)
def _isolated_storage(tmp_path, monkeypatch):
    import collectors.base as collector_base
    import core.cache as cache_mod

    monkeypatch.setattr(collector_base, "RAW_DIR", tmp_path / "raw")
    monkeypatch.setattr(collector_base, "NORMALIZED_DIR", tmp_path / "normalized")
    monkeypatch.setattr(cache_mod, "CACHE_DIR", tmp_path / "cache")

    from collectors import fred
    monkeypatch.setattr(fred, "fetch_series",
        lambda series_key, ttl_seconds=None: DataPoint(
            series_id=series_key, status=DataStatus.PENDING,
            note="network disabled in tests"))
    yield


def test_cci_handles_missing_unemployment_data():
    """score_sahm() should return 0 score when US unemployment data unavailable."""
    score, ma3, min_12m = cci_scoring.score_sahm()
    assert score == 0
    assert ma3 is None
    assert min_12m is None


def test_cci_handles_missing_yield_curve_data():
    """score_yield_curve() should return 0 score when treasury data unavailable."""
    score, spread_10y2y, spread_10y3m, consecutive_inverted = cci_scoring.score_yield_curve()
    assert score == 0
    assert spread_10y2y is None
    assert spread_10y3m is None


def test_cci_handles_missing_credit_oas_data():
    """score_credit_oas() should return 0 score when HY OAS data unavailable."""
    score, hy_oas = cci_scoring.score_credit_oas()
    assert score == 0
    assert hy_oas is None


def test_cci_handles_missing_copper_gold_data():
    """score_copper_gold() should return 0 score when commodity proxy data unavailable."""
    score, ratio = cci_scoring.score_copper_gold()
    assert score == 0
    assert ratio is None


def test_cci_handles_missing_buffett_data():
    """score_buffett() should return 0 score when GDP data unavailable."""
    score, buffett = cci_scoring.score_buffett()
    assert score == 0
    assert buffett is None


def test_cci_handles_missing_semiconductor_data():
    """score_semiconductor_cycle() should return 0 when KOSIS and US data unavailable."""
    score, cycle_index = cci_scoring.score_semiconductor_cycle()
    assert score == 0
    assert cycle_index is None


def test_cci_handles_missing_k_sahm_data():
    """score_k_sahm() should return 0 score when Korean employment data unavailable."""
    score, k_emp = cci_scoring.score_k_sahm()
    assert score == 0
    assert k_emp is None


def test_calculate_cci_returns_all_zeros_when_all_data_missing():
    """calculate_cci() should gracefully return all 0 scores when all data unavailable."""
    cci = cci_scoring.calculate_cci()

    assert cci.total_score == 0
    assert cci.state == "GREEN"
    assert cci.sahm_score == 0
    assert cci.yield_curve_score == 0
    assert cci.harvey_score == 0
    assert cci.copper_gold_score == 0
    assert cci.credit_score == 0
    assert cci.buffett_score == 0
    assert cci.rule20_score == 0
    assert cci.k_sahm_score == 0
    assert cci.semiconductor_score == 0


def test_cci_state_transitions():
    """CCI state should transition based on score thresholds."""
    cci_green = cci_scoring.CCIDetail(
        sahm_score=0, yield_curve_score=0, harvey_score=0,
        copper_gold_score=0, credit_score=0, buffett_score=0,
        rule20_score=0, k_sahm_score=0, semiconductor_score=0,
        total_score=20)
    assert cci_green.state == "GREEN"

    cci_yellow = cci_scoring.CCIDetail(
        sahm_score=10, yield_curve_score=10, harvey_score=10,
        copper_gold_score=0, credit_score=0, buffett_score=0,
        rule20_score=0, k_sahm_score=0, semiconductor_score=0,
        total_score=40)
    assert cci_yellow.state == "YELLOW"

    cci_red = cci_scoring.CCIDetail(
        sahm_score=20, yield_curve_score=15, harvey_score=15,
        copper_gold_score=8, credit_score=15, buffett_score=10,
        rule20_score=5, k_sahm_score=5, semiconductor_score=10,
        total_score=100)
    assert cci_red.state == "RED"
