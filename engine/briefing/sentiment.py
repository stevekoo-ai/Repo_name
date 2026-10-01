"""시장 심리 위젯 — VIX 카드 + CNN 공포·탐욕 게이지 (2026-10-01).

사용자 요청: 방송 화면의 "VIX 16.39 ▲0.31% | CNN 공포탐욕 28" 같은 패널을
HTML 보고서에 넣고, 메일 본문에는 수치만 한 줄로 언급한다.

- HTML 보고서(첨부 .html)  → `widget_html()` : 인라인 SVG·CSS(스크립트 없음)
- 메일 본문                 → `text_line()`   : 수치 한 줄(Gmail은 SVG를 못 그린다)

데이터는 sources/macro-series.csv만 쓴다(us_vix/us_vix_yf 신선도 쌍둥이,
us_fear_greed). 없으면 R3대로 "수집 실패 — 판단 불가"로 표시하고 지어내지 않는다.

색: 공포↔탐욕은 양극(diverging) — 빨강↔파랑, 중립은 회색. 단계 색은
dataviz 검증기로 밝은(#fcfcfb)·어두운(#1c1f26) 표면에서 CVD·정상시각 분리를
통과시켰다. 대비 3:1 미만 칸이 있어 구간 이름을 글자로 직접 달고 표를 함께
둔다(색만으로 구분하지 않음).
"""
from __future__ import annotations

import html as _html
import math
from datetime import date, timedelta

from engine.briefing import context as C

# CNN 공식 구간 경계
ZONES = [
    (0, 25, "극단 공포", "xf"),
    (25, 45, "공포", "f"),
    (45, 55, "중립", "n"),
    (55, 75, "탐욕", "g"),
    (75, 100, "극단 탐욕", "xg"),
]


def zone_of(score: float) -> tuple[str, str]:
    for lo, hi, name, cls in ZONES:
        if score < hi or hi == 100:
            if score >= lo:
                return name, cls
    return "중립", "n"


def _value_on_or_before(rows: list[tuple[str, float]], d: date) -> float | None:
    vals = [v for k, v in rows if k <= d.isoformat()]
    return vals[-1] if vals else None


def collect(as_of: date) -> dict:
    m = C._series_map()
    out: dict = {"as_of": as_of.isoformat()}

    vix, src = C._freshest(m, "us_vix", as_of)
    if len(vix) >= 2:
        (d0, v0), (_, v1) = vix[-1], vix[-2]
        out["vix"] = {"value": v0, "chg_pct": (v0 / v1 - 1) * 100 if v1 else None,
                      "date": d0, "src": src or "fred"}

    fg = [(d, v) for d, v in m.get("us_fear_greed", []) if d <= as_of.isoformat()]
    if fg:
        d0, v0 = fg[-1]
        last = date.fromisoformat(d0)
        out["fg"] = {
            "value": v0, "date": d0, "zone": zone_of(v0)[0], "cls": zone_of(v0)[1],
            "prev": fg[-2][1] if len(fg) >= 2 else None,
            "w1": _value_on_or_before(fg, last - timedelta(days=7)),
            "m1": _value_on_or_before(fg, last - timedelta(days=30)),
            "y1": _value_on_or_before(fg, last - timedelta(days=365)),
        }
    return out


def text_line(data: dict) -> str:
    """메일 본문용 한 줄(마크다운 인용)."""
    parts = []
    v = data.get("vix")
    if v:
        arrow = "▲" if (v["chg_pct"] or 0) >= 0 else "▼"
        chg = f" {arrow}{abs(v['chg_pct']):.2f}%" if v["chg_pct"] is not None else ""
        parts.append(f"VIX **{v['value']:.2f}**{chg} ({v['date']})")
    else:
        parts.append("VIX 수집 실패 — 판단 불가")
    f = data.get("fg")
    if f:
        prev = f", 전일 {f['prev']:.0f}" if f.get("prev") is not None else ""
        parts.append(f"CNN 공포·탐욕 **{f['value']:.0f}** ({f['zone']}{prev}, {f['date']})")
    else:
        parts.append("CNN 공포·탐욕 수집 실패 — 판단 불가")
    return "> 📊 시장 심리: " + " · ".join(parts) + " — 그래픽은 첨부 HTML 보고서"


# ── HTML 위젯 ────────────────────────────────────────────────────────────

_CSS = """
.senti { --xf:#b8312f; --f:#ec8682; --n:#f0efec; --g:#6fa6ea; --xg:#1f5fae;
  display:flex; flex-wrap:wrap; gap:12px; margin:16px 0 20px; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) .senti { --xf:#e65f5a; --f:#a2342f; --n:#383835; --g:#2e5fa8; --xg:#4e91e4; } }
:root[data-theme="dark"] .senti { --xf:#e65f5a; --f:#a2342f; --n:#383835; --g:#2e5fa8; --xg:#4e91e4; }
.senti .card { flex:1 1 240px; background:var(--surface); border:1px solid var(--border);
  border-radius:10px; padding:12px 14px; }
.senti .card h4 { margin:0 0 6px; font-size:.95rem; color:var(--text); }
.senti .vix { flex:0 1 220px; }
.senti .hero { font-size:2.6rem; font-weight:700; line-height:1.1; color:var(--text);
  font-variant-numeric: tabular-nums; }
.senti .chg { font-size:1rem; color:var(--text); margin-top:2px; }
.senti .sub { font-size:.8rem; color:var(--text-muted); margin-top:6px; }
.senti svg { width:100%; max-width:380px; height:auto; display:block; margin:0 auto; }
.senti svg text { fill:var(--text); font-family:inherit; }
.senti svg .muted { fill:var(--text-muted); }
.senti .z { stroke:var(--surface); stroke-width:2; opacity:.5; }
.senti .z.on { opacity:1; stroke:var(--text); stroke-width:1.5; }
.senti .z.xf{fill:var(--xf)} .senti .z.f{fill:var(--f)} .senti .z.n{fill:var(--n)}
.senti .z.g{fill:var(--g)} .senti .z.xg{fill:var(--xg)}
.senti .needle { stroke:var(--text); stroke-width:3; stroke-linecap:round; }
.senti .hub { fill:var(--text); }
.senti table { font-size:.8rem; margin-top:6px; }
.senti th, .senti td { padding:3px 6px; text-align:right; }
.senti th:first-child, .senti td:first-child { text-align:left; }
"""

CX, CY, R_OUT, R_IN = 190, 150, 120, 80


def _pt(score: float, r: float) -> tuple[float, float]:
    th = math.pi * (1 - score / 100)
    return CX + r * math.cos(th), CY - r * math.sin(th)


def _zone_path(lo: float, hi: float) -> str:
    a0, a1 = _pt(lo, R_OUT), _pt(hi, R_OUT)
    b1, b0 = _pt(hi, R_IN), _pt(lo, R_IN)
    return (f"M{a0[0]:.1f},{a0[1]:.1f} A{R_OUT},{R_OUT} 0 0 1 {a1[0]:.1f},{a1[1]:.1f} "
            f"L{b1[0]:.1f},{b1[1]:.1f} A{R_IN},{R_IN} 0 0 0 {b0[0]:.1f},{b0[1]:.1f} Z")


def _gauge_svg(f: dict) -> str:
    score = max(0.0, min(100.0, f["value"]))
    parts = [f'<svg viewBox="0 0 380 200" role="img" aria-label="CNN 공포·탐욕 지수 {score:.0f}, {f["zone"]}">']
    for lo, hi, name, cls in ZONES:
        on = " on" if cls == f["cls"] else ""
        parts.append(f'<path class="z {cls}{on}" d="{_zone_path(lo, hi)}"><title>{name} {lo}~{hi}</title></path>')
        lx, ly = _pt((lo + hi) / 2, R_OUT + 16)
        anchor = "end" if lx < CX - 20 else "start" if lx > CX + 20 else "middle"
        weight = ' font-weight="700"' if on else ""
        parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="11" text-anchor="{anchor}"{weight}>{name}</text>')
    for t in (0, 25, 50, 75, 100):
        tx, ty = _pt(t, R_IN - 12)
        parts.append(f'<text class="muted" x="{tx:.1f}" y="{ty + 4:.1f}" font-size="9" text-anchor="middle">{t}</text>')
    nx, ny = _pt(score, R_OUT - 6)
    parts.append(f'<line class="needle" x1="{CX}" y1="{CY}" x2="{nx:.1f}" y2="{ny:.1f}"><title>현재 {score:.1f}</title></line>')
    parts.append(f'<circle class="hub" cx="{CX}" cy="{CY}" r="6"/>')
    parts.append(f'<text x="{CX}" y="{CY + 36}" font-size="28" font-weight="700" text-anchor="middle">{score:.0f}</text>')
    parts.append("</svg>")
    return "".join(parts)


def widget_html(data: dict) -> str:
    v, f = data.get("vix"), data.get("fg")
    if v:
        arrow = "▲" if (v["chg_pct"] or 0) >= 0 else "▼"
        chg = f"{arrow} {abs(v['chg_pct']):.2f}% <span class=\"sub\">전일 대비</span>" if v["chg_pct"] is not None else ""
        level = "안정(20 미만)" if v["value"] < 20 else "경계(20~30)" if v["value"] < 30 else "공포 확대(30 이상)"
        vix_card = (f'<div class="card vix"><h4>VIX</h4><div class="hero">{v["value"]:.2f}</div>'
                    f'<div class="chg">{chg}</div>'
                    f'<div class="sub">{level} · {v["date"]} 종가 ({_html.escape(v["src"])})</div></div>')
    else:
        vix_card = '<div class="card vix"><h4>VIX</h4><div class="sub">수집 실패 — 판단 불가</div></div>'

    if f:
        def cell(x):
            return f"{x:.0f}" if x is not None else "—"
        table = ("<table><tr><th></th><th>현재</th><th>전일</th><th>1주 전</th><th>1달 전</th><th>1년 전</th></tr>"
                 f"<tr><td>점수</td><td>{cell(f['value'])}</td><td>{cell(f['prev'])}</td>"
                 f"<td>{cell(f['w1'])}</td><td>{cell(f['m1'])}</td><td>{cell(f['y1'])}</td></tr></table>")
        fg_card = (f'<div class="card"><h4>CNN 공포·탐욕 — {f["zone"]}</h4>{_gauge_svg(f)}{table}'
                   f'<div class="sub">{f["date"]} 기준 · 0 극단 공포 ~ 100 극단 탐욕 (CNN Business)</div></div>')
    else:
        fg_card = '<div class="card"><h4>CNN 공포·탐욕</h4><div class="sub">수집 실패 — 판단 불가</div></div>'
    return f'<style>{_CSS}</style><section class="senti" aria-label="시장 심리">{vix_card}{fg_card}</section>'
