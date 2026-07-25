#!/usr/bin/env python3
"""
KIS API로 여러 계좌(일반·ISA·IRP·DC 등)의 보유 종목·평가금액을 조회해
sources/portfolio-holdings.csv에 기록하는 스크립트. GitHub Actions가 매일
실행하고, Claude(또는 다른 에이전트)는 이 CSV를 읽어 "계좌별 보유종목의
거시환경 대비 유불리 판단" 같은 분석에 쓴다 — 판단 자체는 이 스크립트가
하지 않는다(규칙 기반 수집만).

계좌 등록(GitHub Secrets, 채팅에 붙여넣지 말 것) — 계좌마다 고정된 이름의
환경변수 하나씩, 값은 "CANO,ACNT_PRDT_CD"(예: "50123456,01"):
  KIS_ACCOUNT_GEN   — 일반(위탁) 계좌
  KIS_ACCOUNT_ISP   — ISA 계좌
  KIS_ACCOUNT_DC    — DC(퇴직연금) 계좌
  KIS_ACCOUNT_IRP   — IRP(개인퇴직연금) 계좌
  4개 전부 등록할 필요는 없다 — 등록된 것만 조회한다.

⚠ 계좌 종류별로 실제 KIS 잔고조회 TR이 다르다:
  - GEN/ISP(일반·ISA 등 위탁계좌): TR TTTC8434R (문서 기억 기반, --raw로 검증 권장)
  - DC/IRP(퇴직연금계좌): **아직 미구현** — 정확한 TR을 확신할 수 없어
    임의 코드를 넣는 대신 명시적으로 "미구현"을 반환한다. 실제 계정으로
    확인 후 PENSION_BALANCE_TR을 채워 넣을 것.

사용법:
  python3 scripts/portfolio_holdings.py sync                  # 등록된 계좌 전체 조회+CSV 기록
  python3 scripts/portfolio_holdings.py sync --raw --account GEN   # GEN 계좌 원본 JSON만 확인
"""
import os
import sys
import csv
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

KIS_HOSTS = {
    "real": "https://openapi.koreainvestment.com:9443",
    "vts": "https://openapivts.koreainvestment.com:29443",
}

CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "portfolio-holdings.csv"
CSV_FIELDS = [
    "date", "account_label", "ticker", "name", "quantity", "avg_price",
    "current_price", "eval_amount", "profit_loss", "profit_loss_pct",
    "source", "fetched_at",
]

# KIS "주식잔고조회" TR: TTTC8434R(실전)/VTTC8434R(모의) — 일반/ISA 등 위탁계좌
# GET /uapi/domestic-stock/v1/trading/inquire-balance
# ⚠ 필드명은 문서 기억 기반 — 최초 실호출 시 --raw로 검증할 것
GENERAL_BALANCE_TR = {"real": "TTTC8434R", "vts": "VTTC8434R"}
HOLDING_FIELDS = {
    "ticker": "pdno", "name": "prdt_name", "quantity": "hldg_qty",
    "avg_price": "pchs_avg_pric", "current_price": "prpr",
    "eval_amount": "evlu_amt", "profit_loss": "evlu_pfls_amt",
    "profit_loss_pct": "evlu_pfls_rt",
}

# 퇴직연금(IRP/DC) 잔고조회 TR — 미확인. 일반계좌와 다른 TR을 쓰는 것으로
# 알려져 있으나 정확한 코드를 문서 기억만으로 확신할 수 없어 비워둔다.
PENSION_BALANCE_TR = None

# 계좌 슬롯: 환경변수 접미사 -> (표시 라벨, 퇴직연금 여부)
ACCOUNT_SLOTS = {
    "GEN": ("일반", False),
    "ISP": ("ISA", False),
    "DC": ("DC", True),
    "IRP": ("IRP", True),
}


def _get_env_or_die(name):
    v = os.environ.get(name)
    if not v:
        sys.exit(f"환경변수 {name}이(가) 없습니다.")
    return v


def _load_accounts():
    accounts = []
    for suffix, (label, is_pension) in ACCOUNT_SLOTS.items():
        raw = os.environ.get(f"KIS_ACCOUNT_{suffix}")
        if not raw:
            continue
        parts = [p.strip() for p in raw.split(",")]
        if len(parts) != 2:
            sys.exit(
                f"KIS_ACCOUNT_{suffix} 형식이 잘못됐습니다: '{raw}' — "
                f"\"CANO,ACNT_PRDT_CD\" 형식이어야 합니다(예: \"50123456,01\")."
            )
        cano, prdt_cd = parts
        accounts.append({"slot": suffix, "cano": cano, "prdt_cd": prdt_cd, "label": label, "pension": is_pension})
    if not accounts:
        sys.exit(
            "등록된 계좌가 없습니다. KIS_ACCOUNT_GEN/ISP/DC/IRP 중 필요한 것을 "
            "\"CANO,ACNT_PRDT_CD\" 형식으로 GitHub Secrets에 설정하세요."
        )
    return accounts


def kis_get_token(account_type="real"):
    from pathlib import Path as _P
    import json as _json
    from datetime import datetime as _dt, timedelta as _td

    token_cache = _P(__file__).resolve().parent / ".kis_token_cache.json"
    if token_cache.exists():
        cached = _json.loads(token_cache.read_text())
        if cached.get("account_type") == account_type and \
                _dt.fromisoformat(cached["expires_at"]) > _dt.now():
            return cached["access_token"]

    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    host = KIS_HOSTS[account_type]
    body = json.dumps({"grant_type": "client_credentials", "appkey": appkey, "appsecret": appsecret}).encode()
    req = urllib.request.Request(f"{host}/oauth2/tokenP", data=body, method="POST",
                                  headers={"content-type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    token = data["access_token"]
    expires_at = _dt.now() + _td(seconds=int(data.get("expires_in", 86400)) - 300)
    token_cache.write_text(_json.dumps({"account_type": account_type, "access_token": token,
                                         "expires_at": expires_at.isoformat()}))
    return token


def fetch_general_balance(cano, prdt_cd, account_type="real", raw=False):
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    token = kis_get_token(account_type)
    host = KIS_HOSTS[account_type]
    tr_id = GENERAL_BALANCE_TR[account_type]

    params = (
        f"CANO={cano}&ACNT_PRDT_CD={prdt_cd}&AFHR_FLPR_YN=N&OFL_YN=&INQR_DVSN=02"
        f"&UNPR_DVSN=01&FUND_STTL_ICLD_YN=N&FNCG_AMT_AUTO_RDPT_YN=N&PRCS_DVSN=00"
        f"&CTX_AREA_FK100=&CTX_AREA_NK100="
    )
    req = urllib.request.Request(
        f"{host}/uapi/domestic-stock/v1/trading/inquire-balance?{params}",
        headers={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": appkey,
            "appsecret": appsecret,
            "tr_id": tr_id,
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"KIS 잔고조회 API 실패: {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return []

    rows = data.get("output1")
    if rows is None:
        sys.exit(
            "응답에서 output1(보유종목 목록)을 찾지 못했습니다 — --raw로 원본을 "
            "확인하고 추출 키를 응답 구조에 맞게 고치세요."
        )
    if not rows:
        return []  # 보유 종목 없는 빈 계좌 — 정상

    missing = [v for v in HOLDING_FIELDS.values() if v not in rows[0]]
    if missing:
        sys.exit(
            f"예상한 필드가 응답에 없습니다: {missing}. --raw로 원본을 확인해 "
            "이 스크립트 상단 HOLDING_FIELDS를 실제 필드명으로 고치세요."
        )

    holdings = []
    for r in rows:
        qty = int(r[HOLDING_FIELDS["quantity"]])
        if qty == 0:
            continue
        holdings.append({
            "ticker": r[HOLDING_FIELDS["ticker"]],
            "name": r[HOLDING_FIELDS["name"]],
            "quantity": qty,
            "avg_price": r[HOLDING_FIELDS["avg_price"]],
            "current_price": r[HOLDING_FIELDS["current_price"]],
            "eval_amount": r[HOLDING_FIELDS["eval_amount"]],
            "profit_loss": r[HOLDING_FIELDS["profit_loss"]],
            "profit_loss_pct": r[HOLDING_FIELDS["profit_loss_pct"]],
        })
    return holdings


def _read_csv():
    if not CSV_PATH.exists():
        return {}
    rows = {}
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[(row["date"], row["account_label"], row["ticker"])] = row
    return rows


def _write_csv(rows_by_key):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows_by_key.values(), key=lambda r: (r["date"], r["account_label"], r["ticker"]))
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in ordered:
            w.writerow(r)


def upsert_holdings(account_label, holdings, source="kis_api"):
    existing = _read_csv()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    # 오늘자 이 계좌의 기존 행은 전량 청산(매도로 사라진 종목이 남지 않도록)
    existing = {k: v for k, v in existing.items() if not (k[0] == today and k[1] == account_label)}
    for h in holdings:
        key = (today, account_label, h["ticker"])
        existing[key] = {
            "date": today, "account_label": account_label, "ticker": h["ticker"],
            "name": h["name"], "quantity": h["quantity"], "avg_price": h["avg_price"],
            "current_price": h["current_price"], "eval_amount": h["eval_amount"],
            "profit_loss": h["profit_loss"], "profit_loss_pct": h["profit_loss_pct"],
            "source": source, "fetched_at": fetched_at,
        }
    _write_csv(existing)
    return len(holdings)


def cmd_sync(args):
    accounts = _load_accounts()
    if args.account:
        accounts = [a for a in accounts if a["slot"] == args.account.upper()]
        if not accounts:
            sys.exit(f"'{args.account}' 슬롯은 등록되지 않았습니다(GEN/ISP/DC/IRP 중 하나).")

    total = 0
    for acc in accounts:
        if acc["pension"]:
            print(f"[{acc['label']}] 퇴직연금 계좌 — PENSION_BALANCE_TR 미구현, 건너뜀 "
                  f"(정확한 TR 확인 후 코드 보강 필요)", file=sys.stderr)
            continue
        try:
            holdings = fetch_general_balance(acc["cano"], acc["prdt_cd"], args.account_type, raw=args.raw)
        except SystemExit as e:
            print(f"[{acc['label']}] 조회 실패: {e}", file=sys.stderr)
            continue
        if args.raw:
            continue
        n = upsert_holdings(acc["label"], holdings)
        total += n
        print(f"[{acc['label']}] {n}개 보유종목 기록")

    if not args.raw:
        print(f"\n총 {total}개 종목 → {CSV_PATH}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("sync", help="등록된 계좌 전체(또는 --account로 선택 1개) 조회+CSV 기록")
    ps.add_argument("--account", help="GEN/ISP/DC/IRP 중 하나, 생략시 등록된 계좌 전체")
    ps.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    ps.add_argument("--raw", action="store_true", help="파싱하지 않고 원본 JSON만 출력(필드명 검증용)")
    ps.set_defaults(func=cmd_sync)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
