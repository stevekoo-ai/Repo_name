"""Temporary: investigate apply.lh.or.kr (LH청약플러스) site structure for
finding the 모집공고문 PDF, since applyhome.co.kr (청약Home) only has a
summary page, not the actual PDF."""
import re
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (compatible; debug/1.0)"}

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read().decode("utf-8", errors="ignore")

print("=== LH청약플러스 메인 ===")
html = fetch("https://apply.lh.or.kr/")
print(f"length: {len(html)}")
print(html[:2000])

print("\n=== 검색/공고 목록 후보 URL 탐색 ===")
# LH청약플러스가 자체 게시판 검색 기능을 제공하는지 메인 페이지의 링크에서 단서 찾기
links = re.findall(r'href=["\']([^"\']+)["\']', html)
interesting = [l for l in links if any(k in l.lower() for k in ["list", "search", "notice", "pblanc", "sbd", "board", "gongo"])]
for l in sorted(set(interesting))[:40]:
    print(" ", l)
