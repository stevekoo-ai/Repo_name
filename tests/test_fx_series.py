"""engine/fx/series.py — as_of 계약 검증.

FRS 설계의 최우선 제약은 "모든 점수 함수가 as_of를 받는다"인데, 그 제약이
실제로 지켜지는 지점은 **데이터를 읽는 곳**이다. 점수 함수가 as_of를 받아도
내부에서 최신값을 읽으면 look-ahead가 새어든다(기존 CCI의 _get_latest가
그 구조였다). 이 파일은 그 통로가 막혀 있음을 고정한다.
"""
from datetime import date

import pytest

from engine.fx import series as S


def test_series_as_of_never_returns_future_observations():
    """이 저장소의 실제 데이터로, 모든 지표에 대해 미래 누출이 없어야 한다."""
    for name in S.SOURCES:
        for cutoff in (date(2018, 6, 30), date(2021, 3, 15), date(2026, 1, 1)):
            for obs in S.series_as_of(name, cutoff):
                assert obs.date <= cutoff, f"{name}: {obs.date} > {cutoff} (look-ahead)"


def test_series_as_of_is_a_prefix_of_the_full_history():
    """자르기만 할 뿐 값을 바꾸거나 재정렬하지 않는다."""
    full = S.load_series("us_10y")
    cutoff = date(2020, 1, 1)
    sliced = S.series_as_of("us_10y", cutoff)
    assert sliced == [o for o in full if o.date <= cutoff]


def test_observations_are_sorted_ascending():
    for name in ("us_10y", "kr_usdkrw_fred", "kr_base_rate"):
        rows = S.load_series(name)
        assert rows == sorted(rows, key=lambda o: o.date), name


def test_latest_as_of_drops_values_older_than_max_age():
    """오래된 값을 조용히 '최신'으로 쓰는 걸 막는다 — CCI의 62일 사고 재발 방지.

    ⚠ 이 테스트는 처음에 "2010년엔 kr_base_rate가 없다"를 전제로 썼다가,
    같은 날 백필로 그 시리즈가 2005년까지 늘어나면서 깨졌다. 데이터
    커버리지에 기대는 단정은 백필 한 번에 무너지므로, 어떤 시리즈도
    존재할 수 없는 시점을 쓰고 나이 제한 자체를 직접 검증한다."""
    before_everything = date(1900, 1, 1)
    assert S.latest_as_of("kr_base_rate", before_everything) is None
    # 나이 제한이 없으면 마지막 값이 나오지만, 제한을 걸면 None으로 떨어진다
    cutoff = date(2026, 9, 9)
    assert S.value_as_of("us_10y", cutoff, max_age_days=3650) is not None
    assert S.value_as_of("us_10y", cutoff, max_age_days=0) is None


def test_value_n_months_before_walks_back_across_year_boundaries():
    """3월에서 6개월 전은 작년 9월 — 연도 넘김에서 깨지지 않아야 한다."""
    a = S.value_n_months_before("us_10y", date(2021, 3, 15), 6)
    b = S.value_as_of("us_10y", date(2020, 9, 15))
    assert a == b


def test_unknown_series_fails_loudly():
    """조용히 None을 주면 요인이 '미수집'으로 위장돼 원인을 못 찾는다."""
    with pytest.raises(KeyError, match="알 수 없는 지표"):
        S.series_as_of("존재하지_않는_지표", date(2026, 1, 1))


def test_monthly_last_keeps_the_final_observation_of_each_month():
    rows = S.monthly_last("us_10y", date(2020, 3, 31))
    assert rows[-1][0] == "2020-03"
    daily = [o for o in S.series_as_of("us_10y", date(2020, 3, 31))
             if (o.date.year, o.date.month) == (2020, 3)]
    assert rows[-1][1] == daily[-1].value
