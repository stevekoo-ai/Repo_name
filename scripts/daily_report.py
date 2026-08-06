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
)

KST = timezone(timedelta(hours=9))
REPORT_DIR = Path(__file__).resolve().parent.parent / "sources"
PORTFOLIO_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "portfolio-holdings.csv"

# 2026-08-05 신설 — HBM Cycle Score(hbm-cycle-score.md "1.") 6축 중 외국인수급(15점)·
# 보유율(15점) 두 축을 매일 사람이 CSV를 보고 손으로 채점하던 것을 대체하는
# 초안 규칙. ⚠ 이 배점 세부 구간(8/4/3점, 10/5점 등)은 hbm-cycle-score.md에
# 공식 문서화된 적이 없다 — 이 페이지에 명시된 건 "외국인수급 15점/보유율 15점"
# 이라는 축 자체의 배점뿐, 그 안의 세부 채점 규칙은 없었다(그동안 Claude가
# 매일 정성적으로 판단). 아래는 그 정성판단을 재현 가능한 규칙으로 처음
# 코드화한 "초안"이며, hbm-cycle-score.md에 공식 반영되기 전까지는 참고용
# 보조 신호로만 쓸 것 — 최종 확정 점수는 계속 사람(또는 Claude)이 검토.
def score_foreign_flow_axis(ticker):
    """외국인수급 축(15점 만점) 초안 채점: 20일 누적 부호(8점, 붕괴조건④와 동일
    로직) + 20일 대비 5일 모멘텀 방향(4점) + 당일 순매수 부호(3점)."""
    rows = read_ticker_rows(ticker)
    summary = summarize_flows(rows)
    w20, w5, w1 = summary.get(20), summary.get(5), summary.get(1)
    detail = {}
    score = 0.0

    if w20 is None or w20["foreign"] is None:
        detail["20일_누적"] = "미확인(데이터 부족) — 8점 중 4점(중립) 부여"
        score += 4.0
    elif w20["foreign"] > 0:
        detail["20일_누적"] = f"순매수 우위 {w20['foreign']:+,}원 → 8/8점"
        score += 8.0
    else:
        detail["20일_누적"] = f"순매도 우위 {w20['foreign']:+,}원(붕괴조건④ 충족) → 0/8점"

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

    if w1 is None or w1["foreign"] is None:
        detail["당일"] = "미확인 — 3점 중 1.5점(중립) 부여"
        score += 1.5
    elif w1["foreign"] > 0:
        detail["당일"] = f"순매수 {w1['foreign']:+,}원 → 3/3점"
        score += 3.0
    else:
        detail["당일"] = f"순매도 {w1['foreign']:+,}원 → 0/3점"

    return {"score": round(score, 1), "max": 15.0, "detail": detail}


def score_foreign_holding_axis(ticker):
    """외국인 보유율 축(15점 만점) 초안 채점: 전일 대비 %p 변화 부호(10점) +
    최근 5일 스냅샷 평균 변화 방향(5점)."""
    trend = foreign_hold_pct_trend(ticker, days=5)
    detail = {}
    score = 0.0

    change = trend["latest_change_pp"]
    if change is None:
        detail["전일대비"] = "미확인(스냅샷 2건 미만) — 10점 중 5점(중립) 부여"
        score += 5.0
    elif change > 0:
        detail["전일대비"] = f"{change:+.2f}%p 상승 → 10/10점"
        score += 10.0
    elif change < 0:
        detail["전일대비"] = f"{change:+.2f}%p 하락 → 0/10점"
    else:
        detail["전일대비"] = "변화 없음(0.00%p) → 5/10점"
        score += 5.0

    pts = trend["trend"]
    if len(pts) < 2:
        detail["5일평균추세"] = "미확인(스냅샷 부족) — 5점 중 2.5점(중립) 부여"
        score += 2.5
    else:
        avg_change = (pts[-1][1] - pts[0][1]) / (len(pts) - 1)
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
        if cb["direction"] and cb["streak_days"] > 0:
            lines.append(f"- 최근 {cb['streak_days'] + 1}거래일 연속 **{cb['direction']}** 추세")
        elif cb["direction"]:
            lines.append(f"- 전일 대비 {cb['direction']} (연속 추세 아님)")

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
