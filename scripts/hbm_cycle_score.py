"""HBM Cycle Score — 외국인수급·보유율 2축 자동 채점 (hbm-cycle-score.md "1.").

2026-08-05 신설, 2026-08-06 개정(B), **2026-08-27 daily_report.py에서
공유 모듈로 추출** — 이 두 함수는 원래 daily_report.py 안에서만 정의돼
있어서, PEOS 일일 리포트(engine/report/)가 같은 채점을 쓰려면 로직을
그대로 복붙해야 했다(중복 = 한쪽만 고치고 잊어버리는 드리프트 위험).
호출자 둘 다(daily_report.py, engine/report/payload.py) 이 모듈 하나를
import하도록 정리.

⚠ 이 배점 세부 구간은 hbm-cycle-score.md에 공식 문서화된 적이 없다 — 이
페이지에 명시된 건 "외국인수급 15점/보유율 15점"이라는 축 자체의 배점뿐,
그 안의 세부 채점 규칙은 없었다(그동안 Claude가 매일 정성적으로 판단).
아래는 그 정성판단을 재현 가능한 규칙으로 코드화한 "초안"이며,
hbm-cycle-score.md에 공식 반영되기 전까지는 참고용 보조 신호로만 쓸 것 —
최종 확정 점수는 계속 사람(또는 Claude)이 검토.

2026-08-06: 웹 조사(wiki/concepts/automation-vs-ai-narrative-roadmap.md "B")에서
확인한 CNN Fear&Greed Index 방법론 — "고정 임계값 이분법"(8/4/3점 식) 대신
"과거 분포 대비 얼마나 벗어났는지"(z-score)를 0~점수만점 연속 스케일로 압축.
국면이 바뀌어도 임계값을 손으로 재조정할 필요가 없다는 게 이점(과거 분포
자체가 매일 갱신되며 자동 보정). stats_utils.zscore/logistic_scale이 표본
부족(5건 미만) 시 자동으로 중립값을 반환하므로, 데이터 축적 초기에는
기존 "미확인 → 중립 부여" 분기와 동일하게 동작한다.

이 모듈은 두 가지 호출 컨텍스트 모두에서 import 가능해야 한다:
  - `cd scripts && python3 daily_report.py` (사이블링 스타일, scripts/가 sys.path[0])
  - `PYTHONPATH=. python3 -m engine.report.run` (패키지 스타일, repo root가 sys.path[0])
아래 try/except가 그 두 컨텍스트를 모두 처리한다.
"""
from __future__ import annotations

try:
    from scripts.investor_flow import read_ticker_rows, summarize_flows, read_price_snapshot_rows, foreign_hold_pct_trend
    from scripts.stats_utils import zscore, anomaly_label, logistic_scale
except ImportError:
    from investor_flow import read_ticker_rows, summarize_flows, read_price_snapshot_rows, foreign_hold_pct_trend
    from stats_utils import zscore, anomaly_label, logistic_scale


def _rolling_sum_history(rows, key, window):
    """rows(날짜순 정렬)에서 window일 누적합의 시계열. 반환 리스트의 마지막
    값이 rows 전체 기준 최신 window일 누적합, 그 앞은 하루씩 이전 시점 기준
    누적합(=z-score history로 사용). 2026-08-06 신설(B). 청크 안에 빈 값이
    섞이면 그 지점은 None — 지어내지 않는다."""
    vals = [int(r[key]) if r.get(key) not in ("", None) else None for r in rows]
    out = []
    for i in range(window, len(vals) + 1):
        chunk = vals[i - window:i]
        out.append(None if any(v is None for v in chunk) else sum(chunk))
    return out


def score_foreign_flow_axis(ticker):
    """외국인수급 축(15점 만점) 채점: 당일(3점)·20일 누적(8점)은 z-score 연속
    스케일(B), 5일vs20일 모멘텀(4점)은 방향 이분법 유지 — 스프레드 시계열
    z-score에는 최소 25영업일치 원자료가 필요해(20일 누적을 하루씩 밀어야
    함) 아직 표본이 부족할 가능성이 높다. 데이터가 쌓이면 동일 방식으로
    전환 예정."""
    rows = read_ticker_rows(ticker)
    summary = summarize_flows(rows)
    w20, w5, w1 = summary.get(20), summary.get(5), summary.get(1)
    detail = {}
    score = 0.0

    daily_vals = [int(r["foreign_net_krw"]) for r in rows if r["foreign_net_krw"] not in ("", None)]
    if w1 is None or w1["foreign"] is None or len(daily_vals) < 2:
        detail["당일"] = "미확인 — 3점 중 1.5점(중립) 부여"
        score += 1.5
    else:
        z1 = zscore(daily_vals[-1], daily_vals[:-1])
        pts = logistic_scale(z1, max_score=3.0)
        score += pts
        detail["당일"] = f"순매수 {w1['foreign']:+,}원, {anomaly_label(z1)} → {pts}/3.0점"

    sum20_hist = _rolling_sum_history(rows, "foreign_net_krw", 20)
    if w20 is None or w20["foreign"] is None or len(sum20_hist) < 2:
        detail["20일_누적"] = "미확인(데이터 부족) — 8점 중 4점(중립) 부여"
        score += 4.0
    else:
        z20 = zscore(sum20_hist[-1], sum20_hist[:-1])
        pts = logistic_scale(z20, max_score=8.0)
        score += pts
        collapse_note = "(붕괴조건④ 충족)" if w20["foreign"] < 0 else ""
        detail["20일_누적"] = (
            f"순{'매수' if w20['foreign'] >= 0 else '매도'} 우위 {w20['foreign']:+,}원{collapse_note}, "
            f"{anomaly_label(z20)} → {pts}/8.0점"
        )

    if w5 is None or w20 is None or w5["foreign"] is None or w20["foreign"] is None:
        detail["모멘텀(5일vs20일)"] = "미확인 — 4점 중 2점(중립) 부여"
        score += 2.0
    else:
        w5_daily_avg = w5["foreign"] / 5
        w20_daily_avg = w20["foreign"] / 20
        if w5_daily_avg > w20_daily_avg:
            detail["모멘텀(5일vs20일)"] = f"최근 5일 일평균({w5_daily_avg:+,.0f}원) > 20일 일평균({w20_daily_avg:+,.0f}원) → 4/4점"
            score += 4.0
        else:
            detail["모멘텀(5일vs20일)"] = f"최근 5일 일평균({w5_daily_avg:+,.0f}원) ≤ 20일 일평균({w20_daily_avg:+,.0f}원) → 0/4점"

    return {"score": round(score, 1), "max": 15.0, "detail": detail}


def score_foreign_holding_axis(ticker):
    """외국인 보유율 축(15점 만점) 채점: 전일 대비 %p 변화(10점)는 z-score
    연속 스케일(B), 5일평균추세(5점)는 방향 이분법 유지 — 표본 자체가
    스냅샷 5개뿐이라 그 안에서 또 z-score를 낼 과거 분포가 없다(순환참조)."""
    rows = read_price_snapshot_rows(ticker)
    trend = foreign_hold_pct_trend(ticker, days=5)
    detail = {}
    score = 0.0

    change = trend["latest_change_pp"]
    pct_vals = [float(r["foreign_hold_pct"]) for r in rows if r.get("foreign_hold_pct") not in ("", None)]
    daily_diffs = [pct_vals[i] - pct_vals[i - 1] for i in range(1, len(pct_vals))]
    if change is None or len(daily_diffs) < 2:
        detail["전일대비"] = "미확인(스냅샷 2건 미만) — 10점 중 5점(중립) 부여"
        score += 5.0
    else:
        z = zscore(daily_diffs[-1], daily_diffs[:-1])
        pts = logistic_scale(z, max_score=10.0)
        score += pts
        detail["전일대비"] = f"{change:+.2f}%p, {anomaly_label(z)} → {pts}/10.0점"

    pts_trend = trend["trend"]
    if len(pts_trend) < 2:
        detail["5일평균추세"] = "미확인(스냅샷 부족) — 5점 중 2.5점(중립) 부여"
        score += 2.5
    else:
        avg_change = (pts_trend[-1][1] - pts_trend[0][1]) / (len(pts_trend) - 1)
        if avg_change > 0:
            detail["5일평균추세"] = f"일평균 {avg_change:+.3f}%p/일(상승) → 5/5점"
            score += 5.0
        else:
            detail["5일평균추세"] = f"일평균 {avg_change:+.3f}%p/일(하락/보합) → 0/5점"

    return {"score": round(score, 1), "max": 15.0, "detail": detail}
