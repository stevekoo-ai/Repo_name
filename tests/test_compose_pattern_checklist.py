"""
Tests for collectors/subscription_monitor/compose.py::_pattern_checklist_lines()
and its wiring into _income_analysis_lines() — 사용자 요청 2026-09-19:
"'기존 패턴과 일치'라고만 하지 말고, 기존 패턴이 뭔지 체크리스트로 적고
일치 내용을 체크하는 형태로 보고서에 표현해줘. 너만 알면되냐!!!"

Each test asserts on the actual rendered line text (not just presence of a
generic "OK"), since the whole point is that a human reading the report can
verify which specific criterion passed or failed without reading the code.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "collectors", "subscription_monitor"))

import compose  # noqa: E402


def _ok_result(income_scope, exceptions=None, business_type="국민주택형", percentages=None):
    return {
        "status": "ok",
        "business_type": business_type,
        "income_scope": income_scope,
        "applicable_target_line": "(placeholder)",
        "percentages_found": percentages or [100, 140, 200],
        "unknown_percentages": [],
        "exceptions": exceptions or [],
        "pdf_url": "https://apply.lh.or.kr/example",
    }


def test_all_checks_pass_show_checkmarks_not_a_bare_ok_line():
    income = _ok_result("60㎡이하만검증")
    checklist = compose._pattern_checklist_lines(income)
    text = "\n".join(checklist)

    # every row is a ✅ (no ❌ appears anywhere)
    assert "❌" not in text
    # ①②③⑤ apply (④ only applies to income_scope="특별공급만해당(일반공급무관)")
    assert text.count("✅") == 4
    assert "① 소득기준 챕터에서 '적용대상:' 문구를 인식함" in text
    assert "② 축1의 3개 패턴" in text
    assert "60㎡이하만검증" in text
    assert "국민주택형 — 특별공급 전원 + 일반공급은 60㎡ 이하만 소득검증" in text
    assert "③ 국민주택형은 일반공급 60㎡ 초과분에 소득검증이 없음" in text
    assert "⑤ 소득배율(%)이" in text
    assert "[100, 140, 200]" in text


def test_newlywed_pattern_skips_the_60sqm_check_row():
    """신혼희망타운형(전체검증)에는 축3(국민주택형 전용 체크)이 해당되지
    않으므로 체크리스트에 아예 나타나지 않아야 한다 — 무관한 체크를
    억지로 통과시키지 않는다."""
    income = _ok_result("전체검증", business_type="신혼희망타운형")
    checklist = compose._pattern_checklist_lines(income)
    text = "\n".join(checklist)
    assert "③" not in text
    assert "④" not in text
    assert "신혼희망타운형 — 전용면적 무관" in text


def test_special_supply_only_pattern_shows_the_4th_supply_target_check():
    income = _ok_result("특별공급만해당(일반공급무관)")
    checklist = compose._pattern_checklist_lines(income)
    text = "\n".join(checklist)
    assert "④ 문서의 '공급대상' 문구를 대조해" in text
    assert "✅" in text and "❌" not in text


def test_failed_check_shows_x_mark_and_the_actual_exception_text():
    """❌ 항목은 왜 실패했는지(실제 exceptions 문구)를 그 자리에서 바로
    보여줘야 한다 — 사용자가 원문을 다시 찾아보지 않아도 이유를 알 수
    있게."""
    exc = "국민주택형인데 소득검증이 60㎡ 초과까지 적용되는 것으로 보임 — 기존 3건 패턴과 다른 예외"
    income = _ok_result("전체검증", exceptions=[exc])
    checklist = compose._pattern_checklist_lines(income)
    text = "\n".join(checklist)
    assert "[❌] ③" in text
    assert exc in text


def test_unknown_percentage_check_fails_visibly():
    exc = "기존 3건(성남복정·인천계양·양주회천)에 없던 배율값 발견: [175]% — 새 배율 구간이거나 기준연도 개정일 수 있음, 원문 확인 필요"
    income = _ok_result("60㎡이하만검증", exceptions=[exc], percentages=[100, 140, 175])
    checklist = compose._pattern_checklist_lines(income)
    text = "\n".join(checklist)
    assert "[❌] ⑤" in text
    assert exc in text


def test_income_analysis_lines_embeds_checklist_and_drops_bare_matched_line():
    """_income_analysis_lines()가 예전의 불투명한 '✅ 기존 검증 사례 패턴과
    일치, 예외 없음' 한 줄 대신 체크리스트를 포함해야 한다."""
    income = _ok_result("60㎡이하만검증")
    lines = compose._income_analysis_lines(income)
    text = "\n".join(lines)
    assert "판별 체크리스트" in text
    assert "① 소득기준 챕터에서" in text
    assert "기존 검증 사례 패턴과 일치, 예외 없음" not in text  # old opaque line is gone


def test_income_analysis_lines_still_flags_when_exceptions_present():
    exc = "'적용대상' 줄을 찾지 못함 — 소득기준 챕터 형식이 기존 3건과 다름"
    income = _ok_result("미분류", exceptions=[exc])
    lines = compose._income_analysis_lines(income)
    text = "\n".join(lines)
    assert "위 체크리스트에서 ❌ 항목이 있음" in text
    assert exc in text
