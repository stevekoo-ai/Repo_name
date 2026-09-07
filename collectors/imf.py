"""IMF World Economic Outlook (WEO) collector — 국가별 거시 지표 + **전망치**.

2026-09-07 신설. config/api.yaml에 등록만 돼 있고 collectors 구현이 없어
한 번도 쓰인 적 없던 소스 — API 전수 프로브에서 살아 있는 게 확인돼
(KOR 실질GDP성장률 1980~2031 수신) 채웠다.

**이 소스가 다른 소스와 결정적으로 다른 점: 미래 값이 들어 있다.**
FRED/ECOS/KOSIS/BLS는 전부 이미 일어난 일(실측)만 준다. IMF WEO는 연 2회
(4월·10월) 갱신되는 공식 전망을 함께 싣는다 — 2026년 9월 현재 2031년까지의
전망이 들어온다.

그래서 이 모듈은 **실측과 전망을 반드시 분리해서 저장한다**:
- `imf_<지표>_<국가>` — 관측된 과거만
- `imf_<지표>_<국가>_forecast` — 전망 구간만

섞으면 리포트가 "예측을 실측으로" 제시하게 된다. 이 저장소의 R1(실측 우선)
·R3(미수집은 판정이 아니다)와 같은 계열의 규칙이다. 전망은 근거로 쓰되
실측인 척하면 안 된다.

경계선(cutoff)은 이 API가 알려주지 않으므로 추정한다 — WEO는 발표 시점의
직전 완결 연도까지를 실측으로 본다. 보수적으로 **작년까지 실측, 올해부터
전망**으로 나눈다(올해 값은 아직 연중이라 어차피 추정치다).

주의: datamapper API는 다른 소스보다 느리다(프로브 실측 10.4초) — 타임아웃을
넉넉히 준다.
"""
from __future__ import annotations

from datetime import date, datetime

import requests

from core import cache as cache_mod
from core.config import api_config
from core.logger import log_event
from core.models import DataPoint, DataStatus, Frequency, Metadata
from . import base

_TIMEOUT_SECONDS = (15, 45)   # datamapper는 느리다 — 프로브 실측 10.4초

# series_key -> (WEO 지표 코드, 설명, 단위)
IMF_SERIES: dict[str, tuple[str, str, str]] = {
    "gdp_growth": ("NGDP_RPCH", "실질 GDP 성장률(연간, %)", "%"),
    "inflation": ("PCPIPCH", "소비자물가 상승률(연평균, %)", "%"),
    "current_account": ("BCA_NGDPD", "경상수지(GDP 대비 %)", "% of GDP"),
    "govt_debt": ("GGXWDG_NGDP", "일반정부 총부채(GDP 대비 %)", "% of GDP"),
    "unemployment": ("LUR", "실업률(연간, %)", "%"),
}

# 이 저장소가 실제로 비교하는 나라들 — 한국을 중심에 두고 미·중·일.
# 2026-09-07 대화의 4개국 통화 분석과 같은 비교군이라 환율 서사와 붙는다.
COUNTRIES = ["KOR", "USA", "CHN", "JPN"]


def _fetch(indicator: str, country: str) -> dict[str, float]:
    """{연도(str): 값} — API가 주는 원형 그대로. 실측/전망 분리는 상위에서."""
    base_url = api_config()["sources"]["imf"]["base_url"]
    resp = requests.get(f"{base_url}/{indicator}/{country}", timeout=_TIMEOUT_SECONDS)
    base.raise_for_status(resp)
    payload = resp.json()
    values = (payload.get("values", {}) or {}).get(indicator, {}) or {}
    series = values.get(country, {}) or {}
    out: dict[str, float] = {}
    for year, value in series.items():
        if value is None:
            continue
        try:
            out[str(year)] = float(value)
        except (TypeError, ValueError):
            continue
    return out


def _split_actual_forecast(series: dict[str, float], cutoff_year: int
                           ) -> tuple[list[dict], list[dict]]:
    """실측(cutoff_year 이하)과 전망(초과)으로 나눈다.

    WEO는 어느 값이 실측이고 어느 값이 전망인지 이 API로는 표시해주지
    않는다. 보수적으로 작년까지만 실측으로 본다 — 올해 값은 연중이라
    어차피 추정치이고, 그걸 실측 계열에 넣으면 리포트가 추정을 실측으로
    말하게 된다."""
    actual, forecast = [], []
    for year_str, value in sorted(series.items()):
        try:
            year = int(year_str)
        except ValueError:
            continue
        row = {"date": f"{year}-01-01", "value": value}
        (actual if year <= cutoff_year else forecast).append(row)
    return actual, forecast


def fetch_series(series_key: str, country: str = "KOR") -> DataPoint:
    """한 지표·한 국가를 가져와 실측/전망을 **분리 저장**하고, 최신 실측을 반환.

    반환 DataPoint는 언제나 **실측**이다 — 전망을 DataPoint의 value로 돌려주면
    호출부가 그걸 현재값으로 쓸 수 있다. 전망은 normalized의 별도 계열
    (`..._forecast`)로만 남긴다.
    """
    indicator, label, unit = IMF_SERIES[series_key]
    ttl = api_config()["cache_ttl_seconds"]["monthly_macro"]
    cache_key = f"imf:{indicator}:{country}"

    series = cache_mod.get(cache_key, ttl)
    if series is None:
        series = base.retry(lambda: _fetch(indicator, country),
                            label=f"imf:{series_key}:{country}", attempts=2, backoff_seconds=2.0)
        if series:
            cache_mod.set(cache_key, series)

    if not series:
        stale = cache_mod.get_stale(cache_key)
        if stale:
            series = stale
            log_event("collector.imf_served_stale", level="warning", series=series_key, country=country)
        else:
            return DataPoint(series_id=series_key, status=DataStatus.SOURCE_ERROR,
                             note=f"IMF WEO 응답 없음, 캐시도 없음 ({label}/{country})")

    cutoff = datetime.utcnow().year - 1
    actual, forecast = _split_actual_forecast(series, cutoff)

    base.write_raw("imf", f"{series_key}_{country}", series)
    prefix = f"imf_{series_key}_{country.lower()}"
    if actual:
        base.append_normalized(prefix, actual)
    if forecast:
        # 전망은 반드시 별도 계열 — 실측과 섞으면 리포트가 예측을 실측으로 말한다.
        base.append_normalized(f"{prefix}_forecast", forecast)

    if not actual:
        return DataPoint(series_id=series_key, status=DataStatus.NOT_RELEASED,
                         note=f"IMF WEO에 {country} {label} 실측 구간 없음(전망 {len(forecast)}건만 존재)")

    latest = actual[-1]
    metadata = Metadata(
        source="IMF World Economic Outlook",
        unit=unit,
        frequency=Frequency.ANNUAL,
        reliability_grade=5,
        official=True,
        reference_date=date.fromisoformat(latest["date"]),
        confidence=85.0,   # 연 2회 갱신 + 과거 값도 개정된다 — FRED 일간보다 낮게 잡는다
    )
    return DataPoint(series_id=series_key, status=DataStatus.OK,
                     value=float(latest["value"]), metadata=metadata)


def forecast_rows(series_key: str, country: str = "KOR") -> list[dict]:
    """저장된 전망 구간을 읽어온다 — 리포트가 '전망'이라고 명시해서 쓸 때만."""
    df = base.read_normalized(f"imf_{series_key}_{country.lower()}_forecast")
    if df.empty:
        return []
    return [{"date": str(r.date), "value": float(r.value)} for r in df.itertuples()]


def fetch_all(countries: list[str] | None = None) -> dict[str, DataPoint]:
    """전체 지표 × 국가. 호출 수가 지표×국가라 기본 국가군을 좁게 잡아둔다."""
    out: dict[str, DataPoint] = {}
    for country in (countries or COUNTRIES):
        for series_key in IMF_SERIES:
            out[f"{series_key}_{country}"] = fetch_series(series_key, country)
    return out
