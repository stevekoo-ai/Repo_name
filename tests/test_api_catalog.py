"""API 데이터 카탈로그 드리프트 검사 (scripts/build_api_catalog.py).

2026-09-07 신설. 이 저장소는 같은 날 "문서·주석이 코드와 어긋나서 오래
헤매는" 사고를 두 번 겪었다:
- collectors/kosis.py 주석은 실패 원인을 "kosis.kr TCP 타임아웃 / 한국 IP
  제한"이라 적고 있었지만 실제로는 통계표 ID 오류였다.
- scripts/kosis_lookup.py는 "KOSIS엔 외부에서 닿는 검색 API가 없다"고
  단언했지만 통합검색이 존재했고, 그 잘못된 전제 때문에 통계표를 계속
  추측만 하고 있었다.

카탈로그를 손으로 관리하면 같은 드리프트가 반복된다. 이 테스트는 문서가
코드에서 다시 생성 가능한 상태인지를 CI에서 강제한다.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG = REPO_ROOT / "wiki" / "concepts" / "api-data-catalog.md"


def test_catalog_is_not_stale_relative_to_the_collectors():
    """수집기에 시리즈를 추가하고 카탈로그를 재생성하지 않으면 여기서 걸린다."""
    result = subprocess.run(
        [sys.executable, "scripts/build_api_catalog.py", "--check"],
        cwd=REPO_ROOT, env={"PYTHONPATH": str(REPO_ROOT), "PATH": "/usr/bin:/bin"},
        capture_output=True, text=True,
    )
    assert result.returncode == 0, (
        "카탈로그가 코드와 어긋났다. 재생성할 것:\n"
        "  PYTHONPATH=. python3 scripts/build_api_catalog.py\n"
        f"stderr: {result.stderr}"
    )


def test_every_collector_series_appears_in_the_catalog():
    """카탈로그의 존재 이유는 '무엇을 가질 수 있는지 한눈에 보이는 것'이다.
    시리즈 하나가 문서에서 빠지면 그만큼 보이지 않는 공백이 생긴다."""
    from collectors import bls, ecos, fred, imf, kosis

    text = CATALOG.read_text(encoding="utf-8")
    missing = []
    for key in list(fred.SERIES) + list(ecos.ECOS_SERIES) + list(kosis.KOSIS_SERIES) \
            + list(bls.BLS_SERIES) + list(imf.IMF_SERIES):
        if f"`{key}`" not in text:
            missing.append(key)
    assert not missing, f"카탈로그에 빠진 시리즈: {missing}"


def test_catalog_marks_itself_as_generated_so_nobody_hand_edits_it():
    text = CATALOG.read_text(encoding="utf-8")
    assert "자동 생성" in text
    assert "scripts/build_api_catalog.py" in text


def test_catalog_records_the_known_gaps_not_just_what_works():
    """무엇을 못 가져오는지도 카탈로그의 일부다 — 그게 없으면 '없는 데이터'와
    '있는데 안 쓰는 데이터'를 구분할 수 없다(BLS가 정확히 후자였다)."""
    text = CATALOG.read_text(encoding="utf-8")
    assert "아직 못 가져오는 것" in text


def test_catalog_is_linked_from_the_wiki_index():
    """index.md에서 닿지 않는 페이지는 고아 페이지다(wiki/CLAUDE.md 린트 규칙)."""
    index = (REPO_ROOT / "wiki" / "index.md").read_text(encoding="utf-8")
    assert "api-data-catalog.md" in index
