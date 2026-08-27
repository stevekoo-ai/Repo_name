#!/usr/bin/env python3
"""CI 단계 자동 상태로그 — sources/automation-run-log.csv에 한 줄 append.

2026-08-27 헬스체크에서, "GitHub Actions API 수집이 실제로 도는지·재시도가
발동됐는지"를 알 방법이 `mcp__github__actions_list`/`get_job_logs`로 워크플로별
run 이력을 수동으로 훑는 것뿐이었다(트레이스 불가) — 그 대응으로 신설.
재시도 루프(`until ...; done`)를 감싼 5개 워크플로(sk-hynix-daily-report,
portfolio-holdings-sync, macro-data-sync, sec-edgar-capex, real-estate-sync)가
각 스텝의 성공/재시도소진을 이 CSV에 append하면, 다음부터는 이 파일 한 번
읽는 것만으로 "자동수집이 도는지, 재시도가 실제로 발동된 적 있는지"를 즉시
답할 수 있다. append-only — 과거 행은 절대 수정하지 않는다(log-operating-policy
R1-R6와 같은 원칙).

Usage:
    python3 scripts/log_automation_run.py <workflow> <step> <attempts_used> <max_attempts> <result>

    result: success | exhausted
"""
from __future__ import annotations

import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG_PATH = REPO_ROOT / "sources" / "automation-run-log.csv"
HEADER = ["timestamp_utc", "workflow", "step", "attempts_used", "max_attempts", "result"]
VALID_RESULTS = ("success", "exhausted")


def log_path() -> Path:
    # AUTOMATION_LOG_PATH override exists only for tests — CI never sets it,
    # so production runs always write to sources/automation-run-log.csv.
    override = os.environ.get("AUTOMATION_LOG_PATH")
    return Path(override) if override else DEFAULT_LOG_PATH


def append_row(workflow: str, step: str, attempts_used: str, max_attempts: str, result: str,
               path: Path | None = None) -> Path:
    if result not in VALID_RESULTS:
        raise ValueError(f"result must be one of {VALID_RESULTS}, got {result!r}")

    target = path or log_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    is_new = not target.exists()
    with target.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(HEADER)
        writer.writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            workflow, step, attempts_used, max_attempts, result,
        ])
    return target


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(f"usage: {sys.argv[0]} <workflow> <step> <attempts_used> <max_attempts> <result>",
              file=sys.stderr)
        return 2
    workflow, step, attempts_used, max_attempts, result = argv
    try:
        append_row(workflow, step, attempts_used, max_attempts, result)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
