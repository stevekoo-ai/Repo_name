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
    credit_balance_streak, read_latest_short_sale, read_latest_index, read_credit_balance_rows,
    read_price_snapshot_rows, read_short_sale_rows, read_index_rows,
)
from stats_utils import zscore, anomaly_label
from hbm_cycle_score import score_foreign_flow_axis, score_foreign_holding_axis
from capex_periphery import read_hyperscaler_capex, read_ai_periphery

KST = timezone(timedelta(hours=9))
REPORT_DIR = Path(__file__).resolve().parent.parent / "sources"
PORTFOLIO_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "portfolio-holdings.csv"

# HBM Cycle Score(hbm-cycle-score.md "1.") 외국인수급(15점)·보유율(15점)
# 2축 자동 채점은 2026-08-27부로 hbm_cycle_score.py로 옮겼다(전문/이력은
# 그 파일 docstring 참고) — engine/report/payload.py도 같은 모듈을 import해
# 두 리포트가 서로 다른 채점 로직을 쓰는 드리프트를 막는다.


def _month_trend(rows, date_key, value_key, days=30):
    """rows(날짜순 정렬됨)의 최신 값과, 최신 시점 기준 최근 `days` 캘린더일 전
    값을 비교. 2026-09-01 신설 — 사용자 지적("보고서에 트렌드가 안 보여"): 이전엔
    모든 섹션이 그날 하루치 값만 보여줬다. 실측 축적 CSV(sk-hynix-price-snapshot 등)
    는 이미 최소 1개월치가 쌓여 있어 새 수집 없이 여기서 계산만 하면 된다.

    창(30일)을 채울 만큼 데이터가 없으면 있는 것 중 가장 오래된 값으로 대체하고
    `actual_days`로 실제 며칠치인지 명시한다 — 30일 트렌드인 척 지어내지 않는다.
    행이 2건 미만이면 None(섹션에서 "데이터 부족"으로 표시).
    """
    if len(rows) < 2:
        return None
    latest = rows[-1]
    latest_date = datetime.strptime(latest[date_key], "%Y-%m-%d").date()
    cutoff = latest_date - timedelta(days=days)
    window = [r for r in rows if datetime.strptime(r[date_key], "%Y-%m-%d").date() >= cutoff]
    if len(window) < 2:
        window = rows  # 창 안에 데이터가 모자라면 있는 전체로 대체(그만큼 짧게 표기)
    start = window[0]
    start_val = float(start[value_key])
    latest_val = float(latest[value_key])
    vals = [float(r[value_key]) for r in window]
    actual_days = (latest_date - datetime.strptime(start[date_key], "%Y-%m-%d").date()).days
    return {
        "start_date": start[date_key], "start_val": start_val,
        "latest_date": latest[date_key], "latest_val": latest_val,
        "delta": latest_val - start_val,
        "pct": ((latest_val - start_val) / start_val * 100) if start_val else None,
        "min": min(vals), "max": max(vals),
        "actual_days": actual_days, "n": len(window), "window_days": days,
    }


def _fmt_trend_line(label, trend, unit="", decimals=0, hint_cmd=None):
    """_month_trend() 결과 하나를 리포트 한 줄로 렌더. trend가 None이면(데이터
    2건 미만) 값을 지어내지 않고 부족하다고만 표시 — hint_cmd가 있으면 어떤
    명령을 먼저 실행해야 채워지는지 안내(다른 섹션의 기존 관례와 동일)."""
    if trend is None:
        hint = f" — {hint_cmd}를 먼저 실행하세요." if hint_cmd else " — 자동 축적 중, 데이터가 쌓이면 채워집니다."
        return f"- {label}: 데이터 부족(최소 2일치 필요){hint}"
    fmt = "{:,.%df}" % decimals
    start_str, latest_str, delta_str = (fmt.format(trend["start_val"]), fmt.format(trend["latest_val"]),
                                         fmt.format(trend["delta"]))
    sign = "+" if trend["delta"] >= 0 else ""
    pct_str = f", {trend['pct']:+.1f}%" if trend["pct"] is not None else ""
    short_window = trend["actual_days"] < trend["window_days"] - 3
    span_note = f"{trend['actual_days']}일간" + ("(30일 미만 — 데이터 축적 중)" if short_window else "")
    return (f"- {label}: {trend['start_date']} {start_str}{unit} → {trend['latest_date']} {latest_str}{unit} "
            f"({sign}{delta_str}{unit}{pct_str}, {span_note}, 구간 {fmt.format(trend['min'])}~{fmt.format(trend['max'])}{unit})")


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


# read_hyperscaler_capex()/read_ai_periphery()는 2026-08-27부로 capex_periphery.py로
# 옮겼다(전문/이력은 그 파일 docstring 참고) — engine/report/payload.py도 같은
# 모듈을 import해 두 리포트가 서로 다른 CapEx 실측 숫자를 보여주는 드리프트를 막는다.


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

    # --- 최근 1개월 트렌드 (2026-09-01 신설) ---
    # 사용자 지적: "보고서에 트렌드가 안 보여" — 그동안 모든 섹션이 그날 하루치
    # 값만 보여주고, 오르는 중인지 내리는 중인지 알 수 없었다. 이미 매일
    # investor_flow.py snapshot/fetch/credit-balance/short-sale/index-quote가
    # sources/*.csv에 축적해온 실측 데이터를 새로 수집하지 않고 여기서 비교만
    # 한다 — 창작 없음, 데이터가 30일 미만이면 그만큼 짧다고 명시.
    lines.append("\n## 최근 1개월 트렌드 (실측 축적 데이터 기반)")
    lines.append(_fmt_trend_line("주가", _month_trend(read_price_snapshot_rows(ticker), "date", "price"),
                                  unit="원", decimals=0, hint_cmd="investor_flow.py snapshot"))
    lines.append(_fmt_trend_line("외국인 보유율", _month_trend(read_price_snapshot_rows(ticker), "date", "foreign_hold_pct"),
                                  unit="%", decimals=2, hint_cmd="investor_flow.py snapshot"))
    lines.append(_fmt_trend_line("신용융자잔고", _month_trend(read_credit_balance_rows(ticker), "date", "loan_balance_qty"),
                                  unit="주", decimals=0, hint_cmd="investor_flow.py credit-balance"))
    lines.append(_fmt_trend_line("공매도 비중", _month_trend(read_short_sale_rows(ticker), "date", "short_vol_pct"),
                                  unit="%", decimals=2, hint_cmd="investor_flow.py short-sale"))
    lines.append(_fmt_trend_line("코스피지수", _month_trend(read_index_rows("0001"), "date", "price"),
                                  unit="", decimals=2, hint_cmd="investor_flow.py index-quote"))

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
        # 2026-09-01 — crosscheck=RESOLVED_2OF3(3방법 중 rate·hist 두 독립
        # 방법만 일치, calc/diff필드는 배제)은 값을 조용히 섞어 넣지 않고
        # 어떤 근거로 확정됐는지 그대로 노출 — MISMATCH는 아니지만 완전한
        # 3/3 합치도 아니라는 걸 숨기지 않는다.
        resolved_note = (f" [ℹ️ 자동확정: rate·hist 일치, calc 배제 — {adr.get('crosscheck_detail', '')}]"
                          if adr.get("crosscheck") == "RESOLVED_2OF3" else "")
        lines.append(f"- {adr['date']} 기준: **${float(adr['price']):,.2f}** ({float(adr['change']):+,.2f}, {pct:+.2f}%){flag}, 전일종가 ${float(adr['prev_close']):,.2f}{resolved_note}")

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

    # --- AI 밸류체인 변두리 조기경보 (2026-08-07 신설) ---
    periphery = read_ai_periphery()
    if periphery is not None:
        lines.append("\n## AI 밸류체인 변두리 조기경보 (SEC EDGAR, 주도주보다 먼저 꺾이는 자리)")
        alerts = []
        for tk in ("VRT", "GEV", "AMKR", "ALAB", "CRDO", "COHR", "LITE", "SMCI"):
            info = periphery.get(tk)
            if info is None:
                continue
            parts = []
            for metric, label in (("backlog", "백로그"), ("revenue", "매출")):
                m = info["metrics"].get(metric)
                if m is None:
                    continue
                qoq = f"{m['qoq_pct']:+.1f}%" if m["qoq_pct"] is not None else "QoQ 미확인"
                stale = " ⚠스테일" if m["is_stale"] else ""
                parts.append(f"{label} ${m['value_usd']/1e9:,.2f}B({qoq}){stale}")
                # 조기경보 판정 — 백로그 감소가 이 섹션의 핵심 신호
                if m["qoq_pct"] is not None and m["qoq_pct"] < 0:
                    sev = "🔴" if metric == "backlog" else "🟡"
                    alerts.append(f"{sev} {info['company']}({tk}) {label} 전분기 대비 {m['qoq_pct']:+.1f}%")
            if parts:
                lines.append(f"- **{info['company']}({tk})** [{info['layer']}]: " + " / ".join(parts))
        if alerts:
            lines.append("\n**⚠ 감소 전환 감지 — 아래 항목은 사람이 원인 확인 필요:**")
            for a in alerts:
                lines.append(f"  - {a}")
        else:
            lines.append("- ✅ 감소 전환 없음 — 변두리 백로그·매출 전부 증가 또는 유지")
        lines.append("- 한미반도체·HD현대일렉트릭(한국)·이비덴(일본)·ASE(대만)는 SEC 미제출이라 자동수집 대상 밖 — wiki/concepts/ai-value-chain-periphery-monitor.md에서 수동 추적")

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
