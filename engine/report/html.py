"""HTML report renderer — the primary output format the user reads.

Same payload as markdown.py (engine/report/payload.py is the single
source of truth for content); this module only handles presentation.
Self-contained single-file HTML: inline CSS, no external requests, works
opened directly from disk. Light/dark aware via prefers-color-scheme.
"""
from __future__ import annotations

import base64
import html as html_lib
from pathlib import Path

from core.models import DataStatus

REPO_ROOT = Path(__file__).resolve().parents[2]
CLOCK_IMAGE_PATH = REPO_ROOT / "docs" / "clock.png"

STATUS_KR = {
    DataStatus.OK.value: "OK", DataStatus.PENDING.value: "Pending",
    DataStatus.NOT_RELEASED.value: "Not Released", DataStatus.SOURCE_ERROR.value: "Source Error",
}

BAND_TO_BADGE = {
    "strong_expansion": "good", "expansion": "good",
    "unbalanced_expansion": "neutral", "early_slowdown": "neutral",
    "slowdown": "bad", "recession_warning": "bad",
}

TIER_BADGE = {5: "bad", 4: "warn", 3: "neutral", 2: "neutral", 1: "neutral"}
TIER_LABEL = {5: "★★★★★ 반드시 확인/실행", 4: "★★★★☆ 검토", 3: "★★★☆☆ 관찰", 2: "★★☆☆☆ 참고", 1: "보류"}


def _esc(value) -> str:
    if value is None:
        return "Pending"
    return html_lib.escape(str(value))


def _fmt(value, suffix: str = "") -> str:
    if value is None:
        return '<span class="pending">Pending</span>'
    if isinstance(value, float):
        return f"{value:.2f}{suffix}"
    return f"{value}{suffix}"


def _score_badge_class(score_0_100: float | None) -> str:
    if score_0_100 is None:
        return "neutral"
    if score_0_100 >= 70:
        return "good"
    if score_0_100 >= 40:
        return "neutral"
    return "bad"


def _stat_tile(label: str, value: str, sub: str = "", badge: str | None = None) -> str:
    badge_html = f'<span class="dot dot-{badge}"></span>' if badge else ""
    return f"""
    <div class="tile">
      <div class="tile-label">{badge_html}{_esc(label)}</div>
      <div class="tile-value">{value}</div>
      {f'<div class="tile-sub">{_esc(sub)}</div>' if sub else ""}
    </div>"""


def _clock_image_data_uri() -> str | None:
    if not CLOCK_IMAGE_PATH.exists():
        return None
    data = base64.b64encode(CLOCK_IMAGE_PATH.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"


def _section_stat_tiles(payload: dict) -> str:
    macro = payload["macro"]
    p = payload["personal"]
    tiles = [
        _stat_tile("경기 국면", _esc(macro["regime"]), macro["score_band_label"],
                   BAND_TO_BADGE.get(macro["score_band"], "neutral")),
        _stat_tile("Confidence", f"{macro['confidence']}점", "판정 신뢰도",
                   _score_badge_class(macro["confidence"])),
        _stat_tile("Investment Environment", _fmt(p["investment_environment_score"], "점"), "투자 환경",
                   _score_badge_class(p["investment_environment_score"])),
        _stat_tile("반도체", _fmt(p["semiconductor_score"], "점"), p.get("semiconductor_band") or "",
                   _score_badge_class(p["semiconductor_score"])),
        _stat_tile("채권", _fmt(p["bond_score"], "점"), "Bond Score", _score_badge_class(p["bond_score"])),
        _stat_tile("환율", _fmt(p["fx_score"], "점"), "FX Score", _score_badge_class(p["fx_score"])),
        _stat_tile("청약 준비도", _fmt(p["housing_readiness_score"], "점"), "Housing Readiness",
                   _score_badge_class(p["housing_readiness_score"])),
    ]
    return f'<div class="tile-grid">{"".join(tiles)}</div>'


def _section_executive_summary(payload: dict) -> str:
    macro = payload["macro"]
    brief = payload["personal_executive_brief"]
    top_action = payload["actions"][0] if payload["actions"] else None
    changes = "; ".join(c["message"] for c in macro["changes"][:3]) if macro["changes"] else "데이터 부족"
    return f"""
    <section class="card">
      <h2>Executive Summary</h2>
      <ul class="kv-list">
        <li><b>현재 경기 국면</b> {_esc(macro['regime'])} ({_esc(macro['score_band_label'])}, 총점 {macro['score']})</li>
        <li><b>지난달 대비 변화</b> {_esc(macro['previous_regime'])} → {_esc(macro['regime'])}
            {f"({_esc(macro['transition'])})" if macro['transition'] else "(변동 없음)"}</li>
        <li><b>핵심 원인</b> {_esc(changes)}</li>
        <li><b>사용자에게 중요한 의미</b> {_esc(brief['one_line_diagnosis'])}</li>
        <li><b>이번 달 핵심 행동</b> {"[행동] " + _esc(top_action['title']) if top_action else "핵심 지표 확보 후 재평가 필요"}</li>
        <li><b>리포트 충족도</b> <span class="badge badge-{'good' if payload['report_readiness']=='final' else 'neutral' if payload['report_readiness']=='draft' else 'warn'}">{_esc(payload['report_readiness'])}</span></li>
      </ul>
    </section>"""


def _section_investment_clock(payload: dict) -> str:
    clock = payload["macro"].get("us_investment_clock")
    img_uri = _clock_image_data_uri()
    img_html = f'<img class="clock-img" src="{img_uri}" alt="Investment Clock">' if img_uri else ""
    if not clock:
        body = '<p class="pending">데이터 없음 (Pending) — FRED 접속 불가 및 이력 데이터 없음.</p>'
    else:
        staleness = "실시간" if clock.get("source") == "live" else "최근 저장값 (실시간 조회 불가)"
        body = f"""
        <ul class="kv-list">
          <li><b>국면</b> {_esc(clock['phase_kr'])} ({_esc(clock['phase'])})</li>
          <li><b>유리 자산군</b> {_esc(clock['favored_asset_kr'])} ({_esc(clock['favored_asset'])})</li>
          <li><b>성장/물가 모멘텀</b> {_esc(clock['growth_signal'])} / {_esc(clock['inflation_signal'])}</li>
          <li><b>기준일</b> {_esc(clock['as_of'])} · {staleness}</li>
        </ul>
        {f'<p class="tile-sub">{_esc(clock["note"])}</p>' if clock.get("note") else ""}"""
    return f"""
    <section class="card">
      <h2>미국 거시경제 참고 — Investment Clock</h2>
      <p class="tile-sub">기존에 구축한 Macro Investment Clock 프로젝트(미국 성장×물가 4국면 모델)를
      PEOS의 미국/글로벌 참고 신호로 그대로 재사용합니다. 매일 자동 갱신되는 원본 대시보드는
      GitHub Pages가 활성화되어 있다면 별도로 계속 확인할 수 있습니다.</p>
      <div class="clock-row">{img_html}<div>{body}</div></div>
    </section>"""


def _section_macro_dashboard(payload: dict) -> str:
    rows = "".join(
        f"""<tr>
          <td>{_esc(r['indicator'])}</td><td>{_fmt(r['current'])}</td><td>{_fmt(r['previous'])}</td>
          <td>{_esc(r['trend'])}</td><td>{_fmt(r['score'])}</td>
          <td class="muted">{_esc(r['source'] or STATUS_KR.get(r['status'], r['status']))}</td>
        </tr>""" for r in payload["macro_dashboard"]
    )
    return f"""
    <section class="card">
      <h2>Macro Dashboard</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>지표</th><th>현재</th><th>이전</th><th>추세</th><th>점수</th><th>출처</th></tr></thead>
        <tbody>{rows}</tbody>
      </table></div>
    </section>"""


def _section_discussion(payload: dict) -> str:
    points = payload.get("discussion_points", [])
    if not points:
        cards = '<p class="tile-sub">이번 달은 별도로 논의가 필요한 항목이 없습니다.</p>'
    else:
        cards = "".join(f"""
        <div class="discuss-card">
          <div class="discuss-topic">💬 {_esc(p['topic'])}</div>
          <p class="discuss-context">{_esc(p['context'])}</p>
          <p class="discuss-question">{_esc(p['question'])}</p>
        </div>""" for p in points)
    return f"""
    <section class="card">
      <h2>논의가 필요한 결정 사항</h2>
      <p class="tile-sub">숫자로 정리되지 않는, 사용자님의 판단이 필요한 지점들입니다. 다음 대화에서
      답을 주시면 다음 리포트부터 반영합니다.</p>
      {cards}
    </section>"""


def _section_action_plan(payload: dict) -> str:
    by_tier: dict[int, list] = {t: [] for t in (5, 4, 3, 2, 1)}
    for a in payload["actions"]:
        by_tier.setdefault(a["priority"], []).append(a)

    groups = []
    for tier in (5, 4, 3, 2, 1):
        items = by_tier.get(tier, [])
        if not items:
            continue
        cards = "".join(f"""
        <div class="action-card action-{TIER_BADGE[tier]}">
          <div class="action-title">{_esc(a['title'])}</div>
          <div class="action-row"><span class="k">이유</span>{_esc(a['reason'])}</div>
          <div class="action-row"><span class="k">보류 조건</span>{_esc(a['invalid_condition'])}</div>
          <div class="action-row"><span class="k">재점검</span>{_esc(a['recheck'])}</div>
          {f'<div class="action-row action-conflict"><span class="k">조정</span>{_esc(a["conflict_note"])}</div>' if a.get("conflict_note") else ""}
        </div>""" for a in items)
        groups.append(f'<h3><span class="badge badge-{TIER_BADGE[tier]}">{_esc(TIER_LABEL[tier])}</span></h3>{cards}')

    return f"""
    <section class="card">
      <h2>이번 달 Action Plan</h2>
      {"".join(groups) if groups else '<p class="tile-sub">생성된 액션이 없습니다.</p>'}
    </section>"""


def _section_calendar(payload: dict) -> str:
    events = payload["calendar"]
    if not events:
        rows = '<tr><td colspan="4" class="muted">확정된 일정 없음 (data/manual_inputs/calendar.yaml 갱신 필요)</td></tr>'
    else:
        rows = "".join(
            f"""<tr><td>{_esc(e['date'])}</td><td>{_esc(e['name'])}</td>
            <td>{_esc(e['importance_label'])}</td><td>{e['priority_score']}점</td></tr>"""
            for e in events
        )
    return f"""
    <section class="card">
      <h2>경제 캘린더</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>날짜</th><th>이벤트</th><th>중요도</th><th>영향도</th></tr></thead>
        <tbody>{rows}</tbody>
      </table></div>
    </section>"""


def _section_asset_impact(payload: dict) -> str:
    labels = {"stocks": "주식", "etf": "ETF", "bond": "채권", "cash": "현금",
              "subscription_fund": "청약 자금", "fx_exposure": "환율"}
    tiles = []
    for key, label in labels.items():
        a = payload["assets"].get(key, {})
        if a.get("score") is None:
            tiles.append(_stat_tile(label, "Pending", "데이터 부족", "neutral"))
        else:
            tiles.append(_stat_tile(label, _esc(a["stars"]), f"{a['score']}점", _score_badge_class(a["score"])))
    return f'<section class="card"><h2>자산별 영향 분석</h2><div class="tile-grid">{"".join(tiles)}</div></section>'


def _section_scenarios(payload: dict) -> str:
    s = payload["scenarios"]
    cards = "".join(f"""
      <div class="scenario-card scenario-{name}">
        <div class="scenario-title">{label} <span class="scenario-prob">{s[name]['probability']}%</span></div>
        <p><b>전제</b> {_esc(s[name]['premise'])}</p>
        <p><b>기대되는 변화</b> {_esc(s[name]['expected_change'])}</p>
        <p><b>사용자 영향</b> {_esc(s[name]['user_impact'])}</p>
      </div>""" for name, label in (("base", "Base"), ("bull", "Bull"), ("bear", "Bear")))
    conditions = "".join(f"<li>{_esc(c)}</li>" for c in s["invalid_conditions"])
    return f"""
    <section class="card">
      <h2>시나리오 분석</h2>
      <div class="scenario-grid">{cards}</div>
      <h3>깨지는 조건</h3>
      <ul>{conditions}</ul>
    </section>"""


def _section_personal_analysis(payload: dict) -> str:
    p = payload["personal"]
    bias_labels = {"stock_bias": "주식", "etf_bias": "ETF", "bond_bias": "채권", "cash_bias": "현금"}
    bias_text = ""
    if p["investment_biases"]:
        bias_text = " · 편향: " + ", ".join(f"{bias_labels.get(k, k)} {v}" for k, v in p["investment_biases"].items())
    return f"""
    <section class="card">
      <h2>사용자 맞춤 분석</h2>
      <ul class="kv-list">
        <li><b>직업 관점</b> 반도체/AI 인프라 종사자 — 반도체 점수 {_fmt(p['semiconductor_score'], '점')}
            ({_esc(p.get('semiconductor_band'))})은 업황·성과급 사이클에 직접 연결됩니다.</li>
        <li><b>투자 관점</b> Investment Environment {_fmt(p['investment_environment_score'], '점')}{_esc(bias_text)}</li>
        <li><b>채권 관점</b> Bond Score {_fmt(p['bond_score'], '점')}</li>
        <li><b>환율 관점</b> FX Score {_fmt(p['fx_score'], '점')}</li>
        <li><b>공공분양 관점</b> Housing Readiness {_fmt(p['housing_readiness_score'], '점')}</li>
      </ul>
    </section>"""


def _section_brief(payload: dict) -> str:
    b = payload["personal_executive_brief"]
    summary = ", ".join(f"{k}={v}" for k, v in b["asset_summary"].items() if v)
    events = "; ".join(b["top_events"]) if b["top_events"] else "없음"
    return f"""
    <section class="card highlight">
      <h2>Personal Executive Brief</h2>
      <ul class="kv-list">
        <li><b>이번 달 한 줄 진단</b> {_esc(b['one_line_diagnosis'])}</li>
        <li><b>자산별 영향 요약</b> {_esc(summary)}</li>
        <li><b>중요한 이벤트 TOP 5</b> {_esc(events)}</li>
        <li><b>최종 제안</b> [행동] {_esc(b['final_suggestion'])}</li>
      </ul>
    </section>"""


def _section_appendix(payload: dict) -> str:
    a = payload["appendix"]
    sources = ", ".join(a["sources"]) if a["sources"] else "N/A"
    glossary = "".join(f"<li><b>{_esc(k)}</b> {_esc(v)}</li>" for k, v in a["glossary"].items())
    return f"""
    <section class="card">
      <h2>Appendix</h2>
      <ul class="kv-list">
        <li><b>데이터 출처</b> {_esc(sources)}</li>
        <li><b>지난달 Regime</b> {_esc(a['previous_month_regime'] or 'N/A')}</li>
      </ul>
      <h3>용어 설명</h3>
      <ul>{glossary}</ul>
    </section>"""


_CSS = """
:root {
  --bg: #f5f6f8; --surface: #ffffff; --surface-2: #f0f1f4; --border: #e2e4e9;
  --text: #16181d; --text-muted: #5c6270; --accent: #2563eb;
  --good: #157a3d; --good-bg: #e5f6ea; --warn: #92510c; --warn-bg: #fdf0dd;
  --bad: #b3261e; --bad-bg: #fbe6e4; --neutral: #40465a; --neutral-bg: #eceef2;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #14161b; --surface: #1c1f26; --surface-2: #23262f; --border: #333846;
    --text: #eceef2; --text-muted: #a0a6b5; --accent: #7fa8ff;
    --good: #6cd48f; --good-bg: #113222; --warn: #f0b862; --warn-bg: #3a2a10;
    --bad: #f28b82; --bad-bg: #3a1614; --neutral: #b7bccb; --neutral-bg: #262a35;
  }
}
:root[data-theme="dark"] {
  --bg: #14161b; --surface: #1c1f26; --surface-2: #23262f; --border: #333846;
  --text: #eceef2; --text-muted: #a0a6b5; --accent: #7fa8ff;
  --good: #6cd48f; --good-bg: #113222; --warn: #f0b862; --warn-bg: #3a2a10;
  --bad: #f28b82; --bad-bg: #3a1614; --neutral: #b7bccb; --neutral-bg: #262a35;
}
:root[data-theme="light"] {
  --bg: #f5f6f8; --surface: #ffffff; --surface-2: #f0f1f4; --border: #e2e4e9;
  --text: #16181d; --text-muted: #5c6270; --accent: #2563eb;
  --good: #157a3d; --good-bg: #e5f6ea; --warn: #92510c; --warn-bg: #fdf0dd;
  --bad: #b3261e; --bad-bg: #fbe6e4; --neutral: #40465a; --neutral-bg: #eceef2;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font-family: -apple-system, "Segoe UI", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
  line-height: 1.6;
}
.page { max-width: 920px; margin: 0 auto; padding: 24px 16px 64px; }
header.masthead { padding: 8px 0 20px; }
header.masthead h1 { font-size: 1.5rem; margin: 0 0 4px; }
header.masthead .sub { color: var(--text-muted); font-size: 0.9rem; }
.tile-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 12px 0; }
.tile { background: var(--surface-2); border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; }
.tile-label { font-size: 0.78rem; color: var(--text-muted); display: flex; align-items: center; gap: 6px; }
.tile-value { font-size: 1.35rem; font-weight: 700; margin-top: 2px; }
.tile-sub { font-size: 0.78rem; color: var(--text-muted); margin-top: 2px; }
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.dot-good { background: var(--good); } .dot-warn { background: var(--warn); }
.dot-bad { background: var(--bad); } .dot-neutral { background: var(--neutral); }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
  padding: 20px 22px; margin-bottom: 16px; }
.card.highlight { border-color: var(--accent); }
.card h2 { font-size: 1.1rem; margin: 0 0 10px; }
.card h3 { font-size: 0.95rem; margin: 16px 0 8px; color: var(--text-muted); }
.kv-list { list-style: none; padding: 0; margin: 0; }
.kv-list li { padding: 6px 0; border-bottom: 1px dashed var(--border); font-size: 0.92rem; }
.kv-list li:last-child { border-bottom: none; }
.kv-list b { display: inline-block; min-width: 130px; color: var(--text-muted); font-weight: 600; }
.pending { color: var(--text-muted); font-style: italic; }
.muted { color: var(--text-muted); }
.badge { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 0.78rem; font-weight: 600; }
.badge-good { background: var(--good-bg); color: var(--good); }
.badge-warn { background: var(--warn-bg); color: var(--warn); }
.badge-bad { background: var(--bad-bg); color: var(--bad); }
.badge-neutral { background: var(--neutral-bg); color: var(--neutral); }
.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; }
th, td { text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--border); white-space: nowrap; }
th { color: var(--text-muted); font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: .02em; }
.clock-row { display: flex; gap: 18px; align-items: center; flex-wrap: wrap; }
.clock-img { width: 180px; height: 180px; border-radius: 10px; flex-shrink: 0;
  background: #ffffff; padding: 6px; border: 1px solid var(--border); }
.discuss-card { background: var(--surface-2); border-left: 3px solid var(--accent); border-radius: 8px;
  padding: 12px 16px; margin: 10px 0; }
.discuss-topic { font-weight: 700; margin-bottom: 4px; }
.discuss-context { color: var(--text-muted); font-size: 0.88rem; margin: 4px 0; }
.discuss-question { margin: 6px 0 0; font-size: 0.94rem; }
.action-card { border-radius: 10px; border: 1px solid var(--border); padding: 12px 16px; margin: 8px 0 14px; }
.action-good { border-left: 4px solid var(--good); }
.action-warn { border-left: 4px solid var(--warn); }
.action-bad { border-left: 4px solid var(--bad); }
.action-neutral { border-left: 4px solid var(--neutral); }
.action-title { font-weight: 700; margin-bottom: 6px; }
.action-row { font-size: 0.86rem; margin: 3px 0; color: var(--text); }
.action-row .k { display: inline-block; min-width: 68px; color: var(--text-muted); font-weight: 600; }
.action-conflict { color: var(--warn); }
.scenario-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
.scenario-card { background: var(--surface-2); border-radius: 10px; padding: 14px 16px; font-size: 0.85rem; }
.scenario-title { font-weight: 700; font-size: 1rem; margin-bottom: 8px; }
.scenario-prob { color: var(--accent); }
.scenario-card p { margin: 6px 0; }
footer { color: var(--text-muted); font-size: 0.78rem; text-align: center; padding-top: 16px; }
"""


def _section_monthly_changes(payload: dict) -> str:
    items = "".join(f"<li>{_esc(c['message'])}</li>" for c in payload["macro"]["changes"])
    return f'<section class="card"><h2>이번 달 핵심 변화</h2><ul>{items}</ul></section>'


def render_html(payload: dict) -> str:
    body_sections = "".join([
        _section_stat_tiles(payload),
        _section_executive_summary(payload),
        _section_monthly_changes(payload),
        _section_macro_dashboard(payload),
        _section_investment_clock(payload),
        _section_personal_analysis(payload),
        _section_asset_impact(payload),
        _section_scenarios(payload),
        _section_discussion(payload),
        _section_action_plan(payload),
        _section_calendar(payload),
        _section_brief(payload),
        _section_appendix(payload),
    ])

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PEOS 월간 리포트 - {_esc(payload['report_month'])}</title>
<style>{_CSS}</style>
</head>
<body>
<div class="page">
  <header class="masthead">
    <h1>PEOS 월간 리포트 — {_esc(payload['report_month'])}</h1>
    <div class="sub">Personal Economic Operating System · 자동 생성 · 투자 자문 아님</div>
  </header>
  {body_sections}
  <footer>PEOS는 공식 데이터와 사용자 자산/목표를 결합해 행동을 제안하는 개인 경제 의사결정 시스템입니다.
  모든 판단은 참고용이며 최종 결정은 사용자에게 있습니다.</footer>
</div>
</body>
</html>"""
