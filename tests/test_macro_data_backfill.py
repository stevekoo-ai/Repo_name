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


# 2026-09-10 추가 — `fetch --start 2005-01-01`이 ECOS 프리셋에서 조용히
# 실패했다. cmd_fetch가 --start를 그대로 ECOS URL에 넣는데 ECOS는 ISO
# 형식을 안 받는다. FRED는 ISO를 받으므로 같은 명령이 FRED 계열에선
# 성공하고 ECOS 계열에서만 실패해, 워크플로 결과가 "성공했는데 한국
# 계열만 안 늘어남"으로 나타나 원인 파악이 늦어졌다.

def _macro_data_module():
    import importlib.util
    from pathlib import Path

    path = Path(__file__).resolve().parent.parent / "scripts" / "macro_data.py"
    spec = importlib.util.spec_from_file_location("macro_data_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_iso_start_is_converted_to_the_ecos_cycle_format():
    md = _macro_data_module()
    assert md._coerce_ecos_date("2005-01-01", "D") == "20050101"
    assert md._coerce_ecos_date("2005-01-01", "M") == "200501"
    assert md._coerce_ecos_date("2005-08-15", "Q") == "2005Q3"
    assert md._coerce_ecos_date("2005-01-01", "Y") == "2005"


def test_values_already_in_ecos_format_pass_through_untouched():
    md = _macro_data_module()
    assert md._coerce_ecos_date("20050101", "D") == "20050101"
    assert md._coerce_ecos_date("200501", "M") == "200501"


def test_none_stays_none_so_the_caller_can_apply_its_default():
    md = _macro_data_module()
    assert md._coerce_ecos_date(None, "D") is None


def test_unparseable_input_is_left_alone_rather_than_guessed():
    """해석 못 하는 값을 임의로 고치면 틀린 구간을 조용히 받아온다 —
    그대로 넘겨 ECOS가 거부하게 두는 편이 안전하다."""
    md = _macro_data_module()
    assert md._coerce_ecos_date("2005-13-99", "D") == "2005-13-99"
