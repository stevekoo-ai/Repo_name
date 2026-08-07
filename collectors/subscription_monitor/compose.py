"""
Step 3-4 of the subscription-monitor autonomous pipeline: COMPOSE + RENDER email.

Takes judged verdicts (from judge.py) + API health, decides WHICH messages to
send (Step 3 — the "의미있을 때 + 일일 요약" policy) and composes each message
body (Step 4). Step 5 (actual send) is delegated to the low-level helpers in
alerts.py (send_email / create_github_issue) which already handle Gmail SMTP,
GitHub Issues, and the Date/Message-ID anti-silent-drop fix.

Send-event taxonomy (in priority order):
  NEW_MATCH     — a listing matching an alert keyword we haven't notified yet. → email + issue, immediate
  PRIORITY_UP   — an already-known listing's priority rose (e.g. reception D-1 arrived). → email only, immediate
  OUTAGE        — API unhealthy for FAILURE_THRESHOLD consecutive runs. → email + issue, immediate (existing)
  RECOVERY      — API came back after an outage. → email only, immediate (existing)
  DAILY_DIGEST  — once per day, first healthy run at/after HEARTBEAT_HOUR_KST. → email only. The
                   "조사 결과를 꼭 email로 받는다" channel — always sends a summary even with no matches.

State files (migrated from alerts.py):
  alerted_state.json  — was a bare list of ids. Now an object map {id: {"priority": "...", "keyword": ...}}
                        for PRIORITY_UP tracking. Loader is backward-compatible (a bare list is read as
                        {id: {}}). Writer always emits the new shape.
  health_state.json   — structure unchanged; last_heartbeat_date renamed in spirit to last_digest_date
                        (field kept as last_heartbeat_date for backward-compat with existing files).
"""

import json
import os
from datetime import datetime

import alerts
from judge import judge_listings, summarize, ALERT_KEYWORDS, MY_ACCOUNT_SCORE

FAILURE_THRESHOLD = 6  # 6 consecutive 5-min failures ≈ 30 min of no data (matches alerts.py)
HEARTBEAT_HOUR_KST = 9  # daily digest on first healthy run at/after this hour

STATE_PATH = os.path.join(os.path.dirname(__file__), "alerted_state.json")
HEALTH_STATE_PATH = os.path.join(os.path.dirname(__file__), "health_state.json")


# ---------------------------------------------------------------------------
# State (migrated, backward-compatible)
# ---------------------------------------------------------------------------

def load_alerted_state() -> dict:
    """Returns {id: {"priority": str|None, "keyword": str|None}}.
    Backward-compat: a legacy bare list ["id1","id2"] is read as {"id1":{}, "id2":{}}."""
    if not os.path.exists(STATE_PATH):
        return {}
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return {i: {} for i in data}
    return data


def save_alerted_state(state: dict) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


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


# ---------------------------------------------------------------------------
# Message body composition (Step 4) — deterministic templates, no LLM
# ---------------------------------------------------------------------------

def _listing_detail_lines(v: dict) -> list[str]:
    r = v["row"]
    return [
        f"단지명: {v['name']}",
        f"지역: {v.get('region', '-')}",
        f"주소: {r.get('HSSPLY_ADRES', '-')}",
        f"주택구분: {r.get('HOUSE_DTL_SECD_NM', '-')}",
        f"일반공급 접수기간: {r.get('RCEPT_BGNDE', '-')} ~ {r.get('RCEPT_ENDDE', '-')}",
        f"당첨자 발표: {r.get('PRZWNER_PRESNATN_DE', '-')}",
        f"총 세대수: {r.get('TOT_SUPLY_HSHLDCO', '-')}",
        f"청약홈 링크: {r.get('PBLANC_URL', '-')}",
        f"▶ 판단: {v['reason']}",
        f"▶ 권장행동: {v['recommended_action']} (우선순위 {v['priority']})",
    ]


def compose_new_match(v: dict, is_test: bool) -> tuple[str, str]:
    prefix = "[테스트] " if is_test else ""
    title = f"{prefix}[청약 알림 · {v['match_keyword']}] {v['name']}"
    head = "테스트 알림입니다 (실제 매물이 아닙니다).\n" if is_test else ""
    lines = [head, *_listing_detail_lines(v)]
    return title, "\n".join(l for l in lines if l != "" or True)


def compose_priority_up(v: dict) -> tuple[str, str]:
    title = f"[청약 알림 · 우선순위 상승] {v['name']}"
    lines = [
        f"이미 추적 중인 매물의 우선순위가 {v['priority']}로 상승했습니다 (접수 임박 등).",
        "",
        *_listing_detail_lines(v),
    ]
    return title, "\n".join(lines)


def compose_outage(now_str: str) -> tuple[str, str]:
    title = "⚠ 청약 모니터 API 응답 이상 지속 중"
    body = (
        f"청약Home API가 {FAILURE_THRESHOLD}회 연속(약 30분 이상) 정상 응답하지 않고 있습니다.\n"
        f"마지막 확인 시각: {now_str}\n\n"
        f"페이지({alerts.DASHBOARD_URL})의 '마지막 갱신' 시각이 이 시점보다 많이 오래됐다면 실제 장애입니다.\n"
        "data.go.kr 마이페이지에서 활용현황을 확인해보세요."
    )
    return title, body


def compose_recovery(now_str: str) -> tuple[str, str]:
    title = "✅ 청약 모니터 정상 복구됨"
    body = f"API 응답이 다시 정상화됐습니다.\n복구 확인 시각: {now_str}"
    return title, body


def compose_daily_digest(verdicts: list[dict], summary: dict, now_str: str, today_str: str) -> tuple[str, str]:
    title = f"청약 모니터 일일 요약 ({today_str})"
    lines = [
        "매일 발송되는 조사 결과 요약입니다. 이 메일이 계속 온다면 시스템이 정상 작동 중이라는 뜻입니다.",
        "",
        f"마지막 조사: {now_str}",
        f"내 청약통장 점수: {MY_ACCOUNT_SCORE}/40 (가입일 2005-11-03, 249회, 최고액 납입)",
        "",
        "── 오늘 조사 결과 ──",
        f"서울·경기 국민주택 접수 중/예정: {summary['total']}건",
        f"우선순위 분포: HIGH {summary['high']} / MED {summary['med']} / LOW {summary['low']}",
    ]

    # 접수 임박(D-3 이내) 매물
    if summary["imminent"]:
        lines.append("")
        lines.append(f"── 접수 임박 (D-{3} 이내, {summary['imminent_count']}건) ──")
        for v in summary["imminent"]:
            d = v["days_to_open"]
            dtag = f"D-{d}" if d is not None and d > 0 else ("오늘" if d == 0 else "진행중")
            kw = f" [{v['match_keyword']}]" if v["match_keyword"] else ""
            lines.append(f"• {v['name']} ({v['region']}, {dtag}, {v['priority']}){kw}")
    else:
        lines.append("접수 임박 매물: 없음")

    # HIGH 우선순위 매물 전체 (있으면)
    high = [v for v in verdicts if v["priority"] == "HIGH"]
    if high:
        lines.append("")
        lines.append(f"── HIGH 우선순위 ({len(high)}건) ──")
        for v in high:
            kw = f" [{v['match_keyword']}]" if v["match_keyword"] else ""
            lines.append(f"• {v['name']} ({v['region']}){kw} — {v['reason']}")

    lines += [
        "",
        f"감지 키워드: {', '.join(ALERT_KEYWORDS)}",
        "신규 매칭(플랫폼시티/광교/원천동)이 있었다면 별도 즉시 알림을 이미 받으셨을 것입니다.",
        f"대시보드: {alerts.DASHBOARD_URL}",
    ]
    return title, "\n".join(lines)


# ---------------------------------------------------------------------------
# Send dispatch (Step 5 delegation) + policy (Step 3)
# ---------------------------------------------------------------------------

def _env_creds():
    return (
        os.environ.get("GITHUB_REPOSITORY"),
        os.environ.get("GITHUB_TOKEN"),
        os.environ.get("GMAIL_ADDRESS"),
        os.environ.get("GMAIL_APP_PASSWORD"),
        os.environ.get("ALERT_EMAIL_TO") or os.environ.get("GMAIL_ADDRESS") or "",
    )


def _send(title: str, body: str, also_issue: bool) -> None:
    repo, gh_token, gmail_addr, gmail_pw, to_addr = _env_creds()
    alerts._notify(title, body, gh_token, repo, gmail_addr, gmail_pw, to_addr, also_issue=also_issue)


def run_pipeline(verdicts: list[dict], healthy: bool, now_kst: datetime, seoul_gyeonggi_count: int) -> dict:
    """The full compose step. Mutates alerted_state.json + health_state.json.
    Returns a report dict of what fired (for logging)."""
    repo, gh_token, gmail_addr, gmail_pw, to_addr = _env_creds()
    now_str = now_kst.strftime("%Y-%m-%d %H:%M KST")
    today_str = now_kst.strftime("%Y-%m-%d")

    fired = {"new_match": 0, "priority_up": 0, "outage": False, "recovery": False, "digest": False}
    extra_keyword = os.environ.get("EXTRA_TEST_KEYWORD") or None
    is_test = bool(extra_keyword)

    # --- OUTAGE / RECOVERY path (API unhealthy) ---
    health = load_health_state()
    if not healthy:
        health["consecutive_failures"] += 1
        if health["consecutive_failures"] >= FAILURE_THRESHOLD and not health["outage_alerted"]:
            title, body = compose_outage(now_str)
            _send(title, body, also_issue=True)
            health["outage_alerted"] = True
            fired["outage"] = True
        save_health_state(health)
        return fired

    if health["outage_alerted"]:
        title, body = compose_recovery(now_str)
        _send(title, body, also_issue=False)
        fired["recovery"] = True
    health["consecutive_failures"] = 0
    health["outage_alerted"] = False

    # --- NEW_MATCH + PRIORITY_UP (API healthy) ---
    state = load_alerted_state()
    for v in verdicts:
        lid = v["id"]
        if not lid:
            continue
        prev = state.get(lid)
        # NEW_MATCH: keyword-matched listing we've never notified.
        if v["match_keyword"] and (prev is None or not prev.get("notified")):
            title, body = compose_new_match(v, is_test)
            _send(title, body, also_issue=True)
            state[lid] = {"priority": v["priority"], "keyword": v["match_keyword"], "notified": True}
            fired["new_match"] += 1
            continue
        # PRIORITY_UP: known listing whose priority rose since last we saw it.
        if prev is not None and v["priority"] == "HIGH" and prev.get("priority") != "HIGH":
            title, body = compose_priority_up(v)
            _send(title, body, also_issue=False)
            state[lid] = {**prev, "priority": v["priority"], "keyword": v["match_keyword"]}
            fired["priority_up"] += 1
            continue
        # Otherwise just update our record of its current priority.
        if prev is not None:
            state[lid] = {**prev, "priority": v["priority"], "keyword": v["match_keyword"]}
        else:
            state[lid] = {"priority": v["priority"], "keyword": v["match_keyword"]}
    save_alerted_state(state)

    # --- DAILY_DIGEST (heartbeat) ---
    if now_kst.hour >= HEARTBEAT_HOUR_KST and health.get("last_heartbeat_date") != today_str:
        summary = summarize(verdicts)
        title, body = compose_daily_digest(verdicts, summary, now_str, today_str)
        _send(title, body, also_issue=False)
        health["last_heartbeat_date"] = today_str
        fired["digest"] = True

    save_health_state(health)
    return fired
