"""engine/briefing/render_html.py — 마크다운→HTML 변환.

이 변환은 **LLM을 쓰지 않는다**(토큰 0). 대신 손으로 쓴 변환기라 조용히
틀릴 수 있어, 브리핑이 실제로 쓰는 구조를 전부 테스트로 고정한다.
"""
import pytest

from engine.briefing.render_html import markdown_to_body, render_briefing_html


def test_headings_become_h_tags():
    out = markdown_to_body("# 제목\n\n## 절\n\n### 항")
    assert "<h1>제목</h1>" in out and "<h2>절</h2>" in out and "<h3>항</h3>" in out


def test_table_with_alignment_row_is_converted():
    md = "| 지표 | 값 |\n|---|---:|\n| VIX | 16.46 |"
    out = markdown_to_body(md)
    assert "<table>" in out
    assert "text-align:right" in out, "|---:| 정렬이 반영돼야 한다"
    assert "<td style='text-align:right'>16.46</td>" in out


def test_a_pipe_line_without_an_alignment_row_is_not_a_table():
    """본문에 파이프가 들어간 문장을 표로 오인하면 리포트가 깨진다."""
    out = markdown_to_body("이건 a | b 처럼 파이프가 든 문장이다")
    assert "<table>" not in out


def test_bullets_and_numbered_lists():
    assert "<ul><li>가</li><li>나</li></ul>" in markdown_to_body("- 가\n- 나")
    assert "<ol><li>하나</li><li>둘</li></ol>" in markdown_to_body("1. 하나\n2. 둘")


def test_blockquote_and_hr():
    assert "<blockquote>" in markdown_to_body("> 주의")
    assert "<hr>" in markdown_to_body("---\n")


def test_inline_bold_code_and_links():
    out = markdown_to_body("**굵게**와 `코드`와 [링크](https://example.com)")
    assert "<strong>굵게</strong>" in out
    assert "<code>코드</code>" in out
    assert '<a href="https://example.com">링크</a>' in out


def test_relative_links_survive_for_wiki_cross_references():
    out = markdown_to_body("[위키](../../wiki/monitoring/x.md)")
    assert 'href="../../wiki/monitoring/x.md"' in out


# ── 보안: 본문엔 뉴스에서 온 텍스트가 섞인다 ─────────────────

def test_html_in_the_source_is_escaped_not_executed():
    out = markdown_to_body("뉴스 인용: <script>alert(1)</script>")
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


def test_dangerous_link_schemes_are_dropped_keeping_the_label():
    out = markdown_to_body("[클릭](javascript:alert(1))")
    assert "javascript:" not in out
    assert "클릭" in out, "라벨은 남아야 무엇이 제거됐는지 보인다"


def test_escaping_happens_before_markdown_so_syntax_still_works():
    """이스케이프를 나중에 하면 <script>가 남고, 순서가 틀리면 굵게가 깨진다."""
    out = markdown_to_body("**<b>굵게</b>**")
    assert "<strong>&lt;b&gt;굵게&lt;/b&gt;</strong>" in out


# ── 문서 골격 ────────────────────────────────────────────────

def test_frontmatter_is_stripped_and_used_for_the_title():
    md = "---\ntitle: 아침 브리핑 2026-09-11\nslot: AM\n---\n\n# 본문"
    out = render_briefing_html(md)
    assert "<title>아침 브리핑 2026-09-11</title>" in out
    assert "slot: AM" not in out, "frontmatter가 본문에 새면 안 된다"


def test_shared_css_is_reused_not_reinvented():
    """월간 리포트·대시보드와 같은 제품으로 보여야 한다."""
    from engine.report.html_shared import _CSS

    out = render_briefing_html("# x")
    assert _CSS[:200] in out


def test_document_is_well_formed_enough_to_open():
    out = render_briefing_html("# 제목\n\n내용")
    assert out.startswith("<!doctype html>")
    assert out.rstrip().endswith("</html>")
    assert out.count("<body>") == out.count("</body>") == 1


def test_the_real_briefing_converts_without_losing_sections():
    """실제 발행물로 회귀 확인 — 섹션이 조용히 사라지면 안 된다."""
    from pathlib import Path

    md_path = (Path(__file__).resolve().parents[1] / "report" / "briefing"
               / "2026-09-11-AM.md")
    if not md_path.exists():
        pytest.skip("첫 브리핑이 아직 없음")
    md = md_path.read_text(encoding="utf-8")
    out = render_briefing_html(md)
    for heading in ("어젯밤 미국에서 무슨 일이 있었나", "실측이 말하는 것",
                    "위키 추적 신호", "SK하이닉스에 미칠 영향", "결론"):
        assert heading in out, heading
    assert out.count("<table") == md.count("\n|---"), "표 개수가 보존돼야 한다"
