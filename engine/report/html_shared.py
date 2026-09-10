"""리포트·대시보드가 공유하는 HTML 조각.

## 왜 이 모듈이 생겼나 (2026-09-10)

`_CSS`와 `_esc`는 원래 `engine/report/html.py` 안에 있었고, PEOS Daily
Dashboard와 부동산 대시보드가 거기서 가져다 썼다. 그런데 그 파일의 본체인
`render_html`은 **실제 리포트 생성에 쓰이지 않는다** — `run.py`가 쓰는 건
`html_new.py`다. 즉 살아 있는 두 대시보드가 **쓰이지 않는 렌더러에
의존**하는 모양이었고, 그 탓에 "html.py를 지워도 되나?"를 판단할 수 없었다.

공용으로 쓰이는 것만 여기로 옮겨 그 얽힘을 끊는다. 새 스타일을 추가할 때는
이 파일이 **세 곳(월간 리포트 HTML·데일리 대시보드·부동산 대시보드)에
동시에 적용된다**는 걸 염두에 둘 것.
"""
from __future__ import annotations

import html as _html_lib


def _esc(value) -> str:
    """HTML 이스케이프. None은 "Pending"으로 — 리포트에서 미수집을
    빈칸으로 두면 "값이 0"인지 "아직 없음"인지 구분이 안 된다(R3)."""
    if value is None:
        return "Pending"
    return _html_lib.escape(str(value))


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
.spark-cell { white-space: normal; }
.spark { display: block; }
.spark-labels { display: flex; justify-content: space-between; font-size: 0.68rem; color: var(--text-muted);
  width: 176px; }
.spark-empty { font-size: 0.78rem; }
.stale-mark { color: var(--warn); cursor: help; }
.clock-row { display: flex; gap: 18px; align-items: center; flex-wrap: wrap; }
.clock-img { width: 180px; height: 180px; border-radius: 10px; flex-shrink: 0;
  background: #ffffff; padding: 6px; border: 1px solid var(--border); }
.chart-img { width: 100%; height: auto; border-radius: 10px;
  background: #ffffff; padding: 6px; border: 1px solid var(--border); }
.discuss-card { background: var(--surface-2); border-left: 3px solid var(--accent); border-radius: 8px;
  padding: 12px 16px; margin: 10px 0; }
.discuss-topic { font-weight: 700; margin-bottom: 4px; }
.discuss-context { color: var(--text-muted); font-size: 0.88rem; margin: 4px 0; }
.discuss-question { margin: 6px 0 0; font-size: 0.94rem; }
.discuss-input { width: 100%; margin-top: 10px; padding: 8px 10px; border-radius: 8px;
  border: 1px solid var(--border); background: var(--surface); color: var(--text);
  font-family: inherit; font-size: 0.88rem; resize: vertical; box-sizing: border-box; }
.discuss-input:focus { outline: 2px solid var(--accent); outline-offset: 1px; }
.discuss-actions { display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap; }
.discuss-toolbar { display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  padding: 10px 14px; background: var(--surface-2); border-radius: 10px; margin-bottom: 10px; }
.btn-fb { font-family: inherit; font-size: 0.82rem; font-weight: 600; padding: 6px 12px;
  border-radius: 8px; border: 1px solid var(--border); background: var(--surface);
  color: var(--text); cursor: pointer; }
.btn-fb:hover { border-color: var(--accent); }
.btn-fb:disabled { opacity: 0.7; cursor: default; }
.btn-fb-primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.copy-output { margin-top: 10px; padding: 12px 14px; background: var(--surface-2);
  border: 2px dashed var(--accent); border-radius: 10px; }
.copy-output textarea { width: 100%; box-sizing: border-box; padding: 8px 10px; border-radius: 8px;
  border: 1px solid var(--border); background: var(--surface); color: var(--text);
  font-family: inherit; font-size: 0.82rem; resize: vertical; margin-top: 6px; }
.copy-output a#peos-copy-output-link { display: none; margin-top: 8px; color: var(--accent);
  font-size: 0.88rem; font-weight: 600; }
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
