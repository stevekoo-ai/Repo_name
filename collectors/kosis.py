"""통계청 KOSIS collector (CPI, 실업률, 산업생산, 소매판매).

Requires a free KOSIS OpenAPI key (KOSIS_API_KEY). Without one, returns
DataStatus.PENDING for every series — no guessing (7.9).

KOSIS_SERIES holds the (orgId, tblId, itmId, objL1) table coordinates for
each indicator in one place. KOSIS occasionally renumbers table IDs —
verify against the KOSIS OpenAPI '통계표 검색' console before relying on
these in production; correcting a code here doesn't require touching the
fetch logic.

2026-09-07 정정 — 이 자리에 오래 적혀 있던 진단("모든 호출이 TCP connect
timeout이므로 한국 IP 제한으로 보이고, 재시도해도 소용없다")은 **두 개의
서로 다른 문제를 하나로 뭉뚱그린 것**이었고, 그 때문에 "네트워크 문제라
손쓸 수 없다"로 결론나 통계표 좌표를 아무도 고치지 않은 채 몇 달이 갔다.

실제로는 두 가지가 따로 있다:

1. **통계표 좌표(tblId/itmId)가 틀렸다.** API 전수 프로브에서 데이터
   엔드포인트가 "해당 통계표가 존재하지 않습니다"라고 **응답했다** —
   서버에 닿았고 인증도 통과했다는 뜻이다. 아래 KOSIS_SERIES의 좌표들이
   "통계표 ID 확인 필요"라는 메모를 단 채 한 번도 검증되지 않은 게 원인.
   이건 재시도로 절대 해결되지 않는다. 좌표를 고쳐야 한다.
2. **kosis.kr 연결이 간헐적으로 불안정하다.** 같은 날 몇 분 뒤 같은
   호스트의 검색 엔드포인트가 connect timeout=20으로 죽었다. 이쪽은
   재시도가 유효하다.

즉 (2)는 맞는 관찰이었지만 (1)의 원인이 아니었다. **재시도로 해결되는
문제와 좌표를 고쳐야 하는 문제를 구분할 것.**

좌표를 다시 찾으려면: `python -m scripts.kosis_lookup --search <키워드>`
(통합검색 statisticsSearch.do — "KOSIS엔 검색 API가 없다"는 것도 틀린
전제였다). 전수 현황은 wiki/concepts/api-data-catalog.md 참고.
"""
from __future__ import annotations

from datetime import date, datetime

import requests

from core import cache as cache_mod
from core.config import api_config, get_api_key
from core.models import DataPoint, DataStatus, Frequency, Metadata
from . import base

_HISTORY_YEARS = 10

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
    "k_employed_yoy": {
        "org_id": "101", "tbl_id": "DT_1DA7001S", "itm_id": "13103005", "obj_l1": "00",
        "cycle": "M", "unit": "Persons", "note": "취업자 수(YoY 변화) — CCI 모듈 H용",
    },
    "semiconductor_shipment_index": {
        "org_id": "101", "tbl_id": "DT_1E66010", "itm_id": "T10", "obj_l1": "0000",
        "cycle": "M", "unit": "2020=100", "note": "반도체 산업생산지수(출하) — CCI 모듈 I용",
    },
    "semiconductor_inventory_index": {
        "org_id": "101", "tbl_id": "DT_1E66010", "itm_id": "T30", "obj_l1": "0000",
        "cycle": "M", "unit": "2020=100", "note": "반도체 산업생산지수(재고) — CCI 모듈 I용",
    },
}


def _fetch_table(spec: dict, api_key: str, start: str, end: str, timeout: int = 10) -> list[dict] | None:
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
    base.raise_for_status(resp)
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
        start = today.replace(year=today.year - _HISTORY_YEARS).strftime("%Y%m")
        end = today.strftime("%Y%m")
        rows = base.retry(lambda: _fetch_table(spec, api_key, start, end), label=f"kosis:{series_key}",
                           attempts=2, backoff_seconds=1.5)
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
