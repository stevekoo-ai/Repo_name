"""PDF/Excel export extension points (Master Instruction 18.1: "PDF/Excel export 준비").

Not implemented in this MVP (24.3 only requires Markdown output) — kept
here as the documented seam so a future session can add a renderer without
touching payload.py or markdown.py. Both take the same structured payload
that render_markdown() consumes.
"""
from __future__ import annotations

from pathlib import Path


def export_json(payload: dict, out_path: Path) -> Path:
    """The one format guaranteed to round-trip: dump the structured payload as-is."""
    import json
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, default=str, indent=2), encoding="utf-8")
    return out_path


def export_pdf(payload: dict, out_path: Path) -> Path:
    raise NotImplementedError(
        "PDF export is a prepared extension point, not yet implemented. "
        "Suggested approach: render_markdown(payload) -> a Markdown-to-PDF tool "
        "(e.g. weasyprint over an HTML template, or pandoc) — payload.py/markdown.py "
        "need no changes to support it."
    )


def export_excel(payload: dict, out_path: Path) -> Path:
    raise NotImplementedError(
        "Excel export is a prepared extension point, not yet implemented. "
        "Suggested approach: openpyxl workbook with one sheet per payload section "
        "(macro_dashboard, assets, actions, calendar) — payload.py needs no changes."
    )
