"""
Detects 용인 플랫폼시티 공공분양 listings among already-fetched rows and fires
alerts (GitHub Issue + email) exactly once per unique listing.

State (which listings have already been alerted) is persisted to
alerted_state.json so repeated runs don't re-notify for the same listing.
"""

import json
import os
import smtplib
import urllib.request
from email.mime.text import MIMEText

STATE_PATH = os.path.join(os.path.dirname(__file__), "alerted_state.json")
PLATFORM_CITY_KEYWORDS = ["플랫폼시티"]


def load_state() -> set:
    if not os.path.exists(STATE_PATH):
        save_state(set())
        return set()
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_state(ids: set) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(ids), f, ensure_ascii=False, indent=2)


def find_matches(rows: list, extra_keyword: str | None) -> list:
    keywords = list(PLATFORM_CITY_KEYWORDS)
    if extra_keyword:
        keywords.append(extra_keyword)
    matches = []
    for r in rows:
        haystack = f"{r.get('HOUSE_NM', '')} {r.get('HSSPLY_ADRES', '')}"
        if any(kw in haystack for kw in keywords):
            matches.append(r)
    return matches


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
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
        server.starttls()
        server.login(gmail_addr, gmail_app_password)
        server.sendmail(gmail_addr, [to_addr], msg.as_string())


def format_alert(r: dict, is_test: bool) -> tuple:
    name = r.get("HOUSE_NM") or "(이름없음)"
    prefix = "[테스트] " if is_test else ""
    title = f"{prefix}[플랫폼시티 알림] {name}"
    lines = [
        "테스트 알림입니다 (실제 플랫폼시티 매물이 아닙니다).\n" if is_test else "",
        f"단지명: {name}",
        f"지역: {r.get('SUBSCRPT_AREA_CODE_NM', '-')}",
        f"주소: {r.get('HSSPLY_ADRES', '-')}",
        f"주택구분: {r.get('HOUSE_DTL_SECD_NM', '-')}",
        f"일반공급 접수기간: {r.get('RCEPT_BGNDE', '-')} ~ {r.get('RCEPT_ENDDE', '-')}",
        f"당첨자 발표: {r.get('PRZWNER_PRESNATN_DE', '-')}",
        f"총 세대수: {r.get('TOT_SUPLY_HSHLDCO', '-')}",
        f"청약홈 링크: {r.get('PBLANC_URL', '-')}",
    ]
    body = "\n".join(line for line in lines if line != "" or True)
    return title, body


def run_alerts(rows: list) -> int:
    """Checks rows for 플랫폼시티 matches and fires alerts for any not seen before.
    Returns the number of new alerts fired."""
    state = load_state()  # also ensures alerted_state.json exists on disk

    extra_keyword = os.environ.get("EXTRA_TEST_KEYWORD") or None
    is_test = bool(extra_keyword)
    matches = find_matches(rows, extra_keyword)
    if not matches:
        return 0

    new_matches = [m for m in matches if (m.get("HOUSE_MANAGE_NO") or m.get("PBLANC_NO")) not in state]
    if not new_matches:
        return 0

    repo_full_name = os.environ.get("GITHUB_REPOSITORY")
    gh_token = os.environ.get("GITHUB_TOKEN")
    gmail_addr = os.environ.get("GMAIL_ADDRESS")
    gmail_pw = os.environ.get("GMAIL_APP_PASSWORD")
    to_addr = os.environ.get("ALERT_EMAIL_TO") or gmail_addr or ""

    for m in new_matches:
        title, body = format_alert(m, is_test)

        if gh_token and repo_full_name:
            try:
                create_github_issue(repo_full_name, gh_token, title, body)
                print(f"created github issue: {title}")
            except Exception as e:
                print(f"github issue failed: {e}")
        else:
            print("GITHUB_TOKEN/GITHUB_REPOSITORY not set, skipping issue")

        if gmail_addr and gmail_pw and to_addr:
            try:
                send_email(to_addr, gmail_addr, gmail_pw, title, body)
                print(f"sent email: {title}")
            except Exception as e:
                print(f"email failed: {e}")
        else:
            print("email secrets not configured, skipping email")

    state |= {(m.get("HOUSE_MANAGE_NO") or m.get("PBLANC_NO")) for m in new_matches}
    save_state(state)
    return len(new_matches)
