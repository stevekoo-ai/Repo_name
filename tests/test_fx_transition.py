"""engine/fx/transition.py — 전환 경고 감지기.

설계 §3 + §6.5.2(trigger_kind). 백테스트로 측정한 예측력은
DETECTOR_EVIDENCE에 박혀 있고, 이 파일은 감지기가 **역사적으로 맞는 달에**
발화하는지를 고정한다.
"""
from datetime import date

import pytest

from engine.fx import transition as T


# ── 역사적 발화 시점 ─────────────────────────────────────────

def test_2018_episode_fires_the_rate_reversal_trigger():
    """④2017 국면은 연준이 한국을 추월한 2018-03 바로 그 달부터 꺾였다.
    금리차 재확대 감지기가 그 시점에 켜져야 한다."""
    fired = {w.key for w in T.detect_exit_triggers(date(2018, 3, 31)) if w.fired}
    assert "rate_reversal" in fired


def test_2021_episode_fires_the_long_rate_spike_trigger():
    """⑤2020 국면은 금리차가 아니라 미 10년물 급등(0.93→1.74%)이 끝냈다."""
    fired = {w.key for w in T.detect_exit_triggers(date(2021, 3, 31)) if w.fired}
    assert "long_rate_spike" in fired


def test_the_current_episode_has_no_exit_trigger_yet():
    """⑥2026은 아직 시작 2개월째 — 종료 트리거가 켜지면 안 된다."""
    assert not [w for w in T.detect_exit_triggers(date(2026, 9, 9)) if w.fired]


# ── trigger_kind — 장기채 함의를 가르는 정보 ─────────────────

def test_us_tightening_takes_precedence_over_other_causes():
    """장기채 경계가 필요한 경우를 놓치는 쪽이 더 비싸다(§6.5.2)."""
    report = T.evaluate(date(2021, 3, 31))
    if report.fired:
        kinds = {w.kind for w in report.fired}
        if T.TriggerKind.US_TIGHTENING in kinds:
            assert report.trigger_kind == T.TriggerKind.US_TIGHTENING


def test_geopolitical_spike_is_classified_as_a_non_us_shock():
    """안전자산 선호는 미국 긴축과 정반대로 금리를 끌어내린다 —
    2018-10형(무역전쟁)과 같은 계열이라 장기채 함의가 반대다."""
    w = T._trigger_geopolitical_spike(date(2026, 9, 9), {
        "as_of": "2026-09-09", "signals": {"geopolitical_risk": 0.9}})
    assert w.fired and w.kind == T.TriggerKind.NON_US_SHOCK


def test_rate_and_long_rate_triggers_are_us_tightening():
    for w in T.detect_exit_triggers(date(2018, 3, 31)):
        if w.key in ("rate_reversal", "long_rate_spike"):
            assert w.kind == T.TriggerKind.US_TIGHTENING


# ── 집계 규칙 ────────────────────────────────────────────────

def test_the_four_exit_triggers_count_as_one_detector():
    """설계 §3은 '감지기 4종'이다. 종료 트리거 4개를 따로 세면 그 카테고리
    하나가 3단계 문턱(3건)을 혼자 넘겨버린다."""
    report = T.evaluate(date(2018, 3, 31))
    assert len(report.warnings) == 4
    assert {w.key for w in report.warnings} == {
        "momentum_reversal", "exit_trigger", "gap_extreme", "duration"}


def test_level_thresholds_follow_the_design():
    assert T.TransitionReport(date(2026, 1, 1), []).level == "🟢 안정"
    mk = lambda n: T.TransitionReport(date(2026, 1, 1), [
        T.Warning_(f"w{i}", "x", True, T.TriggerKind.UNKNOWN, "") for i in range(n)])
    assert mk(1).level == "🟢 안정"
    assert mk(2).level == "🟡 전환주의"
    assert mk(3).level == "🔴 전환임박"
    assert mk(4).level == "🔴 전환임박"


# ── 측정된 예측력을 숨기지 않는다 ────────────────────────────

def test_every_detector_carries_its_measured_lift():
    """경고가 켜졌다는 사실만 보여주고 그게 얼마나 믿을 만한지 안 보여주면
    R4(근거만 제공)의 취지에 어긋난다."""
    for key in ("duration", "gap_extreme", "exit_trigger", "momentum_reversal"):
        ev = T.evidence_for(key)
        assert "verdict" in ev and ev["verdict"] != "미측정"


def test_credible_fired_excludes_detectors_with_no_measured_lift():
    """모멘텀 반전은 모든 창에서 리프트 ~1.0(정보 없음)이라 걸러져야 하고,
    경과 개월(2.31x)은 남아야 한다."""
    report = T.TransitionReport(date(2026, 1, 1), [
        T.Warning_("momentum_reversal", "모멘텀 반전", True, T.TriggerKind.UNKNOWN, ""),
        T.Warning_("duration", "경과 개월", True, T.TriggerKind.UNKNOWN, ""),
    ])
    keys = {w.key for w in report.credible_fired}
    assert keys == {"duration"}


def test_gap_extreme_is_documented_as_long_lead_not_as_working():
    """0/5는 '실패'가 아니라 '12개월 선행'이라는 실측 결과다 — 그 구분이
    문서에 남아야 다음 세션이 이 감지기를 지우지 않는다."""
    ev = T.evidence_for("gap_extreme")
    assert ev["lift_3m"] == 0.0 and ev["lift_12m"] > 1.2
    assert "장기" in ev["verdict"]


# ── 국면 경과 개월 ───────────────────────────────────────────

def test_current_episode_months_counts_consecutive_below_ma36_months():
    assert T.current_episode_months(date(2026, 9, 9)) == 2   # ⑥ 2026-08~
    assert T.current_episode_months(date(2018, 3, 31)) == 6  # ④ 2017-10~


def test_duration_warning_is_silent_outside_an_episode():
    w = T.detect_duration(date(2019, 6, 30))   # 국면 밖
    assert not w.fired and "하회 국면 아님" in w.detail
