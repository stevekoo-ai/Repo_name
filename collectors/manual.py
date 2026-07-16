"""Manual-input loaders for sources with no accessible official API.

Per 7.3 (반도체 특화 데이터 예외 정책) and the 8.1 note that 청약홈/LH/GH/SH
publish no per-user API, these three domains are updated by hand in
`data/manual_inputs/*.yaml`. If the file is missing or stale, callers get
DataStatus.PENDING/NOT_RELEASED rather than a guess (7.9).

📚 Lesson Learned Reference: docs/LESSON_LEARNED_API_DEBUGGING.md
   수동 입력 데이터 스키마의 housing_type 필드는 API 검증 결과를 기반으로 설계:
   - Issue 5: 3단계 검증 쿼리로 확인된 "플랫폼시티 = 민영 주택" 특성
   - 수동 입력 시 housing_type을 "국민주택" 또는 "민영"으로 명시 필수
"""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from core.models import DataPoint, DataStatus, Frequency, Metadata
from . import base

REPO_ROOT = Path(__file__).resolve().parents[1]
MANUAL_DIR = REPO_ROOT / "data" / "manual_inputs"


def _load(name: str) -> dict[str, Any] | None:
    path = MANUAL_DIR / f"{name}.yaml"
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def fetch_exports() -> dict[str, DataPoint]:
    """총수출 / 반도체수출 YoY, from the manual MOTIE input file (8.1, 7.3)."""
    payload = _load("exports")
    if not payload:
        return {
            "total_exports_yoy": DataPoint("total_exports_yoy", DataStatus.PENDING,
                                            note="data/manual_inputs/exports.yaml missing"),
            "semiconductor_exports_yoy": DataPoint("semiconductor_exports_yoy", DataStatus.PENDING,
                                                    note="data/manual_inputs/exports.yaml missing"),
        }
    base.write_raw("motie", "exports", payload)
    out: dict[str, DataPoint] = {}
    for series_key, rows in payload.get("series", {}).items():
        if not rows:
            out[series_key] = DataPoint(series_key, DataStatus.NOT_RELEASED, note="No rows in manual file")
            continue
        base.append_normalized(f"motie_{series_key}", rows)
        latest = max(rows, key=lambda r: r["date"])
        metadata = Metadata(
            source="산업통상자원부 (수동 입력)", unit="%", frequency=Frequency.MONTHLY,
            reliability_grade=5, official=True,
            reference_date=date.fromisoformat(str(latest["date"])), confidence=85.0,
        )
        out[series_key] = DataPoint(series_key, DataStatus.OK, value=float(latest["value"]), metadata=metadata)
    return out


def fetch_semiconductor_signals() -> DataPoint:
    """Manual semiconductor sub-signal snapshot (12.2), grade capped at 3 (7.3)."""
    payload = _load("semiconductor")
    if not payload:
        return DataPoint("semiconductor_signals", DataStatus.PENDING,
                          note="data/manual_inputs/semiconductor.yaml missing")
    base.write_raw("semiconductor", "signals", payload)
    grade = payload.get("reliability_grade", 3)
    metadata = Metadata(
        source="기업 IR / TrendForce / 산업 리서치 (수동 입력)", unit="signal[-1,1]",
        frequency=Frequency.MONTHLY, reliability_grade=grade, official=False,
        reference_date=date.fromisoformat(payload["as_of"]) if payload.get("as_of") else None,
        confidence=60.0,
    )
    dp = DataPoint("semiconductor_signals", DataStatus.OK, value=0.0, metadata=metadata,
                    note="see detail['signals'] for per-factor scores")
    dp.detail["signals"] = payload.get("signals", {})
    return dp


def get_semiconductor_signal_dict() -> dict[str, float] | None:
    payload = _load("semiconductor")
    if not payload:
        return None
    return payload.get("signals", {})


def fetch_trips() -> list[dict]:
    """출장/여행 일정 (13.10, 13.11). Empty list (not None) if the file is missing."""
    payload = _load("trips")
    if not payload:
        return []
    base.write_raw("travel", "trips", payload)
    return payload.get("trips", [])


def fetch_calendar_events() -> list[dict]:
    """이번 달 이후 경제 캘린더 원본 항목 (13.12, 16.12)."""
    payload = _load("calendar")
    if not payload:
        return []
    base.write_raw("calendar", "events", payload)
    return payload.get("events", [])


def fetch_subscription_notices() -> list[dict]:
    """공공분양/청약 공고 목록 (13.8, 13.9). Empty list (not None) if file missing."""
    payload = _load("subscription_notices")
    if not payload:
        return []
    base.write_raw("subscription", "notices", payload)
    return payload.get("notices", [])
