"""
Low-level send primitives for the subscription-monitor pipeline.

The 5-step autonomous pipeline (judge.py -> compose.py) calls these to actually
deliver a message (Step 5). All send *policy* (which messages to send, when,
how often) lives in compose.py now; this module is just the transport layer:

  - send_email          Gmail SMTP (with Date/Message-ID anti-silent-drop fix)
  - create_github_issue GitHub Issues API
  - _notify             convenience wrapper that does both, gated by also_issue

DASHBOARD_URL is re-exported here so compose.py can reference it without owning
it. ALERT_KEYWORDS moved to judge.py (single source of truth, shared with
fetch_and_render.py).
"""

import json
import os
import smtplib
import urllib.request
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

DASHBOARD_URL = "https://stevekoo-ai.github.io/Repo_name/subscription-monitor.html"


def create_github_issue(repo_full_name: str, token: str, title: str, body: str) -> None:
    url = f"https://api.github.com/repos/{repo_full_name}/issues"
    payload = json.dumps({"title": title, "body": body}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "subscription-monitor",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        resp.read()


def send_email(to_addr: str, gmail_addr: str, gmail_app_password: str, subject: str, body: str) -> None:
    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = gmail_addr
    msg["To"] = to_addr
    # A missing Date/Message-ID is a spam/forgery signal. Gmail has been observed to
    # accept (250 OK) a header-bare self-to-self message and then silently drop it
    # rather than deliver or spam-file it (see core/notify.py for the same fix + why).
    msg["Date"] = formatdate(localtime=False)
    msg["Message-ID"] = make_msgid(domain=gmail_addr.rpartition("@")[2] or None)
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
        server.starttls()
        server.login(gmail_addr, gmail_app_password)
        server.sendmail(gmail_addr, [to_addr], msg.as_string())


def _notify(title: str, body: str, gh_token, repo_full_name, gmail_addr, gmail_pw, to_addr, also_issue: bool) -> None:
    """Send a message via email (always) and GitHub Issue (only if also_issue).
    Failures are logged to stdout but never raised. One transport failing must
    not block the other or the next pipeline step."""
    if also_issue and gh_token and repo_full_name:
        try:
            create_github_issue(repo_full_name, gh_token, title, body)
            print(f"created github issue: {title}")
        except Exception as e:
            print(f"github issue failed: {e}")
    if gmail_addr and gmail_pw and to_addr:
        try:
            send_email(to_addr, gmail_addr, gmail_pw, title, body)
            print(f"sent email: {title}")
        except Exception as e:
            print(f"email failed: {e}")
    elif also_issue and gh_token and repo_full_name:
        # Nothing else fired. Make it visible that email was skipped (misconfig).
        print("email secrets not configured, skipping email")
