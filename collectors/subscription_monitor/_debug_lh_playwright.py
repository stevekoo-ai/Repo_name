"""Temporary: search -> detail page -> find actual PDF download for 성남복정2 A1."""
from playwright.sync_api import sync_playwright

TARGET_NAME = "성남복정2"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    print("=== 1) 메인 접속 + 통합검색 ===")
    page.goto("https://apply.lh.or.kr/", wait_until="networkidle", timeout=30000)
    page.evaluate("""() => {
        const el = document.querySelector('#gnrlPop');
        if (el) el.remove();
    }""")
    search_box = page.locator('#mainSrch')
    search_box.click()
    search_box.fill(TARGET_NAME)
    search_box.press("Enter")
    page.wait_for_load_state("networkidle", timeout=30000)

    print("=== 2) 검색결과에서 상세페이지 링크 추출 ===")
    detail_href = page.eval_on_selector(
        'a[href*="selectWrtancInfo.do"]', "el => el.href"
    )
    print("상세페이지 링크:", detail_href)

    print("\n=== 3) 상세페이지 접속, PDF/다운로드 탐색 ===")
    page.goto(detail_href, wait_until="networkidle", timeout=30000)
    print("URL:", page.url)

    # Download link candidates
    hrefs = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.textContent.trim(), e.getAttribute('onclick')])")
    for href, text, onclick in hrefs:
        if any(k in (href + text + (onclick or "")) for k in ["download", "Download", "pdf", "PDF", "파일", "첨부", "fileDown", "fnDown"]):
            print(f"  {text!r} href={href!r} onclick={onclick!r}")

    print("\n--- onclick 속성 전수조사 (javascript: 링크 포함) ---")
    all_onclick = page.eval_on_selector_all(
        "[onclick]", "els => els.map(e => [e.tagName, e.textContent.trim().slice(0,40), e.getAttribute('onclick')])"
    )
    for tag, text, onclick in all_onclick[:40]:
        print(f"  <{tag}> {text!r} onclick={onclick!r}")

    print("\n--- 페이지 내 모든 a[href] (필터 없이, 최초 60개) ---")
    for href, text, onclick in hrefs[:60]:
        print(f"  {text!r} -> {href}")

    # Try clicking any element whose text suggests a PDF/attachment, and see
    # if navigation or a download event happens.
    print("\n=== 4) 다운로드 이벤트 캡처 시도 ===")
    candidates = page.locator("text=/공고문|첨부|다운로드/")
    count = candidates.count()
    print(f"'공고문/첨부/다운로드' 텍스트 요소 {count}개")
    for i in range(min(count, 10)):
        el = candidates.nth(i)
        try:
            tag = el.evaluate("e => e.tagName")
            txt = el.inner_text()
            print(f"  [{i}] <{tag}> {txt!r}")
        except Exception as e:
            print(f"  [{i}] 오류: {e}")

    browser.close()
