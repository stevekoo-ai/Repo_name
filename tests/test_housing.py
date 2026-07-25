from datetime import date, timedelta

from engine.personal import housing as housing_mod


def _future(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def test_housing_warning_when_deadline_imminent_and_funding_short(monkeypatch):
    """21.4 case 5: 청약 공고 임박 + 자금 준비 부족 -> Housing readiness should be low
    and the platform-city funding gap should be flagged."""
    notice = {
        "name": "테스트 공고", "agency": "LH", "region": "세종 플랫폼시티", "is_platform_city": True,
        "supply_type": "일반공급", "size": "84㎡ 이상", "household_count": 500,
        "announce_date": _future(3), "application_start": _future(10), "application_end": _future(11),
        "expected_price_krw": 600_000_000, "expected_competition_ratio": None,
    }
    monkeypatch.setattr("collectors.manual.fetch_subscription_notices", lambda: [notice])
    # housing.py did `from core.config import user_profile, portfolio_config`, so the
    # local names in engine.personal.housing must be patched directly — patching
    # core.config's attributes wouldn't affect the already-bound local references.
    monkeypatch.setattr("engine.personal.housing.user_profile", lambda: {
        "housing": {"priority_regions": ["세종 플랫폼시티"], "preferred_size": "84㎡ 이상"},
    })
    monkeypatch.setattr("engine.personal.housing.portfolio_config", lambda: {
        "subscription_savings": {"balance_krw": 5_000_000, "account_start": "2024-01-01"},
    })

    result = housing_mod.compute_housing_readiness()
    scored = result["notices"][0]

    assert scored["readiness_score"] < 55  # short lead time + big funding shortfall -> low readiness
    assert scored["platform_city_analysis"]["funding_gap_krw"] > 0
    assert any("자금조달" in note for note in scored["platform_city_analysis"]["risk_notes"])


def test_no_notices_is_pending_not_a_guess(monkeypatch):
    monkeypatch.setattr("collectors.manual.fetch_subscription_notices", lambda: [])
    result = housing_mod.compute_housing_readiness()
    assert result["data_status"] == "pending"
    assert result["notices"] == []
