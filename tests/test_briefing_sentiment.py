"""시장 심리 위젯 — HTML엔 그래픽, 메일 본문엔 수치만(2026-10-01)."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import publish_briefing as P  # noqa: E402
from engine.briefing import sentiment as S  # noqa: E402
from engine.briefing.render_html import render_briefing_html  # noqa: E402

SPARK = [("2026-07-01", 15.0), ("2026-08-01", 18.0), ("2026-09-01", 21.0), ("2026-10-01", 16.39)]
_BASE = {"prev": 16.34, "chg_pct": 0.31, "w1": 15.67, "m1": 16.34, "m3": 16.15,
         "pctile_1y": 35.0, "spark": SPARK, "date": "2026-10-01"}
DATA = {"vix": {**_BASE, "value": 16.39, "src": "yahoo"},
        "fg": {**_BASE, "value": 28.0, "prev": 30.0, "zone": "공포", "cls": "f"}}
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
    assert S.text_line({}).count("판단 불가") == 3
    w = S.widget_html({})
    assert w.count("판단 불가") == 3 and "<svg" not in w


def test_fear_greed_is_a_collected_preset():
    import macro_data as M
    assert M.PRESETS["us_fear_greed"][0] == "cnn"


def test_cards_name_their_market_and_show_history():
    w = S.widget_html(DATA)
    assert "(미국 S&P500)" in w and "(한국 코스피200)" in w and "(미국 주식시장)" in w
    assert w.count('class="spark"') == 2          # VIX·공포탐욕 추이선
    assert "1년 백분위" in w and "3달 전" in w
    assert "VKOSPI" in w and "수집 실패 — 판단 불가" in w   # VKOSPI 미수집은 숨기지 않는다


def test_summarize_reads_history_correctly():
    rows = [(f"2026-0{m}-01", float(m)) for m in range(1, 10)] + [("2026-10-01", 5.0)]
    s = S._summarize(rows, __import__("datetime").date(2026, 10, 2))
    assert s["value"] == 5.0 and s["prev"] == 9.0 and s["m1"] == 9.0
    assert s["pctile_1y"] == 60.0                  # 10개(1~9, 5) 중 5 이하가 6개(1,2,3,4,5,5)
    assert s["spark"][0][0] >= "2026-07-02"        # 최근 약 3개월만
