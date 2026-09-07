"""SK하이닉스 MA120 추세 추적 (scripts/ma120_trend.py).

2026-09-07 사용자 대화에서 손으로 여러 번 반복했던 계산(120일선 최근
기울기로 전고점 도달 시점 추정, 최근 거래일간 선 위/아래 추적 품질)을
매일 자동 재현 가능하게 코드화한 모듈의 회귀 테스트.
"""
from __future__ import annotations

from datetime import date, timedelta

import scripts.ma120_trend as mod
from scripts.ma120_trend import _linear_slope, compute_ma120_trend


def _synthetic_series(n: int, start_price: float = 1_000_000.0, step: float = 1000.0,
                       start: date = date(2026, 1, 1)) -> list[dict]:
    """n개의 평일(거래일)로만 이루어진, 완벽한 선형 가격 시계열 — 회귀 계산의
    기대값을 손으로 검증 가능하게 만들기 위한 픽스처."""
    series = []
    i = 0
    d = start
    while len(series) < n:
        if d.weekday() < 5:
            series.append({"date": d, "close": start_price + i * step})
            i += 1
        d += timedelta(days=1)
    return series


def _snapshot_rows(prev_high: float, prev_high_date: str = "2026-06-25"):
    return [{"day250_high": str(prev_high), "day250_high_date": prev_high_date}]


def test_linear_slope_on_known_sequence():
    assert _linear_slope([1, 2, 3, 4, 5]) == 1.0
    assert _linear_slope([10, 8, 6, 4]) == -2.0
    assert _linear_slope([5]) == 0.0
    assert _linear_slope([]) == 0.0


def test_insufficient_history_returns_pending_not_a_guess():
    """120거래일 미만이면 MA120을 계산할 수 없다 — 값을 지어내지 않고 pending 반환(R3)."""
    series = _synthetic_series(50)
    orig = mod._load_close_series
    mod._load_close_series = lambda ticker="000660": series
    try:
        result = compute_ma120_trend()
    finally:
        mod._load_close_series = orig
    assert result["data_status"] == "pending"


def test_perfectly_linear_series_gives_exact_slope_and_eta(monkeypatch):
    """완벽한 선형 가격 시계열의 MA120도 같은 기울기로 선형이 된다는 성질을
    이용해, 기대값을 손으로 정확히 계산해서 대조한다."""
    series = _synthetic_series(150, start_price=1_000_000.0, step=1000.0)
    monkeypatch.setattr(mod, "_load_close_series", lambda ticker="000660": series)

    # MA120[149] = 1,000,000 + 1000*(149 - 59.5) = 1,089,500
    # 슬로프 1000원/거래일로 5거래일 후 도달하는 값 = 1,089,500 + 5,000 = 1,094,500
    prev_high = 1_094_500.0
    monkeypatch.setattr(mod, "read_price_snapshot_rows",
                         lambda ticker="000660": _snapshot_rows(prev_high))

    result = compute_ma120_trend()
    assert result["data_status"] == "ok"
    assert result["slope_per_trading_day"] == 1000.0
    assert result["current_ma120"] == 1_089_500
    assert result["current_price"] == 1_149_000.0
    assert result["trading_days_to_prev_high"] == 5.0
    assert result["calendar_days_to_prev_high"] == 7.0
    assert result["eta_date"] == (series[-1]["date"] + timedelta(days=7)).isoformat()
    assert result["slope_positive"] is True


def test_tracking_quality_all_above_when_uptrend(monkeypatch):
    """상승 선형 시계열에서는 종가가 항상 MA120 위에 있어야 한다(교차 0회) —
    8/20~9/7 실측에서 봤던 '이탈·재돌파 반복'과 대조되는 깨끗한 케이스."""
    series = _synthetic_series(150, start_price=1_000_000.0, step=1000.0)
    monkeypatch.setattr(mod, "_load_close_series", lambda ticker="000660": series)
    monkeypatch.setattr(mod, "read_price_snapshot_rows",
                         lambda ticker="000660": _snapshot_rows(2_000_000.0))

    result = compute_ma120_trend()
    assert result["tracking_above_days"] == mod.TRACKING_WINDOW_TRADING_DAYS
    assert result["tracking_below_days"] == 0
    assert result["tracking_crossings"] == 0
    assert result["current_above"] is True


def test_flat_slope_never_reaches_prev_high_and_says_so(monkeypatch):
    """기울기가 0(또는 음수)이면 이 방식으로는 영영 도달 못 한다 — 억지로 날짜를
    만들어내지 않고 eta_date=None, slope_positive=False로 명시한다(R3)."""
    series = _synthetic_series(150, start_price=1_000_000.0, step=0.0)
    monkeypatch.setattr(mod, "_load_close_series", lambda ticker="000660": series)
    monkeypatch.setattr(mod, "read_price_snapshot_rows",
                         lambda ticker="000660": _snapshot_rows(2_000_000.0))

    result = compute_ma120_trend()
    assert result["slope_positive"] is False
    assert result["eta_date"] is None
    assert result["trading_days_to_prev_high"] is None


def test_already_at_or_above_prev_high_needs_zero_days(monkeypatch):
    """MA120이 이미 250일 최고가 이상이면 '0일 남음'이어야지, 음수 날짜나
    엉뚱한 외삽이 나오면 안 된다."""
    series = _synthetic_series(150, start_price=1_000_000.0, step=1000.0)
    monkeypatch.setattr(mod, "_load_close_series", lambda ticker="000660": series)
    monkeypatch.setattr(mod, "read_price_snapshot_rows",
                         lambda ticker="000660": _snapshot_rows(1.0))  # 이미 훨씬 낮은 "전고점"

    result = compute_ma120_trend()
    assert result["trading_days_to_prev_high"] == 0.0
    assert result["calendar_days_to_prev_high"] == 0.0
    assert result["eta_date"] == series[-1]["date"].isoformat()


def test_real_repo_data_smoke():
    """실제 저장소 데이터로 크래시 없이 돌아가는지 + 값이 상식적인 범위인지만
    확인(라이브 데이터라 정확한 값은 매일 바뀜 — hbm_cycle_score 테스트와 동일 패턴)."""
    result = compute_ma120_trend()
    assert result["data_status"] in ("ok", "pending")
    if result["data_status"] == "ok":
        assert result["current_price"] > 0
        assert result["current_ma120"] > 0
        assert 0 <= result["tracking_above_days"] <= mod.TRACKING_WINDOW_TRADING_DAYS
        assert result["tracking_above_days"] + result["tracking_below_days"] == mod.TRACKING_WINDOW_TRADING_DAYS
