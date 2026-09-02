"""Deliver the daily 청약 리포트 by email — and say so loudly when it fails.

Same delivery principle as scripts/send_report_email.py (PEOS): generation may
swallow errors, delivery must not. engine.report.subscription_report.run()
only writes report/subscription-report-<date>.md; this script is the loud
half — it sends that file's content as the email body and exits non-zero if
delivery fails, so the workflow can surface it.

Unlike the PEOS report (HTML body + attachment), this one is plain text —
the whole point of splitting it out was to keep it light, and the SK Hynix
3x-daily report already established the precedent of mailing a raw .md body
directly.

    python -m scripts.send_subscription_report_email                # today's report
    python -m scripts.send_subscription_report_email --date 2026-09-02
    python -m scripts.send_subscription_report_email --allow-unconfigured   # local dry run
    python -m scripts.send_subscription_report_email --failure-alert "무엇이 실패했는지"

TRACK BOUNDARY (wiki/concepts/automation-strategy-and-delivery-boundary.md)
This sends housing/subscription judgment reports only — 트랙 A.
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


def find_report(day: date) -> Path | None:
    path = REPORT_DIR / f"subscription-report-{day.isoformat()}.md"
    return path if path.exists() else None


def _run_url() -> str:
    repo = os.environ.get("GITHUB_REPOSITORY")
    run_id = os.environ.get("GITHUB_RUN_ID")
    if repo and run_id:
        return f"https://github.com/{repo}/actions/runs/{run_id}"
    return "(로컬 실행 — Actions 링크 없음)"


def send_failure_alert(reason: str) -> int:
    if not notify.is_configured():
        print("[alert] 알림 채널이 설정되지 않아 실패를 알릴 수 없습니다.", file=sys.stderr)
        return 1

    subject = f"[청약 리포트 실패] {date.today().isoformat()} 리포트가 발행되지 않았습니다"
    body = (
        f"오늘 청약 리포트가 정상적으로 발행/전달되지 않았습니다.\n\n"
        f"사유: {reason}\n"
        f"실행 로그: {_run_url()}\n\n"
        f"이 메일이 온 날은 청약 우려사항/부동산 동향을 신뢰하지 마십시오 — 이월된 값이거나 없습니다."
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
        print(f"[error] {msg}", file=sys.stderr)
        return 1

    report = find_report(day)
    if report is None:
        print(f"[error] {day} 청약 리포트 파일을 찾을 수 없습니다 ({REPORT_DIR}/)", file=sys.stderr)
        return 1

    content = report.read_text(encoding="utf-8")

    # 첫 줄("# 청약 리포트 — 2026-09-02")은 제목에 이미 들어가니 본문에서는 그대로
    # 두고, 우려사항 headline까지 제목에 함께 실어 받은 사람이 열지 않고도 급한지
    # 알 수 있게 한다 — engine.report.subscription_report.email_subject()와
    # 동일 계산을 다시 하지 않도록 리포트 첫 줄 다음의 headline 줄을 그대로 찾는다.
    headline_line = next((l for l in content.splitlines() if l.startswith("**")), "").strip("*")
    subject = f"[청약 리포트] {day.isoformat()}" + (f" — {headline_line}" if headline_line else "")

    try:
        notify.build_channel().send(subject, content)
    except Exception as exc:
        print(f"[error] 발송 실패: {exc}", file=sys.stderr)
        return 1

    print(f"[ok] {report.name} 발송 완료 ({len(content):,}자)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
