"""브리핑 나침반 — 압축 누적 맥락의 상한과 갱신 연산."""
import copy

import pytest

from engine.briefing import compass as C


def _c():
    return copy.deepcopy(C.load())


def test_seed_compass_is_valid_and_compact():
    c = _c()
    C.validate(c)
    assert len(C.render(c)) <= C.MAX_RENDER
    assert c["mission"] and 1 <= len(c["threads"]) <= C.MAX_THREADS


def test_seventh_thread_is_refused_until_something_is_pruned():
    c = _c()
    while len(c["threads"]) < C.MAX_THREADS:
        C.add(c, f"X{len(c['threads'])}", "q", "w", "s", "n", "2026-09-25")
    C.add(c, "T99", "q", "w", "s", "n", "2026-09-25")
    with pytest.raises(C.CompassError):
        C.validate(c)
    C.prune(c, "T99", "곁가지", "2026-09-25")
    C.validate(c)
    assert any("곁가지" in p for p in c["pruned"])


def test_verbose_status_is_refused():
    c = _c()
    C.update(c, "T1", "가" * 200, None, "2026-09-25")
    with pytest.raises(C.CompassError):
        C.validate(c)


def test_recent_conclusions_roll_to_three():
    c = _c()
    for i in range(5):
        C.conclude(c, "AM", f"결론 {i}", "2026-09-25")
    assert len(c["recent_conclusions"]) == 3 and c["recent_conclusions"][-1].endswith("결론 4")


def test_pack_puts_compass_first_after_health():
    from datetime import date
    from engine.briefing.context import build_pack
    pack, _ = build_pack("AM", date(2026, 9, 23))
    keys = [b.key for b in pack.blocks]
    assert keys.index("compass") <= 1 and "previous" not in keys
