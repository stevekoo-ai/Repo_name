"""Tests for engine.exporters.subscription_concern_tracker.

Covers the daily 청약 우려사항 tracker requested by the user: "정보를 취득하면
항상 나를 바라봐야해...긴급하게 처리해야하는지 전략을 수정해야하는지를 알려
주는 daily보고서". Each _check_* function must classify correctly at its
urgency boundaries, and the module must never fabricate data it doesn't have
(Master Instruction 7.9).
"""
from datetime import date, timedelta

from engine.exporters import subscription_concern_tracker as tracker

_PROFILE = {
    "housing": {
        "target_complex": "용인 플랫폼시티 공공분양",
        "income_cap_preference": "none",
        "subscription_priority_strategy": "저축총액(납입총액) 기준 경쟁 — 85㎡ 초과 일반공급, 소득제한 없는 84㎡ 이상 우선",
        "moveout_deadline": None,  # set per-test
    }
}


def _future(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def _patch_common(monkeypatch, profile=None, notices=None, portfolio=None, alerted=None):
    monkeypatch.setattr(tracker, "user_profile", lambda: profile if profile is not None else _PROFILE)
    monkeypatch.setattr(tracker, "portfolio_config", lambda: portfolio or {})
    monkeypatch.setattr(
        "collectors.manual.fetch_subscription_notices", lambda: notices if notices is not None else []
    )
    monkeypatch.setattr(tracker, "_load_alerted_state", lambda: alerted or {})


def test_income_cap_risk_watch_when_strategy_set(monkeypatch):
    _patch_common(monkeypatch)
    item = tracker._check_income_cap_risk(_PROFILE)
    assert item.urgency == tracker.WATCH


def test_income_cap_risk_revise_when_preference_not_none():
    profile = {"housing": {"income_cap_preference": None, "subscription_priority_strategy": None}}
    item = tracker._check_income_cap_risk(profile)
    assert item.urgency == tracker.REVISE


def test_moveout_deadline_urgent_within_90_days(monkeypatch):
    item = tracker._check_moveout_deadline(
        {"housing": {"moveout_deadline": _future(89)}}, date.today()
    )
    assert item.urgency == tracker.URGENT


def test_moveout_deadline_urgent_when_past(monkeypatch):
    item = tracker._check_moveout_deadline(
        {"housing": {"moveout_deadline": (date.today() - timedelta(days=1)).isoformat()}}, date.today()
    )
    assert item.urgency == tracker.URGENT
    assert "경과" in item.status


def test_moveout_deadline_revise_boundary_180_days():
    item = tracker._check_moveout_deadline(
        {"housing": {"moveout_deadline": _future(180)}}, date.today()
    )
    assert item.urgency == tracker.REVISE


def test_moveout_deadline_watch_beyond_180_days():
    item = tracker._check_moveout_deadline(
        {"housing": {"moveout_deadline": _future(181)}}, date.today()
    )
    assert item.urgency == tracker.WATCH


def test_moveout_deadline_watch_when_unset():
    item = tracker._check_moveout_deadline({"housing": {}}, date.today())
    assert item.urgency == tracker.WATCH


def test_platform_city_urgent_when_private_notice_found(monkeypatch):
    notices = [{"name": "용인 플랫폼시티 민영분양", "is_platform_city": True, "housing_type": "민영", "source": "청약홈"}]
    monkeypatch.setattr("collectors.manual.fetch_subscription_notices", lambda: notices)
    item = tracker._check_platform_city_privatization_risk(_PROFILE, {})
    assert item.urgency == tracker.URGENT
    assert "민영" in item.status


def test_platform_city_revise_when_keyword_alerted_but_no_notice(monkeypatch):
    monkeypatch.setattr("collectors.manual.fetch_subscription_notices", lambda: [])
    alerted = {"2026999999": {"priority": "MED", "keyword": "플랫폼시티"}}
    item = tracker._check_platform_city_privatization_risk(_PROFILE, alerted)
    assert item.urgency == tracker.REVISE


def test_platform_city_watch_when_nothing_found(monkeypatch):
    monkeypatch.setattr("collectors.manual.fetch_subscription_notices", lambda: [])
    item = tracker._check_platform_city_privatization_risk(_PROFILE, {})
    assert item.urgency == tracker.WATCH


def test_school_commute_revise_when_far_target_registered(monkeypatch):
    notices = [{
        "name": "수원 원천동(광교) 공공분양",
        "is_platform_city": False,
        "region": "경기도 수원시 영통구 원천동 80번지 일원",
    }]
    monkeypatch.setattr("collectors.manual.fetch_subscription_notices", lambda: notices)
    item = tracker._check_school_commute_constraint(_PROFILE)
    assert item.urgency == tracker.REVISE
    assert "원천동" in item.status


def test_school_commute_watch_when_no_notices(monkeypatch):
    monkeypatch.setattr("collectors.manual.fetch_subscription_notices", lambda: [])
    item = tracker._check_school_commute_constraint(_PROFILE)
    assert item.urgency == tracker.WATCH


def test_funding_gap_never_guesses_without_data(monkeypatch):
    """7.9: 분양가/경쟁률 미정이면 갭 숫자를 만들어내지 않는다."""
    item = tracker._check_funding_gap({}, {})
    assert item.urgency == tracker.WATCH
    assert "추측" in item.recommendation or "근거" in item.status


def test_compute_subscription_concerns_end_to_end(monkeypatch):
    _patch_common(monkeypatch, profile={
        "housing": {
            "target_complex": "용인 플랫폼시티 공공분양",
            "income_cap_preference": "none",
            "subscription_priority_strategy": "저축총액 기준",
            "moveout_deadline": _future(200),
        }
    })
    report = tracker.compute_subscription_concerns({})
    assert len(report.concerns) == 5
    assert report.overall_urgency in (tracker.URGENT, tracker.REVISE, tracker.WATCH)
    assert report.headline


def test_overall_urgency_escalates_to_urgent_when_any_concern_urgent(monkeypatch):
    _patch_common(monkeypatch, profile={
        "housing": {
            "target_complex": "용인 플랫폼시티 공공분양",
            "income_cap_preference": "none",
            "subscription_priority_strategy": "저축총액 기준",
            "moveout_deadline": (date.today() - timedelta(days=5)).isoformat(),  # expired -> URGENT
        }
    })
    report = tracker.compute_subscription_concerns({})
    assert report.overall_urgency == tracker.URGENT
    assert "긴급" in report.headline
