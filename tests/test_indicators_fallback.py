"""KOSIS -> OECD-via-FRED fallback wiring (engine/macro/indicators.py).

KOSIS has been observed to intermittently time out from GitHub Actions IPs;
when that happens, the four KOSIS-sourced Core-10 indicators should fall
back to the OECD Main Economic Indicators series mirrored on FRED
(collectors/fred.py's kr_*_oecd entries) instead of silently going Pending.
No KOSIS_API_KEY is set in the test environment, so kosis.fetch_series
already returns Pending without a network call — exactly the "KOSIS
unreachable" case the fallback exists for.
"""
from __future__ import annotations

import pytest

from core.models import DataPoint, DataStatus, Frequency, Metadata
from engine.macro import indicators as indicators_mod


@pytest.fixture(autouse=True)
def _isolated_storage(tmp_path, monkeypatch):
    import collectors.base as collector_base
    monkeypatch.setattr(collector_base, "RAW_DIR", tmp_path / "raw")
    monkeypatch.setattr(collector_base, "NORMALIZED_DIR", tmp_path / "normalized")

    import core.cache as cache_mod
    monkeypatch.setattr(cache_mod, "CACHE_DIR", tmp_path / "cache")

    monkeypatch.setattr(indicators_mod.fred, "fetch_all", lambda: {})
    yield


def _monthly_rows(start_year: int, start_month: int, count: int, base: float, step: float) -> list[dict]:
    rows = []
    y, m = start_year, start_month
    for i in range(count):
        rows.append({"date": f"{y:04d}-{m:02d}-01", "value": base + step * i})
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return rows


def _stub_fred_fetch_series(monkeypatch, series_key: str, value: float):
    def _fake(key, ttl_seconds=None):
        if key == series_key:
            metadata = Metadata(source="OECD Main Economic Indicators", unit="index",
                                 frequency=Frequency.MONTHLY, reliability_grade=5,
                                 official=True, confidence=90.0)
            return DataPoint(series_id=key, status=DataStatus.OK, value=value, metadata=metadata)
        return DataPoint(series_id=key, status=DataStatus.PENDING)

    monkeypatch.setattr(indicators_mod.fred, "fetch_series", _fake)


def test_cpi_falls_back_to_oecd_when_kosis_unreachable(monkeypatch):
    import collectors.base as collector_base
    rows = _monthly_rows(2025, 1, 14, base=100.0, step=1.0)
    collector_base.append_normalized("fred_kr_cpi_oecd", rows)
    _stub_fred_fetch_series(monkeypatch, "kr_cpi_oecd", rows[-1]["value"])

    readings = indicators_mod.build_core10_readings()
    cpi = readings["cpi"]

    assert cpi.status == DataStatus.OK
    assert "OECD" in (cpi.source or "")
    assert cpi.detail["fields"]["yoy"] is not None
    assert "KOSIS" in cpi.detail["note"]


def test_unemployment_falls_back_to_oecd_when_kosis_unreachable(monkeypatch):
    import collectors.base as collector_base
    rows = _monthly_rows(2025, 1, 14, base=3.0, step=0.02)
    collector_base.append_normalized("fred_kr_unemployment_oecd", rows)
    _stub_fred_fetch_series(monkeypatch, "kr_unemployment_oecd", rows[-1]["value"])

    readings = indicators_mod.build_core10_readings()
    unemployment = readings["unemployment"]

    assert unemployment.status == DataStatus.OK
    assert "OECD" in (unemployment.source or "")
    assert unemployment.detail["fields"]["avg_3m_change"] is not None


def test_retail_sales_uses_oecd_mom_value_directly_when_kosis_unreachable(monkeypatch):
    _stub_fred_fetch_series(monkeypatch, "kr_retail_sales_mom_oecd", 0.7)

    readings = indicators_mod.build_core10_readings()
    retail = readings["retail_sales"]

    assert retail.status == DataStatus.OK
    assert retail.value == 0.7
    assert "OECD" in (retail.source or "")
    assert retail.detail["fields"]["mom"] == 0.7


def test_indicator_stays_pending_when_both_kosis_and_oecd_fail(monkeypatch):
    # kosis.fetch_series -> Pending (no key in test env); OECD mirror also
    # stubbed to fail, so the fallback should degrade cleanly to Pending
    # rather than crash or fabricate a value (7.9's "never guess").
    monkeypatch.setattr(
        indicators_mod.fred, "fetch_series",
        lambda key, ttl_seconds=None: DataPoint(series_id=key, status=DataStatus.SOURCE_ERROR),
    )

    readings = indicators_mod.build_core10_readings()
    cpi = readings["cpi"]

    assert cpi.status != DataStatus.OK
    assert cpi.value is None
