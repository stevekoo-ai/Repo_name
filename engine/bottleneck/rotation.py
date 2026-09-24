"""병목 이동 추적 — 다음 병목 섹터를 단계별로 선제 매수하기 위한 일일 판정.

## 이 모듈이 답하는 질문

1. **현재 병목(HBM)이 풀리고 있나** — 풀릴수록 "하이닉스 하락" 시나리오가
   가까워진다(incumbent 신호).
2. **어느 후보가 다음 병목으로 조여지고 있나** — 후보마다 펀더멘털 2개
   (SEC 백로그·매출) + 주가 2개(상대강도·이평) 신호를 채점한다.
3. **그래서 지금 얼마를 사 둬야 하나** — 단계(정찰→구축→확정)별 누적 목표
   비중과 실제 매수 기록을 비교해 추가 매수액을 제안한다.

## 설계상 하지 않는 것

- **자동 매수하지 않는다.** 제안만 한다. 실제 주문은 사람이 내고
  `bottleneck_hedge_log.csv`에 기록한다.
- **하이닉스 매도를 지시하지 않는다.** 그건 R4 단일 출처
  (`engine/exporters/sk_hynix_decision.py`)의 몫이다.
- **데이터가 없으면 판정하지 않는다.** 없는 신호는 False가 아니라 None —
  단계 승격에 쓰이지 않고, 판정 불가로 드러난다(R3).
- **하루 튄 주가로 단계를 올리지 않는다.** 주가 신호는 오늘과
  persistence_days 전이 둘 다 성립해야 인정한다.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
CONFIG_FILE = REPO / "data" / "manual_inputs" / "bottleneck_rotation.yaml"
LOG_FILE = REPO / "data" / "manual_inputs" / "bottleneck_hedge_log.csv"
PRICES_FILE = REPO / "sources" / "bottleneck-prices.csv"
FUNDAMENTALS_FILE = REPO / "sources" / "ai-periphery-fundamentals.csv"
DIGEST_DIR = REPO / "data" / "wiki_digest"

_OPS = {">": lambda a, b: a > b, "<": lambda a, b: a < b,
        ">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b}


@dataclass
class SignalResult:
    id: str
    desc: str
    kind: str                 # fundamental | market | incumbent
    ok: bool | None           # None = 판정 불가
    detail: str
    forming: bool = False     # 오늘은 성립하나 지속성 미확인(주가 신호)


@dataclass
class CandidateResult:
    id: str
    name: str
    role: str                 # hedge | extension
    why: str
    signals: list[SignalResult]
    stage: int = 0
    stage_name: str = "관찰"
    stage_week_ago: int = 0
    capped_by: str | None = None
    target_krw: int = 0
    executed_krw: int = 0
    instruments_text: str = ""
    instruments: dict = field(default_factory=dict)
    unwind: bool = False
    next_hint: str = ""

    @property
    def score(self) -> int:
        return sum(1 for s in self.signals if s.ok)

    @property
    def unknown(self) -> list[SignalResult]:
        return [s for s in self.signals if s.ok is None]

    @property
    def gap_krw(self) -> int:
        return max(0, self.target_krw - self.executed_krw)


@dataclass
class RotationStatus:
    as_of: date
    budget_krw: int
    budget_confirmed: bool
    anchor_date: date
    anchor_label: str
    incumbent_name: str
    incumbent: list[SignalResult]
    candidates: list[CandidateResult]

    @property
    def incumbent_easing(self) -> int:
        return sum(1 for s in self.incumbent if s.ok)

    @property
    def lead(self) -> CandidateResult | None:
        hedges = [c for c in self.candidates if c.role == "hedge"]
        if not hedges:
            return None
        return max(hedges, key=lambda c: (c.stage, c.score))


# ── 데이터 로더 ────────────────────────────────────────────────

def load_config(path: Path | None = None) -> dict:
    return yaml.safe_load((path or CONFIG_FILE).read_text(encoding="utf-8")) or {}


def load_prices(path: Path | None = None) -> dict[str, list[tuple[date, float]]]:
    p = path or PRICES_FILE
    out: dict[str, list[tuple[date, float]]] = {}
    if not p.exists():
        return out
    with p.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                out.setdefault(r["ticker"], []).append((date.fromisoformat(r["date"]), float(r["close"])))
            except (KeyError, ValueError):
                continue
    for v in out.values():
        v.sort()
    return out


def load_fundamentals(path: Path | None = None) -> list[dict]:
    p = path or FUNDAMENTALS_FILE
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_log(path: Path | None = None) -> list[dict]:
    p = path or LOG_FILE
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r.get("date")]


def executed_by(candidate_id: str, as_of: date, log: list[dict]) -> int:
    total = 0
    for r in log:
        try:
            if r["candidate"] == candidate_id and date.fromisoformat(r["date"]) <= as_of:
                total += int(float(r["amount_krw"]))
        except (KeyError, ValueError):
            continue
    return total


# ── 주가 계산 ──────────────────────────────────────────────────

def _closes(prices: dict, ticker: str, as_of: date, stale_days: int) -> list[float] | None:
    series = [c for d, c in prices.get(ticker, []) if d <= as_of]
    last = [d for d, _ in prices.get(ticker, []) if d <= as_of]
    if not series or (as_of - last[-1]).days > stale_days:
        return None
    return series


def _ret(closes: list[float] | None, days: int) -> float | None:
    if not closes or len(closes) <= days:
        return None
    return (closes[-1] / closes[-1 - days] - 1) * 100


def _basket_ret(prices, basket, as_of, days, stale) -> float | None:
    rs = [_ret(_closes(prices, t, as_of, stale), days) for t in basket]
    rs = [r for r in rs if r is not None]
    # 바스켓 절반 미만만 데이터가 있으면 바스켓을 대표하지 못한다
    if not rs or len(rs) * 2 < len(basket):
        return None
    return sum(rs) / len(rs)


def _ma_majority(prices, basket, as_of, window, position, stale) -> tuple[bool | None, str]:
    hits, n = 0, 0
    for t in basket:
        c = _closes(prices, t, as_of, stale)
        if not c or len(c) < window:
            continue
        n += 1
        ma = sum(c[-window:]) / window
        if (c[-1] > ma) == (position == "above"):
            hits += 1
    if n == 0 or n * 2 < len(basket):
        return None, "주가 데이터 부족"
    return hits * 2 > n, f"{hits}/{n}종목"


# ── 펀더멘털 계산 ──────────────────────────────────────────────

def _yoy_series(rows: list[dict], ticker: str, metric: str, as_of: date,
                stale_days: int) -> list[tuple[date, float]] | None:
    vals: dict[date, float] = {}
    for r in rows:
        if r.get("ticker") != ticker or r.get("metric") != metric:
            continue
        try:
            if date.fromisoformat(r["filed_date"]) > as_of:
                continue  # 그 시점엔 아직 공시되지 않은 값
            vals[date.fromisoformat(r["end_date"])] = float(r["value_usd"])
        except (KeyError, ValueError):
            continue
    if not vals:
        return None
    ends = sorted(vals)
    if (as_of - ends[-1]).days > stale_days:
        return None  # 스테일 — 예: AMKR·LITE 백로그는 2021년에 멈춰 있다
    out = []
    for e in ends:
        prev = [p for p in ends if 330 <= (e - p).days <= 400]
        if prev and vals[prev[-1]]:
            out.append((e, (vals[e] / vals[prev[-1]] - 1) * 100))
    return out or None


def _majority(flags: list[bool | None]) -> bool | None:
    known = [f for f in flags if f is not None]
    if not known:
        return None
    return sum(known) * 2 > len(known)


# ── 신호 평가 ──────────────────────────────────────────────────

def _digest_collapse(slug: str, min_n: int) -> tuple[bool | None, str]:
    p = DIGEST_DIR / f"{slug}.yaml"
    try:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return None, f"{slug} 다이제스트 없음"
    m = re.search(r"붕괴조건\s*(\d)\s*/\s*5", str(d.get("status_label", "")))
    if not m:
        return None, "붕괴조건 개수 판독 불가"
    n = int(m.group(1))
    return n >= min_n, f"붕괴조건 {n}/5 ({d.get('as_of', '날짜 불명')})"


def _market_once(sig: dict, prices: dict, as_of: date, stale: int) -> tuple[bool | None, str]:
    if sig["type"] == "rel_return":
        a = _basket_ret(prices, sig["basket"], as_of, sig["days"], stale)
        b = _basket_ret(prices, [sig["vs"]], as_of, sig["days"], stale)
        if a is None or b is None:
            return None, "주가 데이터 부족"
        diff = a - b
        detail = f"{a:+.1f}% vs {sig['vs']} {b:+.1f}% (차 {diff:+.1f}%p)"
        ok = _OPS[sig["op"]](diff, sig["value"])
        # 덜 빠진 건 순환매가 아니다 — 2026-09-24 첫 실데이터에서 AI 섹터 전체가
        # 하락하는 중에 "전력이 하이닉스보다 덜 빠졌다"가 매수 신호로 켜지는
        # 오탐이 났다. min_abs가 있으면 후보 바스켓 자체 수익률도 그 이상이어야 한다.
        if ok and "min_abs" in sig and a < sig["min_abs"]:
            return False, detail + f" · 바스켓 자체가 {a:+.1f}%라 순환매 아님(동반 하락)"
        return ok, detail
    if sig["type"] == "ma_position":
        return _ma_majority(prices, sig["basket"], as_of, sig["window"], sig["position"], stale)
    raise ValueError(f"알 수 없는 주가 신호 type: {sig['type']}")


def evaluate_signal(sig: dict, kind: str, as_of: date, prices: dict,
                    fundamentals: list[dict], meta: dict) -> SignalResult:
    t = sig["type"]
    stale_f = meta.get("fundamental_stale_days", 200)
    stale_p = meta.get("price_stale_days", 7)

    if t == "digest_collapse":
        ok, detail = _digest_collapse(sig["slug"], sig["min"])
        return SignalResult(sig["id"], sig["desc"], kind, ok, detail)

    if t in ("rel_return", "ma_position"):
        now, detail = _market_once(sig, prices, as_of, stale_p)
        before, _ = _market_once(sig, prices, as_of - timedelta(days=meta.get("persistence_days", 7)), stale_p)
        if now is None:
            return SignalResult(sig["id"], sig["desc"], kind, None, detail)
        if now and before is not True:
            # 오늘 성립했지만 1주 전엔 아니었다(또는 모름) — 형성 중, 아직 인정 안 함
            return SignalResult(sig["id"], sig["desc"], kind, False, detail + " · 형성 중(지속성 미확인)", forming=True)
        return SignalResult(sig["id"], sig["desc"], kind, now, detail)

    if t in ("yoy_level", "yoy_accel"):
        flags, parts = [], []
        for tk in sig["tickers"]:
            ys = _yoy_series(fundamentals, tk, sig["metric"], as_of, stale_f)
            if not ys:
                flags.append(None)
                parts.append(f"{tk} 데이터 없음/스테일")
                continue
            if t == "yoy_level":
                v = ys[-1][1]
                flags.append(v >= sig["min_pct"])
                parts.append(f"{tk} {v:+.0f}%")
            else:
                if len(ys) < 2:
                    flags.append(None)
                    parts.append(f"{tk} 비교 분기 부족")
                    continue
                prev, cur = ys[-2][1], ys[-1][1]
                flags.append(cur > prev)
                parts.append(f"{tk} {prev:+.0f}%→{cur:+.0f}%")
        return SignalResult(sig["id"], sig["desc"], kind, _majority(flags), ", ".join(parts))

    raise ValueError(f"알 수 없는 신호 type: {t}")


# ── 단계 판정 ──────────────────────────────────────────────────

def _stage_for(signals: list[SignalResult], role: str, incumbent_easing: int,
               stages: list[dict]) -> int:
    score = sum(1 for s in signals if s.ok)
    kinds = {s.kind for s in signals if s.ok}
    best = 0
    for st in sorted(stages, key=lambda s: s["stage"]):
        if score < st["min_score"]:
            continue
        if st.get("require_both_kinds") and not {"fundamental", "market"} <= kinds:
            continue
        if role == "hedge" and incumbent_easing < st.get("min_incumbent", 0):
            continue
        best = st["stage"]
    return best


def _next_hint(signals: list[SignalResult], role: str, stage: int, easing: int,
               stages: list[dict]) -> str:
    nxt = next((s for s in sorted(stages, key=lambda s: s["stage"]) if s["stage"] > stage), None)
    if not nxt:
        return "최종 단계"
    score = sum(1 for s in signals if s.ok)
    kinds = {s.kind for s in signals if s.ok}
    need = []
    if score < nxt["min_score"]:
        need.append(f"신호 {nxt['min_score'] - score}개 더")
    if nxt.get("require_both_kinds"):
        for k, label in (("fundamental", "펀더멘털"), ("market", "주가")):
            if k not in kinds:
                need.append(f"{label} 신호 1개 이상")
    if role == "hedge" and easing < nxt.get("min_incumbent", 0):
        need.append(f"현재 병목 약화 신호 {nxt['min_incumbent'] - easing}개 더")
    return f"{nxt['stage']}단계({nxt['name']})까지: " + (", ".join(need) or "조건 충족 — 다음 평가에서 반영")


def _evaluate_at(cfg: dict, as_of: date, prices: dict, fundamentals: list[dict]):
    meta = cfg.get("meta") or {}
    inc_cfg = cfg.get("incumbent") or {}
    incumbent = [evaluate_signal(s, "incumbent", as_of, prices, fundamentals, meta)
                 for s in inc_cfg.get("signals") or []]
    easing = sum(1 for s in incumbent if s.ok)
    stages = cfg.get("stages") or []

    cands = []
    for c in cfg.get("candidates") or []:
        sigs = [evaluate_signal(s, s["kind"], as_of, prices, fundamentals, meta)
                for s in c.get("signals") or []]
        stage = _stage_for(sigs, c.get("role", "hedge"), easing, stages)
        cands.append((c, sigs, stage))

    # extension(메모리 용량)이 강하면 헤지 상한을 건다
    cap = cfg.get("extension_caps_hedge") or {}
    ext_stage = max((st for c, _, st in cands if c.get("role") == "extension"), default=0)
    capped = {}
    if cap and ext_stage >= cap.get("when_extension_stage_at_least", 99):
        for c, _, st in cands:
            if c.get("role") == "hedge" and st > cap["hedge_max_stage"]:
                capped[c["id"]] = f"메모리 용량 병목 {ext_stage}단계 — 헤지 {cap['hedge_max_stage']}단계 상한"
    return incumbent, cands, capped


def evaluate(as_of: date, cfg: dict | None = None, prices: dict | None = None,
             fundamentals: list[dict] | None = None, log: list[dict] | None = None) -> RotationStatus:
    cfg = cfg if cfg is not None else load_config()
    prices = prices if prices is not None else load_prices()
    fundamentals = fundamentals if fundamentals is not None else load_fundamentals()
    log = log if log is not None else load_log()
    meta = cfg.get("meta") or {}
    budget = int(meta.get("hedge_budget_krw", 0))
    stages = {s["stage"]: s for s in cfg.get("stages") or []}

    incumbent, cands, capped = _evaluate_at(cfg, as_of, prices, fundamentals)
    week_ago = as_of - timedelta(days=meta.get("persistence_days", 7))
    _, cands_before, capped_before = _evaluate_at(cfg, week_ago, prices, fundamentals)
    cap_max = (cfg.get("extension_caps_hedge") or {}).get("hedge_max_stage")
    before = {c["id"]: (cap_max if c["id"] in capped_before else st) for c, _, st in cands_before}
    unwind_max = (cfg.get("unwind") or {}).get("max_score", 1)
    score_before = {c["id"]: sum(1 for s in sigs if s.ok) for c, sigs, _ in cands_before}

    results = []
    for c, sigs, stage in cands:
        cap_note = capped.get(c["id"])
        if cap_note:
            stage = (cfg.get("extension_caps_hedge") or {})["hedge_max_stage"]
        st = stages.get(stage, {})
        r = CandidateResult(
            id=c["id"], name=c["name"], role=c.get("role", "hedge"), why=c.get("why", ""),
            signals=sigs, stage=stage, stage_name=st.get("name", "관찰"),
            stage_week_ago=before.get(c["id"], 0), capped_by=cap_note,
            instruments_text=st.get("instruments", ""), instruments=c.get("instruments") or {},
            next_hint=_next_hint(sigs, c.get("role", "hedge"), stage,
                                 sum(1 for s in incumbent if s.ok), cfg.get("stages") or []),
        )
        if r.role == "hedge":
            r.target_krw = int(budget * float(c.get("budget_weight", 0)) * st.get("cum_pct", 0) / 100)
            r.executed_krw = executed_by(c["id"], as_of, log)
            r.unwind = (r.executed_krw > 0 and r.score <= unwind_max
                        and score_before.get(c["id"], 0) <= unwind_max)
        results.append(r)

    return RotationStatus(
        as_of=as_of, budget_krw=budget, budget_confirmed=bool(meta.get("budget_confirmed")),
        anchor_date=date.fromisoformat(str(meta.get("anchor_date", "2027-04-01"))),
        anchor_label=meta.get("anchor_label", ""),
        incumbent_name=(cfg.get("incumbent") or {}).get("name", "현재 병목"),
        incumbent=incumbent, candidates=results,
    )


# ── 렌더링 (브리핑 팩·daily report 공용) ─────────────────────────

_ICON = {True: "✅", False: "❌", None: "❓"}


def _sig_line(s: SignalResult) -> str:
    icon = "⏳" if s.forming else _ICON[s.ok]
    return f"  - {icon} {s.id} {s.desc} — {s.detail}"


def _instrument_names(c: CandidateResult) -> str:
    etf = [f"{i['name']}({i['ticker']})" for i in c.instruments.get("etf") or []]
    lead = [f"{i['name']}({i['ticker']})" for i in c.instruments.get("leaders") or []]
    parts = []
    if etf:
        parts.append("ETF: " + ", ".join(etf))
    if lead:
        parts.append("대장주: " + ", ".join(lead))
    return " / ".join(parts)


def render_markdown(st: RotationStatus, compact: bool = False) -> str:
    lines: list[str] = []
    d_day = (st.anchor_date - st.as_of).days
    lead = st.lead
    if lead:
        lines.append(f"**가장 앞선 다음 병목 후보: {lead.id} {lead.name} — "
                     f"{lead.stage}단계({lead.stage_name}), 신호 {lead.score}/{len(lead.signals)}**")
    lines.append(f"기준 이벤트: {st.anchor_label} (D-{d_day}, {st.anchor_date}) · "
                 f"헤지 예산 {st.budget_krw:,}원" + ("" if st.budget_confirmed else " (잠정 — 예산·배분은 진행하며 결정)"))

    # 단계 변화 알림을 맨 위에
    changes = [c for c in st.candidates if c.stage != c.stage_week_ago]
    for c in changes:
        arrow = "🔔 승격" if c.stage > c.stage_week_ago else "⬇️ 하락"
        lines.append(f"{arrow}: {c.id} {c.name} {c.stage_week_ago}단계 → **{c.stage}단계({c.stage_name})** (1주 전 대비)")

    lines.append(f"\n**현재 병목({st.incumbent_name}) 약화 신호 {st.incumbent_easing}/{len(st.incumbent)}** "
                 "— 켜질수록 '병목 해소 → 하이닉스 하락' 시나리오가 가까워진다")
    if not compact:
        lines += [_sig_line(s) for s in st.incumbent]

    for c in st.candidates:
        tag = "헤지 후보" if c.role == "hedge" else "현재 병목의 연장(하이닉스가 이어받음)"
        lines.append(f"\n**{c.id} {c.name}** [{tag}] — {c.stage}단계({c.stage_name}), 신호 {c.score}/{len(c.signals)}")
        if not compact:
            lines += [_sig_line(s) for s in c.signals]
        if c.unknown:
            lines.append(f"  - ⚠️ 판정 불가 {len(c.unknown)}개(데이터 없음 — 승격 근거로 쓰지 않음): "
                         + ", ".join(s.id for s in c.unknown))
        if c.capped_by:
            lines.append(f"  - 🔒 {c.capped_by}")
        if c.role == "hedge":
            lines.append(f"  - 목표 누적 {c.target_krw:,}원 / 실행 {c.executed_krw:,}원")
            if c.unwind:
                lines.append("  - 🧯 **철회 검토**: 매수분이 있는데 신호가 1주째 꺼져 있다 — "
                             "추가 매수 중단, 보유분 재검토(자동 매도 아님)")
            elif c.gap_krw > 0:
                lines.append(f"  - 👉 **제안: {c.gap_krw:,}원 추가 매수** — {c.instruments_text}")
                lines.append(f"    수단: {_instrument_names(c)}")
            elif c.stage == 0:
                lines.append("  - 관찰 — 매수 없음")
        elif c.stage >= 2:
            lines.append("  - 메모리가 여전히 병목 — 하이닉스 보유 논리 강화, 헤지를 끝까지 채울 이유가 줄어듦")
        if c.next_hint:
            lines.append(f"  - 다음: {c.next_hint}")
    lines.append("\n> 판정만 한다 — 자동 매수·매도 없음. 하이닉스 자체의 매도 지시는 "
                 "sk_hynix_decision(R4) 단일 출처를 따른다. 실제 매수 시 "
                 "`data/manual_inputs/bottleneck_hedge_log.csv`에 기록해야 목표 대비 진척이 반영된다.")
    return "\n".join(lines)
