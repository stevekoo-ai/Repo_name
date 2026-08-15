"""Cross-engine reconciliation — one report, one instruction.

WHY THIS EXISTS
───────────────
On 2026-08-10 the same report told the user, about the same ticker, on the
same page:

    engine/crisis_analysis  →  "적극 매수 (Long), 최대 비중 25%"
    engine/exporters/sk_hynix_decision → "HOLD, 신뢰도 50%"

and separately called the US economy "Recession" while its own crisis index
read GREEN 5/100 with every recession precursor at zero. A reader cannot act
on that, and worse, they can pick whichever line matches what they already
wanted to do.

The fix is NOT to make the engines agree. Forcing agreement destroys
information — the disagreement itself is a signal about how much the report
knows today. The fix is to state each conflict, resolve it under a written
precedence rule, and emit exactly one actionable stance.

PRECEDENCE RULES (change these only with a reason recorded in wiki/log.md)
─────────────────────────────────────────────────────────────────────────
  R1  측정 > 추론.       An observed series beats a value inferred from
                         another series.
  R2  신선 > 이월.       A verdict resting on carried-forward readings loses
                         to one resting on fresh readings.
  R3  미수집은 판정이 아니다.  A missing input scores zero; zero is not a
                         bearish verdict. (See the CCI semiconductor block.)
  R4  포지션 지시는 단일 출처.  Only the domain decision engine may issue a
                         buy/sell/hold instruction. Every other module is
                         context, however confident it sounds.
  R5  신뢰도 하한.        Below CONFIDENCE_FLOOR a signal is not a signal.
                         Two sub-floor engines disagreeing means "do not act",
                         not "pick one".
"""
from __future__ import annotations

from dataclasses import dataclass, field

CONFIDENCE_FLOOR = 55.0   # below this a directional signal is treated as 무판단

# Modules allowed to issue a position instruction. Anything else that emits
# buy/sell language is context and is relabelled as such (R4).
POSITION_AUTHORITY = "engine/exporters/sk_hynix_decision.py"


@dataclass
class Conflict:
    topic: str
    claim_a: str          # the module whose output is being demoted
    claim_b: str          # the output that survives
    rule: str             # which precedence rule decided it
    resolution: str


@dataclass
class Reconciliation:
    conflicts: list[Conflict] = field(default_factory=list)
    tradeable: bool = True
    verdict: str = ""
    blockers: list[str] = field(default_factory=list)


def _stale_ratio(dashboard: list[dict]) -> float:
    if not dashboard:
        return 0.0
    stale = sum(1 for r in dashboard if r.get("status") == "stale")
    return stale / len(dashboard)


def reconcile(payload: dict) -> Reconciliation:
    rec = Reconciliation()

    cci = payload.get("cci_analysis") or {}
    sk = payload.get("sk_hynix_decision")
    macro_us = payload.get("macro_us") or {}
    rate = payload.get("rate_analysis") or {}
    weekly = (payload.get("weekly_analysis") or {}).get("indicators") or {}

    # ── R4: two modules instructing on the same ticker ───────────────────
    cci_action = (cci.get("sk_hynix_action") or {}).get("action")
    if cci_action and sk is not None:
        rec.conflicts.append(Conflict(
            topic="SK하이닉스 포지션 지시",
            claim_a=f"위기지수(CCI): \"{cci_action}\", 최대 비중 "
                    f"{(cci.get('sk_hynix_action') or {}).get('max_weight')}%",
            claim_b=f"의사결정 엔진: {sk.signal} (신뢰도 {sk.confidence:.0f}%)",
            rule="R4 포지션 지시는 단일 출처",
            resolution=(
                "의사결정 엔진의 신호만 유효. CCI의 매수/매도 문구는 위기 국면 "
                "서술일 뿐 종목 지시가 아니므로 '위험 환경 정보'로 격하해 읽을 것."
            ),
        ))

    # ── R2/R3: a regime call resting on carried-forward data ─────────────
    us_stale = _stale_ratio(payload.get("us_macro_dashboard") or [])
    cci_state = cci.get("state")
    if macro_us.get("regime") == "Recession" and cci_state == "GREEN":
        rec.conflicts.append(Conflict(
            topic="미국 경기 국면",
            claim_a=f"거시 엔진: Recession (신뢰도 {macro_us.get('confidence')}점, "
                    f"지표 {us_stale*100:.0f}% 이월)",
            claim_b=f"위기지수: {cci_state} {cci.get('total_score')}/100 "
                    f"— 침체 전조 지표 대부분 0점",
            rule="R2 신선 > 이월",
            resolution=(
                "Recession 판정은 물가지수(CPI/PPI) 하락만으로 성립한 것이며 "
                "수익률곡선·고용·신용스프레드는 침체를 가리키지 않음. "
                "물가 하락 + 정상 수익률곡선은 침체가 아니라 디스인플레이션에 가깝다. "
                "위기지수 쪽을 채택하되, 이월 비중이 높으므로 어느 쪽도 확정으로 쓰지 말 것."
            ),
        ))

    # ── R1: an inferred FX direction vs the measured rate ────────────────
    rationale = (rate.get("sk_hynix_outlook") or {}).get("rationale") or ""
    fx = weekly.get("kr_usdkrw") or {}
    fx_change = fx.get("pct_change")
    if "달러 강세" in rationale and isinstance(fx_change, (int, float)) and fx_change < 0:
        rec.conflicts.append(Conflict(
            topic="환율 방향",
            claim_a="금리 분석: 미-한 금리차 확대 → \"달러 강세\"가 수출을 뒷받침 (추론)",
            claim_b=f"실측 환율: {fx.get('value_12w_ago'):,.1f}원 → "
                    f"{fx.get('current_value'):,.1f}원 ({fx_change:+.1f}%, 원화 강세)",
            rule="R1 측정 > 추론",
            resolution=(
                "실측 환율을 채택. 금리차로부터 달러 강세를 추론했으나 실제로는 원화가 "
                "강세로 갔다. 원화 강세는 수출기업에 역풍이므로, 이 문장을 근거로 "
                "수출 개선을 기대하지 말 것."
            ),
        ))

    # ── R5: is anything actionable today? ────────────────────────────────
    if sk is not None and sk.confidence < CONFIDENCE_FLOOR:
        rec.blockers.append(
            f"SK하이닉스 신호 신뢰도 {sk.confidence:.0f}% < 하한 {CONFIDENCE_FLOOR:.0f}% → 무판단"
        )
    kr_stale = _stale_ratio(payload.get("macro_dashboard") or [])
    if kr_stale >= 0.5 or us_stale >= 0.5:
        rec.blockers.append(
            f"지표 이월 비중 높음 (한국 {kr_stale*100:.0f}%, 미국 {us_stale*100:.0f}%) "
            f"→ 오늘 갱신된 경제 정보 거의 없음"
        )
    if rec.conflicts:
        rec.blockers.append(f"엔진 간 미해소 충돌 {len(rec.conflicts)}건")

    rec.tradeable = not rec.blockers
    rec.verdict = (
        "오늘 이 리포트를 근거로 한 신규 매매 실행은 권장하지 않는다. "
        "구조적 조정(집중도 상한 설정 등 0절 항목)은 데이터와 무관하게 진행 가능하다."
        if not rec.tradeable else
        "충돌 없음 · 신뢰도 하한 통과 — 각 섹션의 신호를 그대로 사용 가능."
    )
    return rec


def render_reconciliation_section(rec: Reconciliation | None) -> str:
    if rec is None:
        return ""

    head = "✅ 실행 가능" if rec.tradeable else "⛔ 오늘 실행 보류"
    lines = [
        "# 0.5 엔진 정합성 점검",
        "",
        f"**판정: {head}**",
        "",
        f"{rec.verdict}",
        "",
    ]

    if rec.blockers:
        lines.append("## 보류 사유")
        lines += [f"- {b}" for b in rec.blockers]
        lines.append("")

    if not rec.conflicts:
        lines.append("## 충돌 없음")
        lines.append("- 모듈 간 상반된 지시가 검출되지 않았습니다.")
        return "\n".join(lines)

    lines.append(f"## 검출된 충돌 {len(rec.conflicts)}건")
    lines.append("")
    for i, c in enumerate(rec.conflicts, 1):
        lines += [
            f"### {i}. {c.topic}",
            f"- **격하되는 쪽**: {c.claim_a}",
            f"- **채택되는 쪽**: {c.claim_b}",
            f"- **적용 규칙**: {c.rule}",
            f"- **판정**: {c.resolution}",
            "",
        ]
    lines += [
        "> 우선순위 규칙(R1~R5)의 정의는 `engine/report/reconciliation.py` 상단 참조.",
        "> 규칙을 바꿀 때는 이유를 `wiki/log.md`에 기록할 것.",
    ]
    return "\n".join(lines)
