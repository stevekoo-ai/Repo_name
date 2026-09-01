"""One-off: download 의정부우정 A2's PDF and print the FULL 소득기준 chapter
(not just the applicable_target_line one-liner) plus any 60㎡/평형 mentions
nearby, to resolve whether 60㎡ 초과 일반공급 신청자에게도 소득요건이
적용되는지 확정한다."""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
import income_analysis  # noqa: E402

with tempfile.TemporaryDirectory() as tmpdir:
    pdf_path, detail_url = income_analysis.search_and_download_lh_pdf("의정부우정", tmpdir)
    print(f"다운로드 성공: {pdf_path}")
    print(f"상세페이지: {detail_url}\n")
    text = income_analysis.extract_text_from_file(pdf_path)
    print(f"전체 텍스트 길이: {len(text)}자\n")

    # Print the whole 소득기준 chapter, generously
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

    print("\n\n=== 공급대상/공급규모 문구 (전용면적 60㎡ 초과분 존재 여부 확인용) ===")
    idx2 = text.find("공급대상")
    if idx2 != -1:
        print(text[idx2:idx2 + 1500])
