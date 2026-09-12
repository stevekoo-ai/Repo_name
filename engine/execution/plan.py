"""주거 전환 자금 조달 — 실행 계획 일일 판정 엔진.

## 이 모듈이 답하는 세 가지 질문

1. **지금 뭘 해야 하나** — 열려 있는 tranche가 있는가, 시간 하한선에
   걸렸는가, 가격 앞당김 조건이 도달했는가
2. **전제가 맞아가고 있나** — 판단 포스트(checkpoint)의 검증일이 도래했는가,
   도래했다면 그 전제는 맞았는가
3. **계획을 뒤집어야 하나** — Critical Decision Point가 발동했는가

## 설계상 하지 않는 것

- **자동 매도하지 않는다.** 이 모듈은 판정만 한다. 실제 주문은 사람이 낸다.
- **주수를 고정하지 않는다.** 계획은 금액이고, 주수는 그날 가격으로 나눈다.
  주가가 오르면 같은 금액에 더 적은 주수가 필요하다 — 그 이득을 버리지 않기 위해서다.
- **값을 못 찾으면 판정하지 않는다.** 데이터가 없는 걸 "조건 미달"로 기록하면
  CDP가 조용히 잠든다. `UNKNOWN`으로 남기고 그 사실을 드러낸다(R3).

## 데이터 재사용

가격·거시 조회는 `engine.briefing.ledger._lookup()`을 그대로 쓴다. 이미
macro-series.csv와 KIS 스냅샷을 모두 커버하고 "검증일 이하의 마지막 값"
규칙(휴장·발표지연 대응)이 검증돼 있으므로 새로 만들지 않는다.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

from engine.briefing import ledger as L

REPO = Path(__file__).resolve().parents[2]
PLAN_FILE = REPO / "data" / "manual_inputs" / "execution_plan.yaml"
LOG_FILE = REPO / "data" / "manual_inputs" / "execution_log.csv"

OPS = L.OPS  # 같은 연산자 표를 쓴다 — 두 벌이 되면 반드시 갈라진다


def load_plan(path: Path | None = None) -> dict:
    p = path or PLAN_FILE
    if not p.exists():
        raise FileNotFoundError(f"실행 계획 파일이 없습니다: {p}")
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def load_log(path: Path | None = None) -> list[dict]:
    """실제 매도 기록. 계획 대비 실적을 보려면 이게 있어야 한다."""
    p = path or LOG_FILE
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r.get("date")]


def raised_by(as_of: date, log: list[dict] | None = None) -> int:
    """as_of까지 실제로 조달한 누적 금액."""
    rows = load_log() if log is None else log
    total = 0
    for r in rows:
        if r["date"] > as_of.isoformat():
            continue
        try:
            total += int(float(r["amount_krw"]))
        except (ValueError, KeyError, TypeError):
            continue
    return total


def shares_for(amount_krw: int, price: float | None) -> int | None:
    """금액을 주수로 환산. 가격을 모르면 None — 추정치를 만들지 않는다."""
    if not price or price <= 0:
        return None
    return -(-int(amount_krw) // int(price))  # 올림 (부족하면 안 되므로)


# ── 판정 결과 ────────────────────────────────────────────────────

@dataclass
class TrancheStatus:
    id: str
    name: str
    state: str            # PENDING | OPEN | DUE | ACCELERATED | DONE
    amount_krw: int
    shares_needed: int | None
    window: tuple[str, str]
    note: str = ""


@dataclass
class CheckpointResult:
    id: str
    date: str
    thesis: str
    status: str           # PENDING | HIT | MISS | UNKNOWN
    actual: float | None
    expected: str
    if_false: str = ""


@dataclass
class CDPResult:
    id: str
    name: str
    severity: str
    fired: bool | None    # None = 데이터 없음(UNKNOWN)
    actual: float | None
    expected: str
    action: str


@dataclass
class ExecutionStatus:
    as_of: date
    price: float | None
    target_krw: int
    raised_krw: int
    remaining_krw: int
    shares_remaining: int | None
    tranches: list[TrancheStatus] = field(default_factory=list)
    checkpoints: list[CheckpointResult] = field(default_factory=list)
    cdps: list[CDPResult] = field(default_factory=list)

    @property
    def progress_pct(self) -> float:
        return 0.0 if not self.target_krw else self.raised_krw / self.target_krw * 100

    @property
    def fired_cdps(self) -> list[CDPResult]:
        return [c for c in self.cdps if c.fired]

    @property
    def unknown_cdps(self) -> list[CDPResult]:
        """데이터를 못 구해 판정하지 못한 CDP. 조용히 숨기면 안 된다."""
        return [c for c in self.cdps if c.fired is None]


def _compare(key: str, op: str, value, as_of: date) -> tuple[bool | None, float | None]:
    actual = L._lookup(key, as_of)
    if actual is None:
        return None, None
    try:
        return OPS[op](actual, float(value)), actual
    except (KeyError, ValueError, TypeError):
        return None, actual


def evaluate(as_of: date, plan: dict | None = None,
             log: list[dict] | None = None) -> ExecutionStatus:
    plan = plan or load_plan()
    tgt = plan["target"]
    price = L._lookup("hynix_close", as_of)
    raised = raised_by(as_of, log)
    remaining = max(0, int(tgt["amount_krw"]) - raised)

    st = ExecutionStatus(
        as_of=as_of, price=price,
        target_krw=int(tgt["amount_krw"]), raised_krw=raised,
        remaining_krw=remaining, shares_remaining=shares_for(remaining, price),
    )

    # ── tranche ──
    for t in plan.get("tranches", []):
        ws, we = t["window_start"], t["window_end"]
        cum_floor = int(t.get("cumulative_floor_krw") or 0)
        acc = t.get("accelerate_if")
        state, note = "PENDING", ""

        if raised >= cum_floor and cum_floor:
            state, note = "DONE", "누적 하한선 충족"
        elif ws <= as_of.isoformat() <= we:
            state = "OPEN"
            if as_of.isoformat() >= t.get("floor_by", we):
                state = "DUE"
                note = (f"시간 하한선 도달 — 누적 {raised:,}원 < "
                        f"하한 {cum_floor:,}원, 차액 {cum_floor - raised:,}원 강제 실행")
            elif t.get("mandatory"):
                note = "무조건 실행 tranche — 가격 조건 없음"
        elif as_of.isoformat() > we:
            state = "DUE"
            note = f"창 종료({we}) 후 미실행 — 누적 {raised:,}원 / 하한 {cum_floor:,}원"
        elif acc and price and price >= float(acc):
            state = "ACCELERATED"
            note = (f"앞당김 조건 도달 (현재 {price:,.0f} ≥ {float(acc):,.0f}) — "
                    f"창({ws}) 이전이지만 실행 가능")

        st.tranches.append(TrancheStatus(
            id=t["id"], name=t["name"], state=state,
            amount_krw=int(t["amount_krw"]),
            shares_needed=shares_for(int(t["amount_krw"]), price),
            window=(ws, we), note=note,
        ))

    # ── 판단 포스트 ──
    for c in plan.get("checkpoints", []):
        if c["date"] > as_of.isoformat():
            st.checkpoints.append(CheckpointResult(
                id=c["id"], date=c["date"], thesis=c["thesis"], status="PENDING",
                actual=None, expected=f"{c['check_key']} {c['check_op']} {c['check_value']}",
                if_false=c.get("if_false", "")))
            continue
        ok, actual = _compare(c["check_key"], c["check_op"], c["check_value"], as_of)
        st.checkpoints.append(CheckpointResult(
            id=c["id"], date=c["date"], thesis=c["thesis"],
            status="UNKNOWN" if ok is None else ("HIT" if ok else "MISS"),
            actual=actual, expected=f"{c['check_key']} {c['check_op']} {c['check_value']}",
            if_false=c.get("if_false", "")))

    # ── CDP ──
    for d in plan.get("critical_decision_points", []):
        fired, actual = _compare(d["check_key"], d["check_op"], d["check_value"], as_of)
        st.cdps.append(CDPResult(
            id=d["id"], name=d["name"], severity=d.get("severity", "warning"),
            fired=fired, actual=actual,
            expected=f"{d['check_key']} {d['check_op']} {d['check_value']}",
            action=d.get("action", "").strip()))

    return st
