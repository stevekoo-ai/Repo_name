#!/usr/bin/env python3
"""
범용 통계 유틸리티 — z-score 정규화, 이상치("역대급") 판정, 로지스틱 압축.

wiki/concepts/automation-vs-ai-narrative-roadmap.md "숫자를 의미화하는 업계
기법" 조사(2026-08-06)에서 확인한 두 가지 확립된 방법론을 이 저장소 스타일로
재현한다:

- **E. z-score/percentile 이상치 탐지**: `credit_balance_streak()`
  (investor_flow.py)에서 "N일 연속 증감"으로 부분 구현했던 패턴을, 표준편차
  기준으로 일반화 — "역대급 순매수" 같은 판단을 사람 손 없이 자동 플래그.
- **B. CNN Fear & Greed Index 방법론**: 7개 지표를 각각 "과거 분포 대비 얼마나
  벗어났는지"로 정규화한 뒤 0~100 스케일로 합산하는 방식 — 이 저장소에서는
  HBM Cycle Score의 고정 점수구간(예: 8/4/3점) 대신 z-score를 로지스틱으로
  압축해 연속 스케일 점수로 변환하는 데 재사용한다.

이 모듈은 순수 통계 계산만 하고 데이터 소스는 모른다(investor_flow.py 등이
호출). stdlib(statistics, math)만 사용 — 별도 의존성 없음.
"""
from __future__ import annotations

import math
import statistics

MIN_SAMPLE_SIZE = 5  # 이보다 적으면 z-score 자체가 통계적으로 불안정 — None 반환


def zscore(value: float, history: list[float]) -> float | None:
    """history(과거 관측값, value 자신은 제외)에 대한 value의 z-score.
    history가 MIN_SAMPLE_SIZE 미만이거나 분산이 0이면(전부 동일값) None —
    지어낸 z-score를 반환하지 않는다."""
    clean = [h for h in history if h is not None]
    if len(clean) < MIN_SAMPLE_SIZE:
        return None
    mean = statistics.mean(clean)
    stdev = statistics.pstdev(clean)
    if stdev == 0:
        return None
    return (value - mean) / stdev


def percentile_rank(value: float, history: list[float]) -> float | None:
    """history 중 value 이하인 비율(0~100). z-score와 달리 분포 모양(정규분포
    가정)에 의존하지 않아, 한쪽으로 치우친 분포(예: 순매수 금액)에 더 안전."""
    clean = [h for h in history if h is not None]
    if len(clean) < MIN_SAMPLE_SIZE:
        return None
    below_or_equal = sum(1 for h in clean if h <= value)
    return below_or_equal / len(clean) * 100


def anomaly_label(z: float | None, high: float = 2.0, extreme: float = 3.0) -> str:
    """z-score를 사람이 읽는 한글 라벨로 변환. 임계값(high=2.0σ, extreme=3.0σ)은
    정규분포에서 각각 상위/하위 약 2.3%, 0.1% 지점 — "이례적"·"역대급" 판정에
    흔히 쓰이는 관례적 기준(CNN Fear&Greed류 지수와 동일한 표준편차 기반 관례)."""
    if z is None:
        return "미확인 — 데이터 부족(과거 관측치 5건 미만 또는 무변동)"
    if z >= extreme:
        return f"역대급 상승(z={z:+.2f}σ)"
    if z >= high:
        return f"이례적 상승(z={z:+.2f}σ)"
    if z <= -extreme:
        return f"역대급 하락(z={z:+.2f}σ)"
    if z <= -high:
        return f"이례적 하락(z={z:+.2f}σ)"
    return f"평이한 수준(z={z:+.2f}σ)"


def logistic_scale(z: float | None, max_score: float, neutral: float = 0.5) -> float:
    """z-score를 [0, max_score] 연속 스케일로 압축(로지스틱 함수) — CNN Fear&Greed
    Index가 여러 지표를 0~100 점수로 정규화할 때 쓰는 것과 같은 방식(각 지표를
    과거 분포 대비 표준편차로 계산한 뒤 유계 스케일로 매핑). z=0(과거 평균과
    동일)이면 max_score의 neutral 비율(기본 50%)을 반환, z가 커질수록 max_score에
    점근, z가 작아질수록 0에 점근 — 고정 점수구간(8/4/3점 식)과 달리 국면이
    바뀌어도 임계값을 손으로 재조정할 필요가 없다(과거 분포 자체가 매일 갱신되며
    자동 보정됨).
    z가 None(데이터 부족)이면 중립값(neutral*max_score)을 반환 — 모르는 것을
    극단값으로 처리하지 않는다."""
    if z is None:
        return round(max_score * neutral, 1)
    # 로지스틱 함수의 기울기(k=0.7)는 z=±3(위 anomaly_label의 "역대급" 임계값)에서
    # 각각 max_score의 약 90%/10%에 도달하도록 보정한 값 — 너무 완만하면(k 작음)
    # 극단치가 만점 근처까지 안 가고, 너무 가파르면(k 큼) z=1 정도의 흔한 변동에도
    # 점수가 요동친다.
    k = 0.7
    squashed = 1 / (1 + math.exp(-k * z))
    return round(max_score * squashed, 1)
