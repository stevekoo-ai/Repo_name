#!/usr/bin/env python3
"""
SK하이닉스(및 기타 종목) 5년치 장기 이력 백필 — 주가(KIS) + 외국인보유율(KRX).

## 배경 (2026-08-04, 사용자 요청)

5년치 데이터를 KIS API 하나로만 뽑으려다 KIS 자체의 구조적 제약에
부딪혔다. 이 저장소가 이미 매일 자동수집 중인 investor_flow.py로도
같은 벽을 한 번 겪은 적이 있어서(아래 ②), 이번엔 처음부터 두 소스로
나눴다.

① **주가는 KIS로 가능** — `inquire-daily-itemchartprice`(TR
   FHKST03010100)는 FID_INPUT_DATE_1/2로 날짜 range를 직접 받는다.
   1회 호출 최대 100건(대략 거래일 100일치)이라, 5년치를 받으려면
   윈도우를 나눠 여러 번 호출해야 한다(이 스크립트가 자동 처리).
   ✅ stevekoo-ai/open-trading-api 공식 예제
   (examples_llm/domestic_stock/inquire_daily_itemchartprice/)로
   파라미터·필드명을 교차검증했다 — 문서 기억 추정이 아니다.

② **외국인 보유율은 KIS 전체를 뒤져도 5년치가 안 나온다.** 이 저장소가
   기존에 쓰던 kis_fetch_price()(investor_flow.py, TR FHKST01010100,
   inquire-price)의 hts_frgn_ehrt 필드는 "오늘 시점 스냅샷" 1건뿐이고,
   이번에 open-trading-api에서 추가로 찾아낸 `inquire-daily-price`
   (TR FHKST01010400)도 날짜별 hts_frgn_ehrt를 주긴 하지만 공식 예제
   docstring에 "최근 30거래일(주,월)로 제한되어 있습니다"라고 명시돼
   있다 — 두 경로 다 30일 벽에 막힌다. investor_flow.py의
   kis_fetch_investor_trend()(TR FHKST01010900, inquire-investor)도
   똑같이 "최근 30영업일"이라 이 벽은 KIS 쪽 구조적 한계로 보는 게
   맞다. → 보유율만 KRX로 분리.

## ⚠️ 이 스크립트의 신뢰도 차이 (중요)

- **price 서브커맨드(KIS)**: 위 open-trading-api 교차검증 덕에 신뢰도
  높음. 그래도 이 세션은 openapi.koreainvestment.com이 네트워크
  정책상 막혀 있어 실호출 자체는 못 해봤다 — 최초 실행 시 --raw로
  실제 응답을 확인할 것.
- **foreign-ownership 서브커맨드(KRX)**: 훨씬 불확실하다. 정식 서비스는
  `openapi.krx.co.kr`(KRX 정보데이터시스템의 웹 대시보드 data.krx.co.kr
  과는 다른 도메인 — 흔히 혼동됨, 승인제 API 키 필요)로 추정되나, 실제
  엔드포인트 경로·요청 파라미터·응답 필드명 전부 문서 없이 작성한
  **최선의 추정**이다. 이 세션에서 data.krx.co.kr·openapi.krx.co.kr
  둘 다 네트워크가 막혀 있어 단 한 번도 실호출로 검증하지 못했다.
  KRX 서비스 신청 후 실제로 내려오는 응답 구조를 --raw로 찍어보고
  FOREIGN_OWNERSHIP_FIELDS 딕셔너리를 고쳐야 한다 — 이 저장소의 다른
  모든 TR과 동일한 원칙(지어낸 값 반환 금지, 필드 안 맞으면 즉시 에러).
  대안으로 커뮤니티 라이브러리 `pykrx`(github.com/sharebook-kr/pykrx)가
  같은 데이터를 비공식 경로(OTP 발급 후 다운로드, 공식 Open API 아님)로
  이미 구현해뒀다 — 정식 API 키 발급이 막히면 이쪽을 검토할 것
  (다만 비공식 스크래핑 경로라 더 깨지기 쉽다는 점은 감안).

## 다른 KIS TR과의 조합 원칙(중요 — 겹침 없음)

이 스크립트는 **일회성 5년 백필 전용**이다. 매일 갱신되는 forward-looking
데이터(당일 종가·외국인 보유율 스냅샷)는 계속 investor_flow.py의
snapshot 커맨드(sources/sk-hynix-price-snapshot.csv)가 담당 — 두
스크립트가 같은 파일을 건드리지 않는다.

환경변수 (.env나 셸 프로파일에 설정 — 절대 이 저장소에 커밋하지 않음):
  KIS_APP_KEY, KIS_APP_SECRET   — price 서브커맨드용(investor_flow.py와 공용,
                                   토큰 캐시도 같은 파일을 공유해 재발급 충돌을 피한다)
  KRX_API_KEY                    — foreign-ownership 서브커맨드용(KRX 정보데이터
                                   시스템 Open API 서비스 신청 후 발급)

사용법:
  # 1) 주가 5년치 백필(KIS, 자동 페이지네이션)
  python3 scripts/hynix_5y_history.py price --ticker 000660 --years 5

  # 필드명 최초 검증용(파싱하지 않고 원본 JSON만 출력)
  python3 scripts/hynix_5y_history.py price --ticker 000660 --years 5 --raw

  # 2) 외국인보유율 5년치 백필(KRX) — 반드시 --raw로 먼저 필드명 확인 후 정식 실행
  python3 scripts/hynix_5y_history.py foreign-ownership --ticker 000660 --years 5 --raw
  python3 scripts/hynix_5y_history.py foreign-ownership --ticker 000660 --years 5

  # 3) 위 두 CSV를 날짜 기준으로 merge해서 차트용 통합 CSV 생성
  python3 scripts/hynix_5y_history.py merge --ticker 000660
"""
import os
import sys
import csv
import json
import time
import argparse
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parent))
# 토큰 발급·캐시(kis_get_token)는 investor_flow.py 것을 그대로 재사용한다 —
# 같은 캐시 파일(scripts/.kis_token_cache.json)을 공유해 두 스크립트가
# 짧은 간격으로 각자 새 토큰을 발급받다 충돌하는 사고(2026-07-28~30
# 실사고, investor_flow.py 코드 주석 참고)를 되풀이하지 않는다.
from investor_flow import (  # noqa: E402
    kis_get_token, KIS_HOSTS, _get_env_or_die,
)

SOURCES_DIR = Path(__file__).resolve().parent.parent / "sources"

# ============================================================
# ① 주가 — KIS inquire-daily-itemchartprice (TR: FHKST03010100)
# ✅ 파라미터·필드명 출처: stevekoo-ai/open-trading-api
#    examples_llm/domestic_stock/inquire_daily_itemchartprice/
#    inquire_daily_itemchartprice.py, chk_inquire_daily_itemchartprice.py
#    (2026-08-04 교차검증, 문서 기억 추정 아님)
# ============================================================
PRICE_5Y_CSV_PATH = SOURCES_DIR / "sk-hynix-price-5y.csv"
PRICE_5Y_CSV_FIELDS = [
    "date", "ticker", "open", "high", "low", "close", "volume", "amount",
    "source", "fetched_at",
]
DAILY_CHART_FIELDS = {
    "date": "stck_bsop_date",   # 주식 영업 일자
    "open": "stck_oprc",        # 시가
    "high": "stck_hgpr",        # 최고가
    "low": "stck_lwpr",         # 최저가
    "close": "stck_clpr",       # 종가
    "volume": "acml_vol",       # 누적 거래량
    "amount": "acml_tr_pbmn",   # 누적 거래대금
}
# 한 번 호출로 최대 ~100건(대략 거래일 100일)까지만 온다(공식 문서·예제
# docstring 명시). 넉넉하게 100 "달력일" 단위로 창을 나눠 호출한다(대략
# 거래일 68일 안팎이라 100건 상한에 걸릴 일이 거의 없다) — 혹시라도 한
# 창에서 정확히 100건이 돌아오면 잘렸을 수 있다는 경고를 찍는다.
WINDOW_CALENDAR_DAYS = 100


def kis_fetch_daily_chart_window(ticker, date_1, date_2, account_type="real",
                                  org_adj_prc="0", raw=False):
    """date_1~date_2(YYYYMMDD) 구간의 일봉을 1회 호출로 가져온다(최대 ~100건).
    org_adj_prc: "0"=수정주가(기본, 액면분할 등 보정 반영), "1"=원주가.
    ⚠ 이 TR과 investor_flow.py가 이미 쓰는 다른 TR(inquire-daily-price,
    FHKST01010400) 사이에 0/1 의미가 서로 반대로 보이는 문서상 불일치를
    발견했다(전자는 "0:수정주가 1:원주가", 후자는 "0:수정주가미반영
    1:수정주가반영") — --raw로 실제 응답의 종가 흐름이 액면분할 이력과
    맞는지 한 번은 눈으로 확인할 것."""
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    token = kis_get_token(account_type)
    host = KIS_HOSTS[account_type]

    params = urllib.parse.urlencode({
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": ticker,
        "FID_INPUT_DATE_1": date_1,
        "FID_INPUT_DATE_2": date_2,
        "FID_PERIOD_DIV_CODE": "D",
        "FID_ORG_ADJ_PRC": org_adj_prc,
    })
    req = urllib.request.Request(
        f"{host}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice?{params}",
        headers={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": appkey,
            "appsecret": appsecret,
            "tr_id": "FHKST03010100",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"KIS API 호출 실패({date_1}~{date_2}): {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return []

    rows = data.get("output2")
    if rows is None:
        sys.exit(
            "API 응답에서 output2(일봉 배열)를 찾지 못했습니다 — --raw로 원본 "
            f"JSON을 확인하세요. 실제 응답 최상위 키: {sorted(data.keys())}"
        )
    if not rows:
        return []  # 해당 구간에 거래일이 없음(휴장 구간 등) — 정상

    missing = [v for v in DAILY_CHART_FIELDS.values() if v not in rows[0]]
    if missing:
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다: {missing}. 실제 응답 키: "
            f"{sorted(rows[0].keys())}\n실제 응답 1건: {json.dumps(rows[0], ensure_ascii=False)}\n"
            "이 스크립트 상단 DAILY_CHART_FIELDS 딕셔너리를 위 실제 필드명으로 고치세요."
        )
    if len(rows) >= 100:
        print(
            f"⚠️ {date_1}~{date_2} 구간이 정확히 {len(rows)}건 반환됐습니다 — "
            "상한(100건)에 걸려 일부가 잘렸을 수 있습니다. WINDOW_CALENDAR_DAYS를 "
            "줄여서 재실행을 검토하세요.",
            file=sys.stderr,
        )

    out = []
    for r in rows:
        d = r[DAILY_CHART_FIELDS["date"]]  # YYYYMMDD
        out.append({
            "date": f"{d[0:4]}-{d[4:6]}-{d[6:8]}",
            "open": int(r[DAILY_CHART_FIELDS["open"]]),
            "high": int(r[DAILY_CHART_FIELDS["high"]]),
            "low": int(r[DAILY_CHART_FIELDS["low"]]),
            "close": int(r[DAILY_CHART_FIELDS["close"]]),
            "volume": int(r[DAILY_CHART_FIELDS["volume"]]),
            "amount": int(r[DAILY_CHART_FIELDS["amount"]]),
        })
    return out


def cmd_price(args):
    if args.raw:
        # --raw는 가장 최근 창 하나만 찍어보고 종료(필드명 검증 목적).
        end = datetime.now()
        start = end - timedelta(days=WINDOW_CALENDAR_DAYS)
        kis_fetch_daily_chart_window(
            args.ticker, start.strftime("%Y%m%d"), end.strftime("%Y%m%d"),
            account_type=args.account_type, org_adj_prc=args.org_adj_prc, raw=True,
        )
        return

    target_start = datetime.now() - timedelta(days=365 * args.years)
    window_end = datetime.now()
    all_rows = {}
    calls = 0
    while window_end >= target_start:
        window_start = max(window_end - timedelta(days=WINDOW_CALENDAR_DAYS - 1), target_start)
        rows = kis_fetch_daily_chart_window(
            args.ticker, window_start.strftime("%Y%m%d"), window_end.strftime("%Y%m%d"),
            account_type=args.account_type, org_adj_prc=args.org_adj_prc,
        )
        calls += 1
        for r in rows:
            all_rows[r["date"]] = r
        print(f"  [{calls}] {window_start:%Y-%m-%d}~{window_end:%Y-%m-%d}: {len(rows)}건 "
              f"(누적 {len(all_rows)}건)", file=sys.stderr)
        window_end = window_start - timedelta(days=1)
        time.sleep(0.3)  # KIS 초당 호출 제한 여유 확보(정확한 한도는 계정별 상이)

    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    with PRICE_5Y_CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=PRICE_5Y_CSV_FIELDS)
        w.writeheader()
        for d in sorted(all_rows):
            r = all_rows[d]
            w.writerow({
                "date": d, "ticker": args.ticker,
                "open": r["open"], "high": r["high"], "low": r["low"], "close": r["close"],
                "volume": r["volume"], "amount": r["amount"],
                "source": "kis_api",
                "fetched_at": datetime.now().isoformat(timespec="seconds"),
            })
    print(f"✅ {PRICE_5Y_CSV_PATH} — {len(all_rows)}건 저장 ({calls}회 호출)")


# ============================================================
# ② 외국인 보유율 — KRX 정보데이터시스템 Open API
# ⚠️⚠️ 미검증 — 이 세션은 실호출을 못 해봤다. 아래 값들은 전부 최선의
# 추정이며, 실제 서비스 신청 후 --raw로 반드시 확인·수정해야 한다.
# 확실한 것: KIS에는 5년치를 줄 수 있는 엔드포인트가 없다(위 ② 설명).
# 불확실한 것: 아래 ENDPOINT 경로, 요청 파라미터명, 응답 필드명 전부.
# ============================================================
# 추정 근거: KRX 정보데이터시스템은 openapi.krx.co.kr에서 승인제로
# API 키를 발급한다(웹 대시보드 data.krx.co.kr과는 다른 도메인 — 흔히
# 혼동됨). "주식 > 외국인 보유량(개별종목)" 서비스가 존재하나, 정확한
# 서비스 ID·엔드포인트 경로는 승인 후 발급되는 명세서로만 확정 가능.
KRX_ENDPOINT_GUESS = "https://openapi.krx.co.kr/svc/apis/sto/frgn_trd_trend"  # ⚠️ 미검증 추정치
FOREIGN_OWNERSHIP_5Y_CSV_PATH = SOURCES_DIR / "sk-hynix-foreign-ownership-5y.csv"
FOREIGN_OWNERSHIP_5Y_CSV_FIELDS = [
    "date", "ticker", "foreign_hold_qty", "foreign_hold_pct", "listed_shares",
    "source", "fetched_at",
]
# ⚠️ 미검증 — 실제 응답 받으면 이 딕셔너리부터 고칠 것
FOREIGN_OWNERSHIP_FIELDS_GUESS = {
    "date": "BAS_DD",              # 기준일자 (추정)
    "foreign_hold_qty": "FORN_HD_QTY",   # 외국인 보유수량 (추정)
    "foreign_hold_pct": "FORN_HD_RT",    # 외국인 보유율(%) (추정)
    "listed_shares": "LIST_SHRS",        # 상장주식수 (추정)
}


def krx_fetch_foreign_ownership_window(ticker, date_1, date_2, raw=False):
    """KRX Open API로 date_1~date_2(YYYYMMDD) 구간 외국인보유율 조회.
    ⚠️ 미검증 함수 — ENDPOINT·파라미터명·응답 필드명 전부 추정치.
    반드시 --raw로 먼저 실제 응답을 확인하고 위 KRX_ENDPOINT_GUESS·
    FOREIGN_OWNERSHIP_FIELDS_GUESS를 실제 값으로 고친 뒤 정식 실행할 것."""
    api_key = _get_env_or_die("KRX_API_KEY")
    # ⚠️ 파라미터명(basDd/strtDd/endDd 등)도 추정 — 실제 서비스 명세서로 교체 필요
    params = urllib.parse.urlencode({
        "AUTH_KEY": api_key,
        "isuCd": ticker,
        "strtDd": date_1,
        "endDd": date_2,
    })
    req = urllib.request.Request(f"{KRX_ENDPOINT_GUESS}?{params}")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(
            f"KRX API 호출 실패({date_1}~{date_2}): {e.code} {e.read().decode(errors='replace')}\n"
            "⚠️ 이 함수는 검증되지 않은 추정 엔드포인트를 씁니다 — 실패가 인증 문제인지 "
            "URL/파라미터명이 틀린 건지 먼저 확인하세요(openapi.krx.co.kr 실제 서비스 "
            "명세서 대조 필요)."
        )
    except urllib.error.URLError as e:
        sys.exit(
            f"KRX API 연결 실패: {e}\n"
            f"⚠️ KRX_ENDPOINT_GUESS({KRX_ENDPOINT_GUESS})가 실제 서비스 URL이 아닐 "
            "가능성이 있습니다 — openapi.krx.co.kr에서 발급받은 실제 명세서로 교체하세요."
        )

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return []

    # ⚠️ 최상위 응답 키(예: "OutBlock_1")도 추정 — 실제 응답 구조 확인 후 고칠 것
    rows = data.get("OutBlock_1") or data.get("output") or data.get("result")
    if rows is None:
        sys.exit(
            f"API 응답에서 데이터 배열을 찾지 못했습니다 — --raw로 원본을 확인하세요. "
            f"실제 응답 최상위 키: {sorted(data.keys())}"
        )
    if not rows:
        return []

    missing = [v for v in FOREIGN_OWNERSHIP_FIELDS_GUESS.values() if v not in rows[0]]
    if missing:
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다(전부 추정치였으니 당연할 수 있음): {missing}\n"
            f"실제 응답 키: {sorted(rows[0].keys())}\n실제 응답 1건: "
            f"{json.dumps(rows[0], ensure_ascii=False)}\n"
            "이 스크립트 상단 FOREIGN_OWNERSHIP_FIELDS_GUESS 딕셔너리를 위 실제 필드명으로 고치세요."
        )

    out = []
    for r in rows:
        d = str(r[FOREIGN_OWNERSHIP_FIELDS_GUESS["date"]])  # YYYYMMDD 가정
        out.append({
            "date": f"{d[0:4]}-{d[4:6]}-{d[6:8]}" if len(d) == 8 else d,
            "foreign_hold_qty": int(r[FOREIGN_OWNERSHIP_FIELDS_GUESS["foreign_hold_qty"]]),
            "foreign_hold_pct": float(r[FOREIGN_OWNERSHIP_FIELDS_GUESS["foreign_hold_pct"]]),
            "listed_shares": int(r[FOREIGN_OWNERSHIP_FIELDS_GUESS["listed_shares"]]),
        })
    return out


def cmd_foreign_ownership(args):
    if args.raw:
        end = datetime.now()
        start = end - timedelta(days=WINDOW_CALENDAR_DAYS)
        krx_fetch_foreign_ownership_window(
            args.ticker, start.strftime("%Y%m%d"), end.strftime("%Y%m%d"), raw=True,
        )
        return

    target_start = datetime.now() - timedelta(days=365 * args.years)
    window_end = datetime.now()
    all_rows = {}
    calls = 0
    while window_end >= target_start:
        window_start = max(window_end - timedelta(days=WINDOW_CALENDAR_DAYS - 1), target_start)
        rows = krx_fetch_foreign_ownership_window(
            args.ticker, window_start.strftime("%Y%m%d"), window_end.strftime("%Y%m%d"),
        )
        calls += 1
        for r in rows:
            all_rows[r["date"]] = r
        print(f"  [{calls}] {window_start:%Y-%m-%d}~{window_end:%Y-%m-%d}: {len(rows)}건 "
              f"(누적 {len(all_rows)}건)", file=sys.stderr)
        window_end = window_start - timedelta(days=1)
        time.sleep(0.3)

    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    with FOREIGN_OWNERSHIP_5Y_CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FOREIGN_OWNERSHIP_5Y_CSV_FIELDS)
        w.writeheader()
        for d in sorted(all_rows):
            r = all_rows[d]
            w.writerow({
                "date": d, "ticker": args.ticker,
                "foreign_hold_qty": r["foreign_hold_qty"], "foreign_hold_pct": r["foreign_hold_pct"],
                "listed_shares": r["listed_shares"],
                "source": "krx_openapi",
                "fetched_at": datetime.now().isoformat(timespec="seconds"),
            })
    print(f"✅ {FOREIGN_OWNERSHIP_5Y_CSV_PATH} — {len(all_rows)}건 저장 ({calls}회 호출)")


# ============================================================
# ③ merge — 두 CSV를 날짜 기준으로 합쳐 차트용 통합 CSV 생성
# ============================================================
MERGED_CSV_PATH = SOURCES_DIR / "hynix_price_foreign_5y.csv"
MERGED_CSV_FIELDS = [
    "date", "ticker", "open", "high", "low", "close", "volume",
    "foreign_hold_pct", "foreign_hold_qty",
]


def cmd_merge(args):
    if not PRICE_5Y_CSV_PATH.exists():
        sys.exit(f"{PRICE_5Y_CSV_PATH}가 없습니다 — 먼저 'price' 서브커맨드를 실행하세요.")
    if not FOREIGN_OWNERSHIP_5Y_CSV_PATH.exists():
        sys.exit(f"{FOREIGN_OWNERSHIP_5Y_CSV_PATH}가 없습니다 — 먼저 'foreign-ownership' 서브커맨드를 실행하세요.")

    price_by_date = {}
    with PRICE_5Y_CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["ticker"] == args.ticker:
                price_by_date[row["date"]] = row

    own_by_date = {}
    with FOREIGN_OWNERSHIP_5Y_CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["ticker"] == args.ticker:
                own_by_date[row["date"]] = row

    # 두 소스의 거래일 캘린더가 100% 일치한다는 보장이 없다(KRX vs KIS 각자
    # 휴장일 처리 차이 가능) — inner join이 아니라 가격 캘린더를 기준으로
    # 삼고, 그 날짜에 보유율 데이터가 없으면 빈 값으로 남긴다(지어내지 않음).
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    matched = 0
    with MERGED_CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MERGED_CSV_FIELDS)
        w.writeheader()
        for d in sorted(price_by_date):
            p = price_by_date[d]
            o = own_by_date.get(d)
            if o:
                matched += 1
            w.writerow({
                "date": d, "ticker": args.ticker,
                "open": p["open"], "high": p["high"], "low": p["low"], "close": p["close"],
                "volume": p["volume"],
                "foreign_hold_pct": o["foreign_hold_pct"] if o else "",
                "foreign_hold_qty": o["foreign_hold_qty"] if o else "",
            })
    total = len(price_by_date)
    print(f"✅ {MERGED_CSV_PATH} — 주가 {total}건 중 보유율 매칭 {matched}건"
          f"({matched/total*100:.0f}%)" if total else "0건")
    if total and matched < total * 0.9:
        print(
            "⚠️ 보유율 매칭률이 90% 미만입니다 — 두 소스의 거래일 캘린더가 어긋나거나 "
            "foreign-ownership 백필이 아직 부분적일 수 있습니다. 빈 값이 많으면 차트에서 "
            "구간이 끊겨 보일 수 있습니다.",
            file=sys.stderr,
        )


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("price", help="주가 5년치 백필(KIS inquire-daily-itemchartprice)")
    pp.add_argument("--ticker", default="000660")
    pp.add_argument("--years", type=int, default=5)
    pp.add_argument("--org-adj-prc", dest="org_adj_prc", default="0",
                     help="0=수정주가(기본), 1=원주가 — 이 TR 기준(다른 TR과 0/1 의미가 다를 수 있음, 상단 주석 참고)")
    pp.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    pp.add_argument("--raw", action="store_true", help="파싱하지 않고 최근 한 구간의 원본 JSON만 출력(필드명 검증용)")
    pp.set_defaults(func=cmd_price)

    pf = sub.add_parser("foreign-ownership", help="외국인보유율 5년치 백필(KRX Open API, ⚠️ 필드명 미검증)")
    pf.add_argument("--ticker", default="000660")
    pf.add_argument("--years", type=int, default=5)
    pf.add_argument("--raw", action="store_true", help="파싱하지 않고 최근 한 구간의 원본 JSON만 출력(필드명 검증 — 반드시 정식 실행 전에 먼저 할 것)")
    pf.set_defaults(func=cmd_foreign_ownership)

    pm = sub.add_parser("merge", help="price+foreign-ownership 5년 CSV를 날짜 기준 merge")
    pm.add_argument("--ticker", default="000660")
    pm.set_defaults(func=cmd_merge)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
