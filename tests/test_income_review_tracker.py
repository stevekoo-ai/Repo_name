"""
Tests for collectors/subscription_monitor/income_review_tracker.py — the
15건 누적 소득요건 검증 카운터 (사용자 요청 2026-09-13).

collectors/subscription_monitor/*.py are run as standalone scripts (no
__init__.py), so we add that directory to sys.path directly, matching
tests/test_subscription_income_analysis.py's pattern.
"""

import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "collectors", "subscription_monitor"))

import income_review_tracker as tracker  # noqa: E402

KST = timezone(timedelta(hours=9))
NOW = datetime(2026, 9, 13, 10, 0, tzinfo=KST)


def _ok_analysis(exceptions=None):
    return {
        "status": "ok",
        "business_type": "국민주택형",
        "income_scope": "60㎡이하만검증",
        "percentages_found": [100, 140, 200],
        "exceptions": exceptions or [],
        "pdf_url": "https://apply.lh.or.kr/example",
    }


def _failed_analysis():
    return {"status": "failed", "stage": "discover", "reason": "검색 결과 없음"}


def test_fresh_state_is_empty_and_not_complete():
    state = {"count": 0, "reviews": []}
    assert not tracker.is_complete(state)
    assert tracker.progress_label(state) == "0회/15회"


def test_record_increments_count_and_returns_entry():
    state = {"count": 0, "reviews": []}
    entry = tracker.record(state, "id1", "테스트단지", "경기", None, NOW, _ok_analysis())
    assert state["count"] == 1
    assert entry["id"] == "id1"
    assert entry["status"] == "ok"
    assert entry["income_scope"] == "60㎡이하만검증"
    assert tracker.progress_label(state) == "1회/15회"


def test_already_reviewed_prevents_double_counting():
    state = {"count": 0, "reviews": []}
    tracker.record(state, "id1", "테스트단지", "경기", None, NOW, _ok_analysis())
    assert tracker.already_reviewed(state, "id1")
    assert not tracker.already_reviewed(state, "id2")


def test_failed_analysis_still_counts_as_one_review():
    """A discover/parse failure still consumed one look at the notice — it's
    not silently retried forever, matching income_analysis.py's own
    graceful-degradation philosophy (a human looks at failures instead)."""
    state = {"count": 0, "reviews": []}
    entry = tracker.record(state, "id1", "테스트단지", "경기", None, NOW, _failed_analysis())
    assert state["count"] == 1
    assert entry["status"] == "failed"
    assert entry["reason"] == "검색 결과 없음"


def test_is_complete_at_cap():
    state = {"count": 0, "reviews": []}
    for i in range(tracker.REVIEW_CAP):
        tracker.record(state, f"id{i}", f"단지{i}", "경기", None, NOW, _ok_analysis())
    assert state["count"] == tracker.REVIEW_CAP
    assert tracker.is_complete(state)
    assert tracker.progress_label(state) == f"{tracker.REVIEW_CAP}회/{tracker.REVIEW_CAP}회"


def test_progress_label_caps_display_even_if_count_somehow_exceeds():
    state = {"count": tracker.REVIEW_CAP + 3, "reviews": []}
    assert tracker.progress_label(state) == f"{tracker.REVIEW_CAP}회/{tracker.REVIEW_CAP}회"


def test_exception_count_only_counts_entries_with_exceptions():
    state = {"count": 0, "reviews": []}
    tracker.record(state, "id1", "단지1", "경기", None, NOW, _ok_analysis())
    tracker.record(state, "id2", "단지2", "경기", None, NOW, _ok_analysis(exceptions=["새 배율값 발견: 175%"]))
    tracker.record(state, "id3", "단지3", "경기", None, NOW, _failed_analysis())
    assert tracker.exception_count(state) == 1


def test_load_state_missing_file_returns_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(tracker, "STATE_PATH", str(tmp_path / "does_not_exist.json"))
    state = tracker.load_state()
    assert state == {"count": 0, "reviews": []}


def test_save_then_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(tracker, "STATE_PATH", str(tmp_path / "income_review_state.json"))
    state = {"count": 0, "reviews": []}
    tracker.record(state, "id1", "단지1", "경기", "광교", NOW, _ok_analysis())
    tracker.save_state(state)

    reloaded = tracker.load_state()
    assert reloaded["count"] == 1
    assert reloaded["reviews"][0]["id"] == "id1"
    assert reloaded["reviews"][0]["keyword"] == "광교"
