"""
Automated income-requirement (소득요건) analysis for a matched listing's
모집공고문 PDF.

Runs only for NEW_MATCH listings (keyword-matched: 플랫폼시티/광교/원천동) —
not for every listing fetched every run — because it downloads and parses a
PDF, which is too expensive to do for the hundreds of unrelated 국민주택
listings nationwide.

Pipeline: PBLANC_URL(청약Home 상세페이지) -> scrape PDF link -> download ->
extract text (pdftotext) -> classify against the rules documented in
wiki/concepts/public-housing-income-requirement-framework.md.

Every stage degrades gracefully: if PDF discovery/download/parsing fails, we
return a status="failed" dict with a reason instead of raising, so a bad PDF
link never breaks the alert pipeline (compose.py just omits the section or
notes "자동분석 실패").

📚 Framework reference (single source of truth for the rules below):
   wiki/concepts/public-housing-income-requirement-framework.md
   - Axis 1: 사업유형 (신혼희망타운=전 평형 검증 vs 국민주택=특별공급+60㎡이하만)
   - Axis 2: 국민주택형끼리는 배율표(%)가 「공공주택 특별법 시행규칙」
     별표6의3 전국 공통 — STANDARD_PERCENTAGES가 그 표준 집합.
   - "예외 사례" 절: 여기서 감지된 예외는 사람이 확인 후 그 페이지에 기록.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
import urllib.request
from dataclasses import dataclass, field

REQUEST_TIMEOUT = 25
USER_AGENT = "Mozilla/5.0 (compatible; subscription-monitor-income-analysis/1.0)"

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
    pdf_url: str | None = None
    business_type: str | None = None      # "국민주택형" | "신혼희망타운형" | "미분류"
    income_scope: str | None = None       # "전체검증" | "60㎡이하만검증" | "미분류"
    applicable_target_line: str | None = None
    percentages_found: list[int] = field(default_factory=list)
    unknown_percentages: list[int] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ---------------------------------------------------------------------------
# Stage 1: find the PDF link from the 청약Home listing detail page
# ---------------------------------------------------------------------------

def find_pdf_link(pblanc_url: str) -> str | None:
    """청약Home 상세페이지(PBLANC_URL)를 열어 첫 .pdf 링크를 찾는다.
    페이지 구조가 시행사/시점마다 달라질 수 있어 완전한 파서가 아니라
    "본문 어디든 .pdf로 끝나는 href가 있으면 그것" 수준의 관대한 스크래핑이다."""
    if not pblanc_url or not pblanc_url.startswith("http"):
        return None
    req = urllib.request.Request(pblanc_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        html = resp.read().decode("utf-8", errors="ignore")

    # Prefer an <a href="....pdf"> style match; fall back to any bare URL ending in .pdf.
    m = re.search(r'href=["\']([^"\']+\.pdf[^"\']*)["\']', html, re.IGNORECASE)
    if not m:
        m = re.search(r'(https?://[^\s"\'<>]+\.pdf)', html, re.IGNORECASE)
    if not m:
        return None
    link = m.group(1)
    if link.startswith("//"):
        link = "https:" + link
    elif link.startswith("/"):
        origin = re.match(r"(https?://[^/]+)", pblanc_url)
        link = (origin.group(1) if origin else "") + link
    return link


# ---------------------------------------------------------------------------
# Stage 2: download + extract text
# ---------------------------------------------------------------------------

def download_pdf(pdf_url: str) -> bytes:
    req = urllib.request.Request(pdf_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        return resp.read()


def extract_text(pdf_bytes: bytes) -> str:
    """pdftotext(poppler-utils) -layout 으로 텍스트 추출. CI(workflow)에서
    apt-get install poppler-utils 필요 — .github/workflows/subscription-monitor.yml 참고."""
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(pdf_bytes)
        f.flush()
        result = subprocess.run(
            ["pdftotext", "-layout", f.name, "-"],
            capture_output=True,
            timeout=30,
            check=True,
        )
    return result.stdout.decode("utf-8", errors="ignore")


# ---------------------------------------------------------------------------
# Stage 3: classify against the framework rules
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
    pblanc_url = row.get("PBLANC_URL")
    if not pblanc_url:
        return IncomeAnalysis(status="failed", stage="discover", reason="PBLANC_URL 없음").to_dict()

    try:
        pdf_url = find_pdf_link(pblanc_url)
    except Exception as e:
        return IncomeAnalysis(status="failed", stage="discover", reason=f"상세페이지 접근 실패: {e}").to_dict()
    if not pdf_url:
        return IncomeAnalysis(status="failed", stage="discover", reason="상세페이지에서 PDF 링크를 찾지 못함").to_dict()

    try:
        pdf_bytes = download_pdf(pdf_url)
    except Exception as e:
        return IncomeAnalysis(status="failed", stage="download", pdf_url=pdf_url, reason=f"PDF 다운로드 실패: {e}").to_dict()

    try:
        text = extract_text(pdf_bytes)
    except Exception as e:
        return IncomeAnalysis(status="failed", stage="extract", pdf_url=pdf_url, reason=f"PDF 텍스트 추출 실패: {e}").to_dict()

    analysis = analyze_text(text)
    analysis.pdf_url = pdf_url
    return analysis.to_dict()
