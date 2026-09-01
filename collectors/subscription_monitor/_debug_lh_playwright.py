"""Temporary: use Playwright to see how apply.lh.or.kr actually renders and
where the 공고문 PDF download is triggered from, since it's a JS SPA that
urllib can't handle. Investigates one known listing (성남복정2 A1,
houseManageNo=2026820008) via the site's own search."""
from playwright.sync_api import sync_playwright

TARGET_NAME = "성남복정2"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    print("=== 1) LH청약플러스 메인 접속 ===")
    page.goto("https://apply.lh.or.kr/", wait_until="networkidle", timeout=30000)
    print("최종 URL:", page.url)
    print("타이틀:", page.title())

    # Dump visible links/buttons that look like search/notice-list entry points
    print("\n=== 2) 메인 페이지 링크 후보 ===")
    hrefs = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.textContent.trim()])")
    for href, text in hrefs:
        if any(k in (href + text) for k in ["공고", "청약", "검색", "notice", "sbd", "board", "list", "gongo"]):
            print(f"  {text!r} -> {href}")

    print("\n=== 3) 페이지 내 검색창 탐색 ===")
    inputs = page.eval_on_selector_all(
        "input", "els => els.map(e => [e.type, e.id, e.name, e.placeholder])"
    )
    for t in inputs[:30]:
        print(" input:", t)

    browser.close()
