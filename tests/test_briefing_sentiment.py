"""시장 심리 위젯 — HTML엔 그래픽, 메일 본문엔 수치만(2026-10-01)."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import publish_briefing as P  # noqa: E402
from engine.briefing import sentiment as S  # noqa: E402
from engine.briefing.render_html import render_briefing_html  # noqa: E402

DATA = {"vix": {"value": 16.39, "chg_pct": 0.31, "date": "2026-10-01", "src": "yahoo"},
        "fg": {"value": 28.0, "date": "2026-10-01", "zone": "공포", "cls": "f",
               "prev": 30.0, "w1": 36.0, "m1": 45.0, "y1": 52.0}}
MD = "---\ntitle: t\n---\n\n# 저녁 브리핑\n\n본문\n"


def test_cnn_zone_boundaries():
    assert S.zone_of(0)[0] == "극단 공포" and S.zone_of(24.9)[0] == "극단 공포"
    assert S.zone_of(25)[0] == "공포" and S.zone_of(28)[0] == "공포"
    assert S.zone_of(50)[0] == "중립" and S.zone_of(60)[0] == "탐욕"
    assert S.zone_of(75)[0] == "극단 탐욕" and S.zone_of(100)[0] == "극단 탐욕"


def test_html_file_gets_graphic_and_mail_body_gets_numbers_only():
    html = P._after_h1(render_briefing_html(MD), S.widget_html(DATA))
    assert "<svg" in html and html.index("<svg") > html.index("</h1>")
    mail = render_briefing_html(P._line_after_h1(MD, S.text_line(DATA)))
    assert "<svg" not in mail and "16.39" in mail and "28" in mail and "공포" in mail


def test_missing_data_says_cannot_judge_not_silent():
    assert S.text_line({}).count("판단 불가") == 2
    w = S.widget_html({})
    assert w.count("판단 불가") == 2 and "<svg" not in w


def test_fear_greed_is_a_collected_preset():
    import macro_data as M
    assert M.PRESETS["us_fear_greed"][0] == "cnn"
