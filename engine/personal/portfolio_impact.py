"""Portfolio / Asset Impact Layer (Master Instruction 14).

Converts the domain-engine scores already computed (Investment
Environment, Semiconductor, Bond, FX, Housing) into a 0-100 impact score
and 1-5 star rating per asset category the user actually holds
(config/portfolio.yaml), rather than re-deriving a parallel scoring
system — 14.3's star bands are the same 85/70/55/40 thresholds used
throughout PEOS (core.models.score_to_stars).
"""
from __future__ import annotations

from core.config import portfolio_config
from core.models import score_to_stars


def _category(score: float | None, holdings_detail: dict | list | None = None) -> dict:
    return {
        "score": score,
        "stars": score_to_stars(score) if score is not None else None,
        "data_status": "ok" if score is not None else "pending",
        "detail": holdings_detail,
    }


def compute_asset_impact(investment: dict, semiconductor: dict, bond: dict, fx: dict,
                          housing: dict, etf_fit: list[dict]) -> dict:
    portfolio = portfolio_config()
    env_score = investment.get("investment_environment_score")
    semi_score = semiconductor.get("semiconductor_score") if semiconductor.get("data_status") == "ok" else None

    stock_scores = []
    for holding in portfolio.get("stocks", []):
        if holding.get("sector") == "semiconductor_memory" and semi_score is not None and env_score is not None:
            stock_scores.append(0.5 * semi_score + 0.5 * env_score)
        elif env_score is not None:
            stock_scores.append(env_score)
    stock_score = round(sum(stock_scores) / len(stock_scores), 1) if stock_scores else None

    etf_scored = [e["fit_score"] for e in etf_fit if e.get("fit_score") is not None]
    etf_score = round(sum(etf_scored) / len(etf_scored), 1) if etf_scored else None

    bond_score = bond.get("bond_score")
    fx_score = fx.get("fx_score")

    cash_score = investment.get("factors", {}).get("risk_penalty_inverse")

    housing_notices = housing.get("notices", [])
    housing_scores = [n["readiness_score"] for n in housing_notices if n.get("readiness_score") is not None]
    housing_score = round(sum(housing_scores) / len(housing_scores), 1) if housing_scores else None

    return {
        "stocks": _category(stock_score, [h["name"] for h in portfolio.get("stocks", [])]),
        "etf": _category(etf_score, etf_fit),
        "bond": _category(bond_score, portfolio.get("bonds", [])),
        "cash": _category(cash_score, portfolio.get("cash", {})),
        "subscription_fund": _category(housing_score, housing_notices),
        "fx_exposure": _category(fx_score, fx.get("detail")),
    }
