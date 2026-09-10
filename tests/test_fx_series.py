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

    ⚠ 이 테스트는 두 번 깨졌다. 처음엔 "2010년엔 kr_base_rate가 없다"를
    전제로 썼다가 백필로 그 시리즈가 2005년까지 늘어나며 깨졌고, 다음엔
    "2026-09-09 기준 us_10y는 0일보다 오래됐다"를 전제로 썼다가 main 병합으로
    그날 값이 새로 들어오며 깨졌다. **데이터 커버리지에 기대는 단정은
    수집이 진행될수록 반드시 깨진다.**

    그래서 여기서는 어떤 날짜도 하드코딩하지 않는다. 실제 마지막 관측일을
    읽어와 그 상대적 거리로만 나이 제한을 검증한다."""
    from datetime import timedelta

    rows = S.load_series("us_10y")
    assert rows, "us_10y는 이 저장소에 항상 있어야 한다"
    last = rows[-1].date

    # 마지막 관측 당일에 조회하면 나이 0 — 어떤 제한에도 살아남는다
    assert S.value_as_of("us_10y", last, max_age_days=0) is not None
    # 10일 뒤 시점에서 보면 나이 10 — 제한 9면 걸러지고 10이면 통과한다
    later = last + timedelta(days=10)
    assert S.value_as_of("us_10y", later, max_age_days=9) is None
    assert S.value_as_of("us_10y", later, max_age_days=10) is not None
    # 데이터가 존재할 수 없는 시점은 나이 제한과 무관하게 None
    assert S.latest_as_of("us_10y", date(1900, 1, 1)) is None


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
