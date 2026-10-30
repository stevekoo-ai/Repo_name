"""
Tests for collectors/subscription_monitor/net_watch.py — API 바깥 감시 그물망.

픽스처는 2026-10-30 GitHub Actions 러너에서 실측한 청약Home 목록 행 /
GH 게시판 앵커 / 구글뉴스 RSS 구조를 그대로 축약한 것(광교 자연앤 센트레빌
A17BL — API에는 없고 이 세 경로엔 있던 바로 그 공고). 네트워크 호출은
테스트하지 않는다(기존 컨벤션: 순수 파싱·판정 로직만).
"""

import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "collectors", "subscription_monitor"))

import net_watch as nw  # noqa: E402

KST = timezone(timedelta(hours=9))
NOW = datetime(2026, 10, 30, 20, 0, tzinfo=KST)

APPLYHOME_HTML = """
<table><tbody>
<tr data-pbno="2026000527" data-hmno="2026000527" data-honm="안산신길2지구 B-1블록 공공분양주택(본청약)">
 <td>경기</td> <td>국민</td> <td>분양주택</td> <td class="txt_l">안산신길2지구 B-1블록 공공분양주택(본청약)</td>
 <td>동부건설(주)</td> <td>☎ 031-297-0311</td> <td>2026-10-30</td> <td>2026-11-09 ~ 2026-11-18</td> <td>2026-11-30</td>
</tr>
<tr data-pbno="2026000528" data-hmno="2026000528" data-honm="광교 자연앤 센트레빌(A17BL) 공공분양주택">
 <td>경기</td> <td>국민</td> <td>분양주택</td> <td class="txt_l">광교 자연앤 센트레빌(A17BL) 공공분양주택</td>
 <td>동부건설(주), (주)에이치제이중공업</td> <td>☎ 031-261-1770</td> <td>2026-10-30</td> <td>2026-11-09 ~ 2026-11-11</td> <td>2026-11-17</td>
</tr>
<tr data-pbno="2026000530" data-hmno="2026000530" data-honm="남춘천 센트레빌">
 <td>강원</td> <td>민영</td> <td>분양주택</td> <td>남춘천 센트레빌</td> <td>동부건설(주)</td> <td>☎ 033</td>
 <td>2026-10-30</td> <td>2026-11-09 ~ 2026-11-11</td> <td>2026-11-17</td>
</tr>
</tbody></table>
"""

GH_HTML = """
<a href="/gh/announcement-of-salerental001.do?mode=view&amp;articleNo=65302" class="x">광교 A17블록 자연&amp;센트레빌 지분적립형 분양주택 및 공공분양주택 입주자 모집공고
 <span>2026-10-30</span></a>
<a href="/gh/announcement-of-salerental001.do?mode=view&amp;articleNo=65166">수원광교, 다산지금A5 경기행복주택 단지 내 임대상가 임차인 모집 안내</a>
<a href="/gh/announcement-of-salerental001.do?mode=view&amp;articleNo=65200">고덕 자연앤하우스디(A4BL) 잔여세대 공고</a>
<a href="/gh/notice.do?mode=view&amp;articleNo=65272">(수정)「GH biz&amp;광교 건립사업」 안전점검 공고</a>
"""

RSS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>t</title>
<item><title>[먼저보기] 광교 자연앤 센트레빌 청약 (‘26. 11/9 예정) - 홈두부</title>
 <link>https://news.google.com/rss/articles/AAA</link><pubDate>Fri, 30 Oct 2026 03:00:00 GMT</pubDate></item>
<item><title>경기도, 광교 A17블록 지분적립형 분양주택 공급…11월 9~11일 청약 - 포커스경제</title>
 <link>https://news.google.com/rss/articles/BBB</link><pubDate>Fri, 30 Oct 2026 05:00:00 GMT</pubDate></item>
<item><title>광교 호수공원 산책로 정비 - 지역신문</title>
 <link>https://news.google.com/rss/articles/CCC</link><pubDate>Fri, 30 Oct 2026 05:00:00 GMT</pubDate></item>
<item><title>광교 공공분양 지난해 결과 정리 - 옛기사</title>
 <link>https://news.google.com/rss/articles/DDD</link><pubDate>Mon, 01 Sep 2025 05:00:00 GMT</pubDate></item>
</channel></rss>"""


def _empty_state():
    return {"seen": {}, "health": {}, "official_keyword_last_seen": {}}


# --- ② 청약Home -------------------------------------------------------------

def test_applyhome_parses_rows_with_dates_and_type():
    rows = nw.parse_applyhome(APPLYHOME_HTML)
    assert len(rows) == 3
    gw = next(r for r in rows if r["id"] == "2026000528")
    assert gw["name"] == "광교 자연앤 센트레빌(A17BL) 공공분양주택"
    assert gw["region"] == "경기"
    assert gw["house_type"] == "국민"
    assert (gw["announce_date"], gw["rcept_begin"], gw["rcept_end"], gw["winner_date"]) == (
        "2026-10-30", "2026-11-09", "2026-11-11", "2026-11-17")


def test_applyhome_only_keyword_rows_become_hits():
    hits = nw.applyhome_hits(nw.parse_applyhome(APPLYHOME_HTML))
    assert [h["house_manage_no"] for h in hits] == ["2026000528"]
    assert hits[0]["keyword"] == "광교"
    assert hits[0]["key"] == "hm:2026000528"


def test_applyhome_empty_page_parses_to_nothing():
    assert nw.parse_applyhome("<html><body>점검 중</body></html>") == []


# --- ③ GH ---------------------------------------------------------------------

def test_gh_parses_announcement_links_and_unescapes():
    items = nw.parse_gh(GH_HTML)
    nos = [i["no"] for i in items]
    assert nos == ["65302", "65166", "65200"]  # notice.do 링크는 공고 게시판이 아니라 제외
    assert items[0]["url"] == "https://www.gh.or.kr/gh/announcement-of-salerental001.do?mode=view&articleNo=65302"
    assert "자연&센트레빌" in items[0]["title"]


def test_gh_hits_require_keyword_and_sale_not_rental_shop():
    hits = nw.gh_hits(nw.parse_gh(GH_HTML))
    assert [h["key"] for h in hits] == ["gh:65302"]  # 광교 임대상가 공고는 '분양'이 없어 제외


# --- ④ 뉴스 -------------------------------------------------------------------

def test_news_hits_need_keyword_context_and_recency():
    hits = nw.news_hits(nw.parse_news_rss(RSS_XML), NOW)
    titles = [h["title"] for h in hits]
    assert len(hits) == 2
    assert all("광교" in t for t in titles)
    assert not any("산책로" in t for t in titles)   # 청약 맥락 단어 없음
    assert not any("옛기사" in t for t in titles)   # 3일 초과


def test_news_suppressed_when_official_path_saw_same_keyword_recently():
    state = _empty_state()
    hits = nw.applyhome_hits(nw.parse_applyhome(APPLYHOME_HTML)) + nw.news_hits(nw.parse_news_rss(RSS_XML), NOW)
    fresh = nw.select_new_hits(hits, state, NOW)
    assert [h["source"] for h in fresh] == ["applyhome"]
    assert sum(1 for v in state["seen"].values() if v.get("suppressed")) == 2


def test_news_alerts_when_official_paths_are_silent():
    """공식 경로가 전부 죽었거나 아직 못 잡았을 때 뉴스가 최후 백업으로 울려야 한다."""
    state = _empty_state()
    fresh = nw.select_new_hits(nw.news_hits(nw.parse_news_rss(RSS_XML), NOW), state, NOW)
    assert len(fresh) == 2 and all(h["source"] == "news" for h in fresh)


def test_already_seen_key_is_not_resent():
    state = _empty_state()
    state["seen"]["hm:2026000528"] = {"first_seen": "2026-10-30T12:00:00+09:00"}
    fresh = nw.select_new_hits(nw.applyhome_hits(nw.parse_applyhome(APPLYHOME_HTML)), state, NOW)
    assert fresh == []


def test_same_key_twice_in_one_run_counts_once():
    state = _empty_state()
    hits = nw.applyhome_hits(nw.parse_applyhome(APPLYHOME_HTML)) * 2
    assert len(nw.select_new_hits(hits, state, NOW)) == 1


# --- 그물 구멍 경보 -------------------------------------------------------------

def test_hole_alert_fires_once_at_threshold_then_recovery():
    state = _empty_state()
    msgs = [nw.record_health(state, "gh", False, "timeout", NOW) for _ in range(nw.HOLE_ALERT_AFTER_FAILURES + 2)]
    fired = [m for m in msgs if m]
    assert len(fired) == 1 and "연속 실패" in fired[0]
    rec = nw.record_health(state, "gh", True, "ok", NOW)
    assert rec and "복구" in rec
    assert nw.record_health(state, "gh", True, "ok", NOW) is None


def test_single_failure_does_not_alert():
    state = _empty_state()
    assert nw.record_health(state, "applyhome", False, "timeout", NOW) is None
    assert nw.record_health(state, "applyhome", True, "ok", NOW) is None


# --- 메일 문구 ------------------------------------------------------------------

def test_alert_flags_api_not_synced():
    hits = nw.applyhome_hits(nw.parse_applyhome(APPLYHOME_HTML))
    subject, body = nw.compose_alert(hits, api_ids=set())
    assert "광교" in subject
    assert "API 동기화: 아직 안 됨" in body


def test_alert_reports_api_synced_and_unknown():
    hits = nw.applyhome_hits(nw.parse_applyhome(APPLYHOME_HTML))
    _, synced = nw.compose_alert(hits, api_ids={"2026000528"})
    _, unknown = nw.compose_alert(hits, api_ids=None)
    assert "API 동기화: 됨" in synced
    assert "확인 불가" in unknown
