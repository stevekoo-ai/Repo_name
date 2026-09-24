#!/usr/bin/env python3
"""보고서 도착 워치독 — 와야 할 보고서가 기한까지 안 오면 상황을 메일로 알린다.

원칙(wiki/concepts/report-delivery-policy.md): 보고서는 조용히 사라지면 안 된다.
안 왔으면 ①무엇이 왜 안 왔는지 ②그 외 보고할 수 있는 내용을 메일로 보낸다.
일정은 data/manual_inputs/report_schedule.yaml 한 곳에서만 정한다.

- briefing: 기한까지 report/briefing/<날짜>-<SLOT>.md가 발송 장부에 없으면
  상황 보고를 써서 직접 발송한다(send_pending_briefings — 장부 기록 포함).
- workflow: 오늘 해당 워크플로의 성공 실행 수가 nth 미만이면 최근 실행 상태로
  원인을 진단해 상황 보고 메일을 보낸다.
같은 건은 하루 한 번만 알린다(data/report_watchdog/alerted.log).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
KST = timezone(timedelta(hours=9))
SCHEDULE = REPO / "data" / "manual_inputs" / "report_schedule.yaml"
ALERTED = REPO / "data" / "report_watchdog" / "alerted.log"
TMP_MD = Path("/tmp/report_watchdog_status.md")


def _at(day: date, hhmm: str) -> datetime:
    h, m = map(int, hhmm.split(":"))
    return datetime(day.year, day.month, day.day, h, m, tzinfo=KST)


def due_reports(now: datetime, schedule: list[dict]) -> list[dict]:
    today = now.date()
    return [r for r in schedule if today.weekday() in r["days"]
            and now >= _at(today, r["due"]) + timedelta(minutes=r["grace_min"])]


def alerted_keys() -> set[str]:
    return set(ALERTED.read_text(encoding="utf-8").split()) if ALERTED.exists() else set()


def mark(key: str) -> None:
    ALERTED.parent.mkdir(parents=True, exist_ok=True)
    with ALERTED.open("a", encoding="utf-8") as fh:
        fh.write(key + "\n")


def workflow_runs(workflow: str, since: datetime) -> list[dict] | None:
    repo, token = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_TOKEN")
    if not repo or not token:
        return None
    url = (f"https://api.github.com/repos/{repo}/actions/workflows/{workflow}/runs"
           f"?per_page=30&created=>={since.astimezone(timezone.utc):%Y-%m-%dT%H:%M:%SZ}")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}",
                                               "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read()).get("workflow_runs", [])
    except Exception:  # noqa: BLE001 — 진단 불가도 결과로 보고한다
        return None


def diagnose(runs: list[dict] | None, nth: int) -> tuple[bool, str]:
    """(도착했나, 원인 문장)."""
    if runs is None:
        return False, "GitHub 실행 기록을 조회하지 못해 원인을 확인할 수 없습니다."
    ok = [r for r in runs if r.get("conclusion") == "success"]
    if len(ok) >= nth:
        return True, ""
    latest = runs[0] if runs else None
    if latest is None:
        return False, ("오늘 이 시간대의 실행이 아예 시작되지 않았습니다 — GitHub 예약 실행 "
                       "대기열 지연(실측 2~4.7시간) 또는 예약 누락입니다.")
    st, concl = latest.get("status"), latest.get("conclusion")
    if st in ("queued", "in_progress", "waiting"):
        return False, f"실행이 아직 끝나지 않았습니다(상태: {st}) — 재시도 루프 중이거나 대기열에 있습니다."
    return False, (f"최근 실행이 '{concl}'로 끝났습니다({latest.get('html_url', '')}). "
                   "성공한 실행이 기대 횟수에 못 미칩니다.")


def handle_briefing(r: dict, today: date) -> str | None:
    from engine.briefing import notice as N
    import send_pending_briefings as S

    md = REPO / "report" / "briefing" / f"{today.isoformat()}-{r['slot']}.md"
    keys = S.sent_keys()
    if md.exists() and S.briefing_key(md) in keys:
        return None
    if not md.exists():
        reason = N.skip_reason(r["slot"], today, None) or "정규 브리핑이 작성되지 않았습니다."
        N.write_notice(r["slot"], today, reason,
                       extra_problem=f"브리핑 루틴이 {r['due']} KST 이후 {r['grace_min']}분이 지나도록 "
                                     "발행하지 않았습니다 — 루틴 미실행·작성 실패·push 실패 중 하나입니다.")
    rc = subprocess.run([sys.executable, str(REPO / "scripts" / "send_pending_briefings.py")],
                        cwd=REPO).returncode
    return f"{r['name']}: 기한 내 미발송 → 상황 보고/미발송분 발송(rc={rc})"


def handle_workflow(r: dict, now: datetime) -> str | None:
    from engine.briefing import notice as N

    since = _at(now.date(), "06:00")
    ok, cause = diagnose(workflow_runs(r["workflow"], since), r["nth"])
    if ok:
        return None
    title = f"[보고서 미도착] {r['name']} — {now.date().isoformat()}"
    TMP_MD.write_text(N.build_status_markdown(
        title=title, heading="무엇이 안 왔고 왜인가",
        problem_lines=[f"{r['name']}이(가) 예정 {r['due']} KST 이후 {r['grace_min'] // 60}시간이 지나도록 도착하지 않았습니다.",
                       cause, f"워크플로: `.github/workflows/{r['workflow']}`"],
        next_line=None, as_of=now.date()), encoding="utf-8")
    rc = subprocess.run([sys.executable, "-m", "scripts.send_markdown_report",
                         "--file", str(TMP_MD), "--subject", title], cwd=REPO).returncode
    return f"{r['name']}: 미도착 알림 발송(rc={rc}) — {cause}"


def main() -> int:
    sys.path.insert(0, str(REPO / "scripts"))
    now = datetime.now(KST)
    schedule = yaml.safe_load(SCHEDULE.read_text(encoding="utf-8"))["reports"]
    done = alerted_keys()
    for r in due_reports(now, schedule):
        key = f"{now.date().isoformat()}:{r['id']}"
        if key in done:
            continue
        msg = handle_briefing(r, now.date()) if r["kind"] == "briefing" else handle_workflow(r, now)
        if msg:
            mark(key)
            print(msg)
        else:
            print(f"✓ {r['name']} 도착 확인")
    return 0


if __name__ == "__main__":
    sys.exit(main())
