"""Entrypoint: fetch -> compute full history -> store -> render -> report -> notify.

Run daily (see .github/workflows/daily-clock-report.yml). Each run recomputes
every historical month's reading from FRED's currently published series and
overwrites data/history.csv, so the first run after this pipeline exists
backfills the full available history automatically.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from core import notify

from . import data_sources, report, storage
from .model import build_full_history, read_clock
from .render import draw_clock, draw_trend_charts

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_HISTORY_PATH = REPO_ROOT / "data" / "history.csv"
DEFAULT_DOCS_DIR = REPO_ROOT / "docs"


def run(history_path: Path = DEFAULT_HISTORY_PATH, docs_dir: Path = DEFAULT_DOCS_DIR) -> None:
    run_date = pd.Timestamp.utcnow().tz_localize(None)

    series = data_sources.fetch_all()
    reading = read_clock(series)
    full_history = build_full_history(series)
    history = storage.write_full_history(history_path, full_history, run_date)

    draw_clock(reading, docs_dir / "clock.png")
    draw_trend_charts(history, docs_dir)
    report.render_report(reading, history, run_date, docs_dir / "index.html")

    # 2026-09-24 — 텍스트 4줄 요약 대신 방금 그린 HTML 대시보드를 본문으로,
    # 차트 PNG를 첨부로 보낸다(사용자: "모든 보고서가 html로 발송되는지 확인").
    try:
        pngs = sorted(p for p in docs_dir.glob("*.png"))
        notify.build_channel().send_document(
            subject=f"[Investment Clock] {reading.phase['name']} ({reading.phase['name_kr']}) — favor {reading.phase['asset']}",
            html_body=(docs_dir / "index.html").read_text(encoding="utf-8"),
            attachments=pngs,
        )
    except Exception as exc:
        # The dashboard (docs/index.html, committed afterwards) is still produced, so the
        # run must not die here — but the failure must not be silent either: the
        # workflow's alert step looks for this marker and mails the user.
        print(f"::error::investment clock email failed: {exc}")
        Path("/tmp/clock_notify_failed").write_text(str(exc), encoding="utf-8")

    print(f"Phase: {reading.phase['name']} -> {reading.phase['asset']}")
    print(f"History rows: {len(history)} (from {history['data_asof'].min()} to {history['data_asof'].max()})")
    print(f"Dashboard written to {docs_dir / 'index.html'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the macro investment clock pipeline once.")
    parser.add_argument("--history", default=str(DEFAULT_HISTORY_PATH))
    parser.add_argument("--docs", default=str(DEFAULT_DOCS_DIR))
    args = parser.parse_args()
    run(history_path=Path(args.history), docs_dir=Path(args.docs))


if __name__ == "__main__":
    main()
