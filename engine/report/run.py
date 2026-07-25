"""PEOS pipeline entrypoint: Collect -> Validate -> Score -> Personal Map -> Action -> Report.

    python -m engine.report.run [--month YYYY-MM] [--no-archive]

Writes report/<month>.html (primary, read this one — always reflects the
latest run for that month), report/<month>.md, and report/<month>.json.

Also archives the same content under report/<YYYY-MM-DD>.{html,md,json} —
one snapshot per calendar day the pipeline actually ran, independent of
which month it reported on. This is what makes the full report (CCI, rate
analysis, real estate, Action Plan, ...) a daily-reportable artifact and
not just the <month> file that gets silently overwritten every run: past
days stay retrievable under their own filename instead of only the latest
run surviving. daily-peos-report.yml already runs this once a day, so in
practice one dated file lands per day it succeeds.

This is the "매월 지표 충족률 검사 -> Macro Engine -> Domain Engines -> Report
생성" flow from 18.3, wired for on-demand or scheduled (GitHub Actions /
cron) execution.
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from core.config import report_config
from core.logger import log_event
from . import daily_history, exporters, payload as payload_mod
from .html_new import render_html
from .markdown import render_markdown

REPO_ROOT = Path(__file__).resolve().parents[2]


def run(month_key: str | None = None, archive: bool = True, archive_date: str | None = None) -> dict[str, Path]:
    payload = payload_mod.build_report_payload(month_key=month_key)
    out_dir = REPO_ROOT / report_config().get("output_dir", "report")
    out_dir.mkdir(parents=True, exist_ok=True)

    html_content = render_html(payload)
    md_content = render_markdown(payload)

    html_path = out_dir / f"{payload['report_month']}.html"
    html_path.write_text(html_content, encoding="utf-8")

    md_path = out_dir / f"{payload['report_month']}.md"
    md_path.write_text(md_content, encoding="utf-8")

    json_path = exporters.export_json(payload, out_dir / f"{payload['report_month']}.json")

    result = {"html": html_path, "markdown": md_path, "json": json_path}

    if archive:
        archive_date = archive_date or date.today().isoformat()
        daily_html_path = out_dir / f"{archive_date}.html"
        daily_html_path.write_text(html_content, encoding="utf-8")
        daily_md_path = out_dir / f"{archive_date}.md"
        daily_md_path.write_text(md_content, encoding="utf-8")
        daily_json_path = exporters.export_json(payload, out_dir / f"{archive_date}.json")
        result.update({
            "daily_html": daily_html_path, "daily_markdown": daily_md_path, "daily_json": daily_json_path,
        })

    result["daily_history"] = daily_history.append_daily_history(payload)

    log_event("pipeline.report_generated", month=payload["report_month"],
              readiness=payload["report_readiness"], html=str(html_path),
              markdown=str(md_path), json=str(json_path),
              archived_as=archive_date if archive else None)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the monthly PEOS report.")
    parser.add_argument("--month", default=None, help="YYYY-MM, defaults to the current month")
    parser.add_argument("--no-archive", action="store_true",
                         help="skip writing the dated report/<YYYY-MM-DD>.* daily archive copy")
    args = parser.parse_args()
    paths = run(month_key=args.month, archive=not args.no_archive)
    print(f"HTML:     {paths['html']}")
    print(f"Markdown: {paths['markdown']}")
    print(f"JSON:     {paths['json']}")
    if "daily_html" in paths:
        print(f"Archived: {paths['daily_html']}")


if __name__ == "__main__":
    main()
