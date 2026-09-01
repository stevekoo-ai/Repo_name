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
