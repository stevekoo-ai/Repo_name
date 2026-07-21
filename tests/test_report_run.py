"""engine/report/run.py: writes report/<month>.* plus a dated report/<YYYY-MM-DD>.*
archive copy each run, so the full report (not just the lightweight daily-history
row) is retrievable per calendar day, not just as whatever the latest run left behind."""
from __future__ import annotations

import pytest

from core.models import DataPoint, DataStatus
from engine.macro import indicators as indicators_mod
from engine.macro import snapshot as snapshot_mod
from engine.report import daily_history as daily_history_mod
from engine.report import run as run_mod


@pytest.fixture(autouse=True)
def _isolated_storage(tmp_path, monkeypatch):
    import collectors.base as collector_base

    monkeypatch.setattr(collector_base, "RAW_DIR", tmp_path / "raw")
    monkeypatch.setattr(collector_base, "NORMALIZED_DIR", tmp_path / "normalized")
    monkeypatch.setattr(snapshot_mod, "SNAPSHOT_DIR", tmp_path / "snapshots")
    monkeypatch.setattr(run_mod, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(daily_history_mod, "DAILY_HISTORY_PATH", tmp_path / "peos_daily_history.csv")

    import core.cache as cache_mod
    monkeypatch.setattr(cache_mod, "CACHE_DIR", tmp_path / "cache")

    monkeypatch.setattr(indicators_mod.fred, "fetch_all", lambda: {})
    monkeypatch.setattr(
        indicators_mod.fred, "fetch_series",
        lambda series_key, ttl_seconds=None: DataPoint(series_id=series_key, status=DataStatus.PENDING,
                                                         note="network disabled in tests"),
    )
    monkeypatch.setattr("engine.macro.us_clock.get_investment_clock_context", lambda: None)
    yield


def test_run_writes_both_the_month_file_and_a_dated_archive_copy():
    paths = run_mod.run(month_key="1999-01", archive_date="1999-01-15")

    assert paths["html"].name == "1999-01.html"
    assert paths["markdown"].name == "1999-01.md"
    assert paths["daily_html"].name == "1999-01-15.html"
    assert paths["daily_markdown"].name == "1999-01-15.md"
    assert paths["daily_json"].name == "1999-01-15.json"

    assert paths["html"].read_text(encoding="utf-8") == paths["daily_html"].read_text(encoding="utf-8")
    assert paths["markdown"].read_text(encoding="utf-8") == paths["daily_markdown"].read_text(encoding="utf-8")


def test_run_can_skip_the_archive_copy():
    paths = run_mod.run(month_key="1999-01", archive=False)

    assert "daily_html" not in paths
    assert "daily_markdown" not in paths
    assert "daily_json" not in paths


def test_consecutive_daily_runs_each_leave_their_own_dated_file():
    run_mod.run(month_key="1999-01", archive_date="1999-01-15")
    run_mod.run(month_key="1999-01", archive_date="1999-01-16")

    out_dir = run_mod.REPO_ROOT / "report"
    assert (out_dir / "1999-01-15.md").exists()
    assert (out_dir / "1999-01-16.md").exists()
    # the month file only ever reflects the latest run, but both dated snapshots survive
    assert (out_dir / "1999-01.md").exists()
