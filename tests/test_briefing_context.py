"""engine/briefing/ — 브리핑 팩과 예측 원장.

이 시스템이 존재하는 이유는 사용자가 겪은 두 실패다: 전부 넣으면 context가
터지고, 아주 간단히 하면 원하는 보고서가 아니다. 그래서 **크기가 고정된
선별 팩**을 만든다. 이 파일은 그 성질을 고정한다.
"""
from datetime import date

import pytest

from engine.briefing import context as C
from engine.briefing import ledger as L


@pytest.fixture(autouse=True)
def _isolated_ledger(monkeypatch, tmp_path):
    """원장은 실제 파일에 쓰므로 테스트마다 격리한다 — 감사추적 오염을
    막은 것과 같은 이유(2026-09-10 tests/conftest.py 참고)."""
    monkeypatch.setattr(L, "LEDGER", tmp_path / "ledger.csv")


AS_OF = date(2026, 9, 11)


# ── 팩 크기가 고정된다는 계약 ────────────────────────────────

def test_pack_stays_far_under_the_hard_cap():
    pack, _ = C.build_pack("AM", AS_OF)
    assert pack.chars < C.MAX_PACK_CHARS
    # 리포트 1개(약 40,000자)를 통째로 넣던 것과 비교하면 한 자릿수 배 작아야 한다
    assert pack.chars < 12_000, f"팩이 예상보다 크다: {pack.chars:,}자"


def test_render_truncates_instead_of_silently_overflowing():
    pack = C.BriefingPack(slot="AM", as_of=C.datetime.now(C.KST),
                          blocks=[C.Block("x", "거대 블록", "가" * (C.MAX_PACK_CHARS + 500))])
    out = pack.render()
    assert len(out) <= C.MAX_PACK_CHARS + 200
    assert "상한" in out, "잘렸다는 사실이 팩 안에 남아야 한다"


def test_digest_selection_is_capped_regardless_of_how_many_exist():
    """위키가 커져도 팩이 안 커지는 이유 — 이게 전체 설계의 핵심이다."""
    chosen = C.select_digests(AS_OF, set())
    assert len(chosen) <= C.DIGEST_SLOTS


# ── 선별 규칙 ────────────────────────────────────────────────

def test_fired_triggers_win_the_slots_over_rotation():
    chosen = C.select_digests(AS_OF, {"fx-regime-score"})
    assert chosen[0]["slug"] == "fx-regime-score"


def test_rotation_fills_remaining_slots_with_the_stalest_digests():
    """트리거가 없는 축이 영원히 안 읽히면 조용히 썩는다 — 실제로 이
    저장소의 monitoring 절반이 3주 이상 미갱신이었다."""
    chosen = C.select_digests(AS_OF, set())
    ages = [str(d.get("as_of", "")) for d in chosen]
    assert ages == sorted(ages), "오래된 순으로 채워야 한다"


def test_stale_digests_are_labelled_with_their_age():
    _, why = C.detect_triggers(AS_OF)
    block = C.build_digest_block(AS_OF, set(), why)
    assert "일 전 판단" in block.body


# ── R3: 없는 건 없다고 말한다 ────────────────────────────────

def test_missing_series_are_named_not_silently_dropped():
    """조용히 빼면 LLM이 있는 줄 알고 지어낸다."""
    block = C.build_fact_sheet(date(1990, 1, 1))
    assert "미수집" in block.body


def test_stale_series_carry_a_delay_marker():
    block = C.build_fact_sheet(AS_OF)
    assert "지연" in block.body, "지연된 계열이 표시돼야 한다"


# ── 게이트 ───────────────────────────────────────────────────

def test_gate_publishes_when_something_actually_moved():
    triggers, why = C.detect_triggers(AS_OF)
    gate = C.evaluate_gate(AS_OF, triggers, why)
    if why:
        assert gate.publish and gate.reasons


def test_gate_stays_quiet_when_nothing_moved_and_nothing_is_due():
    gate = C.evaluate_gate(date(1990, 1, 1), set(), [])
    assert not gate.publish
    assert gate.verdict == "조용한 날"


# ── 예측 원장 ────────────────────────────────────────────────

def test_a_prediction_is_scored_against_real_data():
    L.add("미 10년물이 4.0% 이상", "2026-09-11", "us_10y", ">=", "4.0", "AM", "2026-09-11")
    resolved = L.resolve_due(AS_OF)
    assert len(resolved) == 1 and resolved[0].status == "HIT"


def test_a_wrong_prediction_is_recorded_as_miss_not_hidden():
    L.add("미 10년물이 10% 이상", "2026-09-11", "us_10y", ">=", "10", "AM", "2026-09-11")
    assert L.resolve_due(AS_OF)[0].status == "MISS"


def test_missing_data_is_unverifiable_not_a_miss():
    """데이터가 없는 걸 '틀렸다'로 기록하면 적중률 통계가 오염된다(R3)."""
    L.add("존재하지 않는 지표", "2026-09-11", "no_such_series", ">=", "1", "AM", "2026-09-11")
    r = L.resolve_due(AS_OF)[0]
    assert r.status == "UNVERIFIABLE"
    assert L.scoreboard()["accuracy"] is None, "채점불가는 분모에서 빠져야 한다"


def test_predictions_not_yet_due_stay_open():
    L.add("나중 검증", "2099-01-01", "us_10y", ">=", "1", "AM", "2026-09-11")
    assert L.resolve_due(AS_OF) == []
    assert len(L.open_predictions(AS_OF)) == 1


def test_unscoreable_operators_are_rejected_at_write_time():
    """자유문 예측은 채점이 불가능하다 — 애초에 안 받는 게 제약이자 미덕."""
    with pytest.raises(ValueError, match="지원하지 않는 연산자"):
        L.add("대충 오를 것", "2026-09-11", "us_10y", "대충", "1", "AM", "2026-09-11")


def test_ids_do_not_collide():
    a = L.add("A", "2099-01-01", "us_10y", ">=", "1", "AM", "2026-09-11")
    b = L.add("B", "2099-01-01", "us_10y", ">=", "1", "AM", "2026-09-11")
    assert a.id != b.id
