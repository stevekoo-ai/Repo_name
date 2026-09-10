"""engine/fx/regime_score.py — FRS 8개 요인과 총점.

설계: wiki/architecture/fx-regime-score-design.md
"""
from datetime import date

import pytest

from engine.fx import regime_score as R
from engine.fx import series as S


# ── 계약: as_of 격리 ──────────────────────────────────────────

def test_the_same_as_of_always_produces_the_same_score():
    """결정론 — 백테스트가 성립하려면 같은 as_of는 같은 답이어야 한다."""
    a = R.calculate_frs(date(2026, 6, 30))
    b = R.calculate_frs(date(2026, 6, 30))
    assert a.score == b.score
    assert [f.normalized for f in a.factors] == [f.normalized for f in b.factors]


def test_a_past_as_of_is_unaffected_by_data_that_arrives_later():
    """look-ahead 차단의 본체 — 과거 시점 점수는 그 이후 데이터와 무관해야 한다.

    2020-06 시점 점수를 구할 때 읽은 관측치가 전부 2020-06 이하인지
    직접 확인한다(요인이 참조하는 모든 지표에 대해)."""
    as_of = date(2020, 6, 30)
    for name in S.SOURCES:
        rows = S.series_as_of(name, as_of)
        assert all(o.date <= as_of for o in rows), name
    detail = R.calculate_frs(as_of)
    assert detail.as_of == as_of


def test_score_stays_inside_the_declared_range():
    for d in (date(2017, 3, 31), date(2021, 6, 30), date(2026, 9, 9)):
        detail = R.calculate_frs(d)
        if detail.score is not None:
            assert -100.0 <= detail.score <= 100.0


# ── 계약: R3 미수집은 판정이 아니다 ────────────────────────────

def test_missing_factors_are_excluded_from_the_weight_not_scored_as_zero():
    """미수집을 0점으로 채우면 '모르는 것'이 '중립이라는 판단'으로 둔갑한다."""
    as_of = date(2026, 9, 9)
    detail = R.calculate_frs(as_of)          # fx_risk_events 없이 호출
    geo = detail.factor("geopolitical")
    assert geo is not None and not geo.available
    assert geo.contribution == 0.0
    # 지정학 가중치 10이 분모에서 빠져야 한다
    assert detail.covered_weight == sum(
        f.weight for f in detail.factors if f.available)
    assert geo.weight not in (0, None)
    assert detail.covered_weight <= sum(R.WEIGHTS.values()) - geo.weight


def test_score_is_none_when_nothing_is_available():
    """1900년엔 아무 데이터도 없다 — 0점이 아니라 판정불가여야 한다."""
    detail = R.calculate_frs(date(1900, 1, 1))
    assert detail.score is None
    assert detail.covered_weight == 0
    assert R.regime_label(date(1900, 1, 1), detail) == "판정불가(데이터 부족)"


def test_weights_sum_to_one_hundred():
    assert sum(R.WEIGHTS.values()) == 100


# ── 계약: 부호 규약 (+) = 원화 강세 압력 ──────────────────────

def test_rate_differential_favours_krw_when_korea_pays_more():
    """한국 금리가 미국보다 높으면 원화에 유리 — 부호가 뒤집히면 안 된다."""
    f = R.score_rate_differential(date(2026, 9, 9))
    assert f.available
    # 2026-09 실측은 미국이 0.63%p 높지만 3개월간 격차가 좁혀지는 중이라
    # 방향(가중 0.6)이 레벨(0.4)을 이겨 순압력은 (+)여야 한다.
    assert f.normalized > 0, f.detail


def test_rising_us_10y_pushes_the_score_negative():
    """미 장기금리 상승 = 달러로 자금 흡수 = 원화 약세 압력."""
    f = R.score_us_10y(date(2026, 9, 9))
    assert f.available and f.normalized < 0, f.detail


def test_geopolitical_risk_is_sign_flipped():
    """위험이 높을수록 안전자산 선호 → 달러 강세 → 원화 약세(음수)."""
    calm = R.score_geopolitical(date(2026, 9, 9), {
        "as_of": "2026-09-09",
        "signals": {"geopolitical_risk": 0.0, "pandemic_risk": 0.0,
                    "trade_policy_risk": 0.0, "financial_stress": 0.0}})
    storm = R.score_geopolitical(date(2026, 9, 9), {
        "as_of": "2026-09-09",
        "signals": {"geopolitical_risk": 1.0, "pandemic_risk": 1.0,
                    "trade_policy_risk": 1.0, "financial_stress": 1.0}})
    assert calm.normalized == pytest.approx(1.0)
    assert storm.normalized == pytest.approx(-1.0)


def test_geopolitical_reports_how_old_the_llm_judgement_is():
    """R2 — 신선도를 숨기지 않는다."""
    f = R.score_geopolitical(date(2026, 9, 9), {
        "as_of": "2026-08-09", "signals": {"geopolitical_risk": 0.5}})
    assert "31일 전 판단" in f.detail


def test_geopolitical_without_a_yaml_is_unavailable_not_neutral():
    assert R.score_geopolitical(date(2026, 9, 9), None).normalized is None
    assert R.score_geopolitical(date(2026, 9, 9), {"signals": {}}).normalized is None


# ── 계약: 실측으로 잡은 함정 ──────────────────────────────────

def test_partial_current_month_is_excluded_from_monthly_series():
    """2026-09-10 실측 버그 — customs_export_dlr의 2026-09 행은 월중 부분치라
    작년 9월 전체와 비교하면 YoY -69.5%라는 가짜 폭락이 나왔다."""
    as_of = date(2026, 9, 10)
    rows = S.series_as_of("kr_exports", as_of)
    trimmed = R._completed_months(rows, as_of)
    assert any((o.date.year, o.date.month) == (2026, 9) for o in rows)
    assert not any((o.date.year, o.date.month) == (2026, 9) for o in trimmed)
    f = R.score_exports(as_of)
    assert f.available and f.normalized > 0, f.detail


def test_percentile_rank_is_unit_free():
    """경상수지처럼 단위를 코드가 모르는 시리즈를 자기 이력에 상대화한다."""
    pop = [1.0, 2.0, 3.0, 4.0]
    assert R._percentile_rank(0.0, pop) == 0.0
    assert R._percentile_rank(5.0, pop) == 1.0
    assert R._percentile_rank(2.5, pop) == pytest.approx(0.5)
    # 단위가 1000배로 바뀌어도 순위는 그대로
    assert R._percentile_rank(2.5, pop) == R._percentile_rank(2500.0,
                                                              [x * 1000 for x in pop])


def test_ma36_needs_three_full_years_before_it_judges():
    assert R.ma36_gap(date(2006, 1, 1)) is None
    g = R.ma36_gap(date(2026, 9, 9))
    assert g is not None
    now, ma, gap = g
    assert gap == pytest.approx((now / ma - 1) * 100)
    assert gap < 0, "2026-09은 MA36 하회 국면이어야 한다(국면 ⑥)"


def test_regime_label_separates_gap_sign_from_score_sign():
    """이격 부호(지금 강한가) × 점수 부호(압력이 어디로) 조합이다 —
    둘을 헷갈리면 '강세 국면'과 '약세 진입 시도'가 뒤바뀐다."""
    assert R.regime_label(date(2026, 9, 9)) in R.REGIME_LABELS
