"""engine/fx/bond_return.py — 금리에서 합성한 채권 총수익 검증.

ICE BofA 총수익지수를 FRED가 최근 3년만 공개해서(2026-09-10 실측) 금리에서
합성해 쓰기로 했다. 합성식은 눈으로 맞는지 알 수 없으므로 성질을 고정한다.
"""
import math
import pytest

from engine.fx.bond_return import (
    par_bond_price,
    monthly_total_return,
    cumulative_total_return,
    cash_total_return,
)


def test_par_bond_prices_at_100_when_coupon_equals_yield():
    for maturity in (2.0, 5.0, 10.0, 30.0):
        for y in (0.5, 2.0, 4.0, 8.0):
            assert par_bond_price(y, y, maturity) == pytest.approx(100.0, abs=1e-9)


def test_flat_yield_month_returns_exactly_the_carry():
    """금리가 안 움직이면 한 달 수익 = 반기쿠폰을 1/6로 나눈 복리분."""
    y = 4.0
    r = monthly_total_return(y, y, 10.0)
    expected = (1 + y / 200) ** (1 / 6) - 1  # 1개월 = 반기(6개월)의 1/6
    assert r == pytest.approx(expected, rel=1e-6)


def test_rising_yields_lose_money_and_falling_yields_gain():
    assert monthly_total_return(4.0, 5.0, 10.0) < -0.05
    assert monthly_total_return(4.0, 3.0, 10.0) > 0.05


def test_longer_maturity_is_more_rate_sensitive():
    """같은 금리 변화에 10년물이 2년물보다 훨씬 크게 움직인다(듀레이션)."""
    ten = monthly_total_return(4.0, 5.0, 10.0)
    two = monthly_total_return(4.0, 5.0, 2.0)
    assert ten < two < 0
    assert abs(ten) > 3 * abs(two)


def test_convexity_makes_the_gain_bigger_than_the_loss():
    """±100bp 대칭 충격에서 이익이 손실보다 커야 한다 — 볼록성."""
    up = monthly_total_return(4.0, 5.0, 10.0)
    down = monthly_total_return(4.0, 3.0, 10.0)
    assert down > -up


def test_short_maturities_are_rejected_instead_of_silently_wrong():
    """반기쿠폰 가정이 깨지는 구간을 조용히 계산하면 3개월물 월수익이
    1.3%로 나온다 — 실제로 한 번 그렇게 나왔던 버그라 예외로 고정한다."""
    with pytest.raises(ValueError, match="6개월 미만"):
        par_bond_price(4.0, 4.0, 0.25)


def test_cumulative_chains_monthly_returns():
    ys = [4.0, 4.0, 4.0]
    total = cumulative_total_return(ys, 10.0)
    one = monthly_total_return(4.0, 4.0, 10.0)
    assert total == pytest.approx((1 + one) ** 2 - 1, rel=1e-9)


def test_cash_return_accrues_only_interest():
    """현금은 가격변동이 없다 — 금리를 월할로 쌓기만 한다.
    첫 원소는 진입 시점이라 이자가 안 붙는 게 맞다(구간 수가 n-1)."""
    assert cash_total_return([5.0, 6.0, 6.0]) == pytest.approx(
        (1 + 6.0 / 1200) ** 2 - 1, rel=1e-12
    )


def test_missing_yield_returns_none_instead_of_guessing():
    """R3(미수집은 판정이 아니다) — 값이 비면 0%가 아니라 None."""
    assert monthly_total_return(None, 4.0, 10.0) is None
    assert monthly_total_return(4.0, None, 10.0) is None
    assert cumulative_total_return([4.0, None, 4.0], 10.0) is None
