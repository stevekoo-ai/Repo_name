"""engine/health/* — 데이터 수집 close-loop 시스템.

## 이 테스트가 고정하는 계약

사용자 요청: "데이터 수집 블럭 API 자동 수집 포함 정상 작동 중인지
센싱하고, 신선도와 내용에 비정상이 확인되면 제어하는 feedback closed-loop."

1. **판정 불가는 이상이 아니다** — freshness를 못 구하면 None, STALE로
   단정하지 않는다(R3).
2. **거래일 예외가 진짜로 예외 처리되는지** — 휴장일에 어제 데이터가
   있으면 OK, 휴장일인데 그보다도 더 오래된 데이터면 여전히 이상.
3. **레지스트리 자기 검증** — 이 파일이 등록한 RUN_LOG 소스가 실제
   run-log에 한 번이라도 나타난 적 있는지, CSV 경로가 실존하는지를
   테스트가 검사한다. us-labor-outlook을 RUN_LOG로 잘못 등록했다가
   실제로 --check-only를 돌려보고서야 발견한 사고를 재발 방지한다.
4. **제어 루프 — 임계 돌파 시 딱 한 번만 알림, 회복 시 리셋.**
   subscription_monitor의 검증된 패턴을 그대로 재사용했으므로 그
   계약도 그대로 고정한다.
5. **기존 스윕(data_freshness_audit)과 중복 판정하지 않는다** —
   `data/normalized/*.csv`는 여기서 재등록하지 않는다.
"""
from __future__ import annotations

import csv
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from engine.health import content, control, freshness
from engine.health.check import ANOMALY, MISSING, OK, STALE, SourceStatus, check_all, check_one
from engine.health.registry import SOURCES, FreshnessMode, SourceSpec

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _isolate_health_state(tmp_path, monkeypatch):
    """control.py의 상태/스냅샷 파일은 실제 저장소의 data/health/*를 가리킨다
    — 격리하지 않으면 테스트가 진짜 운영 상태(state.json, latest_report.*)를
    가짜 slug("x")로 덮어써버린다. 모든 테스트에 자동 적용."""
    monkeypatch.setattr(control, "STATE_PATH", tmp_path / "state.json")
    monkeypatch.setattr(control, "REPORT_JSON_PATH", tmp_path / "latest_report.json")
    monkeypatch.setattr(control, "REPORT_MD_PATH", tmp_path / "latest_report.md")


# ── 판정 불가 vs 이상 ────────────────────────────────────────────

def test_missing_file_is_missing_not_stale(tmp_path):
    spec = SourceSpec(slug="t", description="t", workflow="t.yml",
                      mode=FreshnessMode.CSV_FETCHED_AT,
                      path=str((tmp_path / "does-not-exist.csv").relative_to(REPO))
                      if str(tmp_path).startswith(str(REPO)) else "does/not/exist.csv",
                      max_age_hours=24)
    status = check_one(spec)
    assert status.state == MISSING


def test_freshness_none_is_not_treated_as_stale():
    """값을 못 구했을 때(None) is_stale이 True를 내면 안 된다 —
    호출부(check_one)가 MISSING으로 먼저 걸러야 한다."""
    spec = SourceSpec(slug="t", description="t", workflow="t.yml",
                      mode=FreshnessMode.CSV_FETCHED_AT, path="nope.csv", max_age_hours=1)
    result = freshness.FreshnessResult(None, None, None, "no data")
    assert freshness.is_stale(spec, result) is False


# ── 신선도 계산 (실제 파일로) ────────────────────────────────────

def _write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def test_csv_fetched_at_picks_the_max_not_the_last_row(tmp_path, monkeypatch):
    monkeypatch.setattr(freshness, "REPO", tmp_path)
    p = tmp_path / "s.csv"
    now = datetime.now(timezone.utc)
    old = (now - timedelta(hours=50)).isoformat()
    new = (now - timedelta(hours=1)).isoformat()
    _write_csv(p, ["date", "value", "fetched_at"],
              [["2026-01-01", "1", new], ["2026-01-02", "2", old]])  # 일부러 역순
    spec = SourceSpec(slug="s", description="s", workflow="w.yml",
                      mode=FreshnessMode.CSV_FETCHED_AT, path="s.csv", max_age_hours=24)
    result = freshness.compute_freshness(spec)
    assert result.age_hours < 2, "행 순서와 무관하게 가장 최근 fetched_at을 골라야 한다"


def test_stale_when_older_than_max_age(tmp_path, monkeypatch):
    monkeypatch.setattr(freshness, "REPO", tmp_path)
    p = tmp_path / "s.csv"
    old = (datetime.now(timezone.utc) - timedelta(hours=100)).isoformat()
    _write_csv(p, ["date", "value", "fetched_at"], [["2026-01-01", "1", old]])
    spec = SourceSpec(slug="s", description="s", workflow="w.yml",
                      mode=FreshnessMode.CSV_FETCHED_AT, path="s.csv", max_age_hours=24)
    assert freshness.is_stale(spec, freshness.compute_freshness(spec)) is True


# ── 거래일 예외 ──────────────────────────────────────────────────

def test_holiday_with_last_trading_day_data_is_not_stale(tmp_path, monkeypatch):
    """오늘이 휴장이고 마지막 거래일 데이터까지 있으면 나이가 얼마든 OK."""
    monkeypatch.setattr(freshness, "REPO", tmp_path)
    from engine.briefing import calendar as C

    saturday = date(2026, 9, 12)
    friday = date(2026, 9, 11)

    class FixedNow(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2026, 9, 12, 10, 0, tzinfo=timezone.utc)

    monkeypatch.setattr(freshness, "datetime", FixedNow)
    fr = freshness.FreshnessResult(None, friday, 999999, "old but last trading day")
    spec = SourceSpec(slug="s", description="s", workflow="w.yml",
                      mode=FreshnessMode.CSV_FETCHED_AT, path="s.csv",
                      max_age_hours=1, market="KR")
    assert C.is_trading_day("KR", saturday) is False
    assert freshness.is_stale(spec, fr) is False


def test_holiday_missing_even_last_trading_day_is_still_stale(monkeypatch):
    """휴장일 핑계로 진짜 장애를 가리면 안 된다 — 마지막 거래일 데이터조차
    없으면 여전히 STALE."""
    class FixedNow(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2026, 9, 12, 10, 0, tzinfo=timezone.utc)

    monkeypatch.setattr(freshness, "datetime", FixedNow)
    fr = freshness.FreshnessResult(None, date(2026, 9, 8), 999999, "too old")
    spec = SourceSpec(slug="s", description="s", workflow="w.yml",
                      mode=FreshnessMode.CSV_FETCHED_AT, path="s.csv",
                      max_age_hours=1, market="KR")
    assert freshness.is_stale(spec, fr) is True


# ── 내용 검증 ────────────────────────────────────────────────────

def test_missing_required_column_is_flagged(tmp_path, monkeypatch):
    monkeypatch.setattr(content, "REPO", tmp_path)
    p = tmp_path / "s.csv"
    _write_csv(p, ["date", "value"], [["2026-01-01", "1"]])
    spec = SourceSpec(slug="s", description="s", workflow="w.yml",
                      mode=FreshnessMode.CSV_FETCHED_AT, path="s.csv", max_age_hours=24,
                      required_columns=("date", "value", "fetched_at"))
    problems = content.check_content(spec)
    assert problems and "fetched_at" in problems[0]


def test_empty_file_below_min_rows_is_flagged(tmp_path, monkeypatch):
    monkeypatch.setattr(content, "REPO", tmp_path)
    p = tmp_path / "s.csv"
    _write_csv(p, ["date", "value"], [])
    spec = SourceSpec(slug="s", description="s", workflow="w.yml",
                      mode=FreshnessMode.CSV_FETCHED_AT, path="s.csv", max_age_hours=24,
                      min_rows=1)
    assert content.check_content(spec)


def test_content_check_skipped_for_run_log_sources():
    """RUN_LOG/DATED_FILE_GLOB 소스는 path가 없다 — 검사 대상 파일을
    특정할 수 없으므로 예외를 던지지 않고 조용히 빈 리스트를 낸다."""
    spec = SourceSpec(slug="s", description="s", workflow="w.yml",
                      mode=FreshnessMode.RUN_LOG, run_log_workflow="w", run_log_step="s",
                      max_age_hours=24, required_columns=("x",))
    assert content.check_content(spec) == []


# ── 레지스트리 자기 검증 (2026-09-15 us-labor-outlook 오등록 사고 재발 방지) ──

def test_every_run_log_source_has_appeared_at_least_once():
    """RUN_LOG로 등록한 (workflow, step)이 실제 automation-run-log.csv에
    한 번도 없으면 그 소스는 영원히 MISSING만 뜬다 — 등록 자체가 틀렸다는
    뜻이다. us-labor-outlook을 이렇게 잘못 등록했다가 --check-only를
    실행하고서야 발견했다; 이제 테스트가 그 발견을 자동화한다."""
    seen: set[tuple[str, str]] = set()
    log = REPO / "sources" / "automation-run-log.csv"
    if log.exists():
        with log.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                seen.add((r.get("workflow", ""), r.get("step", "")))

    never_seen = []
    for s in SOURCES:
        if s.mode != FreshnessMode.RUN_LOG or s.slug == "subscription-monitor":
            continue  # subscription-monitor는 run-log가 아니라 자체 JSON을 본다
        if (s.run_log_workflow, s.run_log_step) not in seen:
            never_seen.append(s.slug)
    assert not never_seen, (
        f"run-log에 한 번도 안 나타난 RUN_LOG 소스: {never_seen} — "
        "workflow/step 이름이 실제 로그 기록과 다르거나, 그 워크플로가 "
        "애초에 automation-run-log.csv에 기록하지 않는다(등록 모드 재검토 필요)"
    )


def test_every_csv_path_source_points_to_a_real_or_expected_path():
    """오타로 존재하지 않는 경로를 등록하면 영구 MISSING이 된다 — 최소한
    부모 디렉터리(sources/, data/...)는 실존해야 한다는 것만 고정한다
    (파일 자체는 첫 실행 전엔 없을 수 있으므로 강하게 요구하지 않는다)."""
    for s in SOURCES:
        if s.path is None:
            continue
        p = REPO / s.path
        assert p.parent.exists(), f"{s.slug}: {s.path}의 상위 디렉터리가 없다"


def test_registry_has_no_duplicate_slugs():
    slugs = [s.slug for s in SOURCES]
    assert len(slugs) == len(set(slugs))


def test_dated_file_glob_sources_resolve_for_today():
    """오늘 날짜 보고서가 실제로 있는 상태에서(정상 케이스) 글롭이
    맞물리는지 — 템플릿 문법 자체가 깨져 있으면 영원히 MISSING이 뜬다."""
    for s in SOURCES:
        if s.mode != FreshnessMode.DATED_FILE_GLOB:
            continue
        result = freshness.compute_freshness(s)
        # 템플릿이 `.format(date=...)`로 실제 치환 가능한지만 본다 — 오늘
        # 파일이 없을 수도 있으니(주말 등) 존재 여부까진 강하게 요구 안 함.
        assert "{date}" in s.dated_glob_template
        formatted = s.dated_glob_template.format(date="2026-01-01")
        assert "{date}" not in formatted


# ── check_all() 통합 ─────────────────────────────────────────────

def test_check_all_covers_every_registered_source():
    report = check_all()
    slugs = {s.slug for s in report.statuses}
    for spec in SOURCES:
        assert spec.slug in slugs


def test_normalized_sweep_is_folded_in_without_duplicating_registry():
    """data/normalized/*.csv는 registry.SOURCES에 개별 등록돼 있지 않다 —
    check_all()의 결과에만 나타나야 한다."""
    assert not any(s.path and "data/normalized" in s.path for s in SOURCES)
    report = check_all()
    assert any(s.slug.startswith("normalized:") or s.slug == "normalized-series-sweep"
              for s in report.statuses)


def test_bad_and_critical_bad_properties():
    report = check_all()
    assert all(s.state != OK for s in report.bad)
    assert all(s.severity == "critical" for s in report.critical_bad)
    bad_slugs = {s.slug for s in report.bad}
    assert all(s.slug in bad_slugs for s in report.critical_bad)


# ── 제어 루프 (subscription_monitor 패턴 재사용 계약) ─────────────

def _status(slug, state, severity="warning"):
    return SourceStatus(slug=slug, description="d", workflow="w.yml",
                        severity=severity, state=state, detail="d", age_hours=1.0)


def test_alert_fires_exactly_once_at_threshold(monkeypatch):
    sent = []
    monkeypatch.setattr(control.notify, "is_configured", lambda: True)
    monkeypatch.setattr(control.notify, "build_channel",
                        lambda: type("C", (), {"send": lambda self, s, b: sent.append((s, b))})())

    state = {}
    from engine.health.check import HealthReport
    for i in range(control.CONSECUTIVE_THRESHOLD + 2):
        report = HealthReport(checked_at="t", statuses=[_status("x", STALE)])
        result = control.apply_control(report, state=state)
        state = result["state"]
    assert len(sent) == 1, "임계 돌파 후에도 매번 다시 알리면 소음이다"
    assert state["x"]["alerted"] is True


def test_recovery_resets_and_reports_fired(monkeypatch):
    monkeypatch.setattr(control.notify, "is_configured", lambda: True)
    monkeypatch.setattr(control.notify, "build_channel",
                        lambda: type("C", (), {"send": lambda self, s, b: None})())
    from engine.health.check import HealthReport

    state = {"x": {"consecutive_bad": 5, "alerted": True}}
    report = HealthReport(checked_at="t", statuses=[_status("x", OK)])
    result = control.apply_control(report, state=state)
    assert result["state"]["x"] == {"consecutive_bad": 0, "alerted": False}
    assert any(f["kind"] == "recovery" for f in result["fired"])


def test_no_alert_below_threshold(monkeypatch):
    sent = []
    monkeypatch.setattr(control.notify, "is_configured", lambda: True)
    monkeypatch.setattr(control.notify, "build_channel",
                        lambda: type("C", (), {"send": lambda self, s, b: sent.append(1)})())
    from engine.health.check import HealthReport

    state = {}
    for _ in range(control.CONSECUTIVE_THRESHOLD - 1):
        report = HealthReport(checked_at="t", statuses=[_status("x", STALE)])
        state = control.apply_control(report, state=state)["state"]
    assert not sent


def test_unconfigured_channel_does_not_crash(monkeypatch):
    """시크릿이 없는 로컬/테스트 환경에서 알림 시도가 예외를 던지면 안
    된다 — 조용히 건너뛴다."""
    monkeypatch.setattr(control.notify, "is_configured", lambda: False)
    from engine.health.check import HealthReport

    state = {}
    for _ in range(control.CONSECUTIVE_THRESHOLD + 1):
        report = HealthReport(checked_at="t", statuses=[_status("x", STALE, "critical")])
        state = control.apply_control(report, state=state)["state"]
    assert state["x"]["alerted"] is True  # 발송은 못 해도 상태 전이는 일어난다


def test_send_alerts_false_never_calls_notify(monkeypatch):
    called = []
    monkeypatch.setattr(control, "_send", lambda f: called.append(f))
    from engine.health.check import HealthReport

    state = {}
    for _ in range(control.CONSECUTIVE_THRESHOLD + 1):
        report = HealthReport(checked_at="t", statuses=[_status("x", STALE)])
        state = control.apply_control(report, state=state, send_alerts=False)["state"]
    assert called == []


# ── 스냅샷 기록 (브리핑/리포트가 읽는 접점) ───────────────────────

def test_snapshot_written_for_downstream_consumers(tmp_path, monkeypatch):
    monkeypatch.setattr(control, "REPORT_JSON_PATH", tmp_path / "r.json")
    monkeypatch.setattr(control, "REPORT_MD_PATH", tmp_path / "r.md")
    monkeypatch.setattr(control, "STATE_PATH", tmp_path / "s.json")
    monkeypatch.setattr(control.notify, "is_configured", lambda: False)
    from engine.health.check import HealthReport

    report = HealthReport(checked_at="t", statuses=[_status("x", STALE, "critical")])
    control.apply_control(report, state={})
    data = json.loads((tmp_path / "r.json").read_text(encoding="utf-8"))
    assert data["statuses"][0]["slug"] == "x"
    md = (tmp_path / "r.md").read_text(encoding="utf-8")
    assert "x" in md and "🔴" in md
