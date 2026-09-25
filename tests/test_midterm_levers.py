"""중간선거 레버 체크포인트(engine/briefing/midterm_levers.py) — 합성 데이터."""
from datetime import date, timedelta

from engine.briefing import midterm_levers as ML

AS_OF = date(2026, 10, 20)


def _weekly(vals, end=AS_OF):
    return [((end - timedelta(days=7 * (len(vals) - 1 - i))).isoformat(), v) for i, v in enumerate(vals)]


def _get(checks, cid):
    return next(c for c in checks if c.id == cid)


def test_gas_signal_needs_two_consecutive_weeks_below_threshold():
    one = ML.evaluate(AS_OF, {"us_gasoline": _weekly([4.30, 4.10, 3.95])})
    two = ML.evaluate(AS_OF, {"us_gasoline": _weekly([4.30, 3.98, 3.95])})
    assert _get(one, "L1-gas").ok is False
    assert _get(two, "L1-gas").ok is True


def test_missing_or_stale_data_is_unknown_not_false():
    stale = ML.evaluate(AS_OF, {"us_gasoline": _weekly([3.5, 3.4], end=AS_OF - timedelta(days=40))})
    assert _get(stale, "L1-gas").ok is None
    assert _get(ML.evaluate(AS_OF, {}), "L3-30y").ok is None


def test_5y5y_warning_only_on_sharp_rise():
    days = [((AS_OF - timedelta(days=20 - i)).isoformat(), 2.2 + (0.015 * i)) for i in range(21)]
    assert _get(ML.evaluate(AS_OF, {"us_5y5y_infl": days}), "L3-5y5y").ok is True


def test_render_flags_lit_signals_for_the_briefing():
    md = ML.render_markdown(ML.evaluate(AS_OF, {"us_gasoline": _weekly([3.9, 3.8])}), AS_OF)
    assert "🔔" in md and "반영할 것" in md
