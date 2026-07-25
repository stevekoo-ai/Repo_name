"""한국은행 ECOS collector (GDP, PPI, 경상수지, 기준금리, 환율 등).

ECOS requires a free registered API key (ECOS_API_KEY). Without one this
module returns DataStatus.PENDING for every series instead of guessing —
no network call is attempted, per 7.9/19.2.

Statistic table codes below are ECOS's well-known series for each
indicator, recorded so the mapping lives in one place and can be corrected
by editing this dict only (24.1 modularity) — verify against ECOS's
'통계표 검색' before relying on them in production, since ECOS renumbers
occasionally.
"""
from __future__ import annotations

from datetime import date, datetime

import requests

from core import cache as cache_mod
from core.config import api_config, get_api_key
from core.models import DataPoint, DataStatus, Frequency, Metadata
from . import base

ECOS_SERIES: dict[str, dict] = {
    "gdp_growth_qoq": {
        "stat_code": "902Y015", "cycle": "Q", "item_code1": "KOR",
        "unit": "%", "note": "실질 GDP 성장률(전기비, 계절조정) — 9.1.4.1 국제 주요국 경제성장률, item KOR. "
                              "scripts/ecos_lookup.py (StatisticTableList/StatisticItemList)로 2026-07-14 확인됨.",
    },
    "ppi_yoy_level": {
        "stat_code": "404Y014", "cycle": "M", "item_code1": "*AA",
        "unit": "2020=100", "note": "생산자물가지수 총지수 (레벨, YoY는 지표 계층에서 계산) — 2026-07-14 GitHub Actions 실행에서 정상 응답 확인됨",
    },
    "current_account": {
        "stat_code": "301Y013", "cycle": "M", "item_code1": "000000",
        "unit": "백만달러", "note": "경상수지 — 2026-07-14 GitHub Actions 실행에서 정상 응답 확인됨",
    },
    "base_rate": {
        "stat_code": "722Y001", "cycle": "M", "item_code1": "0101000",
        "unit": "%", "note": "한국은행 기준금리 — 2026-07-14 GitHub Actions 실행에서 정상 응답 확인됨",
    },
    "usdkrw": {
        "stat_code": "731Y001", "cycle": "D", "item_code1": "0000001",
        "unit": "KRW", "note": "원/달러 매매기준율 — 2026-07-14 GitHub Actions 실행에서 정상 응답 확인됨",
    },
    "kr_3y_yield": {
        "stat_code": "817Y002", "cycle": "D", "item_code1": "010200000",
        "unit": "%", "note": "국고채 3년물 금리 — 2026-07-14 GitHub Actions 실행에서 정상 응답 확인됨",
    },
}


def _fetch_stat(stat_code: str, cycle: str, item_code1: str, api_key: str,
                 start: str, end: str, timeout: int = 20) -> list[dict] | None:
    base_url = api_config()["sources"]["ecos"]["base_url"]
    url = f"{base_url}/StatisticSearch/{api_key}/json/kr/1/500/{stat_code}/{cycle}/{start}/{end}/{item_code1}"
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    payload = resp.json()
    if "StatisticSearch" not in payload:
        # ECOS returns {"RESULT": {"CODE": ..., "MESSAGE": ...}} on error
        raise RuntimeError(payload.get("RESULT", {}).get("MESSAGE", "ECOS error response"))
    return payload["StatisticSearch"].get("row", [])


_HISTORY_YEARS = 10


def _period_bounds(cycle: str) -> tuple[str, str]:
    today = datetime.utcnow()
    if cycle == "D":
        return (today.replace(year=today.year - _HISTORY_YEARS)).strftime("%Y%m%d"), today.strftime("%Y%m%d")
    if cycle == "M":
        return (today.replace(year=today.year - _HISTORY_YEARS)).strftime("%Y%m"), today.strftime("%Y%m")
    if cycle == "Q":
        y0 = today.year - _HISTORY_YEARS
        return f"{y0}Q1", f"{today.year}Q{((today.month - 1) // 3) + 1}"
    return (today.replace(year=today.year - _HISTORY_YEARS)).strftime("%Y"), today.strftime("%Y")


def fetch_series(series_key: str) -> DataPoint:
    spec = ECOS_SERIES[series_key]
    api_key = get_api_key("ecos")
    ttl = api_config()["cache_ttl_seconds"]["monthly_macro"]

    if not api_key:
        return DataPoint(series_id=series_key, status=DataStatus.PENDING,
                          note="ECOS_API_KEY not set — register a free key at ecos.bok.or.kr")

    cached = cache_mod.get(f"ecos:{series_key}", ttl)
    rows = cached
    if rows is None:
        start, end = _period_bounds(spec["cycle"])
        rows = base.retry(
            lambda: _fetch_stat(spec["stat_code"], spec["cycle"], spec["item_code1"], api_key, start, end),
            label=f"ecos:{series_key}",
        )
        if rows:
            cache_mod.set(f"ecos:{series_key}", rows)

    if not rows:
        stale = cache_mod.get_stale(f"ecos:{series_key}")
        if stale:
            rows = stale
        else:
            return DataPoint(series_id=series_key, status=DataStatus.SOURCE_ERROR,
                              note="ECOS unreachable and no cache available")

    base.write_raw("ecos", series_key, rows[-24:])
    normalized = [{"date": _time_to_date(r["TIME"], spec["cycle"]), "value": float(r["DATA_VALUE"])}
                  for r in rows if r.get("DATA_VALUE") not in (None, "")]
    base.append_normalized(f"ecos_{series_key}", normalized)

    if not normalized:
        return DataPoint(series_id=series_key, status=DataStatus.NOT_RELEASED, note="No numeric rows returned")

    latest = max(normalized, key=lambda r: r["date"])
    metadata = Metadata(
        source="한국은행 ECOS", unit=spec["unit"], frequency=_cycle_to_freq(spec["cycle"]),
        reliability_grade=5, official=True,
        reference_date=date.fromisoformat(latest["date"]), confidence=90.0,
    )
    return DataPoint(series_id=series_key, status=DataStatus.OK, value=latest["value"], metadata=metadata)


def _cycle_to_freq(cycle: str) -> Frequency:
    return {"D": Frequency.DAILY, "M": Frequency.MONTHLY, "Q": Frequency.QUARTERLY, "A": Frequency.ANNUAL}[cycle]


def _time_to_date(time_str: str, cycle: str) -> str:
    if cycle == "D":
        return f"{time_str[0:4]}-{time_str[4:6]}-{time_str[6:8]}"
    if cycle == "M":
        return f"{time_str[0:4]}-{time_str[4:6]}-01"
    if cycle == "Q":
        q = int(time_str[5])
        month = (q - 1) * 3 + 1
        return f"{time_str[0:4]}-{month:02d}-01"
    return f"{time_str[0:4]}-01-01"


def fetch_all() -> dict[str, DataPoint]:
    return {key: fetch_series(key) for key in ECOS_SERIES}
