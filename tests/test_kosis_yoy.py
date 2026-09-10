"""collectors/kosis.py의 레벨→YoY 변환.

2026-09-08에 "k_employed_yoy는 표가 연결되지만 레벨값만 줘서 좌표를 바꾸면
조용한 오작동이 된다"며 보류했던 건을 2026-09-10에 해소한 것. 이 파일은
그 변환이 조용히 틀리지 않는지를 고정한다.
"""
import pytest

from collectors.kosis import KOSIS_SERIES, _to_year_over_year


def _rows(pairs):
    return [{"date": d, "value": v} for d, v in pairs]


def test_yoy_is_percent_change_against_the_same_month_last_year():
    rows = _rows([("2025-01-01", 100.0), ("2026-01-01", 110.0)])
    out = _to_year_over_year(rows)
    assert out == [{"date": "2026-01-01", "value": pytest.approx(10.0)}]


def test_months_without_a_prior_year_pair_are_dropped_not_zeroed():
    """R3 — 짝이 없으면 0%가 아니라 아예 내지 않는다. 0%를 내면
    '변화 없음'이라는 판단으로 읽힌다."""
    out = _to_year_over_year(_rows([("2026-03-01", 50.0)]))
    assert out == []


def test_a_missing_month_does_not_shift_the_comparison():
    """인덱스 -12로 비교하면 중간에 빠진 달 때문에 엉뚱한 달과 대조하게
    되는데, 값이 그럴듯해서 눈에 안 띈다. 날짜로 직접 찾아야 한다."""
    pairs = [(f"2025-{m:02d}-01", 100.0) for m in range(1, 13)]
    pairs.remove(("2025-06-01", 100.0))          # 한 달 결측
    pairs.append(("2026-07-01", 120.0))
    out = _to_year_over_year(_rows(pairs))
    assert out == [{"date": "2026-07-01", "value": pytest.approx(20.0)}]


def test_zero_or_missing_base_is_skipped_instead_of_dividing():
    out = _to_year_over_year(_rows([("2025-05-01", 0.0), ("2026-05-01", 10.0)]))
    assert out == []


def test_negative_growth_is_reported_as_a_negative_percent():
    out = _to_year_over_year(_rows([("2025-02-01", 200.0), ("2026-02-01", 180.0)]))
    assert out[0]["value"] == pytest.approx(-10.0)


def test_the_employment_series_declares_the_conversion_and_a_percent_unit():
    """이름만 _yoy이고 변환 선언이 없으면 레벨이 그대로 흘러 CCI가
    2,900만을 증감률로 받는다 — 2026-09-08에 실제로 우려됐던 시나리오다.
    단위 표기도 %여야 리포트가 '2,900만 %'를 찍지 않는다."""
    spec = KOSIS_SERIES["k_employed_yoy"]
    assert spec.get("derive") == "yoy"
    assert spec["unit"] == "%"


def test_only_series_that_declare_it_are_converted():
    """선언한 지표만 변환된다 — 전역 적용이면 지수 계열까지 망가진다."""
    declared = [k for k, v in KOSIS_SERIES.items() if v.get("derive") == "yoy"]
    assert declared == ["k_employed_yoy"]
