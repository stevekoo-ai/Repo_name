"""Build the static HTML dashboard (docs/index.html) for GitHub Pages.

Besides the "current" clock (a pre-rendered PNG), the page embeds the full
history table as JSON and draws a second, interactive clock on a <canvas>
element, driven by a slider / month picker / play button. Everything is
client-side JS with no build step, since GitHub Pages only serves static
files.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .model import PHASES, ClockReading

PAGE_TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>Macro Investment Clock</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { font-family: -apple-system, "Segoe UI", sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; background:#fafafa; }
  h1 { font-size: 1.4rem; }
  h3 { margin-top: 2rem; }
  .updated { color: #666; font-size: 0.85rem; margin-bottom: 1.5rem; }
  .phase-banner { padding: 1rem; border-radius: 10px; background: __PHASE_COLOR__22; border: 2px solid __PHASE_COLOR__; margin-bottom: 1.5rem; }
  .phase-banner b { color: __PHASE_COLOR__; }
  img { max-width: 100%; height: auto; border-radius: 8px; }
  .grid { display: flex; gap: 1.5rem; flex-wrap: wrap; }
  .grid > div { flex: 1 1 320px; }
  table { border-collapse: collapse; width: 100%; font-size: 0.85rem; margin-top: 1rem; }
  th, td { border: 1px solid #ddd; padding: 6px 10px; text-align: right; }
  th { background: #f0f0f0; }
  td:first-child, th:first-child { text-align: left; }
  footer { margin-top: 2rem; color: #888; font-size: 0.8rem; }

  .timemachine { display: flex; gap: 1.5rem; flex-wrap: wrap; align-items: center; background: #fff; border: 1px solid #e2e2e2; border-radius: 10px; padding: 1.2rem; }
  .timemachine canvas { flex: 0 0 auto; max-width: 360px; width: 100%; height: auto; }
  .tm-controls { flex: 1 1 320px; min-width: 260px; }
  .tm-controls input[type="range"] { width: 100%; }
  .tm-row { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.6rem; flex-wrap: wrap; }
  .tm-date { font-weight: bold; font-size: 1rem; }
  .tm-phase { font-size: 1.05rem; margin: 0.3rem 0; }
  .tm-detail { color: #444; font-size: 0.85rem; }
  .tm-buttons button, .tm-row input[type="month"] { padding: 0.4rem 0.8rem; border-radius: 6px; border: 1px solid #ccc; background: #f5f5f5; cursor: pointer; font-size: 0.85rem; }
  .tm-buttons { margin-top: 0.6rem; display: flex; gap: 0.5rem; flex-wrap: wrap; }
</style>
</head>
<body>
<h1>거시경제 투자 시계 (Macro Investment Clock)</h1>
<p class="updated">Last updated: __UPDATED_AT__ (data as of __DATA_ASOF__, __HISTORY_COUNT__ months on record) ·
  <a href="peos-daily.html">PEOS Daily Dashboard 보기</a></p>

<div class="phase-banner">
  현재 국면: <b>__PHASE_NAME__ (__PHASE_NAME_KR__)</b> &mdash; 유리한 자산군: <b>__ASSET__ (__ASSET_KR__)</b><br>
  성장 모멘텀: __GROWTH_SIGNAL__ (3개월 변화 __GROWTH_CHANGE__) · 물가(CPI YoY) 모멘텀: __INFLATION_SIGNAL__ (3개월 변화 __INFLATION_CHANGE__%p)
</div>

<div class="grid">
  <div><h3>Clock (현재)</h3><img src="clock.png" alt="investment clock"></div>
  <div>
    <h3>Context</h3>
    <ul>
      <li>CPI YoY: __INFLATION_YOY__%</li>
      <li>Core CPI YoY: __CORE_CPI__</li>
      <li>10Y-2Y Treasury spread: __YIELD_CURVE__</li>
      <li>Unemployment rate: __UNEMPLOYMENT__</li>
    </ul>
  </div>
</div>

<h3>타임머신 시계 &mdash; 과거 국면 조회</h3>
<p style="color:#555; font-size:0.9rem;">슬라이더나 월 선택으로 과거 특정 시점의 투자 시계를 확인하세요. 재생 버튼으로 전체 기간의 변화를 애니메이션으로 볼 수 있습니다.</p>
<div class="timemachine">
  <canvas id="tm-canvas" width="360" height="360"></canvas>
  <div class="tm-controls">
    <div class="tm-row">
      <input type="month" id="tm-month">
      <span class="tm-date" id="tm-date"></span>
    </div>
    <input type="range" id="tm-slider" min="0" max="0" value="0" step="1">
    <div class="tm-phase" id="tm-phase"></div>
    <div class="tm-detail" id="tm-detail"></div>
    <div class="tm-buttons">
      <button type="button" id="tm-prev">&#9664; 이전 달</button>
      <button type="button" id="tm-play">&#9654; 재생</button>
      <button type="button" id="tm-next">다음 달 &#9654;</button>
    </div>
  </div>
</div>

<h3>Trend (전체 기간)</h3>
<div class="grid">
  <div><img src="trend_growth.png" alt="growth trend"></div>
  <div><img src="trend_inflation.png" alt="inflation trend"></div>
</div>

<h3>History (최근 30개월)</h3>
__HISTORY_TABLE__

<footer>
  Model: Merrill Lynch Investment Clock (growth vs. inflation momentum, 2-axis / 4-phase).
  Data: FRED (OECD CLI, CPI, Industrial Production, Treasury spread, unemployment), currently-published (revised) series.
  Auto-generated, not investment advice.
</footer>

<script type="application/json" id="clock-history-data">__HISTORY_JSON__</script>
<script type="application/json" id="clock-phases-data">__PHASES_JSON__</script>
<script>
(function () {
  var history = JSON.parse(document.getElementById('clock-history-data').textContent);
  var phases = JSON.parse(document.getElementById('clock-phases-data').textContent);
  if (!history.length) { return; }

  var canvas = document.getElementById('tm-canvas');
  var ctx = canvas.getContext('2d');
  var slider = document.getElementById('tm-slider');
  var monthInput = document.getElementById('tm-month');
  var dateEl = document.getElementById('tm-date');
  var phaseEl = document.getElementById('tm-phase');
  var detailEl = document.getElementById('tm-detail');
  var prevBtn = document.getElementById('tm-prev');
  var nextBtn = document.getElementById('tm-next');
  var playBtn = document.getElementById('tm-play');

  var HOUR_ANGLE = { 12: -Math.PI / 2, 3: 0, 6: Math.PI / 2, 9: Math.PI };
  var playTimer = null;

  slider.max = String(history.length - 1);

  function fmt(v) {
    return (v === null || v === undefined || Number.isNaN(v)) ? 'N/A' : Number(v).toFixed(2);
  }

  function drawClock(rec) {
    var w = canvas.width, h = canvas.height;
    var cx = w / 2, cy = h / 2, R = Math.min(w, h) / 2 - 14;
    ctx.clearRect(0, 0, w, h);

    Object.keys(phases).forEach(function (name) {
      var p = phases[name];
      var center = HOUR_ANGLE[p.hour];
      var isActive = name === rec.phase;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, R, center - Math.PI / 4, center + Math.PI / 4);
      ctx.closePath();
      ctx.fillStyle = p.color;
      ctx.globalAlpha = isActive ? 0.85 : 0.22;
      ctx.fill();
      ctx.globalAlpha = 1;
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();

      var lx = cx + Math.cos(center) * R * 0.62;
      var ly = cy + Math.sin(center) * R * 0.62;
      ctx.textAlign = 'center';
      ctx.fillStyle = isActive ? '#ffffff' : '#444444';
      ctx.font = (isActive ? 'bold ' : '') + '13px sans-serif';
      ctx.fillText(p.name, lx, ly - 6);
      ctx.font = (isActive ? 'bold ' : '') + '11px sans-serif';
      ctx.fillText('(' + p.asset + ')', lx, ly + 10);
    });

    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, 2 * Math.PI);
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#222222';
    ctx.stroke();

    var activePhase = phases[rec.phase];
    if (activePhase) {
      var angle = HOUR_ANGLE[activePhase.hour];
      var hx = cx + Math.cos(angle) * R * 0.7;
      var hy = cy + Math.sin(angle) * R * 0.7;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(hx, hy);
      ctx.lineWidth = 5;
      ctx.strokeStyle = '#111111';
      ctx.stroke();
    }
    ctx.beginPath();
    ctx.arc(cx, cy, 5, 0, 2 * Math.PI);
    ctx.fillStyle = '#111111';
    ctx.fill();
  }

  function render(idx) {
    idx = Math.max(0, Math.min(history.length - 1, idx));
    slider.value = String(idx);
    var rec = history[idx];
    monthInput.value = rec.data_asof.slice(0, 7);
    dateEl.textContent = rec.data_asof + ' 기준';
    var p = phases[rec.phase];
    phaseEl.innerHTML = '<b>' + p.name + ' (' + p.name_kr + ')</b> &rarr; ' + p.asset + ' (' + p.asset_kr + ')';
    detailEl.textContent =
      '성장 ' + rec.growth_signal + ' (3개월 변화 ' + fmt(rec.growth_change_3m) + ') · ' +
      '물가 YoY ' + fmt(rec.inflation_yoy) + '% ' + rec.inflation_signal +
      ' (3개월 변화 ' + fmt(rec.inflation_change_3m) + '%p)';
    drawClock(rec);
  }

  slider.addEventListener('input', function () { render(parseInt(slider.value, 10)); });
  prevBtn.addEventListener('click', function () { render(parseInt(slider.value, 10) - 1); });
  nextBtn.addEventListener('click', function () { render(parseInt(slider.value, 10) + 1); });
  monthInput.addEventListener('change', function () {
    var target = monthInput.value;
    var bestIdx = 0;
    for (var i = 0; i < history.length; i++) {
      if (history[i].data_asof.slice(0, 7) <= target) { bestIdx = i; }
    }
    render(bestIdx);
  });
  playBtn.addEventListener('click', function () {
    if (playTimer) {
      clearInterval(playTimer);
      playTimer = null;
      playBtn.innerHTML = '&#9654; 재생';
      return;
    }
    playBtn.innerHTML = '&#9208; 정지';
    playTimer = setInterval(function () {
      var idx = parseInt(slider.value, 10) + 1;
      if (idx > history.length - 1) { idx = 0; }
      render(idx);
    }, 350);
  });

  render(history.length - 1);
})();
</script>
</body>
</html>
"""


def _fmt(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "N/A"
    return f"{v:.2f}"


def _phases_config() -> dict:
    return {
        p["name"]: {
            "name": p["name"],
            "name_kr": p["name_kr"],
            "asset": p["asset"],
            "asset_kr": p["asset_kr"],
            "hour": p["hour"],
            "color": p["color"],
        }
        for p in PHASES.values()
    }


def _history_records(history: pd.DataFrame) -> list[dict]:
    cols = [
        "data_asof", "phase", "asset",
        "growth_value", "growth_signal", "growth_change_3m",
        "inflation_yoy", "inflation_signal", "inflation_change_3m",
    ]
    safe = history[cols].astype(object).where(pd.notna(history[cols]), None)
    return safe.to_dict("records")


def render_report(
    reading: ClockReading,
    history: pd.DataFrame,
    run_date: pd.Timestamp,
    out_path: str | Path,
) -> Path:
    out_path = Path(out_path)
    as_of = max(reading.growth.as_of, reading.inflation.as_of).date().isoformat()

    recent = history.sort_values("data_asof").tail(30)
    history_table = recent.to_html(
        index=False,
        columns=["data_asof", "growth_value", "growth_signal", "inflation_yoy", "inflation_signal", "phase", "asset"],
        float_format=lambda x: f"{x:.2f}",
    )

    html = PAGE_TEMPLATE
    replacements = {
        "__UPDATED_AT__": run_date.date().isoformat(),
        "__DATA_ASOF__": as_of,
        "__HISTORY_COUNT__": str(len(history)),
        "__PHASE_NAME__": reading.phase["name"],
        "__PHASE_NAME_KR__": reading.phase["name_kr"],
        "__PHASE_COLOR__": reading.phase["color"],
        "__ASSET__": reading.phase["asset"],
        "__ASSET_KR__": reading.phase["asset_kr"],
        "__GROWTH_SIGNAL__": reading.growth.label,
        "__GROWTH_CHANGE__": f"{reading.growth.change:+.2f}",
        "__INFLATION_SIGNAL__": reading.inflation.label,
        "__INFLATION_CHANGE__": f"{reading.inflation.change:+.2f}",
        "__INFLATION_YOY__": f"{reading.inflation.value:.2f}",
        "__CORE_CPI__": _fmt(reading.context.get("core_cpi_yoy")),
        "__YIELD_CURVE__": _fmt(reading.context.get("yield_curve_10y2y")),
        "__UNEMPLOYMENT__": _fmt(reading.context.get("unemployment_rate")),
        "__HISTORY_TABLE__": history_table,
        "__HISTORY_JSON__": json.dumps(_history_records(history), ensure_ascii=False),
        "__PHASES_JSON__": json.dumps(_phases_config(), ensure_ascii=False),
    }
    for token, value in replacements.items():
        html = html.replace(token, value)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return out_path
