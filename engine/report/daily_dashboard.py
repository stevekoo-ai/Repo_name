"""PEOS Daily Dashboard — a single URL the user opens every day to see
history/trend from the oldest data through 1년/6개월/1개월/1주일/오늘, per
their explicit request. Reads data/peos_daily_history.csv (one row per
calendar day, engine/report/daily_history.py) and renders a self-contained
page: a today snapshot banner, a shared period-zoom toggle, and a chart per
tracked metric (headline composite scores, then every KR indicator, then
every US indicator), plus a compact regime-change history (regime is
categorical, not chartable as a line).

Reuses html.py's _CSS/_esc so this page looks like the same product as the
monthly report rather than a separate one-off style.
"""
from __future__ import annotations

import html as html_lib
import json
from pathlib import Path

import pandas as pd

from core.config import rules_config
from . import payload as payload_mod
from .daily_history import DAILY_HISTORY_PATH
from .html import _CSS, _esc

REPO_ROOT = Path(__file__).resolve().parents[2]

HEADLINE_METRICS = [
    ("kr_raw_score", "한국 총점"), ("us_raw_score", "미국 총점"),
    ("kr_confidence", "한국 Confidence"), ("us_confidence", "미국 Confidence"),
    ("investment_environment_score", "Investment Environment"),
    ("semiconductor_score", "반도체"), ("bond_score", "채권"),
    ("fx_score", "환율"), ("housing_readiness_score", "청약 준비도"),
]

PERIODS = [("오늘", 1), ("1주일", 7), ("1개월", 30), ("6개월", 182), ("1년", 365), ("전체", None)]


def _indicator_labels(rules_key: str, order_key: str) -> list[tuple[str, str]]:
    rules = rules_config()[rules_key]
    order = payload_mod.INDICATOR_ORDER if order_key == "kr" else payload_mod.US_INDICATOR_ORDER
    prefix = "kr" if order_key == "kr" else "us"
    return [(f"{prefix}_{key}", rules.get(key, {}).get("label", key)) for key in order]


def _regime_changes(df: pd.DataFrame, column: str) -> list[dict]:
    changes = []
    prev = None
    for _, row in df.iterrows():
        val = row.get(column)
        if pd.isna(val):
            continue
        if val != prev:
            changes.append({"date": row["run_date"], "regime": val})
            prev = val
    return changes


def _chart_block(chart_id: str, label: str) -> str:
    return f"""
    <div class="daily-chart-card">
      <div class="daily-chart-label">{_esc(label)}</div>
      <div class="daily-chart" id="chart-{_esc(chart_id)}"></div>
    </div>"""


def _regime_history_table(changes: list[dict]) -> str:
    if not changes:
        return '<p class="tile-sub">기록된 국면 변경 이력이 없습니다.</p>'
    rows = "".join(f"<tr><td>{_esc(c['date'])}</td><td>{_esc(c['regime'])}</td></tr>" for c in reversed(changes))
    return f"""<div class="table-wrap"><table>
      <thead><tr><th>날짜</th><th>국면</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>"""


_DAILY_JS = """
var PEOS_DAILY_DATA = __DATA_JSON__;
var PEOS_CHART_IDS = __CHART_IDS_JSON__;
var peosCurrentWindow = 30;

function peosFilterSeries(dates, values, windowDays) {
  if (windowDays === null) return { dates: dates, values: values };
  var cutoff = dates.length - windowDays;
  if (cutoff < 0) cutoff = 0;
  return { dates: dates.slice(cutoff), values: values.slice(cutoff) };
}

function peosDrawChart(chartId) {
  var el = document.getElementById('chart-' + chartId);
  if (!el) return;
  var dates = PEOS_DAILY_DATA.dates;
  var raw = PEOS_DAILY_DATA.series[chartId] || [];
  var filtered = peosFilterSeries(dates, raw, peosCurrentWindow);
  var pairs = [];
  for (var i = 0; i < filtered.values.length; i++) {
    if (filtered.values[i] !== null && filtered.values[i] !== undefined) {
      pairs.push([filtered.dates[i], filtered.values[i]]);
    }
  }
  if (pairs.length < 2) {
    el.innerHTML = '<span class="muted spark-empty">이 구간에는 데이터가 부족합니다.</span>';
    return;
  }
  var width = 320, height = 64, pad = 6;
  var values = pairs.map(function (p) { return p[1]; });
  var lo = Math.min.apply(null, values), hi = Math.max.apply(null, values);
  var span = (hi - lo) || 1;
  var n = pairs.length;
  var pts = pairs.map(function (p, i) {
    var x = pad + (width - 2 * pad) * i / (n - 1);
    var y = height - pad - (height - 2 * pad) * (p[1] - lo) / span;
    return x.toFixed(1) + ',' + y.toFixed(1);
  }).join(' ');
  var lastX = pad + (width - 2 * pad);
  var lastY = height - pad - (height - 2 * pad) * (values[n - 1] - lo) / span;
  var startLabel = pairs[0][0] + ' · ' + pairs[0][1].toFixed(2);
  var endLabel = pairs[n - 1][0] + ' · ' + pairs[n - 1][1].toFixed(2);
  el.innerHTML =
    '<svg class="spark" viewBox="0 0 ' + width + ' ' + height + '" width="' + width + '" height="' + height + '">' +
    '<title>' + startLabel + ' \\u2192 ' + endLabel + '</title>' +
    '<polyline points="' + pts + '" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<circle cx="' + lastX.toFixed(1) + '" cy="' + lastY.toFixed(1) + '" r="2.5" fill="var(--accent)"/>' +
    '</svg><div class="spark-labels"><span>' + pairs[0][0] + '</span><span>' + pairs[n - 1][0] + '</span></div>';
}

function peosRedrawAll() {
  for (var i = 0; i < PEOS_CHART_IDS.length; i++) peosDrawChart(PEOS_CHART_IDS[i]);
}

function peosSetPeriod(days, btn) {
  peosCurrentWindow = days;
  var buttons = document.querySelectorAll('.period-toggle button');
  for (var i = 0; i < buttons.length; i++) buttons[i].classList.remove('active');
  btn.classList.add('active');
  peosRedrawAll();
}

document.addEventListener('DOMContentLoaded', peosRedrawAll);
"""


def render_daily_dashboard(history_path: Path | None = None) -> str:
    history_path = history_path or DAILY_HISTORY_PATH
    if not history_path.exists() or history_path.stat().st_size == 0:
        df = pd.DataFrame(columns=["run_date"])
    else:
        df = pd.read_csv(history_path).sort_values("run_date").reset_index(drop=True)

    dates = df["run_date"].tolist() if not df.empty else []
    numeric_cols = [c for c in df.columns if c not in ("run_date", "kr_regime", "us_regime")]
    series = {}
    for col in numeric_cols:
        series[col] = [None if pd.isna(v) else float(v) for v in df[col]] if not df.empty else []

    latest = df.iloc[-1].to_dict() if not df.empty else {}
    kr_regime_changes = _regime_changes(df, "kr_regime") if not df.empty else []
    us_regime_changes = _regime_changes(df, "us_regime") if not df.empty else []

    headline_charts = "".join(_chart_block(key, label) for key, label in HEADLINE_METRICS)
    kr_charts = "".join(_chart_block(key, label) for key, label in _indicator_labels("macro", "kr"))
    us_charts = "".join(_chart_block(key, label) for key, label in _indicator_labels("macro_us", "us"))

    period_buttons = "".join(
        f'<button type="button" class="{"active" if days == 30 else ""}" '
        f'onclick="peosSetPeriod({days if days is not None else "null"}, this)">{_esc(label)}</button>'
        for label, days in PERIODS
    )

    chart_ids = [key for key, _ in HEADLINE_METRICS] + [k for k, _ in _indicator_labels("macro", "kr")] + \
        [k for k, _ in _indicator_labels("macro_us", "us")]

    data_json = json.dumps({"dates": dates, "series": series}, ensure_ascii=False).replace("</script", "<\\/script")
    js = (_DAILY_JS
          .replace("__DATA_JSON__", data_json)
          .replace("__CHART_IDS_JSON__", json.dumps(chart_ids)))

    snapshot_date = latest.get("run_date", "N/A")
    kr_regime = latest.get("kr_regime", "N/A")
    us_regime = latest.get("us_regime", "N/A")

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PEOS Daily Dashboard</title>
<style>{_CSS}
.period-toggle {{ display: flex; gap: 6px; flex-wrap: wrap; margin: 10px 0 16px; }}
.period-toggle button {{ font-family: inherit; font-size: 0.82rem; font-weight: 600; padding: 6px 14px;
  border-radius: 999px; border: 1px solid var(--border); background: var(--surface); color: var(--text);
  cursor: pointer; }}
.period-toggle button.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
.daily-chart-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }}
.daily-chart-card {{ background: var(--surface-2); border: 1px solid var(--border); border-radius: 10px; padding: 10px 12px; }}
.daily-chart-label {{ font-size: 0.82rem; font-weight: 600; color: var(--text-muted); margin-bottom: 4px; }}
</style>
</head>
<body>
<div class="page">
  <header class="masthead">
    <h1>PEOS Daily Dashboard</h1>
    <div class="sub">매일 06:00 KST 자동 갱신 · 오늘 기준일: {_esc(snapshot_date)} ·
      <a href="index.html">Investment Clock 대시보드</a></div>
  </header>

  <section class="card">
    <h2>오늘 스냅샷</h2>
    <div class="tile-grid">
      {_stat_tile_html("미국 국면", us_regime)}
      {_stat_tile_html("한국 국면", kr_regime)}
      {_stat_tile_html("Investment Environment", _fmt_score(latest.get("investment_environment_score")))}
      {_stat_tile_html("반도체", _fmt_score(latest.get("semiconductor_score")))}
    </div>
  </section>

  <section class="card">
    <h2>기간 선택</h2>
    <p class="tile-sub">아래 버튼으로 모든 차트의 기간을 한 번에 바꿀 수 있습니다. 처음 며칠은 데이터가 적어 짧게 보일 수 있고, 매일 쌓일수록 길어집니다.</p>
    <div class="period-toggle">{period_buttons}</div>
  </section>

  <section class="card">
    <h2>핵심 점수 추세</h2>
    <div class="daily-chart-grid">{headline_charts}</div>
  </section>

  <section class="card">
    <h2>한국 Core-10 개별 지표 추세</h2>
    <div class="daily-chart-grid">{kr_charts}</div>
  </section>

  <section class="card">
    <h2>미국 Core Macro 개별 지표 추세</h2>
    <div class="daily-chart-grid">{us_charts}</div>
  </section>

  <section class="card">
    <h2>국면 변경 이력</h2>
    <div class="grid" style="display:flex; gap: 18px; flex-wrap: wrap;">
      <div style="flex:1 1 260px;"><h3>한국</h3>{_regime_history_table(kr_regime_changes)}</div>
      <div style="flex:1 1 260px;"><h3>미국</h3>{_regime_history_table(us_regime_changes)}</div>
    </div>
  </section>

  <footer>PEOS Daily Dashboard — 자동 생성, 투자 자문 아님. 매일 06:00 KST 파이프라인 실행 결과를 누적합니다.</footer>
</div>
<script>{js}</script>
</body>
</html>"""


def _stat_tile_html(label: str, value) -> str:
    value_str = "Pending" if value is None else html_lib.escape(str(value))
    return f"""<div class="tile"><div class="tile-label">{html_lib.escape(label)}</div>
      <div class="tile-value">{value_str}</div></div>"""


def _fmt_score(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    return f"{float(value):.1f}점"


def write_daily_dashboard(out_path: Path | None = None) -> Path:
    out_path = out_path or (REPO_ROOT / "docs" / "peos-daily.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_daily_dashboard(), encoding="utf-8")
    return out_path


def main() -> None:
    path = write_daily_dashboard()
    print(f"Daily dashboard: {path}")


if __name__ == "__main__":
    main()
