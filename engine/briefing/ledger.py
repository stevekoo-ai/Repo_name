"""예측 원장 — 브리핑을 "요약문"이 아니라 "공부 파트너"로 만드는 장치.

## 왜 필요한가

매일 잘 쓴 요약을 받아도, 그게 맞았는지 아무도 안 따지면 **매일 새로
시작하는 감상문**이다. 이 저장소는 이미 그 교훈을 한 번 배웠다 — FRS의
전환 경고 감지기 4종을 만들고 나서 **리프트를 측정**했더니 하나(모멘텀
반전)는 기저율보다도 나빴다. 측정하지 않았으면 넷을 같은 무게로 읽었을
것이다.

같은 방법을 일일 판단에 적용한다. 매 브리핑이 **반증 가능한 예측**을
남기고, 다음 브리핑이 그걸 **데이터로 채점**한다. 누적되면 "내 판단의 어느
축이 자꾸 틀리는가"가 감이 아니라 표로 나온다.

## 왜 자동 채점이 가능한가

이 저장소엔 일별로 갱신되는 시계열이 16개(macro-series) + KIS 6종 있다.
예측을 **그 키와 임계로** 적으면 코드가 판정할 수 있다:

    check_key: us_10y      check_op: ">="   check_value: 5.0
    → 검증일에 us_10y가 5.0 이상이면 적중

자유문 예측은 채점이 불가능하므로 **받지 않는다**. 그 제약이 예측을
날카롭게 만든다.
"""
from __future__ import annotations

import csv
import operator
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "data" / "predictions" / "ledger.csv"

FIELDS = ["id", "issued_at", "slot", "claim", "check_date", "check_key",
          "check_op", "check_value", "status", "result", "resolved_at", "note"]

OPS = {">=": operator.ge, "<=": operator.le, ">": operator.gt,
       "<": operator.lt, "==": operator.eq}

# 채점에 쓸 수 있는 데이터 소스. 여기 없는 키는 예측으로 받지 않는다.
SERIES_SOURCES = {
    "macro": REPO / "sources" / "macro-series.csv",
}
KIS_SOURCES = {
    "hynix_close": ("sk-hynix-price-snapshot.csv", 2),
    "hynix_chg_pct": ("sk-hynix-price-snapshot.csv", 4),
    "hynix_foreign_pct": ("sk-hynix-price-snapshot.csv", 6),
    "hynix_adr_chg": ("sk-hynix-adr-quote.csv", 4),
}


@dataclass
class Prediction:
    id: str
    issued_at: str
    slot: str
    claim: str
    check_date: str
    check_key: str
    check_op: str
    check_value: str
    status: str = "OPEN"        # OPEN | HIT | MISS | UNVERIFIABLE
    result: str = ""
    resolved_at: str = ""
    note: str = ""


def _read() -> list[Prediction]:
    if not LEDGER.exists():
        return []
    with LEDGER.open(encoding="utf-8") as fh:
        return [Prediction(**{k: r.get(k, "") for k in FIELDS})
                for r in csv.DictReader(fh)]


def _write(rows: list[Prediction]) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(asdict(r))


def next_id(rows: list[Prediction] | None = None) -> str:
    rows = _read() if rows is None else rows
    n = 0
    for r in rows:
        if r.id.startswith("P"):
            try:
                n = max(n, int(r.id[1:]))
            except ValueError:
                continue
    return f"P{n + 1:04d}"


def add(claim: str, check_date: str, check_key: str, check_op: str,
        check_value: str, slot: str, issued_at: str) -> Prediction:
    """예측을 원장에 추가한다. 채점 가능한 형태만 받는다."""
    if check_op not in OPS:
        raise ValueError(f"지원하지 않는 연산자: {check_op} (가능: {list(OPS)})")
    rows = _read()
    p = Prediction(id=next_id(rows), issued_at=issued_at, slot=slot, claim=claim,
                   check_date=check_date, check_key=check_key,
                   check_op=check_op, check_value=str(check_value))
    rows.append(p)
    _write(rows)
    return p


def _lookup(key: str, on: date) -> float | None:
    """검증일 기준 값. **그 날짜 이하의 마지막 값**을 쓴다 — 휴장·발표지연이
    있는 계열에서 "그날 정확히" 값을 요구하면 대부분 채점 불가가 된다."""
    if key in KIS_SOURCES:
        fname, col = KIS_SOURCES[key]
        p = REPO / "sources" / fname
        if not p.exists():
            return None
        with p.open(encoding="utf-8") as fh:
            rows = [r for r in csv.reader(fh)][1:]
        rows = [r for r in rows if r and r[0] <= on.isoformat()]
        if not rows:
            return None
        try:
            return float(rows[-1][col])
        except (ValueError, IndexError):
            return None
    p = SERIES_SOURCES["macro"]
    if not p.exists():
        return None
    best = None
    with p.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["series"] != key or r["date"] > on.isoformat():
                continue
            if best is None or r["date"] > best[0]:
                try:
                    best = (r["date"], float(r["value"]))
                except (ValueError, TypeError):
                    continue
    return best[1] if best else None


def resolve_due(as_of: date) -> list[Prediction]:
    """검증일이 도래한 OPEN 예측을 채점한다. 채점된 것만 돌려준다.

    값을 못 찾으면 MISS가 아니라 **UNVERIFIABLE**이다 — 데이터가 없는 걸
    "틀렸다"로 기록하면 적중률 통계가 오염된다(R3)."""
    rows = _read()
    resolved: list[Prediction] = []
    for r in rows:
        if r.status != "OPEN" or not r.check_date or r.check_date > as_of.isoformat():
            continue
        actual = _lookup(r.check_key, as_of)
        r.resolved_at = as_of.isoformat()
        if actual is None:
            r.status = "UNVERIFIABLE"
            r.result = ""
            r.note = f"{r.check_key} 값을 찾지 못함"
        else:
            try:
                hit = OPS[r.check_op](actual, float(r.check_value))
            except (ValueError, KeyError):
                r.status, r.note = "UNVERIFIABLE", "임계값 해석 실패"
                resolved.append(r)
                continue
            r.status = "HIT" if hit else "MISS"
            r.result = f"{actual:g}"
        resolved.append(r)
    if resolved:
        _write(rows)
    return resolved


def open_predictions(as_of: date) -> list[Prediction]:
    return [r for r in _read() if r.status == "OPEN"]


def scoreboard() -> dict:
    """누적 적중률. UNVERIFIABLE은 분모에서 뺀다."""
    rows = _read()
    hit = sum(1 for r in rows if r.status == "HIT")
    miss = sum(1 for r in rows if r.status == "MISS")
    unver = sum(1 for r in rows if r.status == "UNVERIFIABLE")
    total = hit + miss
    return {"hit": hit, "miss": miss, "unverifiable": unver, "open":
            sum(1 for r in rows if r.status == "OPEN"),
            "accuracy": (hit / total * 100) if total else None}
