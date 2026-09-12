"""
Integration tests for the INCOME_REVIEW event added to
collectors/subscription_monitor/compose.py::run_pipeline() — the "앞으로
확인되는 모든 공공분양을 15건까지 직접 열어 확인" pipeline (사용자 요청
2026-09-13).

Mocks income_analysis.analyze_listing (no real Playwright/network) and
alerts._notify (no real email/GitHub issue), and redirects all three state
files to tmp_path so runs don't touch the repo's real state.
"""

import os
import sys
from datetime import datetime, timedelta, timezone

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "collectors", "subscription_monitor"))

import compose  # noqa: E402
import income_review_tracker  # noqa: E402

KST = timezone(timedelta(hours=9))
NOW = datetime(2026, 9, 13, 10, 0, tzinfo=KST)


def _row(id_, name, region="경기", days_offset=10):
    bgn = (NOW + timedelta(days=days_offset)).strftime("%Y-%m-%d")
    return {
        "HOUSE_MANAGE_NO": id_,
        "HOUSE_NM": name,
        "SUBSCRPT_AREA_CODE_NM": region,
        "RCEPT_BGNDE": bgn,
        "RCEPT_ENDDE": bgn,
        "HSSPLY_ADRES": f"{region} 어딘가",
    }


@pytest.fixture(autouse=True)
def isolated_state(tmp_path, monkeypatch):
    monkeypatch.setattr(compose, "STATE_PATH", str(tmp_path / "alerted_state.json"))
    monkeypatch.setattr(compose, "HEALTH_STATE_PATH", str(tmp_path / "health_state.json"))
    monkeypatch.setattr(income_review_tracker, "STATE_PATH", str(tmp_path / "income_review_state.json"))
    # Never actually send anything.
    monkeypatch.setattr(compose, "_send", lambda title, body, also_issue: None)
    yield


def _mock_analysis_ok(row):
    return {
        "status": "ok",
        "business_type": "국민주택형",
        "income_scope": "60㎡이하만검증",
        "percentages_found": [100, 140, 200],
        "exceptions": [],
        "pdf_url": "https://apply.lh.or.kr/example",
    }


def test_plain_new_listings_are_reviewed_and_counted(monkeypatch):
    monkeypatch.setattr(compose.income_analysis, "analyze_listing", _mock_analysis_ok)
    from judge import judge_listings

    rows = [_row(f"id{i}", f"단지{i}") for i in range(3)]
    verdicts = judge_listings(rows, NOW)

    fired = compose.run_pipeline(verdicts, healthy=True, now_kst=NOW, seoul_gyeonggi_count=3)

    assert fired["income_review"] == 3
    state = income_review_tracker.load_state()
    assert state["count"] == 3
    assert {r["id"] for r in state["reviews"]} == {"id0", "id1", "id2"}


def test_already_reviewed_listing_is_not_reopened_on_next_run(monkeypatch):
    calls = []

    def counting_analysis(row):
        calls.append(row["HOUSE_MANAGE_NO"])
        return _mock_analysis_ok(row)

    monkeypatch.setattr(compose.income_analysis, "analyze_listing", counting_analysis)
    from judge import judge_listings

    rows = [_row("id0", "단지0")]
    verdicts = judge_listings(rows, NOW)

    compose.run_pipeline(verdicts, healthy=True, now_kst=NOW, seoul_gyeonggi_count=1)
    compose.run_pipeline(verdicts, healthy=True, now_kst=NOW + timedelta(minutes=30), seoul_gyeonggi_count=1)

    assert calls == ["id0"]  # only opened once, not on the second run


def test_cap_stops_further_reviews_at_15(monkeypatch):
    monkeypatch.setattr(compose.income_analysis, "analyze_listing", _mock_analysis_ok)
    from judge import judge_listings

    rows = [_row(f"id{i}", f"단지{i}") for i in range(20)]
    verdicts = judge_listings(rows, NOW)

    fired = compose.run_pipeline(verdicts, healthy=True, now_kst=NOW, seoul_gyeonggi_count=20)

    assert fired["income_review"] == income_review_tracker.REVIEW_CAP
    state = income_review_tracker.load_state()
    assert state["count"] == income_review_tracker.REVIEW_CAP
    assert income_review_tracker.is_complete(state)


def test_keyword_match_counts_toward_cap_without_double_review(monkeypatch):
    """A NEW_MATCH (플랫폼시티/광교/원천동 keyword) listing must be counted
    exactly once toward the 15건 goal, not skipped by the general review
    pass nor double-counted."""
    calls = []

    def counting_analysis(row):
        calls.append(row["HOUSE_MANAGE_NO"])
        return _mock_analysis_ok(row)

    monkeypatch.setattr(compose.income_analysis, "analyze_listing", counting_analysis)
    from judge import judge_listings

    rows = [_row("id0", "광교신도시 A1블록 공공분양")]
    verdicts = judge_listings(rows, NOW)
    assert verdicts[0]["match_keyword"] == "광교"

    fired = compose.run_pipeline(verdicts, healthy=True, now_kst=NOW, seoul_gyeonggi_count=1)

    assert calls == ["id0"]
    assert fired["new_match"] == 1
    assert fired["income_review"] == 0  # handled inside the NEW_MATCH branch, not the general pass
    state = income_review_tracker.load_state()
    assert state["count"] == 1


def test_daily_digest_includes_progress_line(monkeypatch):
    monkeypatch.setattr(compose.income_analysis, "analyze_listing", _mock_analysis_ok)
    from judge import judge_listings

    rows = [_row("id0", "단지0")]
    verdicts = judge_listings(rows, NOW)
    now_after_heartbeat = NOW.replace(hour=9, minute=30)

    captured = {}

    def capture_send(title, body, also_issue):
        if "일일 요약" in title:
            captured["body"] = body

    monkeypatch.setattr(compose, "_send", capture_send)

    compose.run_pipeline(verdicts, healthy=True, now_kst=now_after_heartbeat, seoul_gyeonggi_count=1)

    assert "body" in captured
    assert "1회/15회" in captured["body"]
