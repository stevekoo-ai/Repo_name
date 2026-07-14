"""Month-over-month change detection (Master Instruction 11.12).

Compares this run's Core-10 fields against the previous month's snapshot
using externalized thresholds (config/thresholds.yaml `change_detection`)
so "무엇이 달라졌는가" has a reproducible, non-arbitrary answer.
"""
from __future__ import annotations

from core.config import thresholds_config
from core.models import IndicatorReading


def _prev_field(previous_snapshot: dict | None, indicator: str, field: str):
    if not previous_snapshot:
        return None
    return (
        previous_snapshot.get("macro", {})
        .get("readings", {})
        .get(indicator, {})
        .get("fields", {})
        .get(field)
    )


def detect_changes(readings: dict[str, IndicatorReading], previous_snapshot: dict | None) -> list[dict]:
    if not previous_snapshot:
        return [{"indicator": "all", "message": "이전 스냅샷 없음 — 이번 달이 최초 기록", "direction": "n/a"}]

    t = thresholds_config()["change_detection"]
    changes: list[dict] = []

    exports_yoy = readings.get("exports").detail.get("fields", {}).get("yoy") if "exports" in readings else None
    prev_exports_yoy = _prev_field(previous_snapshot, "exports", "yoy")
    if exports_yoy is not None and prev_exports_yoy is not None:
        delta = exports_yoy - prev_exports_yoy
        if delta >= t["exports_improve_pp"]:
            changes.append({"indicator": "exports", "message": f"수출 증가율 {delta:+.1f}%p 개선 (강화)",
                             "direction": "improve", "delta": round(delta, 2)})

    cpi_yoy = readings.get("cpi").detail.get("fields", {}).get("yoy") if "cpi" in readings else None
    prev_cpi_yoy = _prev_field(previous_snapshot, "cpi", "yoy")
    if cpi_yoy is not None and prev_cpi_yoy is not None:
        delta = cpi_yoy - prev_cpi_yoy
        if delta <= t["cpi_improve_pp"]:
            changes.append({"indicator": "cpi", "message": f"CPI YoY {delta:+.1f}%p 하락 (개선)",
                             "direction": "improve", "delta": round(delta, 2)})

    unemployment_change = readings.get("unemployment").detail.get("fields", {}).get("avg_3m_change") if "unemployment" in readings else None
    if unemployment_change is not None and unemployment_change >= t["unemployment_caution_pp"]:
        changes.append({"indicator": "unemployment", "message": f"실업률 3개월 평균 {unemployment_change:+.1f}%p 상승 (주의)",
                         "direction": "caution", "delta": round(unemployment_change, 2)})

    ppi_yoy = readings.get("ppi").detail.get("fields", {}).get("yoy") if "ppi" in readings else None
    prev_ppi_yoy = _prev_field(previous_snapshot, "ppi", "yoy")
    if ppi_yoy is not None and prev_ppi_yoy is not None:
        delta = ppi_yoy - prev_ppi_yoy
        if delta <= t["ppi_ease_pp"]:
            changes.append({"indicator": "ppi", "message": f"PPI YoY {delta:+.1f}%p 둔화 (완화)",
                             "direction": "improve", "delta": round(delta, 2)})

    if not changes:
        changes.append({"indicator": "all", "message": "임계치를 넘는 뚜렷한 변화 없음 (관찰 지속)", "direction": "flat"})
    return changes
