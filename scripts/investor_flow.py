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
from datetime import datetime, timedelta, timezone

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
ADR_CSV_FIELDS = ["date", "symbol", "price", "change", "change_pct", "prev_close", "source", "fetched_at"]

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
    with urllib.request.urlopen(req) as resp:
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

    # ⚠ *_tr_pbmn 필드는 실측 결과 "백만원" 단위로 확인됨(2026-07-25 실계정
    # 테스트: 7/24 외국인 1일 순매도 필드값 -1,753,255 → ×1,000,000 = 약
    # -1.753조원, 같은 날 웹검색으로 확보한 "1조7,568억원 순매도" 추정치와
    # 0.2% 오차로 정합 — "원" 단위였다면 100만 배 차이가 났을 것이므로
    # 백만원 단위가 맞다고 판단). 위키 관례(원 단위 표기)에 맞춰 정규화.
    KRW_UNIT_MULTIPLIER = 1_000_000

    parsed = []
    for r in rows:
        d = r[FIELDS["date"]]
        parsed.append({
            "date": f"{d[0:4]}-{d[4:6]}-{d[6:8]}",
            "ticker": ticker,
            "foreign_net_qty": r[FIELDS["foreign_net_qty"]],
            "inst_net_qty": r[FIELDS["inst_net_qty"]],
            "retail_net_qty": r[FIELDS["retail_net_qty"]],
            "foreign_net_krw": int(r[FIELDS["foreign_net_krw"]]) * KRW_UNIT_MULTIPLIER,
            "inst_net_krw": int(r[FIELDS["inst_net_krw"]]) * KRW_UNIT_MULTIPLIER,
            "retail_net_krw": int(r[FIELDS["retail_net_krw"]]) * KRW_UNIT_MULTIPLIER,
            "source": "kis_api",
            "note": "",
        })
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
        with urllib.request.urlopen(req) as resp:
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
        with urllib.request.urlopen(req) as resp:
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
        with urllib.request.urlopen(req) as resp:
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
    required = ["xymd", "clos", "diff", "rate"]
    missing = [k for k in required if k not in latest]
    if missing:
        sys.exit(
            f"예상한 필드가 API 응답에 없습니다: {missing}. 실제 응답 키: "
            f"{sorted(latest.keys())}\n실제 응답 전체(최신행): {json.dumps(latest, ensure_ascii=False)}\n"
            "이 함수의 required 필드명을 위 실제 필드명으로 고치세요."
        )
    price = float(latest["clos"])
    change = float(latest["diff"])
    change_pct = float(latest["rate"])
    trade_date_raw = str(latest["xymd"])  # YYYYMMDD
    trade_date = f"{trade_date_raw[:4]}-{trade_date_raw[4:6]}-{trade_date_raw[6:]}"
    return {
        "symbol": symbol,
        "date": trade_date,
        "price": price,
        "change": change,
        "change_pct": change_pct,
        "prev_close": price - change,
    }


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
    with ADR_CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ADR_CSV_FIELDS)
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
    existing[key] = {
        "date": row_date, "symbol": quote["symbol"],
        "price": quote["price"], "change": quote["change"],
        "change_pct": quote["change_pct"], "prev_close": quote["prev_close"],
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
    flag = " 🚨 급변동(5%+)" if abs(q["change_pct"]) >= 5 else ""
    date_note = f" [{q['date']} 거래일]" if q.get("date") else ""
    print(f"{q['symbol']}  ${q['price']:,.2f}  {q['change']:+,.2f}({q['change_pct']:+.2f}%){flag}  전일종가 ${q['prev_close']:,.2f}{date_note}  → {ADR_CSV_PATH}에 기록")


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

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
