"""Housing / Public-Sale Engine (Master Instruction 13.8, 13.9).

    Housing Readiness Score = 0.30*eligibility_fit + 0.25*funding_readiness
        + 0.20*region_type_match + 0.15*timing_readiness
        + 0.10*competition_adjustment_inverse

Runs once per notice in data/manual_inputs/subscription_notices.yaml (13.8),
plus a dedicated 플랫폼시티 breakdown (13.9) when a notice is tagged
`is_platform_city: true`.
"""
from __future__ import annotations

from datetime import date, datetime

from collectors import manual
from core.config import portfolio_config, rules_config, user_profile
from core.utils import clamp
from engine.scoring.weighted import log_score, weighted_sum_0_100


def _eligibility_fit(account_start: str | None) -> float | None:
    if not account_start:
        return None
    start = datetime.fromisoformat(account_start).date()
    years = (date.today() - start).days / 365.25
    return clamp(years / 10 * 100, 0.0, 100.0)  # 10y+ tenure treated as fully mature for general supply ranking


def _funding_readiness(balance_krw: float | None, expected_price_krw: float | None) -> float | None:
    if balance_krw is None:
        return None
    target = expected_price_krw * 0.20 if expected_price_krw else 50_000_000  # 20% target, or a generic fallback
    if target <= 0:
        return None
    return clamp(balance_krw / target * 100, 0.0, 100.0)


def _region_type_match(notice: dict, priority_regions: list[str], preferred_size: str | None) -> float:
    region = notice.get("region", "")
    region_match = any(pr in region or region in pr for pr in priority_regions)
    size_match = preferred_size is not None and notice.get("size") == preferred_size
    if region_match and size_match:
        return 100.0
    if region_match or size_match:
        return 60.0
    return 25.0


def _timing_readiness(notice: dict) -> float | None:
    app_start = notice.get("application_start")
    if not app_start:
        return None
    days_until = (datetime.fromisoformat(app_start).date() - date.today()).days
    if days_until < 0:
        return None  # already passed — not a live readiness question
    if days_until >= 90:
        return 80.0
    if days_until >= 30:
        return 60.0
    return 40.0


def _competition_adjustment_inverse(notice: dict) -> float | None:
    ratio = notice.get("expected_competition_ratio")
    if ratio is None:
        return None
    return clamp(100 - min(100.0, ratio * 2), 0.0, 100.0)


def _score_notice(notice: dict, profile: dict, portfolio: dict) -> dict:
    weights = rules_config()["housing"]
    housing_profile = profile.get("housing", {})
    subscription = portfolio.get("subscription_savings", {})

    factors = {
        "eligibility_fit": _eligibility_fit(subscription.get("account_start")),
        "funding_readiness": _funding_readiness(subscription.get("balance_krw"), notice.get("expected_price_krw")),
        "region_type_match": _region_type_match(
            notice, housing_profile.get("priority_regions", []), housing_profile.get("preferred_size")
        ),
        "timing_readiness": _timing_readiness(notice),
        "competition_adjustment_inverse": _competition_adjustment_inverse(notice),
    }
    score, breakdown = weighted_sum_0_100(factors, weights)
    readiness_score = round(score, 1) if breakdown else None
    log_score("housing", notice.get("name", "notice"), score, breakdown)

    result = {
        "name": notice.get("name"),
        "agency": notice.get("agency"),
        "region": notice.get("region"),
        "housing_type": notice.get("housing_type"),
        "readiness_score": readiness_score,
        "factors": {k: (round(v, 1) if v is not None else None) for k, v in factors.items()},
        "application_start": notice.get("application_start"),
        "application_end": notice.get("application_end"),
        "data_status": "ok" if readiness_score is not None else "pending",
    }

    if notice.get("is_platform_city"):
        result["platform_city_analysis"] = {
            "location": notice.get("region"),
            "supply_scale_households": notice.get("household_count"),
            "expected_schedule": {
                "announce_date": notice.get("announce_date"),
                "application_start": notice.get("application_start"),
                "application_end": notice.get("application_end"),
            },
            "expected_price_krw": notice.get("expected_price_krw"),
            "funding_gap_krw": (
                (notice.get("expected_price_krw", 0) * 0.20) - subscription.get("balance_krw", 0)
                if notice.get("expected_price_krw") else None
            ),
            "expected_competition_ratio": notice.get("expected_competition_ratio"),
            "user_fit_score": readiness_score,
            "risk_notes": [
                "예상 경쟁률 미확정 — 청약홈 공고 확정 후 재평가 필요" if notice.get("expected_competition_ratio") is None else None,
                "자금조달 갭 발생 시 채권/현금 배분 조정 필요 (Action Engine 충돌 조정 대상)"
                if notice.get("expected_price_krw") and subscription.get("balance_krw", 0) < notice.get("expected_price_krw", 0) * 0.20
                else None,
            ],
        }
        result["platform_city_analysis"]["risk_notes"] = [r for r in result["platform_city_analysis"]["risk_notes"] if r]

    return result


def compute_housing_readiness() -> dict:
    notices = manual.fetch_subscription_notices()
    profile = user_profile()
    portfolio = portfolio_config()

    if not notices:
        return {"notices": [], "data_status": "pending",
                "note": "data/manual_inputs/subscription_notices.yaml 에 공고 없음"}

    scored = [_score_notice(n, profile, portfolio) for n in notices]
    return {"notices": scored, "data_status": "ok"}
