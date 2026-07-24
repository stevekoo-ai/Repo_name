#!/usr/bin/env python3
"""
온디맨드 거시경제 지표 조회기 — 금리/GDP/환율/물가 등을 필요할 때마다 바로
가져오기 위한 범용 스크립트. regime_engine.py(미국 CPI/실업률/기준금리 G/I/L
계산용, 정적 시드 데이터 기반)와는 별개 — 이건 "지금 당장 이 지표 값 좀
보여줘"용 실시간 조회 + 그래프·논의의 재료를 만드는 용도다.

지원 프로바이더:
  - FRED (미국, St. Louis Fed) — 안정적인 공개 API, series_id만 알면 바로 조회
  - ECOS (한국은행 경제통계시스템) — 통계표코드+항목코드 체계, 프리셋 몇 개만
    문서 기억 기반으로 넣어뒀고 나머지는 통계표코드를 직접 넣어 조회

⚠ ECOS의 통계표코드/항목코드는 지표마다 다르고 이 스크립트에 미리 넣어둔
것 외에는 검증되지 않았다 — PRESETS에 없는 지표는 ECOS Open API 페이지
(https://ecos.bok.or.kr/api/)에서 통계표코드를 직접 찾아 --stat-code로
넘겨야 한다. 지어낸 코드로 조용히 틀린 값을 반환하지 않기 위해, 프리셋에
없는 이름을 요청하면 에러를 낸다.

환경변수(필요한 것만 설정, 저장소에 커밋 금지):
  FRED_API_KEY   — https://fred.stlouisfed.org/docs/api/api_key.html
  ECOS_API_KEY   — https://ecos.bok.or.kr/api/

사용법:
  # 프리셋으로 조회 (아래 PRESETS 참고)
  python3 scripts/macro_data.py fetch --series us_fed_funds --start 2023-01-01
  python3 scripts/macro_data.py fetch --series kr_base_rate --start 2023-01

  # ECOS 임의 통계표코드로 직접 조회 (프리셋에 없는 지표)
  python3 scripts/macro_data.py ecos-raw --stat-code <표코드> --item-code <항목코드> \
      --cycle M --start 202301 --end 202607

  # 프리셋 목록 보기
  python3 scripts/macro_data.py list-presets
"""
import os
import sys
import json
import argparse
import urllib.request
import urllib.error

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
ECOS_BASE = "https://ecos.bok.or.kr/api/StatisticSearch"

# (provider, series_id 또는 (stat_code, item_code, cycle), 설명, 검증여부)
PRESETS = {
    "us_fed_funds": ("fred", "FEDFUNDS", "미국 연방기금금리(월평균실효금리)", "검증됨(FRED 표준 series_id)"),
    "us_cpi": ("fred", "CPIAUCSL", "미국 CPI(도시소비자, 계절조정)", "검증됨"),
    "us_unemployment": ("fred", "UNRATE", "미국 실업률", "검증됨"),
    "us_gdp_real": ("fred", "GDPC1", "미국 실질GDP(분기, 연율)", "검증됨"),
    "us_gdp_nominal": ("fred", "GDP", "미국 명목GDP(분기, 연율)", "검증됨"),
    "kr_base_rate": ("ecos", ("722Y001", "0101000", "M"), "한국은행 기준금리", "⚠ 문서기억 기반, --raw로 재검증 권장"),
    "kr_usdkrw": ("ecos", ("731Y001", "0000001", "D"), "원/달러 환율", "⚠ 문서기억 기반, --raw로 재검증 권장"),
}


def _get_env_or_die(name, url):
    v = os.environ.get(name)
    if not v:
        sys.exit(f"환경변수 {name}이(가) 없습니다 — {url} 에서 발급받아 설정하세요.")
    return v


def fred_fetch(series_id, start=None, end=None, raw=False):
    key = _get_env_or_die("FRED_API_KEY", "https://fred.stlouisfed.org/docs/api/api_key.html")
    params = f"series_id={series_id}&api_key={key}&file_type=json"
    if start:
        params += f"&observation_start={start}"
    if end:
        params += f"&observation_end={end}"
    try:
        with urllib.request.urlopen(f"{FRED_BASE}?{params}") as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"FRED API 호출 실패: {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return []

    obs = data.get("observations")
    if obs is None:
        sys.exit(f"응답에 observations가 없습니다 — --raw로 원본 확인: {json.dumps(data)[:300]}")
    return [(o["date"], o["value"]) for o in obs if o["value"] != "."]


def ecos_fetch(stat_code, item_code, cycle, start, end, raw=False):
    key = _get_env_or_die("ECOS_API_KEY", "https://ecos.bok.or.kr/api/")
    url = (f"{ECOS_BASE}/{key}/json/kr/1/1000/{stat_code}/{cycle}/{start}/{end}/{item_code}")
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"ECOS API 호출 실패: {e.code} {e.read().decode(errors='replace')}")

    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return []

    if "RESULT" in data:
        sys.exit(f"ECOS API 오류 응답: {data['RESULT']}")
    rows = data.get("StatisticSearch", {}).get("row")
    if not rows:
        sys.exit(
            f"응답에서 데이터를 찾지 못했습니다 — --raw로 원본을 확인하세요. "
            f"통계표코드/항목코드가 틀렸을 수 있습니다: {json.dumps(data, ensure_ascii=False)[:300]}"
        )
    return [(r["TIME"], r["DATA_VALUE"]) for r in rows]


def cmd_list_presets(args):
    print(f"{'이름':<18}{'제공처':<6}{'설명':<28}검증상태")
    for name, (provider, spec, desc, verified) in PRESETS.items():
        print(f"{name:<18}{provider:<6}{desc:<28}{verified}")


def cmd_fetch(args):
    if args.series not in PRESETS:
        sys.exit(
            f"'{args.series}'는 프리셋에 없습니다. list-presets로 목록을 보거나, "
            f"ECOS 지표라면 ecos-raw 서브커맨드로 통계표코드를 직접 넘기세요."
        )
    provider, spec, desc, verified = PRESETS[args.series]
    print(f"# {desc} [{verified}]", file=sys.stderr)

    if provider == "fred":
        rows = fred_fetch(spec, args.start, args.end, raw=args.raw)
    else:
        stat_code, item_code, cycle = spec
        rows = ecos_fetch(stat_code, item_code, cycle, args.start or "190001", args.end or "999912", raw=args.raw)

    if args.raw:
        return
    for date, value in rows:
        print(f"{date}\t{value}")


def cmd_ecos_raw(args):
    rows = ecos_fetch(args.stat_code, args.item_code, args.cycle, args.start, args.end, raw=args.raw)
    if args.raw:
        return
    for date, value in rows:
        print(f"{date}\t{value}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list-presets", help="지원하는 프리셋 지표 목록")
    pl.set_defaults(func=cmd_list_presets)

    pf = sub.add_parser("fetch", help="프리셋 이름으로 조회")
    pf.add_argument("--series", required=True, help="PRESETS의 키 (list-presets로 확인)")
    pf.add_argument("--start", help="FRED: YYYY-MM-DD, ECOS: YYYYMM 또는 YYYYMMDD(주기에 맞게)")
    pf.add_argument("--end")
    pf.add_argument("--raw", action="store_true")
    pf.set_defaults(func=cmd_fetch)

    pe = sub.add_parser("ecos-raw", help="ECOS 임의 통계표코드로 직접 조회")
    pe.add_argument("--stat-code", required=True)
    pe.add_argument("--item-code", required=True)
    pe.add_argument("--cycle", required=True, help="Y/Q/M/D 등")
    pe.add_argument("--start", required=True)
    pe.add_argument("--end", required=True)
    pe.add_argument("--raw", action="store_true")
    pe.set_defaults(func=cmd_ecos_raw)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
