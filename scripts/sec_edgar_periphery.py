#!/usr/bin/env python3
"""
AI 밸류체인 "변두리" 기업 분기 매출·백로그 실측치 — SEC EDGAR XBRL 자동 수집.

wiki/concepts/ai-value-chain-periphery-monitor.md의 운영지침 ⓐ를 구현한다.
그 페이지의 핵심 발견은 **"주도주(SK하이닉스)의 6축 지표는 전부 주도주 자신의
것이라 조기경보가 안 된다"**는 것이었고, 대안으로 체인 최말단(냉각·전력·광통신·
후공정·인터커넥트·AI서버)의 **백로그/수주잔고**를 보자는 결론이었다 —
백로그는 이미 계약된 미래 매출이라 "주문이 끊겼다"는 신호가 **가장 먼저
나타나는 자리**이기 때문.

이 스크립트는 그 추적을 사람 손·LLM 없이 자동화한다(규칙 기반, 토큰비용 0):
분기 실적은 SEC 정기공시(10-Q)에서 XBRL로 공개되므로 웹검색이 필요 없다.
sec_edgar_capex.py(하이퍼스케일러 CapEx)와 같은 API·같은 인증 방식을 쓰며,
공통 헬퍼(_get_headers/fetch_company_concept)를 그 모듈에서 import해
중복을 만들지 않는다 — 2026-08-06에 고친 데이터 정합성 버그가 이쪽에도
자동으로 적용되도록 하기 위함.

⚠ 자동화 범위의 한계(운영지침에 명시된 그대로):
- **미국 상장 10-Q 제출사만 자동 수집된다.** 한미반도체·HD현대일렉트릭은
  한국 공시(DART), 이비덴은 일본 공시, ASE는 20-F(연간)라 이 스크립트
  범위 밖 — 위키 페이지에서 수동 추적한다.
- 10-Q만 보므로 **4분기(회계연도 마지막 분기)는 빠진다**(10-K에 연간으로만
  실림). sec_edgar_capex.py와 동일한 알려진 한계.

사용법:
  # 8개사 매출+백로그 수집 후 CSV upsert
  python3 scripts/sec_edgar_periphery.py fetch

  # ⚠ 최초 1회 필수 — 백로그(RPO) 태그가 회사마다 어떻게 실리는지 원본 확인
  python3 scripts/sec_edgar_periphery.py fetch --company VRT --raw

  # 저장된 데이터 요약(최근 분기 + QoQ/YoY)
  python3 scripts/sec_edgar_periphery.py show
"""
import argparse
import csv
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# sec_edgar_capex.py와 공통 로직 공유 — User-Agent 정책(SEC 공정접근)·HTTP
# 에러 처리·403 힌트가 이미 실전 검증돼 있어 재사용한다(중복 구현 금지).
from sec_edgar_capex import _get_headers, fetch_company_concept

CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "ai-periphery-fundamentals.csv"
CSV_FIELDS = [
    "company", "ticker", "cik", "layer", "metric", "fiscal_year", "fiscal_period",
    "form", "end_date", "filed_date", "value_usd", "tag", "accn", "source",
    "fetched_at", "note",
]

TICKER_MAP_URL = "https://www.sec.gov/files/company_tickers.json"

# 2026-08-07 조사(ai-value-chain-periphery-monitor.md §2)에서 "체인 최말단"으로
# 확인된 미국 상장사. CIK는 하드코딩하지 않고 SEC 공식 티커맵에서 런타임
# 해석한다 — 이 세션은 SEC 접근이 막혀 CIK를 직접 검증할 수 없었고, 검증
# 못 한 값을 코드에 박아넣지 않기 위함(추측 금지 원칙).
PERIPHERY = {
    "VRT":  {"name": "Vertiv",        "layer": "냉각·전력관리"},
    "GEV":  {"name": "GE Vernova",    "layer": "발전·전력설비"},
    "AMKR": {"name": "Amkor",         "layer": "후공정(OSAT)"},
    "ALAB": {"name": "Astera Labs",   "layer": "인터커넥트"},
    "CRDO": {"name": "Credo",         "layer": "인터커넥트"},
    "COHR": {"name": "Coherent",      "layer": "광통신"},
    "LITE": {"name": "Lumentum",      "layer": "광통신"},
    "SMCI": {"name": "Supermicro",    "layer": "AI서버"},
}

# ASC 606 도입 이후 표준 매출 태그. 단 이 태그가 전체 매출 공시의 약 20%만
# 차지한다는 조사 결과가 있어(회사마다 다른 태그를 씀) 폴백을 넉넉히 둔다.
REVENUE_TAG_CANDIDATES = [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "Revenues",
    "SalesRevenueNet",
]

# 백로그 = ASC 606의 "잔여 수행의무(RPO)". 이게 이 스크립트의 존재 이유
# (매출은 후행, 백로그는 선행)다. RPO는 한 필링에 여러 건(12개월 내/이후/
# 합계)이 실릴 수 있어 같은 end_date에 값이 여러 개 나오며, 아래
# _pick_fact()가 총액(최대값)을 채택하고 나머지를 note에 남긴다.
#
# ⚠ 2026-08-07 실호출 검증 후 수정 — `ContractWithCustomerLiability`를
# 후보에서 **제거**했다. 최초 실행에서 COHR/CRDO/LITE가 RPO를 태깅하지
# 않아 이 태그로 폴백됐는데, 이건 **이연수익(선수금 부채)이지 백로그가
# 아니다**(COHR $70M, LITE $7M, CRDO $3M — 백로그라면 조 단위여야 함).
# 개념이 다른 값을 "백로그"로 리포트에 띄우면 오경보가 나므로, 폴백하느니
# **아예 없는 게 낫다**(숫자를 지어내지 않는다는 원칙의 연장).
BACKLOG_TAG_CANDIDATES = [
    "RevenueRemainingPerformanceObligation",
]

METRICS = {
    "revenue": REVENUE_TAG_CANDIDATES,
    "backlog": BACKLOG_TAG_CANDIDATES,
}

# 분기 duration으로 인정할 일수 범위. 회계분기는 13주(91일)가 표준이나
# 4-4-5 주기·윤년 등으로 88~98일까지 흔들린다.
QUARTER_MIN_DAYS, QUARTER_MAX_DAYS = 80, 100


def resolve_ciks(tickers):
    """SEC 공식 티커→CIK 맵(company_tickers.json)에서 CIK를 해석한다.
    응답은 {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "..."}, ...} 형태이며
    cik_str에 선행 0이 없어 호출 시 zfill(10)이 필요하다(SEC 문서 확인).
    찾지 못한 티커는 지어내지 않고 그대로 실패 목록에 남긴다."""
    req = urllib.request.Request(TICKER_MAP_URL, headers=_get_headers())
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"SEC 티커맵 조회 실패: {e.code} {e.read().decode(errors='replace')[:300]}")
    except urllib.error.URLError as e:
        sys.exit(f"SEC 티커맵 접속 실패: {e.reason} — www.sec.gov 접근 가능 여부를 확인하세요.")

    want = {t.upper() for t in tickers}
    found = {}
    for row in data.values():
        tk = str(row.get("ticker", "")).upper()
        if tk in want:
            found[tk] = str(row["cik_str"])
    missing = sorted(want - set(found))
    return found, missing


def _is_quarterly(fact):
    """duration fact가 '한 분기'인지 판정. SEC companyconcept은 duration 개념
    (매출 등)에 start/end를 함께 주는데, 같은 end에 3개월·6개월·9개월(YTD)
    fact가 **동시에** 실린다.

    ⚠ 2026-08-07 실호출에서 드러난 버그 — 이 필터가 없어서 최대값을 고르는
    바람에 **매출이 전부 누적(YTD)으로 수집됐다**: ALAB 2026-06-30이
    $0.701B(6개월)로 잡혔으나 실제 분기는 $0.392B, COHR은 $5.07B(9개월)
    vs 실제 $1.81B, GEV $20.4B vs $11.1B, SMCI $27.9B vs $10.2B.
    QoQ 증감이 이 프레임의 핵심 판정인데 누적을 쓰면 분기마다 계단식으로
    부풀어 **항상 증가로 보이는 치명적 오판**이 된다."""
    s, e = fact.get("start"), fact.get("end")
    if not s or not e:
        return False
    try:
        days = (datetime.strptime(e, "%Y-%m-%d") - datetime.strptime(s, "%Y-%m-%d")).days
    except ValueError:
        return False
    return QUARTER_MIN_DAYS <= days <= QUARTER_MAX_DAYS


def _pick_fact(entries, metric):
    """같은 end_date에 잡힌 여러 fact 중 하나를 고르고, 고르지 않은 값도 note에
    남긴다(조용히 버리지 않는다 — investor_flow.py ADR crosscheck와 동일 원칙).

    지표별로 규칙이 다르다:
    - **backlog(RPO)**: 총액과 "12개월 내/이후" 분할이 함께 실리므로 **최대값**이
      총액이다.
    - **revenue**: 위 _is_quarterly로 이미 분기분만 남았으므로, 남은 복수 건은
      같은 분기를 여러 필링이 재보고한 것(정정 포함)이다. 이땐 **가장 이른
      filed**를 채택 — sec_edgar_capex.py와 같은 처리."""
    if metric == "backlog":
        entries.sort(key=lambda e: e["val"], reverse=True)
        label = "최대값(RPO 총액) 채택"
    else:
        entries.sort(key=lambda e: e["filed"])
        label = "최초 보고분 채택"
    chosen = entries[0]
    note = ""
    others = [e for e in entries[1:] if e["val"] != chosen["val"]]
    if others:
        detail = ", ".join(f"${e['val']:,}" for e in others[:4])
        note = f"⚠ 같은 end_date에 {len(entries)}건 — {label}. 나머지: {detail}"
    return chosen, note


def fetch_metric_for_company(ticker, cik, metric, raw=False, quarters=8):
    """한 회사의 한 지표(revenue|backlog)를 후보 태그 전부 조회해 수집.
    sec_edgar_capex.fetch_capex_for_company와 같은 원칙:
    - 첫 성공 태그에서 멈추지 않고 전 후보를 조회(회사가 태그를 바꿨을 가능성)
    - end_date를 분기 식별자로 사용(fy/fp는 재보고 시 달라짐)
    데이터를 못 찾으면 빈 리스트를 반환한다 — 이 스크립트는 8개사를 도는
    루프라, 한 회사·한 지표가 없다고 전체를 중단시키지 않는다(capex 쪽은
    4개사 전용이라 sys.exit이었지만 여기선 부분 실패를 허용)."""
    info = PERIPHERY[ticker]
    by_end = {}
    tag_hits = {}  # 어느 태그가 실제로 데이터를 줬는지 — 실패 진단용

    for tag in METRICS[metric]:
        data = fetch_company_concept(cik, tag, raw=raw)
        if data is None:
            continue
        units = data.get("units", {}).get("USD", [])
        if not units:
            continue
        kept = 0
        for u in units:
            if u.get("fp") not in ("Q1", "Q2", "Q3") or u.get("form") != "10-Q":
                continue
            missing = [f for f in ("val", "end", "fy", "fp", "form", "filed") if f not in u]
            if missing:
                print(f"  ⚠ {ticker}/{metric}/{tag}: 필드 누락 {missing} — 이 fact 건너뜀", file=sys.stderr)
                continue
            # 매출은 분기분만 — YTD 누적을 섞으면 QoQ가 무의미해진다(위 주석 참고).
            # 백로그(RPO)는 instant성이라 duration 필터를 적용하지 않는다.
            if metric == "revenue" and not _is_quarterly(u):
                continue
            kept += 1
            by_end.setdefault(u["end"], []).append({
                "val": u["val"], "filed": u["filed"], "fy": u["fy"], "fp": u["fp"],
                "form": u["form"], "tag": tag, "accn": u.get("accn", ""),
            })
        if kept:
            tag_hits[tag] = kept

    if tag_hits:
        print(f"  · {metric} 태그별 채택 fact: " +
              ", ".join(f"{t}={n}" for t, n in tag_hits.items()), file=sys.stderr)

    rows = []
    for end, entries in sorted(by_end.items(), reverse=True)[:quarters]:
        chosen, note = _pick_fact(entries, metric)
        rows.append({
            "company": info["name"], "ticker": ticker, "cik": cik, "layer": info["layer"],
            "metric": metric, "fiscal_year": chosen["fy"], "fiscal_period": chosen["fp"],
            "form": chosen["form"], "end_date": end, "filed_date": chosen["filed"],
            "value_usd": chosen["val"], "tag": chosen["tag"], "accn": chosen["accn"],
            "source": "sec_edgar_xbrl",
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "note": note,
        })
    return rows


def _read_csv():
    if not CSV_PATH.exists():
        return {}
    rows = {}
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[(row["ticker"], row["metric"], row["end_date"])] = row
    return rows


def _write_csv(rows_by_key):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows_by_key.values(), key=lambda r: (r["ticker"], r["metric"], r["end_date"]))
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS, restval="")
        w.writeheader()
        for r in ordered:
            w.writerow(r)


def upsert_rows(new_rows):
    existing = _read_csv()
    for r in new_rows:
        existing[(r["ticker"], r["metric"], r["end_date"])] = {k: r.get(k, "") for k in CSV_FIELDS}
    _write_csv(existing)
    return len(new_rows)


def read_periphery_rows():
    """다른 스크립트(daily_report.py)에서 재사용하는 리더."""
    return list(_read_csv().values())


def cmd_fetch(args):
    tickers = [args.company] if args.company else list(PERIPHERY.keys())
    ciks, missing = resolve_ciks(tickers)
    if missing:
        print(f"⚠ SEC 티커맵에서 못 찾은 티커: {missing} — 상장폐지·티커변경 가능성, 수동 확인 필요", file=sys.stderr)

    total, failed = 0, []
    for ticker in tickers:
        cik = ciks.get(ticker)
        if cik is None:
            failed.append(ticker)
            continue
        print(f"[{ticker}] CIK {cik} 조회 중...", file=sys.stderr)
        got_any = False
        for metric in METRICS:
            try:
                rows = fetch_metric_for_company(ticker, cik, metric, raw=args.raw)
            except SystemExit as e:
                print(f"  ⚠ {ticker}/{metric} 실패: {e}", file=sys.stderr)
                continue
            if args.raw:
                continue
            if not rows:
                print(f"  - {metric}: 데이터 없음(이 회사는 해당 태그 미사용)", file=sys.stderr)
                continue
            got_any = True
            total += upsert_rows(rows)
            print(f"  - {metric}: {len(rows)}개 분기 (최신 {rows[0]['end_date']} = ${rows[0]['value_usd']:,})", file=sys.stderr)
        if not got_any and not args.raw:
            failed.append(ticker)

    if not args.raw:
        print(f"\n총 {total}건 저장 → {CSV_PATH}", file=sys.stderr)
    if failed:
        print(
            f"⚠ 수집 실패: {failed} — --raw --company <티커>로 원본을 확인하고 "
            "REVENUE_TAG_CANDIDATES/BACKLOG_TAG_CANDIDATES에 실제 태그를 추가하세요. "
            "지어낸 값을 채우지 않기 위해 빈 채로 둡니다.",
            file=sys.stderr,
        )


def cmd_show(args):
    rows = read_periphery_rows()
    if not rows:
        print("기록 없음 — 먼저 `fetch`를 실행하세요.")
        return
    by_key = {}
    for r in rows:
        by_key.setdefault((r["ticker"], r["metric"]), []).append(r)

    for ticker, info in PERIPHERY.items():
        printed_header = False
        for metric in METRICS:
            series = sorted(by_key.get((ticker, metric), []), key=lambda r: r["end_date"])
            if not series:
                continue
            if not printed_header:
                print(f"\n## {info['name']} ({ticker}) — {info['layer']}")
                printed_header = True
            latest = series[-1]
            line = f"  {metric:8s} {latest['end_date']}: ${float(latest['value_usd']):,.0f}"
            if len(series) >= 2:
                prev = float(series[-2]["value_usd"])
                if prev:
                    line += f"  (직전분기 대비 {(float(latest['value_usd']) - prev) / prev * 100:+.1f}%)"
            if latest.get("note"):
                line += f"  [{latest['note']}]"
            print(line)
        if not printed_header:
            print(f"\n## {info['name']} ({ticker}) — 기록 없음")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    fetch_p = sub.add_parser("fetch", help="변두리 8개사 매출·백로그 수집 후 CSV 저장")
    fetch_p.add_argument("--company", choices=list(PERIPHERY.keys()), help="특정 회사만(생략시 전체)")
    fetch_p.add_argument("--raw", action="store_true", help="원본 JSON 출력(태그 검증용, CSV 저장 안 함)")
    fetch_p.set_defaults(func=cmd_fetch)

    show_p = sub.add_parser("show", help="저장된 데이터 요약")
    show_p.set_defaults(func=cmd_show)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
