"""Build the static HTML dashboard (docs/index.html) for GitHub Pages."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .model import ClockReading

TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>Macro Investment Clock</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: -apple-system, "Segoe UI", sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; background:#fafafa; }}
  h1 {{ font-size: 1.4rem; }}
  .updated {{ color: #666; font-size: 0.85rem; margin-bottom: 1.5rem; }}
  .phase-banner {{ padding: 1rem; border-radius: 10px; background: {phase_color}22; border: 2px solid {phase_color}; margin-bottom: 1.5rem; }}
  .phase-banner b {{ color: {phase_color}; }}
  img {{ max-width: 100%; height: auto; border-radius: 8px; }}
  .grid {{ display: flex; gap: 1.5rem; flex-wrap: wrap; }}
  .grid > div {{ flex: 1 1 320px; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 0.85rem; margin-top: 1rem; }}
  th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: right; }}
  th {{ background: #f0f0f0; }}
  td:first-child, th:first-child {{ text-align: left; }}
  footer {{ margin-top: 2rem; color: #888; font-size: 0.8rem; }}
</style>
</head>
<body>
<h1>거시경제 투자 시계 (Macro Investment Clock)</h1>
<p class="updated">Last updated: {updated_at} (data as of {data_asof}) ·
  <a href="peos-daily.html">PEOS Daily Dashboard 보기</a></p>

<div class="phase-banner">
  현재 국면: <b>{phase_name} ({phase_name_kr})</b> &mdash; 유리한 자산군: <b>{asset} ({asset_kr})</b><br>
  성장 모멘텀: {growth_signal} (3개월 변화 {growth_change:+.2f}) · 물가(CPI YoY) 모멘텀: {inflation_signal} (3개월 변화 {inflation_change:+.2f}%p)
</div>

<div class="grid">
  <div><h3>Clock</h3><img src="clock.png" alt="investment clock"></div>
  <div>
    <h3>Context</h3>
    <ul>
      <li>CPI YoY: {inflation_yoy:.2f}%</li>
      <li>Core CPI YoY: {core_cpi_yoy}</li>
      <li>10Y-2Y Treasury spread: {yield_curve}</li>
      <li>Unemployment rate: {unemployment}</li>
    </ul>
  </div>
</div>

<h3>Trend</h3>
<div class="grid">
  <div><img src="trend_growth.png" alt="growth trend"></div>
  <div><img src="trend_inflation.png" alt="inflation trend"></div>
</div>

<h3>History (last 30 runs)</h3>
{history_table}

<footer>
  Model: Merrill Lynch Investment Clock (growth vs. inflation momentum, 2-axis / 4-phase).
  Data: FRED (OECD CLI, CPI, Industrial Production, Treasury spread, unemployment). Auto-generated, not investment advice.
</footer>
</body>
</html>
"""


def _fmt(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "N/A"
    return f"{v:.2f}"


def render_report(
    reading: ClockReading,
    history: pd.DataFrame,
    run_date: pd.Timestamp,
    out_path: str | Path,
) -> Path:
    out_path = Path(out_path)
    as_of = max(reading.growth.as_of, reading.inflation.as_of).date().isoformat()

    recent = history.drop_duplicates(subset=["data_asof"], keep="last").sort_values("data_asof").tail(30)
    history_table = recent.to_html(
        index=False,
        columns=["data_asof", "growth_value", "growth_signal", "inflation_yoy", "inflation_signal", "phase", "asset"],
        float_format=lambda x: f"{x:.2f}",
    )

    html = TEMPLATE.format(
        updated_at=run_date.date().isoformat(),
        data_asof=as_of,
        phase_name=reading.phase["name"],
        phase_name_kr=reading.phase["name_kr"],
        phase_color=reading.phase["color"],
        asset=reading.phase["asset"],
        asset_kr=reading.phase["asset_kr"],
        growth_signal=reading.growth.label,
        growth_change=reading.growth.change,
        inflation_signal=reading.inflation.label,
        inflation_change=reading.inflation.change,
        inflation_yoy=reading.inflation.value,
        core_cpi_yoy=_fmt(reading.context.get("core_cpi_yoy")),
        yield_curve=_fmt(reading.context.get("yield_curve_10y2y")),
        unemployment=_fmt(reading.context.get("unemployment_rate")),
        history_table=history_table,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return out_path
