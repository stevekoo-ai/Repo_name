"""부동산 매매·전월세 Daily Dashboard — docs/real-estate-daily.html.

사용자 요청: "HTML보고서에 부동산 매매가 전월세에 대해서 쌓인 데이터만큼
daily 그래프로 보여줘 트렌드가 보고싶다."

2026-09-02에 부동산 매매/전월세 실거래가 섹션이 PEOS(engine/report/html_new.py)
에서 청약 리포트(engine/report/subscription_report.py)로 옮겨갔는데, 그 리포트는
의도적으로 plain-text 이메일이라 그래프를 담을 수 없다(scripts/send_subscription_report_email.py
docstring 참조). 이 모듈은 그 공백을 메운다 — docs/peos-daily.html(engine/report/daily_dashboard.py)
과 같은 패턴(외부 차트 라이브러리 없는 자체 SVG 스파크라인 + 기간 토글)의 독립
페이지를 만들어, 국토교통부 실거래가(collectors/molit*.py)가 이미 정규화 저장소
(data/normalized/molit_*.csv)에 쌓아둔 이력을 그대로 차트로 그린다.

정직성 노트(7.9/R3): MOLIT 실거래가는 원천적으로 "월별 신고 집계"다 — 매일 새
포인트가 찍히는 게 아니라, 매일 재수집을 시도해서 그 달의 최신 신고분이
반영되면 그 달 포인트 값이 갱신되고, 새 달이 되면 포인트가 하나 늘어난다.
"daily 그래프"라는 요청은 그래서 "매일 갱신되는 그래프"로 구현한다(실제 포인트
밀도를 매일로 지어내지 않는다) — 페이지 상단에 이 사실을 명시한다.
"""
from __future__ import annotations

import json
from pathlib import Path

from collectors import base as collector_base
from collectors import kr_regions
from .html import _CSS, _esc

REPO_ROOT = Path(__file__).resolve().parents[2]

_TIERS = [("seoul", "서울"), ("capital_area", "수도권"), ("nationwide", "전국(대표표본)")]
_HIGHLIGHT_NAME = kr_regions.HIGHLIGHT_REGION["name"]  # 용인 기흥구 — 청약 타겟(플랫폼시티) 인근

# (그룹 제목, 정규화 series 접두어, 값 필드 suffix, 단위 라벨)
# 접두어+"_"+tier+"_"+suffix+"_pyeong" / 접두어+"_highlight_"+suffix+"_pyeong" 규칙은
# collectors/molit.py·molit_villa.py·molit_officetel.py·molit_rent.py 4개 수집기가
# 전부 공유하는 저장 규칙(engine/real_estate/market_trend.py·rent_trend.py가 같은
# 규칙으로 읽는다) — 여기서도 그대로 재사용, 새 계산 없음.
_METRIC_GROUPS = [
    {"title": "아파트 매매", "prefix": "molit", "suffix": "price", "unit": "평당가(만원)"},
    {"title": "연립다세대(빌라) 매매", "prefix": "molit_villa", "suffix": "price", "unit": "평당가(만원)"},
    {"title": "오피스텔 매매", "prefix": "molit_officetel", "suffix": "price", "unit": "평당가(만원)"},
    {"title": "아파트 전세", "prefix": "molit_rent_jeonse", "suffix": "price", "unit": "평당 보증금(만원)"},
    {"title": "아파트 월세 — 보증금", "prefix": "molit_rent_wolse", "suffix": "deposit", "unit": "평당 보증금(만원)"},
    {"title": "아파트 월세 — 월세액", "prefix": "molit_rent_wolse", "suffix": "rent", "unit": "평당 월세(만원)"},
]

PERIODS = [("3개월", 90), ("6개월", 182), ("1년", 365), ("전체", None)]

_MANWON = 10_000


def _read_series(series_id: str) -> dict:
    df = collector_base.read_normalized(series_id)
    if df.empty:
        return {"dates": [], "values": []}
    df = df.sort_values("date").reset_index(drop=True)
    return {
        "dates": [str(d) for d in df["date"]],
        "values": [round(float(v) / _MANWON, 1) for v in df["value"]],
    }


def _chart_block(chart_id: str, label: str, source_note: str = "") -> str:
    note_html = f'<div class="daily-chart-source">{_esc(source_note)}</div>' if source_note else ""
    return f"""
    <div class="daily-chart-card">
      <div class="daily-chart-label">{_esc(label)}</div>
      <div class="daily-chart" id="chart-{_esc(chart_id)}"></div>
      {note_html}
    </div>"""


_RE_JS = """
var RE_DAILY_DATA = __DATA_JSON__;
var RE_CHART_IDS = __CHART_IDS_JSON__;
var reCurrentWindow = null;

function reFilterSeries(dates, values, windowDays) {
  if (windowDays === null || dates.length === 0) return { dates: dates, values: values };
  var lastTime = new Date(dates[dates.length - 1]).getTime();
  var cutoffTime = lastTime - windowDays * 86400000;
  var outDates = [], outValues = [];
  for (var i = 0; i < dates.length; i++) {
    if (new Date(dates[i]).getTime() >= cutoffTime) {
      outDates.push(dates[i]);
      outValues.push(values[i]);
    }
  }
  return { dates: outDates, values: outValues };
}

function reDrawChart(chartId) {
  var el = document.getElementById('chart-' + chartId);
  if (!el) return;
  var entry = RE_DAILY_DATA.series[chartId] || { dates: [], values: [] };
  var filtered = reFilterSeries(entry.dates, entry.values, reCurrentWindow);
  var pairs = [];
  for (var i = 0; i < filtered.values.length; i++) {
    if (filtered.values[i] !== null && filtered.values[i] !== undefined) {
      pairs.push([filtered.dates[i], filtered.values[i]]);
    }
  }
  if (pairs.length < 2) {
    el.innerHTML = '<span class="muted spark-empty">이 구간에는 데이터가 부족합니다' +
      (pairs.length === 1 ? ' (1개월치만 존재: ' + pairs[0][0] + ' · ' + pairs[0][1] + ')' : '') + '.</span>';
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
  var startLabel = pairs[0][0] + ' · ' + pairs[0][1].toFixed(1) + '만원';
  var endLabel = pairs[n - 1][0] + ' · ' + pairs[n - 1][1].toFixed(1) + '만원';
  el.innerHTML =
    '<svg class="spark" viewBox="0 0 ' + width + ' ' + height + '" width="' + width + '" height="' + height + '">' +
    '<title>' + startLabel + ' \\u2192 ' + endLabel + '</title>' +
    '<polyline points="' + pts + '" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<circle cx="' + lastX.toFixed(1) + '" cy="' + lastY.toFixed(1) + '" r="2.5" fill="var(--accent)"/>' +
    '</svg><div class="spark-labels"><span>' + pairs[0][0] + '</span><span>' + pairs[n - 1][0] + '</span></div>';
}

function reRedrawAll() {
  for (var i = 0; i < RE_CHART_IDS.length; i++) reDrawChart(RE_CHART_IDS[i]);
}

function reSetPeriod(days, btn) {
  reCurrentWindow = days;
  var buttons = document.querySelectorAll('.period-toggle button');
  for (var i = 0; i < buttons.length; i++) buttons[i].classList.remove('active');
  btn.classList.add('active');
  reRedrawAll();
}

document.addEventListener('DOMContentLoaded', reRedrawAll);
"""


def render_real_estate_dashboard() -> str:
    series: dict[str, dict] = {}
    group_sections = []

    for group in _METRIC_GROUPS:
        prefix, suffix, unit = group["prefix"], group["suffix"], group["unit"]
        blocks = []
        for tier, tier_label in _TIERS:
            chart_id = f"{prefix}_{suffix}_{tier}"
            entry = _read_series(f"{prefix}_{tier}_{suffix}_pyeong")
            series[chart_id] = entry
            note = f"{unit} · {entry['dates'][0]}부터 누적" if entry["dates"] else "데이터 없음 (DATA_GO_KR_KEY 미설정 또는 미수집)"
            blocks.append(_chart_block(chart_id, tier_label, note))

        hl_chart_id = f"{prefix}_{suffix}_highlight"
        hl_entry = _read_series(f"{prefix}_highlight_{suffix}_pyeong")
        series[hl_chart_id] = hl_entry
        hl_note = f"{unit} · {hl_entry['dates'][0]}부터 누적" if hl_entry["dates"] else "데이터 없음"
        blocks.append(_chart_block(hl_chart_id, f"청약 타겟 인근 — {_HIGHLIGHT_NAME}", hl_note))

        group_sections.append(f"""
  <section class="card">
    <h2>{_esc(group['title'])} <span class="tile-sub">({_esc(unit)})</span></h2>
    <div class="daily-chart-grid">{''.join(blocks)}</div>
  </section>""")

    chart_ids = [f"{g['prefix']}_{g['suffix']}_{tier}" for g in _METRIC_GROUPS for tier, _ in _TIERS] + \
        [f"{g['prefix']}_{g['suffix']}_highlight" for g in _METRIC_GROUPS]

    period_buttons = "".join(
        f'<button type="button" class="{"active" if days is None else ""}" '
        f'onclick="reSetPeriod({days if days is not None else "null"}, this)">{_esc(label)}</button>'
        for label, days in PERIODS
    )

    any_data = any(s["dates"] for s in series.values())
    latest_dates = sorted({s["dates"][-1] for s in series.values() if s["dates"]}, reverse=True)
    latest_month = latest_dates[0][:7] if latest_dates else "N/A"

    data_json = json.dumps({"series": series}, ensure_ascii=False).replace("</script", "<\\/script")
    js = (_RE_JS
          .replace("__DATA_JSON__", data_json)
          .replace("__CHART_IDS_JSON__", json.dumps(chart_ids)))

    empty_notice = "" if any_data else """
  <section class="card">
    <p class="tile-sub">아직 수집된 실거래가 데이터가 없습니다 — DATA_GO_KR_KEY 시크릿 설정 또는
    real-estate-sync.yml 최초 실행을 확인하십시오.</p>
  </section>"""

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>부동산 실거래가 Daily Dashboard</title>
<style>{_CSS}
.period-toggle {{ display: flex; gap: 6px; flex-wrap: wrap; margin: 10px 0 16px; }}
.period-toggle button {{ font-family: inherit; font-size: 0.82rem; font-weight: 600; padding: 6px 14px;
  border-radius: 999px; border: 1px solid var(--border); background: var(--surface); color: var(--text);
  cursor: pointer; }}
.period-toggle button.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
.daily-chart-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }}
.daily-chart-card {{ background: var(--surface-2); border: 1px solid var(--border); border-radius: 10px; padding: 10px 12px; }}
.daily-chart-label {{ font-size: 0.82rem; font-weight: 600; color: var(--text-muted); margin-bottom: 4px; }}
.daily-chart-source {{ font-size: 0.72rem; color: var(--text-muted); opacity: 0.75; margin-top: 4px; }}
</style>
</head>
<body>
<div class="page">
  <header class="masthead">
    <h1>부동산 실거래가 Daily Dashboard</h1>
    <div class="sub">매일 03:00 KST 자동 갱신(real-estate-sync.yml) · 최신 반영월: {_esc(latest_month)} ·
      <a href="peos-daily.html">PEOS Daily Dashboard</a> · <a href="index.html">거시경제 투자 시계</a></div>
  </header>

  <section class="card">
    <p class="tile-sub">국토교통부 실거래가 공개시스템(MOLIT) 데이터는 <b>월별 신고 집계</b>라 매일 새
    포인트가 찍히지는 않습니다 — 매일 재수집을 시도해 그 달 신고분이 갱신되면 그 달 포인트 값이
    바뀌고, 새 달이 되면 포인트가 하나 늘어납니다. 이 페이지는 <b>매일 갱신</b>되어 쌓인 데이터를
    그때그때 보여줍니다(포인트 밀도를 지어내지 않습니다). 아파트/연립다세대(빌라)/오피스텔
    매매와 아파트 전세·월세를 서울/수도권/전국(대표표본) + 청약 타겟 인근({_esc(_HIGHLIGHT_NAME)})
    기준으로 나눠 보여줍니다.</p>
    <div class="period-toggle">{period_buttons}</div>
  </section>
{empty_notice}
{''.join(group_sections)}

  <footer>부동산 실거래가 Daily Dashboard — 자동 생성, 투자 자문 아님. 청약 리포트(subscription-report-*.md)와
  같은 원천 데이터(engine/real_estate/*)를 사용합니다.</footer>
</div>
<script>{js}</script>
</body>
</html>"""


def write_real_estate_dashboard(out_path: Path | None = None) -> Path:
    out_path = out_path or (REPO_ROOT / "docs" / "real-estate-daily.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_real_estate_dashboard(), encoding="utf-8")
    return out_path


def main() -> None:
    path = write_real_estate_dashboard()
    print(f"Real estate dashboard: {path}")


if __name__ == "__main__":
    main()
