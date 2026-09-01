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


def test_buffett_and_rule20_are_permanently_disabled_even_with_data():
    """2026-09-01: user asked '위기지수 분석의 기타항목에 5는 뭐야? 왜 계속 같은
    값이야?' — the '5' was Rule of 20 scoring a structurally-guaranteed max
    every day (it compared a CPI *index level* (~330, base year=100) against a
    threshold of 20, which real CPI levels can never fall below). Buffett had
    the mirror-image bug: it compared quarterly GDP growth (~1.5%) against a
    150/180 threshold no realistic growth rate can ever reach, so it was
    structurally guaranteed to always be 0. Neither module has a real data
    source (PER, market-cap/GDP) in this repo, so both must now return
    (0, None) unconditionally — even when the (wrong) proxy series they used
    to consult has data that would have tripped the old broken threshold."""
    import collectors.base as collector_base

    # Seed values that would have triggered the OLD broken formulas (CPI
    # index >20 is true for any real CPI reading; GDP QoQ here is set
    # deliberately far past the old 150 threshold to prove even an extreme
    # value can't revive the disabled scoring).
    collector_base.append_normalized("fred_us_cpi", [{"date": "2026-08-01", "value": 330.5}])
    collector_base.append_normalized("fred_us_gdp_qoq", [{"date": "2026-08-01", "value": 200.0}])

    score, value = cci_scoring.score_rule_of_20()
    assert (score, value) == (0, None), "Rule of 20 must stay disabled regardless of CPI data"

    score, value = cci_scoring.score_buffett()
    assert (score, value) == (0, None), "Buffett must stay disabled regardless of GDP data"


def test_k_sahm_scores_from_real_kosis_series_not_mismatched_fallback_units():
    """2026-09-01 bug fix: the old code compared whichever series was
    available (KOSIS employment YoY % OR the FRED unemployment-rate %
    fallback) against a single threshold (`v < 100000`) meant for neither —
    any realistic percentage is always below 100000, so the fallback path
    was one KOSIS-history-length away from always scoring 5. This pins two
    behaviors: (a) with a real KOSIS YoY history, 3 consecutive negative
    months score 5; (b) with only the FRED fallback, the score stays 0 and
    the fallback value is returned purely as reference info."""
    import collectors.base as collector_base
    from datetime import date, timedelta

    # (a) Real KOSIS series with 3 consecutive negative (YoY declining) months,
    # well within the 90-day window score_k_sahm() reads.
    today = date.today()
    for days_ago, v in [(60, -1.2), (30, -0.8), (5, -0.3)]:
        d = (today - timedelta(days=days_ago)).isoformat()
        collector_base.append_normalized("kosis_k_employed_yoy", [{"date": d, "value": v}])

    import collectors.kosis as kosis_mod
    original_fetch = kosis_mod.fetch_series

    def fake_fetch(series_key):
        return DataPoint(series_id=series_key, status=DataStatus.OK, value=-0.3)

    kosis_mod.fetch_series = fake_fetch
    try:
        score, k_emp = cci_scoring.score_k_sahm()
    finally:
        kosis_mod.fetch_series = original_fetch

    assert score == 5, "3 consecutive negative KOSIS YoY months must score as weak"
    assert k_emp == -0.3


def test_k_sahm_fallback_value_is_informational_only_not_scored():
    """Without the real KOSIS series, the FRED unemployment-rate fallback must
    never drive a score — only surface as reference info (score stays 0)."""
    import collectors.base as collector_base

    collector_base.append_normalized("fred_kr_unemployment_oecd", [{"date": "2026-07-01", "value": 2.8}])

    score, value = cci_scoring.score_k_sahm()
    assert score == 0, "fallback (unrelated metric) must never score — only inform"
    assert value == 2.8


def test_series_as_of_reports_staleness_without_a_freshness_cutoff():
    """2026-09-01: _get_series_window() silently drops values older than its
    window (e.g. 60 days), while _get_latest() returns them anyway with zero
    signal about their age — this exact mismatch is what made
    score_semiconductor_cycle()'s fallback go quietly empty when
    fred_us_industrial_production was 62 days stale (just past the 60-day
    window) despite _get_latest() reporting it as 'the latest value' with no
    complaint. _series_as_of() must report the value AND how old it is,
    with no cutoff of its own."""
    import collectors.base as collector_base
    from datetime import date, timedelta

    old_date = (date.today() - timedelta(days=90)).isoformat()
    collector_base.append_normalized("fred_us_industrial_production", [{"date": old_date, "value": 102.9}])

    value, as_of, days_stale = cci_scoring._series_as_of("fred_us_industrial_production")
    assert value == 102.9
    assert as_of == old_date
    assert days_stale == 90, "a 90-day-old point must be reported as 90 days old, not silently dropped"


def test_module_data_quality_distinguishes_primary_fallback_no_data():
    """calculate_cci()'s data_quality must tell apart a module reading its
    1st-priority series (PRIMARY), one that had to use its fallback series
    (FALLBACK), and one with neither (NO_DATA) — this is the freshness
    signal the CCI report was missing entirely (user: '데이터 신선도가 표시가
    없네!')."""
    import collectors.base as collector_base

    # sahm: primary series present -> PRIMARY.
    collector_base.append_normalized("fred_us_unemployment", [{"date": "2026-08-01", "value": 4.1}])
    # semiconductor: primary (KOSIS) absent, fallback (US indpro) present -> FALLBACK.
    collector_base.append_normalized("fred_us_industrial_production", [{"date": "2026-08-01", "value": 103.0}])
    # credit_oas: nothing seeded at all -> NO_DATA.

    quality = cci_scoring._module_data_quality("sahm")
    assert quality["quality"] == "PRIMARY"
    assert quality["series"] == "fred_us_unemployment"
    assert quality["days_stale"] is not None

    quality = cci_scoring._module_data_quality("semiconductor")
    assert quality["quality"] == "FALLBACK"
    assert quality["series"] == "fred_us_industrial_production"

    quality = cci_scoring._module_data_quality("credit_oas")
    assert quality == {"quality": "NO_DATA", "series": None, "as_of": None, "days_stale": None}

    # buffett/rule_of_20 have no reference series at all (permanently disabled).
    assert cci_scoring._module_data_quality("buffett")["quality"] == "NO_DATA"
    assert cci_scoring._module_data_quality("rule_of_20")["quality"] == "NO_DATA"


def test_calculate_cci_includes_data_quality_for_all_nine_modules():
    """calculate_cci()'s returned CCIDetail must always carry a data_quality
    entry for every one of the 9 modules, even when all underlying data is
    missing (this test's fixture leaves storage empty) — an absent key would
    silently break the report's freshness column instead of showing ⛔."""
    cci = cci_scoring.calculate_cci()
    expected_modules = {"sahm", "yield_curve", "harvey", "copper_gold", "credit_oas",
                        "buffett", "rule_of_20", "k_sahm", "semiconductor"}
    assert set(cci.data_quality.keys()) == expected_modules
    for module, q in cci.data_quality.items():
        assert q["quality"] == "NO_DATA", f"{module} should be NO_DATA with empty storage"


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
