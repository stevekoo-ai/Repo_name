#!/usr/bin/env python3
"""모든 생성된 daily 리포트(.md/.html)를 한 링크 페이지에서 찾아볼 수 있게
docs/reports-index.html을 다시 만든다.

2026-08-27 사용자 요청 — "모든 생성된 html이나 md file형태의 보고서에 대해서,
여기에서 링크를 통해 확인할 수 있도록 해줘". report/*.md는 GitHub이 자체적으로
렌더링해주니 blob URL만 있으면 되지만, report/*.html은 GitHub blob 뷰가
소스코드로만 보여줘서 그대로는 못 읽는다 — 그래서 .html은 docs/archive/로
복사해 GitHub Pages가 렌더링해서 서빙하게 한다(기존에 docs/report.html에
"최신 월간"만 복사하던 관례를 "전체 일별 이력"으로 확장).

멱등(idempotent) — 이미 최신인 파일은 다시 복사하지 않고, 매번 전체 diff
없이 그대로 실행해도 안전. 사용법:
    python3 scripts/build_reports_index.py
"""
from __future__ import annotations

import filecmp
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = REPO_ROOT / "report"
SOURCES_DIR = REPO_ROOT / "sources"
DOCS_DIR = REPO_ROOT / "docs"
ARCHIVE_DIR = DOCS_DIR / "archive"
INDEX_PATH = DOCS_DIR / "reports-index.html"

DATED_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.(md|html)$")
MONTHLY_RE = re.compile(r"^(\d{4}-\d{2})\.(md|html)$")
SK_HYNIX_RE = re.compile(r"^sk-hynix-auto-report-(\d{4}-\d{2}-\d{2})-(\d{4})\.md$")


def _repo_slug() -> str:
    return os.environ.get("GITHUB_REPOSITORY", "stevekoo-ai/Repo_name")


def _blob_url(repo_relative_path: str) -> str:
    return f"https://github.com/{_repo_slug()}/blob/main/{repo_relative_path}"


def _pages_base_url() -> str:
    owner, _, name = _repo_slug().partition("/")
    return f"https://{owner}.github.io/{name}"


def _archive_html(src: Path) -> str:
    """report/*.html을 docs/archive/에 복사(내용이 다를 때만 실제로 씀 —
    커밋마다 불필요한 diff를 만들지 않기 위해)하고, 그 파일의 Pages URL을
    반환."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    dest = ARCHIVE_DIR / src.name
    if not dest.exists() or not filecmp.cmp(src, dest, shallow=False):
        shutil.copy2(src, dest)
    return f"{_pages_base_url()}/archive/{src.name}"


def _collect_peos_reports() -> list[dict]:
    """report/ 아래 YYYY-MM-DD.{md,html} 쌍(과 YYYY-MM 월간 파일)을 날짜별로
    묶는다. 같은 날짜에 md/html이 둘 다 있으면 한 행으로, 하나만 있으면
    있는 것만 링크한다."""
    if not REPORT_DIR.exists():
        return []
    by_date: dict[str, dict] = {}
    for path in REPORT_DIR.iterdir():
        m = DATED_RE.match(path.name)
        if not m:
            continue
        date_str, ext = m.groups()
        by_date.setdefault(date_str, {"date": date_str, "md": None, "html": None})
        if ext == "md":
            by_date[date_str]["md"] = _blob_url(f"report/{path.name}")
        else:
            by_date[date_str]["html"] = _archive_html(path)
    return sorted(by_date.values(), key=lambda r: r["date"], reverse=True)


def _collect_monthly_reports() -> list[dict]:
    if not REPORT_DIR.exists():
        return []
    by_month: dict[str, dict] = {}
    for path in REPORT_DIR.iterdir():
        m = MONTHLY_RE.match(path.name)
        if not m:
            continue
        month_str, ext = m.groups()
        by_month.setdefault(month_str, {"month": month_str, "md": None, "html": None})
        if ext == "md":
            by_month[month_str]["md"] = _blob_url(f"report/{path.name}")
        else:
            # 월간 html은 이미 docs/report.html(최신월 전용)로 매일 동기화되지만,
            # 과거 월도 archive에 남겨 링크가 계속 살아있게 한다.
            by_month[month_str]["html"] = _archive_html(path)
    return sorted(by_month.values(), key=lambda r: r["month"], reverse=True)


def _collect_sk_hynix_reports() -> list[dict]:
    if not SOURCES_DIR.exists():
        return []
    out = []
    for path in SOURCES_DIR.glob("sk-hynix-auto-report-*.md"):
        m = SK_HYNIX_RE.match(path.name)
        if not m:
            continue
        date_str, time_str = m.groups()
        out.append({
            "date": date_str, "time": time_str,
            "md": _blob_url(f"sources/{path.name}"),
        })
    return sorted(out, key=lambda r: (r["date"], r["time"]), reverse=True)


def _collect_misc_html_reports() -> list[dict]:
    """report/ 안의 그 외 일회성 HTML 산출물(daily-brief-*, subscription-desktop-*,
    peos-audit/full/morning-*, PEOS-Final-Report-* 등) — 정기 파이프라인 파일명
    패턴(DATED_RE/MONTHLY_RE)에 안 걸리는 것들을 전부 모아 링크만 제공한다."""
    if not REPORT_DIR.exists():
        return []
    out = []
    for path in sorted(REPORT_DIR.glob("*.html"), reverse=True):
        if DATED_RE.match(path.name) or MONTHLY_RE.match(path.name):
            continue
        out.append({"name": path.name, "html": _archive_html(path)})
    return out


def _row_peos(r: dict) -> str:
    links = []
    if r.get("md"):
        links.append(f'<a href="{r["md"]}">MD</a>')
    if r.get("html"):
        links.append(f'<a href="{r["html"]}">HTML</a>')
    return f'<tr><td>{r.get("date") or r.get("month")}</td><td>{" · ".join(links)}</td></tr>'


def _row_sk_hynix(r: dict) -> str:
    hhmm = f"{r['time'][:2]}:{r['time'][2:]}"
    return f'<tr><td>{r["date"]} {hhmm}</td><td><a href="{r["md"]}">MD</a></td></tr>'


def _row_misc(r: dict) -> str:
    return f'<tr><td>{r["name"]}</td><td><a href="{r["html"]}">HTML</a></td></tr>'


def build_index() -> Path:
    daily = _collect_peos_reports()
    monthly = _collect_monthly_reports()
    sk_hynix = _collect_sk_hynix_reports()
    misc = _collect_misc_html_reports()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>Steve's Wiki — 생성된 리포트 전체 목록</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: -apple-system, "Segoe UI", sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; background:#fafafa; }}
  h1 {{ font-size: 1.4rem; }}
  h2 {{ font-size: 1.1rem; margin-top: 2.2rem; border-bottom: 2px solid #ddd; padding-bottom: 0.3rem; }}
  .updated {{ color: #666; font-size: 0.85rem; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 0.9rem; margin-top: 0.8rem; }}
  th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: left; }}
  th {{ background: #f0f0f0; }}
  tr:nth-child(even) {{ background: #f8f8f8; }}
  a {{ color: #a85a29; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .note {{ color: #888; font-size: 0.85rem; }}
</style>
</head>
<body>
<h1>생성된 리포트 전체 목록</h1>
<p class="updated">마지막 갱신: {now} · 이 페이지 자체도 리포트가 새로 생성될 때마다 자동 갱신됩니다
(scripts/build_reports_index.py, daily-peos-report.yml/sk-hynix-daily-report.yml에서 호출).</p>
<p><a href="report.html">최신 월간 PEOS 리포트(HTML)</a> · <a href="peos-daily.html">PEOS Daily Dashboard</a> · <a href="index.html">거시경제 투자 시계</a></p>

<h2>PEOS 일일 리포트 ({len(daily)}건)</h2>
<table><tr><th>날짜</th><th>링크</th></tr>
{"".join(_row_peos(r) for r in daily) or '<tr><td colspan="2">없음</td></tr>'}
</table>

<h2>PEOS 월간 리포트 ({len(monthly)}건)</h2>
<table><tr><th>월</th><th>링크</th></tr>
{"".join(_row_peos(r) for r in monthly) or '<tr><td colspan="2">없음</td></tr>'}
</table>

<h2>SK하이닉스 자동 리포트 ({len(sk_hynix)}건, 07:00/10:00/19:00 KST)</h2>
<table><tr><th>일시</th><th>링크</th></tr>
{"".join(_row_sk_hynix(r) for r in sk_hynix) or '<tr><td colspan="2">없음</td></tr>'}
</table>

<h2>기타 리포트 ({len(misc)}건)</h2>
<p class="note">정기 파이프라인 파일명 패턴이 아닌 일회성 산출물(초기 실험·수동 발행분 등).</p>
<table><tr><th>파일명</th><th>링크</th></tr>
{"".join(_row_misc(r) for r in misc) or '<tr><td colspan="2">없음</td></tr>'}
</table>
</body>
</html>
"""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(html, encoding="utf-8")
    return INDEX_PATH


if __name__ == "__main__":
    path = build_index()
    print(f"wrote {path}")
