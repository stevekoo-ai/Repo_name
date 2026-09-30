"""팩 ① 신선도 — 쌍둥이 계열 선택과 참고 줄(2026-09-30)."""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import macro_data as M  # noqa: E402
from engine.briefing import context as C  # noqa: E402


def test_twin_used_only_when_fresher_and_never_mixed_within_a_row():
    m = {"us_sp500": [("2026-09-25", 1.0), ("2026-09-28", 2.0)],
         "us_sp500_yf": [("2026-09-25", 1.0), ("2026-09-28", 2.0), ("2026-09-29", 3.0)]}
    rows, src = C._freshest(m, "us_sp500", date(2026, 9, 30))
    assert src == "yahoo" and rows == m["us_sp500_yf"]          # 쌍둥이 계열 통째로
    m["us_sp500"].append(("2026-09-29", 3.0))
    rows, src = C._freshest(m, "us_sp500", date(2026, 9, 30))
    assert src == "" and rows == m["us_sp500"]                  # 같으면 원래 원천 유지


def test_twins_and_references_are_registered_presets():
    fact_keys = {k for k, *_ in C.FACT_SERIES}
    for key, (twin, _) in C.FRESH_TWINS.items():
        assert key in fact_keys and twin in M.PRESETS
    for key, (ref, _) in C.REF_COMPANIONS.items():
        assert key in fact_keys and ref in fact_keys and ref in M.PRESETS


def test_brent_spot_and_futures_are_not_twins():
    # 현물↔선물은 정의가 달라(최근 250일 최대 $28.9 차) 값을 바꿔 쓰면 안 된다
    assert "us_brent" not in C.FRESH_TWINS
    assert C.REF_COMPANIONS["us_brent"][0] == "us_brent_futures"


def test_india_series_for_compass_t7_are_collected_and_shown():
    fact_keys = {k for k, *_ in C.FACT_SERIES}
    for k in ("in_nifty50", "in_usdinr"):
        assert k in M.PRESETS and k in fact_keys
