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
}

DEFAULT_LOOKBACK_DAYS = 1095  # 최초 백필 시 과거 3년치


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


def ecos_fetch(stat_code, item_code, cycle, start, end, raw=False):
    key = _get_env_or_die("ECOS_API_KEY", "https://ecos.bok.or.kr/api/")
    url = f"{ECOS_BASE}/{key}/json/kr/1/1000/{stat_code}/{cycle}/{start}/{end}/{item_code}"
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

    _, rows = _fetch_preset(args.series, start, end, raw=False)
    for d, v in rows:
        print(f"{d}\t{v}")


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
