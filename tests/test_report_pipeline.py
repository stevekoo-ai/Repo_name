"""Integration smoke test: full pipeline (Macro -> Personal -> Action -> Report)
using the real data/manual_inputs/*.yaml example fixtures, with all network-backed
collectors (ECOS/KOSIS/FRED/us_clock) short-circuited so the test is fast and
hermetic regardless of network availability (21.1: each engine independently
testable; this one exercises them wired together, per 21.2's "Report Section
생성 테스트").
"""
from __future__ import annotations

import pandas as pd
import pytest

from core.models import DataPoint, DataStatus
from engine.macro import indicators as indicators_mod
from engine.macro import snapshot as snapshot_mod
from engine.report import payload as payload_mod
from engine.report.html import render_html
from engine.report.markdown import render_markdown


@pytest.fixture(autouse=True)
def _isolated_storage(tmp_path, monkeypatch):
    import collectors.base as collector_base

    monkeypatch.setattr(collector_base, "RAW_DIR", tmp_path / "raw")
    monkeypatch.setattr(collector_base, "NORMALIZED_DIR", tmp_path / "normalized")
    monkeypatch.setattr(snapshot_mod, "SNAPSHOT_DIR", tmp_path / "snapshots")

    import core.cache as cache_mod
    monkeypatch.setattr(cache_mod, "CACHE_DIR", tmp_path / "cache")

    # No ECOS/KOSIS keys and no live network in test environments -> collectors
    # already degrade to Pending without a network call. FRED and the folded-in
    # investment-clock context *do* attempt live calls; short-circuit both so
    # the test doesn't depend on network reachability.
    monkeypatch.setattr(indicators_mod.fred, "fetch_all", lambda: {})
    monkeypatch.setattr("engine.macro.us_clock.get_investment_clock_context", lambda: None)
    yield


def test_full_pipeline_produces_a_readable_report():
    payload = payload_mod.build_report_payload(month_key="1999-01")

    assert payload["report_month"] == "1999-01"
    assert payload["report_readiness"] in ("draft", "final", "insufficient")
    assert payload["macro"]["regime"] in [
        "Recovery", "Early Expansion", "Expansion", "Late Expansion", "Slowdown", "Recession",
    ]
    assert len(payload["macro_dashboard"]) == 10
    assert isinstance(payload["actions"], list)
    for action in payload["actions"]:
        # 15.5: every action must carry all four required parts.
        assert action["title"] and action["reason"] and action["invalid_condition"] and action["recheck"]

    scenario_total = sum(payload["scenarios"][k]["probability"] for k in ("base", "bull", "bear"))
    assert scenario_total == 100

    markdown = render_markdown(payload)
    assert markdown.startswith("# 월간 PEOS 리포트 - 1999-01")
    for heading in ("Executive Summary", "Macro Dashboard", "Action Plan", "Personal Executive Brief"):
        assert heading in markdown

    assert isinstance(payload["discussion_points"], list)
    for point in payload["discussion_points"]:
        assert point["topic"] and point["context"] and point["question"]

    html_doc = render_html(payload)
    assert html_doc.startswith("<!doctype html>")
    assert html_doc.count("<section") == html_doc.count("</section>")
    for heading in ("Executive Summary", "Macro Dashboard", "Action Plan", "논의가 필요한 결정 사항"):
        assert heading in html_doc


def test_pipeline_marks_missing_indicators_as_pending_not_guessed():
    payload = payload_mod.build_report_payload(month_key="1999-02")
    pending_rows = [r for r in payload["macro_dashboard"] if r["status"] == DataStatus.PENDING.value]
    # ECOS/KOSIS have no key in the test environment, so GDP/CPI/PPI/etc. must
    # show up as Pending rather than silently defaulting to a fabricated value.
    assert any(r["indicator"] == "실질 GDP 성장률" for r in pending_rows)
    assert all(r["current"] is None for r in pending_rows)
