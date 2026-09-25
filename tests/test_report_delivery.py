"""보고서 발행 원칙(wiki/concepts/report-delivery-policy.md) — 조용한 미발행 금지."""
from __future__ import annotations

import sys
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import report_watchdog as W  # noqa: E402
import send_pending_briefings as S  # noqa: E402
from engine.briefing import notice as N  # noqa: E402


def test_holiday_editions_and_notice():
    # 휴장일 아침 = 휴장판(발행), 연휴 마지막 날 저녁 = 재개장 전야판(발행),
    # 그 외 휴장일 저녁 = 코드 상황 보고(사유 명시)
    assert N.edition("AM", date(2026, 9, 25)) == "holiday_am"
    assert N.skip_reason("AM", date(2026, 9, 25), None) is None
    assert N.edition("PM", date(2026, 9, 28)) == "eve_pm"
    assert N.skip_reason("PM", date(2026, 9, 28), None) is None
    assert "추석" in N.skip_reason("PM", date(2026, 9, 25), None)


def test_quiet_gate_yields_a_notice_reason():
    class G:
        publish = False
    assert "조용한 날" in N.skip_reason("AM", date(2026, 9, 23), G())


def test_notice_explains_and_carries_other_content_without_llm_directives():
    md = N.build_notice_markdown("PM", date(2026, 9, 24), "휴장", "루틴 미실행")
    assert "정규 브리핑이 없는 이유" in md and "그 외 보고할 수 있는 내용" in md
    assert "notice: true" in md and "반영할 것" not in md


def test_notice_and_regular_briefing_have_different_ledger_keys(tmp_path):
    n = tmp_path / "2026-09-24-AM.md"
    n.write_text("---\ntitle: x\nnotice: true\n---\n", encoding="utf-8")
    assert S.briefing_key(n) == "2026-09-24-AM:notice"
    n.write_text("---\ntitle: x\nslot: AM\n---\n", encoding="utf-8")
    assert S.briefing_key(n) == "2026-09-24-AM"


def test_watchdog_waits_for_grace_then_checks():
    sched = [{"id": "a", "days": list(range(7)), "due": "08:00", "grace_min": 150}]
    assert W.due_reports(datetime(2026, 9, 24, 10, 0, tzinfo=W.KST), sched) == []
    assert W.due_reports(datetime(2026, 9, 24, 10, 31, tzinfo=W.KST), sched) == sched


def test_watchdog_diagnosis_never_treats_unknown_as_delivered():
    assert W.diagnose(None, 1)[0] is False
    assert "시작되지 않았습니다" in W.diagnose([], 1)[1]
    assert W.diagnose([{"conclusion": "success"}], 1) == (True, "")
    assert W.diagnose([{"status": "completed", "conclusion": "success"}], 2)[0] is False


def test_every_scheduled_report_has_required_fields():
    import yaml
    for r in yaml.safe_load(W.SCHEDULE.read_text(encoding="utf-8"))["reports"]:
        assert {"id", "name", "kind", "days", "due", "grace_min"} <= set(r)
        assert r["kind"] in ("briefing", "workflow")
        if r["kind"] == "workflow":
            assert (REPO / ".github" / "workflows" / r["workflow"]).exists()
