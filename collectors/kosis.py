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

2026-09-08 좌표 확정 작업 — 6/7 확정, 1/7 미해결(각 시리즈 note 참고).
전반부(itmId=ALL 추측 기반)는 3개만 확정하고 막혔으나, 이후 KOSIS 공식
통계목록·통계표설명 API(`scripts/kosis_catalog.py`, 카테고리 드릴다운
기록은 wiki/concepts/kosis-category-catalog.md)로 넘어가면서 나머지
3개도 추측 없이 확정했다:

✅ 확정: `cpi_index`(DT_1J22003), `unemployment_rate`(DT_1DA7004S, tbl_id는
원래도 맞았고 itm_id만 틀려 있었다), `retail_sales_index`(DT_1K41002 —
단 지수가 아니라 명목 경상금액임에 주의), `industrial_production_index`·
`semiconductor_shipment_index`·`semiconductor_inventory_index`(모두
DT_1F02001 — 시도/산업별 광공업생산지수, item-meta로 산업별 분류에
C261=반도체 제조업이 있음을 찾고 verify-data로 실데이터까지 확인).

⚠️ 미해결: `k_employed_yoy`(표는 연결되지만 레벨값만 주고 YoY 계산
로직이 없어 좌표만 바꾸면 조용한 오작동이 된다 — § KOSIS_SERIES의
k_employed_yoy note 참고).

과정에서 발견한 것: 연결 자체가 하루 사이 완전히 끊겼다가(2026-09-08 새벽,
14개 후보 전부 connect timeout) 다시 살아난 사례가 있었다 — `kosis.kr`은
좌표가 맞아도 이 저장소의 실행 시점에 따라 아예 응답하지 않을 수 있다.
`scripts/kosis_lookup.py`의 `_connectivity_check()`가 이걸 8초 안에
싸게 확인한다.

⚠️ **후속 과제(2026-09-08 발견, 이번 세션 범위 밖)**: 좌표는 확정됐지만
`semiconductor_shipment_index`·`semiconductor_inventory_index`를 실제로
호출하는 수집 진입점이 코드베이스 어디에도 없다 — `fetch_series()`는
스스로를 호출해 주지 않으므로, 좌표만 고쳐서는
`engine/crisis_analysis/scoring.py::score_semiconductor_cycle()`이 읽는
`data/normalized/kosis_semiconductor_shipment_index.csv` 등이 여전히
생성되지 않고, 이 모듈은 계속 US industrial production 폴백만 쓰게 된다.
`scripts/collect_core10.py::KOSIS_KEYS`는 자기 docstring대로 Core-10
4개 지표 전용이라 여기에 그냥 얹지 않았다 — CCI 반도체 사이클 모듈을
언제·어디서 갱신할지(새 진입점? collect_core10.py 확장? 스케줄은?)는
설계 결정이 필요해 다음 세션/사용자 확인으로 넘긴다.
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
    # ✅ 2026-09-08 실측 확정 — 통계목록(statisticsList.do)·통계표설명
    # (getMeta type=ITM)으로 광업ㆍ제조업(L)→광업제조업동향조사(L_4)→
    # 생산·출하·재고(101_G131)를 드릴다운해 DT_1F02001(시도/산업별
    # 광공업생산지수)을 찾고, verify-data로 실데이터까지 확인(2026-06
    # 123.3 / 2026-07 120.4). itmId=T10(생산지수 원지수)·objL1=00(전국)·
    # objL2=0(총지수). **주의**: 이 표는 "광공업"(광업+제조업) 총지수다 —
    # 서비스업·건설업까지 포함하는 "전산업생산지수"(과거 note에 적혀
    # 있던 이름)와는 포괄범위가 다르다. 한국 언론·한은이 "산업생산"이라
    # 지칭할 때 통상 이 광공업생산지수를 가리키므로 매크로 프록시로는
    # 적절하지만, engine 쪽에서 "전산업" 스케일을 가정한 로직이 있다면
    # 재검토 필요(wiki/concepts/kosis-category-catalog.md 참고).
    "industrial_production_index": {
        "org_id": "101", "tbl_id": "DT_1F02001", "itm_id": "T10", "obj_l1": "00", "obj_l2": "0",
        "cycle": "M", "unit": "2020=100", "note": "광공업생산지수 총지수(전국) — 2026-09-08 실측 확정. 전산업(서비스업 포함)이 아니라 광업+제조업 범위임에 주의",
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
    # ✅ 2026-09-08 실측 확정 — industrial_production_index와 같은 표
    # (DT_1F02001)의 산업별(objL2) 분류에 C261=반도체 제조업이 있다는 걸
    # item-meta로 발견, verify-data로 실데이터 확인(2026-07 159.1).
    # itmId=T11(생산자제품 출하지수 원지수)·objL1=00(전국)·objL2=C261.
    "semiconductor_shipment_index": {
        "org_id": "101", "tbl_id": "DT_1F02001", "itm_id": "T11", "obj_l1": "00", "obj_l2": "C261",
        "cycle": "M", "unit": "2020=100", "note": "반도체 제조업 출하지수(전국) — CCI 모듈 I용. 2026-09-08 실측 확정",
    },
    # ✅ 2026-09-08 실측 확정 — 위와 동일한 표·산업코드, itmId만 T12(재고
    # 지수)로 교체. verify-data로 실데이터 확인(2026-06 88.7, 2026-07 106.5).
    "semiconductor_inventory_index": {
        "org_id": "101", "tbl_id": "DT_1F02001", "itm_id": "T12", "obj_l1": "00", "obj_l2": "C261",
        "cycle": "M", "unit": "2020=100", "note": "반도체 제조업 재고지수(전국) — CCI 모듈 I용. 2026-09-08 실측 확정",
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
    # obj_l2는 선택 — 분류가 2개 이상인 표(예: 시도별×산업별)에서만 필요.
    # 2026-09-08 DT_1F02001(시도/산업별 광공업생산지수) 좌표 확정 때 추가 —
    # 이 표는 objL1(시도)만으로는 어느 산업인지 특정이 안 돼 objL2(산업
    # 코드, 예: C261=반도체 제조업)까지 줘야 원하는 계열이 나온다.
    if spec.get("obj_l2"):
        params["objL2"] = spec["obj_l2"]
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
