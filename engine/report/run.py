"""PEOS pipeline entrypoint: Collect -> Validate -> Score -> Personal Map -> Action -> Report.

    python -m engine.report.run [--month YYYY-MM]

Writes report/<month>.md and report/<month>.json. This is the "매월 지표
충족률 검사 -> Macro Engine -> Domain Engines -> Report 생성" flow from
18.3, wired for on-demand or scheduled (GitHub Actions / cron) execution.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from core.config import report_config
from core.logger import log_event
from . import exporters, payload as payload_mod
from .markdown import render_markdown

REPO_ROOT = Path(__file__).resolve().parents[2]


def run(month_key: str | None = None) -> dict[str, Path]:
    payload = payload_mod.build_report_payload(month_key=month_key)
    out_dir = REPO_ROOT / report_config().get("output_dir", "report")

    md_path = out_dir / f"{payload['report_month']}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_markdown(payload), encoding="utf-8")

    json_path = exporters.export_json(payload, out_dir / f"{payload['report_month']}.json")

    log_event("pipeline.report_generated", month=payload["report_month"],
              readiness=payload["report_readiness"], markdown=str(md_path), json=str(json_path))
    return {"markdown": md_path, "json": json_path}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the monthly PEOS report.")
    parser.add_argument("--month", default=None, help="YYYY-MM, defaults to the current month")
    args = parser.parse_args()
    paths = run(month_key=args.month)
    print(f"Markdown: {paths['markdown']}")
    print(f"JSON:     {paths['json']}")


if __name__ == "__main__":
    main()
