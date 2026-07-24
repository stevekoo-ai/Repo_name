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
from datetime import datetime, timezone, timedelta
from pathlib import Path

from investor_flow import kis_fetch_price, read_ticker_rows, summarize_flows

KST = timezone(timedelta(hours=9))
REPORT_DIR = Path(__file__).resolve().parent.parent / "sources"


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

    lines.append("\n---\n전체 데이터: sources/sk-hynix-investor-flow.csv | 스크립트: scripts/daily_report.py (규칙 기반, LLM 미사용)")
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
