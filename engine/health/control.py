"""제어(closed-loop의 'act' 절반) — 상태 지속, 임계 판정, 알림 발송.

## 설계 — subscription_monitor/compose.py의 검증된 패턴을 그대로 재사용

이 저장소엔 이미 작동 중인 close-loop이 하나 있다(collectors/
subscription_monitor): `consecutive_failures` 카운터 + 임계치 + `outage_alerted`
플래그로 "임계 돌파 시 딱 한 번만 알린다 → 회복하면 리셋"을 구현한다.
매번 새로 알리면 소음이고, 한 번도 안 알리면 조용히 죽는다 — 이 저장소가
이미 검증한 균형점을 그대로 가져온다(새로 설계하지 않는다).

## 알림 채널도 재사용

`core.notify`(scripts/send_report_email.py가 쓰는 것과 같은 채널)를
그대로 쓴다 — 새 이메일 인프라를 안 만든다. GMAIL_ADDRESS 등 시크릿이
없는 로컬/테스트 환경에서는 `notify.is_configured()`가 False라 조용히
건너뛴다(에러 아님 — 이 자체가 컬렉터 장애는 아니므로).

## 임계값

`CONSECUTIVE_THRESHOLD = 3` — 이 헬스체크 자체가 주기적으로(기본 2시간
간격) 도니 3회 연속이면 최소 4~6시간 동안 문제가 지속됐다는 뜻이다.
1회 만에 알리면 일시적 API 지연에도 소음이 되고, 너무 크면 알림이
늦다 — subscription_monitor의 "30분 컬렉터에 6회(=3시간)" 비율과
비슷한 수준으로 맞췄다.
"""
from __future__ import annotations

import json
from pathlib import Path

from core import notify
from engine.health.check import HealthReport, check_all, OK

REPO = Path(__file__).resolve().parents[2]
STATE_PATH = REPO / "data" / "health" / "state.json"
REPORT_JSON_PATH = REPO / "data" / "health" / "latest_report.json"
REPORT_MD_PATH = REPO / "data" / "health" / "latest_report.md"

CONSECUTIVE_THRESHOLD = 3


def _load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True),
                          encoding="utf-8")


def _run_url() -> str:
    import os
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if repo and run_id:
        return f"https://github.com/{repo}/actions/runs/{run_id}"
    return "(로컬 실행 — 링크 없음)"


def apply_control(report: HealthReport, state: dict | None = None,
                   send_alerts: bool = True) -> dict:
    """상태를 갱신하고, 임계를 넘긴 소스에 대해 알림을 발송한다(1회만).
    회복한 소스는 카운터를 리셋한다. 갱신된 state와 이번에 실제로 발송한
    알림 목록을 돌려준다 — 테스트가 이걸로 "알림이 정확히 언제 한 번만
    발송되는지"를 고정한다."""
    st = _load_state() if state is None else dict(state)
    fired: list[dict] = []

    for s in report.statuses:
        entry = st.setdefault(s.slug, {"consecutive_bad": 0, "alerted": False})
        if s.state == OK:
            if entry["alerted"]:
                fired.append({"slug": s.slug, "kind": "recovery", "detail": s.detail})
            entry["consecutive_bad"] = 0
            entry["alerted"] = False
            continue

        entry["consecutive_bad"] += 1
        if entry["consecutive_bad"] >= CONSECUTIVE_THRESHOLD and not entry["alerted"]:
            entry["alerted"] = True
            fired.append({"slug": s.slug, "kind": "alert", "state": s.state,
                         "severity": s.severity, "detail": s.detail,
                         "workflow": s.workflow, "consecutive": entry["consecutive_bad"]})

    if send_alerts:
        for f in fired:
            _send(f)

    _save_state(st)
    _write_report_snapshot(report)
    return {"state": st, "fired": fired}


def _send(fired: dict) -> None:
    if not notify.is_configured():
        print(f"[health] 알림 채널 미설정 — 발송 생략: {fired}")
        return
    if fired["kind"] == "recovery":
        subject = f"[데이터 헬스 회복] {fired['slug']}"
        body = f"{fired['slug']} 데이터 소스가 정상으로 돌아왔습니다.\n\n{fired['detail']}"
    else:
        mark = "🔴" if fired["severity"] == "critical" else "🟠"
        subject = f"[데이터 헬스 {mark}] {fired['slug']} {fired['consecutive']}회 연속 이상"
        body = (
            f"데이터 소스 '{fired['slug']}'가 {fired['consecutive']}회 연속 헬스체크에서 "
            f"'{fired['state']}' 상태입니다.\n\n"
            f"상세: {fired['detail']}\n"
            f"관련 워크플로: {fired['workflow']}\n"
            f"실행 로그: {_run_url()}\n\n"
            f"이 소스에 의존하는 판단(브리핑·리포트)은 이 알림이 해소될 때까지 "
            f"신뢰하지 마십시오."
        )
    notify.build_channel().send(subject, body)
    print(f"[health] 알림 발송: {fired.get('slug')} ({fired['kind']})")


def _write_report_snapshot(report: HealthReport) -> None:
    """브리핑 팩·PEOS 리포트가 이 파일 하나만 읽으면 되게 한다 — 그쪽이
    check_all()을 직접 부르면 매번 전체 소스를 재계산해야 하고, 이 스냅샷이
    없으면 "가장 최근에 확인한 결과"조차 없다."""
    REPORT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON_PATH.write_text(
        json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [f"# 데이터 헬스 — {report.checked_at}", ""]
    bad = report.bad
    if not bad:
        lines.append(f"✅ 전 소스 정상 ({len(report.statuses)}개)")
    else:
        lines.append(f"⚠️ {len(bad)}/{len(report.statuses)}개 소스 이상")
        for s in sorted(bad, key=lambda x: (x.severity != "critical", x.slug)):
            mark = "🔴" if s.severity == "critical" else "🟠"
            lines.append(f"- {mark} **{s.slug}** [{s.state}] {s.description} — {s.detail}")
    REPORT_MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(send_alerts: bool = True) -> dict:
    report = check_all()
    result = apply_control(report, send_alerts=send_alerts)
    result["report"] = report
    return result
