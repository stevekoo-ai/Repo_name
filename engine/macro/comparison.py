"""KR-vs-US macro comparison — the "big picture first" layer the user asked
for: judge the US regime, judge the KR regime, then read Korea's indicators
against that US backdrop instead of in isolation. Pure synthesis over
already-computed engine.macro.engine outputs; doesn't fetch or score
anything itself.
"""
from __future__ import annotations

from core.config import rules_config

# (kr_reading_key, us_reading_key, korean_label) — pairs that exist on both
# sides with directly comparable score semantics (+1 always means "healthy/
# strong" on both the KR and US rule tables, so scores compare directly).
DIRECT_PAIRS = [
    ("gdp", "gdp", "GDP 성장"),
    ("industrial_production", "industrial_production", "산업생산"),
    ("retail_sales", "retail_sales", "소매판매"),
    ("cpi", "cpi", "CPI"),
    ("ppi", "ppi", "PPI"),
    ("unemployment", "unemployment", "고용(실업률)"),
]
# current_account (KR) and trade_balance (US) measure related but not
# identical things (broad external balance vs. goods/services trade only) —
# paired separately and labeled as such rather than folded into DIRECT_PAIRS.
EXTERNAL_BALANCE_PAIR = ("current_account", "trade_balance", "대외수지(경상수지 vs 무역수지)")


def _pair_relationship(kr_score: int | None, us_score: int | None) -> str:
    if kr_score is None or us_score is None:
        return "data_unavailable"
    if kr_score == us_score:
        return "sync"
    return "diverge"


def _build_pairs(kr_readings: dict, us_readings: dict) -> list[dict]:
    pairs = []
    for kr_key, us_key, label in DIRECT_PAIRS + [EXTERNAL_BALANCE_PAIR]:
        kr_r = kr_readings.get(kr_key, {})
        us_r = us_readings.get(us_key, {})
        kr_score, us_score = kr_r.get("score"), us_r.get("score")
        pairs.append({
            "key": kr_key, "label": label,
            "kr_score": kr_score, "us_score": us_score,
            "kr_value": kr_r.get("value"), "us_value": us_r.get("value"),
            "relationship": _pair_relationship(kr_score, us_score),
        })
    return pairs


def _cycle_alignment(kr_regime: str, us_regime: str) -> dict:
    cycle: list[str] = rules_config()["regime"]["cycle"]
    kr_idx = cycle.index(kr_regime) if kr_regime in cycle else None
    us_idx = cycle.index(us_regime) if us_regime in cycle else None
    if kr_idx is None or us_idx is None:
        return {"cycle_gap": None, "alignment": "unknown"}
    gap = kr_idx - us_idx
    if gap == 0:
        alignment = "sync"
    elif gap > 0:
        alignment = "kr_ahead"
    else:
        alignment = "kr_behind"
    return {"cycle_gap": gap, "alignment": alignment}


def _narrative(kr_macro: dict, us_macro: dict, pairs: list[dict], alignment: dict) -> str:
    kr_regime, us_regime = kr_macro["regime"], us_macro["regime"]
    kr_warn, us_warn = kr_macro.get("warning_active", False), us_macro.get("warning_active", False)

    direct = [p for p in pairs if p["key"] != "current_account"]
    scored = [p for p in direct if p["relationship"] != "data_unavailable"]
    synced = [p for p in scored if p["relationship"] == "sync"]
    co_movement_pct = round(len(synced) / len(scored) * 100, 0) if scored else None

    lines = [f"미국은 현재 {us_regime} 국면, 한국은 {kr_regime} 국면입니다."]

    if alignment["alignment"] == "sync":
        lines.append("두 나라가 같은 단계에 있어, 지금 한국의 흐름은 대체로 미국이 이끄는 글로벌 사이클에 함께 실려 가는 모습입니다.")
    elif alignment["alignment"] == "kr_ahead":
        lines.append("한국이 사이클상 미국보다 한 단계 이상 앞서 있어, 미국이 아직 도달하지 않은 국면을 한국이 먼저 겪고 있는 상태입니다 — 한국 고유 요인(반도체 사이클, 정책 등)의 영향인지 점검이 필요합니다.")
    elif alignment["alignment"] == "kr_behind":
        lines.append("한국이 사이클상 미국보다 뒤처져 있어, 미국에서 먼저 나타난 흐름이 시차를 두고 한국에 파급될 가능성을 주시할 필요가 있습니다.")

    if co_movement_pct is not None:
        lines.append(f"비교 가능한 6개 핵심 지표 중 {co_movement_pct:.0f}%가 미국과 같은 방향으로 움직이고 있습니다.")

    if us_warn and not kr_warn:
        lines.append("미국 쪽에 경고 신호가 있지만 한국은 아직 뚜렷한 경고 신호가 없어, 미국발 리스크가 한국에는 아직 본격적으로 옮겨오지 않은 것으로 보입니다 — 다만 선행 지표로 계속 관찰이 필요합니다.")
    elif kr_warn and not us_warn:
        lines.append("미국은 경고 신호가 없는데 한국만 경고 신호가 있어, 이번 흐름은 글로벌 요인보다 한국 특유의 요인에서 비롯됐을 가능성이 큽니다.")
    elif kr_warn and us_warn:
        lines.append("미국과 한국 모두 경고 신호가 있어, 이번 흐름은 한국만의 국지적 문제가 아니라 글로벌 사이클 자체의 위험 신호일 가능성이 있습니다.")
    else:
        lines.append("미국과 한국 모두 뚜렷한 경고 신호는 없는 상태입니다.")

    diverging = [p["label"] for p in direct if p["relationship"] == "diverge"]
    if diverging:
        lines.append(f"방향이 엇갈린 지표: {', '.join(diverging)} — 이 부분이 한국이 미국과 다르게 가는 지점입니다.")

    return " ".join(lines)


def compare_kr_us(kr_macro: dict, us_macro: dict) -> dict:
    kr_readings, us_readings = kr_macro["readings"], us_macro["readings"]
    pairs = _build_pairs(kr_readings, us_readings)
    alignment = _cycle_alignment(kr_macro["regime"], us_macro["regime"])
    narrative = _narrative(kr_macro, us_macro, pairs, alignment)

    return {
        "kr_regime": kr_macro["regime"],
        "us_regime": us_macro["regime"],
        "kr_score_band": kr_macro["score_band"],
        "us_score_band": us_macro["score_band"],
        "cycle_gap": alignment["cycle_gap"],
        "alignment": alignment["alignment"],
        "indicator_pairs": pairs,
        "narrative": narrative,
    }
