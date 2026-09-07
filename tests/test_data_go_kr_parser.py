"""data.go.kr 응답 파서 (collectors/base.parse_data_go_kr_items).

2026-09-07 장애 회귀 테스트. MOLIT 4종이 한 달간(2026-08-11~09-07) 조용히
수집을 멈췄던 원인 — `type=json`을 요청했는데 서버가 XML을 돌려주자
resp.json()이 ValueError를 냈고, 그게 "likely a service/auth error"라는
엉뚱한 진단으로 둔갑한 뒤 서킷브레이커에 먹혀 워크플로는 234회 연속
"success"를 찍었다 — 을 두 번 다시 겪지 않기 위한 테스트.

핵심 계약: **형식이 아니라 resultCode로 성공/실패를 판정한다.**
"""
from __future__ import annotations

import pytest

from collectors import base


class _FakeResponse:
    """requests.Response 중 파서가 쓰는 부분(.text, .json())만 흉내낸다."""

    def __init__(self, text: str, json_payload=None, json_raises: bool = True):
        self.text = text
        self._json_payload = json_payload
        self._json_raises = json_raises

    def json(self):
        if self._json_raises:
            raise ValueError("not json")
        return self._json_payload


# 실제 장애 때 서버가 돌려주던 응답 형태 그대로(강남구 아파트매매, 필드 축약).
_REAL_XML = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<response><header><resultCode>000</resultCode><resultMsg>OK</resultMsg></header>
<body><items>
<item><aptDong> </aptDong><aptNm>우성사원5</aptNm><dealAmount>  95,000</dealAmount><excluUseAr>84.99</excluUseAr></item>
<item><aptDong>101</aptDong><aptNm>상록수</aptNm><dealAmount>120,500</dealAmount><excluUseAr>59.94</excluUseAr></item>
</items></body></response>"""


def test_xml_success_response_is_parsed_not_mistaken_for_an_auth_error():
    """이게 이 파일의 존재 이유 — 이 응답이 예외를 던지면 부동산 수집이 또 멈춘다."""
    rows = base.parse_data_go_kr_items(_FakeResponse(_REAL_XML), "MOLIT 아파트매매")
    assert len(rows) == 2
    assert rows[0]["aptNm"] == "우성사원5"
    assert rows[1]["dealAmount"] == "120,500"


def test_xml_values_survive_the_downstream_float_parsing():
    """XML은 모든 값이 문자열이다. 호출부(_price_per_pyeong)가 쓰는
    float(str(v).replace(",","")) 패턴이 그대로 통해야 JSON 경로와 동작이 같다."""
    from collectors.molit import _price_per_pyeong

    rows = base.parse_data_go_kr_items(_FakeResponse(_REAL_XML), "MOLIT 아파트매매")
    prices = [_price_per_pyeong(r) for r in rows]
    assert all(p is not None and p > 0 for p in prices)


def test_empty_element_becomes_empty_string_not_none():
    """<aptDong> </aptDong> 같은 빈 엘리먼트가 None이면 하위 코드가 TypeError를 낸다."""
    rows = base.parse_data_go_kr_items(_FakeResponse(_REAL_XML), "MOLIT 아파트매매")
    assert rows[0]["aptDong"] == ""


def test_json_flat_envelope_still_works():
    """기존 JSON 경로가 깨지지 않았는지 — 이 API군의 JSON은 평면 구조다."""
    payload = {"header": {"resultCode": "000", "resultMsg": "OK"},
               "body": {"items": {"item": [{"aptNm": "가"}, {"aptNm": "나"}]}}}
    rows = base.parse_data_go_kr_items(
        _FakeResponse("{}", payload, json_raises=False), "MOLIT 아파트매매")
    assert [r["aptNm"] for r in rows] == ["가", "나"]


def test_json_wrapped_envelope_still_works():
    """일부 상품은 "response"로 한 겹 감싼다 — 둘 다 지원해야 한다."""
    payload = {"response": {"header": {"resultCode": "00"},
                            "body": {"items": {"item": {"aptNm": "단건"}}}}}
    rows = base.parse_data_go_kr_items(
        _FakeResponse("{}", payload, json_raises=False), "MOLIT 아파트매매")
    assert rows == [{"aptNm": "단건"}]


def test_zero_transactions_is_empty_list_not_an_error():
    """거래 0건은 정상이다 — 오류로 올리면 서킷브레이커가 헛돈다."""
    xml = ("<response><header><resultCode>000</resultCode><resultMsg>OK</resultMsg>"
           "</header><body><items></items></body></response>")
    assert base.parse_data_go_kr_items(_FakeResponse(xml), "MOLIT 아파트매매") == []


def test_real_error_code_still_raises():
    """진짜 오류(승인 안 된 키 등)는 여전히 예외여야 한다 — 형식 문제와 구분되는
    지점. 이걸 조용히 삼키면 반대 방향의 조용한 실패가 된다."""
    xml = ("<response><header><resultCode>30</resultCode>"
           "<resultMsg>SERVICE_ACCESS_DENIED_ERROR</resultMsg></header></response>")
    with pytest.raises(RuntimeError, match="SERVICE_ACCESS_DENIED_ERROR"):
        base.parse_data_go_kr_items(_FakeResponse(xml), "MOLIT 아파트매매")


def test_json_error_code_still_raises():
    payload = {"header": {"resultCode": "99", "resultMsg": "조회기간은 1년이내만 가능"}}
    with pytest.raises(RuntimeError, match="1년이내"):
        base.parse_data_go_kr_items(
            _FakeResponse("{}", payload, json_raises=False), "관세청")


def test_garbage_response_names_the_body_and_does_not_pretend_to_know_why():
    """JSON도 XML도 아니면 그때는 진짜로 알 수 없는 응답 — 원문을 보여준다."""
    with pytest.raises(RuntimeError, match="JSON도 XML도 아닌"):
        base.parse_data_go_kr_items(_FakeResponse("this is not markup at all {["), "MOLIT")


def test_html_error_page_is_not_silently_read_as_zero_transactions():
    """게이트웨이 HTML 오류 페이지는 ElementTree 기준으론 '멀쩡한 XML'이라,
    형식만 보고 넘어가면 resultCode도 items도 없는 채 빈 리스트가 나가서
    '거래 0건'으로 오독된다 — 이게 정확히 이번에 고친 조용한 실패의 형태다."""
    with pytest.raises(RuntimeError, match="응답 형식이 아님"):
        base.parse_data_go_kr_items(_FakeResponse("<html>502 Bad Gateway</html>"), "MOLIT")


def test_json_that_is_not_this_api_envelope_raises():
    """JSON 경로에도 같은 함정이 있다 — 봉투가 아니면 []가 아니라 예외."""
    with pytest.raises(RuntimeError, match="응답 형식이 아님"):
        base.parse_data_go_kr_items(
            _FakeResponse('{"error":"quota exceeded"}', {"error": "quota exceeded"},
                          json_raises=False), "MOLIT")


def test_api_key_is_redacted_from_unknown_response_bodies():
    """data.go.kr 오류 본문이 요청 파라미터를 echo하는 경우가 있어 방어적으로 마스킹."""
    body = "error at ?serviceKey=SUPERSECRETKEY123&LAWD_CD=11680 :: unparseable"
    with pytest.raises(RuntimeError) as exc:
        base.parse_data_go_kr_items(_FakeResponse(body), "MOLIT")
    assert "SUPERSECRETKEY123" not in str(exc.value)
