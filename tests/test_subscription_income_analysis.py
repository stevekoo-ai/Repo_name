"""
Tests for collectors/subscription_monitor/income_analysis.py.

Only analyze_text() (pure text -> classification) is unit-tested here — the
network-touching stages (find_pdf_link/download_pdf) are I/O and not worth
mocking in detail; analyze_listing()'s try/except-per-stage contract is
simple enough to trust by inspection. These fixtures are minimal synthetic
excerpts modeled on the 3 reference PDFs (성남복정2 A1 / 인천계양 A6 /
양주회천 A-26), not the full documents, so tests don't depend on external
files.

collectors/subscription_monitor/*.py are run as standalone scripts (no
__init__.py — see fetch_and_render.py's bare `from judge import ...`), so we
add that directory to sys.path directly rather than importing as a package.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "collectors", "subscription_monitor"))

from income_analysis import analyze_text, STANDARD_PERCENTAGES  # noqa: E402


NEWLYWED_EXCERPT = """
1. 신청자격
   4. 소득 판정 기준

■ 적용대상 : 본청약(신혼부부·예비신혼부부·한부모가족) 신청자 (* 사전청약 당첨자의 경우 재심사하지 않음)

<표5> 전년도 도시근로자 가구당 월평균소득 기준
                  전년도 도시근로자 가구당 월평균소득의 70%
                  전년도 도시근로자 가구당 월평균소득의 80%
                  전년도 도시근로자 가구당 월평균소득의 100%
                  전년도 도시근로자 가구당 월평균소득의 130%
                  전년도 도시근로자 가구당 월평균소득의 200%
"""

NATIONAL_HOUSING_EXCERPT = """
   4. 소득기준

■ 적용대상 : 다자녀 ․ 노부모부양 ․ 생애최초 ․ 신혼부부 ․ 신생아 특별공급 및 전용면적 60㎡ 이하 일반공급 신청자(* 사전청약 당첨자의 경우 재심사하지 않음)

              공급유형                    구분               3인 이하
     일반 60㎡          도시근로자 가구당 월평균소득액의 100%
     이하    우선공급(1순위자)   도시근로자 가구당 월평균소득액의 140%
              추첨공급(20%)      도시근로자 가구당 월평균소득액의 200%
"""

NO_INCOME_CHAPTER_TEXT = "이 문서에는 소득기준 챕터가 아예 없다 (형식이 완전히 다른 공고)."

# 실제 사례(2026-09-18, 힐스테이트 고덕엘리스트 A12BL/A65BL — 사용자가 직접
# 발견한 discover 실패를 계기로 소득요건 자동검증 15건 확대 중 확인) 기반.
# 공급대상(전용면적 구성)이 "4. 소득기준" 챕터보다 앞쪽에 나오는 실제 문서
# 순서를 그대로 재현 — _extract_unit_sizes_sqm()이 전체 text에서 '공급대상'을
# 찾으므로 순서가 맞아야 한다.
SPECIAL_SUPPLY_ONLY_OVER_60_EXCERPT = """
공급대상 : 공공분양주택 837세대 (전용면적 84㎡A 500세대, 84㎡A1 155세대, 84㎡B 155세대, 84㎡B1 27세대)

(본문 생략)

4. 소득기준
■ 적용대상 : 다자녀가구ㆍ 신혼부부ㆍ생애최초ㆍ노부모부양ㆍ신생아 특별공급 신청자

<표4> 전년도 도시근로자 가구당 월평균소득 기준
                    도시근로자 가구당 월평균소득액의 100%
                    도시근로자 가구당 월평균소득액의 140%
                    도시근로자 가구당 월평균소득액의 200%
"""


def test_newlywed_town_classified_as_full_verification():
    result = analyze_text(NEWLYWED_EXCERPT)
    assert result.status == "ok"
    assert result.business_type == "신혼희망타운형"
    assert result.income_scope == "전체검증"
    assert result.exceptions == []


def test_national_housing_classified_as_60sqm_only():
    result = analyze_text(NATIONAL_HOUSING_EXCERPT)
    assert result.status == "ok"
    assert result.business_type == "국민주택형"
    assert result.income_scope == "60㎡이하만검증"
    assert result.exceptions == []


def test_supply_quota_percentages_are_not_mistaken_for_income_multipliers():
    """'추첨공급(20%)' is a supply-quota ratio, not an income multiplier —
    it must not appear in percentages_found (regression for the false-positive
    found during manual validation against the 3 reference PDFs)."""
    result = analyze_text(NATIONAL_HOUSING_EXCERPT)
    assert 20 not in result.percentages_found
    assert result.percentages_found == [100, 140, 200]


def test_unknown_percentage_flagged_as_exception():
    text = NATIONAL_HOUSING_EXCERPT.replace(
        "도시근로자 가구당 월평균소득액의 200%", "도시근로자 가구당 월평균소득액의 175%"
    )
    result = analyze_text(text)
    assert 175 not in STANDARD_PERCENTAGES
    assert 175 in result.unknown_percentages
    assert any("175" in exc for exc in result.exceptions)


def test_missing_income_chapter_fails_gracefully():
    result = analyze_text(NO_INCOME_CHAPTER_TEXT)
    assert result.status == "failed"
    assert result.stage == "parse"
    assert result.reason


def test_missing_applicable_target_line_is_flagged():
    text = "4. 소득기준\n\n(적용대상 문구 없이 바로 표만 나오는 이례적 형식)\n도시근로자 가구당 월평균소득액의 100%"
    result = analyze_text(text)
    assert result.status == "ok"
    assert result.applicable_target_line is None
    assert any("적용대상" in exc for exc in result.exceptions)


def test_special_supply_only_pattern_when_all_units_over_60sqm():
    """No '60㎡ 이하' AND no '일반공급' mention, but the document's own
    '공급대상' confirms every unit is >60㎡ — this is a legitimate third
    pattern (일반공급 자체에 소득요건이 없음), not an unclassified exception."""
    result = analyze_text(SPECIAL_SUPPLY_ONLY_OVER_60_EXCERPT)
    assert result.status == "ok"
    assert result.business_type == "국민주택형"
    assert result.income_scope == "특별공급만해당(일반공급무관)"
    assert result.exceptions == []


def test_special_supply_only_pattern_flagged_if_60sqm_unit_actually_exists():
    """Same 적용대상 wording, but 공급대상 reveals a unit ≤60㎡ mixed in —
    this would mean the notice forgot to mention 일반공급 60㎡ 이하 income
    requirements, a real discrepancy that must NOT be silently accepted."""
    text = SPECIAL_SUPPLY_ONLY_OVER_60_EXCERPT.replace("84㎡B1 27세대", "59㎡C 27세대")
    result = analyze_text(text)
    assert result.status == "ok"
    assert result.income_scope == "특별공급만해당(일반공급무관)"
    assert any("60㎡ 이하" in exc for exc in result.exceptions)


def test_special_supply_only_pattern_flagged_if_unit_composition_unknown():
    """No '공급대상' text found at all to cross-check against — can't confirm
    the "all >60㎡" assumption, so it must stay flagged for manual review."""
    text = SPECIAL_SUPPLY_ONLY_OVER_60_EXCERPT.split("4. 소득기준", 1)[1]
    text = "4. 소득기준" + text  # drop everything before the chapter, incl. 공급대상
    result = analyze_text(text)
    assert result.status == "ok"
    assert result.income_scope == "특별공급만해당(일반공급무관)"
    assert any("공급대상" in exc for exc in result.exceptions)
