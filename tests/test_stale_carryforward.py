"""Daily-cadence stale carry-forward (engine/macro/engine.py._carry_forward_stale).

A daily run's live fetch can fail on any given day for reasons unrelated to
whether the underlying economic figure changed (ECOS/KOSIS have both shown
intermittent access failures in this pipeline). Rather than regressing a
real prior reading to Pending every time that happens, the last successful
value from this month's own snapshot should be carried forward and marked
DataStatus.STALE — never fabricated, always a real past reading.
"""
from __future__ import annotations

from core.models import DataStatus, IndicatorReading
from engine.macro import engine as macro_engine


def test_carry_forward_reuses_last_ok_value_and_marks_stale():
    readings = {"cpi": IndicatorReading(name="cpi", value=None, status=DataStatus.SOURCE_ERROR, score=None)}
    current_month_snapshot = {
        "macro": {"readings": {"cpi": {
            "value": 2.5, "score": 1, "source": "KOSIS",
            "fields": {"yoy": 2.5}, "last_fresh_at": "2026-07-01T00:00:00+00:00",
        }}},
        "saved_at": "2026-07-01T00:00:00+00:00",
    }

    macro_engine._carry_forward_stale(readings, current_month_snapshot, "macro")
    r = readings["cpi"]

    assert r.status == DataStatus.STALE
    assert r.value == 2.5
    assert r.score == 1
    assert "이전 값" in r.note


def test_carry_forward_skips_when_no_prior_snapshot():
    readings = {"cpi": IndicatorReading(name="cpi", value=None, status=DataStatus.PENDING, score=None)}
    macro_engine._carry_forward_stale(readings, None, "macro")
    assert readings["cpi"].status == DataStatus.PENDING


def test_carry_forward_skips_when_prior_reading_never_scored():
    readings = {"cpi": IndicatorReading(name="cpi", value=None, status=DataStatus.PENDING, score=None)}
    current_month_snapshot = {"macro": {"readings": {"cpi": {"value": None, "score": None}}}, "saved_at": "x"}
    macro_engine._carry_forward_stale(readings, current_month_snapshot, "macro")
    assert readings["cpi"].status == DataStatus.PENDING


def test_carry_forward_never_touches_a_fresh_ok_reading():
    readings = {"cpi": IndicatorReading(name="cpi", value=3.0, status=DataStatus.OK, score=0)}
    current_month_snapshot = {"macro": {"readings": {"cpi": {"value": 2.5, "score": 1}}}, "saved_at": "x"}
    macro_engine._carry_forward_stale(readings, current_month_snapshot, "macro")
    assert readings["cpi"].value == 3.0
    assert readings["cpi"].status == DataStatus.OK


def test_carry_forward_preserves_the_original_last_fresh_timestamp():
    # The snapshot itself was saved on day 3, but the carried value was last
    # genuinely fresh on day 1 — that origin point must survive the chain,
    # not get reset to "yesterday" on every subsequent stale day.
    readings = {"cpi": IndicatorReading(name="cpi", value=None, status=DataStatus.SOURCE_ERROR, score=None)}
    current_month_snapshot = {
        "macro": {"readings": {"cpi": {
            "value": 2.5, "score": 1, "last_fresh_at": "2026-07-01T00:00:00+00:00",
        }}},
        "saved_at": "2026-07-03T00:00:00+00:00",
    }
    macro_engine._carry_forward_stale(readings, current_month_snapshot, "macro")
    assert readings["cpi"].detail["last_fresh_at"] == "2026-07-01T00:00:00+00:00"
