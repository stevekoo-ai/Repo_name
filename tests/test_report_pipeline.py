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
from engine.report.html_new import render_html
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
    # the test doesn't depend on network reachability. fetch_series also needs
    # stubbing directly — indicators.py's KOSIS-unreachable fallback calls it
    # (not just fetch_all) to try the OECD-via-FRED mirror.
    monkeypatch.setattr(indicators_mod.fred, "fetch_all", lambda: {})
    monkeypatch.setattr(
        indicators_mod.fred, "fetch_series",
        lambda series_key, ttl_seconds=None: DataPoint(series_id=series_key, status=DataStatus.PENDING,
                                                         note="network disabled in tests"),
    )
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
    assert markdown.startswith("# PEOS 일일 리포트 - 1999-01")
    # 2026-09-10 — "Macro Dashboard"는 5섹션 개편 때 "1. 거시 경제 대시보드"로
    # **이름만** 바뀌었는데(내용은 한국/미국 거시 상황 그대로) 이 단정이 옛
    # 영문 헤딩에 묶여 있어 계속 실패하고 있었다. 나머지 세 헤딩은 legacy
    # Appendix에 그대로 남아 있어 영문 그대로 둔다.
    for heading in ("Executive Summary", "1. 거시 경제 대시보드", "Action Plan",
                    "Personal Executive Brief"):
        assert heading in markdown

    assert isinstance(payload["discussion_points"], list)
    for point in payload["discussion_points"]:
        assert point["id"] and point["topic"] and point["context"] and point["question"]

    # 2026-09-10 — engine/report/html.py를 삭제하고 이 단정을 production
    # 렌더러(html_new.py)로 옮겼다. 지운 쪽은 아무 데서도 호출되지 않는
    # 죽은 코드였는데, 여기서만 테스트되고 있어 "검증된 렌더러"처럼
    # 보였다. Executive Summary·Action Plan·논의사항은 그 파일에만 있던
    # 섹션이라 삭제 전에 html_new로 이식했다 — 그래서 아래 단정이 그대로
    # 성립한다(이번엔 실제로 발송되는 리포트에 대해).
    html_doc = render_html(payload)
    assert html_doc.startswith("<!DOCTYPE html>")
    assert html_doc.count("<div") == html_doc.count("</div>")
    for heading in ("Executive Summary", "Action Plan", "논의가 필요한 결정 사항"):
        assert heading in html_doc


def test_macro_dashboard_renders_10y_trend_and_feedback_ui(tmp_path):
    import collectors.base as collector_base

    # Simulate 10 years of monthly GDP history already sitting in the
    # normalized tier (as it would after collectors/ecos.py's widened
    # 10-year fetch window runs against a live API), independent of whether
    # a prior monthly PEOS snapshot exists.
    dates = pd.date_range("2016-07-01", periods=40, freq="QS")
    rows = [{"date": d.strftime("%Y-%m-%d"), "value": 1.0 + i * 0.05} for i, d in enumerate(dates)]
    collector_base.append_normalized("ecos_gdp_growth_qoq", rows)

    payload = payload_mod.build_report_payload(month_key="1999-03")

    gdp_row = next(r for r in payload["macro_dashboard"] if r["indicator"] == "실질 GDP 성장률")
    assert len(gdp_row["history"]) >= 2
    assert gdp_row["previous"] is not None
    assert gdp_row["previous_source"] == "series_history"

    html_doc = render_html(payload)
    assert 'class="spark"' in html_doc
    assert 'class="discuss-input"' in html_doc or "이번 달은 별도로 논의가 필요한 항목이 없습니다" in html_doc
    assert "peosCopyOne" in html_doc and "peosIssueOne" in html_doc and "peosCopyAll" in html_doc


def test_pipeline_marks_missing_indicators_as_pending_not_guessed():
    payload = payload_mod.build_report_payload(month_key="1999-02")
    pending_rows = [r for r in payload["macro_dashboard"] if r["status"] == DataStatus.PENDING.value]
    # ECOS/KOSIS have no key in the test environment, so GDP/CPI/PPI/etc. must
    # show up as Pending rather than silently defaulting to a fabricated value.
    assert any(r["indicator"] == "실질 GDP 성장률" for r in pending_rows)
    assert all(r["current"] is None for r in pending_rows)


def test_the_production_html_renderer_also_produces_a_usable_report():
    """⚠ 2026-09-10 발견 — 위 test_full_pipeline_produces_a_readable_report는
    `engine/report/html.py`의 render_html을 검증하는데, **매일 실제로 발송·
    게시되는 리포트를 만드는 건 `engine/report/html_new.py`** 다
    (run.py 34행: `from .html_new import render_html`).

    즉 production 렌더러엔 파이프라인 테스트가 없었다. html.py::render_html은
    이 테스트 파일에서만 호출되고, 그 모듈이 살아 있는 실질적 이유는
    daily_dashboard/real_estate_dashboard가 재사용하는 _CSS·_esc 뿐이다.

    두 렌더러를 통합하거나 한쪽을 정리하는 건 별건이라, 여기서는 최소한
    **실제로 나가는 렌더러가 깨지지 않는지**를 고정한다."""
    from engine.report.html_new import render_html as render_production_html

    payload = payload_mod.build_report_payload(month_key="1999-04")
    html_doc = render_production_html(payload)

    assert html_doc.startswith("<!DOCTYPE html>")
    assert html_doc.rstrip().endswith("</html>")
    assert html_doc.count("<div") == html_doc.count("</div>"), "div 짝이 안 맞는다"
    # 이 리포트의 뼈대 — 하나라도 빠지면 사용자가 받는 페이지가 반쪽이 된다
    for marker in ("PEOS 일일 리포트", "포지션", "위기지수"):
        assert marker in html_doc, marker
