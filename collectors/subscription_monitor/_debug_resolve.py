"""One-off, step 2: search the 청약Home API directly (not LH청약플러스's own
search box) for 남양주진접2's PBLANC_URL/HOUSE_MANAGE_NO, then try
discover_pdf() with that URL so Stage 0 (청약Home's own archived detail
page) gets a chance — LH청약플러스's own search index already dropped this
closed listing (confirmed run 37211886267), but 청약Home's detail pages
tend to stay reachable by direct URL/HOUSE_MANAGE_NO long after closing."""
import json
import os
import re
import sys
import tempfile
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
import income_analysis  # noqa: E402

BASE_URL = "https://api.odcloud.kr/api/ApplyhomeInfoDetailSvc/v1/getAPTLttotPblancDetail"


def fetch_page(service_key, page, extra):
    params = {"page": page, "perPage": 50}
    params.update(extra)
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Infuser {service_key}"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def main():
    key = os.environ["DATA_GO_KR_KEY"]
    data = fetch_page(key, 1, {"cond[HOUSE_NM::LIKE]": "남양주진접2"})
    rows = data.get("data", [])
    print(f"API 검색 결과: {len(rows)}건")
    for r in rows:
        print(f"  HOUSE_MANAGE_NO={r.get('HOUSE_MANAGE_NO')} PBLANC_NO={r.get('PBLANC_NO')} "
              f"HOUSE_NM={r.get('HOUSE_NM')!r}")
        print(f"  PBLANC_URL={r.get('PBLANC_URL')}")

    if not rows:
        print("API에도 없음 — 완전히 소급 불가")
        return

    row = rows[0]
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            pdf_path, detail_url = income_analysis.discover_pdf(row, tmpdir)
        except Exception as e:
            print(f"\ndiscover 실패(Stage 0 포함 둘 다): {e}")
            return

        print(f"\n다운로드 성공: {pdf_path}")
        print(f"상세페이지: {detail_url}\n")
        text = income_analysis.extract_text_from_file(pdf_path)
        print(f"전체 텍스트 길이: {len(text)}자\n")

        print("=== '소득' 등장 위치 전체 ===")
        for m in re.finditer("소득", text):
            start = m.start()
            print(f"  offset {start}: ...{text[max(0,start-40):start+80]!r}...")

        print("\n=== '적용대상' 등장 위치 전체 ===")
        for m in re.finditer("적용대상", text):
            start = m.start()
            print(f"  offset {start}: ...{text[max(0,start-20):start+150]!r}...")

        print("\n=== '공급대상' 문구 ===")
        idx2 = text.find("공급대상")
        if idx2 != -1:
            print(text[idx2:idx2 + 500])


if __name__ == "__main__":
    main()
