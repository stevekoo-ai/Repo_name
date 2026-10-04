"""One-off: resolve the long-open 남양주진접2지구 A-4블록(잔여세대) parsing
failure (wiki/concepts/public-housing-income-requirement-framework.md
"❌ 파싱 실패, 원인 미확정" since 2026-09-01) — download its PDF via
discover_pdf() (now has the Stage-0 청약Home-button path that didn't exist
back then) and print the FULL text (not just an 8000자 window around a
header we're not sure exists) so we can find the real chapter heading this
"잔여세대 추가입주자모집공고" uses for income requirements."""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
import income_analysis  # noqa: E402

HOUSE_NM = "남양주진접2지구 A-4블록 신혼희망타운(공공분양) 잔여세대 추가입주자모집공고"

row = {"HOUSE_NM": HOUSE_NM}  # no PBLANC_URL on hand — Stage 0 skipped, straight to LH청약플러스 search

with tempfile.TemporaryDirectory() as tmpdir:
    try:
        pdf_path, detail_url = income_analysis.discover_pdf(row, tmpdir)
    except Exception as e:
        print(f"discover 실패: {e}")
        raise SystemExit(1)

    print(f"다운로드 성공: {pdf_path}")
    print(f"상세페이지: {detail_url}\n")
    text = income_analysis.extract_text_from_file(pdf_path)
    print(f"전체 텍스트 길이: {len(text)}자\n")

    print("=== '소득' 등장 위치 전체 (어떤 챕터 제목을 쓰는지 찾기) ===")
    for m in re.finditer("소득", text):
        start = m.start()
        print(f"  offset {start}: ...{text[max(0,start-40):start+80]!r}...")

    print("\n=== '적용대상' 등장 위치 전체 ===")
    for m in re.finditer("적용대상", text):
        start = m.start()
        print(f"  offset {start}: ...{text[max(0,start-20):start+150]!r}...")

    print("\n=== '공급대상' 문구 (전용면적 구성) ===")
    idx2 = text.find("공급대상")
    if idx2 != -1:
        print(text[idx2:idx2 + 500])
