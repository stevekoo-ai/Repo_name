"""engine/fx/backtest.py — 설계 §6 합격 기준을 테스트로 고정한다.

이 파일이 통과하는 한 FRS는 "과거 5개 국면을 재현하고, 미래를 훔쳐보지
않는다"가 보장된다. 가중치를 바꾸면 여기가 먼저 깨져야 한다.
"""
from datetime import date

import pytest

from engine.fx import backtest as B
from engine.fx.regime_score import calculate_frs

START, END = date(2008, 1, 1), date(2026, 9, 30)


@pytest.fixture(scope="module")
def points():
    return B.run(START, END)


# ── 합격 기준 1: 5개 국면 재현 (±3개월) ──────────────────────

def test_all_five_completed_episodes_are_reproduced_within_three_months(points):
    results = {tag: (verdict, detail) for tag, verdict, detail in
               B.match_known_episodes(points)}
    for tag in ("①", "②", "③", "④", "⑤"):
        verdict, detail = results[tag]
        assert verdict == "✅ 재현", f"{tag}: {verdict} — {detail}"


def test_the_ongoing_episode_is_reported_as_undetected_not_mismatched(points):
    """2026-09-10 실측으로 잡은 매칭 버그 — ⑥은 아직 2개월이라 탐지
    최소길이(3개월)에 못 미치는데, '가장 가까운 구간'을 무조건 붙이던
    때는 70개월 떨어진 ⑤에 매칭돼 '불일치'로 보고됐다. 미탐지와
    오탐지는 다른 사건이라 구분돼야 한다."""
    results = {tag: verdict for tag, verdict, _ in B.match_known_episodes(points)}
    assert results["⑥"] == "⚠ 미탐지"


def test_detected_episodes_are_at_least_three_months_long(points):
    for start, end in B.detected_episodes(points, min_months=3):
        assert B._months_between(start, end) + 1 >= 3


# ── 합격 기준 2: look-ahead bias 0 ───────────────────────────

def test_a_backtest_point_equals_a_standalone_call_at_that_date(points):
    """백테스트 경로와 실사용 경로가 같은 코드여야 한다 — 다르면 백테스트가
    검증하는 대상이 리포트가 쓰는 대상이 아니게 된다."""
    for p in points[::37]:
        assert p.score == (calculate_frs(p.as_of).score)


def test_truncating_the_backtest_does_not_change_earlier_points():
    """2020년까지만 돌린 결과가, 2026년까지 돌린 결과의 앞부분과 같아야 한다.
    다르면 어딘가에서 미래 데이터가 새고 있다는 뜻이다."""
    short = B.run(START, date(2020, 12, 31))
    long = B.run(START, END)
    assert [(p.month, p.score) for p in short] == \
           [(p.month, p.score) for p in long[:len(short)]]


def test_month_end_is_the_last_day_of_the_month():
    assert B.month_end(2020, 2) == date(2020, 2, 29)   # 윤년
    assert B.month_end(2021, 2) == date(2021, 2, 28)
    assert B.month_end(2020, 12) == date(2020, 12, 31)  # 연말 넘김
    assert B.month_end(2020, 1) == date(2020, 1, 31)


# ── 요인이 실제로 국면을 설명하는가 ──────────────────────────

def test_scores_are_clearly_higher_inside_below_ma36_episodes():
    r = B.separation_report(START, END)
    assert r["포함_하회"]["중앙값"] > r["포함_그외"]["중앙값"] + 5
    assert r["포함_하회"]["양수비율"] > r["포함_그외"]["양수비율"]


def test_the_separation_is_not_an_artefact_of_the_ma36_factor_itself():
    """⚠ 순환논리 점검 — MA36 이격이 요인이자 국면 정의라 자기참조가 있다.
    그 요인을 빼도 분리가 유지돼야 결과를 믿을 수 있다.
    실측(2026-09-10): 빼면 오히려 더 선명해진다(+14.3→+18.3)."""
    r = B.separation_report(START, END)
    assert r["제외_하회"]["중앙값"] > r["제외_그외"]["중앙값"] + 5
    assert r["제외_하회"]["중앙값"] >= r["포함_하회"]["중앙값"]


def test_score_without_ma36_renormalises_on_the_remaining_weight():
    detail = calculate_frs(date(2026, 9, 9))
    ma = detail.factor("ma36_gap")
    assert ma is not None and ma.available
    adjusted = B.score_without_ma36(detail)
    expected_raw = detail.score * detail.covered_weight / 100 - ma.contribution
    assert adjusted == pytest.approx(
        expected_raw / (detail.covered_weight - ma.weight) * 100)
