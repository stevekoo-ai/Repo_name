"""통계청 KOSIS collector (CPI, 실업률, 산업생산, 소매판매).

Requires a free KOSIS OpenAPI key (KOSIS_API_KEY). Without one, returns
DataStatus.PENDING for every series — no guessing (7.9).

KOSIS_SERIES holds the (orgId, tblId, itmId, objL1) table coordinates for
each indicator in one place. KOSIS occasionally renumbers table IDs —
verify against the KOSIS OpenAPI '통계표 검색' console before relying on
these in production; correcting a code here doesn't require touching the
fetch logic.
"""
from __future__ import annotations

from datetime import date, datetime

import requests

from core import cache as cache_mod
from core.config import api_config, get_api_key
from core.models import DataPoint, DataStatus, Frequency, Metadata
from . import base

KOSIS_SERIES: dict[str, dict] = {
    "cpi_index": {
        "org_id": "101", "tbl_id": "DT_1J17009", "itm_id": "T60", "obj_l1": "0000",
        "cycle": "M", "unit": "2020=100", "note": "소비자물가지수 총지수(레벨) — 통계표 ID 확인 필요",
    },
    "unemployment_rate": {
        "org_id": "101", "tbl_id": "DT_1DA7004S", "itm_id": "13103005", "obj_l1": "00",
        "cycle": "M", "unit": "%", "note": "실업률 — 통계표 ID 확인 필요",
    },
    "industrial_production_index": {
        "org_id": "101", "tbl_id": "DT_1JH20151", "itm_id": "13103141670T4", "obj_l1": "00",
        "cycle": "M", "unit": "2020=100", "note": "전산업생산지수 — 통계표 ID 확인 필요",
    },
    "retail_sales_index": {
        "org_id": "101", "tbl_id": "DT_1K31009", "itm_id": "13103159999T2A", "obj_l1": "00",
        "cycle": "M", "unit": "2020=100", "note": "소매판매액지수 — 통계표 ID 확인 필요",
    },
}


def _fetch_table(spec: dict, api_key: str, start: str, end: str, timeout: int = 20) -> list[dict] | None:
    base_url = api_config()["sources"]["kosis"]["base_url"]
    url = f"{base_url}/Param/statisticsParameterData.do"
    params = {
        "method": "getList",
        "apiKey": api_key,
        "itmId": spec["itm_id"],
        "objL1": spec["obj_l1"],
        "format": "json",
        "jsonVD": "Y",
        "prdSe": spec["cycle"],
        "startPrdDe": start,
        "endPrdDe": end,
        "orgId": spec["org_id"],
        "tblId": spec["tbl_id"],
    }
    resp = requests.get(url, params=params, timeout=timeout)
    resp.raise_for_status()
    payload = resp.json()
    if isinstance(payload, dict) and payload.get("err"):
        raise RuntimeError(payload.get("errMsg", "KOSIS error response"))
    return payload if isinstance(payload, list) else None


def fetch_series(series_key: str) -> DataPoint:
    spec = KOSIS_SERIES[series_key]
    api_key = get_api_key("kosis")
    ttl = api_config()["cache_ttl_seconds"]["monthly_macro"]

    if not api_key:
        return DataPoint(series_id=series_key, status=DataStatus.PENDING,
                          note="KOSIS_API_KEY not set — register a free key at kosis.kr/openapi")

    cached = cache_mod.get(f"kosis:{series_key}", ttl)
    rows = cached
    if rows is None:
        today = datetime.utcnow()
        start = today.replace(year=today.year - 3).strftime("%Y%m")
        end = today.strftime("%Y%m")
        rows = base.retry(lambda: _fetch_table(spec, api_key, start, end), label=f"kosis:{series_key}")
        if rows:
            cache_mod.set(f"kosis:{series_key}", rows)

    if not rows:
        stale = cache_mod.get_stale(f"kosis:{series_key}")
        if stale:
            rows = stale
        else:
            return DataPoint(series_id=series_key, status=DataStatus.SOURCE_ERROR,
                              note="KOSIS unreachable and no cache available")

    base.write_raw("kosis", series_key, rows[-24:])
    normalized = [
        {"date": _prd_to_date(r["PRD_DE"]), "value": float(r["DT"])}
        for r in rows if r.get("DT") not in (None, "", "-")
    ]
    base.append_normalized(f"kosis_{series_key}", normalized)

    if not normalized:
        return DataPoint(series_id=series_key, status=DataStatus.NOT_RELEASED, note="No numeric rows returned")

    latest = max(normalized, key=lambda r: r["date"])
    metadata = Metadata(
        source="통계청 KOSIS", unit=spec["unit"], frequency=Frequency.MONTHLY,
        reliability_grade=5, official=True,
        reference_date=date.fromisoformat(latest["date"]), confidence=90.0,
    )
    return DataPoint(series_id=series_key, status=DataStatus.OK, value=latest["value"], metadata=metadata)


def _prd_to_date(prd_de: str) -> str:
    if len(prd_de) == 6:
        return f"{prd_de[0:4]}-{prd_de[4:6]}-01"
    return f"{prd_de[0:4]}-01-01"


def fetch_all() -> dict[str, DataPoint]:
    return {key: fetch_series(key) for key in KOSIS_SERIES}
