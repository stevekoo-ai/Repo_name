"""일회성 탐침(throwaway branch 전용, main 병합 금지).

API 외 2차·3차 감시 경로 후보가 GitHub Actions 러너에서 실제로 열리는지,
그리고 2026-10-30 공고된 '광교 자연앤 센트레빌'이 각 경로에 보이는지 실측.
"""

import re
import urllib.parse
import urllib.request

from playwright.sync_api import sync_playwright

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
NEEDLES = ["자연앤 센트레빌", "자연앤센트레빌", "광교", "원천동", "A17"]

PAGES = {
    "applyhome_apt_list": "https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancListView.do",
    "applyhome_main": "https://www.applyhome.co.kr/co/coa/selectMainView.do",
    "gh_apply_main": "https://apply.gh.or.kr/",
    "gh_main": "https://www.gh.or.kr/",
    "lh_sale_list_1026": "https://apply.lh.or.kr/lhapply/apply/wt/wrtanc/selectWrtancList.do?mi=1026",
    "myhome_notice": "https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcView.do",
    "naver_news": "https://search.naver.com/search.naver?where=news&sort=1&query="
                  + urllib.parse.quote("광교 자연앤 센트레빌"),
    "google_news_rss": "https://news.google.com/rss/search?hl=ko&gl=KR&ceid=KR:ko&q="
                       + urllib.parse.quote("광교 공공분양 입주자모집공고"),
}


def report(name: str, text: str) -> None:
    print(f"  length={len(text)}")
    for n in NEEDLES:
        idx = text.find(n)
        if idx >= 0:
            snippet = re.sub(r"\s+", " ", text[max(0, idx - 80): idx + 120])
            print(f"  HIT '{n}': ...{snippet}...")
        else:
            print(f"  miss '{n}'")


def via_urllib(name: str, url: str) -> None:
    print(f"\n### [urllib] {name}: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ko-KR,ko"})
        with urllib.request.urlopen(req, timeout=25) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(f"  status={resp.status}")
            report(name, body)
    except Exception as e:
        print(f"  ERROR {type(e).__name__}: {e}")


def via_browser(page, name: str, url: str) -> None:
    print(f"\n### [browser] {name}: {url}")
    try:
        resp = page.goto(url, wait_until="networkidle", timeout=45000)
        print(f"  status={resp.status if resp else None} final_url={page.url}")
        text = page.inner_text("body")
        report(name, text)
        links = page.eval_on_selector_all(
            "a", "els => els.map(e => [e.innerText.trim().slice(0,60), e.getAttribute('href') || '', e.getAttribute('onclick') || ''])")
        hits = [l for l in links if any(n in l[0] for n in NEEDLES)]
        print(f"  anchors={len(links)}, keyword anchors={len(hits)}")
        for l in hits[:8]:
            print(f"    - {l}")
        rows = page.eval_on_selector_all("table tr", "els => els.slice(0,6).map(e => e.innerText.replace(/\\s+/g,' ').slice(0,160))")
        print(f"  first table rows: {rows}")
    except Exception as e:
        print(f"  ERROR {type(e).__name__}: {e}")


def main():
    for name, url in PAGES.items():
        via_urllib(name, url)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent=UA, locale="ko-KR")
        for name, url in PAGES.items():
            if name == "google_news_rss":
                continue
            via_browser(page, name, url)
        browser.close()


if __name__ == "__main__":
    main()
