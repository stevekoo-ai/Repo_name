"""
Tests for collectors/subscription_monitor/fetch_and_render.py::merge_catchup_rows()
— the narrow-window-notice catch-up fix (2026-10-14).

사용자 "소득요건 자동검증 진행에 대해서 재조사해봐" 요청으로 90일 전국
재조회를 돌린 결과, 접수기간이 단 하루(08-03~08-04)였던 수원당수지구
A5블록이 alerted_state.json에 전혀 없었음을 발견 — fetch_all()의
RCEPT_ENDDE>=today 필터만 쓰면 접수창이 극히 짧은 공고는 30분 폴링
사이클이 "열려있는" 그 짧은 창을 못 맞추면 영원히 놓친다. 이 테스트는
그 보완책(merge_catchup_rows, fetch_recent_announcements)의 핵심 병합
로직만 검증 — 실제 HTTP 호출은 하지 않는다(기존 프로젝트 컨벤션,
network-touching 함수는 순수 로직만 단위테스트).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "collectors", "subscription_monitor"))

from fetch_and_render import merge_catchup_rows  # noqa: E402


def _row(id_, name):
    return {"HOUSE_MANAGE_NO": id_, "HOUSE_NM": name}


def test_no_overlap_keeps_both_sets():
    open_rows = [_row("id1", "단지1")]
    recent_rows = [_row("id2", "단지2")]
    merged = merge_catchup_rows(open_rows, recent_rows)
    assert {r["HOUSE_MANAGE_NO"] for r in merged} == {"id1", "id2"}


def test_duplicate_id_not_added_twice():
    """id2는 이미 '현재 접수중'으로 잡혔으니 catch-up 쪽에서 또 들어오면
    안 된다 — 중복이 judge_listings/run_pipeline로 두 번 들어가면 안 됨."""
    open_rows = [_row("id1", "단지1"), _row("id2", "단지2")]
    recent_rows = [_row("id2", "단지2(다른 필드값일 수도)"), _row("id3", "단지3")]
    merged = merge_catchup_rows(open_rows, recent_rows)
    ids = [r["HOUSE_MANAGE_NO"] for r in merged]
    assert ids.count("id2") == 1
    assert set(ids) == {"id1", "id2", "id3"}


def test_open_row_wins_on_duplicate_not_recent_row():
    """중복일 때 open_rows(최신 fetch)의 데이터를 쓰고, recent_rows 쪽
    사본은 버린다."""
    open_rows = [_row("id1", "단지1-최신")]
    recent_rows = [_row("id1", "단지1-과거버전")]
    merged = merge_catchup_rows(open_rows, recent_rows)
    assert len(merged) == 1
    assert merged[0]["HOUSE_NM"] == "단지1-최신"


def test_empty_recent_rows_is_noop():
    open_rows = [_row("id1", "단지1")]
    merged = merge_catchup_rows(open_rows, [])
    assert merged == open_rows


def test_empty_open_rows_still_adds_all_recent():
    """현재 접수중인 건이 0건이어도(오늘 대시보드처럼) catch-up 건은
    여전히 검토 대상에 들어가야 한다."""
    recent_rows = [_row("id1", "단지1"), _row("id2", "단지2")]
    merged = merge_catchup_rows([], recent_rows)
    assert len(merged) == 2


def test_falls_back_to_pblanc_no_when_house_manage_no_missing():
    open_rows = [{"PBLANC_NO": "p1", "HOUSE_NM": "단지1"}]
    recent_rows = [{"PBLANC_NO": "p1", "HOUSE_NM": "단지1-중복"}, {"PBLANC_NO": "p2", "HOUSE_NM": "단지2"}]
    merged = merge_catchup_rows(open_rows, recent_rows)
    assert len(merged) == 2
