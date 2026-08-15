"""Deliver the daily economic report by email — and say so loudly when it fails.

WHY THIS EXISTS
───────────────
Generating a report and delivering one are different things, and this repo has
already learned the difference the expensive way:

  2026-08-08~10  리포트 3일 연속 생성 성공 → git push 거부 → 통째로 폐기
  2026-08-11~    발행 워크플로가 main에서 사라져 자동 생성 자체가 0건

Both were silent. Nobody found out from the system; the user found out by
noticing the reports had stopped. So the rule this script enforces is:

    보고서가 도착하지 않은 날에는, 도착하지 않았다는 사실이 전달되어야 한다.

`engine/report/run.py` already pushes a short text summary through
`core.notify`, and deliberately swallows failures there — report generation
must not die because SMTP hiccuped. This script is the other half: it sends the
**report itself** (HTML body + attachment), and unlike the pipeline it exits
non-zero when a configured channel fails, so the workflow can surface it.

    python -m scripts.send_report_email                  # today's report
    python -m scripts.send_report_email --date 2026-08-13
    python -m scripts.send_report_email --allow-unconfigured   # local dry run
    python -m scripts.send_report_email --failure-alert "무엇이 실패했는지"

TRACK BOUNDARY (wiki/concepts/automation-strategy-and-delivery-boundary.md)
This sends economic-judgment reports only — 트랙 A. It reads from report/ and
nothing else, and it must never be pointed at company material (트랙 B), which
may not leave the machine by GitHub or by mail.
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path

from core import notify

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "report"

# Gmail rejects very large messages, and a report whose HTML has ballooned is a
# bug worth seeing rather than a mail worth sending.
MAX_ATTACHMENT_BYTES = 20 * 1024 * 1024


def find_report(day: date) -> Path | None:
    """The dated archive copy first, then the month file it was cut from.

    run.py writes both: report/<YYYY-MM-DD>.html (that day's archive) and
    report/<YYYY-MM>.html ("latest"). Preferring the dated one means a rerun for
    an older date mails that date's report rather than today's.
    """
    dated = REPORT_DIR / f"{day.isoformat()}.html"
    if dated.exists():
        return dated
    monthly = REPORT_DIR / f"{day.strftime('%Y-%m')}.html"
    return monthly if monthly.exists() else None


def _run_url() -> str:
    """Link back to the Actions run, when we are inside one."""
    repo = os.environ.get("GITHUB_REPOSITORY")
    run_id = os.environ.get("GITHUB_RUN_ID")
    if repo and run_id:
        return f"https://github.com/{repo}/actions/runs/{run_id}"
    return "(로컬 실행 — Actions 링크 없음)"


def send_failure_alert(reason: str) -> int:
    """Tell the user the report did not arrive. This is the whole point."""
    if not notify.is_configured():
        print("[alert] 알림 채널이 설정되지 않아 실패를 알릴 수 없습니다.", file=sys.stderr)
        return 1

    subject = f"[PEOS 실패] {date.today().isoformat()} 리포트가 발행되지 않았습니다"
    body = (
        f"오늘 리포트가 정상적으로 발행/전달되지 않았습니다.\n\n"
        f"사유: {reason}\n"
        f"실행 로그: {_run_url()}\n\n"
        f"이 메일이 온 날은 리포트를 신뢰하지 마십시오 — 아예 없거나 이월된 값입니다."
    )
    notify.build_channel().send(subject, body)
    print(f"[alert] 실패 알림 발송: {reason}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (기본: 오늘)")
    ap.add_argument("--allow-unconfigured", action="store_true",
                    help="채널이 없어도 성공으로 처리 (로컬 실행용)")
    ap.add_argument("--failure-alert", metavar="REASON", default=None,
                    help="리포트 대신 실패 알림을 보낸다")
    args = ap.parse_args()

    if args.failure_alert:
        return send_failure_alert(args.failure_alert)

    day = date.fromisoformat(args.date) if args.date else date.today()

    if not notify.is_configured():
        msg = ("알림 채널이 설정되지 않았습니다 "
               "(GMAIL_ADDRESS+GMAIL_APP_PASSWORD / SMTP_* / SLACK_WEBHOOK_URL 중 하나 필요)")
        if args.allow_unconfigured:
            print(f"[skip] {msg}")
            return 0
        # In CI this is a misconfiguration, not a quiet no-op: the secrets are
        # registered, so an unconfigured channel means the workflow forgot to
        # pass them through `env:`.
        print(f"[error] {msg}", file=sys.stderr)
        return 1

    report = find_report(day)
    if report is None:
        print(f"[error] {day} 리포트 파일을 찾을 수 없습니다 ({REPORT_DIR}/)", file=sys.stderr)
        return 1

    size = report.stat().st_size
    if size > MAX_ATTACHMENT_BYTES:
        print(f"[error] 리포트가 {size:,}바이트로 상한({MAX_ATTACHMENT_BYTES:,})을 넘습니다 "
              f"— 렌더러 회귀를 의심하십시오", file=sys.stderr)
        return 1

    html = report.read_text(encoding="utf-8")
    subject = f"[PEOS 리포트] {day.isoformat()}"

    try:
        notify.build_channel().send_document(subject, html, attachments=[report])
    except Exception as exc:
        # Unlike run.py's best-effort summary, a failure here must be visible —
        # this IS the delivery.
        print(f"[error] 발송 실패: {exc}", file=sys.stderr)
        return 1

    print(f"[ok] {report.name} 발송 완료 ({size:,}바이트)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
