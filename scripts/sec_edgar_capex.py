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
공정접근 정책(https://www.sec.gov/os/webmaster-faq#developers)상 **모든 요청에
식별 가능한 User-Agent(회사/개인명 + 연락처)를 반드시 포함**해야 한다 — 없으면
403이 돌아온다(이 저장소 collectors/fred.py의 범용 UA 관례와 달리, 여기서는
SEC 요구사항에 맞춘 전용 UA를 쓴다).

⚠ 이 샌드박스는 아웃바운드 네트워크가 SEC 도메인에 막혀 있어(2026-08-05 확인:
직접 curl → 프록시 자체 차단, WebFetch 도구 → 403 — 둘 다 이 코드 작성 전
직접 검증 시도했으나 실패) **실호출 검증을 못 한 상태로 작성됐다**. CIK
번호(구글 1652044/MS 789019/아마존 1018724/메타 1326801)와 응답 JSON 구조
(units.USD 배열의 val/end/fy/fp/form/filed/accn 필드)는 SEC 공식문서·다수
튜토리얼 교차검증으로 확인했지만, XBRL 태그명(PaymentsToAcquire...) 자체가
회사마다 다를 수 있어 **최초 실행 시 반드시 --raw로 원본을 확인**하고,
아래 CAPEX_TAG_CANDIDATES에 없는 태그를 쓰는 회사가 있으면 그 회사만 실패
목록에 남기고 나머지는 계속 진행한다(투자자_flow.py와 동일 원칙 — 지어낸
값을 채우지 않고 실패는 눈에 띄게 남긴다).

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
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "hyperscaler-capex.csv"
CSV_FIELDS = [
    "company", "ticker", "cik", "fiscal_year", "fiscal_period", "form",
    "end_date", "filed_date", "value_usd", "tag", "accn", "source", "fetched_at",
]

# SEC 공정접근 정책 요구사항 — 식별 가능한 UA(https://www.sec.gov/os/webmaster-faq#developers).
# 저장소를 연락 채널로 명시(collectors/fred.py의 "+https://github.com" 관례와 동일 정신).
HEADERS = {"User-Agent": "PEOS-wiki-research/1.0 (+https://github.com/stevekoo-ai/Repo_name)"}

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
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # 이 회사가 이 태그를 안 쓴다 — 다음 후보 태그로 넘어감
        sys.exit(f"SEC EDGAR API 호출 실패({tag}): {e.code} {e.read().decode(errors='replace')}")
    except urllib.error.URLError as e:
        sys.exit(f"SEC EDGAR 접속 실패: {e.reason} — data.sec.gov 접근 가능 여부(방화벽/프록시)를 확인하세요.")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:5000])
    return data


def fetch_capex_for_company(ticker, raw=False, quarters=8):
    """4개 후보 태그를 순서대로 시도해 첫 성공한 태그로 최근 N개 분기(10-Q 기준,
    fp가 Q1/Q2/Q3인 것만 — FY는 연간 누적치라 분기 비교에 안 섞는다) 데이터를 반환."""
    info = HYPERSCALERS[ticker]
    cik = info["cik"]

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
        # 섞으면 왜곡되므로 제외. 최신순 정렬 후 quarters개만.
        quarterly = [u for u in units if u.get("fp") in ("Q1", "Q2", "Q3") and u.get("form") == "10-Q"]
        quarterly.sort(key=lambda u: u["end"], reverse=True)
        rows = []
        for u in quarterly[:quarters]:
            rows.append({
                "company": info["name"], "ticker": ticker, "cik": cik,
                "fiscal_year": u["fy"], "fiscal_period": u["fp"], "form": u["form"],
                "end_date": u["end"], "filed_date": u["filed"], "value_usd": u["val"],
                "tag": tag, "accn": u.get("accn", ""),
                "source": "sec_edgar_xbrl", "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            })
        return rows

    sys.exit(
        f"{ticker}: 후보 태그 {CAPEX_TAG_CANDIDATES} 중 어느 것도 응답에서 데이터를 "
        f"찾지 못했습니다 — --raw --company {ticker}로 개별 태그 원본을 확인하고 "
        "CAPEX_TAG_CANDIDATES에 실제 태그를 추가하세요. 지어낸 값을 채우지 않기 위해 여기서 중단합니다."
    )


def _read_csv():
    if not CSV_PATH.exists():
        return {}
    rows = {}
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[(row["ticker"], row["fiscal_year"], row["fiscal_period"])] = row
    return rows


def _write_csv(rows_by_key):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows_by_key.values(), key=lambda r: (r["ticker"], r["fiscal_year"], r["fiscal_period"]))
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in ordered:
            w.writerow(r)


def upsert_rows(new_rows):
    existing = _read_csv()
    for r in new_rows:
        existing[(r["ticker"], r["fiscal_year"], r["fiscal_period"])] = {k: r.get(k, "") for k in CSV_FIELDS}
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
