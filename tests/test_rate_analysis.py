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


def test_spread_is_computed_once_both_sides_of_normalized_data_exist(monkeypatch, tmp_path):
    """Regression guard: with real kr_10y_yield data present, the spread should compute —
    previously kr_10y stayed None forever because nothing ever populated this series.

    2026-09-10 — 이 테스트는 저장소의 **진짜** data/normalized/에 2026-07-01
    행을 심고 그게 최신값이길 기대했다. 실수집이 2026-09까지 늘어나자
    _get_latest_rate()가 진짜 최신값을 집어와 깨졌다.

    격리하고 나니 두 번째 원인이 드러났다 — 심어둔 2026-07-01이 71일 전이라
    **신선도 가드(MAX_RATE_AGE_DAYS=45)에 걸려** None이 됐다. 그건 production이
    옳게 동작한 것이다(R2). 진짜 원인은 **테스트가 날짜를 하드코딩한 것**이라,
    격리된 디렉터리 + 오늘 기준 날짜로 바꿔 시간이 지나도 안 깨지게 한다.
    검증 의도(양쪽 데이터가 있으면 스프레드가 계산된다)는 그대로다.
    """
    from datetime import date as _date

    import collectors.base as collector_base

    today = _date.today().isoformat()

    monkeypatch.setattr(rate_scoring.ecos, "fetch_series", lambda series_key: None)
    monkeypatch.setattr(collector_base, "NORMALIZED_DIR", tmp_path)

    collector_base.append_normalized("fred_us_10y_treasury", [{"date": today, "value": 4.30}])
    collector_base.append_normalized("ecos_kr_10y_yield", [{"date": today, "value": 2.90}])

    detail = rate_scoring.calculate_rate_score()

    assert detail.us_10y == 4.30
    assert detail.kr_10y == 2.90
    assert detail.spread is not None
    assert round(detail.spread, 2) == 140.0
