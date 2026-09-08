"""KOSIS 공식 카탈로그 도구 (scripts/kosis_catalog.py).

2026-09-08 신설. 사용자 질문 "지금 요청하는 항목이 실제 제공 가능한 게
맞아? 전체 제공 가능 리스트는 확보해서 저장했어?"로 시작 — KOSIS의 공식
통계목록(statisticsList.do)·통계표설명(getMeta type=ITM) 서비스를 처음
연결하는 모듈이라, 응답 파싱과 에러 처리가 이 테스트의 전부다. 실제
kosis.kr 왕복은 GitHub Actions에서만 가능하다(이 샌드박스는 EGRESS_BLOCKED).
"""
from __future__ import annotations

import json

import pytest

import scripts.kosis_catalog as mod


class _FakeResponse:
    def __init__(self, json_payload, ok: bool = True, content: bytes = b""):
        self._json_payload = json_payload
        self._ok = ok
        self.content = content

    def raise_for_status(self):
        pass

    def json(self):
        return self._json_payload


def test_list_category_returns_rows_on_success(monkeypatch):
    rows = [{"LIST_ID": "A", "LIST_NM": "물가"}, {"TBL_ID": "DT_1", "TBL_NM": "소비자물가지수"}]
    monkeypatch.setattr(mod.requests, "get", lambda *a, **k: _FakeResponse(rows))
    result = mod.list_category("MT_ZTITLE", "", "fake-key")
    assert result == rows


def test_list_category_returns_none_on_kosis_error_envelope(monkeypatch, capsys):
    """KOSIS는 오류를 HTTP 200 + {"err": ...} 형태로 준다 — 예외가 아니라
    dict로 온다. 이걸 리스트로 착각하면 안 된다."""
    monkeypatch.setattr(mod.requests, "get",
                        lambda *a, **k: _FakeResponse({"err": "10", "errMsg": "필수 값 누락"}))
    result = mod.list_category("MT_ZTITLE", "bad-id", "fake-key")
    assert result is None
    assert "필수 값 누락" in capsys.readouterr().out


def test_table_item_metadata_returns_rows_on_success(monkeypatch):
    rows = [{"OBJ_ID": "T", "OBJ_NM": "항목", "OBJ_VAL_ID": "T10", "OBJ_VAL_NM": "전국"}]
    monkeypatch.setattr(mod.requests, "get", lambda *a, **k: _FakeResponse(rows))
    result = mod.table_item_metadata("101", "DT_1J22003", "fake-key")
    assert result == rows


def test_table_item_metadata_returns_none_on_unexpected_shape(monkeypatch, capsys):
    """리스트도 아니고 err도 없는 응답 — 형식이 바뀐 경우. 조용히 빈 걸로
    처리하지 않고 알린다(R3 — 미수집은 판정이 아니다)."""
    monkeypatch.setattr(mod.requests, "get", lambda *a, **k: _FakeResponse({"unexpected": True}))
    result = mod.table_item_metadata("101", "DT_1JH20151", "fake-key")
    assert result is None
    assert "예상과 다른 응답 형식" in capsys.readouterr().out


def test_download_manual_rejects_non_pdf_response(monkeypatch, capsys):
    """URL이 바뀌거나 게이트웨이 오류 페이지가 오면 %PDF 매직바이트로 걸러야
    한다 — 안 그러면 HTML 오류 페이지를 'PDF'라고 커밋하게 된다."""
    monkeypatch.setattr(mod.requests, "get",
                        lambda *a, **k: _FakeResponse(None, content=b"<html>404</html>"))
    assert mod.download_manual() is False
    assert "PDF가 아닌 응답" in capsys.readouterr().out


def test_download_manual_accepts_real_pdf_magic_bytes(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "MANUAL_PATH", tmp_path / "docs" / "kosis" / "manual.pdf")
    monkeypatch.setattr(mod.requests, "get",
                        lambda *a, **k: _FakeResponse(None, content=b"%PDF-1.4 fake content"))
    assert mod.download_manual() is True
    assert mod.MANUAL_PATH.exists()
    assert mod.MANUAL_PATH.read_bytes().startswith(b"%PDF")


def test_raw_responses_are_saved_with_a_timestamped_filename_not_overwritten(monkeypatch, tmp_path):
    """이 저장소의 raw-tier 관례(collectors/base.write_raw)와 동일하게,
    같은 조회를 다시 해도 이전 응답을 덮어쓰지 않아야 한다 — 감사 추적."""
    monkeypatch.setattr(mod, "RAW_DIR", tmp_path / "kosis")
    p1 = mod._save_raw("category_MT_ZTITLE_root", [{"a": 1}])
    p2 = mod._save_raw("category_MT_ZTITLE_root", [{"a": 2}])
    assert p1 != p2
    assert json.loads(p1.read_text())[0]["a"] == 1
    assert json.loads(p2.read_text())[0]["a"] == 2


def test_error_messages_are_redacted_before_truncation():
    """2026-09-07 KOSIS 키 유출 사고와 같은 클래스의 실수를 반복하지 않기
    위한 소스 코드 수준 고정 — 마스킹 없이 자르는 패턴이 있으면 안 된다."""
    from pathlib import Path

    text = Path(mod.__file__).read_text(encoding="utf-8")
    assert "str(exc)[:" not in text, "마스킹 없이 예외를 자르고 있다"
    assert "str(last_error)[:" not in text, "마스킹 없이 예외를 자르고 있다"
