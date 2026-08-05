"""법정동코드(5자리 시군구 코드, 행정표준코드관리시스템 code.go.kr 기준) 지역군 정의.

국토교통부 실거래가 공개시스템 API들(아파트 매매/전월세, 연립다세대 매매, 오피스텔 매매 —
collectors/molit*.py)이 모두 동일한 지역코드 체계를 쓰기 때문에 여기 한 곳에서만 관리한다.
특정 지역이 계속 빈 배열만 돌려준다면 구·시 통합/신설로 코드가 바뀌었을 가능성이 있으니
그 지역만 code.go.kr에서 재확인하면 된다 — 나머지 지역 집계에는 영향 없음.
"""
from __future__ import annotations

SEOUL_DISTRICTS: list[dict[str, str]] = [
    {"name": "종로구", "code": "11110"}, {"name": "중구", "code": "11140"},
    {"name": "용산구", "code": "11170"}, {"name": "성동구", "code": "11200"},
    {"name": "광진구", "code": "11215"}, {"name": "동대문구", "code": "11230"},
    {"name": "중랑구", "code": "11260"}, {"name": "성북구", "code": "11290"},
    {"name": "강북구", "code": "11305"}, {"name": "도봉구", "code": "11320"},
    {"name": "노원구", "code": "11350"}, {"name": "은평구", "code": "11380"},
    {"name": "서대문구", "code": "11410"}, {"name": "마포구", "code": "11440"},
    {"name": "양천구", "code": "11470"}, {"name": "강서구", "code": "11500"},
    {"name": "구로구", "code": "11530"}, {"name": "금천구", "code": "11545"},
    {"name": "영등포구", "code": "11560"}, {"name": "동작구", "code": "11590"},
    {"name": "관악구", "code": "11620"}, {"name": "서초구", "code": "11650"},
    {"name": "강남구", "code": "11680"}, {"name": "송파구", "code": "11710"},
    {"name": "강동구", "code": "11740"},
]

# 서울 제외, 수도권(경기·인천) 주요 대도시 — 33개 경기 시군 전체 대신 인구 상위권 위주로
# 추려 호출 수를 관리한다. 용인 기흥구는 사용자 청약 타겟(플랫폼시티) 인근이라 하이라이트.
CAPITAL_AREA_EXTRA: list[dict[str, str]] = [
    {"name": "인천 미추홀구", "code": "28177"}, {"name": "인천 연수구", "code": "28185"},
    {"name": "인천 남동구", "code": "28200"}, {"name": "인천 부평구", "code": "28237"},
    {"name": "인천 계양구", "code": "28245"}, {"name": "인천 서구", "code": "28260"},
    {"name": "수원 영통구", "code": "41117"}, {"name": "성남 분당구", "code": "41135"},
    {"name": "안양 동안구", "code": "41173"}, {"name": "부천시", "code": "41190"},
    {"name": "안산 단원구", "code": "41273"}, {"name": "고양 일산동구", "code": "41285"},
    {"name": "남양주시", "code": "41360"}, {"name": "시흥시", "code": "41390"},
    {"name": "하남시", "code": "41450"},
    {"name": "용인 기흥구", "code": "41463", "highlight": "용인 플랫폼시티 인근 — 청약 타겟 지역"},
    {"name": "화성시", "code": "41590"}, {"name": "김포시", "code": "41570"},
]

# 수도권 제외, 8개 특·광역시 + 주요 도청소재지 대표 도시 1곳씩 — 전국 250여개 시군구
# 전량 조회는 호출량이 과도해 대표 표본으로 대체한 것. "전국" 수치는 전수조사가 아닌
# 대표 도시 표본 기준 추정치임을 리포트에도 명시한다.
NATIONWIDE_EXTRA: list[dict[str, str]] = [
    {"name": "부산 해운대구", "code": "26350"}, {"name": "대구 수성구", "code": "27260"},
    {"name": "광주 서구", "code": "29140"}, {"name": "대전 서구", "code": "30170"},
    {"name": "울산 남구", "code": "31140"}, {"name": "세종시", "code": "36110"},
    {"name": "청주 흥덕구", "code": "43113"}, {"name": "천안 서북구", "code": "44133"},
    {"name": "전주 완산구", "code": "45111"}, {"name": "포항 남구", "code": "47111"},
    {"name": "창원 성산구", "code": "48123"}, {"name": "제주시", "code": "50110"},
]

REGION_TIERS: dict[str, list[dict[str, str]]] = {
    "seoul": SEOUL_DISTRICTS,
    "capital_area": SEOUL_DISTRICTS + CAPITAL_AREA_EXTRA,
    "nationwide": SEOUL_DISTRICTS + CAPITAL_AREA_EXTRA + NATIONWIDE_EXTRA,
}

TIER_LABELS = {"seoul": "서울", "capital_area": "수도권", "nationwide": "전국(대표표본)"}

HIGHLIGHT_REGION = next(r for r in CAPITAL_AREA_EXTRA if r.get("highlight"))


def all_regions() -> list[dict[str, str]]:
    """Every configured region, deduplicated by code (capital_area/nationwide reuse seoul)."""
    seen: dict[str, dict[str, str]] = {}
    for region in REGION_TIERS["nationwide"]:
        seen.setdefault(region["code"], region)
    return list(seen.values())
