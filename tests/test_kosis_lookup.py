"""KOSIS 후보검증 스크립트(scripts/kosis_lookup.py)의 연결 사전확인.

2026-09-08 신설. 좌표 확정 작업 중 실측 — 후보 14개(지표 7개 × 후보 2개씩)를
전부 돌렸는데 **하나도 빠짐없이 connect timeout**이었다. tblId가 뭐든 상관없이
TCP 연결 자체가 안 됐다는 뜻인데, 이걸 모른 채 순진하게 14개를 순서대로
다 돌리면 (15초 timeout × 최대 2회) × 14개 + 대기시간 ≈ 12분을 태우고서야
"전멸"을 알게 된다. `_connectivity_check()`는 본 검증에 들어가기 전 단 한 번
(8초 제한) 찔러봐서, 연결 자체가 죽어 있으면 즉시 멈추고 이유를 알린다.
"""
from __future__ import annotations

import scripts.kosis_lookup as mod


def test_connectivity_check_returns_true_on_a_normal_json_response(monkeypatch):
    """서버가 뭐라고 응답하든(성공이든 "통계표 없음" 오류든) 연결 자체가
    됐으면 True — 이 함수는 좌표가 맞는지가 아니라 연결이 되는지만 본다."""
    class _Resp:
        def raise_for_status(self): pass
        def json(self): return {"err": "030", "errMsg": "해당 통계표가 존재하지 않습니다"}

    monkeypatch.setattr(mod.requests, "get", lambda *a, **k: _Resp())
    assert mod._connectivity_check("fake-key") is True


def test_connectivity_check_returns_false_on_connect_timeout(monkeypatch):
    """2026-09-08 실측 재현 — 14개 후보가 전부 이 예외로 죽었다."""
    def _raise(*a, **k):
        raise mod.requests.exceptions.ConnectTimeout("Connection to kosis.kr timed out")

    monkeypatch.setattr(mod.requests, "get", _raise)
    assert mod._connectivity_check("fake-key") is False


def test_connectivity_check_uses_a_short_timeout_not_the_full_15s():
    """본 검증(15초)과 똑같이 길게 잡으면 사전확인의 존재 의미가 없다 —
    "빠르게 죽었는지 확인" 이 목적이므로 짧아야 한다."""
    import inspect

    src = inspect.getsource(mod._connectivity_check)
    assert "timeout=8" in src


def test_main_stops_before_the_candidate_sweep_when_connectivity_check_fails(monkeypatch, capsys):
    """연결이 죽어 있으면 CANDIDATES 순회(14개 후보, 최대 12분)를 절대
    시작하지 않아야 한다 — 이게 이 사전확인의 존재 이유다."""
    import sys

    monkeypatch.setattr(sys, "argv", ["kosis_lookup"])
    monkeypatch.setenv("KOSIS_API_KEY", "fake-key")
    monkeypatch.setattr(mod, "_connectivity_check", lambda api_key: False)

    called = []
    monkeypatch.setattr(mod, "_try_candidate", lambda *a, **k: called.append(1))

    import pytest
    with pytest.raises(SystemExit) as exc_info:
        mod.main()

    assert exc_info.value.code == 1   # 워크플로의 기존 3회 재시도가 이 실패는 잡아야 함
    assert called == []               # 후보 순회는 단 한 번도 시작 안 됨


def test_main_proceeds_to_the_candidate_sweep_when_connectivity_check_succeeds(monkeypatch):
    """반대로 연결이 살아 있으면 정상적으로 후보 순회가 시작돼야 한다 —
    사전확인이 너무 엄격해서 정상 케이스까지 막으면 안 된다."""
    import sys

    monkeypatch.setattr(sys, "argv", ["kosis_lookup", "cpi_index"])
    monkeypatch.setenv("KOSIS_API_KEY", "fake-key")
    monkeypatch.setattr(mod, "_connectivity_check", lambda api_key: True)
    monkeypatch.setattr(mod, "time", type("T", (), {"sleep": staticmethod(lambda *_: None)}))

    called = []
    monkeypatch.setattr(
        mod, "_try_candidate",
        lambda *a, **k: called.append(a) or {"ok": False, "error": "empty response"})

    mod.main()   # 정상 흐름에선 예외 없이 끝까지 실행돼야 함
    assert len(called) == len(mod.CANDIDATES["cpi_index"])


# --------------------------------------------------------------------------
# 확정 좌표 고정 (2026-09-08 GitHub Actions run 34183313334 실측)
# --------------------------------------------------------------------------
#
# KOSIS_SERIES의 값은 손으로 추측한 것과 실제 API로 검증된 것을 구분할 방법이
# 코드만 봐서는 없다 — 이번에도 "13103005" 같은 그럴듯해 보이는 코드가 사실은
# 존재하지도 않는 값이었다. 실측으로 확정한 좌표를 여기 고정해, 누군가 이
# 값을 "정리"랍시고 되돌리면 바로 여기서 걸리게 한다.

def test_confirmed_coordinates_have_not_drifted_back_to_the_old_wrong_guesses():
    """실측 확정 3개 시리즈 — 예전 오답으로 되돌아가면 이 테스트가 잡는다."""
    import collectors.kosis as kosis_mod

    cpi = kosis_mod.KOSIS_SERIES["cpi_index"]
    assert (cpi["tbl_id"], cpi["itm_id"], cpi["obj_l1"]) == ("DT_1J22003", "T", "T10")

    unemployment = kosis_mod.KOSIS_SERIES["unemployment_rate"]
    # tbl_id는 원래부터 맞았다 — itm_id("13103005", 존재하지 않는 코드)만 틀렸었다.
    assert (unemployment["tbl_id"], unemployment["itm_id"], unemployment["obj_l1"]) \
        == ("DT_1DA7004S", "T80", "00")

    retail = kosis_mod.KOSIS_SERIES["retail_sales_index"]
    assert (retail["tbl_id"], retail["itm_id"], retail["obj_l1"]) == ("DT_1K41002", "T1", "G0")
    # 지수(index)가 아니라 명목 경상금액이다 — unit 메모가 "2020=100"으로
    # 되돌아가면 안 된다(그 표는 이제 안 쓴다).
    assert "지수" not in retail["unit"] or "아님" in retail["unit"]


def test_k_employed_yoy_coordinates_were_not_swapped_for_a_level_series_without_yoy_logic():
    """표는 연결되지만 레벨값만 주는 DT_1DA7012S/DT_1DA7004S로 좌표를 바꾸면,
    score_k_sahm()의 `v < 0` 판정이 절대 참이 될 수 없는 양수 레벨값을
    "YoY"라는 이름으로 받게 돼 늘 0점을 내는 조용한 오작동이 된다 — 이게
    바로 이 저장소가 이번에 반복해서 겪은 실패 패턴(멀쩡해 보이지만 틀림)과
    같은 종류라 좌표를 일부러 그대로 뒀다. YoY 계산 로직 없이 이 값이
    바뀌면 이 테스트가 잡는다."""
    import collectors.kosis as kosis_mod

    k_emp = kosis_mod.KOSIS_SERIES["k_employed_yoy"]
    assert k_emp["tbl_id"] not in ("DT_1DA7012S", "DT_1DA7004S"), (
        "레벨 표로 좌표가 바뀌었다 — fetch_series에 YoY 계산 로직을 먼저 추가할 것"
    )
