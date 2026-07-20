"""PEOS pipeline entrypoint: Collect -> Validate -> Score -> Personal Map -> Action -> Report.

    python -m engine.report.run [--daily | --monthly] [--month YYYY-MM]

Daily mode: 일일 시장/투자 업데이트. Writes report/<YYYY-MM-DD>.json (dated
snapshot) + report/daily.html (stable URL, includes the period-selectable
trend section fed by data/peos_daily_history.csv) + appends today's row to
that history CSV.

Monthly mode: 월간 거시경제 심층 분석 (상세, 전략 재점검용). Writes
report/<YYYY-MM>.html/.md/.json — a separate cadence from daily, not folded
into the daily history series.
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from core.config import report_config
from core.logger import log_event
from . import daily_history, exporters, payload as payload_mod
from .html import render_html
from .markdown import render_markdown

REPO_ROOT = Path(__file__).resolve().parents[2]


def run(month_key: str | None = None, report_type: str = "monthly") -> dict[str, Path]:
    """Build and export report.

    Args:
        month_key: YYYY-MM, defaults to current month
        report_type: 'daily' or 'monthly' (affects payload content & naming)
    """
    payload = payload_mod.build_report_payload(month_key=month_key, report_type=report_type)
    out_dir = REPO_ROOT / report_config().get("output_dir", "report")
    out_dir.mkdir(parents=True, exist_ok=True)

    if report_type == "monthly":
        # Monthly key stays YYYY-MM (payload["report_month"]) — one file per month.
        report_key = payload["report_month"]
        json_path = exporters.export_json(payload, out_dir / f"{report_key}.json")

        html_path = out_dir / f"{report_key}.html"
        html_path.write_text(render_html(payload), encoding="utf-8")

        md_path = out_dir / f"{report_key}.md"
        md_path.write_text(render_markdown(payload), encoding="utf-8")

        log_event("pipeline.monthly_report_generated", month=report_key,
                  readiness=payload.get("report_readiness"),
                  html=str(html_path), markdown=str(md_path), json=str(json_path))
        return {"html": html_path, "markdown": md_path, "json": json_path}
    else:  # daily
        # Dated key so same-month daily runs don't collide with each other or
        # with the monthly YYYY-MM file; daily.html is the stable URL the
        # email links to and the user bookmarks.
        report_key = date.today().isoformat()
        json_path = exporters.export_json(payload, out_dir / f"{report_key}.json")

        history_path = daily_history.append_daily_history(payload, run_date=report_key)
        history_json = daily_history.load_history_json(history_path)
        html_path = out_dir / "daily.html"
        html_path.write_text(render_html(payload, history=history_json), encoding="utf-8")

        log_event("pipeline.daily_report_generated", date=report_key,
                  html=str(html_path), json=str(json_path), daily_history=str(history_path))
        return {"html": html_path, "json": json_path, "daily_history": history_path}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate PEOS report (daily or monthly)."
    )
    parser.add_argument(
        "--daily", action="store_true",
        help="일일 업데이트 모드 (일일 시장/투자 정보)"
    )
    parser.add_argument(
        "--monthly", action="store_true",
        help="월간 심층 분석 모드 (거시경제 분석)"
    )
    parser.add_argument(
        "--month", default=None,
        help="YYYY-MM, defaults to the current month"
    )
    args = parser.parse_args()

    report_type = "daily" if args.daily else "monthly"
    paths = run(month_key=args.month, report_type=report_type)

    for key, path in paths.items():
        print(f"{key.upper()}: {path}")


if __name__ == "__main__":
    main()
