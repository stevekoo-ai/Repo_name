#!/usr/bin/env python3
"""
GitHub Actions용 1차 리포트 생성기 — 순수 규칙 기반, LLM 호출 없음.

investor_flow.py로 이미 모아둔 시세·수급 데이터를 가지고 "판단이 필요 없는"
기계적 계산만 수행한다: 오늘 등락률 ±5% 플래그, 외국인/기관/개인 1·5·20·60일
누적 순매수, HBM Cycle Score 붕괴조건④(외국인 20일 누적 순매도 전환) 체크.
뉴스 해석·모순 발견·서사 종합 같은 "진짜 판단"은 여기서 하지 않는다 — 그건
사람이 이 리포트를 읽고 필요하면 Claude(또는 다른 LLM)에게 넘기는 몫이다.

사용법:
  python3 scripts/daily_report.py --ticker 000660
  # sources/sk-hynix-auto-report-<날짜시각>.md 생성 + stdout에도 출력(이메일 본문용)
"""
import argparse
import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path

from investor_flow import (
    kis_fetch_price, read_ticker_rows, summarize_flows, read_latest_adr, read_latest_price_snapshot,
    foreign_hold_pct_trend, credit_balance_streak, read_latest_short_sale, read_latest_index,
    read_price_snapshot_rows, read_credit_balance_rows,
)
from stats_utils import zscore, anomaly_label, logistic_scale

KST = timezone(timedelta(hours=9))
REPORT_DIR = Path(__file__).resolve().parent.parent / "sources"
PORTFOLIO_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "portfolio-holdings.csv"
HYPERSCALER_CAPEX_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "hyperscaler-capex.csv"
HYPERSCALER_CAPEX_STALE_DAYS = 150  # 분기 실적은 보통 분기말+30~45일 내 공시 — 5개월 이상 지나면 스테일로 취급

# 2026-08-05 신설, 2026-08-06 개정(B) — HBM Cycle Score(hbm-cycle-score.md "1.")
# 6축 중 외국인수급(15점)·보유율(15점) 두 축을 매일 사람이 CSV를 보고 손으로
# 채점하던 것을 대체하는 초안 규칙. ⚠ 이 배점 세부 구간은 hbm-cycle-score.md에
# 공식 문서화된 적이 없다 — 이 페이지에 명시된 건 "외국인수급 15점/보유율 15점"
# 이라는 축 자체의 배점뿐, 그 안의 세부 채점 규칙은 없었다(그동안 Claude가
# 매일 정성적으로 판단). 아래는 그 정성판단을 재현 가능한 규칙으로 코드화한
# "초안"이며, hbm-cycle-score.md에 공식 반영되기 전까지는 참고용 보조 신호로만
# 쓸 것 — 최종 확정 점수는 계속 사람(또는 Claude)이 검토.
#
# 2026-08-06: 웹 조사(wiki/concepts/automation-vs-ai-narrative-roadmap.md "B")에서
# 확인한 CNN Fear&Greed Index 방법론 — "고정 임계값 이분법"(8/4/3점 식) 대신
# "과거 분포 대비 얼마나 벗어났는지"(z-score)를 0~점수만점 연속 스케일로 압축.
# 국면이 바뀌어도 임계값을 손으로 재조정할 필요가 없다는 게 이점(과거 분포
# 자체가 매일 갱신되며 자동 보정). stats_utils.zscore/logistic_scale이 표본
# 부족(5건 미만) 시 자동으로 중립값을 반환하므로, 데이터 축적 초기에는
# 기존 "미확인 → 중립 부여" 분기와 동일하게 동작한다.
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


def read_latest_portfolio_summary():
    """portfolio-holdings.csv에서 계좌별 최신 날짜 기준 합계 평가금액 + SK하이닉스
    비중을 계산. 2026-08-05 신설 — sources/portfolio-holdings.csv가 없거나
    비어있으면 None(섹션 자체 생략, 억지로 만들지 않음)."""
    if not PORTFOLIO_CSV_PATH.exists():
        return None
    rows = []
    with PORTFOLIO_CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return None

    latest_date = max(r["date"] for r in rows)
    latest_rows = [r for r in rows if r["date"] == latest_date]

    by_account = {}
    for r in latest_rows:
        acc = r["account_label"]
        by_account.setdefault(acc, {"total": 0.0, "sk_hynix": 0.0, "rows": []})
        amt = float(r["eval_amount"])
        by_account[acc]["total"] += amt
        by_account[acc]["rows"].append(r)
        if r["ticker"] == "000660":
            by_account[acc]["sk_hynix"] += amt

    grand_total = sum(a["total"] for a in by_account.values())
    grand_sk = sum(a["sk_hynix"] for a in by_account.values())
    return {
        "date": latest_date, "by_account": by_account,
        "grand_total": grand_total, "grand_sk": grand_sk,
        "sk_pct": (grand_sk / grand_total * 100) if grand_total else None,
    }


def read_hyperscaler_capex():
    """sources/hyperscaler-capex.csv(scripts/sec_edgar_capex.py, SEC EDGAR XBRL)에서
    회사별 최신 분기 CapEx + 직전 분기 대비 QoQ%를 계산. 2026-08-06 신설 —
    HBM Cycle Score "고객재고" 축(10점, 지금까지 전적으로 어닝콜 논조 해석)에
    실측 CapEx 숫자를 보조 근거로 붙인다(축 자체를 자동채점하진 않음 — 논조
    판단은 여전히 사람/Claude 몫, 여기선 "숫자가 실제로 얼마였나"만 제공).

    ⚠ 2026-08-06 데이터 정합성 버그 발견·수정: SEC companyconcept API가 같은
    분기(end_date)를 서로 다른 fiscal_year/fiscal_period로 중복 보고하는
    경우가 있어(나중 필링의 "전년동기 비교치"로 재수록될 때) 예전 코드가
    이를 별개 분기처럼 저장했었다 — end_date 기준으로 재정리하도록 고쳤다
    (scripts/sec_edgar_capex.py 참고). 값 자체가 충돌하는 경우(MSFT 사례
    확인됨)는 CSV `note` 컬럼에 남겨두고 여기서도 그대로 노출한다 — 조용히
    하나를 버리지 않는다.
    스테일 판정: 최신 end_date가 오늘로부터 HYPERSCALER_CAPEX_STALE_DAYS일
    이상 지났으면 "확인됐지만 오래된 값"으로 명시 표기(최신인 것처럼 꾸미지
    않는다) — 이 세션은 SEC 라이브 접속이 막혀 있어 재조회로 최신성을 직접
    검증하지 못했다, GitHub Actions 재실행 필요."""
    if not HYPERSCALER_CAPEX_CSV_PATH.exists():
        return None
    with HYPERSCALER_CAPEX_CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return None

    by_ticker = {}
    for r in rows:
        by_ticker.setdefault(r["ticker"], []).append(r)

    today = datetime.now(KST).date()
    out = {}
    for ticker, company_rows in by_ticker.items():
        company_rows.sort(key=lambda r: r["end_date"])
        latest = company_rows[-1]
        end_date = datetime.strptime(latest["end_date"], "%Y-%m-%d").date()
        days_stale = (today - end_date).days
        qoq_pct = None
        if len(company_rows) >= 2:
            prev_val = float(company_rows[-2]["value_usd"])
            if prev_val:
                qoq_pct = (float(latest["value_usd"]) - prev_val) / prev_val * 100
        out[ticker] = {
            "company": latest["company"], "end_date": latest["end_date"],
            "value_usd": float(latest["value_usd"]), "qoq_pct": qoq_pct,
            "days_stale": days_stale, "is_stale": days_stale >= HYPERSCALER_CAPEX_STALE_DAYS,
            "note": latest.get("note", ""),
        }
    return out


def build_report(ticker: str) -> str:
    now = datetime.now(KST)
    lines = []
    lines.append(f"# SK하이닉스 자동 1차 리포트 ({ticker})")
    lines.append(f"\n생성 시각: {now.strftime('%Y-%m-%d %H:%M')} KST")
    lines.append("\n⚠ 이 리포트는 규칙 기반 자동 생성입니다 — 뉴스 해석·모순 검증·서사 종합은 포함하지 않습니다. 판단이 필요하면 이 리포트를 근거로 별도 요청하세요.\n")

    # --- 시세 ---
    lines.append("## 시세")
    try:
        q = kis_fetch_price(ticker)
        flag = " 🚨 급변동(당일 ±5% 이상)" if abs(q["change_pct"]) >= 5 else ""
        lines.append(f"- 현재가/종가: **{q['price']:,}원** ({q['change']:+,}원, {q['change_pct']:+.2f}%){flag}")
        lines.append(f"- 거래량: {q['volume']:,}주")
    except SystemExit as e:
        lines.append(f"- 시세 조회 실패: {e}")

    # --- 외국인 보유율 & 250일 최고가 대비 드로다운 ---
    # 2026-07-28 추가: 그동안 "KSD 보유율 미확인"·"정확한 종가 미확인"으로
    # 반복 표기되던 항목을 investor_flow.py snapshot 커맨드가 채워둔
    # sk-hynix-price-snapshot.csv에서 읽어온다(웹검색 불필요).
    lines.append("\n## 외국인 보유율 & 250일 최고가 대비")
    snap = read_latest_price_snapshot(ticker)
    if snap is None:
        lines.append("- 기록 없음 — investor_flow.py snapshot을 먼저 실행하세요.")
    else:
        lines.append(f"- {snap['date']} 기준 외국인 보유율: **{float(snap['foreign_hold_pct']):.2f}%** (보유 {int(snap['foreign_hold_qty']):,}주)")
        lines.append(
            f"- 250일 최고가: {int(snap['day250_high']):,}원({snap['day250_high_date']}) "
            f"대비 **{float(snap['day250_high_vrss_pct']):+.2f}%**"
        )

    # --- ADR ---
    lines.append("\n## ADR(SKHY, 나스닥)")
    adr = read_latest_adr("SKHY")
    if adr is None:
        lines.append("- 기록 없음 — investor_flow.py adr-quote를 먼저 실행하세요(미국 장중에만 유의미).")
    elif adr.get("crosscheck") == "MISMATCH" or not adr.get("change_pct"):
        # 2026-08-01 — change_pct 크로스체크(3가지 방법) 불일치 시 investor_flow.py가
        # 숫자를 지어내지 않고 이 필드를 비워둔다. 여기서도 float()로 억지로
        # 채우지 않고 그대로 미확정 표시 — 사람이 보고 결정할 몫이다.
        lines.append(
            f"- {adr.get('date', '?')} 기준: **${float(adr['price']):,.2f}**, 전일종가 ${float(adr['prev_close']):,.2f} — "
            f"⚠️ change_pct 크로스체크 불일치(MISMATCH), 등락률 미확정: {adr.get('crosscheck_detail', '')} "
            "(사용자 확인 필요, sk-hynix-adr-quote.csv 참고)"
        )
    else:
        pct = float(adr["change_pct"])
        flag = " 🚨 급변동(±5% 이상)" if abs(pct) >= 5 else ""
        lines.append(f"- {adr['date']} 기준: **${float(adr['price']):,.2f}** ({float(adr['change']):+,.2f}, {pct:+.2f}%){flag}, 전일종가 ${float(adr['prev_close']):,.2f}")

    # --- 수급 ---
    lines.append("\n## 투자자별 순매수")
    rows = read_ticker_rows(ticker)
    if not rows:
        lines.append("- 기록 없음 — investor_flow.py fetch를 먼저 실행하세요.")
    else:
        latest = rows[-1]
        lines.append(f"- 최신 기록일: {latest['date']}")
        summary = summarize_flows(rows)
        label_ko = {"foreign": "외국인", "inst": "기관", "retail": "개인"}
        for window, result in summary.items():
            if result is None:
                lines.append(f"- {window}일 누적: 미확인 — {window}영업일치 기록 부족(현재 {len(rows)}일치 보유)")
                continue
            parts = []
            for key, ko in label_ko.items():
                v = result[key]
                parts.append(f"{ko} {'미확인' if v is None else f'{v:+,}원'}")
            lines.append(f"- {window}일 누적: " + " / ".join(parts))

        # --- 붕괴조건④: 외국인 20일 누적 순매도 전환 ---
        lines.append("\n## HBM Cycle Score 붕괴조건 ④ 체크 (외국인 20일 누적 순매도 전환)")
        w20 = summary.get(20)
        if w20 is None or w20["foreign"] is None:
            lines.append("- 미확인 — 20영업일치 데이터 부족(자동 축적 중, 매일 실행하면 채워짐)")
        elif w20["foreign"] < 0:
            lines.append(f"- 🔴 **충족** — 외국인 20일 누적 순매도 {w20['foreign']:+,}원")
        else:
            lines.append(f"- 미충족 — 외국인 20일 누적 {w20['foreign']:+,}원(순매수 우위)")

    # --- HBM Cycle Score 6축 중 외국인수급·보유율 2축 초안 채점 (2026-08-05 신설) ---
    lines.append("\n## HBM Cycle Score — 외국인수급·보유율 2축 초안 채점 (30/100점)")
    lines.append("⚠ 이 두 축의 세부 채점 규칙은 hbm-cycle-score.md에 아직 공식 반영되지 않은 초안입니다 — 참고용 보조 신호로 취급하세요.")
    flow_score = score_foreign_flow_axis(ticker)
    hold_score = score_foreign_holding_axis(ticker)
    lines.append(f"\n**외국인수급 축: {flow_score['score']}/{flow_score['max']}점**")
    for k, v in flow_score["detail"].items():
        lines.append(f"  - {k}: {v}")
    lines.append(f"\n**외국인 보유율 축: {hold_score['score']}/{hold_score['max']}점**")
    for k, v in hold_score["detail"].items():
        lines.append(f"  - {k}: {v}")
    lines.append(f"\n**소계: {flow_score['score'] + hold_score['score']:.1f}/30점** (전체 100점 중 나머지 70점은 ASP·엔비디아&CoWoS·공급확대·고객재고 — 뉴스 해석 필요, 자동화 대상 아님)")

    # --- 신용융자잔고 (2026-08-05 신설) ---
    lines.append("\n## 신용융자잔고 (찐반등 신호① — 빚의 청산)")
    cb = credit_balance_streak(ticker)
    if cb["latest"] is None:
        lines.append("- 기록 없음 — investor_flow.py credit-balance를 먼저 실행하세요.")
    else:
        latest = cb["latest"]
        lines.append(f"- {latest['date']} 기준 융자잔고: **{int(latest['loan_balance_qty']):,}주** (비율 {latest['loan_balance_rate']}%)")
        if cb["direction"]:
            # 2026-08-06 버그 수정 — 예전엔 streak_days+1을 표시했는데,
            # investor_flow.py의 credit_balance_streak()가 반환하는
            # streak_days 자체가 이미 "연속 N거래일"의 N이다(가장 최근
            # diff부터 같은 방향인 diff를 셈 — 최근 diff 1개만 맞아도
            # streak_days=1). +1을 더하면 항상 하루 과대표기됐다 — 예를
            # 들어 오늘처럼 어제 하루만 반전됐을 뿐인데 "2거래일 연속"으로
            # 잘못 표시되는 식. streak_days를 그대로 쓴다.
            lines.append(f"- 최근 {cb['streak_days']}거래일 연속 **{cb['direction']}** 추세")
        # 2026-08-06 신설(E) — 연속 추세와 별개로, 오늘 변화폭 자체가 과거
        # 분포에서 얼마나 벗어난 값인지 stats_utils.zscore로 판정. "3거래일
        # 연속 감소"는 방향은 알려주지만 크기는 알려주지 않는다 — 예를 들어
        # 3일 연속 소폭 감소와 하루 만의 급격한 감소는 다른 신호인데, 연속
        # 판정만으론 구분이 안 된다.
        cb_rows = read_credit_balance_rows(ticker)
        cb_qtys = [int(r["loan_balance_qty"]) for r in cb_rows if r.get("loan_balance_qty") not in ("", None)]
        cb_diffs = [cb_qtys[i] - cb_qtys[i - 1] for i in range(1, len(cb_qtys))]
        if len(cb_diffs) < 2:
            lines.append("- 변화폭 이상치 판정: 미확인(데이터 부족, 자동 축적 중)")
        else:
            z_cb = zscore(cb_diffs[-1], cb_diffs[:-1])
            lines.append(f"- 변화폭 이상치 판정: {anomaly_label(z_cb)}")

    # --- 공매도 (2026-08-05 신설) ---
    lines.append("\n## 공매도 추이")
    ss = read_latest_short_sale(ticker)
    if ss is None:
        lines.append("- 기록 없음 — investor_flow.py short-sale을 먼저 실행하세요.")
    else:
        lines.append(f"- {ss['date']} 기준 공매도 거래량 비중: **{ss['short_vol_pct']}%** (누적 비중 {ss['cum_short_vol_pct']}%)")

    # --- 코스피/코스닥 지수 (2026-08-05 신설) ---
    lines.append("\n## 코스피/코스닥 지수")
    for code, name in (("0001", "코스피"), ("1001", "코스닥")):
        idx = read_latest_index(code)
        if idx is None:
            lines.append(f"- {name}: 기록 없음 — investor_flow.py index-quote를 먼저 실행하세요.")
        else:
            lines.append(
                f"- {name}({idx['date']}): **{float(idx['price']):,.2f}** ({float(idx['change']):+,.2f}, {float(idx['change_pct']):+.2f}%), "
                f"상한 {idx['limit_up']}종목/하한 {idx['limit_down']}종목 (상승 {idx['advancers']}/하락 {idx['decliners']}/보합 {idx['unchanged']})"
            )

    # --- 하이퍼스케일러 CapEx 실측 (2026-08-06 신설, HBM Cycle Score 고객재고 축 보조근거) ---
    lines.append("\n## 하이퍼스케일러 CapEx 실측 (SEC EDGAR, HBM Cycle Score 고객재고 축 보조근거)")
    capex = read_hyperscaler_capex()
    if capex is None:
        lines.append("- 기록 없음 — scripts/sec_edgar_capex.py fetch를 먼저 실행하세요.")
    else:
        for t in ("GOOGL", "MSFT", "AMZN", "META"):
            c = capex.get(t)
            if c is None:
                lines.append(f"- {t}: 기록 없음")
                continue
            stale_note = f" ⚠ {c['days_stale']}일 전 데이터 — 최신 아닐 수 있음, 재조회 필요" if c["is_stale"] else ""
            qoq_note = f", 전분기 대비 {c['qoq_pct']:+.1f}%" if c["qoq_pct"] is not None else ""
            conflict_note = f" [{c['note']}]" if c["note"] else ""
            lines.append(f"- **{c['company']}({t})**: {c['end_date']} 분기 ${c['value_usd']/1e9:,.1f}B{qoq_note}{stale_note}{conflict_note}")
        lines.append("- 어닝콜 논조(재고 센티먼트 0~10점 판정)는 이 스크립트 범위 밖 — 위 숫자는 \"실제로 CapEx가 얼마였나\"만 제공")

    # --- 포트폴리오 (2026-08-05 신설, 데이터 없으면 섹션 생략) ---
    port = read_latest_portfolio_summary()
    if port is not None:
        lines.append("\n## 보유 포트폴리오 평가금액")
        lines.append(f"- {port['date']} 기준 총 평가금액: **{port['grand_total']:,.0f}원**")
        if port["sk_pct"] is not None:
            lines.append(f"- SK하이닉스(000660) 비중: **{port['sk_pct']:.1f}%** ({port['grand_sk']:,.0f}원)")
        for acc, data in sorted(port["by_account"].items()):
            acc_sk_pct = (data["sk_hynix"] / data["total"] * 100) if data["total"] else None
            sk_note = f", SK하이닉스 {acc_sk_pct:.1f}%" if acc_sk_pct is not None else ""
            lines.append(f"  - {acc}: {data['total']:,.0f}원{sk_note}")

    lines.append("\n---\n전체 데이터: sources/sk-hynix-investor-flow.csv, sources/sk-hynix-credit-balance.csv, sources/sk-hynix-short-sale.csv, sources/kr-index-quote.csv, sources/portfolio-holdings.csv | 스크립트: scripts/daily_report.py (규칙 기반, LLM 미사용)")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ticker", default="000660")
    args = p.parse_args()

    report = build_report(args.ticker)
    print(report)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(KST).strftime("%Y-%m-%d-%H%M")
    out_path = REPORT_DIR / f"sk-hynix-auto-report-{ts}.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"\n(저장됨: {out_path})", flush=True)


if __name__ == "__main__":
    main()
