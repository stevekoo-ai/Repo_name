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

from . import data_sources, notify, report, storage
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

    channel = notify.build_channel()
    channel.send(
        subject=f"[Investment Clock] {reading.phase['name']} phase — favor {reading.phase['asset']}",
        body_text=(
            f"Data as of {max(reading.growth.as_of, reading.inflation.as_of).date()}\n"
            f"Growth: {reading.growth.label} ({reading.growth.change:+.2f})\n"
            f"Inflation (CPI YoY): {reading.inflation.label} ({reading.inflation.change:+.2f}pp), "
            f"level {reading.inflation.value:.2f}%\n"
            f"Phase: {reading.phase['name']} ({reading.phase['name_kr']}) -> {reading.phase['asset']}"
        ),
    )

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
