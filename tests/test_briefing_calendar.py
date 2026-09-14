"""engine/briefing/calendar.py — 휴장·시차 인지 + 다음주 예정 일정.

사용자 요청 두 가지를 코드로 고정한다:
  1. "한국·미국 거래 없는 날을 알고, 그게 서로에게 time delay로 어떻게
     작용할지 의견에 포함돼야 한다" → describe_trading_gap()
  2. "주말 보고서에는 다음주 예정 일정을 미리 알려달라" → upcoming_events(),
     pattern_events(), context.build_weekly_outlook_block()
"""
from datetime import date

import pytest

from engine.briefing import calendar as C
from engine.briefing import context as CTX
from engine.briefing import ledger as L


@pytest.fixture(autouse=True)
def _isolated_ledger(monkeypatch, tmp_path):
    monkeypatch.setattr(L, "LEDGER", tmp_path / "ledger.csv")


# ── 거래일 판정 ──────────────────────────────────────────────

def test_weekend_is_never_a_trading_day():
    saturday = date(2026, 9, 12)
    sunday = date(2026, 9, 13)
    assert not C.is_trading_day("KR", saturday)
    assert not C.is_trading_day("US", sunday)


def test_registered_kr_holiday_is_not_a_trading_day():
    # 2026-08-15 광복절
    assert not C.is_trading_day("KR", date(2026, 8, 15))


def test_registered_us_holiday_is_not_a_trading_day():
    # 2026-01-01 New Year's Day
    assert not C.is_trading_day("US", date(2026, 1, 1))


def test_ordinary_weekday_is_a_trading_day():
    # 2026-09-11 (금) — 휴장일 아님
    assert C.is_trading_day("KR", date(2026, 9, 11))
    assert C.is_trading_day("US", date(2026, 9, 11))


def test_kr_and_us_holidays_are_independent():
    """한 시장의 휴장이 다른 시장까지 휴장으로 잘못 판정하면 안 된다."""
    # 2026-07-17 제헌절은 한국만 휴장, 미국은 정상 개장(금요일)
    d = date(2026, 7, 17)
    assert not C.is_trading_day("KR", d)
    assert C.is_trading_day("US", d)


# ── 시차 서술 ────────────────────────────────────────────────

def test_am_notes_long_us_holiday_gap():
    """미국이 연휴로 이틀 이상 쉬었으면 AM 브리핑이 그 사실을 명시해야
    한다 — 안 그러면 '어젯밤' 서술이 실제로는 며칠 치 뉴스를 하루로 뭉갠다.

    ⚠️ 이 테스트는 원래 `assert "휴장" in note.text or note.lag_days_us >= 0`
    이었다. `lag_days_us`는 `max(gap, 0)`이라 **항상 0 이상** — 즉 뒷조건이
    무조건 참이라 **절대 실패할 수 없는 테스트**였다. 그래서 2026-09-14에
    "gap이 평일엔 항상 -1로 계산돼 휴장 경고가 한 번도 뜰 수 없던" 버그를
    통과시켰다. 이제 텍스트와 숫자를 둘 다 단정한다."""
    # 2026-09-08(화) 기준 직전 세션은 노동절(9/7 월)을 건너뛴 9/4(금).
    note = C.describe_trading_gap(date(2026, 9, 8), "AM")
    assert note.us_last_trading == date(2026, 9, 4), "직전 미국 세션 판정이 틀렸다"
    assert note.lag_days_us == 3, "주말(2일)+노동절(1일) = 3일 갭이어야 한다"
    assert "휴장" in note.text


def test_am_after_a_weekend_flags_the_two_day_gap():
    """2026-09-14(월) 실제 사고 재현. 이날 AM은 '정상 시차' 판정을 받아
    주말 이틀치 뉴스(AI 속도조절론)를 조사 대상에서 빠뜨렸고, 그날
    코스피는 그 재료로 -3.26% 급락했다."""
    note = C.describe_trading_gap(date(2026, 9, 14), "AM")
    assert note.us_last_trading == date(2026, 9, 11), "월요일 아침의 직전 미국 세션은 금요일이다"
    assert note.lag_days_us == 2
    assert "정상 시차" not in note.text, "주말 뒤 월요일을 '정상 시차'로 부르면 안 된다"
    assert "조사 대상 기간" in note.text


def test_ordinary_weekday_am_is_normal_lag():
    """갭 경고가 매일 뜨면 경고가 아니게 된다 — 평시엔 조용해야 한다."""
    note = C.describe_trading_gap(date(2026, 9, 15), "AM")   # 화요일
    assert note.lag_days_us == 0
    assert "정상 시차" in note.text


# ── 필수 검색 체크리스트 (2026-09-14 사고 대응) ──────────────────

def test_required_searches_widen_the_window_after_a_gap():
    qs = C.required_searches(date(2026, 9, 14), "AM")
    assert any("2026-09-11" in q and "휴장 2일치" in q for q in qs), \
        "갭이 있으면 조사 기간을 '어젯밤'이 아니라 갭 전체로 넓혀야 한다"


def test_narrative_axis_is_always_searched():
    """2026-09-14에 놓친 'AI 속도조절론'은 지수도 지표도 공시도 아닌
    **업계 리더의 발언**이었다. 시장 반응만 훑으면 영영 못 잡는다."""
    for slot in ("AM", "PM", "WEEKEND"):
        qs = C.required_searches(date(2026, 9, 15), slot)
        assert any("속도조절" in q for q in qs), f"{slot}에 서사 축이 없다"
        assert any("데이터센터" in q for q in qs)


def test_calendar_block_carries_the_checklist():
    for slot in ("AM", "PM"):
        body = CTX.build_calendar_block(date(2026, 9, 14), slot).body
        assert "필수 검색 항목" in body
        assert "검색함 → 해당 없음" in body, "미검색과 '찾았는데 없음'을 구분하게 해야 한다"


def test_weekend_pack_sweeps_news_not_just_the_calendar():
    """주말엔 AM·PM이 안 돈다. 여기서 안 훑으면 월요일 개장 때 가격으로
    먼저 만나게 된다 — 2026-09-14가 정확히 그랬다."""
    pack, _ = CTX.build_pack("WEEKEND", date(2026, 9, 12))
    titles = [b.title for b in pack.blocks]
    assert any("주말 뉴스 스윕" in t for t in titles)
    body = next(b.body for b in pack.blocks if "주말 뉴스 스윕" in b.title)
    assert "속도조절" in body


def test_pm_flags_when_korea_is_closed_today():
    note = C.describe_trading_gap(date(2026, 8, 15), "PM")  # 광복절
    assert not note.kr_open_today
    assert "휴장" in note.text


def test_am_flags_when_korea_is_closed_today():
    note = C.describe_trading_gap(date(2026, 8, 15), "AM")
    assert not note.kr_open_today
    assert "성립하지 않는다" in note.text


# ── 예정 일정 ────────────────────────────────────────────────

def test_upcoming_events_excludes_today_and_far_future():
    events = C.upcoming_events(date(2026, 9, 12), horizon_days=5)
    dates = {e["date"] for e in events}
    assert "2026-09-12" not in dates  # 당일 제외
    for d in dates:
        assert date(2026, 9, 12) < date.fromisoformat(d) <= date(2026, 9, 17)


def test_upcoming_events_finds_known_fomc_date():
    events = C.upcoming_events(date(2026, 9, 12), horizon_days=5)
    names = [e["name"] for e in events]
    assert any("FOMC" in n for n in names)


def test_pattern_events_are_marked_unconfirmed_in_data():
    patterns = C.pattern_events()
    assert patterns, "반복 패턴 일정이 하나도 없으면 안 된다"
    assert all(e.get("confirmed") is False for e in patterns)


# ── context.py 통합 ──────────────────────────────────────────

def test_calendar_block_is_present_in_am_and_pm_packs():
    for slot in ("AM", "PM"):
        pack, _ = CTX.build_pack(slot, date(2026, 9, 11))
        titles = [b.title for b in pack.blocks]
        assert any("거래 캘린더" in t for t in titles), f"{slot} 팩에 캘린더 블록 없음"


def test_weekend_slot_always_publishes_regardless_of_market_moves():
    """평시 게이트는 '움직임이 있어야' 발행하지만, 주간 전망은 시장이
    안 움직여도 매주 유효하므로 항상 발행해야 한다."""
    pack, gate = CTX.build_pack("WEEKEND", date(2026, 9, 12))
    assert gate.publish is True
    titles = [b.title for b in pack.blocks]
    assert any("다음주 예정 일정" in t for t in titles)


def test_weekend_pack_has_no_today_fact_sheet():
    """주말엔 '오늘의 실측'이 의미가 없다(휴장) — 블록 ①이 빠져야 한다."""
    pack, _ = CTX.build_pack("WEEKEND", date(2026, 9, 12))
    titles = [b.title for b in pack.blocks]
    assert not any("오늘의 실측" in t for t in titles)


def test_weekend_outlook_surfaces_predictions_due_next_week(tmp_path, monkeypatch):
    monkeypatch.setattr(L, "LEDGER", tmp_path / "ledger.csv")
    L.add("테스트 예측", "2026-09-16", "us_nasdaq", ">", "0", "AM", "2026-09-12")
    block = CTX.build_weekly_outlook_block(date(2026, 9, 12))
    assert "테스트 예측" in block.body


def test_weekend_outlook_lists_stale_digests_for_followup():
    block = CTX.build_weekly_outlook_block(date(2026, 9, 12))
    assert "오래 안 갱신된" in block.body


# ── 과거 유사 사례 비교 (사용자 요청: "선거·정책 이벤트 시장 영향 히스토리") ──

def test_historical_analog_returns_fomc_pattern():
    analog = C.historical_analog("FOMC")
    assert analog is not None
    assert analog["confirmed"] is False
    assert "note" in analog


def test_historical_analog_unknown_type_returns_none():
    assert C.historical_analog("NOT_A_REAL_TYPE") is None


def test_weekly_outlook_attaches_historical_note_to_fomc_event():
    block = CTX.build_weekly_outlook_block(date(2026, 9, 12))
    assert "과거 유사 사례" in block.body
    assert "확정 아님" in block.body


def test_rate_outlook_scenario_trigger_fires_on_kr_base_rate_change():
    triggers, why = CTX.detect_triggers(date(2026, 8, 1))  # kr_base_rate 7월→8월 변동일
    assert "rate-outlook-scenario" in triggers
