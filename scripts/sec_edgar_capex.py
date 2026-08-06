#!/usr/bin/env python3
"""
하이퍼스케일러(구글/MS/아마존/메타) 분기 CapEx(설비투자) 실측치 — SEC EDGAR
XBRL Company Concept API로 자동 수집.

wiki/concepts/automation-vs-ai-narrative-roadmap.md "2단계"에서 조사한 대로,
매일 데일리 체크가 "🇺🇸 하이퍼스케일러 고객 동향"을 전적으로 웹검색+뉴스해석
(재고 센티먼트 점수 0~10 등)으로만 채우던 것 중, 최소한 **"CapEx가 실제로
얼마였나"라는 실측 숫자**는 SEC 정기공시(10-Q/10-K)에서 매 분기 공식 발표되는
값이라 API로 완전 대체 가능하다 — 이 스크립트가 그 부분을 담당한다.
(어닝콜 논조의 "재고 센티먼트 점수"는 여전히 뉴스 해석이 본질이라 이 스크립트
범위 밖 — 자동화 불가 항목으로 로드맵 문서에 명시돼 있다.)

data.sec.gov는 인증(API 키) 없이 완전 무료로 XBRL 데이터를 제공하지만, SEC의
공정접근 정책(https://www.sec.gov/os/webmaster-faq#developers)상 **모든 요청의
User-Agent에 실제 이메일 주소가 포함된 "이름/조직 email@domain.com" 형식**을
요구한다 — 단순히 식별 가능한 문자열이면 되는 게 아니라, 이메일 패턴이 없으면
"Undeclared Automated Tool"로 간주해 403을 반환한다(2026-08-06 GitHub Actions
실제 실행 로그로 확인 — 아래 "실행 이력" 참고). 이 값은 환경변수
`SEC_EDGAR_CONTACT`에서 읽는다 — GitHub Actions에서는 별도 시크릿을 새로
만들지 않고 이미 등록된 **`GMAIL_ADDRESS` 시크릿을 재사용**해
`.github/workflows/sec-edgar-capex.yml`이 조합해 넘긴다(2026-08-06 사용자
제안, 시크릿 중복 생성 방지). 로컬 실행 시에는 `SEC_EDGAR_CONTACT` 환경변수를
직접 export하면 된다. 값이 없거나 이메일 형식이 아니면 즉시 에러로 중단
(investor_flow.py의 `_get_env_or_die` 패턴과 동일 — 값을 지어내거나 조용히
실패하지 않는다).

⚠ 실행 이력: 2026-08-06 GitHub Actions에서 raw:true 최초 실행(2회) → 4개사
전부 403("Undeclared Automated Tool")로 실패, 원인은 XBRL 태그명이 아니라
**User-Agent에 이메일 형식이 없었던 것**으로 확인(PR #48). 이후 신규 시크릿
대신 GMAIL_ADDRESS 재사용으로 전환(PR #49) → **같은 날 raw:true 재실행
성공** — CIK 4개·CAPEX_TAG_CANDIDATES 첫 후보(PaymentsToAcquirePropertyPlant
AndEquipment)가 4개사 전부에서 그대로 매칭 확인(예: Meta CIK 1326801,
entityName "Meta Platforms, Inc." 응답 확인). 곧이어 정식 모드(raw 아님)
실행도 성공해 `sources/hyperscaler-capex.csv`에 실측 데이터 커밋 완료.
CAPEX_TAG_CANDIDATES의 2·3번째 대체 태그는 실전에서 쓰인 적 없음(1번째로
4개사 전부 해결) — 향후 회사가 추가되거나 태그를 바꾸면 그때 검증할 것.

⚠ 2026-08-06 데이터 정합성 버그 발견·수정(daily_report.py에 실제 연결하려던
중 발견): (1) SEC companyconcept API가 같은 분기(end_date)를 나중 필링의
"전년동기 비교치"로 재수록할 때 다른 fiscal_year/fiscal_period를 붙이는
경우가 있어, 예전 코드(upsert 키 = ticker+fy+fp)는 이를 별개 분기처럼
중복 저장했었다(GOOGL/META/MSFT 3사 확인) — 키를 **(ticker, end_date)**로
바꿨다. (2) MSFT 한 분기(2025-03-31)에서 진짜 값 충돌 발견($16.7B vs
$47.5B) — 위 "실행 이력"에서 인용했던 "MSFT FY2026Q3 $47.5B"는 실은 이
충돌 중 한쪽이었다(정정: 어느 쪽이 맞는지 이 커밋 시점엔 미확인, 아래
`note` 컬럼에 두 값 모두 남겨둠 — investor_flow.py ADR crosscheck MISMATCH와
동일 원칙, 조용히 하나를 버리지 않는다). (3) 첫 성공 태그에서 멈추던
로직을 후보 태그 전부 조회하도록 변경 — AMZN이 2017년 분기에서 멈춰있던
원인(최근엔 다른 태그를 쓸 가능성)에 대응. 다음 실제 실행(`fetch`, 이
PR 병합 후)에서 새 로직이 실제로 더 최신 데이터를 찾아내는지, MSFT 충돌
값 중 어느 쪽이 맞는지 확인 필요 — 상세는 wiki
concepts/automation-vs-ai-narrative-roadmap.md "SEC EDGAR 데이터 정합성
버그" 참고.

사용법:
  # 4개 회사 최근 8개 분기 CapEx를 가져와 CSV에 upsert
  python3 scripts/sec_edgar_capex.py fetch

  # 원본 API 응답 구조 확인용(최초 1회 필드명 검증 목적)
  python3 scripts/sec_edgar_capex.py fetch --company GOOGL --raw

  # 저장된 데이터 요약(최근 4개 분기, 전분기 대비 증감률)
  python3 scripts/sec_edgar_capex.py show
"""
import argparse
import csv
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "hyperscaler-capex.csv"
CSV_FIELDS = [
    "company", "ticker", "cik", "fiscal_year", "fiscal_period", "form",
    "end_date", "filed_date", "value_usd", "tag", "accn", "source", "fetched_at", "note",
]


def _get_headers():
    """SEC 공정접근 정책(https://www.sec.gov/os/webmaster-faq#developers)이 요구하는
    "이름/조직 email@domain.com" 형식 User-Agent — GitHub Secret에서 읽는다(개인
    이메일을 공개 저장소 코드에 평문 커밋하지 않기 위함, investor_flow.py의
    _get_env_or_die 패턴과 동일). 2026-08-06 실호출 확인: 이메일 형식이 없으면
    "Undeclared Automated Tool" 403."""
    contact = os.environ.get("SEC_EDGAR_CONTACT")
    if not contact:
        sys.exit(
            "환경변수 SEC_EDGAR_CONTACT이(가) 설정되지 않았습니다. SEC EDGAR는 "
            "User-Agent에 실제 이메일이 포함된 형식(예: \"PEOS-research "
            "your-email@example.com\")을 요구합니다(없으면 403) — GitHub Secrets에 "
            "SEC_EDGAR_CONTACT를 등록하고 .github/workflows/sec-edgar-capex.yml의 "
            "env로 주입하세요. 이 값을 저장소 파일에 절대 커밋하지 마세요."
        )
    if "@" not in contact:
        sys.exit(
            f"SEC_EDGAR_CONTACT 값에 '@'(이메일)이 없습니다: {contact!r} — SEC가 "
            "이메일 형식 없는 User-Agent를 자동화 도구로 판정해 403을 반환합니다. "
            "\"이름/조직 email@domain.com\" 형식으로 다시 설정하세요."
        )
    return {"User-Agent": contact}

# 2026-08-05 웹검색으로 교차검증된 CIK — Alphabet/Meta는 실제 SEC 문서 URL
# (sec.gov/Archives/edgar/data/1652044/..., CIK-0001326801)에서 직접 확인,
# Microsoft/Amazon은 다수 EDGAR 파일링 URL(edgar/data/789019/..., .../1018724/...)
# 에서 확인 — 4개 전부 이 저장소 코드 작성 시점 기준 재검증 완료.
HYPERSCALERS = {
    "GOOGL": {"name": "Alphabet (Google)", "cik": "1652044"},
    "MSFT": {"name": "Microsoft", "cik": "789019"},
    "AMZN": {"name": "Amazon", "cik": "1018724"},
    "META": {"name": "Meta Platforms", "cik": "1326801"},
}

# us-gaap 표준 태그 중 "설비투자"에 해당하는 현금흐름표 항목 — 회사마다 실제
# 쓰는 태그가 다를 수 있어 후보를 순서대로 시도한다(첫 성공 태그를 채택).
# PaymentsToAcquirePropertyPlantAndEquipment가 가장 흔한 표준 태그.
CAPEX_TAG_CANDIDATES = [
    "PaymentsToAcquirePropertyPlantAndEquipment",
    "PaymentsToAcquireProductiveAssets",
    "PaymentsForCapitalImprovements",
]


def fetch_company_concept(cik, tag, raw=False):
    """단일 (CIK, 태그) 조합의 companyconcept 응답을 가져온다. 실패하면 None."""
    cik_padded = cik.zfill(10)
    url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_padded}/us-gaap/{tag}.json"
    req = urllib.request.Request(url, headers=_get_headers())
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # 이 회사가 이 태그를 안 쓴다 — 다음 후보 태그로 넘어감
        body = e.read().decode(errors="replace")
        hint = (
            "\n힌트: 403 + \"Undeclared Automated Tool\"이면 태그 문제가 아니라 "
            "SEC_EDGAR_CONTACT의 User-Agent에 이메일 형식이 없는 경우입니다(2026-08-06 "
            "실사례) — \"이름 email@domain.com\" 형식인지 확인하세요."
            if e.code == 403 and "Undeclared Automated Tool" in body else ""
        )
        sys.exit(f"SEC EDGAR API 호출 실패({tag}): {e.code} {body}{hint}")
    except urllib.error.URLError as e:
        sys.exit(f"SEC EDGAR 접속 실패: {e.reason} — data.sec.gov 접근 가능 여부(방화벽/프록시)를 확인하세요.")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:5000])
    return data


def fetch_capex_for_company(ticker, raw=False, quarters=8):
    """후보 태그를 **전부** 시도해 결과를 end_date 기준으로 합친다.

    2026-08-06 버그 수정 — 원래는 "첫 성공한 태그"에서 멈췄는데, 이 방식으로
    받은 실제 CSV를 검사해보니 AMZN이 2016~2017년 데이터에서 멈춰 있었다
    (그 회사가 최근 분기엔 다른 태그를 쓰는데 이전 태그에도 오래된 값이
    남아있어 "성공"으로 오판, 다음 후보 태그를 시도하지 않은 것으로 추정) —
    회사가 태그를 바꿨을 가능성을 놓치지 않도록 전 후보를 다 조회해 합친다.

    또한 SEC companyconcept API는 같은 (end_date) 분기를 **서로 다른
    fiscal_year/fiscal_period 라벨로 중복 보고**하는 경우가 있다(그 분기가
    나중 분기 보고서의 "전년동기 비교치"로 다시 실릴 때, fy/fp가 원래 분기가
    아니라 그 나중 보고서 기준으로 붙는 경우가 있음 — 2026-08-06 실제 CSV에서
    GOOGL/META/MSFT 전부 이 패턴 발견). 그래서 fy/fp가 아니라 **end_date를
    분기 식별자로 삼아** 중복을 제거한다: 같은 end_date에 값도 같으면 가장
    먼저 제출된(filed 가장 이른) 쪽을 채택, **값이 다르면(진짜 데이터 충돌)
    지어내거나 조용히 하나를 버리지 않고 note 필드에 남긴다**(먼저 제출된
    쪽을 잠정 채택하되 다른 값도 기록 — investor_flow.py의 ADR crosscheck
    MISMATCH와 동일한 원칙)."""
    info = HYPERSCALERS[ticker]
    cik = info["cik"]

    combined = []  # (end_date, filed, val, fy, fp, form, tag, accn)
    for tag in CAPEX_TAG_CANDIDATES:
        data = fetch_company_concept(cik, tag, raw=raw)
        if data is None:
            continue
        units = data.get("units", {}).get("USD", [])
        if not units:
            continue

        missing = [f for f in ("val", "end", "fy", "fp", "form", "filed") if f not in units[0]]
        if missing:
            sys.exit(
                f"{ticker}({tag}) 응답에 예상 필드가 없습니다: {missing}. 실제 키: "
                f"{sorted(units[0].keys())}\n--raw로 원본을 확인하고 이 스크립트를 고치세요."
            )

        # 10-Q 분기 보고분만(fp in Q1/Q2/Q3) — FY(연간 누적)는 분기 트렌드 비교에
        # 섞으면 왜곡되므로 제외.
        for u in units:
            if u.get("fp") in ("Q1", "Q2", "Q3") and u.get("form") == "10-Q":
                combined.append((u["end"], u["filed"], u["val"], u["fy"], u["fp"], u["form"], tag, u.get("accn", "")))

    if not combined:
        sys.exit(
            f"{ticker}: 후보 태그 {CAPEX_TAG_CANDIDATES} 중 어느 것도 응답에서 데이터를 "
            f"찾지 못했습니다 — --raw --company {ticker}로 개별 태그 원본을 확인하고 "
            "CAPEX_TAG_CANDIDATES에 실제 태그를 추가하세요. 지어낸 값을 채우지 않기 위해 여기서 중단합니다."
        )

    # end_date별로 묶어 filed가 가장 이른 것을 canonical로 채택, 값 충돌은 note에 기록
    by_end = {}
    for end, filed, val, fy, fp, form, tag, accn in combined:
        by_end.setdefault(end, []).append((filed, val, fy, fp, form, tag, accn))

    rows = []
    for end, entries in sorted(by_end.items(), reverse=True)[:quarters]:
        entries.sort(key=lambda e: e[0])  # filed 오름차순 — 가장 이른 제출을 canonical로
        filed, val, fy, fp, form, tag, accn = entries[0]
        note = ""
        distinct_vals = {e[1] for e in entries}
        if len(distinct_vals) > 1:
            others = ", ".join(f"${v:,}(filed {e[0]})" for e in entries[1:] for v in [e[1]])
            note = f"⚠ CONFLICT: 같은 end_date에 다른 값 발견, 가장 이른 filed 채택. 다른 값: {others}"
        rows.append({
            "company": info["name"], "ticker": ticker, "cik": cik,
            "fiscal_year": fy, "fiscal_period": fp, "form": form,
            "end_date": end, "filed_date": filed, "value_usd": val,
            "tag": tag, "accn": accn,
            "source": "sec_edgar_xbrl", "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "note": note,
        })
    return rows


def _read_csv():
    if not CSV_PATH.exists():
        return {}
    rows = {}
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # 2026-08-06: 키를 (ticker, fiscal_year, fiscal_period)에서
            # (ticker, end_date)로 변경 — fy/fp는 같은 분기라도 어느 필링에서
            # 재보고됐는지에 따라 달라질 수 있어(위 fetch_capex_for_company
            # 주석 참고) 진짜 분기 식별자가 못 됨. 이 필드로 옛 CSV(구 키
            # 체계로 저장된 행)를 읽어도 자동으로 end_date 기준 재정렬된다.
            rows[(row["ticker"], row["end_date"])] = row
    return rows


def _write_csv(rows_by_key):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows_by_key.values(), key=lambda r: (r["ticker"], r["end_date"]))
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS, restval="")
        w.writeheader()
        for r in ordered:
            w.writerow(r)


def upsert_rows(new_rows):
    existing = _read_csv()
    for r in new_rows:
        existing[(r["ticker"], r["end_date"])] = {k: r.get(k, "") for k in CSV_FIELDS}
    _write_csv(existing)
    return len(new_rows)


def cmd_fetch(args):
    tickers = [args.company] if args.company else list(HYPERSCALERS.keys())
    total = 0
    failed = []
    for ticker in tickers:
        print(f"[{ticker}] SEC EDGAR 조회 중...", file=sys.stderr)
        try:
            rows = fetch_capex_for_company(ticker, raw=args.raw)
        except SystemExit as e:
            print(f"⚠ {ticker} 실패: {e}", file=sys.stderr)
            failed.append(ticker)
            continue
        if args.raw:
            continue
        n = upsert_rows(rows)
        total += n
        print(f"  {n}개 분기 upsert 완료 (최신: {rows[0]['fiscal_year']}{rows[0]['fiscal_period']} = ${rows[0]['value_usd']:,})", file=sys.stderr)

    if not args.raw:
        print(f"\n총 {total}건 저장 → {CSV_PATH}", file=sys.stderr)
    if failed:
        print(f"⚠ 실패한 회사: {failed} — 위 에러 메시지 참고, CAPEX_TAG_CANDIDATES 보정 필요할 수 있음", file=sys.stderr)
        sys.exit(1)


def cmd_show(args):
    rows = list(_read_csv().values())
    if not rows:
        print("기록 없음 — 먼저 `fetch`를 실행하세요.")
        return
    by_ticker = {}
    for r in rows:
        by_ticker.setdefault(r["ticker"], []).append(r)

    for ticker, info in HYPERSCALERS.items():
        company_rows = sorted(by_ticker.get(ticker, []), key=lambda r: r["end_date"])
        if not company_rows:
            print(f"\n## {info['name']} ({ticker}) — 기록 없음")
            continue
        print(f"\n## {info['name']} ({ticker})")
        for i, r in enumerate(company_rows[-4:]):
            val = float(r["value_usd"])
            line = f"  {r['fiscal_year']}{r['fiscal_period']} ({r['end_date']}): ${val:,.0f}"
            idx_in_full = company_rows.index(r)
            if idx_in_full > 0:
                prev_val = float(company_rows[idx_in_full - 1]["value_usd"])
                if prev_val:
                    qoq = (val - prev_val) / prev_val * 100
                    line += f"  (전분기 대비 {qoq:+.1f}%)"
            print(line)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    fetch_p = sub.add_parser("fetch", help="SEC EDGAR에서 4개 하이퍼스케일러 CapEx 조회 후 CSV 저장")
    fetch_p.add_argument("--company", choices=list(HYPERSCALERS.keys()), help="특정 회사만 조회(생략시 4개 전부)")
    fetch_p.add_argument("--raw", action="store_true", help="원본 JSON 응답만 출력(필드명 검증용, CSV 저장 안 함)")
    fetch_p.set_defaults(func=cmd_fetch)

    show_p = sub.add_parser("show", help="저장된 CapEx 데이터 요약(최근 4개 분기 + 전분기 대비 증감률)")
    show_p.set_defaults(func=cmd_show)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
