"""One-off: download 힐스테이트 고덕엘리스트 A12BL/A65BL's PDFs and print the
FULL 소득기준 chapter (not just the applicable_target_line one-liner), plus
every "적용대상" occurrence position, to resolve why business_type=국민주택형
came back income_scope=미분류 (no "60㎡ 이하" marker found) for both blocks —
see wiki/concepts/public-housing-income-requirement-framework.md 2026-09-18
"부수 발견" section for the working hypothesis (multiple "적용대상:" lines in
this chapter, only the first — 특별공급 — being captured)."""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
import income_analysis  # noqa: E402

ROWS = [
    {"HOUSE_NM": "힐스테이트 고덕엘리스트 A12BL 공공분양주택",
     "PBLANC_URL": "https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancDetail.do?houseManageNo=2026000437&pblancNo=2026000437"},
    {"HOUSE_NM": "힐스테이트 고덕엘리스트 A65BL 공공분양주택",
     "PBLANC_URL": "https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancDetail.do?houseManageNo=2026000438&pblancNo=2026000438"},
]

for row in ROWS:
    print("=" * 90)
    print(row["HOUSE_NM"])
    print("=" * 90)
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path, detail_url = income_analysis.discover_pdf(row, tmpdir)
        print(f"다운로드 성공: {pdf_path}")
        print(f"상세페이지/PBLANC_URL 소스: {detail_url}\n")
        text = income_analysis.extract_text_from_file(pdf_path)
        print(f"전체 텍스트 길이: {len(text)}자\n")

        idx = text.find("4. 소득기준")
        if idx == -1:
            idx = text.find("4. 소득 판정 기준")
        if idx == -1:
            print("소득기준 챕터를 못 찾음 — 전체 텍스트에서 '소득' 등장 위치:")
            for m in re.finditer("소득", text):
                print(" ", m.start())
        else:
            print("=== 4. 소득기준 챕터 전문 (8000자) ===")
            print(text[idx:idx + 8000])

            print("\n=== '적용대상' 등장 위치 전체 (몇 번 나오는지 확인) ===")
            for m in re.finditer("적용대상", text[idx:idx + 8000]):
                start = m.start()
                print(f"  offset {start}: ...{text[idx+max(0,start-20):idx+start+120]!r}...")

            print("\n=== '일반공급' 등장 위치 전체 (챕터 전체에서, 소득기준과 무관한 문맥 포함) ===")
            for m in re.finditer("일반공급", text[idx:idx + 8000]):
                start = m.start()
                print(f"  offset {start}: ...{text[idx+max(0,start-30):idx+start+60]!r}...")

    print("\n=== 공급대상/공급규모 문구 (전용면적 구성 확인용 — 60㎡ 이하 세대가 있는지) ===")
    idx2 = text.find("공급대상")
    if idx2 != -1:
        print(text[idx2:idx2 + 2000])
    else:
        print("'공급대상' 텍스트를 못 찾음 — '전용면적' 등장 위치:")
        for m in re.finditer("전용면적", text[:5000]):
            start = m.start()
            print(f"  offset {start}: ...{text[max(0,start-30):start+100]!r}...")

    print()
