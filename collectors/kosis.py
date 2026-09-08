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

2026-09-08 좌표 확정 작업 — 3/7 확정, 4/7 미해결(각 시리즈 note 참고):

✅ 확정: `cpi_index`(DT_1J22003), `unemployment_rate`(DT_1DA7004S, tbl_id는
원래도 맞았고 itm_id만 틀려 있었다), `retail_sales_index`(DT_1K41002 —
단 지수가 아니라 명목 경상금액임에 주의).

⚠️ 미해결: `industrial_production_index`·`semiconductor_shipment_index`·
`semiconductor_inventory_index`(후보 전부 "표 없음" 또는 "표는 있으나 이
파라미터 조합엔 데이터 없음"), `k_employed_yoy`(표는 연결되지만 레벨값만
주고 YoY 계산 로직이 없어 좌표만 바꾸면 조용한 오작동이 된다 — §
KOSIS_SERIES의 k_employed_yoy note 참고).

과정에서 발견한 것: 연결 자체가 하루 사이 완전히 끊겼다가(2026-09-08 새벽,
14개 후보 전부 connect timeout) 다시 살아난 사례가 있었다 — `kosis.kr`은
좌표가 맞아도 이 저장소의 실행 시점에 따라 아예 응답하지 않을 수 있다.
`scripts/kosis_lookup.py`의 `_connectivity_check()`가 이걸 8초 안에
싸게 확인한다.
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
    # ✅ 2026-09-08 실측 확정(scripts/kosis_lookup.py 후보검증, GitHub Actions
    # run 34183313334) — itmId=ALL/objL1=ALL(objL2 없이)로 228행 정상 수신,
    # ITM_NM="소비자물가지수(총지수)" C1_NM="전국"(2025-09 117.06) 확인.
    "cpi_index": {
        "org_id": "101", "tbl_id": "DT_1J22003", "itm_id": "T", "obj_l1": "T10",
        "cycle": "M", "unit": "2020=100", "note": "소비자물가지수 총지수(전국) — 2026-09-08 실측 확정",
    },
    # ✅ 2026-09-08 실측 확정 — tbl_id는 원래도 맞았다(itm_id만 틀렸었다:
    # "13103005"는 존재하지 않는 코드). itmId=ALL/objL1=ALL로 1881행 수신,
    # ITM_NM="실업률" C1_NM="계"(전국, 2025-09 2.1%) 확인.
    "unemployment_rate": {
        "org_id": "101", "tbl_id": "DT_1DA7004S", "itm_id": "T80", "obj_l1": "00",
        "cycle": "M", "unit": "%", "note": "실업률(전국) — 2026-09-08 실측 확정",
    },
    # ⚠️ 2026-09-08 후보 2개 전부 실패 — 아직 미해결.
    # DT_1JH20151: "해당 통계표가 존재하지 않습니다"(표 자체가 없음).
    # DT_1F01012: "데이터가 존재하지 않습니다"(표는 실재하나 이 파라미터
    # 조합엔 데이터 없음 — itmId/objL1을 "ALL" 대신 구체적 코드로 지정해야
    # 할 가능성. WebSearch로는 이 표가 "광공업생산지수"(2015=100, 산업별)로
    # 확인됨 — "전산업생산지수"와는 포괄범위가 다를 수 있어 재검토 필요).
    "industrial_production_index": {
        "org_id": "101", "tbl_id": "DT_1JH20151", "itm_id": "13103141670T4", "obj_l1": "00",
        "cycle": "M", "unit": "2020=100", "note": "전산업생산지수 — 통계표 ID 미확정(2026-09-08 재검증 필요, kosis_lookup.py CANDIDATES 참고)",
    },
    # ✅ 2026-09-08 실측 확정 — 단, **지수(index)가 아니라 경상금액(억원)이다.**
    # itmId=ALL/objL1=ALL로 220행 수신, ITM_NM="경상금액" C1_NM="합계"
    # (2025-09 56,873,548백만원). 원래 unit 메모("2020=100" 지수)는 틀렸다 —
    # 이 표는 명목 판매액이지 물가효과를 제거한 지수가 아니다. 진짜
    # "소매판매액지수"(2020=100) 표가 따로 있을 수 있으나 이번 검증에선
    # 못 찾았다. 지수가 필요하면 FRED OECD 미러(kr_retail_sales_mom_oecd)를
    # 계속 쓰고, 이건 명목 판매액 실측 보조지표로만 쓸 것.
    "retail_sales_index": {
        "org_id": "101", "tbl_id": "DT_1K41002", "itm_id": "T1", "obj_l1": "G0",
        "cycle": "M", "unit": "억원(경상금액, 지수 아님)", "note": "소매판매액(명목, 합계) — 2026-09-08 실측 확정, 지수 아닌 금액임에 주의",
    },
    # ⚠️ 2026-09-08 실측 — 표 자체는 살아있다(DT_1DA7012S/DT_1DA7004S 둘 다
    # 연결되고 취업자 수 "레벨"을 정상 수신, 2025-09 전국 29,153.5천명).
    # 하지만 **이 값은 레벨이지 전년동월비(YoY)가 아니다** — KOSIS가 YoY를
    # 미리 계산해서 주는 별도 항목을 이 두 표에서 찾지 못했다. 좌표만
    # 바꿔서 이 레벨값을 그대로 흘려보내면 engine/crisis_analysis/scoring.py
    # score_k_sahm()의 `weak_months = v < 0` 판정이 절대 참이 될 수 없는
    # 값(2,900만 명대 양수)을 "YoY"라는 이름으로 받게 돼 겉보기엔 정상
    # 작동하는 것처럼 보이면서 실제로는 항상 0점을 내는, 이전보다 더
    # 발견하기 어려운 조용한 실패가 된다 — 그래서 **좌표를 아직 바꾸지
    # 않았다.** 고치려면 fetch_series에 전년동월 대비 증감률 계산을
    # 추가하거나(레벨 시계열에서 자체 계산), 이 값 자체를 이미 YoY로 주는
    # 다른 표를 찾아야 한다(둘 다 이번 세션 범위 밖).
    "k_employed_yoy": {
        "org_id": "101", "tbl_id": "DT_1DA7001S", "itm_id": "13103005", "obj_l1": "00",
        "cycle": "M", "unit": "Persons", "note": "취업자 수(YoY 변화) — CCI 모듈 H용. 2026-09-08: 좌표 후보(DT_1DA7012S/DT_1DA7004S)는 연결되지만 레벨값만 준다 — YoY 계산 로직 추가 전까지 좌표 교체 보류",
    },
    # ⚠️ 2026-09-08 후보 2개 전부 실패 — DT_1F01012 "데이터가 존재하지
    # 않습니다"(표는 실재), DT_1E66010 "해당 통계표가 존재하지 않습니다"
    # (표 자체가 없음). 미해결 — 아래 semiconductor_inventory_index와 동일.
    "semiconductor_shipment_index": {
        "org_id": "101", "tbl_id": "DT_1E66010", "itm_id": "T10", "obj_l1": "0000",
        "cycle": "M", "unit": "2020=100", "note": "반도체 산업생산지수(출하) — CCI 모듈 I용. 통계표 ID 미확정(2026-09-08 재검증 필요)",
    },
    "semiconductor_inventory_index": {
        "org_id": "101", "tbl_id": "DT_1E66010", "itm_id": "T30", "obj_l1": "0000",
        "cycle": "M", "unit": "2020=100", "note": "반도체 산업생산지수(재고) — CCI 모듈 I용. 통계표 ID 미확정(2026-09-08 재검증 필요, kosis_lookup.py CANDIDATES 참고)",
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
