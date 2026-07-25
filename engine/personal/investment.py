"""Investment / ETF Engine (Master Instruction 13.4, 13.5).

Investment Environment Score turns Macro + Semiconductor + liquidity/risk
into a single 0-100 read, then that composite (plus its sub-factors) is
reused to bias Stock/ETF/Bond/Cash allocation and to score ETF-bucket fit.
"""
from __future__ import annotations

from core.config import portfolio_config, rules_config
from . import market_conditions
from engine.scoring.weighted import log_score, weighted_sum_0_100


def _risk_penalty_inverse(macro_payload: dict) -> float:
    warnings = len(macro_payload.get("warnings_kr", []))
    downgrades = len(macro_payload.get("downgrade_signals", []))
    penalty = min(100.0, warnings * 25 + downgrades * 10)
    return 100.0 - penalty


def _bias_label(score: float, procyclical: bool) -> str:
    effective = score if procyclical else (100 - score)
    if effective >= 70:
        return "확대"
    if effective >= 55:
        return "소폭 확대"
    if effective >= 40:
        return "중립"
    return "축소/방어"


def compute_investment_environment(macro_payload: dict, semiconductor_payload: dict) -> dict:
    weights = rules_config()["investment_environment"]

    macro_norm = market_conditions.macro_score_normalized(macro_payload)
    semi_score = semiconductor_payload["semiconductor_score"] if semiconductor_payload.get("data_status") == "ok" else None
    rate_score, rate_detail = market_conditions.rate_direction_score()
    risk_inverse = _risk_penalty_inverse(macro_payload)

    factors = {
        "macro_score_normalized": macro_norm,
        "semiconductor_score": semi_score,
        "liquidity_rate_condition": rate_score,
        "risk_penalty_inverse": risk_inverse,
    }
    score, breakdown = weighted_sum_0_100(factors, weights)
    env_score = round(score, 1) if breakdown else None
    log_score("investment", "investment_environment_score", score, breakdown)

    biases = None
    if env_score is not None:
        biases = {
            "stock_bias": _bias_label(env_score, procyclical=True),
            "etf_bias": _bias_label(env_score, procyclical=True),
            "bond_bias": _bias_label(env_score, procyclical=False),
            "cash_bias": _bias_label(env_score, procyclical=False),
        }

    return {
        "investment_environment_score": env_score,
        "biases": biases,
        "factors": {k: (round(v, 1) if v is not None else None) for k, v in factors.items()},
        "rate_detail": rate_detail,
        "data_status": "ok" if env_score is not None else "pending",
    }


def compute_etf_fit(macro_score_normalized: float | None, semiconductor_score: float | None,
                     rate_score: float | None, risk_inverse: float | None) -> list[dict]:
    """13.5 ETF Fit per holding, using the same shared sub-scores (bucket exposure heuristic)."""
    weights = rules_config()["etf_fit"]
    portfolio = portfolio_config()
    results = []
    for etf in portfolio.get("etf", []):
        bucket = etf.get("bucket", "diversified")
        semi_exposure = semiconductor_score if bucket in (
            "semiconductor", "semiconductor_global", "ai_infrastructure"
        ) else 50.0
        factors = {
            "cycle_sensitivity_fit": macro_score_normalized,
            "semiconductor_ai_exposure_fit": semi_exposure,
            "rate_sensitivity_fit": rate_score,
            "defensive_need_fit": risk_inverse,
        }
        score, breakdown = weighted_sum_0_100(factors, weights)
        results.append({
            "ticker": etf["ticker"],
            "name": etf["name"],
            "bucket": bucket,
            "fit_score": round(score, 1) if breakdown else None,
            "data_status": "ok" if breakdown else "pending",
        })
    return results
