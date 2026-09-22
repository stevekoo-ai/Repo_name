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
class EarlyWarningResult:
    """임계가 **깨지기 전에** 뜨는 경보. CDP와 역할이 다르다 — CDP는 넘은
    순간 발동하고, 이건 접근·이탈 중일 때 미리 뜬다(2026-09-22 신설)."""
    id: str
    name: str
    kind: str                  # "approach" | "premise_drift"
    severity: str              # companion_axis가 🔴이면 승격된 값이 들어온다
    fired: bool | None         # None = 데이터 없음(R3: 판정 불가는 이상이 아니다)
    actual: float | None
    distance: float | None     # 임계까지 남은 거리(approach) / 전제와의 격차(drift)
    detail: str
    action: str
    plan_b: str
    linked: list[str] = field(default_factory=list)
    escalated_by: str = ""     # 승격시킨 companion_axis slug


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
    early_warnings: list[EarlyWarningResult] = field(default_factory=list)

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

    @property
    def fired_early_warnings(self) -> list[EarlyWarningResult]:
        return [w for w in self.early_warnings if w.fired]


def _compare(key: str, op: str, value, as_of: date) -> tuple[bool | None, float | None]:
    actual = L._lookup(key, as_of)
    if actual is None:
        return None, None
    try:
        return OPS[op](actual, float(value)), actual
    except (KeyError, ValueError, TypeError):
        return None, actual


_SEVERITY_LADDER = ["opportunity", "warning", "critical"]


def _axis_is_red(slug: str) -> bool:
    """companion_axis(위키 digest)가 🔴 상태인지. 파일이 없거나 못 읽으면
    False — 없는 걸 위험으로 치면 매일 헛경보가 뜬다(R3)."""
    p = REPO / "data" / "wiki_digest" / f"{slug}.yaml"
    if not p.exists():
        return False
    try:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception:  # noqa: BLE001 — digest가 깨져도 실행계획 판정은 계속돼야 한다
        return False
    return "🔴" in str(d.get("status_label", ""))


def _evaluate_early_warning(w: dict, as_of: date) -> EarlyWarningResult:
    kind = w.get("type", "approach")
    severity = w.get("severity", "warning")
    escalated_by = ""

    companion = w.get("companion_axis")
    if companion and _axis_is_red(companion):
        idx = min(_SEVERITY_LADDER.index(severity) + 1, len(_SEVERITY_LADDER) - 1) \
            if severity in _SEVERITY_LADDER else len(_SEVERITY_LADDER) - 1
        severity = _SEVERITY_LADDER[idx]
        escalated_by = companion

    actual = L._lookup(w["watch_key"], as_of)
    if actual is None:
        return EarlyWarningResult(
            id=w["id"], name=w["name"], kind=kind, severity=severity,
            fired=None, actual=None, distance=None,
            detail=f"{w['watch_key']} 값을 구하지 못해 판정 불가",
            action=w.get("action", "").strip(), plan_b=w.get("plan_b", "").strip(),
            linked=list(w.get("linked", [])), escalated_by=escalated_by)

    if kind == "premise_drift":
        # 계획이 기대하는 전제에서 얼마나 벌어졌는지. 확인일이 지났으면
        # 그건 사전 경보가 아니라 CP 본판정의 몫이라 여기서는 끈다.
        target = float(w["premise_value"])
        op = w.get("premise_op", ">=")
        gap = (target - actual) if op in (">=", ">") else (actual - target)
        before_check = str(as_of) < str(w.get("check_date", "9999-12-31"))
        fired = bool(gap >= float(w["drift_margin"]) and before_check)
        detail = (f"{w['watch_key']} 실측 {actual:g} vs 전제 {op} {target:g} — "
                  f"{gap:+.2f} 벌어짐"
                  + (f" (확인일 {w['check_date']} 전)" if before_check
                     else f" (확인일 {w.get('check_date')} 경과 — CP 본판정으로 이관)"))
        return EarlyWarningResult(
            id=w["id"], name=w["name"], kind=kind, severity=severity,
            fired=fired, actual=actual, distance=gap, detail=detail,
            action=w.get("action", "").strip(), plan_b=w.get("plan_b", "").strip(),
            linked=list(w.get("linked", [])), escalated_by=escalated_by)

    threshold = float(w["threshold"])
    distance = (threshold - actual) if w.get("direction", "up") == "up" else (actual - threshold)
    fired = bool(distance <= float(w["warn_margin"]))
    detail = (f"{w['watch_key']} 실측 {actual:g}, 임계 {threshold:g}까지 "
              f"{distance:+.2f} 남음 (경보선 {w['warn_margin']})")
    return EarlyWarningResult(
        id=w["id"], name=w["name"], kind=kind, severity=severity,
        fired=fired, actual=actual, distance=distance, detail=detail,
        action=w.get("action", "").strip(), plan_b=w.get("plan_b", "").strip(),
        linked=list(w.get("linked", [])), escalated_by=escalated_by)


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
    #
    # ## 앞당김은 한 번에 하나만 (2026-09-14 추가 — 사용자 지시)
    #
    # 이전 구현은 가격이 임계를 넘으면 **그 임계를 넘는 모든** 미래
    # tranche를 동시에 ACCELERATED로 열었다. 주가가 2,500,000원이 되면
    # T2(2,000,000)·T3(2,200,000)·T4(2,400,000)가 같은 날 전부 열려
    # 사실상 "오늘 1.29억 전부 매도 가능"이 된다 — **분할 전환 원칙이
    # 급등 하루에 스스로 무너지는 경로**였다. 그 가격이 고점이 아니라
    # 통과점이었다면 나머지를 전부 싸게 판 셈이 된다.
    #
    # 임계를 벌리는 방법도 있지만 그건 동시 통과 "확률"을 낮출 뿐
    # 보장이 못 된다. 대신 순서를 구조로 막는다:
    #
    #   앞선 tranche가 전부 누적 하한선을 채운(DONE) 뒤에야
    #   뒤 tranche가 ACCELERATED로 열린다.
    #
    # ⚠️ **DUE에는 이 제약을 걸지 않는다.** 일정이 밀려 따라잡아야 하는
    # 상황까지 막으면 데드라인을 놓친다 — 앞당김(기회 포착)은 순서대로,
    # 만회(기한 방어)는 제한 없이.
    prior_all_done = True
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
            if prior_all_done:
                state = "ACCELERATED"
                note = (f"앞당김 조건 도달 (현재 {price:,.0f} ≥ {float(acc):,.0f}) — "
                        f"창({ws}) 이전이지만 실행 가능")
            else:
                # 가격 조건은 맞지만 차례가 아니다. 조건이 충족됐다는
                # 사실 자체는 숨기지 않는다 — 숨기면 왜 안 열렸는지
                # 사람이 알 수 없다.
                note = (f"앞당김 조건은 충족(현재 {price:,.0f} ≥ {float(acc):,.0f})했으나 "
                        f"앞선 tranche 미완료 — 분할 전환 유지를 위해 대기")

        if state != "DONE":
            prior_all_done = False

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

    # ── 사전 경보 ── 임계가 깨지기 전에 미리 뜬다(2026-09-22 신설)
    for w in plan.get("early_warnings", []):
        st.early_warnings.append(_evaluate_early_warning(w, as_of))

    return st
