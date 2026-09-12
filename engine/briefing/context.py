"""브리핑 팩 — LLM이 **위키 대신 읽는** 크기 고정 컨텍스트.

## 왜 이게 필요한가

사용자가 겪은 두 실패:
  1. 위키·기존 리포트를 전부 넣기 → context 폭발 → 내용이 부실해짐
  2. 아주 간단히만 → 원하는 보고서가 아님

둘 다 같은 원인이다 — **선별 계층이 없어서** "전부 아니면 아무것도" 두 극단
밖에 없었다. 실측하면 이유가 분명하다:

    위키 268페이지 6.8MB   → 통째로 읽는 건 애초에 불가능
    리포트 1개 40,415자    → 약 27,000토큰. 이것만으로 예산이 날아간다
    digest 5개 약 4,000자  → 약 2,700토큰

그래서 이 모듈은 **크기가 고정된 팩**을 만든다. 위키가 500페이지가 돼도
팩 크기는 안 변한다 — 요약이 아니라 **선별**이기 때문이다. 오늘 안 고른
페이지는 잃는 게 아니라 다음에 고르면 된다.

## 규칙

- LLM은 `wiki/`를 직접 읽지 않는다. 이 팩만 읽는다.
- 팩의 모든 숫자는 **코드가 계산**한다. LLM이 만드는 건 서사와 판단뿐.
- 미수집은 "없음"으로 명시한다. 조용히 빼면 LLM이 있는 줄 알고 지어낸다(R3).
"""
from __future__ import annotations

import csv
import glob
import os
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
KST = timezone(timedelta(hours=9))

# 팩의 크기 상한(문자). 넘으면 잘라내고 잘렸다고 표기한다 —
# 조용히 넘치면 그날 리포트만 이상해지고 원인을 못 찾는다.
MAX_PACK_CHARS = 24_000

# digest 선별 개수. 늘리면 팩이 커지고 줄이면 맥락이 얇아진다.
DIGEST_SLOTS = 5


@dataclass
class Block:
    key: str
    title: str
    body: str
    chars: int = 0

    def __post_init__(self):
        self.chars = len(self.body)


@dataclass
class BriefingPack:
    slot: str                    # "AM" | "PM"
    as_of: datetime              # KST
    blocks: list[Block] = field(default_factory=list)

    @property
    def chars(self) -> int:
        return sum(b.chars for b in self.blocks)

    def render(self) -> str:
        head = (f"# 브리핑 팩 — {self.slot} ({self.as_of.strftime('%Y-%m-%d %H:%M')} KST)\n\n"
                f"> 이 파일은 코드가 생성했다. 여기 없는 숫자는 **없는 것이다** — "
                f"위키나 기억에서 끌어와 채우지 말 것.\n")
        parts = [head]
        for b in self.blocks:
            parts.append(f"\n## {b.title}\n\n{b.body}\n")
        out = "".join(parts)
        if len(out) > MAX_PACK_CHARS:
            out = out[:MAX_PACK_CHARS] + (
                f"\n\n⚠️ 팩이 상한({MAX_PACK_CHARS:,}자)을 넘어 잘렸다 — "
                "선별 규칙을 좁혀야 한다.\n")
        return out


# ─────────────────────────────────────────────────────────────
# 블록 ① 오늘의 실측 팩트시트
# ─────────────────────────────────────────────────────────────
def _series_map() -> dict[str, list[tuple[str, float]]]:
    path = REPO / "sources" / "macro-series.csv"
    out: dict[str, list[tuple[str, float]]] = {}
    if not path.exists():
        return out
    with path.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                out.setdefault(r["series"], []).append((r["date"], float(r["value"])))
            except (ValueError, TypeError):
                continue
    for k in out:
        out[k].sort()
    return out


def _change(rows: list[tuple[str, float]], days: int) -> tuple[float, float, str] | None:
    """(최신값, 변화율%, 최신일). days 영업일 전 대비."""
    if len(rows) < 2:
        return None
    last_d, last_v = rows[-1]
    idx = max(0, len(rows) - 1 - days)
    prev_v = rows[idx][1]
    if prev_v == 0:
        return None
    return last_v, (last_v / prev_v - 1) * 100, last_d


# 팩트시트에 싣는 지표. (키, 표시명, 단위, 변화 표기 방식)
FACT_SERIES = [
    ("us_nasdaq", "나스닥", "", "pct"),
    ("us_sp500", "S&P500", "", "pct"),
    ("us_vix", "VIX", "", "level"),
    ("us_10y", "미 10년물", "%", "bp"),
    ("us_2y", "미 2년물", "%", "bp"),
    ("us_3m", "미 3개월물", "%", "bp"),
    ("us_hy_oas", "하이일드 스프레드", "%p", "bp"),
    ("us_dollar_index", "달러지수", "", "pct"),
    ("us_brent", "브렌트유", "$", "pct"),
    ("kr_usdkrw", "원/달러(ECOS)", "원", "pct"),
]


def build_fact_sheet(as_of: date) -> Block:
    m = _series_map()
    lines = ["| 지표 | 최신 | 1일 | 5일 | 기준일 |", "|---|---:|---:|---:|---|"]
    missing = []
    for key, label, unit, mode in FACT_SERIES:
        rows = [(d, v) for d, v in m.get(key, []) if d <= as_of.isoformat()]
        if len(rows) < 2:
            missing.append(label)
            continue
        last_v, d1, last_d = _change(rows, 1) or (None, None, None)
        _, d5, _ = _change(rows, 5) or (None, None, None)
        age = (as_of - date.fromisoformat(last_d)).days
        stale = f" ⚠️{age}일 지연" if age >= 3 else ""

        def fmt(pct):
            if pct is None:
                return "—"
            if mode == "bp":
                return f"{pct * last_v / 100 * 100:+.0f}bp" if last_v else "—"
            if mode == "level":
                return f"{pct:+.1f}%"
            return f"{pct:+.2f}%"

        lines.append(f"| {label} | {last_v:,.2f}{unit} | {fmt(d1)} | {fmt(d5)} | {last_d}{stale} |")
    body = "\n".join(lines)
    if missing:
        body += f"\n\n**미수집**: {', '.join(missing)} — 없는 것이므로 언급하지 말 것."
    return Block("facts", "① 오늘의 실측 (macro-series.csv)", body)


def build_hynix_block(as_of: date) -> Block:
    """KIS 실측 — 하이닉스 시세·수급·신용·공매도·ADR."""
    def tail(name: str, n: int = 1) -> list[list[str]]:
        p = REPO / "sources" / f"{name}.csv"
        if not p.exists():
            return []
        with p.open(encoding="utf-8") as fh:
            rows = [r for r in csv.reader(fh) if r]
        body = [r for r in rows[1:] if r and r[0] <= as_of.isoformat()]
        return body[-n:]

    lines = []
    snap = tail("sk-hynix-price-snapshot")
    if snap:
        r = snap[-1]
        lines.append(f"- **종가** {r[0]}: {int(float(r[2])):,}원 "
                     f"({float(r[4]):+.2f}%), 외국인 보유율 {r[6]}%")
    flow = tail("sk-hynix-investor-flow", 5)
    if flow:
        try:
            frn = sum(float(r[5]) for r in flow) / 1e12
            org = sum(float(r[6]) for r in flow) / 1e12
            ind = sum(float(r[7]) for r in flow) / 1e12
            lines.append(f"- **최근 5거래일 순매수**: 외국인 {frn:+.2f}조 / "
                         f"기관 {org:+.2f}조 / 개인 {ind:+.2f}조")
        except (ValueError, IndexError):
            pass
    adr = tail("sk-hynix-adr-quote")
    if adr:
        r = adr[-1]
        lines.append(f"- **ADR** {r[0]}: ${r[2]} ({float(r[4]):+.2f}%) "
                     f"← 밤사이 미국 반응의 직접 지표")
    credit = tail("sk-hynix-credit-balance", 2)
    if len(credit) == 2:
        try:
            delta = float(credit[-1][2]) - float(credit[-2][2])
            lines.append(f"- **신용융자잔고** {credit[-1][0]}: "
                         f"{int(float(credit[-1][2])):,}주 ({delta:+,.0f})")
        except (ValueError, IndexError):
            pass
    if not lines:
        lines = ["- (KIS 수집 데이터 없음 — 브랜치가 main과 갈라졌는지 확인할 것)"]
    return Block("hynix", "② SK하이닉스 실측 (KIS)", "\n".join(lines))


# ─────────────────────────────────────────────────────────────
# 블록 ③ 위키 digest 선별 — 이 팩의 핵심 아이디어
# ─────────────────────────────────────────────────────────────
def _load_digests() -> list[dict]:
    out = []
    for f in sorted(glob.glob(str(REPO / "data" / "wiki_digest" / "*.yaml"))):
        try:
            d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if d.get("one_line_summary"):
            d["slug"] = os.path.basename(f)[:-5]
            out.append(d)
    return out


def select_digests(as_of: date, triggers: set[str], slots: int = DIGEST_SLOTS) -> list[dict]:
    """오늘 읽힐 digest를 고른다 — **요약이 아니라 선별**이다.

    위키가 커져도 팩 크기가 안 커지는 이유가 여기 있다. 오늘 안 고른
    페이지는 잃는 게 아니라 다음에 고르면 된다.

    규칙(우선순위 순):
      1. 오늘 켜진 트리거에 대응하는 digest — 실제로 움직인 것
      2. 남는 자리는 **가장 오래 안 읽힌 순**으로 채운다(로테이션)

    2번이 없으면 조용한 축은 영원히 안 읽히고, 그 축이 조용히 썩는다.
    실제로 이 저장소의 monitoring 페이지 절반이 3주 이상 미갱신이었다.
    """
    digests = _load_digests()
    by_slug = {d["slug"]: d for d in digests}
    chosen: list[dict] = []

    for slug in TRIGGER_TO_DIGEST_ORDER:
        if slug in triggers and slug in by_slug and by_slug[slug] not in chosen:
            chosen.append(by_slug[slug])
        if len(chosen) >= slots:
            return chosen[:slots]

    # 로테이션 — as_of가 오래된 순
    rest = sorted((d for d in digests if d not in chosen),
                  key=lambda d: str(d.get("as_of", "")))
    chosen.extend(rest[: slots - len(chosen)])
    return chosen[:slots]


# 트리거 이름 = digest slug. 우선순위는 이 순서대로.
TRIGGER_TO_DIGEST_ORDER = [
    "fx-regime-score",
    "hbm-cycle-score",
    "sk-hynix-analyst-thesis-checkpoints",
    "market-cycles-leverage-risk",
    "panic-recovery-signals",
    "semiconductor-export-peak-recovery",
    "kospi-valuation-tracker",
    "macro-regime-history",
    "trump-midterm-tracker",
    "data-center-construction-vs-opposition",
    "situational-awareness-fund-liquidation",
    "sk-hynix-decision-tracker",
    "rate-outlook-scenario",
]


def detect_triggers(as_of: date) -> tuple[set[str], list[str]]:
    """오늘 무엇이 움직였나 → (digest 트리거 집합, 사람이 읽는 사유 목록).

    이 판정이 곧 §블록③의 선별 근거이자 §게이트의 입력이다."""
    fired: set[str] = set()
    why: list[str] = []
    m = _series_map()

    def rows(key):
        return [(d, v) for d, v in m.get(key, []) if d <= as_of.isoformat()]

    # FX 국면 — 경고가 켜졌거나 이격이 큰가
    try:
        from engine.fx.regime_score import calculate_frs, ma36_gap
        from engine.fx.transition import evaluate
        from collectors.manual import fetch_fx_risk_events
        ev = fetch_fx_risk_events()
        rep = evaluate(as_of, ev)
        if rep.count:
            fired.add("fx-regime-score")
            why.append(f"FX 전환 경고 {rep.count}/4 ({rep.trigger_kind.value})")
        g = ma36_gap(as_of)
        if g and abs(g[2]) >= 5:
            fired.add("fx-regime-score")
            why.append(f"원/달러 MA36 이격 {g[2]:+.1f}%")
    except Exception:
        pass

    # 하이닉스 급변
    snap = REPO / "sources" / "sk-hynix-price-snapshot.csv"
    if snap.exists():
        with snap.open(encoding="utf-8") as fh:
            body = [r for r in csv.reader(fh)][1:]
        body = [r for r in body if r and r[0] <= as_of.isoformat()]
        if body:
            try:
                chg = float(body[-1][4])
                if abs(chg) >= 3.0:
                    fired |= {"hbm-cycle-score", "sk-hynix-analyst-thesis-checkpoints"}
                    why.append(f"SK하이닉스 {chg:+.2f}%")
            except (ValueError, IndexError):
                pass

    # 미 장기금리 급등 — 국면 종료 트리거이자 장기채 경계
    r10 = rows("us_10y")
    if len(r10) > 20:
        chg = r10[-1][1] - r10[-21][1]
        if abs(chg) >= 0.25:
            fired.add("macro-regime-history")
            why.append(f"미 10년물 20일 {chg:+.2f}%p")

    # 위험선호 급변
    rv = rows("us_vix")
    if len(rv) > 5 and rv[-6][1]:
        chg = (rv[-1][1] / rv[-6][1] - 1) * 100
        if abs(chg) >= 20:
            fired |= {"market-cycles-leverage-risk", "panic-recovery-signals"}
            why.append(f"VIX 5일 {chg:+.0f}%")

    # 금리 전망 3대 시나리오 — 한은 기준금리 변동(디커플링 축 직접 증거)
    # 또는 FOMC/금통위가 임박했을 때(±3일) 켜진다. 2026-09-12
    # rate-outlook-scenarios-2026 참고.
    rb = rows("kr_base_rate")
    if len(rb) >= 2 and rb[-1][1] != rb[-2][1]:
        fired.add("rate-outlook-scenario")
        why.append(f"한국 기준금리 변동 {rb[-2][1]:.2f}→{rb[-1][1]:.2f}")
    try:
        from engine.briefing import calendar as C
        for ev in C.upcoming_events(as_of, horizon_days=3):
            if ev.get("type") in ("FOMC", "BOK"):
                fired.add("rate-outlook-scenario")
                why.append(f"{ev['date']} {ev['name']} 임박")
                break
    except Exception:
        pass

    return fired, why


def build_digest_block(as_of: date, triggers: set[str], why: list[str]) -> Block:
    chosen = select_digests(as_of, triggers)
    lines = []
    if why:
        lines.append(f"**오늘 켜진 신호**: {' · '.join(why)}\n")
    for d in chosen:
        age = ""
        try:
            days = (as_of - date.fromisoformat(str(d.get("as_of")))).days
            if days >= 7:
                age = f" ⚠️{days}일 전 판단"
        except (ValueError, TypeError):
            age = " ⚠️날짜 불명"
        lines.append(f"### {d.get('status_label', d['slug'])}{age}\n"
                     f"{str(d['one_line_summary']).strip()}\n"
                     f"→ `{d.get('monitoring_page', '')}`\n")
    return Block("digests", f"③ 위키 추적 신호 (선별 {len(chosen)}건)", "\n".join(lines))


# ─────────────────────────────────────────────────────────────
# 블록 ④ 직전 브리핑의 결론만 / 블록 ⑤ 예측 원장
# ─────────────────────────────────────────────────────────────
BRIEF_DIR = REPO / "report" / "briefing"


def build_previous_block(as_of: date, slot: str) -> Block:
    """직전 브리핑의 **결론 섹션만**. 전문을 넣으면 예산이 날아간다
    (리포트 1개가 약 27,000토큰)."""
    if not BRIEF_DIR.exists():
        return Block("previous", "④ 직전 브리핑", "(이전 브리핑 없음 — 첫 발행)")
    files = sorted(BRIEF_DIR.glob("*.md"))
    files = [f for f in files if f.stem[:10] <= as_of.isoformat()]
    if not files:
        return Block("previous", "④ 직전 브리핑", "(이전 브리핑 없음 — 첫 발행)")
    text = files[-1].read_text(encoding="utf-8")
    marker = "## 결론"
    body = text.split(marker, 1)[1].strip() if marker in text else text[-800:]
    body = body[:1200]
    return Block("previous", f"④ 직전 브리핑 결론 ({files[-1].stem})", body)


def build_ledger_block(as_of: date) -> Block:
    from engine.briefing import ledger as L

    resolved = L.resolve_due(as_of)
    open_rows = L.open_predictions(as_of)
    sb = L.scoreboard()

    lines = []
    if resolved:
        lines.append("**오늘 채점된 예측** — 빗나간 게 있으면 왜 틀렸는지 쓰는 게 오늘의 핵심이다.\n")
        for r in resolved:
            mark = {"HIT": "✅", "MISS": "❌", "UNVERIFIABLE": "⚪"}.get(r.status, "?")
            lines.append(f"- {mark} `{r.id}` {r.claim} "
                         f"(기준 {r.check_key} {r.check_op} {r.check_value} / 실측 {r.result or '없음'})")
        lines.append("")
    else:
        lines.append("오늘 검증일이 도래한 예측: 없음\n")

    if open_rows:
        lines.append("**열린 예측**")
        for r in open_rows[:8]:
            lines.append(f"- `{r.id}` ({r.check_date} 검증) {r.claim}")
        lines.append("")

    acc = f"{sb['accuracy']:.0f}%" if sb["accuracy"] is not None else "—"
    lines.append(f"**누적**: 적중 {sb['hit']} / 빗나감 {sb['miss']} / "
                 f"채점불가 {sb['unverifiable']} / 열림 {sb['open']} → 적중률 {acc}")
    return Block("ledger", "⑤ 예측 원장", "\n".join(lines))


# ─────────────────────────────────────────────────────────────
# 게이트 — 조용한 날엔 조용히
# ─────────────────────────────────────────────────────────────
@dataclass
class Gate:
    publish: bool
    reasons: list[str]

    @property
    def verdict(self) -> str:
        return "발행" if self.publish else "조용한 날"


def evaluate_gate(as_of: date, triggers: set[str], why: list[str]) -> Gate:
    """LLM을 부르기 전에 **코드가** 발행 여부를 정한다.

    사용자가 Routine을 정지시킨 이유가 "대충 만드는데 토큰이 아깝다"였다.
    매일 억지로 뭔가 쓰게 하면 내용이 묽어지고 비용만 든다 — 쓸 게 있는
    날에만 쓰는 게 품질과 비용 양쪽에 낫다."""
    from engine.briefing import ledger as L

    reasons = list(why)
    if L.open_predictions(as_of):
        due = [r for r in L.open_predictions(as_of) if r.check_date <= as_of.isoformat()]
        if due:
            reasons.append(f"검증일 도래 예측 {len(due)}건")
    m = _series_map()
    for key, label in (("us_nasdaq", "나스닥"), ("kr_usdkrw", "원/달러")):
        rows = [(d, v) for d, v in m.get(key, []) if d <= as_of.isoformat()]
        if len(rows) >= 2 and rows[-2][1]:
            chg = (rows[-1][1] / rows[-2][1] - 1) * 100
            if abs(chg) >= 1.0:
                reasons.append(f"{label} 1일 {chg:+.2f}%")
    return Gate(publish=bool(reasons), reasons=reasons)


# ─────────────────────────────────────────────────────────────
# 조립
# ─────────────────────────────────────────────────────────────
def build_calendar_block(as_of: date, slot: str) -> Block:
    """⑥ 거래 캘린더 — 휴장·시차를 코드가 판정해서 알려준다.

    LLM이 "왜 숫자가 오래됐는지"를 추측하지 않게 한다(R1). WEEKEND
    슬롯에서는 "다음주 예정 일정"이 이 블록을 대체한다(별도 함수)."""
    from engine.briefing import calendar as C

    gap = C.describe_trading_gap(as_of, slot)
    lines = [gap.text]
    events = C.upcoming_events(as_of, horizon_days=5)
    if events:
        lines.append("\n**5일 내 예정된 확정 일정**:")
        for e in events:
            lines.append(f"- {e['date']} {e.get('country', '')} {e['name']}")
    return Block("calendar", "⑥ 거래 캘린더 (휴장·시차)", "\n".join(lines))


def build_weekly_outlook_block(as_of: date) -> Block:
    """⑦ 다음주 예정 일정 — 주말(WEEKEND) 슬롯 전용.

    사용자 요청: "주말 보고서에는 다음주 어떤 일정들이 예정돼 있는지
    미리 알려달라 — 지표 발표 주기, 실적발표, 주요 선거, 지난 보고서에서
    확인된 이슈의 follow up." 이 함수가 그 네 가지를 조립한다."""
    from engine.briefing import calendar as C
    from engine.briefing import ledger as L

    lines = []

    confirmed = C.upcoming_events(as_of, horizon_days=9)
    if confirmed:
        lines.append("**확정 일정**")
        for e in confirmed:
            lines.append(f"- {e['date']} [{e.get('country','')}/{e.get('type','')}] {e['name']}")
            analog = C.historical_analog(e.get("type", ""))
            if analog:
                lines.append(f"  - 📜 과거 유사 사례(패턴 참고용, 확정 아님): {analog['note'].strip()}")
        lines.append("")

    patterns = C.pattern_events()
    if patterns:
        lines.append("**반복 패턴(정확한 날짜는 재확인 필요, 근사치)**")
        for e in patterns:
            lines.append(f"- {e['date']} [{e.get('country','')}] {e['name']} (추정)")
        lines.append("")

    due_next_week = [r for r in L.open_predictions(as_of)
                     if as_of.isoformat() < r.check_date <= (as_of + timedelta(days=9)).isoformat()]
    if due_next_week:
        lines.append("**다음주 검증일 도래 예측 (follow up 대상)**")
        for r in due_next_week:
            lines.append(f"- `{r.id}` ({r.check_date} 검증) {r.claim}")
        lines.append("")

    stale = sorted(
        (d for d in _load_digests()),
        key=lambda d: str(d.get("as_of", "")),
    )[:5]
    if stale:
        lines.append("**가장 오래 안 갱신된 위키 추적 축 (follow up 후보)**")
        for d in stale:
            lines.append(f"- {d.get('status_label', d['slug'])} (판단일 {d.get('as_of', '?')}) "
                        f"→ `{d.get('monitoring_page', '')}`")

    if not lines:
        lines = ["다음주 확정 일정 없음, follow up 대상 없음."]

    return Block("weekly_outlook", "⑦ 다음주 예정 일정 (주간 전망)", "\n".join(lines))


def build_pack(slot: str, as_of: date | None = None) -> tuple[BriefingPack, Gate]:
    now = datetime.now(KST)
    as_of = as_of or now.date()

    if slot == "WEEKEND":
        # 주말 전망은 "오늘 시장이 움직였나"로 게이트를 걸지 않는다 —
        # 주간 캘린더는 시장이 안 움직여도 매주 유효한 정보다.
        pack = BriefingPack(slot=slot, as_of=now, blocks=[
            build_hynix_block(as_of),
            build_digest_block(as_of, *detect_triggers(as_of)),
            build_ledger_block(as_of),
            build_weekly_outlook_block(as_of),
        ])
        return pack, Gate(publish=True, reasons=["주간 전망은 항상 발행"])

    triggers, why = detect_triggers(as_of)
    gate = evaluate_gate(as_of, triggers, why)
    pack = BriefingPack(slot=slot, as_of=now, blocks=[
        build_fact_sheet(as_of),
        build_hynix_block(as_of),
        build_digest_block(as_of, triggers, why),
        build_previous_block(as_of, slot),
        build_ledger_block(as_of),
        build_calendar_block(as_of, slot),
    ])
    return pack, gate
