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

  # 4) 신용융자잔고(융자/대주) — 찐반등 신호①(빚의 청산)의 데이터소스
  python3 scripts/investor_flow.py credit-balance --ticker 000660

  # 5) 코스피/코스닥 지수 현재가 + 상승/하락/상한/하한 종목수
  python3 scripts/investor_flow.py index-quote --index-code 0001  # 코스피
  python3 scripts/investor_flow.py index-quote --index-code 1001  # 코스닥

  # 6) 공매도 일별추이
  python3 scripts/investor_flow.py short-sale --ticker 000660

  # 7) ETF/ETN 현재가+NAV+괴리율(포트폴리오 보유 ETF 점검용)
  python3 scripts/investor_flow.py etf-nav --ticker 469150

  # 8) 종목/지수 월봉 이력(scripts/correlation_analysis.py 입력용)
  python3 scripts/investor_flow.py monthly-history --code 000660 --label SK하이닉스 --months 24
  python3 scripts/investor_flow.py monthly-history --code 0001 --is-index --months 24  # 코스피
  python3 scripts/investor_flow.py monthly-history --code 000660 --months 3 --raw  # 필드명 최초 검증용
  python3 scripts/investor_flow.py monthly-history --code 0001 --is-index --start 1980-01-01  # 장기 backfill(1회성)

  # 9) 종목/지수 일봉 이력(2026-08-17 추가, correlation_analysis.py 일봉 확대 차트용)
  python3 scripts/investor_flow.py daily-history --code 000660 --label SK하이닉스 --days 60
  python3 scripts/investor_flow.py daily-history --code 0001 --is-index --start 2023-01-01  # 장기 backfill(1회성)
"""
import os
import sys
import csv
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import date, datetime, timedelta, timezone

CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "sk-hynix-investor-flow.csv"
TOKEN_CACHE = Path(__file__).resolve().parent / ".kis_token_cache.json"

KIS_HOSTS = {
    "real": "https://openapi.koreainvestment.com:9443",
    "vts": "https://openapivts.koreainvestment.com:29443",
}

# 2026-08-17 실측: 이 파일의 모든 urlopen(req) 호출에 timeout이 전혀 없었다
# (기본 socket timeout=None → 연결이 멎으면 무한 대기). kis-old-history-probe
# 실행 중 monthly-history 구간 호출 하나가 3분+ 걸려 멈춰서 발견 —
# customs_trade.py/molit.py가 이미 겪은 것과 같은 종류의 간헐적 연결 문제로
# 보이지만, 이쪽엔 타임아웃이 없어서 job이 끝없이 매달릴 수 있었다. 모든
# urlopen에 이 타임아웃을 적용한다(개별 함수의 retry/circuit-breaker 로직과
# 별개로, 최소한 "멎지는 않는다"를 보장).
KIS_HTTP_TIMEOUT_S = 20

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

# KIS "국내주식 현재가 시세" TR: FHKST01010100
# GET /uapi/domestic-stock/v1/quotations/inquire-price
# ✅ 2026-07-28 실계정 --raw 응답으로 검증 완료(더 이상 문서기억 기반 아님).
# 이때 부수 발견 — 응답에 hts_frgn_ehrt(외국인 보유율/소진율)·frgn_hldn_qty
# (외국인 보유수량)·d250_hgpr(250일 최고가)·d250_hgpr_vrss_prpr_rate(그
# 대비 등락률, 즉 드로다운)가 이미 들어있었다. 그동안 위키에서 매번
# "KSD 보유율 미확인"·"정확한 종가 미확인"·드로다운 수기 계산으로 처리해온
# 세 가지가 전부 이 한 번의 API 호출로 해결된다 — snapshot 커맨드로 별도
# 영속화한다(아래 PRICE_SNAPSHOT_FIELDS).
PRICE_FIELDS = {
    "price": "stck_prpr",       # 현재가(장중)/종가(장마감후)
    "change": "prdy_vrss",      # 전일대비
    "change_pct": "prdy_ctrt",  # 전일대비율(%)
    "volume": "acml_vol",       # 누적거래량
}

# 위 TR의 부가 필드 — 외국인 보유율/최고가 대비 드로다운. snapshot 커맨드
# 전용(quote 커맨드의 즉석 조회에는 안 씀, 하위호환 유지).
PRICE_SNAPSHOT_EXTRA_FIELDS = {
    "foreign_hold_pct": "hts_frgn_ehrt",             # 외국인 보유율(%)
    "foreign_hold_qty": "frgn_hldn_qty",             # 외국인 보유수량
    "day250_high": "d250_hgpr",                      # 250거래일 최고가
    "day250_high_date": "d250_hgpr_date",            # 그 날짜(YYYYMMDD)
    "day250_high_vrss_pct": "d250_hgpr_vrss_prpr_rate",  # 최고가 대비 등락률(=드로다운, 부호 반전 아님에 유의)
}

# KIS "해외주식 현재가상세" TR: HHDFS76200200 (ADR·해외상장 종목용)
# GET /uapi/overseas-price/v1/quotations/price-detail
# ✅ 2026-07-28 실계정 --raw 응답으로 검증 완료. 애초 예상했던 diff/rate
# 필드는 존재하지 않았다 — 실제 응답엔 last(현재가)·base(전일종가)만 있고
# 전일대비/등락률은 별도 필드로 안 내려온다(t_xdif/t_xrat은 원화 환산
# 기준으로 보이는 값이라 신뢰하지 않고, last-base로 직접 계산한다).
OVERSEAS_PRICE_FIELDS = {
    "price": "last",       # 현재가
    "prev_close": "base",  # 전일종가
}

ADR_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "sk-hynix-adr-quote.csv"
ADR_CSV_FIELDS = [
    "date", "symbol", "price", "change", "change_pct", "prev_close",
    "crosscheck", "crosscheck_detail", "source", "fetched_at",
]

# 2026-08-01 신설 — change_pct 부호버그(diff는 +인데 API의 rate 필드는 -로
# 나온 사례, 7/31 SKHY 발견) 재발 방지용 크로스체크. 서로 독립적인 3가지
# 방법으로 등락률을 각각 계산해 서로 맞는지 대조하고, 어긋나면 숫자를
# 지어내지 않고 change_pct를 비워둔 채 "MISMATCH"로 표시한다 — 사용자
# 요청("3가지 방법이 모두 같으면 확정, 안 맞으면 나한테 보고하고 내가
# 결정")에 따른 설계. 자동화 파이프라인(GitHub Actions)은 판단을 못 하니
# 여기서는 "숨기지 않고 눈에 띄게 기록"까지만 하고, 실제 결정은 이 CSV를
# 읽는 사람(또는 Claude 세션)이 사용자에게 보고 후 받는다.
ADR_CROSSCHECK_TOLERANCE_PCT = 0.1  # 이 안이면 "사실상 같음"으로 간주(반올림 오차)

# 2026-07-31 신설 — stevekoo-ai/open-trading-api(KIS 공식 예제 저장소) 조사로
# 발견한 4개 신규 TR. 그동안 위키에서 "미확인"으로 남아있던 신용융자잔고
# (찐반등 신호①)와, 코스피/코스닥 지수·상한가 종목수(매번 웹검색하던 것)를
# API로 대체한다. 아래 4개 TR 전부 이 샌드박스에서 실호출 검증을 못 했다
# (아웃바운드 네트워크 차단) — open-trading-api의 chk_*.py 예제 파일에 있는
# COLUMN_MAPPING을 근거로 필드명을 채웠으나, 최초 실행 시 반드시 --raw로
# 원본 응답을 확인할 것(이 저장소의 기존 원칙과 동일).

# KIS "국내주식 신용잔고 일별추이" TR: FHPST04760000
# GET /uapi/domestic-stock/v1/quotations/daily-credit-balance
# 출처: open-trading-api examples_llm/domestic_stock/daily_credit_balance/
CREDIT_BALANCE_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "sk-hynix-credit-balance.csv"
CREDIT_BALANCE_CSV_FIELDS = [
    "date", "ticker",
    "loan_new_qty", "loan_redeem_qty", "loan_balance_qty", "loan_balance_amt", "loan_balance_rate",
    "short_new_qty", "short_redeem_qty", "short_balance_qty", "short_balance_amt", "short_balance_rate",
    "source", "fetched_at",
]
CREDIT_BALANCE_FIELDS = {
    "date": "stlm_date",                          # 결제 일자
    "loan_new_qty": "whol_loan_new_stcn",          # 전체 융자 신규 주수
    "loan_redeem_qty": "whol_loan_rdmp_stcn",      # 전체 융자 상환 주수(매도상환+현금상환 합계)
    "loan_balance_qty": "whol_loan_rmnd_stcn",     # 전체 융자 잔고 주수
    "loan_balance_amt": "whol_loan_rmnd_amt",      # 전체 융자 잔고 금액 — 단위 미검증, --raw로 확인 후 사용
    "loan_balance_rate": "whol_loan_rmnd_rate",    # 전체 융자 잔고 비율(%)
    "short_new_qty": "whol_stln_new_stcn",         # 전체 대주 신규 주수
    "short_redeem_qty": "whol_stln_rdmp_stcn",     # 전체 대주 상환 주수
    "short_balance_qty": "whol_stln_rmnd_stcn",    # 전체 대주 잔고 주수
    "short_balance_amt": "whol_stln_rmnd_amt",     # 전체 대주 잔고 금액
    "short_balance_rate": "whol_stln_rmnd_rate",   # 전체 대주 잔고 비율(%)
}

# KIS "국내업종 현재지수" TR: FHPUP02100000
# GET /uapi/domestic-stock/v1/quotations/inquire-index-price
# 출처: open-trading-api examples_llm/domestic_stock/inquire_index_price/
# 종목코드 대신 업종코드 사용: 코스피=0001, 코스닥=1001, 코스피200=2001
INDEX_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "kr-index-quote.csv"
INDEX_CSV_FIELDS = [
    "date", "index_code", "index_name", "price", "change", "change_pct",
    "advancers", "decliners", "unchanged", "limit_up", "limit_down",
    "source", "fetched_at",
]
INDEX_NAMES = {"0001": "KOSPI", "1001": "KOSDAQ", "2001": "KOSPI200"}

# 월봉 이력 저장 — code별로 한 파일에 섞어 쓴다(종목·지수 구분은 code 컬럼).
MONTHLY_PRICE_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "monthly-price-history.csv"
MONTHLY_PRICE_CSV_FIELDS = ["date", "code", "label", "close", "source", "fetched_at"]
# 2026-08-17 사용자 요청 — 일봉은 별도 파일. monthly-price-history.csv에
# 섞으면 "한 달에 한 행"을 가정하는 correlation_analysis.py의 월별 로직이
# 깨진다(한 달에 20여 개의 일봉 행이 들어가버림).
DAILY_PRICE_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "daily-price-history.csv"
DAILY_PRICE_CSV_FIELDS = ["date", "code", "label", "close", "source", "fetched_at"]
INDEX_FIELDS = {
    "price": "bstp_nmix_prpr",          # 업종 지수 현재가
    "change": "bstp_nmix_prdy_vrss",    # 전일 대비
    "change_pct": "bstp_nmix_prdy_ctrt",  # 전일 대비율(%)
    "advancers": "ascn_issu_cnt",       # 상승 종목 수
    "decliners": "down_issu_cnt",       # 하락 종목 수
    "unchanged": "stnr_issu_cnt",       # 보합 종목 수
    "limit_up": "uplm_issu_cnt",        # 상한 종목 수 — "코스피 톱5 중 3개 상한가" 같은 서술을 API로 확인 가능
    "limit_down": "lslm_issu_cnt",      # 하한 종목 수
}

# KIS "국내주식 공매도 일별추이" TR: FHPST04830000
# GET /uapi/domestic-stock/v1/quotations/daily-short-sale
# 출처: open-trading-api examples_llm/domestic_stock/daily_short_sale/
SHORT_SALE_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "sk-hynix-short-sale.csv"
SHORT_SALE_CSV_FIELDS = [
    "date", "ticker", "short_qty", "short_vol_pct", "cum_short_qty", "cum_short_vol_pct",
    "short_amt", "source", "fetched_at",
]
SHORT_SALE_FIELDS = {
    "date": "stck_bsop_date",                   # 주식 영업 일자
    "short_qty": "ssts_cntg_qty",                # 공매도 체결 수량
    "short_vol_pct": "ssts_vol_rlim",            # 공매도 거래량 비중(%)
    "cum_short_qty": "acml_ssts_cntg_qty",       # 누적 공매도 체결 수량
    "cum_short_vol_pct": "acml_ssts_cntg_qty_rlim",  # 누적 공매도 체결 수량 비중(%)
    "short_amt": "ssts_tr_pbmn",                 # 공매도 거래 대금
}

# KIS "ETF/ETN 현재가" TR: FHPST02400000
# GET /uapi/etfetn/v1/quotations/inquire-price
# 출처: open-trading-api examples_llm/etfetn/inquire_price/
# 포트폴리오 보유 ETF(ACE AI반도체TOP3+, SOL AI반도체소부장, KODEX 인도Nifty50 등)의
# NAV·괴리율을 매일 수집해 portfolio-holdings.csv의 현재가와 대조하는 용도.
ETF_NAV_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "portfolio-etf-nav.csv"
ETF_NAV_CSV_FIELDS = [
    "date", "ticker", "price", "nav", "nav_change", "nav_change_pct",
    "tracking_error_pct", "divergence_pct", "source", "fetched_at",
]
ETF_NAV_FIELDS = {
    "price": "stck_prpr",           # 주식 현재가
    "nav": "nav",                   # NAV
    "nav_change": "nav_prdy_vrss",  # NAV 전일 대비
    "nav_change_pct": "nav_prdy_ctrt",  # NAV 전일 대비율(%)
    "tracking_error_pct": "trc_errt",  # 추적 오차율(%)
    "divergence_pct": "dprt",       # 괴리율(%) — 시장가가 NAV 대비 얼마나 괴리됐는지
}

# 2026-07-28 신설 — 본주 종가·외국인 보유율·250일 최고가 대비 등락률을
# 매일 영속화. 그동안 위키 리포트에서 "정확한 종가 미확인"·"KSD 보유율
# 미확인"으로 반복 표기되던 두 항목과, 드로다운 수기 계산을 이 파일
# 하나로 대체한다. investor-flow.csv(수급)와는 별도 파일 — 수급은 30일
# 이력 TR이라 갱신 주기가 다르고, 이건 당일 스냅샷이라 성격이 다르다.
PRICE_SNAPSHOT_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "sk-hynix-price-snapshot.csv"
PRICE_SNAPSHOT_CSV_FIELDS = [
    "date", "ticker", "price", "change", "change_pct", "volume",
    "foreign_hold_pct", "foreign_hold_qty",
    "day250_high", "day250_high_date", "day250_high_vrss_pct",
    "source", "fetched_at",
]


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
    """KIS OAuth2 접근토큰 발급. 24시간 유효 — 로컬에 캐시해 재발급 최소화.

    ⚠ 2026-07-31 수정: 캐시 형식을 scripts/portfolio_holdings.py와 동일한
    "{account_type}:{appkey}" 키 방식으로 통일했다. 예전엔 이 스크립트만
    단일 엔트리 형식을 써서, 같은 파일을 쓰더라도 portfolio_holdings.py가
    이 스크립트가 막 발급한 토큰을 읽지 못했다(형식 불일치) — 그 결과 두
    스크립트가 GitHub Actions에서 비슷한 시각에 각자 새 토큰을 발급받으려다
    KIS의 "동일 appkey 단시간 재발급 제한"에 걸려 하나가 403으로 실패하는
    사고가 반복됐다(2026-07-28~30, portfolio-holdings-sync.yml 3일 연속 실패
    — sk-hynix-daily-report.yml 저녁 실행과 45~90초 간격으로 겹침). 형식을
    통일하고 워크플로에 actions/cache로 이 파일을 공유하게 하면, 먼저 도는
    쪽이 발급한 토큰을 나중 쪽이 재사용해 충돌을 피한다."""
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    cache_key = f"{account_type}:{appkey}"

    cached_all = {}
    if TOKEN_CACHE.exists():
        try:
            cached_all = json.loads(TOKEN_CACHE.read_text())
        except json.JSONDecodeError:
            cached_all = {}
        entry = cached_all.get(cache_key)
        if entry and datetime.fromisoformat(entry["expires_at"]) > datetime.now():
            return entry["access_token"]

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
    with urllib.request.urlopen(req, timeout=KIS_HTTP_TIMEOUT_S) as resp:
        data = json.loads(resp.read())

    token = data["access_token"]
    expires_at = datetime.now() + timedelta(seconds=int(data.get("expires_in", 86400)) - 300)
    cached_all[cache_key] = {"access_token": token, "expires_at": expires_at.isoformat()}
    TOKEN_CACHE.write_text(json.dumps(cached_all))
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
        with urllib.request.urlopen(req, timeout=KIS_HTTP_TIMEOUT_S) as resp:
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

    # ⚠ *_tr_pbmn 필드는 실측 결과 "백만원" 단위로 확인됨(2026-07-25 실계정
    # 테스트: 7/24 외국인 1일 순매도 필드값 -1,753,255 → ×1,000,000 = 약
    # -1.753조원, 같은 날 웹검색으로 확보한 "1조7,568억원 순매도" 추정치와
    # 0.2% 오차로 정합 — "원" 단위였다면 100만 배 차이가 났을 것이므로
    # 백만원 단위가 맞다고 판단). 위키 관례(원 단위 표기)에 맞춰 정규화.
    KRW_UNIT_MULTIPLIER = 1_000_000

    # ⚠ 2026-08-21 발견 — 장중(특히 개장 직후) 조회 시 당일 행의 *_tr_pbmn
    # 필드가 KIS 쪽에서 아직 정산 전이라 빈 문자열('')로 내려오는 경우가
    # 있음(int('') → ValueError로 스크립트 전체가 죽어 07:00/10:00 KST
    # 자동 리포트가 여러 날 연속 실패한 원인 — GitHub Actions 로그로 확인).
    # 값을 지어내지 않되, 그 행 하나 때문에 나머지 29일치까지 버리지 않도록
    # 해당 행만 건너뛴다(끊긴 하루보다 "말없이 전체 실패"가 더 나쁘다는
    # 판단 — Prime Directive: 창작 금지가 곧 조용한 전체 실패를 정당화하진
    # 않음).
    parsed = []
    skipped_dates = []
    for r in rows:
        d = r[FIELDS["date"]]
        date_str = f"{d[0:4]}-{d[4:6]}-{d[6:8]}"
        try:
            foreign_net_krw = int(r[FIELDS["foreign_net_krw"]]) * KRW_UNIT_MULTIPLIER
            inst_net_krw = int(r[FIELDS["inst_net_krw"]]) * KRW_UNIT_MULTIPLIER
            retail_net_krw = int(r[FIELDS["retail_net_krw"]]) * KRW_UNIT_MULTIPLIER
        except ValueError:
            skipped_dates.append(date_str)
            continue
        parsed.append({
            "date": date_str,
            "ticker": ticker,
            "foreign_net_qty": r[FIELDS["foreign_net_qty"]],
            "inst_net_qty": r[FIELDS["inst_net_qty"]],
            "retail_net_qty": r[FIELDS["retail_net_qty"]],
            "foreign_net_krw": foreign_net_krw,
            "inst_net_krw": inst_net_krw,
            "retail_net_krw": retail_net_krw,
            "source": "kis_api",
            "note": "",
        })
    if skipped_dates:
        print(
            f"[경고] {len(skipped_dates)}개 행(날짜: {', '.join(skipped_dates)})은 "
            "순매수대금 필드가 KIS에서 아직 미정산(빈 문자열)이라 건너뜀 — "
            "보통 조회 당일 장중(정산 전) 조회 시 발생, 장마감 후 재조회하면 채워짐.",
            file=sys.stderr,
        )
    return parsed


def kis_fetch_price(ticker, account_type="real", raw=False, with_snapshot_extra=False):
    """국내주식 현재가 시세(가격/전일대비/등락률/거래량) 조회.
    with_snapshot_extra=True면 외국인 보유율·250일 최고가 대비 등락률도
    함께 반환(snapshot 커맨드 전용, 기존 quote 커맨드는 하위호환 위해 기본값 False)."""
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    token = kis_get_token(account_type)
    host = KIS_HOSTS[account_type]

    params = f"FID_COND_MRKT_DIV_CODE=J&FID_INPUT_ISCD={ticker}"
    req = urllib.request.Request(
        f"{host}/uapi/domestic-stock/v1/quotations/inquire-price?{params}",
        headers={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": appkey,
            "appsecret": appsecret,
            "tr_id": "FHKST01010100",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=KIS_HTTP_TIMEOUT_S) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"KIS API 호출 실패: {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return None

    row = data.get("output")
    if not row:
        sys.exit(
            "API 응답에서 시세 데이터를 찾지 못했습니다 — --raw로 원본 JSON을 "
            "확인하고 이 스크립트의 output 추출 키를 응답 구조에 맞게 고치세요."
        )
    missing = [v for v in PRICE_FIELDS.values() if v not in row]
    if missing:
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다: {missing}. --raw로 원본을 "
            "확인해 이 스크립트 상단 PRICE_FIELDS 딕셔너리를 실제 필드명으로 고치세요."
        )
    result = {
        "ticker": ticker,
        "price": int(row[PRICE_FIELDS["price"]]),
        "change": int(row[PRICE_FIELDS["change"]]),
        "change_pct": float(row[PRICE_FIELDS["change_pct"]]),
        "volume": int(row[PRICE_FIELDS["volume"]]),
    }
    if with_snapshot_extra:
        missing_extra = [v for v in PRICE_SNAPSHOT_EXTRA_FIELDS.values() if v not in row]
        if missing_extra:
            sys.exit(
                f"snapshot 부가 필드가 API 응답에 없습니다: {missing_extra}. 실제 응답 키: "
                f"{sorted(row.keys())}\nPRICE_SNAPSHOT_EXTRA_FIELDS를 고치세요."
            )
        result["foreign_hold_pct"] = float(row[PRICE_SNAPSHOT_EXTRA_FIELDS["foreign_hold_pct"]])
        result["foreign_hold_qty"] = int(row[PRICE_SNAPSHOT_EXTRA_FIELDS["foreign_hold_qty"]])
        result["day250_high"] = int(row[PRICE_SNAPSHOT_EXTRA_FIELDS["day250_high"]])
        d = row[PRICE_SNAPSHOT_EXTRA_FIELDS["day250_high_date"]]
        result["day250_high_date"] = f"{d[0:4]}-{d[4:6]}-{d[6:8]}"
        result["day250_high_vrss_pct"] = float(row[PRICE_SNAPSHOT_EXTRA_FIELDS["day250_high_vrss_pct"]])
    return result


def kis_fetch_overseas_price(symbol, excd="NAS", account_type="real", raw=False):
    """해외상장 종목(ADR 등) 현재가 조회. 국내주식 API보다 검증도가 낮음."""
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    token = kis_get_token(account_type)
    host = KIS_HOSTS[account_type]

    params = f"AUTH=&EXCD={excd}&SYMB={symbol}"
    req = urllib.request.Request(
        f"{host}/uapi/overseas-price/v1/quotations/price-detail?{params}",
        headers={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": appkey,
            "appsecret": appsecret,
            "tr_id": "HHDFS76200200",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=KIS_HTTP_TIMEOUT_S) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"KIS 해외주식 API 호출 실패: {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return None

    row = data.get("output")
    if not row:
        sys.exit(
            "API 응답에서 해외주식 시세를 찾지 못했습니다 — --raw로 원본 JSON을 "
            "확인하고 output 추출 키를 응답 구조에 맞게 고치세요."
        )
    missing = [v for v in OVERSEAS_PRICE_FIELDS.values() if v not in row]
    if missing:
        # 2026-07-28 발견: 이 진단 메시지가 필드명만 나열하고 실제 응답을
        # 보여주지 않아서, sk-hynix-adr-quote.csv가 생성 이래 단 한 번도
        # 채워지지 않은 채로 (adr-quote ... || true)에 조용히 묻혀 있었다.
        # 실제 응답 키를 로그에 함께 남겨 재발 시 --raw 왕복 없이 바로
        # 고칠 수 있게 한다.
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다: {missing}. 실제 응답 키: "
            f"{sorted(row.keys())}\n실제 응답 전체: {json.dumps(row, ensure_ascii=False)}\n"
            "이 스크립트 상단 OVERSEAS_PRICE_FIELDS 딕셔너리를 위 실제 필드명으로 고치세요."
        )
    price = float(row[OVERSEAS_PRICE_FIELDS["price"]])
    prev_close = float(row[OVERSEAS_PRICE_FIELDS["prev_close"]])
    # 응답에 전일대비/등락률 필드가 직접 없어 여기서 계산한다(위 주석 참고).
    change = price - prev_close
    change_pct = (change / prev_close * 100) if prev_close else 0.0
    return {
        "symbol": symbol,
        "price": price,
        "change": change,
        "change_pct": change_pct,
        "prev_close": prev_close,
    }


def kis_fetch_overseas_daily_price(symbol, excd="NAS", account_type="real", raw=False):
    """해외상장 종목(ADR 등)의 **일별 확정 시세**를 조회한다 — 이 저장소의
    자동체크 3회(07:00/10:00/19:00 KST)가 전부 나스닥 정규장(22:30~05:00
    KST) 밖에 있어, 기존 kis_fetch_overseas_price()(실시간 현재가 조회,
    HHDFS76200200)가 장 마감 후 스냅샷을 되돌려주면서 "현재가=전일종가"가
    되어 change_pct가 계속 0.0%으로 찍히던 문제(2026-07-30~31 사용자 지적)
    를 해결하기 위한 함수. 이 TR은 확정된 거래일 종가 시계열을 주므로 호출
    시각과 무관하게 마지막으로 마감된 세션의 정확한 종가·전일대비를 얻을
    수 있다. **이게 ADR 확인의 주(main) 경로**여야 하고, 실시간 현재가는
    미국 장중(22:30~05:00 KST)에만 보조적으로 의미가 있다.
    ⚠ TR HHDFS76240000("해외주식 기간별시세"), 파라미터·필드명은 KIS
    공식문서 기반 최선 추정이며 이 샌드박스는 아웃바운드 네트워크가
    막혀있어 실호출로 검증하지 못했다 — 이 저장소의 다른 TR과 동일한
    원칙대로, 최초 실행 시 --raw로 원본 응답을 반드시 확인하고 output2
    배열의 정렬 순서(최신이 [0]인지 [-1]인지)와 필드명(xymd/clos/diff/rate)이
    다르면 아래 코드를 그에 맞게 고칠 것."""
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    token = kis_get_token(account_type)
    host = KIS_HOSTS[account_type]

    # GUBN=0(일별), BYMD=공백(최근 기준), MODP=0(수정주가 미반영)
    params = f"AUTH=&EXCD={excd}&SYMB={symbol}&GUBN=0&BYMD=&MODP=0"
    req = urllib.request.Request(
        f"{host}/uapi/overseas-price/v1/quotations/dailyprice?{params}",
        headers={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": appkey,
            "appsecret": appsecret,
            "tr_id": "HHDFS76240000",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=KIS_HTTP_TIMEOUT_S) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"KIS 해외주식 일별시세 API 호출 실패: {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return None

    rows = data.get("output2")
    if not rows:
        sys.exit(
            "API 응답에서 일별시세 리스트(output2)를 찾지 못했습니다 — --raw로 "
            "원본 JSON을 확인하고 이 함수의 추출 키를 응답 구조에 맞게 고치세요."
        )
    latest = rows[0]  # 최신순(내림차순) 정렬 가정 — 응답이 과거순이면 rows[-1]로 수정
    required = ["xymd", "clos", "diff"]
    missing = [k for k in required if k not in latest]
    if missing:
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다: {missing}. 실제 응답 키: "
            f"{sorted(latest.keys())}\n실제 응답 전체(최신행): {json.dumps(latest, ensure_ascii=False)}\n"
            "이 함수의 required 필드명을 위 실제 필드명으로 고치세요."
        )
    price = float(latest["clos"])
    change = float(latest["diff"])
    prev_close_same_row = price - change
    trade_date_raw = str(latest["xymd"])  # YYYYMMDD
    trade_date = f"{trade_date_raw[:4]}-{trade_date_raw[4:6]}-{trade_date_raw[6:]}"

    # 2026-08-01 — 3방법 크로스체크 신설. 실계정 검증(2026-07-31)에서
    # diff(+3.10, 상승)와 API의 rate 필드(-2.08%, 하락)가 서로 어긋나는
    # 응답이 실제로 수신됐다 — 어느 한쪽을 그냥 믿는 대신, 서로 독립적인
    # 3가지 방법으로 등락률을 각각 구해서 대조한다(사용자 요청: "3가지
    # 방법이 모두 같으면 확정, 안 맞으면 나한테 보고하고 내가 결정").
    #
    #   A) rate  — API가 자체 계산해 주는 등락률 필드를 그대로 신뢰
    #   B) calc  — 같은 행의 diff·종가로 직접 재계산(prev_close = clos-diff)
    #   C) hist  — 이 응답의 바로 다음 행(output2[1], 즉 전 거래일의
    #              확정 종가)을 독립적인 전일종가로 삼아 재계산 — diff에
    #              전혀 의존하지 않는 유일한 방법이라 A·B가 같은 원인으로
    #              동시에 틀렸을 경우에도 걸러낼 수 있다.
    rate_pct = None
    if "rate" in latest and latest["rate"] not in (None, ""):
        try:
            rate_pct = float(latest["rate"])
        except (TypeError, ValueError):
            rate_pct = None
    calc_pct = (change / prev_close_same_row * 100) if prev_close_same_row else None
    hist_pct = None
    if len(rows) > 1:
        try:
            hist_prev_close = float(rows[1]["clos"])
            if hist_prev_close:
                hist_pct = (price - hist_prev_close) / hist_prev_close * 100
        except (KeyError, TypeError, ValueError):
            hist_pct = None

    methods = {"rate": rate_pct, "calc": calc_pct, "hist": hist_pct}
    available = {k: v for k, v in methods.items() if v is not None}
    detail = "|".join(f"{k}:{v:+.2f}" for k, v in methods.items() if v is not None)

    if len(available) >= 2:
        spread = max(available.values()) - min(available.values())
        if spread <= ADR_CROSSCHECK_TOLERANCE_PCT:
            crosscheck = "OK" if len(available) == 3 else "OK_PARTIAL(2/3)"
            # 합치하면 diff 기반(calc)을 확정치로 채택 — 세 방법 모두 오차
            # 범위 안이므로 어느 걸 골라도 사실상 같지만, diff는 이 응답
            # 자체가 준 값이라 반올림이 가장 덜 누적된 값으로 우선한다.
            change_pct = calc_pct if calc_pct is not None else next(iter(available.values()))
        else:
            crosscheck = "MISMATCH"
            change_pct = None
            print(
                f"⚠️ ADR change_pct 크로스체크 불일치 감지 ({symbol}, {trade_date}): "
                f"{detail} — 자동으로 숫자를 확정하지 않고 change_pct를 비워둡니다. "
                f"{ADR_CSV_PATH.name}의 crosscheck=MISMATCH 행을 확인해 사용자에게 "
                "보고하고 어느 값을 쓸지 결정을 받으세요.",
                file=sys.stderr,
            )
    elif len(available) == 1:
        crosscheck = "PARTIAL_SINGLE(1/3)"
        change_pct = next(iter(available.values()))
    else:
        crosscheck = "NO_METHOD"
        change_pct = None

    return {
        "symbol": symbol,
        "date": trade_date,
        "price": price,
        "change": change,
        "change_pct": change_pct,
        "prev_close": prev_close_same_row,
        "crosscheck": crosscheck,
        "crosscheck_detail": detail,
    }


def kis_fetch_credit_balance(ticker, account_type="real", raw=False):
    """국내주식 신용잔고 일별추이(융자·대주) 조회 — 찐반등 신호①(빚의 청산)의
    데이터 소스. 결제일자(FID_INPUT_DATE_1)를 오늘 날짜로 주면 최근 30건까지
    반환된다."""
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    token = kis_get_token(account_type)
    host = KIS_HOSTS[account_type]

    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    params = (
        f"FID_COND_MRKT_DIV_CODE=J&FID_COND_SCR_DIV_CODE=20476"
        f"&FID_INPUT_ISCD={ticker}&FID_INPUT_DATE_1={today}"
    )
    req = urllib.request.Request(
        f"{host}/uapi/domestic-stock/v1/quotations/daily-credit-balance?{params}",
        headers={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": appkey,
            "appsecret": appsecret,
            "tr_id": "FHPST04760000",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=KIS_HTTP_TIMEOUT_S) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"KIS 신용잔고 API 호출 실패: {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return []

    rows = data.get("output") or []
    if not rows:
        sys.exit(
            "API 응답에서 신용잔고 데이터를 찾지 못했습니다 — --raw로 원본 JSON을 "
            "확인하고 output 추출 키를 응답 구조에 맞게 고치세요."
        )
    missing = [v for v in CREDIT_BALANCE_FIELDS.values() if v not in rows[0]]
    if missing:
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다: {missing}. 실제 응답 키: "
            f"{sorted(rows[0].keys())}\nCREDIT_BALANCE_FIELDS를 위 실제 필드명으로 고치세요."
        )

    parsed = []
    for r in rows:
        d = r[CREDIT_BALANCE_FIELDS["date"]]
        parsed.append({
            "date": f"{d[0:4]}-{d[4:6]}-{d[6:8]}",
            "ticker": ticker,
            "loan_new_qty": r[CREDIT_BALANCE_FIELDS["loan_new_qty"]],
            "loan_redeem_qty": r[CREDIT_BALANCE_FIELDS["loan_redeem_qty"]],
            "loan_balance_qty": r[CREDIT_BALANCE_FIELDS["loan_balance_qty"]],
            "loan_balance_amt": r[CREDIT_BALANCE_FIELDS["loan_balance_amt"]],
            "loan_balance_rate": r[CREDIT_BALANCE_FIELDS["loan_balance_rate"]],
            "short_new_qty": r[CREDIT_BALANCE_FIELDS["short_new_qty"]],
            "short_redeem_qty": r[CREDIT_BALANCE_FIELDS["short_redeem_qty"]],
            "short_balance_qty": r[CREDIT_BALANCE_FIELDS["short_balance_qty"]],
            "short_balance_amt": r[CREDIT_BALANCE_FIELDS["short_balance_amt"]],
            "short_balance_rate": r[CREDIT_BALANCE_FIELDS["short_balance_rate"]],
            "source": "kis_api",
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })
    return parsed


def kis_fetch_index_price(index_code, account_type="real", raw=False):
    """국내업종 현재지수 조회 — 코스피(0001)/코스닥(1001)/코스피200(2001).
    상승/하락/보합/상한/하한 종목수까지 함께 내려와, "코스피 톱5 중 3개
    상한가" 같은 서술을 웹검색 없이 확인할 수 있다."""
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    token = kis_get_token(account_type)
    host = KIS_HOSTS[account_type]

    params = f"FID_COND_MRKT_DIV_CODE=U&FID_INPUT_ISCD={index_code}"
    req = urllib.request.Request(
        f"{host}/uapi/domestic-stock/v1/quotations/inquire-index-price?{params}",
        headers={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": appkey,
            "appsecret": appsecret,
            "tr_id": "FHPUP02100000",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=KIS_HTTP_TIMEOUT_S) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"KIS 지수 API 호출 실패: {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return None

    row = data.get("output")
    if isinstance(row, list):
        row = row[0] if row else None
    if not row:
        sys.exit(
            "API 응답에서 지수 데이터를 찾지 못했습니다 — --raw로 원본 JSON을 "
            "확인하고 output 추출 키를 응답 구조에 맞게 고치세요."
        )
    missing = [v for v in INDEX_FIELDS.values() if v not in row]
    if missing:
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다: {missing}. 실제 응답 키: "
            f"{sorted(row.keys())}\nINDEX_FIELDS를 위 실제 필드명으로 고치세요."
        )
    return {
        "index_code": index_code,
        "index_name": INDEX_NAMES.get(index_code, index_code),
        "price": float(row[INDEX_FIELDS["price"]]),
        "change": float(row[INDEX_FIELDS["change"]]),
        "change_pct": float(row[INDEX_FIELDS["change_pct"]]),
        "advancers": int(row[INDEX_FIELDS["advancers"]]),
        "decliners": int(row[INDEX_FIELDS["decliners"]]),
        "unchanged": int(row[INDEX_FIELDS["unchanged"]]),
        "limit_up": int(row[INDEX_FIELDS["limit_up"]]),
        "limit_down": int(row[INDEX_FIELDS["limit_down"]]),
    }


# 2026-08-15 신설 — scripts/correlation_analysis.py가 수출입동향(월별 %YoY)과
# 대조할 실측 월별 이력이 필요해서 추가. 기존 sk-hynix-price-snapshot.csv·
# kr-index-quote.csv는 2026-07-28부터 매일 쌓이기 시작한 스냅샷이라 아직
# 2주치뿐이고, 4~7월 상관관계는 그걸로 계산할 수 없다. 웹검색으로 월말
# 종가를 찾으려 했으나 namu.wiki·investing.com이 이 환경의 egress
# 프록시에서 차단돼 있고, 검색 스니펫은 "코스피 5월 7천선 돌파" 같은
# 정성적 설명뿐이라 정확한 종가로 신뢰할 수 없었다 — 지어낸 숫자를
# "실측"으로 커밋하지 않는다는 이 저장소의 원칙(8년 묵은 금리를 현재값으로
# 발행했던 사고 이후 확립)에 따라 그 값을 쓰지 않았다.
#
# 대신 이미 이 저장소가 신뢰하는 실제 출처(KIS)에서 월봉을 직접 받는다 —
# TR FHKST03010100(국내주식기간별시세일/주/월/년, inquire-daily-itemchartprice)
# 는 개별 종목·ETF의 과거 캔들을 기간 지정해 반환하고 FID_PERIOD_DIV_CODE=M
# 이 월봉이다.
#
# 2026-08-17 실측으로 확인됨: 지수(코스피, code=0001)는 이 종목용 엔드포인트를
# FID_COND_MRKT_DIV_CODE=U로 불러도 "ERROR INVALID FID_COND_MRKT_DIV_CODE"
# (rt_cd=2, msg_cd=OPSQ2001)로 거부된다 — 애초 주석의 우려("별도 TR이 필요할
# 가능성")가 맞았다. 지수는 완전히 다른 엔드포인트(국내주식업종기간별시세
# 일/주/월/년, inquire-daily-indexchartprice / TR FHKUP03500100)가 필요하다.
# 이 엔드포인트/TR/필드명은 KIS 공식 문서 기억 기반으로 아직 실호출
# 미검증 — 다음 실행에서 --raw로 확인해 틀렸으면 고칠 것(막연히 "됐겠지"로
# 넘기지 않는다, 이 파일의 다른 모든 kis_fetch_*와 동일 원칙).
MONTHLY_PRICE_FIELDS = {
    "date": "stck_bsop_date",   # 영업일자(월봉이면 그 달의 마지막 거래일)
    "close": "stck_clpr",       # 종가
    "open": "stck_oprc",
    "high": "stck_hgpr",
    "low": "stck_lwpr",
    "volume": "acml_vol",
}
# 지수용(업종지수) 필드명 — 종목과 접두어가 다를 가능성이 높음(문서 기억
# 기반, 미검증). date는 종목과 동일한 키를 쓰는 경우가 많아 우선 재사용.
MONTHLY_INDEX_PRICE_FIELDS = {
    "date": "stck_bsop_date",
    "close": "bstp_nmix_prpr",  # 업종지수 현재가(종가)
    "open": "bstp_nmix_oprc",
    "high": "bstp_nmix_hgpr",
    "low": "bstp_nmix_lwpr",
    "volume": "acml_vol",
}


_PERIOD_LABELS = {"D": "일봉", "M": "월봉"}


def kis_fetch_price_history(code, is_index=False, period="M", months=24, account_type="real", raw=False,
                             start_date=None, end_date=None):
    """종목/지수의 일봉/월봉 이력을 조회한다(FID_PERIOD_DIV_CODE=period) —
    correlation_analysis.py의 실측 입력 경로. months는 대략치(월 단위 근사,
    KIS는 일 단위 기간을 받으므로 30일*months로 환산) — start_date/end_date를
    직접 주면 그쪽이 우선한다(kis_fetch_*_price_history_deep이 구간별로
    반복 호출할 때 사용).

    2026-08-17 실측(kis-monthly-depth-probe.yml, period="M"): FID_INPUT_DATE_1~2
    로 넓은 기간(예: 90개월)을 요청해도 응답은 최근 ~50개월로 잘린다 — 기간의
    앞부분이 아니라 뒷부분(최신 쪽)만 채워진다. period="D"도 같은 절단
    증상일 가능성이 높다(미검증 — 실측해서 확인할 것). 그보다 긴 이력이
    필요하면 이 함수를 여러 번, end_date를 과거로 당겨가며 호출해야 한다."""
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    token = kis_get_token(account_type)
    host = KIS_HOSTS[account_type]

    end = end_date or datetime.now(timezone.utc).date()
    start = start_date or (end - timedelta(days=months * 31))

    # 2026-08-17 실측: 지수(0001)를 종목용 엔드포인트+market_div=U로 부르면
    # rt_cd=2 "ERROR INVALID FID_COND_MRKT_DIV_CODE"로 거부됨 — 완전히 다른
    # 엔드포인트/TR이 필요하다(아래 endpoint/tr_id/fields 분기). 이 지수용
    # 분기 자체는 아직 실호출 미검증 — 틀리면 --raw로 확인 후 고칠 것.
    if is_index:
        endpoint = "inquire-daily-indexchartprice"
        tr_id = "FHKUP03500100"
        market_div = "U"
        fields = MONTHLY_INDEX_PRICE_FIELDS
    else:
        endpoint = "inquire-daily-itemchartprice"
        tr_id = "FHKST03010100"
        market_div = "J"
        fields = MONTHLY_PRICE_FIELDS
    params = (
        f"FID_COND_MRKT_DIV_CODE={market_div}&FID_INPUT_ISCD={code}"
        f"&FID_INPUT_DATE_1={start.strftime('%Y%m%d')}&FID_INPUT_DATE_2={end.strftime('%Y%m%d')}"
        f"&FID_PERIOD_DIV_CODE={period}&FID_ORG_ADJ_PRC=0"
    )
    req = urllib.request.Request(
        f"{host}/uapi/domestic-stock/v1/quotations/{endpoint}?{params}",
        headers={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": appkey,
            "appsecret": appsecret,
            "tr_id": tr_id,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=KIS_HTTP_TIMEOUT_S) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"KIS {_PERIOD_LABELS.get(period, period)} API 호출 실패({code}): "
                  f"{e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return None

    rows = data.get("output2")
    if not rows:
        sys.exit(
            f"API 응답에서 {_PERIOD_LABELS.get(period, period)} 리스트(output2)를 찾지 못했습니다"
            f"({code}, endpoint={endpoint}) — "
            f"rt_cd={data.get('rt_cd')} msg_cd={data.get('msg_cd')} msg1={data.get('msg1')!r}. "
            "--raw로 원본 JSON을 확인하고 이 함수의 endpoint/tr_id/추출 키를 응답 구조에 맞게 고치세요."
        )
    missing = [v for v in fields.values() if v not in rows[0]]
    if missing:
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다({code}): {missing}. 실제 응답 키: "
            f"{sorted(rows[0].keys())}\n"
            f"{'MONTHLY_INDEX_PRICE_FIELDS' if is_index else 'MONTHLY_PRICE_FIELDS'}를 "
            "위 실제 필드명으로 고치세요."
        )
    out = []
    for r in rows:
        d = r[fields["date"]]
        out.append({
            "date": f"{d[0:4]}-{d[4:6]}-{d[6:8]}",
            "close": float(r[fields["close"]]),
        })
    out.sort(key=lambda row: row["date"])
    return out


def kis_fetch_monthly_price_history(code, is_index=False, months=24, account_type="real", raw=False,
                                     start_date=None, end_date=None):
    """kis_fetch_price_history(period="M")의 하위호환 진입점 — 기존 호출부
    (cmd_monthly_history 등)를 그대로 둔 채 일봉 지원을 추가하기 위한 얇은
    래퍼."""
    return kis_fetch_price_history(code, is_index=is_index, period="M", months=months,
                                    account_type=account_type, raw=raw,
                                    start_date=start_date, end_date=end_date)


def _backward_date_windows(end_date, target_start_date, months_per_window=45, days_per_window=None):
    """end_date에서 target_start_date까지, end를 과거로 당겨가며 겹치지 않는
    (start, end) 날짜 구간 리스트를 만든다. kis_fetch_price_history가 1회
    호출당 최근 구간만(월봉은 ~50개월, 2026-08-17 실측) 잘려서 오는 문제를
    우회하기 위한 분할 — customs_trade.py의 _year_windows()와 같은 목적,
    다른 제약(달력 연도가 아니라 대략적인 기간).

    days_per_window를 주면 그쪽이 우선한다(일봉 backfill처럼 "개월" 단위가
    안 맞는 경우용) — 안 주면 기존처럼 months_per_window*31일로 환산."""
    if days_per_window is None:
        days_per_window = months_per_window * 31
    windows = []
    cur_end = end_date
    while cur_end >= target_start_date:
        cur_start = cur_end - timedelta(days=days_per_window)
        if cur_start < target_start_date:
            cur_start = target_start_date
        windows.append((cur_start, cur_end))
        if cur_start <= target_start_date:
            break
        cur_end = cur_start - timedelta(days=1)
    return windows


def kis_fetch_monthly_price_history_deep(code, is_index=False, account_type="real",
                                          start_date=None, months_per_window=45):
    """kis_fetch_monthly_price_history를 여러 번(과거로 구간을 당겨가며) 호출해
    start_date까지의 월봉을 채운다 — 1회 호출은 최근 ~50개월로 잘리므로
    (2026-08-17 실측, kis-monthly-depth-probe.yml) 장기 이력은 이 함수가
    필요하다. 최초 1회성 backfill 용도 — 평소 매일 갱신은 여전히
    kis_fetch_monthly_price_history(months=24)만으로 충분하다."""
    # 2026-08-17 실측(kis-old-history-probe.yml): 코스피(0001) 월봉은 실제로
    # 1983-01(지수 출범 시점, 118.27)까지 실측이 나온다 — 2019-01은 KIS의
    # 하드 제약이 아니라 이 저장소가 (사용자의 첫 요청 "2019년부터"를 따라)
    # 임의로 고른 값이었을 뿐이다. 종목(예: 하이닉스)은 상장일 이전엔 당연히
    # 데이터가 없으므로, 기본값을 넉넉히 옛날로 잡고 실제 상장/출범 이전
    # 구간은 아래 빈 응답 처리로 자연히 멈추게 한다.
    if start_date is None:
        start_date = date(1980, 1, 1)
    end_date = datetime.now(timezone.utc).date()
    windows = _backward_date_windows(end_date, start_date, months_per_window)
    merged = {}
    for win_start, win_end in windows:
        try:
            rows = kis_fetch_monthly_price_history(
                code, is_index=is_index, account_type=account_type,
                start_date=win_start, end_date=win_end,
            )
        except SystemExit as e:
            # kis_fetch_monthly_price_history는 output2가 비어 있으면
            # sys.exit한다 — 상장/출범 이전 구간을 요청했을 때(정상적으로
            # 데이터가 없는 경우)도 같은 방식으로 실패한다. 여기서는 그걸
            # "더 과거로 갈 수 없는 경계에 도달했다"는 신호로 보고 조용히
            # 멈춘다(에러를 삼키지는 않음 — stderr에 남긴다) — 나머지(더
            # 과거) 구간을 계속 두드리는 건 낭비이고, 진짜 API 에러였어도
            # 이미 모은 구간까지는 유효하다.
            print(f"[stop] {code} {win_start}~{win_end}: {e} — 더 과거로는 데이터가 "
                  "없거나 호출 실패로 보고 여기서 멈춘다", file=sys.stderr)
            break
        for r in rows:
            merged[r["date"]] = r
    return sorted(merged.values(), key=lambda r: r["date"])


def kis_fetch_daily_price_history_deep(code, is_index=False, account_type="real",
                                        start_date=None, days_per_window=60):
    """kis_fetch_price_history(period="D")를 여러 번(과거로 구간을 당겨가며)
    호출해 start_date까지의 일봉을 채운다 — 2026-08-17 사용자 요청: 수출입
    지표는 월별이 원 주기지만 주가/지수는 매일 발표되므로, 그 주기 그대로
    (일봉) 써야 "더 자주 발표되는 지표가 다른 지표를 선행해서 보인다"가
    실제로 성립한다(월봉으로 뭉개면 그 정보가 사라진다).

    kis_fetch_monthly_price_history_deep과 같은 구조 — 1회 호출당 최근
    구간으로 잘리는 문제(2026-08-17 kis-daily-period-probe.yml 실측:
    200일 요청 시 종목은 최근 100행, 지수는 최근 50행까지만 옴 — 지수 쪽이
    더 좁다). days_per_window=60(약 42거래일)은 두 쪽 모두의 캡보다
    확실히 작게 잡은 값. 상장/출범 이전 구간은 kis_fetch_monthly_price_history_deep
    과 동일하게 빈 응답으로 자연히 멈춘다."""
    if start_date is None:
        start_date = date(2023, 1, 1)
    end_date = datetime.now(timezone.utc).date()
    windows = _backward_date_windows(end_date, start_date, days_per_window=days_per_window)
    merged = {}
    for win_start, win_end in windows:
        try:
            rows = kis_fetch_price_history(
                code, is_index=is_index, period="D", account_type=account_type,
                start_date=win_start, end_date=win_end,
            )
        except SystemExit as e:
            print(f"[stop] {code} {win_start}~{win_end}: {e} — 더 과거로는 데이터가 "
                  "없거나 호출 실패로 보고 여기서 멈춘다", file=sys.stderr)
            break
        for r in rows:
            merged[r["date"]] = r
    return sorted(merged.values(), key=lambda r: r["date"])


def kis_fetch_short_sale(ticker, account_type="real", raw=False):
    """국내주식 공매도 일별추이 조회."""
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    token = kis_get_token(account_type)
    host = KIS_HOSTS[account_type]

    params = f"FID_COND_MRKT_DIV_CODE=J&FID_INPUT_ISCD={ticker}&FID_INPUT_DATE_1=&FID_INPUT_DATE_2="
    req = urllib.request.Request(
        f"{host}/uapi/domestic-stock/v1/quotations/daily-short-sale?{params}",
        headers={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": appkey,
            "appsecret": appsecret,
            "tr_id": "FHPST04830000",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=KIS_HTTP_TIMEOUT_S) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"KIS 공매도 API 호출 실패: {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return []

    # output2가 일별 리스트(open-trading-api 예제 기준) — output1은 최신 단건 요약으로 추정.
    rows = data.get("output2") or data.get("output1") or []
    if not rows:
        sys.exit(
            "API 응답에서 공매도 데이터를 찾지 못했습니다 — --raw로 원본 JSON을 "
            "확인하고 output1/output2 추출 키를 응답 구조에 맞게 고치세요."
        )
    missing = [v for v in SHORT_SALE_FIELDS.values() if v not in rows[0]]
    if missing:
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다: {missing}. 실제 응답 키: "
            f"{sorted(rows[0].keys())}\nSHORT_SALE_FIELDS를 위 실제 필드명으로 고치세요."
        )

    parsed = []
    for r in rows:
        d = r[SHORT_SALE_FIELDS["date"]]
        parsed.append({
            "date": f"{d[0:4]}-{d[4:6]}-{d[6:8]}",
            "ticker": ticker,
            "short_qty": r[SHORT_SALE_FIELDS["short_qty"]],
            "short_vol_pct": r[SHORT_SALE_FIELDS["short_vol_pct"]],
            "cum_short_qty": r[SHORT_SALE_FIELDS["cum_short_qty"]],
            "cum_short_vol_pct": r[SHORT_SALE_FIELDS["cum_short_vol_pct"]],
            "short_amt": r[SHORT_SALE_FIELDS["short_amt"]],
            "source": "kis_api",
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })
    return parsed


def kis_fetch_etf_nav(ticker, account_type="real", raw=False):
    """ETF/ETN 현재가+NAV+괴리율 조회 — 포트폴리오 보유 ETF 점검용."""
    appkey = _get_env_or_die("KIS_APP_KEY")
    appsecret = _get_env_or_die("KIS_APP_SECRET")
    token = kis_get_token(account_type)
    host = KIS_HOSTS[account_type]

    params = f"FID_COND_MRKT_DIV_CODE=J&FID_INPUT_ISCD={ticker}"
    req = urllib.request.Request(
        f"{host}/uapi/etfetn/v1/quotations/inquire-price?{params}",
        headers={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": appkey,
            "appsecret": appsecret,
            "tr_id": "FHPST02400000",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=KIS_HTTP_TIMEOUT_S) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"KIS ETF API 호출 실패: {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return None

    row = data.get("output")
    if not row:
        sys.exit(
            "API 응답에서 ETF 데이터를 찾지 못했습니다 — --raw로 원본 JSON을 "
            "확인하고 output 추출 키를 응답 구조에 맞게 고치세요."
        )
    missing = [v for v in ETF_NAV_FIELDS.values() if v not in row]
    if missing:
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다: {missing}. 실제 응답 키: "
            f"{sorted(row.keys())}\nETF_NAV_FIELDS를 위 실제 필드명으로 고치세요."
        )
    return {
        "ticker": ticker,
        "price": float(row[ETF_NAV_FIELDS["price"]]),
        "nav": float(row[ETF_NAV_FIELDS["nav"]]),
        "nav_change": float(row[ETF_NAV_FIELDS["nav_change"]]),
        "nav_change_pct": float(row[ETF_NAV_FIELDS["nav_change_pct"]]),
        "tracking_error_pct": float(row[ETF_NAV_FIELDS["tracking_error_pct"]]),
        "divergence_pct": float(row[ETF_NAV_FIELDS["divergence_pct"]]),
    }


def _generic_upsert(csv_path, fields, key_fields, rows_by_new, extra=None):
    """credit-balance/short-sale/index-quote/etf-nav 공용 append-only CSV 갱신
    헬퍼 — 기존 _read_csv/_write_csv와 같은 패턴이나 파일·키가 매번 달라 범용화."""
    existing = {}
    if csv_path.exists():
        with csv_path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                existing[tuple(row[k] for k in key_fields)] = row
    for r in rows_by_new:
        row = {k: r.get(k, "") for k in fields}
        if extra:
            row.update(extra)
        existing[tuple(row[k] for k in key_fields)] = row
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(existing.values(), key=lambda r: tuple(r[k] for k in key_fields))
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in ordered:
            w.writerow(r)
    return len(rows_by_new)


def _read_adr_csv():
    if not ADR_CSV_PATH.exists():
        return {}
    rows = {}
    with ADR_CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[(row["date"], row["symbol"])] = row
    return rows


def _write_adr_csv(rows_by_key):
    ADR_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows_by_key.values(), key=lambda r: (r["date"], r["symbol"]))
    # restval="" — 2026-08-01에 crosscheck/crosscheck_detail 컬럼을 새로
    # 추가하기 전에 기록된 옛 행에는 이 키들이 아예 없다. 그대로 두면
    # DictWriter가 ValueError를 내므로 빈 문자열로 채워 하위호환한다.
    with ADR_CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ADR_CSV_FIELDS, restval="")
        w.writeheader()
        for r in ordered:
            w.writerow(r)


def upsert_adr_row(quote, source="kis_api"):
    existing = _read_adr_csv()
    # 일별시세(daily) 응답은 실제 거래일(quote["date"])을 주므로 그걸 키로
    # 쓴다 — 예전엔 항상 "오늘(UTC)" 날짜로 덮어써서, 예를 들어 KST 아침에
    # 조회한 게 실제로는 그제 미국장 마감분이어도 "오늘" 행으로 잘못
    # 기록됐다. 실시간 현재가(intraday) 경로처럼 거래일 정보가 없는
    # 경우에만 UTC 오늘 날짜로 폴백한다.
    row_date = quote.get("date") or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    key = (row_date, quote["symbol"])
    # crosscheck/crosscheck_detail — kis_fetch_overseas_daily_price()(일별
    # 확정시세 경로)만 채운다. 실시간현재가(intraday) 경로는 방법이 하나뿐
    # (price-prev_close 직접계산)이라 대조할 다른 방법이 없으므로 "N/A"로
    # 명시해 크로스체크를 아예 안 거쳤다는 걸 숨기지 않는다.
    existing[key] = {
        "date": row_date, "symbol": quote["symbol"],
        "price": quote["price"], "change": quote["change"],
        "change_pct": quote["change_pct"], "prev_close": quote["prev_close"],
        "crosscheck": quote.get("crosscheck", "N/A_INTRADAY"),
        "crosscheck_detail": quote.get("crosscheck_detail", ""),
        "source": source, "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    _write_adr_csv(existing)


def read_latest_adr(symbol):
    """가장 최근 fetched_at 기준 ADR 기록 1건 반환(없으면 None) — 다른 스크립트 재사용용."""
    rows = [r for (d, s), r in _read_adr_csv().items() if s == symbol]
    if not rows:
        return None
    rows.sort(key=lambda r: r["fetched_at"])
    return rows[-1]


def _read_price_snapshot_csv():
    if not PRICE_SNAPSHOT_CSV_PATH.exists():
        return {}
    rows = {}
    with PRICE_SNAPSHOT_CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[(row["date"], row["ticker"])] = row
    return rows


def _write_price_snapshot_csv(rows_by_key):
    PRICE_SNAPSHOT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows_by_key.values(), key=lambda r: (r["date"], r["ticker"]))
    with PRICE_SNAPSHOT_CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=PRICE_SNAPSHOT_CSV_FIELDS)
        w.writeheader()
        for r in ordered:
            w.writerow(r)


def upsert_price_snapshot_row(q, source="kis_api"):
    existing = _read_price_snapshot_csv()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    key = (today, q["ticker"])
    existing[key] = {
        "date": today, "ticker": q["ticker"],
        "price": q["price"], "change": q["change"], "change_pct": q["change_pct"], "volume": q["volume"],
        "foreign_hold_pct": q["foreign_hold_pct"], "foreign_hold_qty": q["foreign_hold_qty"],
        "day250_high": q["day250_high"], "day250_high_date": q["day250_high_date"],
        "day250_high_vrss_pct": q["day250_high_vrss_pct"],
        "source": source, "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    _write_price_snapshot_csv(existing)


def read_latest_price_snapshot(ticker):
    """가장 최근 fetched_at 기준 스냅샷 1건 반환(없으면 None) — 다른 스크립트 재사용용."""
    rows = [r for (d, t), r in _read_price_snapshot_csv().items() if t == ticker]
    if not rows:
        return None
    rows.sort(key=lambda r: r["fetched_at"])
    return rows[-1]


def read_price_snapshot_rows(ticker):
    """스냅샷 CSV에서 해당 종목 행만 날짜순 정렬 — 외국인보유율 추세(daily_report.py
    HBM 축 채점) 계산용. 2026-08-05 신설."""
    rows = [r for (d, t), r in _read_price_snapshot_csv().items() if t == ticker]
    rows.sort(key=lambda r: r["date"])
    return rows


def foreign_hold_pct_trend(ticker, days=5):
    """외국인 보유율(%)의 최근 N일 스냅샷과, 최신 1건의 전일 대비 %p 변화를 반환.
    2026-08-05 신설 — HBM Cycle Score "외국인 보유율 변화(전일 대비 %p)" 축(15점,
    hbm-cycle-score.md "1." 참고)을 매일 웹검색/수기 판단 없이 스냅샷 CSV만으로
    채점하기 위한 헬퍼. 스냅샷이 매일 쌓이지 않으면(휴장일 등) None을 반환 —
    값을 지어내지 않는다."""
    rows = read_price_snapshot_rows(ticker)
    if len(rows) < 2:
        return {"trend": [], "latest_change_pp": None}
    recent = rows[-days:] if len(rows) >= days else rows
    trend = [(r["date"], float(r["foreign_hold_pct"])) for r in recent]
    latest_change_pp = trend[-1][1] - trend[-2][1] if len(trend) >= 2 else None
    return {"trend": trend, "latest_change_pp": latest_change_pp}


def read_credit_balance_rows(ticker):
    """신용잔고 CSV에서 해당 종목 행만 날짜순 정렬. 2026-08-05 신설."""
    if not CREDIT_BALANCE_CSV_PATH.exists():
        return []
    rows = []
    with CREDIT_BALANCE_CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["ticker"] == ticker:
                rows.append(row)
    rows.sort(key=lambda r: r["date"])
    return rows


def credit_balance_streak(ticker):
    """융자잔고(loan_balance_qty) N거래일 연속 증가/감소 판정. 2026-08-05 신설 —
    그동안 daily 체크에서 "3거래일 연속 감소 확정" 같은 판단을 사람이 CSV를
    눈으로 훑어 손으로 세던 것을 대체. 데이터 2건 미만이면 미확인."""
    rows = read_credit_balance_rows(ticker)
    if len(rows) < 2:
        return {"direction": None, "streak_days": 0, "latest": rows[-1] if rows else None}
    qtys = [int(r["loan_balance_qty"]) for r in rows]
    latest = rows[-1]
    diffs = [qtys[i] - qtys[i - 1] for i in range(1, len(qtys))]
    last_sign = 1 if diffs[-1] > 0 else (-1 if diffs[-1] < 0 else 0)
    streak = 0
    for d in reversed(diffs):
        sign = 1 if d > 0 else (-1 if d < 0 else 0)
        if sign == last_sign and sign != 0:
            streak += 1
        else:
            break
    direction = {1: "증가", -1: "감소", 0: "보합"}.get(last_sign)
    return {"direction": direction, "streak_days": streak, "latest": latest}


def read_latest_short_sale(ticker):
    """공매도 CSV에서 해당 종목 최신 행. 2026-08-05 신설."""
    if not SHORT_SALE_CSV_PATH.exists():
        return None
    rows = []
    with SHORT_SALE_CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["ticker"] == ticker:
                rows.append(row)
    if not rows:
        return None
    rows.sort(key=lambda r: r["date"])
    return rows[-1]


def read_short_sale_rows(ticker):
    """공매도 CSV에서 해당 종목 행만 날짜순 정렬 — 1개월 추이 계산용(daily_report.py).
    2026-09-01 신설."""
    if not SHORT_SALE_CSV_PATH.exists():
        return []
    rows = []
    with SHORT_SALE_CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["ticker"] == ticker:
                rows.append(row)
    rows.sort(key=lambda r: r["date"])
    return rows


def read_latest_index(index_code):
    """지수 CSV에서 해당 업종코드 최신 행(코스피=0001/코스닥=1001/코스피200=2001).
    2026-08-05 신설."""
    if not INDEX_CSV_PATH.exists():
        return None
    rows = []
    with INDEX_CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["index_code"] == index_code:
                rows.append(row)
    if not rows:
        return None
    rows.sort(key=lambda r: r["date"])
    return rows[-1]


def read_index_rows(index_code):
    """지수 CSV에서 해당 업종코드 행만 날짜순 정렬 — 1개월 추이 계산용(daily_report.py).
    2026-09-01 신설."""
    if not INDEX_CSV_PATH.exists():
        return []
    rows = []
    with INDEX_CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["index_code"] == index_code:
                rows.append(row)
    rows.sort(key=lambda r: r["date"])
    return rows


def read_ticker_rows(ticker):
    """CSV에서 해당 종목 행만 날짜순으로 정렬해 반환 — 다른 스크립트에서도 재사용."""
    rows = [r for (d, t), r in _read_csv().items() if t == ticker]
    rows.sort(key=lambda r: r["date"])
    return rows


def summarize_flows(rows, windows=(1, 5, 20, 60)):
    """윈도우별 외국인/기관/개인 누적 순매수(원). 데이터 부족한 윈도우는 None."""
    out = {}
    for window in windows:
        chunk = rows[-window:]
        if len(chunk) < window:
            out[window] = None
            continue
        window_result = {}
        for label, key in (("foreign", "foreign_net_krw"), ("inst", "inst_net_krw"), ("retail", "retail_net_krw")):
            vals = [int(r[key]) for r in chunk if r[key] not in ("", None)]
            window_result[label] = sum(vals) if len(vals) == len(chunk) else None
        out[window] = window_result
    return out


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


def cmd_quote(args):
    q = kis_fetch_price(args.ticker, args.account_type, raw=args.raw)
    if args.raw:
        return
    flag = " 🚨 급변동(5%+)" if abs(q["change_pct"]) >= 5 else ""
    print(f"{q['ticker']}  {q['price']:,}원  {q['change']:+,}({q['change_pct']:+.2f}%){flag}  거래량 {q['volume']:,}주")


def cmd_snapshot(args):
    q = kis_fetch_price(args.ticker, args.account_type, raw=args.raw, with_snapshot_extra=True)
    if args.raw:
        return
    upsert_price_snapshot_row(q)
    print(
        f"{q['ticker']}  {q['price']:,}원({q['change_pct']:+.2f}%)  "
        f"외국인보유율 {q['foreign_hold_pct']:.2f}%  "
        f"250일최고 {q['day250_high']:,}원({q['day250_high_date']}, 대비 {q['day250_high_vrss_pct']:+.2f}%)  "
        f"→ {PRICE_SNAPSHOT_CSV_PATH}에 기록"
    )


def cmd_adr_quote(args):
    # 2026-07-31부터 기본 경로를 일별 확정시세(daily)로 전환 — 이 저장소의
    # 자동체크 3회가 전부 나스닥 정규장 밖 시각이라, 실시간 현재가(intraday)
    # 경로는 "현재가=전일종가"인 마감 스냅샷만 돌려줘 change_pct가 계속
    # 0.0%으로 찍히는 문제가 있었다. --intraday를 명시하면 예전 실시간
    # 경로(미국 장중 디버깅용)를 그대로 쓸 수 있다.
    if args.intraday:
        q = kis_fetch_overseas_price(args.symbol, args.excd, args.account_type, raw=args.raw)
    else:
        q = kis_fetch_overseas_daily_price(args.symbol, args.excd, args.account_type, raw=args.raw)
    if args.raw:
        return
    upsert_adr_row(q)
    date_note = f" [{q['date']} 거래일]" if q.get("date") else ""
    if q["change_pct"] is None:
        # 크로스체크 불일치 — 숫자를 지어내지 않고 있는 그대로 눈에 띄게
        # 보고한다. GitHub Actions 로그에도 남아 다음 사람이 놓치지 않는다.
        print(
            f"⚠️ {q['symbol']}  ${q['price']:,.2f}  전일종가 ${q['prev_close']:,.2f}{date_note}  "
            f"— change_pct 크로스체크 불일치(MISMATCH), 값 미확정: {q.get('crosscheck_detail', '')}  "
            f"→ {ADR_CSV_PATH}에 crosscheck=MISMATCH로 기록. 사용자에게 보고하고 결정 받을 것."
        )
        return
    flag = " 🚨 급변동(5%+)" if abs(q["change_pct"]) >= 5 else ""
    cc_note = f" [크로스체크 {q['crosscheck']}]" if q.get("crosscheck") else ""
    print(f"{q['symbol']}  ${q['price']:,.2f}  {q['change']:+,.2f}({q['change_pct']:+.2f}%){flag}  전일종가 ${q['prev_close']:,.2f}{date_note}{cc_note}  → {ADR_CSV_PATH}에 기록")


def cmd_credit_balance(args):
    rows = kis_fetch_credit_balance(args.ticker, args.account_type, raw=args.raw)
    if args.raw:
        return
    n = _generic_upsert(CREDIT_BALANCE_CSV_PATH, CREDIT_BALANCE_CSV_FIELDS, ("date", "ticker"), rows,
                         extra={"source": "kis_api", "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    latest = rows[-1] if rows else None
    if latest:
        print(f"{args.ticker} 신용잔고: 융자잔고 {int(latest['loan_balance_qty']):,}주(비율 {latest['loan_balance_rate']}%), "
              f"대주잔고 {int(latest['short_balance_qty']):,}주(비율 {latest['short_balance_rate']}%) → {CREDIT_BALANCE_CSV_PATH}에 {n}건 기록")


def cmd_index_quote(args):
    q = kis_fetch_index_price(args.index_code, args.account_type, raw=args.raw)
    if args.raw:
        return
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    row = {
        "date": today, "index_code": q["index_code"], "index_name": q["index_name"],
        "price": q["price"], "change": q["change"], "change_pct": q["change_pct"],
        "advancers": q["advancers"], "decliners": q["decliners"], "unchanged": q["unchanged"],
        "limit_up": q["limit_up"], "limit_down": q["limit_down"],
    }
    _generic_upsert(INDEX_CSV_PATH, INDEX_CSV_FIELDS, ("date", "index_code"), [row],
                     extra={"source": "kis_api", "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    print(f"{q['index_name']}  {q['price']:,.2f}  {q['change']:+,.2f}({q['change_pct']:+.2f}%)  "
          f"상승{q['advancers']}/하락{q['decliners']}/보합{q['unchanged']}  상한{q['limit_up']}/하한{q['limit_down']}  → {INDEX_CSV_PATH}에 기록")


def cmd_monthly_history(args):
    if args.start:
        if args.raw:
            sys.exit("--start와 --raw는 함께 쓸 수 없습니다(--raw는 단일 호출 원본 확인용).")
        start_date = datetime.strptime(args.start, "%Y-%m-%d").date()
        rows = kis_fetch_monthly_price_history_deep(
            args.code, is_index=args.is_index, account_type=args.account_type,
            start_date=start_date,
        )
    else:
        rows = kis_fetch_monthly_price_history(
            args.code, is_index=args.is_index, months=args.months,
            account_type=args.account_type, raw=args.raw,
        )
    if args.raw:
        return
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    label = INDEX_NAMES.get(args.code, args.code) if args.is_index else (args.label or args.code)
    csv_rows = [{"date": r["date"], "code": args.code, "label": label, "close": r["close"]} for r in rows]
    n = _generic_upsert(MONTHLY_PRICE_CSV_PATH, MONTHLY_PRICE_CSV_FIELDS, ("date", "code"), csv_rows,
                         extra={"source": "kis_api", "fetched_at": fetched_at})
    print(f"{label} ({args.code}): {n}개 월봉 → {MONTHLY_PRICE_CSV_PATH}에 기록 "
          f"(범위 {rows[0]['date']} ~ {rows[-1]['date']})")


def cmd_daily_history(args):
    """monthly-history와 같은 구조, 일봉(period="D")용. --start를 주면 깊게
    (여러 구간 호출) backfill, 아니면 --days만큼 최근만."""
    if args.start:
        if args.raw:
            sys.exit("--start와 --raw는 함께 쓸 수 없습니다(--raw는 단일 호출 원본 확인용).")
        start_date = datetime.strptime(args.start, "%Y-%m-%d").date()
        rows = kis_fetch_daily_price_history_deep(
            args.code, is_index=args.is_index, account_type=args.account_type,
            start_date=start_date,
        )
    else:
        end = datetime.now(timezone.utc).date()
        start = end - timedelta(days=args.days)
        if args.raw:
            kis_fetch_price_history(args.code, is_index=args.is_index, period="D",
                                     account_type=args.account_type, raw=True,
                                     start_date=start, end_date=end)
            return
        rows = kis_fetch_price_history(args.code, is_index=args.is_index, period="D",
                                        account_type=args.account_type,
                                        start_date=start, end_date=end)
    if args.raw:
        return
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    label = INDEX_NAMES.get(args.code, args.code) if args.is_index else (args.label or args.code)
    csv_rows = [{"date": r["date"], "code": args.code, "label": label, "close": r["close"]} for r in rows]
    n = _generic_upsert(DAILY_PRICE_CSV_PATH, DAILY_PRICE_CSV_FIELDS, ("date", "code"), csv_rows,
                         extra={"source": "kis_api", "fetched_at": fetched_at})
    print(f"{label} ({args.code}): {n}개 일봉 → {DAILY_PRICE_CSV_PATH}에 기록 "
          f"(범위 {rows[0]['date']} ~ {rows[-1]['date']})")


def cmd_short_sale(args):
    rows = kis_fetch_short_sale(args.ticker, args.account_type, raw=args.raw)
    if args.raw:
        return
    n = _generic_upsert(SHORT_SALE_CSV_PATH, SHORT_SALE_CSV_FIELDS, ("date", "ticker"), rows,
                         extra={"source": "kis_api", "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    latest = rows[-1] if rows else None
    if latest:
        print(f"{args.ticker} 공매도: 당일 {int(latest['short_qty']):,}주(비중 {latest['short_vol_pct']}%), "
              f"누적 {int(latest['cum_short_qty']):,}주 → {SHORT_SALE_CSV_PATH}에 {n}건 기록")


def cmd_etf_nav(args):
    q = kis_fetch_etf_nav(args.ticker, args.account_type, raw=args.raw)
    if args.raw:
        return
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    row = {
        "date": today, "ticker": q["ticker"], "price": q["price"], "nav": q["nav"],
        "nav_change": q["nav_change"], "nav_change_pct": q["nav_change_pct"],
        "tracking_error_pct": q["tracking_error_pct"], "divergence_pct": q["divergence_pct"],
    }
    _generic_upsert(ETF_NAV_CSV_PATH, ETF_NAV_CSV_FIELDS, ("date", "ticker"), [row],
                     extra={"source": "kis_api", "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    print(f"{q['ticker']}  현재가 {q['price']:,.0f}  NAV {q['nav']:,.2f}({q['nav_change_pct']:+.2f}%)  "
          f"추적오차 {q['tracking_error_pct']:.2f}%  괴리율 {q['divergence_pct']:+.2f}%  → {ETF_NAV_CSV_PATH}에 기록")


def cmd_show(args):
    existing = read_ticker_rows(args.ticker)
    if not existing:
        print(f"{args.ticker} 기록 없음 — fetch나 append로 먼저 데이터를 채우세요.")
        return

    tail = existing[-args.last:]
    print(f"=== {args.ticker} 최근 {len(tail)}일 ===")
    for r in tail:
        print(f"{r['date']}  외인 {r['foreign_net_krw']:>15}원 ({r['foreign_net_qty']:>10}주)  "
              f"기관 {r['inst_net_krw']:>15}원  개인 {r['retail_net_krw']:>15}원  [{r['source']}]")

    print("\n=== 누적 순매수(원) ===")
    label_ko = {"foreign": "외국인", "inst": "기관", "retail": "개인"}
    for window, result in summarize_flows(existing).items():
        if result is None:
            print(f"{window}일 누적: 미확인 — {window}영업일치 기록 부족")
            continue
        for key, ko in label_ko.items():
            v = result[key]
            print(f"{window}일 {ko}: {'미확인' if v is None else f'{v:+,}원'}")


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

    pq = sub.add_parser("quote", help="증권사 API로 현재가/전일대비/등락률 조회")
    pq.add_argument("--ticker", default="000660")
    pq.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    pq.add_argument("--raw", action="store_true")
    pq.set_defaults(func=cmd_quote)

    psn = sub.add_parser("snapshot", help="현재가+외국인보유율+250일최고가 조회, sources/sk-hynix-price-snapshot.csv에 기록")
    psn.add_argument("--ticker", default="000660")
    psn.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    psn.add_argument("--raw", action="store_true")
    psn.set_defaults(func=cmd_snapshot)

    pa2 = sub.add_parser("adr-quote", help="ADR(해외상장) 시세 조회(기본: 일별 확정시세), sources/sk-hynix-adr-quote.csv에 기록")
    pa2.add_argument("--symbol", default="SKHY")
    pa2.add_argument("--excd", default="NAS", help="거래소 코드(NASDAQ=NAS)")
    pa2.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    pa2.add_argument("--raw", action="store_true")
    pa2.add_argument("--intraday", action="store_true", help="일별 확정시세 대신 실시간 현재가 조회(미국 장중 22:30~05:00 KST에서만 의미 있음)")
    pa2.set_defaults(func=cmd_adr_quote)

    pcb = sub.add_parser("credit-balance", help="신용융자잔고(융자/대주) 조회, sources/sk-hynix-credit-balance.csv에 기록 — 찐반등 신호① 데이터소스")
    pcb.add_argument("--ticker", default="000660")
    pcb.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    pcb.add_argument("--raw", action="store_true")
    pcb.set_defaults(func=cmd_credit_balance)

    pix = sub.add_parser("index-quote", help="코스피/코스닥 지수 현재가+등락종목수 조회, sources/kr-index-quote.csv에 기록")
    pix.add_argument("--index-code", default="0001", help="코스피=0001, 코스닥=1001, 코스피200=2001")
    pix.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    pix.add_argument("--raw", action="store_true")
    pix.set_defaults(func=cmd_index_quote)

    pmh = sub.add_parser("monthly-history", help="종목/지수 월봉 이력 조회, sources/monthly-price-history.csv에 기록")
    pmh.add_argument("--code", required=True, help="종목코드(예: 000660) 또는 지수코드(예: 0001=코스피)")
    pmh.add_argument("--is-index", action="store_true", help="code가 지수코드면 지정")
    pmh.add_argument("--label", default=None, help="종목일 때 표시용 이름(예: SK하이닉스). 지수는 INDEX_NAMES에서 자동")
    pmh.add_argument("--months", type=int, default=24, help="조회할 개월 수(근사, --start 미지정시)")
    pmh.add_argument("--start", default=None,
                      help="YYYY-MM-DD — 지정하면 이 날짜까지 여러 번 호출해 깊게 채운다"
                           "(최초 1회성 backfill용, --months 무시, 1회 호출 최근 ~50개월 절단 우회)")
    pmh.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    pmh.add_argument("--raw", action="store_true")
    pmh.set_defaults(func=cmd_monthly_history)

    pdh = sub.add_parser("daily-history", help="종목/지수 일봉 이력 조회, sources/daily-price-history.csv에 기록")
    pdh.add_argument("--code", required=True, help="종목코드(예: 000660) 또는 지수코드(예: 0001=코스피)")
    pdh.add_argument("--is-index", action="store_true", help="code가 지수코드면 지정")
    pdh.add_argument("--label", default=None, help="종목일 때 표시용 이름(예: SK하이닉스). 지수는 INDEX_NAMES에서 자동")
    pdh.add_argument("--days", type=int, default=60, help="조회할 최근 일수(--start 미지정시)")
    pdh.add_argument("--start", default=None,
                      help="YYYY-MM-DD — 지정하면 이 날짜까지 여러 번 호출해 깊게 채운다"
                           "(최초 1회성 backfill용, --days 무시)")
    pdh.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    pdh.add_argument("--raw", action="store_true")
    pdh.set_defaults(func=cmd_daily_history)

    pss = sub.add_parser("short-sale", help="공매도 일별추이 조회, sources/sk-hynix-short-sale.csv에 기록")
    pss.add_argument("--ticker", default="000660")
    pss.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    pss.add_argument("--raw", action="store_true")
    pss.set_defaults(func=cmd_short_sale)

    pen = sub.add_parser("etf-nav", help="ETF/ETN 현재가+NAV+괴리율 조회, sources/portfolio-etf-nav.csv에 기록")
    pen.add_argument("--ticker", required=True, help="ETF 종목코드(예: 469150=ACE AI반도체TOP3+)")
    pen.add_argument("--account-type", default=os.environ.get("KIS_ACCOUNT_TYPE", "real"), choices=["real", "vts"])
    pen.add_argument("--raw", action="store_true")
    pen.set_defaults(func=cmd_etf_nav)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
