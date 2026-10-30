"""
청약 감시 그물망 — data.go.kr API 바깥의 2·3·4차 경로.

2026-10-30 광교 자연앤 센트레빌(A17BL) 누락의 근본원인은 data.go.kr Open API가
공고를 아직 동기화하지 않은 것이었다(같은 날 청약Home 웹사이트·GH 게시판·뉴스엔
이미 게시됨 — Actions 러너에서 실측 확인). API 한 경로에만 의존하면 이 공백이
구조적으로 반복되므로, 독립된 경로를 겹쳐 둔다:

  ② applyhome  청약Home 웹 APT 분양정보 목록 (공고일 당일 게시 확인)
  ③ gh         GH(경기주택도시공사) 분양/임대 공고 게시판 (사업주체 직접)
  ④ news       구글뉴스 RSS — 공식 채널이 모두 실패할 때의 최후 백업

각 경로는 서로 독립적으로 실패한다(try/except). 키워드(judge.ALERT_KEYWORDS)
매칭 건이 처음 보이면 즉시 메일+이슈. 한 경로가 연속 실패하면 "그물 구멍"
경보를 따로 보낸다 — 조용히 꺼진 그물은 없는 것과 같다.

DRY_RUN=1이면 발송·상태저장 없이 결과만 출력한다(디버그 브랜치 실측용).
"""

import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

sys.path.insert(0, os.path.dirname(__file__))
from judge import ALERT_KEYWORDS  # noqa: E402
import alerts  # noqa: E402

KST = timezone(timedelta(hours=9))
STATE_PATH = os.path.join(os.path.dirname(__file__), "net_state.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

APPLYHOME_LIST_URL = "https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancListView.do"
APPLYHOME_DETAIL_HINT = "https://www.applyhome.co.kr (APT 분양정보 → 주택관리번호 {id})"
GH_URLS = ["https://www.gh.or.kr/gh/announcement-of-salerental001.do", "https://www.gh.or.kr/"]
GH_BASE = "https://www.gh.or.kr"
NEWS_QUERIES = [f"{kw} 공공분양" for kw in ALERT_KEYWORDS] + [f"{kw} 입주자모집공고" for kw in ALERT_KEYWORDS]
NEWS_CONTEXT_WORDS = ("공공분양", "입주자모집", "입주자 모집", "모집공고", "청약")
NEWS_MAX_AGE_DAYS = 3
# 뉴스는 백업 경로다 — 같은 키워드를 공식 경로(②③ 또는 API)가 최근 이미
# 잡았다면 기사마다 메일을 보내지 않는다(광교 기사 수십 건 → 수십 통 방지).
NEWS_SUPPRESS_IF_OFFICIAL_WITHIN_DAYS = 30
HOLE_ALERT_AFTER_FAILURES = 6   # 30분 주기 × 6 = 약 3시간 연속 실패 시 경보

SOURCE_LABELS = {
    "applyhome": "② 청약Home 웹 목록",
    "gh": "③ GH 분양공고 게시판",
    "news": "④ 뉴스(구글뉴스 RSS)",
}


def _get(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ko-KR,ko"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def match_keyword(text: str) -> str | None:
    return next((kw for kw in ALERT_KEYWORDS if kw in (text or "")), None)


# --- ② 청약Home 웹 목록 -------------------------------------------------------

_APPLYHOME_ROW = re.compile(
    r'<tr\s+data-pbno="(?P<pbno>[^"]*)"\s+data-hmno="(?P<hmno>[^"]*)"\s+data-honm="(?P<honm>[^"]*)"[^>]*>(?P<body>.*?)</tr>',
    re.S)
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def parse_applyhome(page_html: str) -> list[dict]:
    """청약Home APT 분양정보 목록 HTML → 공고 행 목록.
    행 순서: 지역, 주택구분(국민/민영), 분양/임대, 주택명, 시공사, 문의처,
    모집공고일, 청약기간(시작~끝), 당첨자발표 …"""
    rows = []
    for m in _APPLYHOME_ROW.finditer(page_html):
        cells = [_strip_tags(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", m.group("body"), re.S)]
        dates = _DATE.findall(_strip_tags(m.group("body")))
        rows.append({
            "id": m.group("hmno") or m.group("pbno"),
            "name": html.unescape(m.group("honm")),
            "region": cells[0] if len(cells) > 0 else "",
            "house_type": cells[1] if len(cells) > 1 else "",
            "announce_date": dates[0] if len(dates) > 0 else "",
            "rcept_begin": dates[1] if len(dates) > 1 else "",
            "rcept_end": dates[2] if len(dates) > 2 else "",
            "winner_date": dates[3] if len(dates) > 3 else "",
        })
    return rows


def applyhome_hits(rows: list[dict]) -> list[dict]:
    hits = []
    for r in rows:
        kw = match_keyword(r["name"])
        if kw:
            hits.append({
                "key": f"hm:{r['id']}",
                "source": "applyhome",
                "keyword": kw,
                "title": r["name"],
                "detail": (f"{r['region']} · {r['house_type']} · 공고 {r['announce_date']} · "
                           f"청약 {r['rcept_begin']}~{r['rcept_end']} · 당첨발표 {r['winner_date']}"),
                "url": APPLYHOME_DETAIL_HINT.format(id=r["id"]),
                "house_manage_no": r["id"],
            })
    return hits


# --- ③ GH 분양/임대 공고 게시판 ------------------------------------------------

_GH_ANCHOR = re.compile(
    r'<a[^>]+href="(?P<href>/gh/announcement-of-salerental001\.do\?mode=view&(?:amp;)?articleNo=(?P<no>\d+))"[^>]*>(?P<text>.*?)</a>',
    re.S)


def parse_gh(page_html: str) -> list[dict]:
    items, seen = [], set()
    for m in _GH_ANCHOR.finditer(page_html):
        no = m.group("no")
        title = _strip_tags(m.group("text"))
        if not title or no in seen:
            continue
        seen.add(no)
        items.append({"no": no, "title": title, "url": GH_BASE + html.unescape(m.group("href"))})
    return items


def gh_hits(items: list[dict]) -> list[dict]:
    hits = []
    for it in items:
        kw = match_keyword(it["title"])
        # 임대상가·행복주택 공고는 제외 — 분양 공고만 (예: "광교 … 임대상가 임차인 모집"은 무관).
        if kw and "분양" in it["title"]:
            hits.append({"key": f"gh:{it['no']}", "source": "gh", "keyword": kw,
                         "title": it["title"], "detail": "사업주체(GH) 게시판 게시", "url": it["url"]})
    return hits


# --- ④ 구글뉴스 RSS ------------------------------------------------------------

def parse_news_rss(xml_text: str) -> list[dict]:
    items = []
    root = ET.fromstring(xml_text)
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        pub = it.findtext("pubDate")
        try:
            pub_dt = parsedate_to_datetime(pub) if pub else None
        except (TypeError, ValueError):
            pub_dt = None
        items.append({"title": title, "url": link, "published": pub_dt})
    return items


def news_hits(items: list[dict], now: datetime) -> list[dict]:
    hits = []
    for it in items:
        kw = match_keyword(it["title"])
        if not kw or not any(w in it["title"] for w in NEWS_CONTEXT_WORDS):
            continue
        if it["published"] is None or now - it["published"] > timedelta(days=NEWS_MAX_AGE_DAYS):
            continue
        hits.append({"key": f"news:{it['url']}", "source": "news", "keyword": kw, "title": it["title"],
                     "detail": f"기사 {it['published'].astimezone(KST):%Y-%m-%d %H:%M} KST", "url": it["url"]})
    return hits


# --- 상태·판정 -----------------------------------------------------------------

def load_state() -> dict:
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        state = {}
    state.setdefault("seen", {})
    state.setdefault("health", {})
    state.setdefault("official_keyword_last_seen", {})
    return state


def save_state(state: dict) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2, sort_keys=True)


def select_new_hits(hits: list[dict], state: dict, now: datetime) -> list[dict]:
    """처음 보는 key만, 그리고 뉴스는 공식 경로가 최근 같은 키워드를 이미 잡았으면 제외."""
    official_cutoff = now - timedelta(days=NEWS_SUPPRESS_IF_OFFICIAL_WITHIN_DAYS)
    for h in hits:
        if h["source"] in ("applyhome", "gh"):
            state["official_keyword_last_seen"][h["keyword"]] = now.isoformat()
    fresh, keys = [], set()
    for h in hits:
        if h["key"] in state["seen"] or h["key"] in keys:
            continue
        if h["source"] == "news":
            last = state["official_keyword_last_seen"].get(h["keyword"])
            if last and datetime.fromisoformat(last) >= official_cutoff:
                state["seen"][h["key"]] = {"first_seen": now.isoformat(), "suppressed": "official_recent"}
                continue
        keys.add(h["key"])
        fresh.append(h)
    return fresh


def record_health(state: dict, source: str, ok: bool, note: str, now: datetime) -> str | None:
    """경로 건강 기록. 연속 실패가 임계치에 처음 도달하면 경보 문구를, 복구되면 복구 문구를 돌려준다."""
    h = state["health"].setdefault(source, {"consecutive_failures": 0, "hole_alerted": False})
    if ok:
        msg = None
        if h.get("hole_alerted"):
            msg = f"✅ {SOURCE_LABELS[source]} 복구됨 ({note})"
        h.update({"consecutive_failures": 0, "hole_alerted": False, "last_ok": now.isoformat(), "last_note": note})
        return msg
    h["consecutive_failures"] = h.get("consecutive_failures", 0) + 1
    h["last_error"] = note
    h["last_error_at"] = now.isoformat()
    if h["consecutive_failures"] >= HOLE_ALERT_AFTER_FAILURES and not h.get("hole_alerted"):
        h["hole_alerted"] = True
        return (f"❌ {SOURCE_LABELS[source]} {h['consecutive_failures']}회 연속 실패 — 그물에 구멍이 났습니다. "
                f"마지막 오류: {note}")
    return None


# --- 실행 ----------------------------------------------------------------------

def collect(now: datetime) -> tuple[list[dict], dict[str, tuple[bool, str]]]:
    hits: list[dict] = []
    status: dict[str, tuple[bool, str]] = {}

    try:
        rows = parse_applyhome(_get(APPLYHOME_LIST_URL))
        if not rows:
            raise ValueError("목록 행 0건 — 페이지 구조 변경 의심")
        hits += applyhome_hits(rows)
        status["applyhome"] = (True, f"목록 {len(rows)}건 파싱")
    except Exception as e:  # noqa: BLE001 — 경로별 독립 실패
        status["applyhome"] = (False, f"{type(e).__name__}: {e}")

    try:
        items: dict[str, dict] = {}
        errors = []
        for url in GH_URLS:
            try:
                for it in parse_gh(_get(url)):
                    items.setdefault(it["no"], it)
            except Exception as e:  # noqa: BLE001
                errors.append(f"{url}: {type(e).__name__}")
        if not items:
            raise ValueError("공고 링크 0건 — " + ("; ".join(errors) or "페이지 구조 변경 의심"))
        hits += gh_hits(list(items.values()))
        status["gh"] = (True, f"공고 링크 {len(items)}건 파싱")
    except Exception as e:  # noqa: BLE001
        status["gh"] = (False, f"{type(e).__name__}: {e}")

    try:
        n_items, errors = 0, []
        for q in NEWS_QUERIES:
            url = ("https://news.google.com/rss/search?hl=ko&gl=KR&ceid=KR:ko&q=" + urllib.parse.quote(q))
            try:
                items = parse_news_rss(_get(url))
                n_items += len(items)
                hits += news_hits(items, now)
            except Exception as e:  # noqa: BLE001
                errors.append(f"{q}: {type(e).__name__}")
        if errors and len(errors) == len(NEWS_QUERIES):
            raise ValueError("모든 뉴스 질의 실패 — " + "; ".join(errors))
        status["news"] = (True, f"기사 {n_items}건 확인")
    except Exception as e:  # noqa: BLE001
        status["news"] = (False, f"{type(e).__name__}: {e}")

    return hits, status


def compose_alert(new_hits: list[dict], api_ids: set[str] | None) -> tuple[str, str]:
    names = sorted({h["title"] for h in new_hits if h["source"] != "news"} or {h["title"] for h in new_hits})
    subject = f"[청약 그물망 · {', '.join(sorted({h['keyword'] for h in new_hits}))}] 신규 감지 {len(new_hits)}건 — {names[0][:40]}"
    lines = ["data.go.kr API 바깥의 감시 경로에서 관심 키워드 공고를 새로 발견했습니다.", ""]
    for h in new_hits:
        lines.append(f"■ [{SOURCE_LABELS[h['source']]}] {h['title']}")
        lines.append(f"   {h['detail']}")
        lines.append(f"   {h['url']}")
        if h.get("house_manage_no"):
            if api_ids is None:
                lines.append("   API 동기화 여부: 확인 불가(API 조회 실패)")
            elif h["house_manage_no"] in api_ids:
                lines.append("   API 동기화: 됨 — 소득요건 자동분석 메일이 별도로 갑니다")
            else:
                lines.append("   ⚠ API 동기화: 아직 안 됨 — 기존 자동분석은 이 공고를 아직 못 봅니다. 모집공고문을 직접 확인하세요")
        lines.append("")
    lines.append(f"감시 키워드: {', '.join(ALERT_KEYWORDS)}")
    lines.append(f"대시보드: {alerts.DASHBOARD_URL}")
    return subject, "\n".join(lines)


def api_ids_from_env() -> set[str] | None:
    """fetch_and_render.py가 같은 실행에서 남긴 API 공고 ID 목록(있으면) — 교차검증용."""
    path = os.environ.get("NET_API_IDS_PATH")
    if not path or not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return set(json.load(f))


def send(subject: str, body: str) -> None:
    to_addr = os.environ.get("ALERT_EMAIL_TO")
    gmail, pw = os.environ.get("GMAIL_ADDRESS"), os.environ.get("GMAIL_APP_PASSWORD")
    if to_addr and gmail and pw:
        alerts.send_email(to_addr, gmail, pw, subject, body)
    repo, token = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_TOKEN")
    if repo and token:
        alerts.create_github_issue(repo, token, subject, body)


def main() -> int:
    dry = os.environ.get("DRY_RUN") == "1"
    now = datetime.now(KST)
    state = load_state()
    hits, status = collect(now)

    hole_msgs = [m for src, (ok, note) in status.items() if (m := record_health(state, src, ok, note, now))]
    new_hits = select_new_hits(hits, state, now)

    for src, (ok, note) in status.items():
        print(f"[{'OK' if ok else 'FAIL'}] {SOURCE_LABELS[src]}: {note}")
    print(f"매칭 {len(hits)}건, 신규 {len(new_hits)}건")
    for h in new_hits:
        print(f"  NEW [{h['source']}] {h['title']} | {h['detail']}")

    if dry:
        return 0

    if new_hits:
        subject, body = compose_alert(new_hits, api_ids_from_env())
        send(subject, body)
        for h in new_hits:
            state["seen"][h["key"]] = {"first_seen": now.isoformat(), "source": h["source"], "title": h["title"]}
    if hole_msgs:
        body = "\n".join(hole_msgs + ["", "다른 경로는 계속 감시 중이지만, 이 경로가 복구될 때까지 그물이 한 겹 얇아진 상태입니다.",
                                      "상태 파일: collectors/subscription_monitor/net_state.json"])
        send(f"[청약 그물망 점검] 감시 경로 상태 변화 {len(hole_msgs)}건", body)
    state["last_run"] = now.isoformat()
    save_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
