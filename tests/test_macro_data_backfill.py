"""macro_data.py fetch --save — 과거 구간 백필 경로.

2026-09-09 신설. 36개월 이동평균(월봉) 분석에 2007년 이후 원/달러가 필요해지면서
드러난 구조적 공백을 고정한다: `fetch`는 출력 전용이었고 `sync`는 "기존 마지막
날짜 - 7일"부터만 증분 수집해서, **이미 있는 데이터보다 과거로 넓히는 경로가
코드 어디에도 없었다**. 워크플로에 입력만 뚫었을 때 fetch가 조용히 출력만 하고
CSV를 안 건드려 "성공했는데 데이터가 그대로"인 상태로 끝난 실제 사고가 있었다.
"""
from __future__ import annotations

import argparse
import scripts.macro_data as mod


def _args(**kw):
    base = dict(series="usd_krw_fred", start=None, end=None, raw=False, save=False)
    base.update(kw)
    return argparse.Namespace(**base)


def test_fetch_without_save_does_not_touch_csv(monkeypatch, capsys):
    """기본 동작(출력 전용)은 그대로여야 한다 — 기존 호출자를 깨지 않는다."""
    monkeypatch.setattr(mod, "_fetch_preset", lambda *a, **k: ("fred", [("2005-01-03", 1043.5)]))
    called = []
    monkeypatch.setattr(mod, "upsert_series_rows", lambda *a, **k: called.append(a))

    mod.cmd_fetch(_args())

    assert called == [], "--save 없이 CSV에 쓰면 안 된다"
    assert "2005-01-03" in capsys.readouterr().out


def test_fetch_with_save_persists_rows(monkeypatch):
    """--save는 방금 가져온 행을 그대로 upsert에 넘겨야 한다."""
    rows = [("2005-01-03", 1043.5), ("2005-01-04", 1040.2)]
    monkeypatch.setattr(mod, "_fetch_preset", lambda *a, **k: ("fred", rows))
    captured = {}

    def fake_upsert(series_name, r, provider):
        captured.update(series=series_name, rows=r, provider=provider)
        return len(r)

    monkeypatch.setattr(mod, "upsert_series_rows", fake_upsert)
    mod.cmd_fetch(_args(save=True))

    assert captured["series"] == "usd_krw_fred"
    assert captured["rows"] == rows
    assert captured["provider"] == "fred"


def test_fetch_with_save_skips_write_on_empty_response(monkeypatch):
    """응답 0건일 때 빈 걸로 덮어쓰지 않는다(R3 — 미수집은 판정이 아니다)."""
    monkeypatch.setattr(mod, "_fetch_preset", lambda *a, **k: ("fred", []))
    called = []
    monkeypatch.setattr(mod, "upsert_series_rows", lambda *a, **k: called.append(a))

    mod.cmd_fetch(_args(save=True))

    assert called == [], "0건 응답으로 CSV를 건드리면 안 된다"
