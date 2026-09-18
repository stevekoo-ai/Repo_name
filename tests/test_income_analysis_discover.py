"""
Tests for the Stage 0 (청약Home own-page PDF button) / Stage 1-2 (LH청약플러스
search) fallback logic added to collectors/subscription_monitor/income_analysis.py
on 2026-09-18 — triggered by a real failure the user found: 힐스테이트
고덕엘리스트 A12BL(평택고덕국제화계획지구)'s LH청약플러스 search failed
(leading token '힐스테이트' is a private brand name, not an LH-registered
project name), but 청약Home's own detail page had a "모집공고문 보기" button
that downloads the PDF directly.

No real Playwright/browser/network is used — find_applyhome_pdf() is tested
against a minimal fake `page` object exposing just the Locator-like surface
it calls, and discover_pdf()'s dispatch order is tested by monkeypatching
the two stage functions directly (matching tests/test_compose_income_review.py's
style for the rest of this pipeline).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "collectors", "subscription_monitor"))

import income_analysis  # noqa: E402


# ---------------------------------------------------------------------------
# find_applyhome_pdf() — fake Playwright page
# ---------------------------------------------------------------------------

class _FakeDownload:
    def __init__(self, saved_to):
        self._saved_to = saved_to

    def save_as(self, path):
        self._saved_to.append(path)


class _FakeDownloadContext:
    """Mimics Playwright's `with page.expect_download() as info:` — the
    `value` is available immediately here since there's no real event loop."""

    def __init__(self, download):
        self._download = download

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    @property
    def value(self):
        return self._download


class _FakeLocator:
    def __init__(self, count, on_click=None):
        self._count = count
        self._on_click = on_click

    def count(self):
        return self._count

    @property
    def first(self):
        return self

    def click(self):
        if self._on_click:
            self._on_click()


class _FakeContext:
    """Mimics page.context.expect_event("download", ...) — the fix for the
    real 2026-09-18 failure (힐스테이트 고덕엘리스트 A12BL): the button opens
    a new tab, so the download event lands on the *context*, not the
    original page. See find_applyhome_pdf()'s docstring."""

    def __init__(self, download, downloads_ok):
        self._download = download
        self.downloads_ok = downloads_ok

    def expect_event(self, event_name, timeout=None):
        assert event_name == "download"
        if not self.downloads_ok:
            raise TimeoutError("expect_event('download') timed out")
        return _FakeDownloadContext(self._download)


class _FakePage:
    """button_count=0 simulates "no 모집공고문 보기 button on this page"
    (the original 3 reference listings). button_count>0 + downloads_ok=True
    simulates 힐스테이트 고덕엘리스트's case."""

    def __init__(self, button_count=1, downloads_ok=True):
        self.button_count = button_count
        self.downloads_ok = downloads_ok
        self.goto_calls = []
        self._download = _FakeDownload(saved_to=[])
        self.context = _FakeContext(self._download, downloads_ok)

    def goto(self, url, **kwargs):
        self.goto_calls.append(url)

    def get_by_text(self, pattern):
        return _FakeLocator(self.button_count, on_click=self._click)

    def _click(self):
        pass  # the click itself always "succeeds"; whether a download
        # follows is decided by _FakeContext.expect_event above, matching
        # how the real bug manifested (click succeeded, download event was
        # what went missing).


def test_no_button_returns_none_without_raising(tmp_path):
    page = _FakePage(button_count=0)
    result = income_analysis.find_applyhome_pdf(page, "https://www.applyhome.co.kr/detail?x=1", str(tmp_path))
    assert result is None
    assert page.goto_calls == ["https://www.applyhome.co.kr/detail?x=1"]


def test_button_present_downloads_pdf(tmp_path):
    page = _FakePage(button_count=1, downloads_ok=True)
    result = income_analysis.find_applyhome_pdf(page, "https://www.applyhome.co.kr/detail?x=1", str(tmp_path))
    assert result is not None
    assert result.endswith("notice_applyhome.pdf")


def test_button_present_but_no_download_returns_none(tmp_path):
    """Button exists but click doesn't yield a download (e.g. opens a viewer
    tab) — this is 'stage 0 doesn't apply here', not a hard failure."""
    page = _FakePage(button_count=1, downloads_ok=False)
    result = income_analysis.find_applyhome_pdf(page, "https://www.applyhome.co.kr/detail?x=1", str(tmp_path))
    assert result is None


# ---------------------------------------------------------------------------
# discover_pdf() — dispatch order (stage 0 first, LH fallback second).
# Injected via the `browser` param (see income_analysis.py docstring) so
# these tests need no real `playwright` package installed — only CI installs
# it (pip install playwright + playwright install chromium).
# ---------------------------------------------------------------------------

class _FakeBrowser:
    def new_page(self):
        return object()  # never touched directly; stage functions are monkeypatched

    def close(self):
        pass


def test_discover_pdf_uses_applyhome_stage_when_it_succeeds(monkeypatch, tmp_path):
    lh_calls = []
    monkeypatch.setattr(income_analysis, "find_applyhome_pdf", lambda page, url, d: str(tmp_path / "a.pdf"))
    monkeypatch.setattr(
        income_analysis,
        "search_and_download_lh_pdf",
        lambda page, name, d: lh_calls.append(name) or ("should-not-be-used.pdf", "lh-url"),
    )

    row = {"HOUSE_NM": "힐스테이트 고덕엘리스트 A12BL", "PBLANC_URL": "https://www.applyhome.co.kr/x"}
    path, url = income_analysis.discover_pdf(row, str(tmp_path), browser=_FakeBrowser())

    assert path == str(tmp_path / "a.pdf")
    assert url == "https://www.applyhome.co.kr/x"
    assert lh_calls == []  # LH청약플러스 fallback never invoked


def test_discover_pdf_falls_back_to_lh_when_applyhome_has_no_pdf(monkeypatch, tmp_path):
    monkeypatch.setattr(income_analysis, "find_applyhome_pdf", lambda page, url, d: None)
    monkeypatch.setattr(
        income_analysis,
        "search_and_download_lh_pdf",
        lambda page, name, d: (str(tmp_path / "lh.pdf"), "https://apply.lh.or.kr/detail"),
    )

    row = {"HOUSE_NM": "성남복정2 A1블록", "PBLANC_URL": "https://www.applyhome.co.kr/y"}
    path, url = income_analysis.discover_pdf(row, str(tmp_path), browser=_FakeBrowser())

    assert path == str(tmp_path / "lh.pdf")
    assert url == "https://apply.lh.or.kr/detail"


def test_discover_pdf_falls_back_when_applyhome_stage_raises(monkeypatch, tmp_path):
    """A nav timeout or layout change on 청약Home's own page must not be a
    hard failure — it just means stage 0 doesn't apply, fall back to LH."""
    def _boom(page, url, d):
        raise TimeoutError("navigation timeout")

    monkeypatch.setattr(income_analysis, "find_applyhome_pdf", _boom)
    monkeypatch.setattr(
        income_analysis,
        "search_and_download_lh_pdf",
        lambda page, name, d: (str(tmp_path / "lh.pdf"), "https://apply.lh.or.kr/detail"),
    )

    row = {"HOUSE_NM": "인천계양지구 A6블록", "PBLANC_URL": "https://www.applyhome.co.kr/z"}
    path, url = income_analysis.discover_pdf(row, str(tmp_path), browser=_FakeBrowser())

    assert path == str(tmp_path / "lh.pdf")


def test_discover_pdf_falls_back_when_pblanc_url_missing(monkeypatch, tmp_path):
    """No PBLANC_URL at all (row missing the field) — skip stage 0 entirely,
    go straight to LH청약플러스, matching pre-2026-09-18 behavior."""
    called = []
    monkeypatch.setattr(
        income_analysis, "find_applyhome_pdf", lambda *a, **k: called.append("applyhome") or None
    )
    monkeypatch.setattr(
        income_analysis,
        "search_and_download_lh_pdf",
        lambda page, name, d: (str(tmp_path / "lh.pdf"), "https://apply.lh.or.kr/detail"),
    )

    row = {"HOUSE_NM": "양주회천지구 A-26블록"}  # no PBLANC_URL
    path, url = income_analysis.discover_pdf(row, str(tmp_path), browser=_FakeBrowser())

    assert called == []  # stage 0 never attempted without a PBLANC_URL
    assert path == str(tmp_path / "lh.pdf")
