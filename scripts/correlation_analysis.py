"""Correlate MOTIE monthly export growth against SK Hynix price and KOSPI.

WHY YoY, NOT LEVELS
────────────────────
The user's claim to check was "수출입동향 수치와 하이닉스 주가, 코스피 주가간에
상관관계를 보인다" — but naively correlating a growth RATE (수출 %YoY) against
a price LEVEL (원화 주가, 지수 포인트) is close to guaranteed to look
"significant" for the wrong reason: both trend upward over a multi-year
uptrend/cycle, so almost any two upward-trending series correlate strongly
without one causing or tracking the other (spurious correlation from a
shared trend). This repo has already paid for treating a coincidence as a
signal once (the fabricated US-KR rate spread published from an 8-year-old
observation) — the fix here is methodological: convert price and the index
to YoY% themselves before correlating, so all four series are the same kind
of quantity (a growth rate) and a high correlation actually means the rates
moved together, not just that both happened to rise.

INPUTS (all real, no estimates)
────────────────────────────────
  data/normalized/customs_export_dlr.csv                (date, value) $, from
    collectors/customs_trade.py (관세청 수출입총괄 GW, 실측 1990.01~ 확인됨) —
    이게 있으면 총수출 %YoY의 1차 출처. 이 파일이 커버 못 하는 달만
    motie_total_exports_yoy.csv(수동, 2026-04~)로 보충한다.
  data/normalized/motie_total_exports_yoy.csv          (date, value) %YoY
  data/normalized/motie_semiconductor_exports_yoy.csv   (date, value) %YoY
  sources/monthly-price-history.csv                     (date, code, label,
                                                           close, ...) — via
    `python -m scripts.investor_flow monthly-history --code 000660 ...`
    `python -m scripts.investor_flow monthly-history --code 0001 --is-index`
  sources/daily-price-history.csv    2026-08-17 added, same shape as monthly
                                      but one row per trading day — via
    `python -m scripts.investor_flow daily-history --code 000660 ...`
    `python -m scripts.investor_flow daily-history --code 0001 --is-index`
    Only the daily-focus chart/markdown (build_daily_focus_dataset) reads
    this; the monthly/QoQ/annual outputs are untouched by it.
  Price/index YoY% is derived here (close_m / close_{m-12} - 1) * 100 — it is
  not itself a stored series, so a short price history simply yields fewer
  YoY points rather than an error.
  data/manual_inputs/exports_preliminary.yaml   2026-08-17 added — 관세청
    10일 단위 수출입 현황 [잠정치] (1~10일 released day 11, 1~20일 released
    day 21, both ahead of the day-1-of-next-month final figure). Never
    merged into total_exports_yoy — load_exports_preliminary() surfaces it
    separately so callers can draw it as a distinctly-styled "next point"
    (dashed line + hollow marker) rather than pretend it's a real
    observation. Update the file's `latest` block by hand when a new
    10-day/20-day release lands (no clean structured export-side API found
    on data.go.kr as of this writing — only an import-side one).

OUTPUTS
────────
  monitoring/exports-price-correlation.md   pairwise correlation table + a
                                             stated sample size for every
                                             pair (a correlation without n is
                                             not trustworthy — see 한계 절)
  monitoring/exports-price-correlation.png  all three series (총수출/
                                             하이닉스/코스피, %YoY) overlaid,
                                             z-score normalized onto one
                                             chart so different scales sit
                                             comparably and each series'
                                             own variation stays visible
                                             even though 총수출 covers a much
                                             longer span (1990~) than the
                                             KIS price history (1983~/1996~)
  monitoring/exports-price-correlation-qoq.{md,png}   2026-08-17 added — same
                                             three series, but %QoQ (vs prior
                                             quarter) instead of %YoY, on a
                                             quarterly grid instead of monthly.
  monitoring/exports-price-correlation-2023-zoom.png   2026-08-17 added — same
                                             three monthly %YoY series as the
                                             main PNG, but sliced to
                                             ZOOM_START~present and
                                             re-z-scored within that slice
                                             (not the full-history z-score)
                                             so recent detail isn't flattened
                                             by 35+ years of total_exports
                                             history dominating the scale.
  monitoring/exports-price-correlation-daily-focus.{md,png}   2026-08-17
                                             added — total_exports stays at
                                             its native monthly resolution
                                             (small markers, sparse), but
                                             hynix/kospi are plotted at their
                                             native DAILY resolution instead
                                             of resampled to monthly — the
                                             daily lines naturally extend
                                             further right than the monthly
                                             one (more frequently published
                                             data reads as "leading" without
                                             any artificial time-shift).
                                             Last DAILY_FOCUS_DISPLAY_DAYS
                                             (~2yr) only. This is the chart
                                             the user asked to keep tracking
                                             (SK Hynix running far ahead of
                                             exports, then diving back below
                                             the exports trend — watching for
                                             whether it curls back up).

CURRENT (IN-PROGRESS) MONTH IS ALWAYS EXCLUDED
────────────────────────────────────────────────
_drop_current_incomplete_month() drops the calendar month this script runs
in from every level series before YoY/QoQ is computed. Found 2026-08-17: the
in-progress month's export total (customs clearance so far, not the full
month) or price close (latest trading day, not month-end) is a partial
figure — comparing it to a prior COMPLETE period produces a swing that looks
like a real move but is actually just "we haven't finished counting yet"
(e.g. 총수출 2026-08 showed as -32.8% %YoY from a partial ~39억불 vs other
months' ~85~102억불, purely a partial-month artifact).

Run:
  python -m scripts.correlation_analysis
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates
import matplotlib.pyplot as plt
import pandas as pd
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
NORMALIZED = REPO_ROOT / "data" / "normalized"
MANUAL_INPUTS = REPO_ROOT / "data" / "manual_inputs"
MONTHLY_PRICE_CSV = REPO_ROOT / "sources" / "monthly-price-history.csv"
DAILY_PRICE_CSV = REPO_ROOT / "sources" / "daily-price-history.csv"
EXPORTS_ANNUAL_YAML = MANUAL_INPUTS / "exports_annual.yaml"
KOSPI_ANNUAL_YAML = MANUAL_INPUTS / "kospi_annual.yaml"
EXPORTS_PRELIMINARY_YAML = MANUAL_INPUTS / "exports_preliminary.yaml"
OUT_DIR = REPO_ROOT / "monitoring"
OUT_MD = OUT_DIR / "exports-price-correlation.md"
OUT_PNG = OUT_DIR / "exports-price-correlation.png"
OUT_MD_ANNUAL = OUT_DIR / "exports-kospi-correlation-annual.md"
OUT_PNG_ANNUAL = OUT_DIR / "exports-kospi-correlation-annual.png"
OUT_MD_QOQ = OUT_DIR / "exports-price-correlation-qoq.md"
OUT_PNG_QOQ = OUT_DIR / "exports-price-correlation-qoq.png"
OUT_PNG_ZOOM = OUT_DIR / "exports-price-correlation-2023-zoom.png"
ZOOM_START = pd.Timestamp("2023-01-01")
OUT_MD_DAILY_FOCUS = OUT_DIR / "exports-price-correlation-daily-focus.md"
OUT_PNG_DAILY_FOCUS = OUT_DIR / "exports-price-correlation-daily-focus.png"
# 2026-08-17 사용자 요청 — "최근 2년 정도를 집중해서", "지수가 발표되는
# 가장 짧은 주기(일봉)로 해상도를 높여서". 총수출은 원 주기가 월별이라
# 그대로 두고(더 잘게 쪼갤 수 없다), 하이닉스·코스피는 일봉을 그대로 쓴다
# — 매일 갱신되는 쪽이 한 달에 한 번만 찍히는 총수출보다 자연히 더 최근
# 시점까지 그려지므로("선행"), 시간축을 인위적으로 밀지 않아도 그 자체로
# "먼저 움직이는 걸 보여준다"는 요청을 만족한다.
DAILY_FOCUS_DISPLAY_DAYS = 730

# 표본이 이보다 적으면 상관계수를 표에는 싣되 "신뢰 불가"로 명시한다 —
# 조용히 숫자만 보여주면 n=3짜리 상관계수도 확신처럼 읽힌다.
MIN_TRUSTWORTHY_N = 6

SERIES_LABELS = {
    "total_exports_yoy": "총수출 (%YoY)",
    "semi_exports_yoy": "반도체수출 (%YoY)",
    "hynix_price_yoy": "SK하이닉스 주가 (%YoY)",
    "kospi_yoy": "코스피 지수 (%YoY)",
}

# matplotlib on a bare ubuntu-latest Actions runner only has DejaVu Sans
# (no CJK glyphs) — Hangul in the PNG renders as missing-glyph boxes. The
# markdown table above doesn't have this problem (plain UTF-8 text, no font
# dependency), so only the chart needs an ASCII fallback.
SERIES_LABELS_CHART = {
    "total_exports_yoy": "Total exports (%YoY)",
    "semi_exports_yoy": "Semiconductor exports (%YoY)",
    "hynix_price_yoy": "SK Hynix price (%YoY)",
    "kospi_yoy": "KOSPI index (%YoY)",
}


def _load_motie(series_id: str) -> pd.Series:
    path = NORMALIZED / f"{series_id}.csv"
    if not path.exists():
        return pd.Series(dtype=float)
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")["value"].sort_index()


CUSTOMS_EXPORT_CSV = NORMALIZED / "customs_export_dlr.csv"


def _current_incomplete_month_start() -> pd.Timestamp:
    """오늘이 속한 달의 1일 — 이 달은 아직 안 끝났으니 그 달의 레벨(수출
    달러, 종가)은 전부 부분치다."""
    now = pd.Timestamp.now(tz="UTC").tz_localize(None)
    return pd.Timestamp(year=now.year, month=now.month, day=1)


def _drop_current_incomplete_month(level: pd.Series) -> pd.Series:
    """월 인덱스 시리즈에서 진행 중인 이번 달을 제거한다.

    2026-08-17 실측으로 발견: 총수출 %YoY 마지막 점(2026-08)이 -32.8%로
    급락해 보였는데, 실제 원인은 수출이 줄어서가 아니라 관세청 집계가
    8/17까지치(39억불)뿐이라 다른 달(85~102억불)의 절반도 안 됐기 때문 —
    "부분월 vs 완결월"을 비교해 생긴 착시다. 이 함수는 그 부분월을 아예
    입력에서 빼서, YoY(월별)든 QoQ(분기 합계)든 애초에 왜곡된 값이 나올
    소지를 없앤다. 월봉 가격(KIS)도 같은 문제(이번 달은 월말이 아니라
    최신 거래일까지의 스냅샷)라 여기서 같이 처리한다."""
    if level.empty:
        return level
    cutoff = _current_incomplete_month_start()
    return level[level.index < cutoff]


def _load_customs_export_level() -> pd.Series:
    """관세청 수출입총괄(GW) 실측 월별 총수출(달러) 레벨 — YoY(월별)·QoQ(분기)
    양쪽의 공통 원천. collectors/customs_trade.py가 채우는
    data/normalized/customs_export_dlr.csv 기반 — data/manual_inputs/
    exports.yaml(수동, 2026-04~뿐)보다 이력이 훨씬 길고(실측 1990.01~
    확인됨, config/api.yaml customs_trade 참고) 자동 갱신된다."""
    if not CUSTOMS_EXPORT_CSV.exists():
        return pd.Series(dtype=float)
    df = pd.read_csv(CUSTOMS_EXPORT_CSV)
    df["date"] = pd.to_datetime(df["date"])
    close = df.set_index("date")["value"].sort_index()
    return _drop_current_incomplete_month(close)


def _series_yoy(level: pd.Series) -> pd.Series:
    """월 레벨 시리즈 -> %YoY(12개월 전 대비)."""
    yoy = {}
    for month, val in level.items():
        prior_month = month - pd.DateOffset(years=1)
        if prior_month in level.index:
            prior = level.loc[prior_month]
            if prior:
                yoy[month] = (val / prior - 1) * 100
    return pd.Series(yoy, dtype=float).sort_index()


def _load_customs_export_yoy() -> pd.Series:
    """관세청 실측 월별 총수출(달러) -> %YoY. build_dataset()에서 이 실측값이
    수동 값(motie_total_exports_yoy)보다 항상 우선한다."""
    return _series_yoy(_load_customs_export_level())


def load_exports_preliminary() -> dict | None:
    """관세청 10일 단위 수출입 현황 [잠정치](data/manual_inputs/
    exports_preliminary.yaml) — 진행 중인 달이 끝나기 전에 미리 나오는
    부분기간 수치를 그 달의 %YoY '추정치'로 쓴다. 2026-08-17 사용자 요청.

    중요: total_exports_yoy(실측) 시계열에는 절대 섞지 않는다 — 호출부가
    이 dict를 받아 별도로(점선/빈 마커) 그려야 한다. 반환값이 이미 지난
    달(오늘 기준 진행 중인 달이 아님)이면 None — 최신치를 안 챙겨서 낡은
    잠정치가 이번 달 자리에 잘못 찍히는 걸 막는다."""
    if not EXPORTS_PRELIMINARY_YAML.exists():
        return None
    payload = yaml.safe_load(EXPORTS_PRELIMINARY_YAML.read_text(encoding="utf-8")) or {}
    latest = payload.get("latest")
    if not latest:
        return None
    target_month = pd.Timestamp(latest["target_month"])
    if target_month != _current_incomplete_month_start():
        return None  # 낡은 잠정치 — 이번 달이 이미 지났으면 표시하지 않는다
    period_start, period_end = latest.get("period_start"), latest.get("period_end")
    # 차트 범례는 ASCII만(DejaVu Sans엔 한글 글리프가 없음, SERIES_LABELS_CHART와
    # 같은 이유) — period_label(한글)은 markdown에서만 쓰고, 차트용은 날짜에서
    # 직접 만든다.
    label_en = (f"{pd.Timestamp(period_start).strftime('%b %-d')}-"
                f"{pd.Timestamp(period_end).strftime('%-d')} prelim."
                if period_start and period_end else "prelim.")
    return {
        "date": target_month,
        "value": float(latest["total_exports_yoy"]),
        "label": latest.get("period_label", ""),
        "label_en": label_en,
        "source": latest.get("source", ""),
    }


def _load_price_level(code: str) -> pd.Series:
    """월봉 종가 레벨 — YoY·QoQ 공통 원천. 진행 중인 이번 달은
    _drop_current_incomplete_month()로 제외한다."""
    if not MONTHLY_PRICE_CSV.exists():
        return pd.Series(dtype=float)
    # dtype=str on "code" is load-bearing: without it, pandas infers an
    # all-digit column (e.g. "0001", "000660") as int64 and silently strips
    # the leading zeros on read, so this filter would never match again —
    # found while adding the annual-KOSPI test below (same bug existed here
    # too, just never surfaced because monthly-price-history.csv has never
    # actually been populated in this sandbox).
    df = pd.read_csv(MONTHLY_PRICE_CSV, dtype={"code": str})
    df = df[df["code"] == str(code)].copy()
    if df.empty:
        return pd.Series(dtype=float)
    df["date"] = pd.to_datetime(df["date"])
    # Normalize each observation onto the first-of-month so it lines up with
    # MOTIE's monthly index regardless of which day-of-month KIS reports.
    df["month"] = df["date"].values.astype("datetime64[M]")
    # groupby(...).last() rather than set_index("month")["close"]: a deep
    # backfill can leave TWO rows in the same calendar month (an early
    # mid-month snapshot from one run, the true month-end close from a later
    # run — upsert dedupes by exact (date, code), not by month) — a raw
    # set_index would then have a duplicate month index and every .loc[month]
    # lookup below would return a Series instead of a scalar. .last() (after
    # sorting by date) always collapses to the most complete observation.
    close = df.sort_values("date").groupby("month")["close"].last()
    return _drop_current_incomplete_month(close)


def _load_price_yoy(code: str) -> pd.Series:
    """Monthly close -> %YoY. Requires a close roughly 12 months earlier to
    exist in the same file — with less than a year of KIS history this
    returns an empty series rather than guessing, which is correct: no
    fabricated YoY belongs in a "grade 5 official" comparison."""
    return _series_yoy(_load_price_level(code))


def build_dataset() -> pd.DataFrame:
    # 실측(관세청) 우선, 없는 달만 수동 파일(motie_total_exports_yoy)로 보충 —
    # _load_kospi_annual_yoy()의 "실측이 수동을 덮어쓴다" 패턴과 동일.
    manual_exports_yoy = _load_motie("motie_total_exports_yoy")
    real_exports_yoy = _load_customs_export_yoy()
    total_exports_yoy = (real_exports_yoy.combine_first(manual_exports_yoy)
                          if not real_exports_yoy.empty else manual_exports_yoy)
    series = {
        "total_exports_yoy": total_exports_yoy,
        "semi_exports_yoy": _load_motie("motie_semiconductor_exports_yoy"),
        "hynix_price_yoy": _load_price_yoy("000660"),
        "kospi_yoy": _load_price_yoy("0001"),
    }
    df = pd.DataFrame(series)
    df.index.name = "month"
    return df


# ── quarterly (QoQ) dataset ─────────────────────────────────────────────────
# 2026-08-17 사용자 요청 — 월별(YoY)과 별개로 분기별(QoQ) 관계도 보고 싶다.
# 반도체수출은 motie 수동 파일이 4개월치뿐이라 분기로 묶어봐야 최대 2개
# 분기 — 상관계수를 낼 표본이 못 된다. 그래서 QoQ는 실측 이력이 충분히 긴
# 총수출/하이닉스/코스피 3개만 다룬다(annual과 같은 3-시리즈 구성).

QOQ_SERIES_LABELS = {
    "total_exports_qoq": "총수출 (%QoQ)",
    "hynix_price_qoq": "SK하이닉스 주가 (%QoQ)",
    "kospi_qoq": "코스피 지수 (%QoQ)",
}
QOQ_SERIES_LABELS_CHART = {
    "total_exports_qoq": "Total exports (%QoQ)",
    "hynix_price_qoq": "SK Hynix price (%QoQ)",
    "kospi_qoq": "KOSPI index (%QoQ)",
}


def _current_incomplete_quarter_end() -> pd.Timestamp:
    """진행 중인(아직 안 끝난) 분기의 resample("QE") 라벨(그 분기 마지막 날짜)."""
    now = pd.Timestamp.now(tz="UTC").tz_localize(None)
    return now.to_period("Q").end_time.normalize()


def _drop_current_incomplete_quarter(level_quarterly: pd.Series) -> pd.Series:
    """resample("QE") 결과에서 진행 중인 이번 분기 라벨을 제거한다 — 수출
    합계뿐 아니라 가격의 "분기 마지막 관측치"도 마찬가지 문제를 겪는다:
    아직 안 끝난 분기의 "마지막 관측치"는 그 분기의 마지막 거래일이 아니라
    그냥 지금까지 중 가장 최근 거래일이라, 다음 달에 다시 돌리면 같은
    분기의 QoQ 값이 바뀐다(완결된 분기는 안 바뀌어야 정상)."""
    if level_quarterly.empty:
        return level_quarterly
    return level_quarterly[level_quarterly.index != _current_incomplete_quarter_end()]


def _quarterly_sum(level: pd.Series) -> pd.Series:
    """유량 변수(수출 달러)용 분기 집계 — 그 분기에 속한 월별 관측치를 전부
    더한다. 3개월이 다 안 채워진 분기는 버린다 — 2개월 합을 3개월 분기
    옆에 나란히 두면 부분월 문제가 분기 단위로 재발한다
    (_drop_current_incomplete_month가 부분월 자체는 이미 걸러내지만, 그래도
    한 분기에 1~2개월치만 쌓인 상태로 넘어올 수 있다)."""
    if level.empty:
        return level
    counts = level.resample("QE").count()
    totals = level.resample("QE").sum()
    return _drop_current_incomplete_quarter(totals[counts >= 3])


def _quarterly_last(level: pd.Series) -> pd.Series:
    """저량 변수(주가·지수 종가)용 분기 집계 — 그 분기의 마지막 관측치."""
    if level.empty:
        return level
    return _drop_current_incomplete_quarter(level.resample("QE").last())


def _qoq(level_quarterly: pd.Series) -> pd.Series:
    """분기 레벨 시리즈 -> %QoQ(직전 분기 대비)."""
    if level_quarterly.empty:
        return level_quarterly
    prior = level_quarterly.shift(1)
    return ((level_quarterly / prior - 1) * 100).dropna()


def build_qoq_dataset() -> pd.DataFrame:
    exports_level = _load_customs_export_level()
    hynix_level = _load_price_level("000660")
    kospi_level = _load_price_level("0001")
    series = {
        "total_exports_qoq": _qoq(_quarterly_sum(exports_level)),
        "hynix_price_qoq": _qoq(_quarterly_last(hynix_level)),
        "kospi_qoq": _qoq(_quarterly_last(kospi_level)),
    }
    df = pd.DataFrame(series)
    df.index.name = "quarter"
    return df


# ── daily-focus dataset (2026-08-17 추가) ───────────────────────────────────
# 사용자 요청: "최근 2년 정도를 집중해서", "지수가 발표되는 가장 짧은 주기의
# 값들로 데이터 해상도를 높여서 ... 매일 발표되는 것이 있다면 그건 다른
# 지표를 선행하여 그래프에 나타내줘". 하이닉스·코스피는 매일 거래되니
# 일봉(sources/daily-price-history.csv, collectors 아니라
# scripts.investor_flow daily-history가 채움)을 그대로 쓰고, 총수출은 원
# 주기가 월별이라(더 잘게 쪼갤 원천 데이터가 없다) 그대로 월별 %YoY.

DAILY_FOCUS_SERIES_LABELS = {
    "total_exports_yoy": "총수출 (%YoY, 월별)",
    "hynix_price_yoy_daily": "SK하이닉스 주가 (%YoY, 일별)",
    "kospi_yoy_daily": "코스피 지수 (%YoY, 일별)",
}
DAILY_FOCUS_SERIES_LABELS_CHART = {
    "total_exports_yoy": "Total exports (%YoY, monthly)",
    "hynix_price_yoy_daily": "SK Hynix price (%YoY, daily)",
    "kospi_yoy_daily": "KOSPI index (%YoY, daily)",
}


def _load_daily_price_level(code: str) -> pd.Series:
    """일봉 종가 레벨 — sources/daily-price-history.csv 기반(collectors가
    아니라 scripts.investor_flow daily-history CLI가 채운다). 이 파일이
    아직 없거나(최초 실행 전) 해당 code가 없으면 빈 시리즈."""
    if not DAILY_PRICE_CSV.exists():
        return pd.Series(dtype=float)
    df = pd.read_csv(DAILY_PRICE_CSV, dtype={"code": str})
    df = df[df["code"] == str(code)].copy()
    if df.empty:
        return pd.Series(dtype=float)
    df["date"] = pd.to_datetime(df["date"])
    s = df.sort_values("date").drop_duplicates(subset=["date"], keep="last").set_index("date")["close"]
    return s.sort_index()


def _daily_yoy(level: pd.Series, tolerance_days: int = 5) -> pd.Series:
    """일별 %YoY — 정확히 365일 전이 거래일이 아닐 수 있어(주말·공휴일)
    ±tolerance_days 안에서 가장 가까운 관측치를 찾는다. 그 범위 안에
    아무것도 없으면(이력이 아직 1년이 안 됐거나 구멍이 있으면) 그 날은
    건너뛴다 — 억지로 먼 값을 끌어써서 가짜 YoY를 만들지 않는다."""
    if level.empty:
        return level
    idx = level.index
    tol = pd.Timedelta(days=tolerance_days)
    yoy = {}
    for d, val in level.items():
        target = d - pd.DateOffset(years=1)
        window = idx[(idx >= target - tol) & (idx <= target + tol)]
        if window.empty:
            continue
        nearest = min(window, key=lambda x: abs((x - target).days))
        prior = level.loc[nearest]
        if prior:
            yoy[d] = (val / prior - 1) * 100
    return pd.Series(yoy, dtype=float).sort_index()


def _filter_from(series: pd.Series, cutoff: pd.Timestamp) -> pd.Series:
    """series.index >= cutoff, but empty()인 시리즈는 RangeIndex라 Timestamp와
    비교 자체가 TypeError — 그 경우 그대로 통과시킨다."""
    if series.empty:
        return series
    return series[series.index >= cutoff]


def build_daily_focus_dataset(display_days: int = DAILY_FOCUS_DISPLAY_DAYS) -> pd.DataFrame:
    cutoff = pd.Timestamp.now(tz="UTC").tz_localize(None) - pd.Timedelta(days=display_days)

    hynix_yoy = _daily_yoy(_load_daily_price_level("000660"))
    kospi_yoy = _daily_yoy(_load_daily_price_level("0001"))
    exports_yoy = _load_customs_export_yoy()  # 월별, 현재 진행 중인 달은 이미 제외됨

    hynix_yoy = _filter_from(hynix_yoy, cutoff)
    kospi_yoy = _filter_from(kospi_yoy, cutoff)
    exports_yoy = _filter_from(exports_yoy, cutoff)

    idx = hynix_yoy.index.union(kospi_yoy.index).union(exports_yoy.index).sort_values()
    df = pd.DataFrame(index=idx)
    df["total_exports_yoy"] = exports_yoy
    df["hynix_price_yoy_daily"] = hynix_yoy
    df["kospi_yoy_daily"] = kospi_yoy
    df.index.name = "date"
    return df


# ── annual (long-run) dataset ───────────────────────────────────────────────
# 2026-08-15 신설 — 사용자 요청("수출입동향과 코스피지수 관계를 가장 길고
# 오래된 데이터를 모두 가져와서"). 월별 실측(위 build_dataset)은 2026-04
# 이후뿐이라 n=4가 최선이었다 — 연간 결산 발표를 거슬러 올라가면 표본을
# n=7까지 늘릴 수 있다. 두 데이터셋은 성격이 달라(연간 vs 월별) 표/차트도
# 분리해서 낸다.

ANNUAL_SERIES_LABELS = {
    "total_exports_yoy": "총수출 (%YoY, 연간)",
    "semi_exports_yoy": "반도체수출 (%YoY, 연간)",
    "kospi_yoy": "코스피 지수 (%YoY, 연간)",
}
ANNUAL_SERIES_LABELS_CHART = {
    "total_exports_yoy": "Total exports (%YoY, annual)",
    "semi_exports_yoy": "Semiconductor exports (%YoY, annual)",
    "kospi_yoy": "KOSPI index (%YoY, annual)",
}


def _load_manual_yaml_series(path: Path, series_key: str) -> pd.Series:
    if not path.exists():
        return pd.Series(dtype=float)
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rows = payload.get("series", {}).get(series_key, [])
    if not rows:
        return pd.Series(dtype=float)
    s = pd.Series({pd.to_datetime(r["date"]): float(r["value"]) for r in rows})
    return s.sort_index()


def _load_kospi_annual_yoy() -> pd.Series:
    """Year-end KOSPI close -> %YoY between consecutive annual observations.

    Prefers a real KIS-collected December close from monthly-price-history.csv
    over the manually-sourced kospi_annual.yaml for any year both cover —
    once exports-price-correlation.yml has been collecting for a while, this
    lets the live source take over year by year without anyone editing the
    manual file."""
    manual = _load_manual_yaml_series(KOSPI_ANNUAL_YAML, "close")
    close_by_year: dict[int, float] = {d.year: v for d, v in manual.items()}

    if MONTHLY_PRICE_CSV.exists():
        # See the matching comment in _load_price_yoy — dtype=str is required
        # or "0001" round-trips through pandas as int 1 and never matches.
        df = pd.read_csv(MONTHLY_PRICE_CSV, dtype={"code": str})
        df = df[df["code"] == "0001"].copy()
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            december = df[df["date"].dt.month == 12]
            for year, group in december.groupby(december["date"].dt.year):
                close_by_year[int(year)] = float(group.sort_values("date")["close"].iloc[-1])

    years = sorted(close_by_year)
    yoy = {}
    for y in years:
        if (y - 1) in close_by_year and close_by_year[y - 1]:
            yoy[pd.Timestamp(year=y, month=1, day=1)] = (close_by_year[y] / close_by_year[y - 1] - 1) * 100
    return pd.Series(yoy, dtype=float).sort_index()


def build_annual_dataset() -> pd.DataFrame:
    series = {
        "total_exports_yoy": _load_manual_yaml_series(EXPORTS_ANNUAL_YAML, "total_exports_yoy"),
        "semi_exports_yoy": _load_manual_yaml_series(EXPORTS_ANNUAL_YAML, "semiconductor_exports_yoy"),
        "kospi_yoy": _load_kospi_annual_yoy(),
    }
    df = pd.DataFrame(series)
    df.index.name = "year"
    return df


def pairwise_correlations(df: pd.DataFrame) -> list[dict]:
    cols = list(df.columns)
    out = []
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            pair = df[[a, b]].dropna()
            n = len(pair)
            r = pair[a].corr(pair[b]) if n >= 2 else float("nan")
            out.append({"a": a, "b": b, "r": r, "n": n})
    out.sort(key=lambda row: (row["r"] is not None and not pd.isna(row["r"]), abs(row["r"]) if not pd.isna(row["r"]) else -1), reverse=True)
    return out


def render_markdown(df: pd.DataFrame, pairs: list[dict], preliminary: dict | None = None) -> str:
    lines = [
        "# 수출입동향 × SK하이닉스 × 코스피 상관관계",
        "",
        f"자동 생성 — `python -m scripts.correlation_analysis` "
        f"(source: data/normalized/customs_export_dlr.csv, data/normalized/motie_*.csv, "
        f"sources/monthly-price-history.csv)",
        "",
        "모든 값은 %YoY로 통일해 비교했다 — 성장률(수출)과 가격 수준(주가)을",
        "그대로 맞대면 둘 다 장기 우상향이라 원인 없이도 높은 상관계수가",
        "나오기 쉽다(추세 공유로 인한 가짜 상관). 4개 지표를 전부 같은",
        "종류(YoY 증가율)로 바꾼 뒤에야 비교가 의미를 가진다.",
        "",
        "## 표본 데이터",
        "",
        "| 월 | " + " | ".join(SERIES_LABELS.values()) + " |",
        "|---|" + "---|" * len(SERIES_LABELS),
    ]
    # reindex rather than raw column access — a caller (or a test) may pass a
    # frame missing a metric entirely (e.g. no price data collected yet);
    # that should render as "—" for every month, not crash the whole report.
    df_full = df.reindex(columns=list(SERIES_LABELS))
    for month, row in df_full.iterrows():
        cells = [f"{row[c]:.1f}" if pd.notna(row[c]) else "—" for c in SERIES_LABELS]
        lines.append(f"| {month.strftime('%Y-%m')} | " + " | ".join(cells) + " |")

    if preliminary is not None:
        lines += [
            "",
            f"## 진행 중인 달 잠정치 (아직 확정 아님)",
            "",
            f"**{preliminary['date'].strftime('%Y-%m')}** 총수출 %YoY 추정: "
            f"**{preliminary['value']:+.1f}%** — 관세청 {preliminary['label']} 잠정치를 그 달 "
            "전체의 %YoY로 근사한 값이다(2026-08-17 사용자 요청). 실제 발표값(관세청, "
            "다음 달 1일 확정치)과 다를 수 있다 — 상반월/월 전체의 조업일수·통관 타이밍 "
            "차이 때문. 위 표·상관계수 계산에는 포함하지 않았고, 차트에서만 점선+빈 "
            "마름모로 별도 표시했다.",
            f"\n출처: {preliminary['source']}" if preliminary.get("source") else "",
        ]

    lines += ["", "## 쌍별 상관계수 (Pearson r, 표본 많은/상관 높은 순)", "",
              "| 지표 A | 지표 B | r | n | 비고 |", "|---|---|---|---|---|"]
    for p in pairs:
        r = p["r"]
        r_str = f"{r:+.2f}" if pd.notna(r) else "계산불가"
        note = "" if pd.isna(r) else ("⚠ n<6 — 표본 부족, 신뢰 불가" if p["n"] < MIN_TRUSTWORTHY_N else "")
        lines.append(f"| {SERIES_LABELS[p['a']]} | {SERIES_LABELS[p['b']]} | {r_str} | {p['n']} | {note} |")

    no_price_data = all(pd.isna(p["r"]) for p in pairs
                         if "hynix_price_yoy" in (p["a"], p["b"]) or "kospi_yoy" in (p["a"], p["b"]))
    trustworthy = [p for p in pairs if pd.notna(p["r"]) and p["n"] >= MIN_TRUSTWORTHY_N]
    lines += ["", "## 해석"]
    if no_price_data:
        lines.append(
            "**가격 데이터가 아직 없다** — `sources/monthly-price-history.csv`가 "
            "비어 있어 수출-주가/지수 상관은 전부 계산 불가(n=0). "
            "`python -m scripts.investor_flow monthly-history --code 000660 ...`와 "
            "`--code 0001 --is-index`를 실행해 KIS 월봉을 채운 뒤 이 스크립트를 "
            "다시 돌리면 채워진다. 아래는 그때까지 계산 가능한 두 수출 지표 "
            "간의 참고용 상관일 뿐, 사용자가 물은 '수출-주가 상관관계'가 아니다."
        )
    if trustworthy:
        top = trustworthy[0]
        lines.append(
            f"표본이 {MIN_TRUSTWORTHY_N}개월 이상인 쌍 중 가장 강한 상관: "
            f"**{SERIES_LABELS[top['a']]} ↔ {SERIES_LABELS[top['b']]}** "
            f"(r={top['r']:+.2f}, n={top['n']}). 아래 차트 참고."
        )
    else:
        best = pairs[0] if pairs else None
        if best and pd.notna(best["r"]):
            lines.append(
                f"현재 모든 쌍이 표본 {MIN_TRUSTWORTHY_N}개월 미만이다 — 가장 높은 "
                f"상관(r={best['r']:+.2f}, n={best['n']})조차 결론을 내리기엔 이르다. "
                f"KIS 월봉 이력이 쌓일수록(매월 자동 갱신) n이 늘어나고 신뢰도가 오른다."
            )
        else:
            lines.append("아직 두 지표를 겹쳐볼 수 있는 달이 없다 — 월봉 이력이 더 필요하다.")
    # 2026-08-17 이전엔 총수출이 motie 수동 파일(2026-04~)뿐이라 "수출입동향은
    # 4개월분"이 표본을 제한하는 진짜 이유였다. 관세청 실측(1990.01~)이 붙은
    # 뒤로는 그 문장이 거짓이 됐다 — 지금 표본을 실제로 제한하는 건 보통 가격
    # 계열(KIS 월봉 이력이 짧음) 쪽이다. 하드코딩 대신 실제 non-null 개수를
    # 비교해서 매번 맞는 쪽을 지목한다.
    counts = {c: int(df_full[c].notna().sum()) for c in SERIES_LABELS}
    available = {c: n for c, n in counts.items() if n > 0}
    if available:
        shortest_col = min(available, key=available.get)
        longest_col = max(available, key=available.get)
        if shortest_col != longest_col and available[shortest_col] < available[longest_col]:
            limit_note = (
                f"현재 표본을 실제로 제한하는 지표는 **{SERIES_LABELS[shortest_col]}**"
                f"({available[shortest_col]}개월치)다 — {SERIES_LABELS[longest_col]}은 "
                f"{available[longest_col]}개월치까지 있지만, 상관계수는 두 지표가 "
                f"겹치는 달만 쓸 수 있어 짧은 쪽에 맞춰진다."
            )
        else:
            limit_note = f"모든 지표가 {available[shortest_col]}개월치로 표본 크기가 같다."
    else:
        limit_note = "아직 어떤 지표도 데이터가 없다."
    lines.append(
        f"\n**한계**: {limit_note} 상관계수가 높게 나와도 n이 작으면 우연일 "
        "가능성을 배제할 수 없다. n이 10 미만이면 방향성 참고 이상으로 쓰지 말 것."
    )
    return "\n".join(lines) + "\n"


def render_annual_markdown(df: pd.DataFrame, pairs: list[dict]) -> str:
    lines = [
        "# 수출입동향 × 코스피 지수 — 연간 장기 비교 (2019~2025)",
        "",
        "자동 생성 — `python -m scripts.correlation_analysis` "
        "(source: data/manual_inputs/exports_annual.yaml, "
        "data/manual_inputs/kospi_annual.yaml 또는 sources/monthly-price-history.csv)",
        "",
        "월별 실측(수출입동향 2026-04~)만으로는 표본이 4개월뿐이라, 산업통상부의",
        "연간 결산 발표를 거슬러 올라가 표본을 늘린 별도 분석이다. 월별 분석과",
        "마찬가지로 %YoY로 통일해 비교한다(추세 공유로 인한 가짜 상관 방지).",
        "",
        "## 표본 데이터",
        "",
        "| 연도 | " + " | ".join(ANNUAL_SERIES_LABELS.values()) + " |",
        "|---|" + "---|" * len(ANNUAL_SERIES_LABELS),
    ]
    df_full = df.reindex(columns=list(ANNUAL_SERIES_LABELS))
    for year, row in df_full.iterrows():
        cells = [f"{row[c]:.1f}" if pd.notna(row[c]) else "—" for c in ANNUAL_SERIES_LABELS]
        lines.append(f"| {year.strftime('%Y')} | " + " | ".join(cells) + " |")

    lines += ["", "## 쌍별 상관계수 (Pearson r, 표본 많은/상관 높은 순)", "",
              "| 지표 A | 지표 B | r | n | 비고 |", "|---|---|---|---|---|"]
    for p in pairs:
        r = p["r"]
        r_str = f"{r:+.2f}" if pd.notna(r) else "계산불가"
        note = "" if pd.isna(r) else ("⚠ n<6 — 표본 부족, 신뢰 불가" if p["n"] < MIN_TRUSTWORTHY_N else "")
        lines.append(f"| {ANNUAL_SERIES_LABELS[p['a']]} | {ANNUAL_SERIES_LABELS[p['b']]} | {r_str} | {p['n']} | {note} |")

    trustworthy = [p for p in pairs if pd.notna(p["r"]) and p["n"] >= MIN_TRUSTWORTHY_N]
    lines += ["", "## 해석"]
    if trustworthy:
        top = trustworthy[0]
        lines.append(
            f"표본이 {MIN_TRUSTWORTHY_N}개 연도 이상인 쌍 중 가장 강한 상관: "
            f"**{ANNUAL_SERIES_LABELS[top['a']]} ↔ {ANNUAL_SERIES_LABELS[top['b']]}** "
            f"(r={top['r']:+.2f}, n={top['n']}). 아래 차트 참고."
        )
    else:
        best = pairs[0] if pairs else None
        if best and pd.notna(best["r"]):
            lines.append(
                f"모든 쌍이 표본 {MIN_TRUSTWORTHY_N}개 연도 미만이다 — 가장 높은 "
                f"상관(r={best['r']:+.2f}, n={best['n']})조차 결론을 내리기엔 이르다."
            )
        else:
            lines.append("두 지표를 겹쳐볼 수 있는 연도가 아직 없다.")
    lines.append(
        "\n**한계**: 연 단위 관측 7개(2019~2025)로는 표본이 여전히 작다 — "
        "일반적으로 상관계수를 어느 정도 신뢰하려면 n≥10~15가 바람직하다. "
        "이 결과는 방향성 참고이지 인과관계의 증거가 아니다. 또한 각 지표는 "
        "서로 다른 시점의 집계(수출은 연중 누계, 코스피는 그 해 마지막 거래일)라 "
        "완전히 동시점 비교는 아니다."
    )
    return "\n".join(lines) + "\n"


def render_qoq_markdown(df: pd.DataFrame, pairs: list[dict]) -> str:
    lines = [
        "# 수출입동향 × SK하이닉스 × 코스피 — 분기별(QoQ) 비교",
        "",
        "자동 생성 — `python -m scripts.correlation_analysis` "
        "(source: data/normalized/customs_export_dlr.csv, "
        "sources/monthly-price-history.csv)",
        "",
        "월별(%YoY, exports-price-correlation.md)과 달리 여기는 직전 분기 대비",
        "%QoQ다 — 분기 단위로 방향이 바뀌는 지점(전분기보다 늘었다/줄었다)을",
        "보려는 목적. 수출은 그 분기 3개월 합계, 주가·지수는 그 분기 마지막",
        "거래일 종가를 쓴다. 진행 중인(아직 안 끝난) 이번 달/분기는 제외했다 —",
        "부분월 데이터를 완결된 분기와 나란히 비교하면 착시가 생긴다.",
        "",
        "## 표본 데이터",
        "",
        "| 분기 | " + " | ".join(QOQ_SERIES_LABELS.values()) + " |",
        "|---|" + "---|" * len(QOQ_SERIES_LABELS),
    ]
    df_full = df.reindex(columns=list(QOQ_SERIES_LABELS))
    for quarter, row in df_full.iterrows():
        q_label = f"{quarter.year}Q{quarter.quarter}"
        cells = [f"{row[c]:.1f}" if pd.notna(row[c]) else "—" for c in QOQ_SERIES_LABELS]
        lines.append(f"| {q_label} | " + " | ".join(cells) + " |")

    lines += ["", "## 쌍별 상관계수 (Pearson r, 표본 많은/상관 높은 순)", "",
              "| 지표 A | 지표 B | r | n | 비고 |", "|---|---|---|---|---|"]
    for p in pairs:
        r = p["r"]
        r_str = f"{r:+.2f}" if pd.notna(r) else "계산불가"
        note = "" if pd.isna(r) else ("⚠ n<6 — 표본 부족, 신뢰 불가" if p["n"] < MIN_TRUSTWORTHY_N else "")
        lines.append(f"| {QOQ_SERIES_LABELS[p['a']]} | {QOQ_SERIES_LABELS[p['b']]} | {r_str} | {p['n']} | {note} |")

    trustworthy = [p for p in pairs if pd.notna(p["r"]) and p["n"] >= MIN_TRUSTWORTHY_N]
    lines += ["", "## 해석"]
    if trustworthy:
        top = trustworthy[0]
        lines.append(
            f"표본이 {MIN_TRUSTWORTHY_N}개 분기 이상인 쌍 중 가장 강한 상관: "
            f"**{QOQ_SERIES_LABELS[top['a']]} ↔ {QOQ_SERIES_LABELS[top['b']]}** "
            f"(r={top['r']:+.2f}, n={top['n']}). 아래 차트 참고."
        )
    else:
        best = pairs[0] if pairs else None
        if best and pd.notna(best["r"]):
            lines.append(
                f"현재 모든 쌍이 표본 {MIN_TRUSTWORTHY_N}개 분기 미만이다 — 가장 높은 "
                f"상관(r={best['r']:+.2f}, n={best['n']})조차 결론을 내리기엔 이르다."
            )
        else:
            lines.append("두 지표를 겹쳐볼 수 있는 분기가 아직 없다.")
    lines.append(
        "\n**한계**: QoQ는 YoY보다 계절성(예: 반도체 수출은 통상 4분기가 강함)에 "
        "더 취약하다 — 분기별 등락이 계절 패턴 때문인지 추세 전환인지 이 표만으로는 "
        "구분 못 한다. 상관계수가 높게 나와도 n이 작으면 우연일 가능성을 배제할 수 "
        "없다. n이 10 미만이면 방향성 참고 이상으로 쓰지 말 것."
    )
    return "\n".join(lines) + "\n"


# 월별 차트 색상 — annual 차트(render_annual_chart)와 지표별로 같은 색을
# 재사용한다(파랑=총수출, 초록=코스피, 주황=하이닉스/반도체수출) — 필터·차트가
# 바뀌어도 "이 색은 이 지표"가 유지돼야 식별이 색 자체가 아니라 범례에
# 의존하지 않는다.
MONTHLY_CHART_COLORS = {
    "total_exports_yoy": "#2a78d6",
    "hynix_price_yoy": "#eb6834",
    "kospi_yoy": "#3fa34d",
    "semi_exports_yoy": "#a35fd1",
}


def _render_monthly_chart(df: pd.DataFrame, top_pair: dict | None, out_path: Path,
                           start: pd.Timestamp | None = None, title_note: str = "",
                           markersize: float | None = None,
                           preliminary: dict | None = None) -> None:
    """render_chart의 실제 구현 — start를 주면 그 시점부터만 잘라서 그린다
    (2026-08-17 사용자 요청: "2023년부터 zoom in"). z-score는 잘린 구간
    안에서 다시 계산한다 — 전체 이력 기준 z-score를 그대로 쓰면 최근 구간이
    이미 전체 차트에서 보이는 것과 똑같은 모양으로 눌려 나온다(총수출처럼
    1990~ 표본이 긴 지표일수록 심함); 구간 안에서 재정규화해야 그 구간
    자체의 등락폭이 자기 스케일로 드러난다 — "확대"의 실질적 의미.

    markersize: None이면 점 없이 선만(전체 이력 차트 — 500개월치를 점까지
    찍으면 너무 빽빽하다). 확대 차트는 표본이 훨씬 적어(3년 안팎) 작은 점을
    찍어도 안 빽빽하고, 사용자가 명시적으로 요청(2026-08-17).

    preliminary: load_exports_preliminary()의 반환값 — 진행 중인 달의
    "다음 점"을 관세청 10일 단위 잠정치로 미리 찍어본다(2026-08-17 사용자
    요청: "잠정치로 예측 가능한 다음 점을 찍어보자"). total_exports_yoy의
    실측 마지막 점에서 점선으로 이어지는 속이 빈 마름모로 그린다 — 실측과
    같은 파란색이지만 선 스타일과 마커를 확실히 다르게 해서 "이건 확정치가
    아니다"가 범례만 봐도 드러나게 한다. z-score는 실측 total_exports_yoy
    시리즈의 평균/표준편차를 그대로 재사용한다(잠정치 자체를 평균/표준편차
    계산에 넣지 않는다 — 아직 확정 안 된 값이 정규화 기준을 흔들면 안 된다)."""
    if top_pair is None:
        return
    cols = [c for c in ("total_exports_yoy", "hynix_price_yoy", "kospi_yoy") if c in df.columns]
    plot_df = df[cols].dropna(how="all")
    if start is not None:
        plot_df = plot_df[plot_df.index >= start]
    if plot_df.empty:
        return

    # 2026-08-17: 사용자 요청 — 점 마커를 없애고 선을 얇게 해서(1.8→1.1) 세
    # 곡선의 상승/하강이 점에 가려지지 않고 잘 보이도록.
    fig, ax = plt.subplots(figsize=(10, 5))
    exports_stats = None  # (mean, std, last_date, last_z) — 잠정치 점을 실측과 같은 척도로 찍기 위해 기억해둔다
    for c in cols:
        series = plot_df[c].dropna()
        if series.empty:
            continue
        mean, std = series.mean(), series.std(ddof=0)
        z = (series - mean) / std
        marker_kwargs = {"marker": "o", "markersize": markersize} if markersize else {}
        ax.plot(z.index, z.values, linewidth=1.1,
                color=MONTHLY_CHART_COLORS.get(c, "#888888"), label=SERIES_LABELS_CHART[c],
                **marker_kwargs)
        if c == "total_exports_yoy":
            exports_stats = (mean, std, z.index[-1], z.values[-1])

    if preliminary is not None and exports_stats is not None:
        mean, std, last_date, last_z = exports_stats
        prelim_date, prelim_value = preliminary["date"], preliminary["value"]
        if start is None or prelim_date >= start:
            prelim_z = (prelim_value - mean) / std
            color = MONTHLY_CHART_COLORS["total_exports_yoy"]
            ax.plot([last_date, prelim_date], [last_z, prelim_z], linestyle="--", linewidth=1.1,
                    color=color, alpha=0.7)
            ax.plot([prelim_date], [prelim_z], marker="D", markersize=7, markerfacecolor="none",
                    markeredgecolor=color, markeredgewidth=1.5, linestyle="none",
                    label=f"Total exports (%YoY, {preliminary['label_en']})")

    ax.axhline(0, color="#999999", linewidth=0.8, linestyle="--")
    ax.set_title(
        f"Exports vs SK Hynix vs KOSPI, monthly (%YoY, z-score normalized){title_note}\n"
        f"strongest pair (full history): {SERIES_LABELS_CHART[top_pair['a']]} vs "
        f"{SERIES_LABELS_CHART[top_pair['b']]} (r={top_pair['r']:+.2f}, n={top_pair['n']})",
        fontsize=11,
    )
    ax.set_ylabel("z-score (mean 0, std 1)")
    ax.set_xlabel("month")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def render_chart(df: pd.DataFrame, top_pair: dict | None, preliminary: dict | None = None) -> None:
    """2026-08-17: 사용자가 총수출도 같이 그려달라고 요청 — 원래는 상관 가장
    높은 쌍(하이닉스 vs 코스피) 2개 지표만 그렸는데, render_annual_chart와
    같은 방식(전 지표를 z-score로 겹쳐 그리기)으로 통일했다. 총수출은
    1990~이라 표본이 훨씬 길지만, z-score는 각 지표를 자기 자신의 평균/표준
    편차로 정규화하므로 그 변동폭이 다른 지표에 묻히지 않고 그대로 보인다."""
    _render_monthly_chart(df, top_pair, OUT_PNG, preliminary=preliminary)


def render_chart_zoom(df: pd.DataFrame, top_pair: dict | None, start: pd.Timestamp,
                       preliminary: dict | None = None) -> None:
    """render_chart의 확대판 — start 이후 구간만, 그 구간 안에서 재정규화해
    그린다(위 _render_monthly_chart 참고). 작은 점 마커 포함(2026-08-17
    사용자 요청)."""
    _render_monthly_chart(df, top_pair, OUT_PNG_ZOOM, start=start,
                           title_note=f" — {start.strftime('%Y-%m')}~", markersize=3.5,
                           preliminary=preliminary)


def render_annual_chart(df: pd.DataFrame, top_pair: dict | None) -> None:
    """Same all-series-overlaid approach as render_chart (both were originally
    top-pair-only; render_chart switched to this pattern 2026-08-17 per user
    request to show total exports alongside price) — showing every metric is
    more informative than picking just the best-correlated two, and is closer
    to what was actually asked for ("관계를 그래프를 그려보자").

    2026-08-17: 점 마커 제거 + 선 얇게(2→1.1) — 월별/QoQ 차트에 적용한 것과
    같은 스타일로 통일해달라는 사용자 요청. 연간은 표본이 7개뿐이라 마커
    없이는 개별 관측치가 잘 안 보일 수 있지만, 세 차트가 같은 관례를
    따르는 쪽을 우선한다."""
    cols = [c for c in ANNUAL_SERIES_LABELS if c in df.columns and df[c].notna().any()]
    plot_df = df[cols].dropna(how="all")
    if plot_df.empty:
        return
    z = (plot_df - plot_df.mean()) / plot_df.std(ddof=0)

    colors = {"total_exports_yoy": "#2a78d6", "semi_exports_yoy": "#eb6834", "kospi_yoy": "#3fa34d"}
    fig, ax = plt.subplots(figsize=(9, 5))
    for c in cols:
        series = z[c].dropna()
        ax.plot(series.index, series.values, linewidth=1.1,
                color=colors.get(c, "#888888"), label=ANNUAL_SERIES_LABELS_CHART[c])
    ax.axhline(0, color="#999999", linewidth=0.8, linestyle="--")
    title = "Exports vs KOSPI, annual (%YoY, z-score normalized)"
    if top_pair is not None:
        title += f"\nstrongest pair: {ANNUAL_SERIES_LABELS_CHART[top_pair['a']]} vs " \
                  f"{ANNUAL_SERIES_LABELS_CHART[top_pair['b']]} (r={top_pair['r']:+.2f}, n={top_pair['n']})"
    ax.set_title(title, fontsize=11)
    ax.set_ylabel("z-score (mean 0, std 1)")
    ax.set_xlabel("year")
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG_ANNUAL, dpi=150)
    plt.close(fig)


def render_qoq_chart(df: pd.DataFrame, top_pair: dict | None) -> None:
    """render_chart(월별)와 같은 스타일(점 없이 얇은 선, 지표별 고정 색) —
    2026-08-17 사용자 요청으로 월별 차트를 이렇게 바꾼 직후라 QoQ도 처음부터
    같은 관례를 따른다."""
    cols = [c for c in QOQ_SERIES_LABELS if c in df.columns and df[c].notna().any()]
    plot_df = df[cols].dropna(how="all")
    if plot_df.empty:
        return

    colors = {"total_exports_qoq": "#2a78d6", "hynix_price_qoq": "#eb6834", "kospi_qoq": "#3fa34d"}
    fig, ax = plt.subplots(figsize=(10, 5))
    for c in cols:
        series = plot_df[c].dropna()
        if series.empty:
            continue
        z = (series - series.mean()) / series.std(ddof=0)
        ax.plot(z.index, z.values, linewidth=1.1,
                color=colors.get(c, "#888888"), label=QOQ_SERIES_LABELS_CHART[c])
    ax.axhline(0, color="#999999", linewidth=0.8, linestyle="--")
    title = "Exports vs SK Hynix vs KOSPI, quarterly (%QoQ, z-score normalized)"
    if top_pair is not None:
        title += f"\nstrongest pair: {QOQ_SERIES_LABELS_CHART[top_pair['a']]} vs " \
                  f"{QOQ_SERIES_LABELS_CHART[top_pair['b']]} (r={top_pair['r']:+.2f}, n={top_pair['n']})"
    ax.set_title(title, fontsize=11)
    ax.set_ylabel("z-score (mean 0, std 1)")
    ax.set_xlabel("quarter")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG_QOQ, dpi=150)
    plt.close(fig)


DAILY_FOCUS_CHART_COLORS = {
    "total_exports_yoy": "#2a78d6",
    "hynix_price_yoy_daily": "#eb6834",
    "kospi_yoy_daily": "#3fa34d",
}


def render_daily_focus_chart(df: pd.DataFrame) -> dict | None:
    """일봉(하이닉스·코스피) + 월별(총수출) 오버레이 — 사용자가 계속
    트레이스하자고 한 차트(2026-08-17). 총수출은 한 달에 한 점뿐이라 작은
    점으로, 하이닉스·코스피는 매일이라 촘촘한 선으로 — 그 밀도 차이 자체가
    "매일 발표되는 지표가 선행해 보인다"는 요청을 시각적으로 만족시킨다
    (인위적으로 시점을 당기지 않는다 — 그건 실제로 검증 안 된 리드-래그
    주장이 되어버린다).

    각 시리즈는 이 표시 구간(기본 2년) 안에서 z-score 재정규화한다 —
    render_chart_zoom과 같은 이유."""
    cols = [c for c in DAILY_FOCUS_SERIES_LABELS if c in df.columns and df[c].notna().any()]
    plot_df = df[cols]
    if plot_df.dropna(how="all").empty:
        return None

    fig, ax = plt.subplots(figsize=(11, 5.5))
    for c in cols:
        series = plot_df[c].dropna()
        if series.empty:
            continue
        z = (series - series.mean()) / series.std(ddof=0)
        is_monthly = c == "total_exports_yoy"
        marker_kwargs = {"marker": "o", "markersize": 4} if is_monthly else {}
        ax.plot(z.index, z.values, linewidth=1.1 if not is_monthly else 1.3,
                color=DAILY_FOCUS_CHART_COLORS.get(c, "#888888"),
                label=DAILY_FOCUS_SERIES_LABELS_CHART[c], **marker_kwargs)
    ax.axhline(0, color="#999999", linewidth=0.8, linestyle="--")

    corr_note = ""
    daily_pair = None
    if "hynix_price_yoy_daily" in plot_df.columns and "kospi_yoy_daily" in plot_df.columns:
        pair = plot_df[["hynix_price_yoy_daily", "kospi_yoy_daily"]].dropna()
        if len(pair) >= 2:
            r = pair["hynix_price_yoy_daily"].corr(pair["kospi_yoy_daily"])
            n = len(pair)
            daily_pair = {"r": r, "n": n}
            corr_note = f"\nSK Hynix vs KOSPI (daily, same-day): r={r:+.2f}, n={n}"

    ax.set_title(
        f"Exports (monthly) vs SK Hynix vs KOSPI (daily), %YoY, z-score normalized"
        f" — last {DAILY_FOCUS_DISPLAY_DAYS} days{corr_note}",
        fontsize=11,
    )
    ax.set_ylabel("z-score (mean 0, std 1)")
    ax.set_xlabel("date")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG_DAILY_FOCUS, dpi=150)
    plt.close(fig)
    return daily_pair


def render_daily_focus_markdown(df: pd.DataFrame, daily_pair: dict | None) -> str:
    """전체 일별 표는 안 낸다(2년치면 수백 행) — 최근 관측치 요약 + 상관계수만.
    실제 상세 데이터는 sources/daily-price-history.csv,
    data/normalized/customs_export_dlr.csv에 그대로 있다."""
    lines = [
        "# SK하이닉스 vs 코스피 vs 총수출 — 일별 확대 추적",
        "",
        "자동 생성 — `python -m scripts.correlation_analysis` "
        "(source: sources/daily-price-history.csv, "
        "data/normalized/customs_export_dlr.csv)",
        "",
        f"최근 {DAILY_FOCUS_DISPLAY_DAYS}일(약 2년)만 — 총수출은 원 주기(월별) 그대로, "
        "하이닉스·코스피는 원 주기(일별) 그대로 겹쳐 그린다. 매일 갱신되는 "
        "가격 계열이 한 달에 한 번 찍히는 총수출보다 항상 더 최근 날짜까지 "
        "그려지므로, 인위적인 시점 이동 없이도 '더 자주 발표되는 지표가 "
        "앞서 보인다'가 성립한다.",
        "",
        "사용자 관전 포인트(2026-08-17): 하이닉스 주가가 총수출을 급격히 "
        "따돌리고 올라간 뒤 급락하며 총수출 추세선을 뚫고 내려갔다가, 다시 "
        "말려 올라올지를 이 차트로 계속 트레이스한다.",
        "",
        "## 최근 관측치",
        "",
    ]
    tail_cols = [c for c in DAILY_FOCUS_SERIES_LABELS if c in df.columns]
    tail = df[tail_cols].dropna(how="all").tail(10)
    if tail.empty:
        lines.append("데이터 없음 — sources/daily-price-history.csv를 먼저 채우세요 "
                      "(`python -m scripts.investor_flow daily-history ...`).")
    else:
        lines.append("| 날짜 | " + " | ".join(DAILY_FOCUS_SERIES_LABELS[c] for c in tail_cols) + " |")
        lines.append("|---|" + "---|" * len(tail_cols))
        for d, row in tail.iterrows():
            cells = [f"{row[c]:.1f}" if pd.notna(row[c]) else "—" for c in tail_cols]
            lines.append(f"| {d.strftime('%Y-%m-%d')} | " + " | ".join(cells) + " |")
    lines += ["", "## 상관계수"]
    if daily_pair is not None:
        note = "" if daily_pair["n"] >= MIN_TRUSTWORTHY_N else "⚠ 표본 부족, 신뢰 불가"
        lines.append(
            f"SK하이닉스 주가 (%YoY, 일별) ↔ 코스피 지수 (%YoY, 일별): "
            f"r={daily_pair['r']:+.2f}, n={daily_pair['n']} {note}"
        )
    else:
        lines.append("하이닉스·코스피 일봉이 아직 부족해 계산 불가.")
    lines.append(
        "\n총수출(월별)은 하이닉스·코스피(일별)와 주기가 달라 이 표에서 상관계수를 "
        "내지 않는다 — 정확히 같은 날짜에 값이 있는 경우가 우연이 아니면 없어서 "
        "표본이 사실상 0이 된다. 세 지표의 관계는 위 차트(시각적 겹침)로, "
        "정량적 상관은 exports-price-correlation.md(월별)·-qoq.md(분기별)를 참고."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    df = build_dataset()
    if df.dropna(how="all").empty:
        print("입력 데이터가 전혀 없습니다 — motie exports.yaml과 "
              "sources/monthly-price-history.csv를 먼저 채우세요.", file=sys.stderr)
        return 1

    pairs = pairwise_correlations(df)
    preliminary = load_exports_preliminary()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_markdown(df, pairs, preliminary=preliminary), encoding="utf-8")

    trustworthy = [p for p in pairs if pd.notna(p["r"]) and p["n"] >= MIN_TRUSTWORTHY_N]
    top_pair = trustworthy[0] if trustworthy else (pairs[0] if pairs and pd.notna(pairs[0]["r"]) else None)
    render_chart(df, top_pair, preliminary=preliminary)
    render_chart_zoom(df, top_pair, ZOOM_START, preliminary=preliminary)

    print(f"[월별] {len(pairs)}개 쌍 계산 완료 → {OUT_MD}")
    if OUT_PNG.exists():
        print(f"[월별] 차트 저장 → {OUT_PNG}")
    if OUT_PNG_ZOOM.exists():
        print(f"[월별 확대 {ZOOM_START.strftime('%Y-%m')}~] 차트 저장 → {OUT_PNG_ZOOM}")
    if preliminary is not None:
        print(f"  잠정치 다음 점: {preliminary['date'].strftime('%Y-%m')} "
              f"{preliminary['value']:+.1f}% ({preliminary['label']})")
    for p in pairs:
        r_str = f"{p['r']:+.2f}" if pd.notna(p["r"]) else "N/A"
        print(f"  {p['a']:<18} x {p['b']:<18} r={r_str} n={p['n']}")

    # ── annual (long-run) ────────────────────────────────────────────────
    adf = build_annual_dataset()
    if not adf.dropna(how="all").empty:
        apairs = pairwise_correlations(adf)
        OUT_MD_ANNUAL.write_text(render_annual_markdown(adf, apairs), encoding="utf-8")
        a_trustworthy = [p for p in apairs if pd.notna(p["r"]) and p["n"] >= MIN_TRUSTWORTHY_N]
        a_top_pair = a_trustworthy[0] if a_trustworthy else (apairs[0] if apairs and pd.notna(apairs[0]["r"]) else None)
        render_annual_chart(adf, a_top_pair)

        print(f"\n[연간] {len(apairs)}개 쌍 계산 완료 → {OUT_MD_ANNUAL}")
        if OUT_PNG_ANNUAL.exists():
            print(f"[연간] 차트 저장 → {OUT_PNG_ANNUAL}")
        for p in apairs:
            r_str = f"{p['r']:+.2f}" if pd.notna(p["r"]) else "N/A"
            print(f"  {p['a']:<18} x {p['b']:<18} r={r_str} n={p['n']}")
    else:
        print("\n[연간] 입력 데이터 없음 — data/manual_inputs/exports_annual.yaml, "
              "kospi_annual.yaml 확인 필요", file=sys.stderr)

    # ── quarterly (QoQ) ──────────────────────────────────────────────────
    qdf = build_qoq_dataset()
    if not qdf.dropna(how="all").empty:
        qpairs = pairwise_correlations(qdf)
        OUT_MD_QOQ.write_text(render_qoq_markdown(qdf, qpairs), encoding="utf-8")
        q_trustworthy = [p for p in qpairs if pd.notna(p["r"]) and p["n"] >= MIN_TRUSTWORTHY_N]
        q_top_pair = q_trustworthy[0] if q_trustworthy else (qpairs[0] if qpairs and pd.notna(qpairs[0]["r"]) else None)
        render_qoq_chart(qdf, q_top_pair)

        print(f"\n[분기] {len(qpairs)}개 쌍 계산 완료 → {OUT_MD_QOQ}")
        if OUT_PNG_QOQ.exists():
            print(f"[분기] 차트 저장 → {OUT_PNG_QOQ}")
        for p in qpairs:
            r_str = f"{p['r']:+.2f}" if pd.notna(p["r"]) else "N/A"
            print(f"  {p['a']:<18} x {p['b']:<18} r={r_str} n={p['n']}")
    else:
        print("\n[분기] 입력 데이터 없음 — data/normalized/customs_export_dlr.csv, "
              "sources/monthly-price-history.csv 확인 필요", file=sys.stderr)

    # ── daily focus (2년, 일봉) ──────────────────────────────────────────
    ddf = build_daily_focus_dataset()
    if not ddf.dropna(how="all").empty:
        daily_pair = render_daily_focus_chart(ddf)
        OUT_MD_DAILY_FOCUS.write_text(render_daily_focus_markdown(ddf, daily_pair), encoding="utf-8")
        print(f"\n[일별 확대] {OUT_MD_DAILY_FOCUS}")
        if OUT_PNG_DAILY_FOCUS.exists():
            print(f"[일별 확대] 차트 저장 → {OUT_PNG_DAILY_FOCUS}")
        if daily_pair is not None:
            print(f"  hynix_price_yoy_daily x kospi_yoy_daily  r={daily_pair['r']:+.2f} n={daily_pair['n']}")
    else:
        print("\n[일별 확대] 입력 데이터 없음 — sources/daily-price-history.csv 확인 필요 "
              "(python -m scripts.investor_flow daily-history ...)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
