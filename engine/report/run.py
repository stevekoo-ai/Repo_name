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

from core import notify
from core.config import report_config
from core.logger import log_event
from . import daily_history, exporters, payload as payload_mod
from .html_new import render_html
from .markdown import render_markdown

REPO_ROOT = Path(__file__).resolve().parents[2]


def _notify_summary(payload: dict) -> None:
    """Push a short summary via the configured notification channel (see core/notify.py).

    Defaults to a no-op — the dashboard/report files are the always-on delivery
    mechanism, this is only active once GMAIL_ADDRESS+GMAIL_APP_PASSWORD, SMTP_*,
    or SLACK_WEBHOOK_URL are set as GitHub Actions secrets.

    Delivery is best-effort: report/<month>.{html,md,json} are already written to
    disk by the time this runs, and the caller (daily-peos-report.yml) still needs
    to commit+push them. A bad SMTP login or a transient network block must not
    take down report generation, so any failure here is logged and swallowed
    rather than propagated.
    """
    macro, macro_us, personal = payload["macro"], payload["macro_us"], payload["personal"]
    subject = (
        f"[PEOS 리포트] {payload['report_month']} — "
        f"한국 {macro['regime']} / 미국 {macro_us['regime']} ({payload['report_readiness']})"
    )
    body = (
        f"한국 Regime: {macro['regime']} (점수 {macro['score']}, 신뢰도 {macro['confidence']:.1f})\n"
        f"미국 Regime: {macro_us['regime']} (점수 {macro_us['score']}, 신뢰도 {macro_us['confidence']:.1f})\n"
        f"투자환경 점수: {personal['investment_environment_score']}\n"
        f"반도체 점수: {personal['semiconductor_score']} ({personal['semiconductor_band']})\n"
        f"액션 아이템: {len(payload['actions'])}건\n\n"
        f"전체 리포트: report/{payload['report_month']}.md (GitHub Pages: docs/report.html)"
    )
    try:
        notify.build_channel().send(subject, body)
    except Exception as exc:
        log_event("notify.send_failed", level="warning", error=str(exc))


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

    _notify_summary(payload)

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
