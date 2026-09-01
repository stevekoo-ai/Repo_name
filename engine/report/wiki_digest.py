"""위키 판단형 지식 -> daily 리포트 브리지 (Phase 4, 2026-08-27).

`data/wiki_digest/*.yaml`을 읽어 payload에 실어 나르고, 각 digest가 대응
하는 `wiki/monitoring/*.md`보다 stale하지 않은지 확인한다. 이 모듈은
판단을 하지 않는다 — 위키가 유일한 원천이고, 여기선 그 압축 요약을 그대로
전달·검증만 한다(data/wiki_digest/README.md 참고).

이 모듈이 wiki/*.md 본문을 파싱하는 유일한 지점은 frontmatter(맨 위
`--- ... ---` 블록)뿐이다 — 자유문 프로즈(Latest Status 본문)는 절대
파싱하지 않는다. 그건 정확히 이 브리지가 존재하는 이유(자유문 파싱은
깨지기 쉽고 신뢰할 수 없음)와 모순되기 때문.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DIGEST_DIR = REPO_ROOT / "data" / "wiki_digest"

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def read_frontmatter(md_path: Path) -> dict[str, Any]:
    """wiki/*.md 파일 맨 위 frontmatter 블록만 파싱. 파일이 없거나 frontmatter가
    없거나 YAML이 깨졌으면 빈 dict(예외를 던지지 않음 — 이 정보는 있으면
    좋은 보조 신호지, 없다고 리포트 파이프라인 전체를 막을 이유는 아니다)."""
    if not md_path.exists():
        return {}
    text = md_path.read_text(encoding="utf-8")
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def load_wiki_digests() -> list[dict[str, Any]]:
    """data/wiki_digest/*.yaml 전부 로드 + 각각의 drift 여부(대응 monitoring
    페이지 frontmatter updated:보다 as_of가 오래됐는지) 표시. 파일 하나가
    없거나 깨졌다고 나머지를 막지 않는다 — 그 digest만 건너뛴다."""
    if not DIGEST_DIR.exists():
        return []
    out: list[dict[str, Any]] = []
    for path in sorted(DIGEST_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if not data.get("as_of"):
            continue
        as_of = str(data["as_of"])  # same YAML-date-vs-str normalization as page_updated below

        monitoring_page = data.get("monitoring_page")
        page_updated = None
        is_stale = False
        if monitoring_page:
            fm = read_frontmatter(REPO_ROOT / monitoring_page)
            raw_updated = fm.get("updated")
            # YAML parses an unquoted ISO date (every wiki page's frontmatter
            # convention) into a datetime.date, not a str — normalize so
            # callers always get a plain string to compare/format with.
            page_updated = str(raw_updated) if raw_updated is not None else None
            if page_updated and page_updated > as_of:
                is_stale = True

        out.append({
            "slug": path.stem,
            "concept_page": data.get("concept_page"),
            "monitoring_page": monitoring_page,
            "as_of": as_of,
            "status_label": data.get("status_label", ""),
            "one_line_summary": data.get("one_line_summary", ""),
            "page_updated": page_updated,
            "is_stale": is_stale,
        })
    return out
