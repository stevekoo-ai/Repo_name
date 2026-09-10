"""FRS 백테스트 하네스 — 과거 월말을 순회하며 5개 국면을 재현하는지 본다.

설계 §1의 "계산 엔진과 백테스트 동시 진행"이 여기서 회수된다. 별도 로직이
없다 — `calculate_frs(as_of)`를 과거 월말마다 부르는 게 전부다. 그게 가능한
이유는 모든 데이터 접근이 `series.py`의 as_of 필터를 통과하기 때문이고,
그 성질은 tests/test_fx_series.py가 고정한다.

합격 기준(설계 §6):
  1. 과거 5개 국면의 진입/이탈을 ±3개월 이내로 잡는가
  2. look-ahead bias 0 (테스트로 고정)
"""
from __future__ import annotations

import statistics
from dataclasses import dataclass
from datetime import date, timedelta

from engine.fx.regime_score import FRSDetail, calculate_frs, ma36_gap, regime_label

# wiki/concepts/usdkrw-below-ma36-episodes.md 의 국면 정의 (양끝 포함, 월 단위)
KNOWN_EPISODES: list[tuple[str, str, str | None]] = [
    ("①", "2010-09", "2012-04"),
    ("②", "2012-06", "2013-04"),
    ("③", "2013-08", "2014-10"),
    ("④", "2017-10", "2018-09"),
    ("⑤", "2020-10", "2021-07"),
    ("⑥", "2026-08", None),      # 진행 중
]


@dataclass(frozen=True)
class MonthlyPoint:
    month: str            # YYYY-MM
    as_of: date           # 그 달의 말일
    score: float | None
    coverage: float
    gap: float | None     # MA36 이격 %
    label: str


def month_end(year: int, month: int) -> date:
    """그 달의 마지막 날. 백테스트의 as_of는 항상 월말이다 —
    월중 시점을 쓰면 월간 시리즈의 발표 지연 때문에 달마다 커버리지가
    들쭉날쭉해져 비교가 안 된다."""
    first_next = date(year + (month // 12), month % 12 + 1, 1)
    return first_next - timedelta(days=1)


def iter_month_ends(start: date, end: date):
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        d = month_end(y, m)
        if d <= end:
            yield d
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def run(start: date, end: date, risk_events: dict | None = None) -> list[MonthlyPoint]:
    """월말마다 FRS를 계산한다. 이게 백테스트의 전부다."""
    out: list[MonthlyPoint] = []
    for as_of in iter_month_ends(start, end):
        detail: FRSDetail = calculate_frs(as_of, risk_events)
        g = ma36_gap(as_of)
        out.append(MonthlyPoint(
            month=f"{as_of.year:04d}-{as_of.month:02d}",
            as_of=as_of,
            score=detail.score,
            coverage=detail.coverage,
            gap=None if g is None else g[2],
            label=regime_label(as_of, detail),
        ))
    return out


def detected_episodes(points: list[MonthlyPoint], min_months: int = 3
                      ) -> list[tuple[str, str]]:
    """MA36 이격이 음수인 구간(= 하회 국면)을 기계 추출한다.

    국면 '라벨'이 아니라 이격 부호로 뽑는 이유 — 국면의 정의 자체가
    usdkrw-below-ma36-episodes.md에서 MA36 하회이고, FRS 점수는 그 국면
    안에서 압력의 방향을 말하는 별개 축이기 때문이다. 둘을 섞으면 무엇을
    재현했는지 알 수 없게 된다."""
    runs: list[tuple[str, str]] = []
    cur_start: str | None = None
    prev: str | None = None
    for p in points:
        below = p.gap is not None and p.gap < 0
        if below and cur_start is None:
            cur_start = p.month
        elif not below and cur_start is not None:
            if _months_between(cur_start, prev) + 1 >= min_months:
                runs.append((cur_start, prev))
            cur_start = None
        if below:
            prev = p.month
    if cur_start is not None and prev is not None:
        if _months_between(cur_start, prev) + 1 >= min_months:
            runs.append((cur_start, prev))
    return runs


def _months_between(a: str, b: str) -> int:
    ya, ma = int(a[:4]), int(a[5:7])
    yb, mb = int(b[:4]), int(b[5:7])
    return (yb * 12 + mb) - (ya * 12 + ma)


def match_known_episodes(points: list[MonthlyPoint], tolerance_months: int = 3):
    """탐지된 구간을 알려진 국면과 대조한다 → [(tag, 판정, 상세)].

    ⚠ 허용오차 밖의 후보와는 **짝을 짓지 않는다.** 처음엔 "가장 가까운
    구간"을 무조건 붙였더니, 아직 2개월밖에 안 지나 탐지 최소길이(3개월)에
    못 미치는 ⑥국면이 70개월 떨어진 ⑤에 매칭돼 "시작 오차 70개월 불일치"로
    보고됐다. 미탐지와 오탐지는 다른 사건이라 구분해서 보고해야 한다."""
    found = detected_episodes(points)
    results = []
    for tag, known_start, known_end in KNOWN_EPISODES:
        candidates = [
            (abs(_months_between(known_start, f_start)), f_start, f_end)
            for f_start, f_end in found
            if abs(_months_between(known_start, f_start)) <= tolerance_months
        ]
        if not candidates:
            ongoing = " (진행 중 — 탐지 최소길이 미달일 수 있음)" if known_end is None else ""
            results.append((tag, "⚠ 미탐지",
                            f"실제 {known_start}~{known_end or '진행중'}{ongoing}"))
            continue
        d_start, f_start, f_end = min(candidates)
        d_end = (None if known_end is None
                 else abs(_months_between(known_end, f_end)))
        ok = d_end is None or d_end <= tolerance_months
        detail = (f"실제 {known_start}~{known_end or '진행중'} / "
                  f"탐지 {f_start}~{f_end} (시작 오차 {d_start}개월"
                  + (f", 종료 오차 {d_end}개월)" if d_end is not None else ")"))
        results.append((tag, "✅ 재현" if ok else "❌ 종료 불일치", detail))
    return results


def score_stats_by_regime(points: list[MonthlyPoint]) -> dict[str, dict]:
    """하회 국면 안 vs 밖에서 FRS 점수 분포가 실제로 다른가.

    다르지 않다면 요인·가중치가 국면을 설명하지 못한다는 뜻이고, 설계 §6대로
    가중치를 다시 잡아야 한다."""
    inside = [p.score for p in points if p.gap is not None and p.gap < 0 and p.score is not None]
    outside = [p.score for p in points if p.gap is not None and p.gap >= 0 and p.score is not None]
    def summarize(xs):
        if not xs:
            return {"n": 0}
        return {"n": len(xs), "중앙값": statistics.median(xs),
                "평균": statistics.fmean(xs),
                "양수비율": sum(1 for x in xs if x > 0) / len(xs) * 100}
    return {"하회 국면 중": summarize(inside), "그 외": summarize(outside)}


def score_without_ma36(detail) -> float | None:
    """ma36_gap 요인을 빼고 남은 가중치로 재정규화한 점수.

    ⚠ 순환논리 점검용 — MA36 이격은 8개 요인 중 하나(가중 5)인데 국면 구분
    자체도 MA36 이격 부호로 한다. 즉 "FRS가 국면을 구분한다"는 결과에
    구조적으로 자기참조가 섞여 있다. 가중 5/100라 영향이 작을 것으로
    예상했지만 확인 없이 넘어가면 안 되는 종류의 문제다.

    2026-09-10 실측 결과: 이 요인을 빼면 분리가 오히려 **더 선명해진다**
    (하회 중 중앙값 +14.3→+18.3, 그 외 +2.7→+0.8) — 나머지 7개 요인이
    국면을 실제로 설명하고 있고 순환논리가 결과를 만든 게 아니다."""
    if detail.score is None:
        return None
    ma = detail.factor("ma36_gap")
    if ma is None or not ma.available:
        return detail.score
    raw = detail.score * detail.covered_weight / 100 - ma.contribution
    remaining = detail.covered_weight - ma.weight
    return None if remaining <= 0 else raw / remaining * 100


def separation_report(start: date, end: date, risk_events: dict | None = None) -> dict:
    """하회 국면 안/밖에서 점수 분포가 다른지 — ma36 포함/제외 양쪽으로.

    다르지 않다면 요인·가중치가 국면을 설명하지 못한다는 뜻이고 설계 §6대로
    가중치를 다시 잡아야 한다."""
    buckets: dict[str, list[float]] = {
        "포함_하회": [], "포함_그외": [], "제외_하회": [], "제외_그외": []}
    for as_of in iter_month_ends(start, end):
        detail = calculate_frs(as_of, risk_events)
        g = ma36_gap(as_of)
        if detail.score is None or g is None:
            continue
        below = g[2] < 0
        buckets["포함_하회" if below else "포함_그외"].append(detail.score)
        adj = score_without_ma36(detail)
        if adj is not None:
            buckets["제외_하회" if below else "제외_그외"].append(adj)

    def summarize(xs: list[float]) -> dict:
        if not xs:
            return {"n": 0}
        return {"n": len(xs), "중앙값": statistics.median(xs),
                "평균": statistics.fmean(xs),
                "양수비율": sum(1 for x in xs if x > 0) / len(xs) * 100}
    return {k: summarize(v) for k, v in buckets.items()}
