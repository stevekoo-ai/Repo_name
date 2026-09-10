"""테스트가 **실제 데이터 파일을 오염시키지 못하게** 막는다.

## 왜 필요한가 (2026-09-10 실측)

리포트 파이프라인 테스트는 `build_report_payload(month_key="1999-01")`처럼
가짜 월을 넣어 돌리는데, 그 안의 기록 단계가 **저장소의 진짜 파일에 쓴다**.
결과로 감사추적 CSV에 이런 행이 남았다:

    2026-09-10,HOLD,50,WAIT,80,Recorded from PEOS pipeline (1999-01)
    2026-09-10,HOLD,50,WAIT,80,Recorded from PEOS pipeline (1999-02)

`data/daily_signals/`는 CLAUDE.md가 "append-only 감사추적, 절대 손대지 말 것"
으로 지정한 파일이다. 테스트 픽스처 날짜(1999)가 섞인 행이 append되면
**되돌리는 것 말고는 방법이 없고**(append-only라 지울 수도 없다), 하루
두 번 그 일이 벌어졌다.

## 왜 production 코드를 고치지 않는가

`signal_recorder.py`는 CLAUDE.md의 "❌ Never Touch" 목록에 있다. 경로
상수에 환경변수 훅을 넣는 것도 그 파일을 건드리는 일이라, **테스트 쪽에서만**
모듈 상수를 임시 디렉터리로 돌린다. production 동작은 한 글자도 바뀌지 않고,
훅이 없어져도 이 파일만 지우면 된다.

## 무엇을 돌리고 무엇을 그대로 두는가

- 돌린다: **쓰기 전용** 산출물(감사추적·일일 이력·스냅샷·raw 덤프,
  그리고 `docs/reports-index.html`·`docs/archive/` — 리포트 인덱스 테스트가
  실제 저장소를 대상으로 빌더를 돌리는데, **입력은 진짜 report/를 읽고
  출력만 tmp로 가면** 테스트의 검증 의도(실제 파일을 다 찾는가)는 그대로
  유지되면서 커밋 대상 파일은 안 더럽혀진다)
- 그대로 둔다: `data/normalized/`는 **읽기**에도 쓰인다. FRS 테스트를 비롯해
  여러 테스트가 실제 수집 데이터를 읽어 검증하므로 여기를 tmp로 돌리면
  테스트가 검증하는 대상 자체가 사라진다. 실측 확인 결과 테스트 실행이
  이 디렉터리를 더럽히지도 않았다.
"""
from __future__ import annotations

import pytest


@pytest.fixture(autouse=True, scope="session")
def _isolate_generated_data(tmp_path_factory):
    """테스트 세션 동안 쓰기 산출물 경로를 임시 디렉터리로 돌린다."""
    root = tmp_path_factory.mktemp("peos_generated")

    from engine.macro import snapshot as snapshot_mod
    from engine.report import daily_history as history_mod
    from engine.report import signal_recorder as signal_mod
    from collectors import base as collector_base
    from scripts import build_reports_index as index_mod

    originals = {
        (signal_mod, "DATA_DIR"): signal_mod.DATA_DIR,
        (history_mod, "DAILY_HISTORY_PATH"): history_mod.DAILY_HISTORY_PATH,
        (snapshot_mod, "SNAPSHOT_DIR"): snapshot_mod.SNAPSHOT_DIR,
        (collector_base, "RAW_DIR"): collector_base.RAW_DIR,
        (index_mod, "ARCHIVE_DIR"): index_mod.ARCHIVE_DIR,
        (index_mod, "INDEX_PATH"): index_mod.INDEX_PATH,
    }
    redirects = {
        (signal_mod, "DATA_DIR"): root / "daily_signals",
        (history_mod, "DAILY_HISTORY_PATH"): root / "peos_daily_history.csv",
        (snapshot_mod, "SNAPSHOT_DIR"): root / "snapshots",
        (collector_base, "RAW_DIR"): root / "raw",
        (index_mod, "ARCHIVE_DIR"): root / "docs_archive",
        (index_mod, "INDEX_PATH"): root / "docs_reports-index.html",
    }
    for (module, name), path in redirects.items():
        setattr(module, name, path)
        (path if path.suffix == "" else path.parent).mkdir(parents=True, exist_ok=True)

    yield root

    for (module, name), original in originals.items():
        setattr(module, name, original)
