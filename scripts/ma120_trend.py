"""SK하이닉스 120일 이동평균선(MA120) 추세 추적.

2026-09-07 사용자 대화에서 시작된 분석 — "120일선 최근 상승 기울기로
전고점까지 며칠 걸리는지", "8/20 이후 주가가 120일선을 얼마나 잘 따라가고
있는지" — 을 매일 자동으로 재계산 가능한 형태로 코드화한 것. 대화에서는
매번 다른 lookback 구간(5/10/20/30일, 07-02~현재 등)을 손으로 골라
기울기를 재봤지만, 자동화 파이프라인은 매번 사람이 구간을 고를 수 없으므로
**최근 20거래일(SLOPE_WINDOW_TRADING_DAYS) 고정 창**을 기본값으로 삼는다 —
5~10일보다 노이즈에 덜 민감하고, 30일보다는 최근성이 있는 절충점(대화에서
실측한 4개 창 중 20일이 5일과 가장 비슷한 값을 냈다). 특정 이벤트(예:
자사주 매입 발표일) 기준 구간을 보고 싶으면 이 모듈이 아니라 그때그때
직접 계산할 것 — 이건 "오늘 기준 최근 한 달"이라는 고정된 관점만 매일
추적한다.

이 모듈은 두 가지를 계산한다:
1. **전고점(250일 최고가) 도달 예상 시점** — MA120의 최근 20거래일
   기울기를 선형 외삽해 언제 250일 최고가(day250_high, 이미 매일 수집되는
   필드)에 닿는지 추정. 이건 예측이 아니라 "지금 기울기가 그대로면"이라는
   기계적 계산이다 — 그렇게 명시해서 렌더링할 것.
2. **추적 품질(tracking quality)** — 최근 20거래일간 종가가 MA120 위/
   아래로 얼마나 왔다갔다했는지(며칠이 선 위였는지, 교차 횟수, 평균/최대/
   최소 괴리율). "꾸준히 선을 타고 올라가는지" vs "이탈과 재돌파를
   반복하는지"를 구분하기 위한 지표.

데이터 소스: `sources/daily-price-history.csv`(2023년~, 긴 이력, MA120
계산에 필요) + `sources/sk-hynix-price-snapshot.csv`(최신 스냅샷, 당일
포함). 두 파일을 날짜로 합치고 주말(토·일) 행만 제외한다 — 주말 스냅샷은
장이 안 열려 전일 종가를 그대로 들고 있는 캐리포워드 중복이기 때문.
**공휴일 캐리포워드까지는 걸러내지 않는다**(요일만으로는 구분 불가) —
알려진 한계로, 실제 값에 미치는 영향은 미미하다(연간 공휴일이 거래일의
5% 미만).

120거래일 미만의 이력만 있으면 MA120 자체를 계산할 수 없으므로
data_status="pending"을 반환한다(R3 — 값을 지어내지 않는다).

이 모듈은 두 호출 컨텍스트 모두에서 import 가능해야 한다(hbm_cycle_score.py와
동일한 이유·동일한 try/except 패턴):
  - `cd scripts && python3 daily_report.py`
  - `PYTHONPATH=. python3 -m engine.report.run`
"""
from __future__ import annotations

import csv
from datetime import date as date_cls, timedelta
from pathlib import Path

try:
    from scripts.investor_flow import read_price_snapshot_rows, DAILY_PRICE_CSV_PATH
except ImportError:
    from investor_flow import read_price_snapshot_rows, DAILY_PRICE_CSV_PATH

MA_WINDOW = 120
SLOPE_WINDOW_TRADING_DAYS = 20
TRACKING_WINDOW_TRADING_DAYS = 20


def _load_close_series(ticker: str) -> list[dict]:
    """긴 이력(daily-price-history.csv) + 최신 스냅샷을 합쳐 날짜순 종가 시계열을
    만든다. 같은 날짜가 양쪽에 있으면 스냅샷 쪽(더 최신 fetched_at)을 채택."""
    rows_by_date: dict[str, float] = {}
    if DAILY_PRICE_CSV_PATH.exists():
        with DAILY_PRICE_CSV_PATH.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("code") == ticker:
                    try:
                        rows_by_date[row["date"]] = float(row["close"])
                    except (KeyError, ValueError):
                        continue
    for row in read_price_snapshot_rows(ticker):
        try:
            rows_by_date[row["date"]] = float(row["price"])
        except (KeyError, ValueError):
            continue

    out = []
    for d, close in sorted(rows_by_date.items()):
        dt = date_cls.fromisoformat(d)
        if dt.weekday() >= 5:  # 토(5)·일(6) — 비거래일 캐리포워드 제외
            continue
        out.append({"date": dt, "close": close})
    return out


def _linear_slope(values: list[float]) -> float:
    """단순 최소자승 선형회귀 기울기(값/스텝). numpy 의존 없이 계산."""
    n = len(values)
    if n < 2:
        return 0.0
    x_mean = (n - 1) / 2
    y_mean = sum(values) / n
    num = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
    den = sum((i - x_mean) ** 2 for i in range(n))
    return num / den if den else 0.0


def compute_ma120_trend(ticker: str = "000660") -> dict:
    """MA120 기울기 기반 전고점 도달 추정 + 최근 20거래일 추적 품질."""
    series = _load_close_series(ticker)
    if len(series) < MA_WINDOW + SLOPE_WINDOW_TRADING_DAYS:
        return {
            "data_status": "pending",
            "note": f"{MA_WINDOW}거래일 이동평균 + 기울기 계산에 필요한 이력 부족 "
                    f"(보유 {len(series)}거래일)",
        }

    closes = [r["close"] for r in series]
    ma120: list[float | None] = [None] * len(closes)
    for i in range(MA_WINDOW - 1, len(closes)):
        ma120[i] = sum(closes[i - MA_WINDOW + 1: i + 1]) / MA_WINDOW

    valid_idx = [i for i, v in enumerate(ma120) if v is not None]
    if len(valid_idx) < SLOPE_WINDOW_TRADING_DAYS:
        return {"data_status": "pending", "note": "MA120 유효 구간이 기울기 계산 창보다 짧음"}

    latest_idx = valid_idx[-1]
    current_price = closes[latest_idx]
    current_date = series[latest_idx]["date"]
    current_ma120 = ma120[latest_idx]

    recent_idx = valid_idx[-SLOPE_WINDOW_TRADING_DAYS:]
    slope_per_trading_day = _linear_slope([ma120[i] for i in recent_idx])

    # 250일 최고가 — 이미 매일 수집되는 필드(day250_high), 새로 계산하지 않음(R3)
    snapshot_rows = read_price_snapshot_rows(ticker)
    prev_high = prev_high_date = None
    if snapshot_rows:
        latest_snap = snapshot_rows[-1]
        try:
            prev_high = float(latest_snap.get("day250_high") or 0) or None
        except ValueError:
            prev_high = None
        prev_high_date = latest_snap.get("day250_high_date")

    trading_days_needed = calendar_days_needed = None
    eta_date = None
    if prev_high:
        gap = prev_high - current_ma120
        if gap <= 0:
            trading_days_needed = calendar_days_needed = 0.0
            eta_date = current_date
        elif slope_per_trading_day > 0:
            trading_days_needed = gap / slope_per_trading_day
            calendar_days_needed = trading_days_needed * 7 / 5
            eta_date = current_date + timedelta(days=round(calendar_days_needed))
        # slope <= 0이면 이 기울기로는 영영 도달 못 함 — eta_date=None 유지, 렌더러가 명시

    # 추적 품질 — 최근 TRACKING_WINDOW_TRADING_DAYS 동안 종가가 MA120 위/아래로 어떻게 다녔는지
    track_idx = valid_idx[-TRACKING_WINDOW_TRADING_DAYS:]
    diffs = [
        (series[i]["date"], closes[i] - ma120[i], (closes[i] - ma120[i]) / ma120[i] * 100)
        for i in track_idx
    ]
    above_days = sum(1 for _, d, _ in diffs if d > 0)
    crossings = sum(
        1 for j in range(1, len(diffs)) if (diffs[j][1] > 0) != (diffs[j - 1][1] > 0)
    )
    avg_diff_pct = sum(p for _, _, p in diffs) / len(diffs)
    max_diff = max(diffs, key=lambda t: t[2])
    min_diff = min(diffs, key=lambda t: t[2])

    return {
        "data_status": "ok",
        "as_of": current_date.isoformat(),
        "current_price": current_price,
        "current_ma120": round(current_ma120),
        "slope_window_trading_days": SLOPE_WINDOW_TRADING_DAYS,
        "slope_per_trading_day": round(slope_per_trading_day, 1),
        "prev_high": prev_high,
        "prev_high_date": prev_high_date,
        "trading_days_to_prev_high": round(trading_days_needed, 1) if trading_days_needed is not None else None,
        "calendar_days_to_prev_high": round(calendar_days_needed, 1) if calendar_days_needed is not None else None,
        "eta_date": eta_date.isoformat() if eta_date else None,
        "slope_positive": slope_per_trading_day > 0,
        "tracking_window_trading_days": TRACKING_WINDOW_TRADING_DAYS,
        "tracking_above_days": above_days,
        "tracking_below_days": len(diffs) - above_days,
        "tracking_crossings": crossings,
        "tracking_avg_diff_pct": round(avg_diff_pct, 2),
        "tracking_max_diff_pct": round(max_diff[2], 2),
        "tracking_max_diff_date": max_diff[0].isoformat(),
        "tracking_min_diff_pct": round(min_diff[2], 2),
        "tracking_min_diff_date": min_diff[0].isoformat(),
        "current_diff_pct": round(diffs[-1][2], 2),
        "current_above": diffs[-1][1] > 0,
    }
