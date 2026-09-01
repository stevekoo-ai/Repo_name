"""Temporary one-off debug: dump the 청약Home listing detail page HTML so we
can see why find_pdf_link() isn't finding a .pdf link. Not part of any
workflow — run manually via workflow_dispatch on a throwaway branch, then
deleted once income_analysis.find_pdf_link() is fixed."""

import re
import urllib.request

URLS = [
    "https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancDetail.do?houseManageNo=2026820008&pblancNo=2026820008",
]

for url in URLS:
    print(f"=== {url} ===")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; debug/1.0)"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    print(f"length: {len(html)} chars")

    # Any literal .pdf mention anywhere
    pdf_mentions = [m.start() for m in re.finditer(r"\.pdf", html, re.IGNORECASE)]
    print(f".pdf substring occurrences: {len(pdf_mentions)}")
    for pos in pdf_mentions[:10]:
        print("  ...", html[max(0, pos - 120):pos + 30].replace("\n", " "))

    # Common attachment/download related keywords
    for kw in ["공고문", "첨부", "다운로드", "download", "attach", "fileDown", "javascript:fn_"]:
        count = html.count(kw)
        if count:
            print(f"keyword {kw!r}: {count} occurrences")
            idx = html.find(kw)
            print("  ctx:", html[max(0, idx - 100):idx + 150].replace("\n", " "))

    print()
    print("--- first 3000 chars ---")
    print(html[:3000])
