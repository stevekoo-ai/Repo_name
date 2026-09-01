"""
Automated income-requirement (소득요건) analysis for a matched listing's
모집공고문 PDF.

Runs only for NEW_MATCH listings (keyword-matched: 플랫폼시티/광교/원천동) —
not for every listing fetched every run — because it drives a headless
browser to search+download a PDF, which is too expensive to do for the
hundreds of unrelated 국민주택 listings nationwide.

Pipeline (discovered empirically 2026-09-01, see wiki/log.md for the trace):
  1. 청약Home API's PBLANC_URL only points to a SUMMARY page — it explicitly
     says "기타 자세한 모집공고문 내용은 사업주체 홈페이지... 참고" (no PDF
     lives there at all).
  2. The 시행사(사업주체) for 국민주택 is almost always LH — so the actual
     PDF lives on LH청약플러스(apply.lh.or.kr), which is a JS SPA (urllib
     gets only an 87-byte redirect shell). Playwright (headless Chromium) is
     required to render it.
  3. On apply.lh.or.kr: 메인 페이지 통합검색(#mainSrch) 검색 -> 결과의
     a[href*="selectWrtancInfo.do"] 상세페이지 링크 -> 그 페이지의
     "...모집공고...pdf" 텍스트를 가진 a[href^="javascript:fileDownLoad"]
     클릭 -> Playwright download event로 실제 PDF 파일 캡처.

Only LH is supported for now (GH/SH/기타 지방공사는 이번 4건 표본에 없었음—
확장 필요시 이 파일에 사업주체별 검색 함수를 추가).

Every stage degrades gracefully: if search/discovery/download fails, we
return a status="failed" dict with a reason instead of raising, so a bad
listing never breaks the alert pipeline (compose.py just notes "자동분석
실패, 수동확인 필요").

📚 Framework reference (single source of truth for the classification rules):
   wiki/concepts/public-housing-income-requirement-framework.md
   - Axis 1: 사업유형 (신혼희망타운=전 평형 검증 vs 국민주택=특별공급+60㎡이하만)
   - Axis 2: 국민주택형끼리는 배율표(%)가 「공공주택 특별법 시행규칙」
     별표6의3 전국 공통 — STANDARD_PERCENTAGES가 그 표준 집합.
   - "예외 사례" 절: 여기서 감지된 예외는 사람이 확인 후 그 페이지에 기록.
"""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field

LH_MAIN_URL = "https://apply.lh.or.kr/"
LH_NAV_TIMEOUT_MS = 30000
LH_DOWNLOAD_TIMEOUT_MS = 30000

# Standard income-multiplier percentages seen across the 3 reference 국민주택형
# announcements (성남복정2 A1 / 인천계양 A6 / 양주회천 A-26), incl. the
# 출산가구 소득기준 완화 table (+10~20%p). A percentage found in a new PDF
# that is NOT in this set is flagged as a possible exception worth a human
# look — it doesn't necessarily mean the PDF is wrong.
STANDARD_PERCENTAGES = {
    50, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 200, 210, 220,
}

INCOME_SECTION_HEADERS = ["4. 소득기준", "4. 소득 판정 기준"]
NEWLYWED_MARKER = "신혼희망타운"
SIXTY_SQM_MARKER = "60㎡ 이하"


@dataclass
class IncomeAnalysis:
    status: str  # "ok" | "failed"
    stage: str | None = None       # where it failed, if status=="failed"
    reason: str | None = None
    pdf_url: str | None = None     # detail page URL (source), not a raw file URL — LH's download is a JS action, not a stable link
    business_type: str | None = None      # "국민주택형" | "신혼희망타운형" | "미분류"
    income_scope: str | None = None       # "전체검증" | "60㎡이하만검증" | "미분류"
    applicable_target_line: str | None = None
    percentages_found: list[int] = field(default_factory=list)
    unknown_percentages: list[int] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ---------------------------------------------------------------------------
# Stage 1+2: search apply.lh.or.kr, find the detail page, download the PDF
# ---------------------------------------------------------------------------

def _search_keyword(house_name: str) -> str:
    """HOUSE_NM's leading token is what LH청약플러스 통합검색 matches on
    reliably (e.g. '성남복정2 A1블록 신혼희망타운(공공분양)(본청약)' -> '성남복정2') —
    the full name (with 블록/괄호 suffixes) does not reliably match."""
    return (house_name or "").split()[0] if (house_name or "").strip() else ""


def search_and_download_lh_pdf(house_name: str, download_dir: str) -> tuple[str, str]:
    """Search LH청약플러스 for house_name, open the listing detail page, and
    download its 모집공고문 PDF (not the .hwpx or 팸플릿 attachments).

    Returns (local_pdf_path, detail_page_url). Raises RuntimeError/LookupError
    with a specific message on any failure — analyze_listing() catches and
    wraps these.
    """
    from playwright.sync_api import sync_playwright  # imported lazily: only NEW_MATCH pays this cost

    keyword = _search_keyword(house_name)
    if not keyword:
        raise ValueError(f"검색어를 추출할 수 없음 (house_name={house_name!r})")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(LH_MAIN_URL, wait_until="networkidle", timeout=LH_NAV_TIMEOUT_MS)
            # A promotional popup (#gnrlPop) covers the page and intercepts
            # clicks on load — remove outright rather than hunting its close
            # button (banner content rotates unpredictably).
            page.evaluate("""() => { const el = document.querySelector('#gnrlPop'); if (el) el.remove(); }""")

            # #mainSrch is the visible main-page search box — a second hidden
            # input shares name="totalSearch" with it, so select by id.
            search_box = page.locator("#mainSrch")
            search_box.click()
            search_box.fill(keyword)
            search_box.press("Enter")
            page.wait_for_load_state("networkidle", timeout=LH_NAV_TIMEOUT_MS)

            detail_link = page.locator('a[href*="selectWrtancInfo.do"]').first
            if detail_link.count() == 0:
                raise LookupError(
                    f"LH청약플러스에서 '{keyword}' 검색결과에 공고 상세 링크 없음 "
                    "(아직 미등록이거나 검색어가 실제 공고명과 다를 수 있음)"
                )
            detail_url = detail_link.get_attribute("href")

            page.goto(detail_url, wait_until="networkidle", timeout=LH_NAV_TIMEOUT_MS)

            # The detail page lists several attachments (.hwpx forms, 팸플릿,
            # 위임장 etc.) as javascript:fileDownLoad('id') links — the main
            # notice is the one whose text contains both "모집공고" and ".pdf".
            pdf_link = page.locator("a").filter(has_text=re.compile(r"모집공고.*\.pdf$"))
            if pdf_link.count() == 0:
                raise LookupError(
                    "상세페이지에서 '...모집공고...pdf' 링크를 찾지 못함 "
                    "(첨부파일 구성이 기존 사례와 다를 수 있음)"
                )

            with page.expect_download(timeout=LH_DOWNLOAD_TIMEOUT_MS) as download_info:
                pdf_link.first.click()
            download = download_info.value
            local_path = os.path.join(download_dir, "notice.pdf")
            download.save_as(local_path)

            return local_path, page.url
        finally:
            browser.close()


# ---------------------------------------------------------------------------
# Stage 3: extract text
# ---------------------------------------------------------------------------

def extract_text_from_file(pdf_path: str) -> str:
    """pdftotext(poppler-utils) -layout 으로 텍스트 추출. CI(workflow)에서
    apt-get install poppler-utils 필요 — .github/workflows/*.yml 참고."""
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True,
        timeout=30,
        check=True,
    )
    return result.stdout.decode("utf-8", errors="ignore")


# ---------------------------------------------------------------------------
# Stage 4: classify against the framework rules
# ---------------------------------------------------------------------------

def _extract_income_section(text: str) -> str | None:
    for header in INCOME_SECTION_HEADERS:
        idx = text.find(header)
        if idx != -1:
            # Take a generous window after the header — enough to cover the
            # "적용대상" line and the income-multiplier table, not so much
            # that unrelated later chapters leak in.
            return text[idx: idx + 6000]
    return None


def _find_applicable_target_line(income_section: str) -> str | None:
    m = re.search(r"적용대상\s*[:：]\s*(.+)", income_section)
    if not m:
        return None
    return m.group(1).strip()


def _classify_business_type(text: str, applicable_line: str | None) -> str:
    if NEWLYWED_MARKER in text[:2000] or (applicable_line and "예비신혼부부" in applicable_line and "한부모가족" in applicable_line):
        return "신혼희망타운형"
    return "국민주택형"


def _classify_income_scope(applicable_line: str | None, business_type: str) -> str:
    if applicable_line is None:
        return "미분류"
    if SIXTY_SQM_MARKER in applicable_line:
        return "60㎡이하만검증"
    if business_type == "신혼희망타운형":
        return "전체검증"
    return "미분류"


def _extract_percentages(income_section: str) -> list[int]:
    """Only percentages attached to '월평균소득(액)의 NNN%' — not every bare
    NN% in the section (e.g. '일반공급(30%)' is a supply-quota ratio, not an
    income multiplier, and would be a false positive if matched loosely)."""
    found = {int(n) for n in re.findall(r"월평균소득액?의\s*(\d{2,3})\s*%", income_section)}
    return sorted(found)


def analyze_text(text: str) -> IncomeAnalysis:
    """Pure function: PDF full text -> classified analysis. No I/O, easy to
    unit-test against the 3 reference PDFs' extracted text."""
    income_section = _extract_income_section(text)
    if income_section is None:
        return IncomeAnalysis(
            status="failed", stage="parse",
            reason="'4. 소득기준' 챕터를 찾지 못함 (공고문 형식이 표준과 다를 수 있음)",
        )

    applicable_line = _find_applicable_target_line(income_section)
    business_type = _classify_business_type(text, applicable_line)
    income_scope = _classify_income_scope(applicable_line, business_type)
    percentages = _extract_percentages(income_section)
    unknown = [p for p in percentages if p not in STANDARD_PERCENTAGES]

    exceptions: list[str] = []
    if applicable_line is None:
        exceptions.append("'적용대상' 줄을 찾지 못함 — 소득기준 챕터 형식이 기존 3건과 다름")
    if income_scope == "미분류":
        exceptions.append(
            f"소득검증 범위를 판별 못함 (business_type={business_type}, applicable_line={applicable_line!r}) — "
            "프레임워크의 축1 규칙(신혼희망타운=전체 / 국민주택=60㎡이하만)에 안 맞는 새 패턴일 수 있음"
        )
    if business_type == "국민주택형" and income_scope == "전체검증":
        exceptions.append("국민주택형인데 소득검증이 60㎡ 초과까지 적용되는 것으로 보임 — 기존 3건 패턴과 다른 예외")
    if unknown:
        exceptions.append(
            f"기존 3건(성남복정·인천계양·양주회천)에 없던 배율값 발견: {unknown}% — "
            "새 배율 구간이거나 기준연도 개정일 수 있음, 원문 확인 필요"
        )

    return IncomeAnalysis(
        status="ok",
        business_type=business_type,
        income_scope=income_scope,
        applicable_target_line=applicable_line,
        percentages_found=percentages,
        unknown_percentages=unknown,
        exceptions=exceptions,
    )


# ---------------------------------------------------------------------------
# Entry point: full pipeline for one listing row
# ---------------------------------------------------------------------------

def analyze_listing(row: dict) -> dict:
    """row is a raw 청약Home API row (same shape judge.py/compose.py use).
    Never raises — every failure mode returns a status="failed" dict so the
    calling alert pipeline can proceed regardless."""
    house_name = row.get("HOUSE_NM")
    if not house_name:
        return IncomeAnalysis(status="failed", stage="discover", reason="HOUSE_NM 없음").to_dict()

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                pdf_path, detail_url = search_and_download_lh_pdf(house_name, tmpdir)
            except Exception as e:
                return IncomeAnalysis(status="failed", stage="discover", reason=f"LH청약플러스 검색/다운로드 실패: {e}").to_dict()

            try:
                text = extract_text_from_file(pdf_path)
            except Exception as e:
                return IncomeAnalysis(status="failed", stage="extract", pdf_url=detail_url, reason=f"PDF 텍스트 추출 실패: {e}").to_dict()
    except Exception as e:
        # Catches anything from Playwright/browser setup itself (e.g. missing
        # chromium install) that isn't already one of the two stages above.
        return IncomeAnalysis(status="failed", stage="discover", reason=f"예기치 않은 오류: {e}").to_dict()

    analysis = analyze_text(text)
    analysis.pdf_url = detail_url
    return analysis.to_dict()
