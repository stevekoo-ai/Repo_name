"""
Detects 용인 플랫폼시티 및 광교신도시 공공분양 listings among already-fetched rows
and fires alerts (GitHub Issue + email) exactly once per unique listing.

State (which listings have already been alerted) is persisted to
alerted_state.json so repeated runs don't re-notify for the same listing.
"""

import json
import os
import smtplib
import urllib.request
from email.mime.text import MIMEText

STATE_PATH = os.path.join(os.path.dirname(__file__), "alerted_state.json")
HEALTH_STATE_PATH = os.path.join(os.path.dirname(__file__), "health_state.json")
# 광교신도시 공공분양은 "광교"가 정식 명칭/주소에 없는 경우도 있어(예: 원천동 80번지
# 일원 600세대 공공분양 — 2026-07-23 사용자 제보, 청약홈 미등록 확인됨) "원천동"도 함께
# 감지한다. See docs/LESSON_LEARNED_API_DEBUGGING.md for the keyword-matching lessons.
ALERT_KEYWORDS = ["플랫폼시티", "광교", "원천동"]
DASHBOARD_URL = "https://stevekoo-ai.github.io/Repo_name/subscription-monitor.html"

FAILURE_THRESHOLD = 6  # 6 consecutive 5-minute failures = ~30 minutes of no data
HEARTBEAT_HOUR_KST = 9  # send the daily "still alive" heartbeat on the first successful run at/after this hour


def load_state() -> set:
    if not os.path.exists(STATE_PATH):
        save_state(set())
        return set()
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_state(ids: set) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(ids), f, ensure_ascii=False, indent=2)


def find_matches(rows: list, extra_keyword: str | None) -> list[tuple[dict, str]]:
    """Returns (row, matched_keyword) pairs so alerts can say which keyword fired."""
    keywords = list(ALERT_KEYWORDS)
    if extra_keyword:
        keywords.append(extra_keyword)
    matches = []
    for r in rows:
        haystack = f"{r.get('HOUSE_NM', '')} {r.get('HSSPLY_ADRES', '')}"
        matched_kw = next((kw for kw in keywords if kw in haystack), None)
        if matched_kw:
            matches.append((r, matched_kw))
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


def format_alert(r: dict, matched_keyword: str, is_test: bool) -> tuple:
    name = r.get("HOUSE_NM") or "(이름없음)"
    prefix = "[테스트] " if is_test else ""
    title = f"{prefix}[청약 알림 · {matched_keyword}] {name}"
    lines = [
        "테스트 알림입니다 (실제 매물이 아닙니다).\n" if is_test else "",
        f"매칭 키워드: {matched_keyword}",
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
    """Checks rows for 플랫폼시티/광교 matches and fires alerts for any not seen before.
    Returns the number of new alerts fired."""
    state = load_state()  # also ensures alerted_state.json exists on disk

    extra_keyword = os.environ.get("EXTRA_TEST_KEYWORD") or None
    is_test = bool(extra_keyword)
    matches = find_matches(rows, extra_keyword)
    if not matches:
        return 0

    new_matches = [(m, kw) for m, kw in matches if (m.get("HOUSE_MANAGE_NO") or m.get("PBLANC_NO")) not in state]
    if not new_matches:
        return 0

    repo_full_name = os.environ.get("GITHUB_REPOSITORY")
    gh_token = os.environ.get("GITHUB_TOKEN")
    gmail_addr = os.environ.get("GMAIL_ADDRESS")
    gmail_pw = os.environ.get("GMAIL_APP_PASSWORD")
    to_addr = os.environ.get("ALERT_EMAIL_TO") or gmail_addr or ""

    for m, kw in new_matches:
        title, body = format_alert(m, kw, is_test)

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

    state |= {(m.get("HOUSE_MANAGE_NO") or m.get("PBLANC_NO")) for m, kw in new_matches}
    save_state(state)
    return len(new_matches)


def load_health_state() -> dict:
    default = {"consecutive_failures": 0, "outage_alerted": False, "last_heartbeat_date": None}
    if not os.path.exists(HEALTH_STATE_PATH):
        save_health_state(default)
        return default
    with open(HEALTH_STATE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {**default, **data}


def save_health_state(state: dict) -> None:
    with open(HEALTH_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _notify(title: str, body: str, gh_token, repo_full_name, gmail_addr, gmail_pw, to_addr, also_issue: bool) -> None:
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


def run_health_monitor(healthy: bool, now_kst, seoul_gyeonggi_count: int) -> None:
    """Tracks API health across runs and sends:
    - an outage alert (Issue + email) after FAILURE_THRESHOLD consecutive unhealthy runs
    - a recovery notice (email) once it comes back
    - one daily "still alive" heartbeat email regardless of match activity
    """
    state = load_health_state()
    repo_full_name = os.environ.get("GITHUB_REPOSITORY")
    gh_token = os.environ.get("GITHUB_TOKEN")
    gmail_addr = os.environ.get("GMAIL_ADDRESS")
    gmail_pw = os.environ.get("GMAIL_APP_PASSWORD")
    to_addr = os.environ.get("ALERT_EMAIL_TO") or gmail_addr or ""
    now_str = now_kst.strftime("%Y-%m-%d %H:%M KST")

    if not healthy:
        state["consecutive_failures"] += 1
        if state["consecutive_failures"] >= FAILURE_THRESHOLD and not state["outage_alerted"]:
            title = "⚠ 청약 모니터 API 응답 이상 지속 중"
            body = (
                f"청약Home API가 {FAILURE_THRESHOLD}회 연속(약 30분 이상) 정상 응답하지 않고 있습니다.\n"
                f"마지막 확인 시각: {now_str}\n\n"
                f"페이지({DASHBOARD_URL})의 '마지막 갱신' 시각이 이 시점보다 많이 오래됐다면 실제 장애입니다.\n"
                "data.go.kr 마이페이지에서 활용현황을 확인해보세요."
            )
            _notify(title, body, gh_token, repo_full_name, gmail_addr, gmail_pw, to_addr, also_issue=True)
            state["outage_alerted"] = True
        save_health_state(state)
        return

    if state["outage_alerted"]:
        title = "✅ 청약 모니터 정상 복구됨"
        body = f"API 응답이 다시 정상화됐습니다.\n복구 확인 시각: {now_str}"
        _notify(title, body, gh_token, repo_full_name, gmail_addr, gmail_pw, to_addr, also_issue=False)

    state["consecutive_failures"] = 0
    state["outage_alerted"] = False

    today_str = now_kst.strftime("%Y-%m-%d")
    if now_kst.hour >= HEARTBEAT_HOUR_KST and state.get("last_heartbeat_date") != today_str:
        title = f"청약 모니터 정상 작동 중 ({today_str})"
        body = (
            "매일 발송되는 상태 확인 메일입니다. 이 메일이 계속 온다면 시스템이 정상 작동 중이라는 뜻입니다.\n\n"
            f"마지막 갱신: {now_str}\n"
            f"현재 서울·경기 국민주택 매칭: {seoul_gyeonggi_count}건\n"
            f"감지 키워드: {', '.join(ALERT_KEYWORDS)}\n"
            "플랫폼시티/광교신도시 신규 알림: 있었다면 이미 별도 메일/Issue로 받으셨을 것입니다.\n\n"
            f"대시보드: {DASHBOARD_URL}"
        )
        _notify(title, body, gh_token, repo_full_name, gmail_addr, gmail_pw, to_addr, also_issue=False)
        state["last_heartbeat_date"] = today_str

    save_health_state(state)
