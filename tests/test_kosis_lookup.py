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
