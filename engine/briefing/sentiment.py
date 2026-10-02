"""시장 심리 위젯 — VIX(미국)·VKOSPI(한국) 카드 + CNN 공포·탐욕(미국) 게이지.

2026-10-01 신설, 2026-10-02 개편(사용자: "대상 시장을 표시하고, VKOSPI도 넣고,
과거 기록을 참고해 변화가 계속 업데이트되며 보이게").

- HTML 보고서(첨부 .html) → `widget_html()` : 카드 3개. 각 카드에 현재값·전일 대비,
  최근 3개월 추이선(점에 마우스를 올리면 날짜·값), 1주·1달·3달 전 값, 최근 1년 중
  현재 위치. 매 발행 때 수집 이력에서 다시 그리므로 날마다 자동으로 갱신된다.
- 메일 본문 → `text_line()` : 수치 한 줄(Gmail은 SVG를 못 그린다).

데이터: sources/macro-series.csv(us_vix/us_vix_yf 신선도 쌍둥이, us_fear_greed),
sources/daily-price-history.csv(code 0503 = VKOSPI, KIS 일봉). 없으면 R3대로
"수집 실패 — 판단 불가"로 표시하고 지어내지 않는다.

색: 공포↔탐욕 게이지는 양극(빨강↔회색↔파랑), 추이선은 단일 계열이라 한 색(파랑).
단계 색은 dataviz 검증기로 밝은(#fcfcfb)·어두운(#1c1f26) 표면에서 통과시켰다.
대비 3:1 미만 칸이 있어 구간 이름을 글자로 달고 숫자 표를 함께 둔다.
"""
from __future__ import annotations

import csv
import html as _html
import math
from datetime import date, timedelta
from pathlib import Path

from engine.briefing import context as C

DAILY_PRICE = Path(__file__).resolve().parents[2] / "sources" / "daily-price-history.csv"
VKOSPI_CODE = "0503"
SPARK_DAYS = 92          # 추이선 구간(달력일 기준 약 3개월)

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


def _daily_price(code: str) -> list[tuple[str, float]]:
    if not DAILY_PRICE.exists():
        return []
    out = {}
    with DAILY_PRICE.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("code") == code:
                try:
                    out[r["date"]] = float(r["close"])
                except (ValueError, TypeError):
                    continue
    return sorted(out.items())


def _summarize(rows: list[tuple[str, float]], as_of: date) -> dict | None:
    """현재값·전일 대비·1주/1달/3달 전·1년 중 위치·추이선 구간."""
    rows = [(d, v) for d, v in rows if d <= as_of.isoformat()]
    if len(rows) < 2:
        return None
    d0, v0 = rows[-1]
    last = date.fromisoformat(d0)
    year = [v for d, v in rows if d > (last - timedelta(days=365)).isoformat()]
    rank = sum(1 for v in year if v <= v0) / len(year) * 100 if year else None
    return {
        "value": v0, "date": d0, "prev": rows[-2][1],
        "chg_pct": (v0 / rows[-2][1] - 1) * 100 if rows[-2][1] else None,
        "w1": _value_on_or_before(rows, last - timedelta(days=7)),
        "m1": _value_on_or_before(rows, last - timedelta(days=30)),
        "m3": _value_on_or_before(rows, last - timedelta(days=91)),
        "pctile_1y": rank,
        "spark": [(d, v) for d, v in rows if d > (last - timedelta(days=SPARK_DAYS)).isoformat()],
    }


def collect(as_of: date) -> dict:
    m = C._series_map()
    out: dict = {"as_of": as_of.isoformat()}
    vix, src = C._freshest(m, "us_vix", as_of)
    s = _summarize(vix, as_of)
    if s:
        out["vix"] = {**s, "src": src or "fred"}
    s = _summarize(_daily_price(VKOSPI_CODE), as_of)
    if s:
        out["vkospi"] = {**s, "src": "KIS"}
    s = _summarize(m.get("us_fear_greed", []), as_of)
    if s:
        name, cls = zone_of(s["value"])
        out["fg"] = {**s, "zone": name, "cls": cls}
    return out


def _arrow(chg):
    return "▲" if (chg or 0) >= 0 else "▼"


def text_line(data: dict) -> str:
    """메일 본문용 한 줄(마크다운 인용)."""
    parts = []
    for key, label in (("vix", "VIX(미국)"), ("vkospi", "VKOSPI(한국)")):
        v = data.get(key)
        if v:
            chg = f" {_arrow(v['chg_pct'])}{abs(v['chg_pct']):.2f}%" if v["chg_pct"] is not None else ""
            parts.append(f"{label} **{v['value']:.2f}**{chg} ({v['date']})")
        else:
            parts.append(f"{label} 수집 실패 — 판단 불가")
    f = data.get("fg")
    if f:
        prev = f", 전일 {f['prev']:.0f}" if f.get("prev") is not None else ""
        parts.append(f"CNN 공포·탐욕(미국) **{f['value']:.0f}** ({f['zone']}{prev}, {f['date']})")
    else:
        parts.append("CNN 공포·탐욕(미국) 수집 실패 — 판단 불가")
    return "> 📊 시장 심리: " + " · ".join(parts) + " — 그래픽·추이는 첨부 HTML 보고서"


# ── HTML 위젯 ────────────────────────────────────────────────────────────

_CSS = """
.senti { --xf:#b8312f; --f:#ec8682; --n:#f0efec; --g:#6fa6ea; --xg:#1f5fae; --line:#2a78d6;
  display:flex; flex-wrap:wrap; gap:12px; margin:16px 0 20px; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) .senti { --xf:#e65f5a; --f:#a2342f; --n:#383835; --g:#2e5fa8; --xg:#4e91e4; --line:#3987e5; } }
:root[data-theme="dark"] .senti { --xf:#e65f5a; --f:#a2342f; --n:#383835; --g:#2e5fa8; --xg:#4e91e4; --line:#3987e5; }
.senti .card { flex:1 1 250px; background:var(--surface); border:1px solid var(--border);
  border-radius:10px; padding:12px 14px; min-width:0; }
.senti .card.wide { flex:2 1 340px; }
.senti .card h4 { margin:0 0 6px; font-size:.95rem; color:var(--text); }
.senti .card h4 .mk { font-weight:400; color:var(--text-muted); font-size:.82rem; }
.senti .hero { font-size:2.3rem; font-weight:700; line-height:1.1; color:var(--text);
  font-variant-numeric: tabular-nums; }
.senti .chg { font-size:.95rem; color:var(--text); margin-top:2px; }
.senti .sub { font-size:.78rem; color:var(--text-muted); margin-top:6px; }
.senti svg { width:100%; height:auto; display:block; }
.senti svg.gauge { max-width:340px; margin:0 auto; }
.senti svg.spark { max-width:420px; }
.senti .fgbody { display:flex; flex-wrap:wrap; gap:8px 16px; align-items:center; }
.senti .fgbody > svg.gauge { flex:1 1 240px; }
.senti .fgbody .fgside { flex:1 1 260px; min-width:0; }
.senti svg text { fill:var(--text); font-family:inherit; }
.senti svg .muted { fill:var(--text-muted); }
.senti .z { stroke:var(--surface); stroke-width:2; opacity:.5; }
.senti .z.on { opacity:1; stroke:var(--text); stroke-width:1.5; }
.senti .z.xf{fill:var(--xf)} .senti .z.f{fill:var(--f)} .senti .z.n{fill:var(--n)}
.senti .z.g{fill:var(--g)} .senti .z.xg{fill:var(--xg)}
.senti .needle { stroke:var(--text); stroke-width:3; stroke-linecap:round; }
.senti .hub { fill:var(--text); }
.senti .sp-line { fill:none; stroke:var(--line); stroke-width:2; stroke-linejoin:round; }
.senti .sp-ref { stroke:var(--border); stroke-width:1; stroke-dasharray:3 3; }
.senti .sp-last { fill:var(--line); stroke:var(--surface); stroke-width:2; }
.senti .sp-hit { fill:transparent; }
.senti .sp-hit:hover { fill:var(--line); opacity:.35; }
.senti table { width:100%; font-size:.78rem; margin-top:6px; border-collapse:collapse; }
.senti th, .senti td { padding:3px 4px; text-align:right; border-bottom:1px solid var(--border); }
.senti th { color:var(--text-muted); font-weight:500; }
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
    parts = [f'<svg class="gauge" viewBox="0 0 380 200" role="img" '
             f'aria-label="CNN 공포·탐욕 지수 {score:.0f}, {f["zone"]}">']
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


def _spark_svg(rows: list[tuple[str, float]], refs: list[tuple[float, str]], label: str,
               fmt: str = "{:.2f}") -> str:
    """최근 3개월 추이선. 기준선(refs)은 범위 안에 들 때만 점선으로. 점마다 툴팁."""
    if len(rows) < 2:
        return ""
    W, H, PL, PR, PT, PB = 300, 84, 30, 8, 8, 18
    vals = [v for _, v in rows]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.12 or 1.0
    lo, hi = lo - pad, hi + pad
    n = len(rows)

    def x(i): return PL + (W - PL - PR) * i / (n - 1)
    def y(v): return PT + (H - PT - PB) * (1 - (v - lo) / (hi - lo))

    out = [f'<svg class="spark" viewBox="0 0 {W} {H}" role="img" aria-label="{_html.escape(label)} 최근 3개월 추이">']
    for rv, rl in refs:
        if lo < rv < hi:
            out.append(f'<line class="sp-ref" x1="{PL}" x2="{W - PR}" y1="{y(rv):.1f}" y2="{y(rv):.1f}"/>'
                       f'<text class="muted" x="{PL - 4}" y="{y(rv) + 3:.1f}" font-size="9" text-anchor="end">{rl}</text>')
    pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, (_, v) in enumerate(rows))
    out.append(f'<polyline class="sp-line" points="{pts}"/>')
    for i, (d, v) in enumerate(rows):
        out.append(f'<circle class="sp-hit" cx="{x(i):.1f}" cy="{y(v):.1f}" r="6"><title>{d}  {fmt.format(v)}</title></circle>')
    out.append(f'<circle class="sp-last" cx="{x(n - 1):.1f}" cy="{y(vals[-1]):.1f}" r="4"/>')
    out.append(f'<text class="muted" x="{PL}" y="{H - 4}" font-size="9">{rows[0][0][5:]}</text>'
               f'<text class="muted" x="{W - PR}" y="{H - 4}" font-size="9" text-anchor="end">{rows[-1][0][5:]}</text>')
    out.append("</svg>")
    return "".join(out)


def _history_table(s: dict, fmt: str = "{:.2f}") -> str:
    def cell(v):
        return fmt.format(v) if v is not None else "—"
    pct = f"{s['pctile_1y']:.0f}%" if s.get("pctile_1y") is not None else "—"
    return ("<table><tr><th></th><th>전일</th><th>1주 전</th><th>1달 전</th><th>3달 전</th><th title='최근 1년 값 중 지금보다 낮거나 같은 날의 비율'>1년 백분위</th></tr>"
            f"<tr><td>값</td><td>{cell(s['prev'])}</td><td>{cell(s['w1'])}</td>"
            f"<td>{cell(s['m1'])}</td><td>{cell(s['m3'])}</td><td>{pct}</td></tr></table>")


def _vol_card(s: dict | None, title: str, market: str, refs, level_fn) -> str:
    head = f'<h4>{title} <span class="mk">({market})</span></h4>'
    if not s:
        return f'<div class="card">{head}<div class="sub">수집 실패 — 판단 불가</div></div>'
    chg = (f"{_arrow(s['chg_pct'])} {abs(s['chg_pct']):.2f}% <span class=\"sub\">전일 대비</span>"
           if s["chg_pct"] is not None else "")
    return (f'<div class="card">{head}<div class="hero">{s["value"]:.2f}</div><div class="chg">{chg}</div>'
            f'{_spark_svg(s["spark"], refs, title)}{_history_table(s)}'
            f'<div class="sub">{level_fn(s)} · {s["date"]} 종가 ({_html.escape(s["src"])})</div></div>')


def _vix_level(s):
    v = s["value"]
    return "안정(20 미만)" if v < 20 else "경계(20~30)" if v < 30 else "공포 확대(30 이상)"


def _rel_level(s):
    # VKOSPI는 국내 관행 임계값이 확립돼 있지 않아 자기 1년 분포로 읽는다
    p = s.get("pctile_1y")
    if p is None:
        return "1년 분포 부족"
    return "1년 중 낮은 편(평온)" if p < 33 else "1년 중 보통" if p < 67 else "1년 중 높은 편(불안)"


def widget_html(data: dict) -> str:
    vix_card = _vol_card(data.get("vix"), "VIX", "미국 S&P500", [(20, "20"), (30, "30")], _vix_level)
    vk = data.get("vkospi")
    vk_refs = []
    if vk:
        yr = sorted(v for _, v in vk["spark"]) or [vk["value"]]
        vk_refs = [(yr[len(yr) // 2], "중앙")]
    vk_card = _vol_card(vk, "VKOSPI", "한국 코스피200", vk_refs, _rel_level)

    f = data.get("fg")
    head = '<h4>CNN 공포·탐욕 <span class="mk">(미국 주식시장)</span>'
    if f:
        fg_card = (f'<div class="card wide">{head} — {f["zone"]}</h4><div class="fgbody">{_gauge_svg(f)}'
                   f'<div class="fgside">{_spark_svg(f["spark"], [(25, "25"), (50, "50"), (75, "75")], "공포·탐욕", "{:.0f}")}'
                   f'{_history_table(f, "{:.0f}")}</div></div>'
                   f'<div class="sub">{f["date"]} 기준 · 0 극단 공포 ~ 100 극단 탐욕 (CNN Business, 미국 지표 7개 합성)</div></div>')
    else:
        fg_card = f'<div class="card wide">{head}</h4><div class="sub">수집 실패 — 판단 불가</div></div>'
    return (f'<style>{_CSS}</style><section class="senti" aria-label="시장 심리">'
            f'{vix_card}{vk_card}{fg_card}</section>')
