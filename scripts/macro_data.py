#!/usr/bin/env python3
"""
거시경제 지표(금리/GDP/환율/물가) 수집기 — GitHub Actions가 매일 자동으로
돌려서 sources/macro-series.csv에 쌓아두는 용도. Claude는 이 CSV를 읽기만
하면 되므로, 대화 세션에 FRED_API_KEY/ECOS_API_KEY가 없어도 "금리 어때?"
같은 질문에 최신 데이터로 답할 수 있다 — 키는 GitHub Secrets에만 있으면 됨.

regime_engine.py(미국 CPI/실업률/기준금리로 G/I/L 계산)와는 별개 레이어 —
이건 특정 계산 없이 "지표 원자료를 계속 최신으로 유지"만 담당한다.

지원 프로바이더:
  - FRED (미국, St. Louis Fed) — 표준 series_id, 안정적
  - ECOS (한국은행 경제통계시스템) — 통계표코드+항목코드 체계

⚠ ECOS 프리셋의 통계표코드/항목코드는 문서 기억 기반이라 최초 실행 시
--raw로 검증 필요(잘못됐으면 API가 빈 응답이나 에러를 반환하므로 조용히
틀린 값이 들어가진 않는다 — ecos_fetch가 빈 rows면 즉시 에러를 낸다).

환경변수(GitHub Secrets에 등록, 로컬 테스트 시엔 셸에 export):
  FRED_API_KEY, ECOS_API_KEY

사용법:
  # 프리셋 전체(또는 --series로 선택)를 조회해 CSV에 upsert — Actions가 매일 실행
  python3 scripts/macro_data.py sync
  python3 scripts/macro_data.py sync --series kr_base_rate us_fed_funds

  # 단발 조회(디버깅/검증용, CSV에 안 쌓임)
  python3 scripts/macro_data.py fetch --series us_fed_funds --start 2023-01-01
  python3 scripts/macro_data.py fetch --series kr_base_rate --raw

  # ECOS 임의 통계표코드 직접 조회 (프리셋에 없는 지표)
  python3 scripts/macro_data.py ecos-raw --stat-code <표코드> --item-code <항목코드> \
      --cycle M --start 202301 --end 202607

  # 프리셋 목록
  python3 scripts/macro_data.py list-presets
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

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
ECOS_BASE = "https://ecos.bok.or.kr/api/StatisticSearch"

SERIES_CSV_PATH = Path(__file__).resolve().parent.parent / "sources" / "macro-series.csv"
SERIES_CSV_FIELDS = ["series", "date", "value", "provider", "fetched_at"]

# 이름 -> (provider, series_id 또는 (stat_code, item_code, cycle), 설명, 검증여부)
PRESETS = {
    "us_fed_funds": ("fred", "FEDFUNDS", "미국 연방기금금리(월평균실효금리)", "검증됨(FRED 표준 series_id)"),
    "us_cpi": ("fred", "CPIAUCSL", "미국 CPI(도시소비자, 계절조정)", "검증됨"),
    "us_unemployment": ("fred", "UNRATE", "미국 실업률", "검증됨"),
    "us_gdp_real": ("fred", "GDPC1", "미국 실질GDP(분기, 연율)", "검증됨"),
    "us_gdp_nominal": ("fred", "GDP", "미국 명목GDP(분기, 연율)", "검증됨"),
    "kr_base_rate": ("ecos", ("722Y001", "0101000", "M"), "한국은행 기준금리", "⚠ 문서기억 기반, --raw로 재검증 권장"),
    "kr_usdkrw": ("ecos", ("731Y001", "0000001", "D"), "원/달러 환율", "⚠ 문서기억 기반, --raw로 재검증 권장"),
    # 유가는 CPI 에너지 항목의 선행변수라 거시국면 판단에 직접 쓰인다.
    # 2026-07-26 위키 정정 사건("7월 유가 급등"을 차트 육안 판독으로 추정하다
    # 레벨과 속도를 혼동)의 재발 방지로 추가. 그런데 이 프리셋을 작업
    # 브랜치에만 추가하고 main에 반영하지 않아 2026-07-28까지 실제로는 한
    # 번도 동기화되지 않았던 게 뒤늦게 발견됨 — PR #34로 main에 반영.
    "us_brent": ("fred", "DCOILBRENTEU", "브렌트유 현물(일별, $/배럴)", "검증됨(FRED 표준 series_id)"),
    "us_wti": ("fred", "DCOILWTICO", "WTI 현물(일별, $/배럴)", "검증됨(FRED 표준 series_id)"),
    # 2026-08-09 추가 — SK Hynix Investment Thesis "Layer 0: Valuation Band"의
    # ERP(Equity Risk Premium) 계산에 필요한 무위험금리. Earnings Yield(1/PER
    # 근사) - 이 시리즈 = ERP. concepts/sk-hynix-investment-thesis.md 참고.
    "us_10y": ("fred", "DGS10", "미국 10년물 국채금리(일별)", "검증됨(FRED 표준 series_id)"),
    # 2026-09-07 추가 — 사용자 요청("원·달러·엔·위안 4개국 통화 상호 영향 진단").
    # 기존엔 kr_usdkrw(ECOS) 하나뿐이라 엔/위안과의 상호 움직임을 볼 수가 없었다.
    # 셋 다 "1달러당 해당 통화" 표기라 방향이 통일돼 있다(값 상승 = 달러 강세)
    # — 상관계수 부호를 추가 변환 없이 그대로 읽을 수 있다. usd_krw_fred는
    # kr_usdkrw(ECOS 고시)와 같은 환율의 다른 출처로, 교차검증용(값이 갈리면
    # R1 실측 우선 원칙에 따라 한국은행 고시인 ECOS를 채택).
    "usd_jpy": ("fred", "DEXJPUS", "엔/달러 환율(일별)", "검증됨(FRED 표준 series_id)"),
    "usd_cny": ("fred", "DEXCHUS", "위안/달러 환율(일별)", "검증됨(FRED 표준 series_id)"),
    "usd_krw_fred": ("fred", "DEXKOUS", "원/달러 환율(일별, ECOS 교차검증용)", "검증됨(FRED 표준 series_id)"),
    # 2026-09-10 추가 — 사용자 요청("환율 국면에서 나스닥/S&P/금리/채권이 어떻게
    # 움직였는지 보고, 환전 후 달러 투자처까지 판단하자"). 지금까지 이 저장소는
    # 미국 "주식" 계열을 단 하나도 안 갖고 있었고 us_10y조차 2016년부터라
    # 36개월선 하회 5개 국면(2010~2021) 중 앞 3개를 덮지 못했다.
    #
    # ⚠ FRED의 S&P Dow Jones 라이선스 계열(SP500·DJIA)은 최근 10년만 공개된다
    # — 2016년 이전 국면엔 못 쓴다. 그래서 장기 이력이 열려 있는 두 계열을
    # 함께 넣어 앞 구간을 덮는다: NASDAQCOM(1971~, Nasdaq OMX)과
    # WILL5000IND(1970~, Wilshire 광의 미국주식 = S&P 대용).
    "us_sp500": ("fred", "SP500", "S&P 500 지수(일별, ⚠FRED 라이선스로 최근 10년만)", "⚠ 실측 확인: 2016-09~ 만 제공"),
    "us_nasdaq": ("fred", "NASDAQCOM", "나스닥 종합지수(일별, 1971~)", "검증됨(2026-09-10 백필로 2005~ 확인)"),
    # 2026-09-10 1차 백필 실측: WILL5000IND는 존재하지 않는 id였다(FRED 거부).
    # 전량 가격지수 id인 WILL5000PRFC로 교체 + OECD 월간 미국 주가지수를
    # S&P 장기 대용으로 병기(둘 중 살아남는 쪽을 쓴다).
    "us_wilshire": ("fred", "WILL5000PRFC", "윌셔5000 전량가격지수(일별, S&P 장기 대용)", "⚠ 미검증 — 2차 백필로 확정"),
    "us_sp500_oecd": ("fred", "SPASTT01USM661N", "미국 주가지수 OECD 월간(1960~, S&P 추종 장기 대용)", "⚠ 미검증 — 2차 백필로 확정"),
    "us_vix": ("fred", "VIXCLS", "VIX 변동성지수(1990~, 위험선호 장기 대용)", "⚠ 미검증 — 2차 백필로 확정"),
    # 금리 커브 — 환율 국면의 시작/종료 트리거가 대부분 미국 금리에서 왔다
    # (usdkrw-below-ma36-episodes.md: 6회 중 5회 종료 트리거가 미 긴축 전환).
    # us_3m은 "달러를 그냥 들고 있을 때"의 기준선(MMF/단기국채 수익률)이라
    # 투자처 비교의 벤치마크로 반드시 필요하다.
    "us_2y": ("fred", "DGS2", "미국 2년물 국채금리(일별, 정책기대 반영)", "검증됨(2026-09-10 백필)"),
    "us_3m": ("fred", "DGS3MO", "미국 3개월물 국채금리(일별, 달러 현금 기준선)", "검증됨(2026-09-10 백필)"),
    # 채권은 금리(yield)만 보면 투자 성과를 알 수 없다 — 금리가 오르면
    # 보유 채권은 평가손이 난다. 그래서 총수익지수(Total Return Index Value)를
    # 같이 받는다. 이게 있어야 "그 달러로 채권 사면 얼마 벌었나"에 답할 수 있다.
    "us_ig_tr": ("fred", "BAMLCC0A0CMTRIV", "미국 우량회사채 총수익지수(ICE BofA)", "⚠ 실측: FRED 라이선스로 최근 3년만 제공 — 국면 분석엔 못 씀"),
    "us_hy_tr": ("fred", "BAMLHYH0A0HYM2TRIV", "미국 하이일드채 총수익지수(ICE BofA)", "⚠ 실측: 최근 3년만 제공 — 국면 분석엔 못 씀"),
    "us_hy_oas": ("fred", "BAMLH0A0HYM2", "미국 하이일드 스프레드 OAS(위험선호 지표)", "⚠ 실측: 최근 3년만 제공 — 장기 대용은 us_vix"),
    # 달러지수 — FRS 설계안(fx-regime-score-design.md)의 DXY 요인(가중치 15)
    # 입력. DTWEXBGS는 2006년부터라 2005년 이전 구간엔 2020년 폐지된
    # DTWEXM(1973~2020)을 이어붙여 쓴다.
    "us_dollar_index": ("fred", "DTWEXBGS", "달러지수 광의(일별, 2006~)", "검증됨(2026-09-10 백필)"),
    "us_dollar_index_major": ("fred", "DTWEXM", "달러지수 주요통화(1973~2020 폐지, 2006년 이전 대용)", "검증됨(2026-09-10 백필)"),
}

DEFAULT_LOOKBACK_DAYS = 3652  # 최초 백필 시 과거 10년치


def _get_env_or_die(name, url):
    v = os.environ.get(name)
    if not v:
        sys.exit(f"환경변수 {name}이(가) 없습니다 — {url} 에서 발급받아 설정하세요.")
    return v


def _fmt_fred(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def _fmt_ecos(d: date, cycle: str) -> str:
    if cycle == "D":
        return d.strftime("%Y%m%d")
    if cycle == "M":
        return d.strftime("%Y%m")
    if cycle == "Q":
        q = (d.month - 1) // 3 + 1
        return f"{d.year}Q{q}"
    if cycle == "Y":
        return d.strftime("%Y")
    raise ValueError(f"알 수 없는 cycle: {cycle}")


def _normalize_ecos_date(raw: str, cycle: str) -> str:
    """ECOS의 다양한 날짜 표기를 ISO YYYY-MM-DD로 통일(CSV 저장용)."""
    if cycle == "D":
        return f"{raw[0:4]}-{raw[4:6]}-{raw[6:8]}"
    if cycle == "M":
        return f"{raw[0:4]}-{raw[4:6]}-01"
    if cycle == "Y":
        return f"{raw}-01-01"
    if cycle == "Q":
        y, q = raw.split("Q")
        month = (int(q) - 1) * 3 + 1
        return f"{y}-{month:02d}-01"
    return raw


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


def _ecos_fetch_page(key, stat_code, item_code, cycle, start, end, row_from, row_to):
    url = f"{ECOS_BASE}/{key}/json/kr/{row_from}/{row_to}/{stat_code}/{cycle}/{start}/{end}/{item_code}"
    try:
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"ECOS API 호출 실패: {e.code} {e.read().decode(errors='replace')}")


def ecos_fetch(stat_code, item_code, cycle, start, end, raw=False):
    """ECOS는 요청당 최대 1000행 — 일별(D) 시리즈는 10년치가 1000행을
    훌쩍 넘기므로(전체 응답의 list_total_count 확인 후) 페이지네이션한다.
    페이지네이션 안 하면 "가장 오래된 1000행"만 오고 최근 데이터가 통째로
    누락되는 버그가 있었음(2026-07-25 실계정 테스트로 발견 — kr_usdkrw가
    2016~2020년치만 채워지고 2020~2026년은 비어있었음)."""
    key = _get_env_or_die("ECOS_API_KEY", "https://ecos.bok.or.kr/api/")

    first = _ecos_fetch_page(key, stat_code, item_code, cycle, start, end, 1, 1000)
    if raw:
        print(json.dumps(first, ensure_ascii=False, indent=2))
        return []

    if "RESULT" in first:
        sys.exit(f"ECOS API 오류 응답: {first['RESULT']}")
    search = first.get("StatisticSearch", {})
    rows = search.get("row")
    if not rows:
        sys.exit(
            f"응답에서 데이터를 찾지 못했습니다 — --raw로 원본을 확인하세요. "
            f"통계표코드/항목코드가 틀렸을 수 있습니다: {json.dumps(first, ensure_ascii=False)[:300]}"
        )

    total = int(search.get("list_total_count", len(rows)))
    row_from = 1001
    while row_from <= total:
        row_to = min(row_from + 999, total)
        page = _ecos_fetch_page(key, stat_code, item_code, cycle, start, end, row_from, row_to)
        page_rows = page.get("StatisticSearch", {}).get("row")
        if not page_rows:
            break
        rows.extend(page_rows)
        row_from += 1000

    return [(r["TIME"], r["DATA_VALUE"]) for r in rows]


def _read_series_csv():
    if not SERIES_CSV_PATH.exists():
        return {}
    rows = {}
    with SERIES_CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[(row["series"], row["date"])] = row
    return rows


def _write_series_csv(rows_by_key):
    SERIES_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows_by_key.values(), key=lambda r: (r["series"], r["date"]))
    with SERIES_CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=SERIES_CSV_FIELDS)
        w.writeheader()
        for r in ordered:
            w.writerow(r)


def upsert_series_rows(series_name, rows, provider):
    existing = _read_series_csv()
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for date_str, value in rows:
        existing[(series_name, date_str)] = {
            "series": series_name, "date": date_str, "value": value,
            "provider": provider, "fetched_at": fetched_at,
        }
    _write_series_csv(existing)
    return len(rows)


def cmd_list_presets(args):
    print(f"{'이름':<18}{'제공처':<6}{'설명':<28}검증상태")
    for name, (provider, spec, desc, verified) in PRESETS.items():
        print(f"{name:<18}{provider:<6}{desc:<28}{verified}")


def _fetch_preset(name, start=None, end=None, raw=False):
    provider, spec, desc, verified = PRESETS[name]
    print(f"# {desc} [{verified}]", file=sys.stderr)
    if provider == "fred":
        rows = fred_fetch(spec, start, end, raw=raw)
        return provider, rows
    stat_code, item_code, cycle = spec
    raw_rows = ecos_fetch(stat_code, item_code, cycle, start, end, raw=raw)
    if raw:
        return provider, []
    return provider, [(_normalize_ecos_date(d, cycle), v) for d, v in raw_rows]


def cmd_fetch(args):
    if args.series not in PRESETS:
        sys.exit(
            f"'{args.series}'는 프리셋에 없습니다. list-presets로 목록을 보거나, "
            f"ECOS 지표라면 ecos-raw 서브커맨드로 통계표코드를 직접 넘기세요."
        )
    provider, spec, desc, verified = PRESETS[args.series]
    if args.raw:
        if provider == "fred":
            fred_fetch(spec, args.start, args.end, raw=True)
        else:
            stat_code, item_code, cycle = spec
            ecos_fetch(stat_code, item_code, cycle, args.start or _fmt_ecos(date.today() - timedelta(days=DEFAULT_LOOKBACK_DAYS), cycle), args.end or _fmt_ecos(date.today(), cycle), raw=True)
        return

    start = args.start
    end = args.end
    if provider == "ecos" and (start is None or end is None):
        stat_code, item_code, cycle = spec
        start = start or _fmt_ecos(date.today() - timedelta(days=DEFAULT_LOOKBACK_DAYS), cycle)
        end = end or _fmt_ecos(date.today(), cycle)

    provider_used, rows = _fetch_preset(args.series, start, end, raw=False)
    for d, v in rows:
        print(f"{d}\t{v}")

    # 2026-09-09 추가 — fetch는 원래 출력 전용이었고 sync는 "기존 마지막
    # 날짜 - 7일"부터만 증분 수집한다. 그래서 이미 있는 데이터보다 *과거*로
    # 넓히는 경로가 코드 어디에도 없었다(36개월 이동평균 분석에 2007년치가
    # 필요해지면서 드러남). --save는 fetch가 방금 가져온 걸 그대로 저장만
    # 하게 한다 — upsert가 (series,date) 키 멱등 병합이라 기존 행은 안 깨진다.
    if getattr(args, "save", False):
        if not rows:
            print("저장할 행이 없습니다(응답 0건) — CSV를 건드리지 않습니다.", file=sys.stderr)
            return
        n = upsert_series_rows(args.series, rows, provider_used)
        print(f"저장 완료: {args.series} {n}행 ({rows[0][0]} ~ {rows[-1][0]})", file=sys.stderr)


def cmd_ecos_raw(args):
    rows = ecos_fetch(args.stat_code, args.item_code, args.cycle, args.start, args.end, raw=args.raw)
    if args.raw:
        return
    for d, v in rows:
        print(f"{d}\t{v}")


def cmd_sync(args):
    targets = args.series or list(PRESETS.keys())
    total = 0
    for name in targets:
        if name not in PRESETS:
            print(f"건너뜀: '{name}'은 프리셋에 없음", file=sys.stderr)
            continue
        provider, spec, desc, verified = PRESETS[name]

        existing_dates = [r["date"] for (s, d), r in _read_series_csv().items() if s == name]
        if existing_dates:
            start_date = date.fromisoformat(max(existing_dates)) - timedelta(days=7)
        else:
            start_date = date.today() - timedelta(days=DEFAULT_LOOKBACK_DAYS)
        end_date = date.today()

        if provider == "fred":
            start_str, end_str = _fmt_fred(start_date), _fmt_fred(end_date)
        else:
            _, _, cycle = spec
            start_str, end_str = _fmt_ecos(start_date, cycle), _fmt_ecos(end_date, cycle)

        try:
            _, rows = _fetch_preset(name, start_str, end_str, raw=False)
        except SystemExit as e:
            print(f"'{name}' 동기화 실패: {e}", file=sys.stderr)
            continue

        n = upsert_series_rows(name, rows, provider)
        total += n
        print(f"{name}: {n}개 데이터포인트 upsert ({start_str} ~ {end_str})")

    print(f"\n총 {total}개 데이터포인트 갱신 → {SERIES_CSV_PATH}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list-presets", help="지원하는 프리셋 지표 목록")
    pl.set_defaults(func=cmd_list_presets)

    psy = sub.add_parser("sync", help="프리셋(전체 또는 선택)을 조회해 sources/macro-series.csv에 upsert")
    psy.add_argument("--series", nargs="+", help="특정 시리즈만 동기화(기본: 전체 프리셋)")
    psy.set_defaults(func=cmd_sync)

    pf = sub.add_parser("fetch", help="프리셋 이름으로 단발 조회(CSV에 안 남음, 디버깅용)")
    pf.add_argument("--series", required=True, help="PRESETS의 키 (list-presets로 확인)")
    pf.add_argument("--start", help="FRED: YYYY-MM-DD, ECOS: 주기에 맞는 포맷(YYYYMM 등)")
    pf.add_argument("--end")
    pf.add_argument("--raw", action="store_true")
    pf.add_argument("--save", action="store_true",
                    help="가져온 값을 macro-series.csv에 저장(기본은 출력만) — 과거 구간 백필용")
    pf.set_defaults(func=cmd_fetch)

    pe = sub.add_parser("ecos-raw", help="ECOS 임의 통계표코드로 직접 조회(프리셋에 없는 지표)")
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
