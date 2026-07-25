"""Scenario Analysis (Master Instruction 16.9, 16.10).

Probabilities are tied directly to counted signals (upgrade vs.
downgrade+warning) rather than invented numbers (16.9's "근거 없는 숫자
사용 금지"), always sum to 100, and never fall outside
[min_probability, max_probability] from config/thresholds.yaml.
"""
from __future__ import annotations

from core.config import thresholds_config
from core.utils import clamp


def _split_probabilities(upgrade_count: int, bear_count: int) -> tuple[int, int, int]:
    cfg = thresholds_config()["scenario_probability"]
    shift = cfg["signal_shift_per_count"]
    min_p, max_p = cfg["min_probability"], cfg["max_probability"]

    bull = int(round(clamp(20 + upgrade_count * shift, min_p, max_p)))
    bear = int(round(clamp(20 + bear_count * shift, min_p, max_p)))
    base = 100 - bull - bear

    if base < min_p:
        overflow = min_p - base
        total = max(bull + bear, 1)
        bull = max(min_p, bull - round(overflow * bull / total))
        bear = 100 - min_p - bull
        base = min_p

    return base, bull, bear


def compute_scenarios(macro_payload: dict, semiconductor: dict, investment: dict) -> dict:
    upgrade_signals = macro_payload.get("upgrade_signals", [])
    downgrade_signals = macro_payload.get("downgrade_signals", [])
    warning_labels = macro_payload.get("warnings_kr", [])
    bear_count = len(downgrade_signals) + len(warning_labels)

    base_p, bull_p, bear_p = _split_probabilities(len(upgrade_signals), bear_count)

    regime = macro_payload.get("regime")
    semi_label = semiconductor.get("status_label_kr", "미분류")
    env_score = investment.get("investment_environment_score")

    invalid_conditions = [
        "수출 감소 전환", "반도체 수출 감소 전환", "CPI 재상승", "PPI 상승 지속 (6% 이상)",
        "환율 급등", "미국 고용 지표 악화",
    ]

    return {
        "base": {
            "probability": base_p,
            "premise": f"현재 국면({regime})과 반도체 업황({semi_label})의 추세가 유지된다.",
            "expected_change": "지표가 현재 범위 내에서 등락하며 국면 전환 신호는 제한적.",
            "user_impact": f"Investment Environment Score {env_score if env_score is not None else 'N/A'}점 수준의 배분 유지가 합리적.",
        },
        "bull": {
            "probability": bull_p,
            "premise": f"상향 신호({', '.join(upgrade_signals) if upgrade_signals else '추가 확인 필요'})가 강화된다.",
            "expected_change": "수출/반도체 개선과 물가 안정이 동반되며 국면이 한 단계 상향될 가능성.",
            "user_impact": "주식/ETF 비중 확대, 반도체/AI 인프라 비중 우선순위 상향을 검토할 수 있다.",
        },
        "bear": {
            "probability": bear_p,
            "premise": (
                f"하향/경고 신호({', '.join(downgrade_signals + warning_labels) if (downgrade_signals or warning_labels) else '잠재 리스크'})가 "
                "현실화된다."
            ),
            "expected_change": "수출 둔화 또는 물가 재상승으로 국면이 한 단계 하향될 가능성.",
            "user_impact": "현금/채권 비중 확대, 청약·출장 자금 유동성 우선 확보가 합리적.",
        },
        "invalid_conditions": invalid_conditions,
    }
