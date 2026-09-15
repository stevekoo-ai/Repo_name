"""내용 이상 탐지 — "파일은 새로 왔는데 내용이 망가졌다"를 잡는다.

신선도만 보면 못 잡는 사고가 있다: 컬렉터가 매일 성공 종료하면서 빈
파일이나 컬럼이 빠진 파일을 계속 덮어쓰는 경우, fetched_at은 매번
갱신되니 신선도 검사는 통과하지만 내용은 죽어있다. 채권 누락 사고
(TR이 채권을 안 줘서 "없는 것"으로 취급할 뻔한 건)와 같은 계열이다.

여기서 하는 검사는 의도적으로 얕다 — 값의 "의미"를 판정하지 않고
**구조**만 본다(행이 있는가, 필요한 컬럼이 있는가). 의미 판정(가격이
말이 되는가 등)은 소스마다 달라 일반화하면 오탐이 늘어난다.
"""
from __future__ import annotations

import csv
from pathlib import Path

from engine.health.registry import SourceSpec

REPO = Path(__file__).resolve().parents[2]


def check_content(spec: SourceSpec) -> list[str]:
    """이상 목록을 돌려준다. 빈 리스트 = 이상 없음(또는 검사 대상 아님)."""
    if not spec.path:
        return []  # RUN_LOG/DATED_FILE_GLOB 소스는 대상 파일이 특정되지 않아 생략
    p = REPO / spec.path
    if not p.exists():
        return []  # 파일 부재는 freshness 쪽 MISSING이 이미 잡는다 — 중복 보고 안 함

    problems: list[str] = []
    with p.open(encoding="utf-8") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration:
            return [f"{spec.path}: 헤더 행조차 없음(완전히 빈 파일)"]
        rows = list(reader)

    if spec.required_columns:
        missing = [c for c in spec.required_columns if c not in header]
        if missing:
            problems.append(f"{spec.path}: 필수 컬럼 누락 {missing} (현재 헤더: {header})")

    if len(rows) < spec.min_rows:
        problems.append(f"{spec.path}: 행 {len(rows)}개 < 최소 요구 {spec.min_rows}개")

    return problems
