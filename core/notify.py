"""Notification channel abstraction, shared by every scheduled pipeline in this repo.

Each pipeline always writes its dashboard/report to docs/ or report/
(committed to the repo and served via GitHub Pages) — that channel has no
dependency on secrets and always runs. Push-style notifications (email/Slack)
are opt-in: `NoopChannel` is the default (dashboard-only delivery), and it
flips to `EmailChannel` / `SlackChannel` by setting the relevant env vars as
GitHub Actions secrets. No caller needs to change to switch channels — only
`build_channel()`'s env var check.
"""
from __future__ import annotations

import mimetypes
import os
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from pathlib import Path
from typing import Protocol

import requests


class NotificationChannel(Protocol):
    def send(self, subject: str, body_text: str) -> None: ...

    def send_document(self, subject: str, html_body: str,
                      attachments: list[Path] | None = None) -> None: ...


class NoopChannel:
    """Default: no push notification, dashboard-only delivery."""

    def send(self, subject: str, body_text: str) -> None:
        print(f"[notify:noop] {subject}\n{body_text}")

    def send_document(self, subject: str, html_body: str,
                      attachments: list[Path] | None = None) -> None:
        names = ", ".join(p.name for p in (attachments or [])) or "없음"
        print(f"[notify:noop] {subject} (html {len(html_body)}자, 첨부: {names})")


class SlackChannel:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, subject: str, body_text: str) -> None:
        requests.post(self.webhook_url, json={"text": f"*{subject}*\n{body_text}"}, timeout=10)

    def send_document(self, subject: str, html_body: str,
                      attachments: list[Path] | None = None) -> None:
        # A webhook cannot carry an HTML document or a file. Posting the raw
        # markup would be worse than useless, so send the headline only and let
        # the repo/Pages copy be the document channel.
        self.send(subject, "리포트가 생성되었습니다 (본문은 저장소의 report/ 참조).")


class EmailChannel:
    def __init__(self, smtp_host: str, smtp_port: int, user: str, password: str, to_addr: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.user = user
        self.password = password
        self.to_addr = to_addr

    def send(self, subject: str, body_text: str) -> None:
        msg = MIMEText(body_text)
        msg["Subject"] = subject
        msg["From"] = self.user
        msg["To"] = self.to_addr
        # MIMEText doesn't set these on its own. A missing Date/Message-ID is a
        # strong spam/forgery signal to receiving servers — Gmail in particular
        # has been observed to accept (250 OK) a header-bare self-to-self message
        # over SMTP and then silently drop it rather than deliver or spam-file it,
        # which looks identical to success from the sending side.
        msg["Date"] = formatdate(localtime=False)
        msg["Message-ID"] = make_msgid(domain=self.user.rpartition("@")[2] or None)
        self._deliver(msg.as_string())

    def send_document(self, subject: str, html_body: str,
                      attachments: list[Path] | None = None) -> None:
        """Send the report itself: HTML in the body, plus the file attached.

        The body is what makes this useful on a phone — the reader should not
        have to download anything to see the report. The attachment is the
        archival copy, and the reason both are sent is that mail clients differ
        wildly in what HTML they will render.
        """
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.user
        msg["To"] = self.to_addr
        msg["Date"] = formatdate(localtime=False)
        msg["Message-ID"] = make_msgid(domain=self.user.rpartition("@")[2] or None)

        # A text/plain alternative is not decoration: clients that refuse the
        # HTML part fall back to this, and its absence is itself a spam signal.
        msg.set_content("이 메일은 HTML 리포트입니다. HTML을 지원하는 클라이언트에서 열어주세요.")
        msg.add_alternative(html_body, subtype="html")

        for path in attachments or []:
            ctype, _ = mimetypes.guess_type(path.name)
            maintype, _, subtype = (ctype or "application/octet-stream").partition("/")
            msg.add_attachment(path.read_bytes(), maintype=maintype,
                               subtype=subtype or "octet-stream", filename=path.name)

        self._deliver(msg.as_string())

    def _deliver(self, raw: str) -> None:
        with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
            server.login(self.user, self.password)
            server.sendmail(self.user, [self.to_addr], raw)


def build_channel() -> NotificationChannel:
    """Pick a channel based on which secrets/env vars are present.

    Precedence: Slack > generic SMTP > Gmail > Noop.

    - SLACK_WEBHOOK_URL alone enables Slack.
    - SMTP_HOST + SMTP_USER + SMTP_PASSWORD + NOTIFY_EMAIL_TO enables a
      generic SMTP server.
    - GMAIL_ADDRESS + GMAIL_APP_PASSWORD enables Gmail specifically (smtp.gmail.com,
      SSL/465) — this repo's other pipelines (sk-hynix-daily-report.yml,
      subscription-monitor.yml) already register these two secrets against a
      real Gmail account, so this reuses that instead of asking for a second,
      redundant set of SMTP_* secrets. Recipient defaults to GMAIL_ADDRESS
      itself (send-to-self) unless NOTIFY_EMAIL_TO overrides it.

    Add the relevant env vars as GitHub Actions secrets to enable a push
    channel without touching any caller.
    """
    slack_url = os.environ.get("SLACK_WEBHOOK_URL")
    if slack_url:
        return SlackChannel(slack_url)

    smtp_host = os.environ.get("SMTP_HOST")
    to_addr = os.environ.get("NOTIFY_EMAIL_TO")
    if smtp_host and to_addr:
        return EmailChannel(
            smtp_host=smtp_host,
            smtp_port=int(os.environ.get("SMTP_PORT", "465")),
            user=os.environ["SMTP_USER"],
            password=os.environ["SMTP_PASSWORD"],
            to_addr=to_addr,
        )

    gmail_addr = os.environ.get("GMAIL_ADDRESS")
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD")
    if gmail_addr and gmail_password:
        return EmailChannel(
            smtp_host="smtp.gmail.com",
            smtp_port=465,
            user=gmail_addr,
            password=gmail_password,
            to_addr=to_addr or gmail_addr,
        )

    return NoopChannel()


def is_configured() -> bool:
    """Whether a real push channel exists, as opposed to the no-op default.

    Callers need this to tell two very different outcomes apart: "nothing was
    sent because no channel is configured" (fine locally, a misconfiguration in
    CI) and "a channel exists and sending failed" (always an incident). Treating
    both as success is how three days of reports went missing unnoticed.
    """
    return not isinstance(build_channel(), NoopChannel)
