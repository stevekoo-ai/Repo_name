#!/usr/bin/env python3
"""
SK하이닉스(및 기타 종목) 투자자별(외국인/기관/개인) 일별 순매수 수급 트래커.

market-cycles-leverage-risk.md "1-4-1"에서 반복적으로 "미확인"으로 남아있던
구멍 — 종목 특정 외국인/기관/개인 1·5·20·60일 누적 순매수 — 을 웹검색 대신
증권사 Open API로 직접 채우기 위한 스크립트. regime_engine.py와 같은 철학:
숫자를 지어내지 않고, 데이터가 없으면 "미확인"으로 남긴다. 데이터 주입
경로는 두 가지를 모두 지원한다 — (a) 증권사 API 실시간 조회, (b) 웹검색 등
다른 경로로 확보한 값을 --append로 수동 기록. 저장 형식(append-only CSV)만
지키면 이 스크립트 입장에서는 값이 어디서 왔는지 상관없다.

기본 프로바이더는 한국투자증권(KIS) Developers Open API — 개인 무료 발급이
가장 흔한 선택지라 기본값으로 삼았다. 다른 증권사 API를 쓰게 되면
kis_fetch_investor_trend() 자리에 해당 프로바이더의 fetch 함수만 바꿔 끼우면
된다(현재는 프로바이더 1개뿐이라 추상 레이어를 만들지 않았다).

⚠ KIS API 응답 필드명은 이 스크립트 작성 시점에 문서 기억에 기반해 넣었다 —
실제 계정으로 최초 호출할 때 --raw로 원본 JSON을 찍어보고 필드명이 다르면
FIELDS 딕셔너리만 고치면 된다. 지어낸 숫자를 반환하지 않기 위해, 예상한
필드가 응답에 없으면 조용히 넘어가지 않고 즉시 에러를 낸다.

환경변수(필수, .env나 셸 프로파일에 설정 — 절대 이 저장소에 커밋하지 않음):
  KIS_APP_KEY, KIS_APP_SECRET   — KIS Developers 포털에서 발급
  KIS_ACCOUNT_TYPE (선택)       — "real"(기본) 또는 "vts"(모의투자)

사용법:
  # 1) 증권사 API로 최근 N일 실측치를 가져와 CSV에 append(중복 날짜는 덮어씀)
  python3 scripts/investor_flow.py fetch --ticker 000660 --days 30

  # 2) API 미가입 상태 등에서 웹검색으로 확보한 값을 수동 기록
  python3 scripts/investor_flow.py append --date 2026-07-24 --ticker 000660 \
      --foreign-krw -1756800000000 --inst-krw -86730000000 \
      --source websearch --note "파이낸셜뉴스 7/24 기사"

  # 3) 최근 기록 + 1/5/20/60일 누적 순매수 요약 (위키 1-4-1에 바로 쓸 수 있는 형태)
  python3 scripts/investor_flow.py show --ticker 000660

  # 원본 API 응답 구조 확인용(최초 1회 필드명 검증 목적)
  python3 scripts/investor_flow.py fetch --ticker 000660 --days 5 --raw
"""
import os
import sys
import csv
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timedelta

CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "sk-hynix-investor-flow.csv"
TOKEN_CACHE = Path(__file__).resolve().parent / ".kis_token_cache.json"

KIS_HOSTS = {
    "real": "https://openapi.koreainvestment.com:9443",
    "vts": "https://openapivts.koreainvestment.com:29443",
}

CSV_FIELDS = [
    "date", "ticker", "foreign_net_qty", "inst_net_qty", "retail_net_qty",
    "foreign_net_krw", "inst_net_krw", "retail_net_krw", "source", "note",
]

# KIS "국내주식 종목별 투자자매매동향(일별)" TR: FHKST01010900
# GET /uapi/domestic-stock/v1/quotations/inquire-investor
# ⚠ 필드명은 문서 기억 기반 — 최초 실호출 시 --raw로 검증할 것
FIELDS = {
    "date": "stck_bsop_date",
    "foreign_net_qty": "frgn_ntby_qty",
    "inst_net_qty": "orgn_ntby_qty",
    "retail_net_qty": "prsn_ntby_qty",
    "foreign_net_krw": "frgn_ntby_tr_pbmn",
    "inst_net_krw": "orgn_ntby_tr_pbmn",
    "retail_net_krw": "prsn_ntby_tr_pbmn",
}


def _get_env_or_die(name):
    v = os.environ.get(name)
    if not v:
        sys.exit(
            f"환경변수 {name}이(가) 설정되지 않았습니다. KIS Developers 포털"
            f"(https://apiportal.koreainvestment.com)에서 발급받은 값을"
            f" 셸 프로파일(.bashrc/.zshrc 등)에 export 해두세요. 이 값을"
            f" 저장소 파일에 절대 커밋하지 마세요."
        )
    return v


def kis_get_token(account_type="real"):
    """KIS OAuth2 접근토큰 발급. 24시간 유효 — 로컬에 캐시해 재발급 최소화."""
    if TOKEN_CACHE.exists():
        cached = json.loads(TOKEN_CACHE.read_text())
        if cached.get("account_type") == account_type and \
                datetime.fromisoformat(cached["expires_at"]) > datetime.now():
            return cached["access_token"]

    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    host = KIS_HOSTS[account_type]

    body = json.dumps({
        "grant_type": "client_credentials",
        "appkey": appkey,
        "appsecret": appsecret,
    }).encode()
    req = urllib.request.Request(
        f"{host}/oauth2/tokenP", data=body, method="POST",
        headers={"content-type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    token = data["access_token"]
    expires_at = datetime.now() + timedelta(seconds=int(data.get("expires_in", 86400)) - 300)
    TOKEN_CACHE.write_text(json.dumps({
        "account_type": account_type,
        "access_token": token,
        "expires_at": expires_at.isoformat(),
    }))
    return token


def kis_fetch_investor_trend(ticker, account_type="real", raw=False):
    """일별 투자자매매동향(최근 30영업일, KIS 기준) 원자료를 가져온다."""
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    token = kis_get_token(account_type)
    host = KIS_HOSTS[account_type]

    params = f"FID_COND_MRKT_DIV_CODE=J&FID_INPUT_ISCD={ticker}"
    req = urllib.request.Request(
        f"{host}/uapi/domestic-stock/v1/quotations/inquire-investor?{params}",
        headers={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": appkey,
            "appsecret": appsecret,
            "tr_id": "FHKST01010900",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"KIS API 호출 실패: {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return []

    rows = data.get("output") or data.get("output2") or []
    if not rows:
        sys.exit(
            "API 응답에서 데이터 행을 찾지 못했습니다 — --raw로 원본 JSON을 "
            "확인하고 이 스크립트의 rows 추출 키(output/output2)를 응답 구조에 "
            "맞게 고치세요. 지어낸 값을 채우지 않기 위해 여기서 중단합니다."
        )

    missing = [v for v in FIELDS.values() if v not in rows[0]]
    if missing:
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다: {missing}. --raw로 원본을 "
            "확인해 이 스크립트 상단 FIELDS 딕셔너리를 실제 필드명으로 고치세요."
        )

    parsed = []
    for r in rows:
        d = r[FIELDS["date"]]
        parsed.append({
            "date": f"{d[0:4]}-{d[4:6]}-{d[6:8]}",
            "ticker": ticker,
            "foreign_net_qty": r[FIELDS["foreign_net_qty"]],
            "inst_net_qty": r[FIELDS["inst_net_qty"]],
            "retail_net_qty": r[FIELDS["retail_net_qty"]],
            "foreign_net_krw": r[FIELDS["foreign_net_krw"]],
            "inst_net_krw": r[FIELDS["inst_net_krw"]],
            "retail_net_krw": r[FIELDS["retail_net_krw"]],
            "source": "kis_api",
            "note": "",
        })
    return parsed


def _read_csv():
    if not CSV_PATH.exists():
        return {}
    rows = {}
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[(row["date"], row["ticker"])] = row
    return rows


def _write_csv(rows_by_key):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows_by_key.values(), key=lambda r: (r["date"], r["ticker"]))
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in ordered:
            w.writerow(r)


def upsert_rows(new_rows):
    existing = _read_csv()
    for r in new_rows:
        existing[(r["date"], r["ticker"])] = {k: r.get(k, "") for k in CSV_FIELDS}
    _write_csv(existing)
    return len(new_rows)


def cmd_fetch(args):
    if args.days > 30:
        print("참고: KIS 이 TR은 최근 30영업일까지만 반환합니다 — days>30은 의미 없음.", file=sys.stderr)
    rows = kis_fetch_investor_trend(args.ticker, args.account_type, raw=args.raw)
    if args.raw:
        return
    n = upsert_rows(rows)
    print(f"{n}개 행을 {CSV_PATH}에 기록(중복 날짜는 갱신)했습니다.")


def cmd_append(args):
    row = {
        "date": args.date, "ticker": args.ticker,
        "foreign_net_qty": args.foreign_qty or "",
        "inst_net_qty": args.inst_qty or "",
        "retail_net_qty": args.retail_qty or "",
        "foreign_net_krw": args.foreign_krw or "",
        "inst_net_krw": args.inst_krw or "",
        "retail_net_krw": args.retail_krw or "",
        "source": args.source,
        "note": args.note or "",
    }
    upsert_rows([row])
    print(f"{args.date} {args.ticker} 수동 기록 완료 → {CSV_PATH}")


def cmd_show(args):
    existing = [r for (d, t), r in _read_csv().items() if t == args.ticker]
    existing.sort(key=lambda r: r["date"])
    if not existing:
        print(f"{args.ticker} 기록 없음 — fetch나 append로 먼저 데이터를 채우세요.")
        return

    tail = existing[-args.last:]
    print(f"=== {args.ticker} 최근 {len(tail)}일 ===")
    for r in tail:
        print(f"{r['date']}  외인 {r['foreign_net_krw']:>15}원 ({r['foreign_net_qty']:>10}주)  "
              f"기관 {r['inst_net_krw']:>15}원  개인 {r['retail_net_krw']:>15}원  [{r['source']}]")

    print("\n=== 누적 순매수(원) ===")
    for window in (1, 5, 20, 60):
        chunk = existing[-window:]
        if len(chunk) < window:
            print(f"{window}일 누적: 미확인 — {window}영업일 중 {len(chunk)}일치만 확보")
            continue
        for label, key in (("외국인", "foreign_net_krw"), ("기관", "inst_net_krw"), ("개인", "retail_net_krw")):
            vals = [int(r[key]) for r in chunk if r[key] not in ("", None)]
            if len(vals) < len(chunk):
                print(f"{window}일 {label}: 미확인(기록 {len(vals)}/{len(chunk)}일치만 확보)")
            else:
                print(f"{window}일 {label}: {sum(vals):+,}원")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pf = sub.add_parser("fetch", help="증권사 API로 최근 N일 실측치를 가져와 CSV에 기록")
    pf.add_argument("--ticker", default="000660")
    pf.add_argument("--days", type=int, default=30)
    pf.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    pf.add_argument("--raw", action="store_true", help="파싱하지 않고 원본 JSON만 출력(필드명 검증용)")
    pf.set_defaults(func=cmd_fetch)

    pa = sub.add_parser("append", help="웹검색 등 다른 경로로 확보한 값을 수동 기록")
    pa.add_argument("--date", required=True, help="YYYY-MM-DD")
    pa.add_argument("--ticker", default="000660")
    pa.add_argument("--foreign-qty", type=int)
    pa.add_argument("--inst-qty", type=int)
    pa.add_argument("--retail-qty", type=int)
    pa.add_argument("--foreign-krw", type=int)
    pa.add_argument("--inst-krw", type=int)
    pa.add_argument("--retail-krw", type=int)
    pa.add_argument("--source", default="websearch")
    pa.add_argument("--note", default="")
    pa.set_defaults(func=cmd_append)

    ps = sub.add_parser("show", help="최근 기록 + 1/5/20/60일 누적 순매수 요약")
    ps.add_argument("--ticker", default="000660")
    ps.add_argument("--last", type=int, default=10)
    ps.set_defaults(func=cmd_show)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
