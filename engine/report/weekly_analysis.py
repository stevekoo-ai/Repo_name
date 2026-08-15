"""
12주 거시 지표 변화 분석 자동화 모듈

매일 실행되어 지난 12주의 주요 지표 추이를 분석하고,
의사결정 리포트에 포함될 근거 데이터를 생성합니다.
"""
import csv
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
SERIES_CSV_PATH = REPO_ROOT / "sources" / "macro-series.csv"


@dataclass
class IndicatorAnalysis:
    """단일 지표의 12주 분석 결과"""
    name: str  # 지표명 (영문)
    label: str  # 한글명
    unit: str  # 단위
    current_value: float  # 현재값
    value_12w_ago: Optional[float]  # 12주 전 값
    pct_change: Optional[float]  # % 변화
    abs_change: Optional[float]  # 절대값 변화
    trend: str  # 상향/보합/하향
    latest_date: str  # 최신 데이터 날짜
    data_points: list[tuple[str, float]]  # (날짜, 값) 튜플 리스트


@dataclass
class WeeklyAnalysisResult:
    """12주 변화 분석 결과"""
    analysis_date: str  # 분석 실행 날짜
    period_start: str  # 분석 시작일
    period_end: str  # 분석 종료일
    indicators: dict[str, IndicatorAnalysis]  # 지표별 분석


def _read_series_data(series_name: str, lookback_weeks: int = 12) -> list[tuple[str, float]]:
    """
    macro-series.csv에서 특정 시리즈의 N주 데이터 추출

    Args:
        series_name: 추출할 시리즈명 (e.g., "us_10y", "kr_usdkrw")
        lookback_weeks: 역사 기간 (기본 12주)

    Returns:
        [(date_str, value), ...] 형태의 리스트
    """
    if not SERIES_CSV_PATH.exists():
        return []

    today = datetime.now().date()
    lookback_date = today - timedelta(weeks=lookback_weeks)

    data = []
    try:
        with SERIES_CSV_PATH.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("series") != series_name:
                    continue
                try:
                    date = datetime.strptime(row["date"], "%Y-%m-%d").date()
                    if lookback_date <= date <= today:
                        data.append((row["date"], float(row["value"])))
                except (ValueError, KeyError):
                    continue
    except Exception:
        return []

    return sorted(data, key=lambda x: x[0])


def _extract_weekly_values(data: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """
    일일 데이터를 주간 데이터로 변환 (7일 단위)

    Args:
        data: [(date_str, value), ...] 형태의 데이터

    Returns:
        주간 마감 데이터 (7일 이상 간격의 마지막 값)
    """
    if len(data) < 2:
        return data

    weekly = []
    current_week_end = None

    for date_str, value in data:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        if not current_week_end or (date - current_week_end).days >= 7:
            # 새로운 주 시작
            weekly.append((date_str, value))
            current_week_end = date
        else:
            # 같은 주, 마지막 값 업데이트
            if weekly:
                weekly[-1] = (date_str, value)

    return weekly


def analyze_indicator(
    series_name: str,
    label: str,
    unit: str,
    lookback_weeks: int = 12
) -> Optional[IndicatorAnalysis]:
    """
    단일 지표를 분석하여 IndicatorAnalysis 객체 반환

    Args:
        series_name: 시리즈명
        label: 한글 레이블
        unit: 단위
        lookback_weeks: 분석 기간

    Returns:
        IndicatorAnalysis 또는 None (데이터 부족 시)
    """
    raw_data = _read_series_data(series_name, lookback_weeks)
    if len(raw_data) < 2:
        return None

    # 주간 데이터로 변환
    weekly_data = _extract_weekly_values(raw_data)
    if len(weekly_data) < 2:
        return None

    # 추세 판정 (최근 4주 vs 12주 평균)
    recent_4w = [v for _, v in weekly_data[-4:]]
    all_12w = [v for _, v in weekly_data]

    recent_avg = sum(recent_4w) / len(recent_4w) if recent_4w else all_12w[-1]
    all_avg = sum(all_12w) / len(all_12w) if all_12w else 0

    if recent_avg > all_avg * 1.01:
        trend = "상향"
    elif recent_avg < all_avg * 0.99:
        trend = "하향"
    else:
        trend = "보합"

    # 변화율 계산
    current_value = weekly_data[-1][1]
    value_12w_ago = weekly_data[0][1] if len(weekly_data) > 1 else None

    if value_12w_ago and value_12w_ago != 0:
        pct_change = ((current_value - value_12w_ago) / abs(value_12w_ago)) * 100
        abs_change = current_value - value_12w_ago
    else:
        pct_change = None
        abs_change = None

    return IndicatorAnalysis(
        name=series_name,
        label=label,
        unit=unit,
        current_value=current_value,
        value_12w_ago=value_12w_ago,
        pct_change=pct_change,
        abs_change=abs_change,
        trend=trend,
        latest_date=weekly_data[-1][0],
        data_points=weekly_data[-8:]  # 최근 8주만 포함 (리포트용)
    )


def generate_weekly_analysis() -> WeeklyAnalysisResult:
    """
    12주 거시 지표 변화 분석 실행

    Returns:
        WeeklyAnalysisResult 객체
    """
    today = datetime.now().date()
    lookback_weeks = 12
    lookback_date = today - timedelta(weeks=lookback_weeks)

    # 분석할 주요 지표
    target_series = [
        ("us_10y", "미국 10년물 국채금리", "%"),
        ("kr_base_rate", "한국은행 기준금리", "%"),
        ("kr_usdkrw", "원/달러 환율", "원"),
        ("us_brent", "브렌트유", "$/배럴"),
        ("us_fed_funds", "미국 연방기금금리", "%"),
    ]

    indicators = {}

    for series_name, label, unit in target_series:
        result = analyze_indicator(series_name, label, unit, lookback_weeks)
        if result:
            indicators[series_name] = result

    return WeeklyAnalysisResult(
        analysis_date=today.isoformat(),
        period_start=lookback_date.isoformat(),
        period_end=today.isoformat(),
        indicators=indicators
    )


if __name__ == "__main__":
    result = generate_weekly_analysis()
    print(f"분석 날짜: {result.analysis_date}")
    print(f"분석 기간: {result.period_start} ~ {result.period_end}")
    print(f"\n분석된 지표: {len(result.indicators)}개")

    for series_name, analysis in result.indicators.items():
        print(f"\n{analysis.label} ({analysis.unit})")
        print(f"  현재값: {analysis.current_value:.2f}")
        if analysis.pct_change is not None:
            print(f"  변화: {analysis.pct_change:+.2f}%")
        print(f"  추세: {analysis.trend}")
