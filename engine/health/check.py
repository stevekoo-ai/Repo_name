"""전 소스 헬스 판정 — sensing의 최종 조립 지점.

`check_all()`이 registry.SOURCES를 순회하며 각 소스를 판정한다. 이 모듈은
**판정만** 한다 — 알림 발송이나 상태 파일 기록은 control.py가 한다
(sensing과 acting을 분리해야 sensing 로직을 알림 없이 테스트할 수 있다).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from engine.health import content, freshness
from engine.health.registry import SOURCES, SourceSpec

REPO = Path(__file__).resolve().parents[2]
SUBSCRIPTION_HEALTH_STATE = REPO / "collectors" / "subscription_monitor" / "health_state.json"
NORMALIZED_AUDIT_PREFIX = "normalized:"

# SourceStatus.state 값
OK = "OK"
STALE = "STALE"
ANOMALY = "ANOMALY"          # 신선하지만 내용이 이상함
MISSING = "MISSING"          # 데이터를 한 번도 못 찾음(신선도 판정 자체가 불가)


@dataclass
class SourceStatus:
    slug: str
    description: str
    workflow: str
    severity: str
    state: str
    detail: str
    age_hours: float | None


def _check_subscription_monitor(spec: SourceSpec) -> SourceStatus:
    """자체 close-loop(health_state.json)을 이미 가진 소스 — 그 결과를
    그대로 반영해 표시만 한다. 이중으로 알림을 만들지 않는다(그 컬렉터의
    compose.py가 이미 outage/recovery 메일을 보낸다) — 여기서는 대시보드에
    "이미 자체 감시 중"이라는 사실만 드러낸다."""
    if not SUBSCRIPTION_HEALTH_STATE.exists():
        return SourceStatus(spec.slug, spec.description, spec.workflow, spec.severity,
                            MISSING, "health_state.json 없음 — 최초 실행 전이거나 경로 변경됨", None)
    try:
        state = json.loads(SUBSCRIPTION_HEALTH_STATE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return SourceStatus(spec.slug, spec.description, spec.workflow, spec.severity,
                            ANOMALY, f"health_state.json 파싱 실패: {e}", None)
    consecutive = state.get("consecutive_failures", 0)
    outage = state.get("outage_alerted", False)
    heartbeat = state.get("last_heartbeat_date")
    if outage or consecutive >= 3:
        return SourceStatus(spec.slug, spec.description, spec.workflow, spec.severity,
                            STALE, f"자체 감시가 이미 outage 판정 중 (연속실패 {consecutive}, "
                            f"outage_alerted={outage}, 최근 심박 {heartbeat})", None)
    return SourceStatus(spec.slug, spec.description, spec.workflow, spec.severity,
                        OK, f"자체 감시 정상 (연속실패 {consecutive}, 최근 심박 {heartbeat})", None)


def check_one(spec: SourceSpec) -> SourceStatus:
    if spec.slug == "subscription-monitor":
        return _check_subscription_monitor(spec)

    fr = freshness.compute_freshness(spec)
    if fr.age_hours is None and fr.last_seen_date is None:
        return SourceStatus(spec.slug, spec.description, spec.workflow, spec.severity,
                            MISSING, fr.detail, None)

    problems = content.check_content(spec)
    if problems:
        return SourceStatus(spec.slug, spec.description, spec.workflow, spec.severity,
                            ANOMALY, "; ".join(problems), fr.age_hours)

    if freshness.is_stale(spec, fr):
        return SourceStatus(spec.slug, spec.description, spec.workflow, spec.severity,
                            STALE, fr.detail, fr.age_hours)

    return SourceStatus(spec.slug, spec.description, spec.workflow, spec.severity,
                        OK, fr.detail, fr.age_hours)


def check_normalized_series() -> list[SourceStatus]:
    """`data/normalized/*.csv`(232개 시리즈) 전수 스윕 — 새 판정 로직을 만들지
    않고 기존 `scripts/data_freshness_audit.py`를 그대로 호출한다.

    2026-09-15 실측: 이 스윕이 이미 DEAD 22개·stale 18개를 찾아내고
    있었는데, `core10-collect.yml`에서 GitHub Actions 로그의 `::warning::`
    한 줄로만 남고 알림도, 리포트 반영도 없었다 — sensing은 있었지만
    acting이 없는 반쪽짜리 loop였다. 여기서 그 결과를 흡수해 나머지
    절반(제어·알림·리포트 노출)을 이어붙인다.

    'ok' 시리즈는 개별 등록하지 않고(232개를 전부 SourceStatus로 만들면
    대시보드가 못 쓸 정도로 길어진다) 요약 1건으로 묶는다. 문제 있는
    시리즈만 slug가 부여돼 control.py의 연속-이상 카운터가 개별 추적한다."""
    from scripts.data_freshness_audit import audit

    rows = audit()
    bad = [r for r in rows if r["status"] != "ok"]
    out: list[SourceStatus] = []
    for r in bad:
        state = STALE  # dead도 "이 시리즈에 대한 최신값이 없다"는 점에서 STALE로 통일
        severity = "critical" if r["status"] == "dead" else "warning"
        out.append(SourceStatus(
            slug=f"{NORMALIZED_AUDIT_PREFIX}{r['series']}",
            description=f"정규화 시리즈: {r['series']} ({r['frequency']})",
            workflow="scripts/data_freshness_audit.py (core10-collect.yml 등)",
            severity=severity, state=state,
            detail=f"{r['status'].upper()} — 최신 {r['last']}, {r['age_days']}일 경과",
            age_hours=r["age_days"] * 24.0,
        ))
    out.append(SourceStatus(
        slug="normalized-series-sweep",
        description=f"data/normalized/*.csv 전수 스윕 ({len(rows)}개 시리즈)",
        workflow="scripts/data_freshness_audit.py",
        severity="warning",
        state=OK if not bad else ANOMALY,
        detail=f"ok {len(rows)-len(bad)} / 이상 {len(bad)}"
               + (f" — 상세는 개별 {NORMALIZED_AUDIT_PREFIX}* 항목 참고" if bad else ""),
        age_hours=None,
    ))
    return out


@dataclass
class HealthReport:
    checked_at: str
    statuses: list[SourceStatus]

    @property
    def bad(self) -> list[SourceStatus]:
        return [s for s in self.statuses if s.state != OK]

    @property
    def critical_bad(self) -> list[SourceStatus]:
        return [s for s in self.bad if s.severity == "critical"]

    def to_dict(self) -> dict:
        return {
            "checked_at": self.checked_at,
            "statuses": [
                {"slug": s.slug, "description": s.description, "workflow": s.workflow,
                 "severity": s.severity, "state": s.state, "detail": s.detail,
                 "age_hours": s.age_hours}
                for s in self.statuses
            ],
        }


def check_all() -> HealthReport:
    now = datetime.now(timezone.utc).isoformat()
    statuses = [check_one(s) for s in SOURCES]
    statuses.extend(check_normalized_series())
    return HealthReport(checked_at=now, statuses=statuses)
