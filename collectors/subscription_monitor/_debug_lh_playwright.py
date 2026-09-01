"""Temporary: use Playwright to trace apply.lh.or.kr's search -> detail -> PDF
download flow for a known listing (성남복정2 A1)."""
from playwright.sync_api import sync_playwright

TARGET_NAME = "성남복정2"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    print("=== 1) 메인 접속 + 통합검색 ===")
    page.goto("https://apply.lh.or.kr/", wait_until="networkidle", timeout=30000)
    # A promotional popup (#gnrlPop, notice banners) covers the page on load
    # and intercepts clicks — remove it outright rather than hunting for its
    # close button (banner content is unpredictable/rotating).
    removed = page.evaluate("""() => {
        const el = document.querySelector('#gnrlPop');
        if (el) { el.remove(); return true; }
        return false;
    }""")
    print(f"gnrlPop 팝업 제거: {removed}")
    # There are two inputs sharing name="totalSearch" (a hidden header-popup one
    # and the visible main-page one, id="mainSrch") — id disambiguates.
    search_box = page.locator('#mainSrch')
    search_box.click()
    search_box.fill(TARGET_NAME)
    search_box.press("Enter")
    page.wait_for_load_state("networkidle", timeout=30000)
    print("검색 후 URL:", page.url)

    print("\n=== 2) 검색결과 페이지 링크 덤프 ===")
    hrefs = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.textContent.trim()])")
    for href, text in hrefs:
        if text or "pdf" in href.lower():
            print(f"  {text!r} -> {href}")

    print("\n=== 3) 검색결과 페이지 본문 텍스트(첫 3000자) ===")
    body_text = page.locator("body").inner_text()
    print(body_text[:3000])

    print("\n=== 4) '모집공고문' 목록 페이지 직접 접속 시도 ===")
    page2 = browser.new_page()
    try:
        page2.goto(
            "https://apply.lh.or.kr/lhapply/apply/bfh/slpa/list.do?mi=1349",
            wait_until="networkidle",
            timeout=30000,
        )
        print("URL:", page2.url)
        hrefs2 = page2.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.textContent.trim()])")
        pdf_like = [h for h in hrefs2 if TARGET_NAME in h[1] or "성남" in h[1]]
        print(f"'{TARGET_NAME}' 또는 '성남' 포함 링크 {len(pdf_like)}개:")
        for href, text in pdf_like[:10]:
            print(f"  {text!r} -> {href}")
        if not pdf_like:
            print("본문 첫 2000자:")
            print(page2.locator("body").inner_text()[:2000])
    except Exception as e:
        print("실패:", e)

    browser.close()
