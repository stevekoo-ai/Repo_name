"""engine/rate_analysis/scoring.py: calculate_rate_score() must actually fetch every
series it reads. kr_10y_yield had no caller anywhere in the pipeline (only kr_3y_yield
was fetched, by engine/macro/indicators.py), so the KR side of the US-KR spread always
read as unavailable regardless of network conditions — not a data problem, a wiring bug."""
from __future__ import annotations

import pandas as pd
import pytest

from core.models import DataPoint, DataStatus
from engine.rate_analysis import scoring as rate_scoring


@pytest.fixture(autouse=True)
def _isolated_storage(tmp_path, monkeypatch):
    import collectors.base as collector_base
    import core.cache as cache_mod

    monkeypatch.setattr(collector_base, "RAW_DIR", tmp_path / "raw")
    monkeypatch.setattr(collector_base, "NORMALIZED_DIR", tmp_path / "normalized")
    monkeypatch.setattr(cache_mod, "CACHE_DIR", tmp_path / "cache")
    yield


def test_calculate_rate_score_fetches_kr_10y_yield(monkeypatch):
    calls = []

    def _fake_fetch_series(series_key):
        calls.append(series_key)
        return DataPoint(series_id=series_key, status=DataStatus.PENDING, note="network disabled in tests")

    monkeypatch.setattr(rate_scoring.ecos, "fetch_series", _fake_fetch_series)

    rate_scoring.calculate_rate_score()

    assert "kr_10y_yield" in calls


def test_spread_is_computed_once_both_sides_of_normalized_data_exist(monkeypatch):
    """Regression guard: with real kr_10y_yield data present, the spread should compute —
    previously kr_10y stayed None forever because nothing ever populated this series."""
    import collectors.base as collector_base

    monkeypatch.setattr(rate_scoring.ecos, "fetch_series", lambda series_key: None)

    collector_base.append_normalized("fred_us_10y_treasury", [{"date": "2026-07-01", "value": 4.30}])
    collector_base.append_normalized("ecos_kr_10y_yield", [{"date": "2026-07-01", "value": 2.90}])

    detail = rate_scoring.calculate_rate_score()

    assert detail.us_10y == 4.30
    assert detail.kr_10y == 2.90
    assert detail.spread is not None
    assert round(detail.spread, 2) == 140.0
