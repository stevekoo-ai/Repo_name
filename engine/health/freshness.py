"""신선도 판정 — registry.py의 4가지 모드를 실제로 계산한다.

값을 못 구하면(파일 없음, 컬럼 없음, run-log에 기록 없음) **None을
반환한다 — 0시간 전이나 무한대로 추정하지 않는다.** 판정 불가와 이상은
다르다(R3: 미수집은 판정이 아니다). 호출부(check.py)가 이 구분을 안다.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from engine.health.registry import FreshnessMode, SourceSpec

REPO = Path(__file__).resolve().parents[2]
RUN_LOG = REPO / "sources" / "automation-run-log.csv"


@dataclass
class FreshnessResult:
    last_seen: datetime | None       # 마지막으로 확인된 시각(UTC, tz-aware)
    last_seen_date: date | None      # CSV_LATEST_DATE용 — 날짜만 있는 경우
    age_hours: float | None
    detail: str


def _parse_iso(s: str) -> datetime | None:
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _read_csv_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _csv_fetched_at(path: Path) -> FreshnessResult:
    rows = _read_csv_rows(path)
    if not rows:
        return FreshnessResult(None, None, None, "파일이 비어있거나 없음")
    best: datetime | None = None
    for r in rows:
        dt = _parse_iso(r.get("fetched_at", ""))
        if dt and (best is None or dt > best):
            best = dt
    if best is None:
        return FreshnessResult(None, None, None, "fetched_at 컬럼에서 파싱 가능한 값 없음")
    age = (datetime.now(timezone.utc) - best).total_seconds() / 3600
    return FreshnessResult(best, best.date(), age, f"fetched_at={best.isoformat()}")


def _csv_latest_date(path: Path) -> FreshnessResult:
    rows = _read_csv_rows(path)
    if not rows:
        return FreshnessResult(None, None, None, "파일이 비어있거나 없음")
    best: date | None = None
    for r in rows:
        try:
            d = date.fromisoformat(r.get("date", "")[:10])
        except ValueError:
            continue
        if best is None or d > best:
            best = d
    if best is None:
        return FreshnessResult(None, None, None, "date 컬럼에서 파싱 가능한 값 없음")
    age = (datetime.now(timezone.utc).date() - best).days * 24.0
    return FreshnessResult(None, best, age, f"최신 데이터 날짜={best.isoformat()}")


def _run_log(workflow: str, step: str) -> FreshnessResult:
    """sources/automation-run-log.csv — 기존 6개 워크플로가 이미 채우고 있는
    (workflow, step, timestamp_utc) 성공 로그. 새 인프라를 안 만들고 재사용."""
    if not RUN_LOG.exists():
        return FreshnessResult(None, None, None, "automation-run-log.csv 없음")
    best: datetime | None = None
    with RUN_LOG.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r.get("workflow") != workflow or r.get("step") != step:
                continue
            dt = _parse_iso(r.get("timestamp_utc", ""))
            if dt and (best is None or dt > best):
                best = dt
    if best is None:
        return FreshnessResult(None, None, None,
                               f"run-log에 {workflow}/{step} 기록 없음")
    age = (datetime.now(timezone.utc) - best).total_seconds() / 3600
    return FreshnessResult(best, best.date(), age, f"마지막 성공={best.isoformat()}")


def _dated_file_glob(template: str, lookback_days: int) -> FreshnessResult:
    today = datetime.now(timezone.utc).date()
    for back in range(lookback_days + 1):
        d = date.fromordinal(today.toordinal() - back)
        p = REPO / template.format(date=d.isoformat())
        if p.exists() and p.stat().st_size > 0:
            age = back * 24.0
            return FreshnessResult(None, d, age, f"{p.relative_to(REPO)} 존재 ({back}일 전 날짜)")
    return FreshnessResult(None, None, None,
                           f"최근 {lookback_days}일 내 {template} 매칭 파일 없음")


def compute_freshness(spec: SourceSpec) -> FreshnessResult:
    if spec.mode == FreshnessMode.CSV_FETCHED_AT:
        return _csv_fetched_at(REPO / spec.path)
    if spec.mode == FreshnessMode.CSV_LATEST_DATE:
        return _csv_latest_date(REPO / spec.path)
    if spec.mode == FreshnessMode.RUN_LOG:
        return _run_log(spec.run_log_workflow, spec.run_log_step)
    if spec.mode == FreshnessMode.DATED_FILE_GLOB:
        return _dated_file_glob(spec.dated_glob_template, spec.dated_lookback_days)
    raise ValueError(f"알 수 없는 freshness mode: {spec.mode}")


def is_stale(spec: SourceSpec, result: FreshnessResult) -> bool:
    """거래일 예외를 반영한 최종 STALE 판정.

    시장 데이터는 휴장일엔 새 데이터가 없는 게 정상이다 — 오늘이 휴장이면
    "마지막 거래일 데이터까지는 왔는가"만 확인한다. 그 요구조차 미달이면
    (휴장 핑계로 진짜 장애를 가리면 안 되므로) 여전히 STALE이다."""
    if result.age_hours is None:
        return False  # 판정 불가는 STALE이 아니다 — MISSING/UNKNOWN으로 별도 처리
    if not spec.market:
        return result.age_hours > spec.max_age_hours

    from engine.briefing import calendar as C
    today = datetime.now(timezone.utc).date()
    if C.is_trading_day(spec.market, today):
        return result.age_hours > spec.max_age_hours
    # 오늘 휴장 — 마지막 거래일 데이터까지는 있어야 한다
    last_trading = C.last_trading_day(spec.market, today + timedelta(days=1))
    seen_date = result.last_seen_date
    if seen_date is None:
        return result.age_hours > spec.max_age_hours
    return seen_date < last_trading
