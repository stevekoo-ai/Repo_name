"""Notification channel abstraction.

The daily pipeline always writes the dashboard to docs/ (committed to the
repo and served via GitHub Pages) — that channel has no dependency on
secrets and always runs. Push-style notifications (email/Slack) are opt-in:
implement `NoopChannel` by default, and flip to `EmailChannel` /
`SlackChannel` by setting the relevant env vars as GitHub Actions secrets.
No code elsewhere needs to change to switch channels — only
`build_channel()`'s env var check.
"""
from __future__ import annotations

import os
import smtplib
from email.mime.text import MIMEText
from typing import Protocol

import requests


class NotificationChannel(Protocol):
    def send(self, subject: str, body_text: str) -> None: ...


class NoopChannel:
    """Default: no push notification, dashboard-only delivery."""

    def send(self, subject: str, body_text: str) -> None:
        print(f"[notify:noop] {subject}\n{body_text}")


class SlackChannel:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, subject: str, body_text: str) -> None:
        requests.post(self.webhook_url, json={"text": f"*{subject}*\n{body_text}"}, timeout=10)


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
        with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
            server.login(self.user, self.password)
            server.sendmail(self.user, [self.to_addr], msg.as_string())


def build_channel() -> NotificationChannel:
    """Pick a channel based on which secrets/env vars are present.

    Precedence: Slack > Gmail > generic SMTP > Noop.
    - SLACK_WEBHOOK_URL for Slack
    - GMAIL_ADDRESS + GMAIL_APP_PASSWORD for Gmail (smtp.gmail.com:465,
      sends to itself unless NOTIFY_EMAIL_TO overrides the recipient)
    - SMTP_HOST + NOTIFY_EMAIL_TO + SMTP_USER + SMTP_PASSWORD for any other
      SMTP provider
    Add the relevant env vars as GitHub Actions secrets to enable a push
    channel without touching main.py.
    """
    slack_url = os.environ.get("SLACK_WEBHOOK_URL")
    if slack_url:
        return SlackChannel(slack_url)

    gmail_address = os.environ.get("GMAIL_ADDRESS")
    gmail_app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if gmail_address and gmail_app_password:
        return EmailChannel(
            smtp_host="smtp.gmail.com",
            smtp_port=465,
            user=gmail_address,
            password=gmail_app_password,
            to_addr=os.environ.get("NOTIFY_EMAIL_TO", gmail_address),
        )

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

    return NoopChannel()
