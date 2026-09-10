"""리포트 §1.7 — 환율 국면.

설계: wiki/architecture/fx-regime-score-design.md §3(출력 A·B), §6.5.3(§1.7-B)

## 이 섹션이 **하지 않는** 것

R4(포지션 지시는 단일 출처) + §6.5.1의 실측 결과에 따라:

- 헤지하라/말라, 달러를 사라/팔라 같은 **지시를 하지 않는다**
- 종목·ETF·상품 **추천을 하지 않는다**
- **목표 환율을 만들지 않는다**(R3)
- 자산배분 **비중을 제시하지 않는다**

특히 마지막이 중요하다. MA36 하회 국면 중 진입의 나스닥 초과성과는 12개월
기준 +0.0%p였다 — **환율 국면은 자산 선택에 정보를 주지 않는다**. 그런데도
국면 점수로 비중을 정하면, 표본기간(2011~2024)의 미국 강세장을 국면 탓으로
착각한 것을 코드로 굳히게 된다.

살아남은 연결은 **종료 경고 ↔ 장기채** 하나뿐이고, 그것도 trigger_kind가
US_TIGHTENING일 때만이다(wiki/concepts/fx-episode-dollar-assets.md §4).
"""
from __future__ import annotations

from datetime import date

from engine.fx import series as S
from engine.fx.regime_score import calculate_frs, ma36_gap, regime_label
from engine.fx.transition import (
    TriggerKind, current_episode_months, evaluate_verbose, evidence_for,
)


def build_fx_regime_payload(as_of: date, risk_events: dict | None = None) -> dict:
    """리포트가 렌더할 수 있는 형태로 FRS 결과를 담는다."""
    detail = calculate_frs(as_of, risk_events)
    report, exit_triggers = evaluate_verbose(as_of, risk_events)
    gap = ma36_gap(as_of)
    return {
        "as_of": as_of.isoformat(),
        "score": detail.score,
        "coverage": detail.coverage,
        "label": regime_label(as_of, detail),
        "factors": [
            {"key": f.key, "label": f.label, "weight": f.weight,
             "normalized": f.normalized, "detail": f.detail,
             "available": f.available}
            for f in detail.factors
        ],
        "gap": None if gap is None else {
            "spot": gap[0], "ma36": gap[1], "pct": gap[2]},
        "episode_months": current_episode_months(as_of),
        "warning_level": report.level,
        "warning_count": report.count,
        "trigger_kind": report.trigger_kind.name,
        "warnings": [
            {"key": w.key, "label": w.label, "fired": w.fired,
             "detail": w.detail, "evidence": evidence_for(w.key)}
            for w in report.warnings
        ],
        "exit_triggers": [
            {"key": w.key, "label": w.label, "fired": w.fired, "detail": w.detail}
            for w in exit_triggers
        ],
        "dollar_context": _dollar_context(as_of),
    }


def _dollar_context(as_of: date) -> dict:
    """§1.7-B의 재료 — 사실만. 추천은 만들지 않는다."""
    return {
        "cash_yield": S.value_as_of("us_3m", as_of, 30),
        "us_2y": S.value_as_of("us_2y", as_of, 30),
        "us_10y": S.value_as_of("us_10y", as_of, 30),
        "hy_oas": S.value_as_of("us_hy_oas", as_of, 30),
        "vix": S.value_as_of("us_vix", as_of, 30),
    }


def render_fx_regime_section(payload: dict) -> str:
    """§1.7 마크다운. payload["fx_regime"]이 없으면 조용히 생략한다."""
    fx = payload.get("fx_regime")
    if not fx or fx.get("score") is None:
        return ""

    lines = ["# 1.7 환율 국면 (FRS)", ""]

    # ── 출력 A: 현재 국면 ────────────────────────────────
    gap = fx.get("gap")
    score = fx["score"]
    head = f"**{fx['label']}** — FRS **{score:+.0f}** (−100~+100, (+)=원화 강세 압력)"
    if fx["coverage"] < 1.0:
        head += f", 커버리지 {fx['coverage']*100:.0f}%"
    lines += [head, ""]
    if gap:
        months = fx.get("episode_months")
        dur = f", {months}개월째" if months else ""
        lines += [
            f"현물 {gap['spot']:,.1f}원 vs 36개월선 {gap['ma36']:,.1f}원 "
            f"(**{gap['pct']:+.1f}%**{dur})",
            "",
        ]

    lines += ["| 요인 | 가중 | 점수 | 근거 |", "|---|---:|---:|---|"]
    for f in fx["factors"]:
        val = f"{f['normalized']:+.2f}" if f["available"] else "—"
        lines.append(f"| {f['label']} | {f['weight']} | {val} | {f['detail']} |")
    lines.append("")

    # ── 출력 B: 전환 경고 ────────────────────────────────
    lines += [f"## 국면 전환 경고 — {fx['warning_level']} ({fx['warning_count']}/4)", ""]
    lines += ["| 감지기 | 상태 | 근거 | 실측 예측력 |", "|---|:--:|---|---|"]
    for w in fx["warnings"]:
        ev = w.get("evidence") or {}
        lines.append(
            f"| {w['label']} | {'🔥' if w['fired'] else '·'} | {w['detail']} | "
            f"{ev.get('verdict', '미측정')} |")
    lines += [
        "",
        "> 예측력은 2008~2026 하회 국면 83개월 백테스트에서 측정한 리프트다"
        "(1.0 = 정보 없음). 켜진 경고를 전부 같은 무게로 읽으면 안 된다.",
        "",
    ]

    # ── §1.7-B 달러 자산 맥락 (사실 4줄) ─────────────────
    lines += _dollar_block(fx)

    lines += [
        "",
        "> 이 섹션은 **국면과 경고만** 제시한다. 헤지·매매 지시, 종목·비중 추천, "
        "목표 환율은 만들지 않는다(R4). 환율 국면이 자산 선택에 정보를 주지 "
        "않는다는 실측 근거는 "
        "[환율 국면과 달러 자산](../wiki/concepts/fx-episode-dollar-assets.md) §3.",
        "",
    ]
    return "\n".join(lines)


def _dollar_block(fx: dict) -> list[str]:
    """§6.5.3의 사실 4줄. 없는 값은 그 줄을 통째로 생략한다(R3)."""
    ctx = fx.get("dollar_context") or {}
    out = ["## 달러 자산 맥락 (판단 재료 — 추천 아님)", ""]

    cash = ctx.get("cash_yield")
    if cash is not None:
        out.append(
            f"- **달러 현금 기준선**: 미 3개월물 **{cash:.2f}%**. "
            "과거 5개 국면 중 4개는 미국이 제로금리라 '환전 후 대기'가 무수익이었다 "
            "— 지금은 아무것도 안 해도 이만큼이 기준선이다.")

    gap = fx.get("gap")
    if gap:
        out.append(
            f"- **환차익 구조**: 국면 전체를 보유하면 환차익은 구조적으로 0에 가깝다"
            "(국면 양끝이 모두 36개월선 교차점이라 레벨이 비슷하다 — 20개월짜리 "
            f"①국면도 −0.9%였다). 현재 이격 {gap['pct']:+.1f}%. **목표 환율은 제시하지 않는다.**")

    if fx["warning_count"] > 0:
        kind = fx.get("trigger_kind")
        if kind == TriggerKind.US_TIGHTENING.name:
            out.append(
                "- **⚠ 장기채 함의**: 종료 경고 원인이 **미국 긴축 전환**이다. "
                "과거 국면 종료 직후 진입한 10년물은 12개월 수익 중앙값 −0.3%로 "
                "무조건 진입(+3.9%)보다 4.2%p 나빴다 — 긴축이 금리를 밀어올려 "
                "평가손이 나기 때문.")
        elif kind == TriggerKind.NON_US_SHOCK.name:
            out.append(
                "- **장기채 함의**: 종료 경고 원인이 **미국 외 충격**이다. "
                "2018-10형(무역전쟁)처럼 연준이 오히려 완화로 돌아서면 장기채가 "
                "가장 좋은 성적을 낸 전례가 있다(그 국면 12개월 +16.2%) — "
                "긴축형과 정반대다.")
        else:
            out.append(
                "- **장기채 함의**: 종료 경고는 켜졌으나 원인이 특정되지 않았다. "
                "긴축형인지 아닌지에 따라 장기채 함의가 정반대라 판단을 보류한다(R3).")

    hy, vix = ctx.get("hy_oas"), ctx.get("vix")
    if hy is not None or vix is not None:
        bits = []
        if hy is not None:
            bits.append(f"하이일드 스프레드 {hy:.2f}%p")
        if vix is not None:
            bits.append(f"VIX {vix:.1f}")
        out.append(f"- **위험 보상 맥락**: {', '.join(bits)}. "
                   "스프레드가 좁을수록 위험을 져도 받는 보상이 얇다는 뜻이다.")
    return out
