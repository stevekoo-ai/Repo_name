"""청약(공공분양) 우려사항 추적 — daily 방향성/긴급도 판정 엔진.

WHY THIS EXISTS
────────────────
사용자가 명시적으로 요청한 것: "정보를 취득하면 항상 나를 바라봐야 한다.
내가 현재 우려하는 것들에 대해서 그 정보들이 진행되고 있는 방향을 분석해서
긴급하게 처리해야하는지 전략을 수정해야하는지를 알려주는 daily보고서".

즉 이 모듈의 산출물은 "시장이 어떻다"가 아니라 "당신의 5가지 우려사항 각각이
오늘 기준 어느 단계인가"다. sk_hynix_decision.py/real_estate_decision.py와
같은 결정엔진 패턴(payload 전체를 받아 dataclass로 판정 반환)을 따른다.

추적 대상 5가지 우려사항 (2026-09-01 대화에서 사용자가 직접 확인한 것 —
추측으로 만든 목록이 아니라 그 세션에서 명시적으로 도출됨):

  1. 소득제한 특별공급 배제 위험 — 고소득자라 소득제한 있는 특별공급 유형은
     못 쓴다. "60㎡ 초과 + 일반공급" 전략이 이미 확립돼 있는지가 관건.
  2. 플랫폼시티 민영 분류 위험 — 메인 타겟(용인 플랫폼시티)이 역사적으로
     전부 민영주택으로 분류돼 왔다. 국민주택 공고가 뜨는지 매일 확인 필요.
  3. 전세 계약 만료 임박 — moveout_deadline까지 D-day. 갱신청구권 이미
     사용해 재연장 불가.
  4. 자녀 통학거리 제약 — 후보지가 현재 학군(용인 수지구)과 얼마나 먼가.
  5. 자금조달 갭 & 경쟁률 불확실성 — 가용 현금 대비 목표가 미정 상태를
     그대로 노출(추측 금액을 만들지 않음, 7.9 원칙).

각 항목은 URGENCY 3단계로 판정한다:
  🔴 긴급   — 지금 당장 사람이 행동해야 함 (기한 임박, 신규 공고 감지 등)
  🟡 재검토 — 전략/가정을 다시 볼 시점 (추세가 불리하게 이동 중)
  🟢 관망   — 별다른 조치 불필요, 계속 관찰만
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import date

from core.config import user_profile, portfolio_config
from collectors import manual as manual_collectors

URGENT = "🔴 긴급"
REVISE = "🟡 전략재검토"
WATCH = "🟢 관망"

_URGENCY_RANK = {URGENT: 2, REVISE: 1, WATCH: 0}

ALERTED_STATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "collectors", "subscription_monitor", "alerted_state.json",
)

# subscription-monitor.yml이 5~30분마다 갱신하는 실시간 감지 키워드
# (collectors/subscription_monitor/judge.py ALERT_KEYWORDS와 동일하게 유지).
ALERT_KEYWORDS = ["플랫폼시티", "광교", "원천동"]


@dataclass
class ConcernItem:
    name: str
    urgency: str            # URGENT | REVISE | WATCH
    status: str             # 현재 상태 한 줄
    recommendation: str     # 권고 행동 한 줄
    detail: list[str] = field(default_factory=list)  # 부연 설명 (근거)


@dataclass
class SubscriptionConcernReport:
    concerns: list[ConcernItem]
    overall_urgency: str
    headline: str


def _load_alerted_state() -> dict:
    if not os.path.exists(ALERTED_STATE_PATH):
        return {}
    try:
        with open(ALERTED_STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _check_income_cap_risk(profile: dict) -> ConcernItem:
    housing = profile.get("housing", {})
    pref = housing.get("income_cap_preference")
    strategy = housing.get("subscription_priority_strategy")

    if pref == "none" and strategy:
        return ConcernItem(
            name="소득제한 특별공급 배제 위험",
            urgency=WATCH,
            status="전략 확립됨 — 소득무관 60㎡ 초과 일반공급 우선 지원 방침 유지 중",
            recommendation="변화 없음. 새 공고가 뜨면 income_analysis.py가 60㎡ 초과분 소득요건 자동 확인",
            detail=[
                f"현재 전략: {strategy}",
                "2026-09-01 실전 검증(income_analysis.py, LH청약플러스 Playwright 검색)으로 "
                "'60㎡ 초과 일반공급 = 소득 무관' 규칙을 라이브 데이터로 재확인 완료",
            ],
        )
    return ConcernItem(
        name="소득제한 특별공급 배제 위험",
        urgency=REVISE,
        status="소득제한 회피 전략이 config/user.yaml에 명시돼 있지 않음",
        recommendation="config/user.yaml housing.income_cap_preference를 확인/설정할 것",
    )


def _check_platform_city_privatization_risk(profile: dict, alerted_state: dict) -> ConcernItem:
    housing = profile.get("housing", {})
    target = housing.get("target_complex", "")
    notices = manual_collectors.fetch_subscription_notices()
    platform_city_notice = next(
        (n for n in notices if n.get("is_platform_city") or "플랫폼시티" in (n.get("name") or "")),
        None,
    )

    # alerted_state.json에 매칭된 keyword가 있으면(compose.py NEW_MATCH가
    # 실제로 발동했다는 뜻) — 5~30분 주기 실시간 감시가 이미 뭔가 잡았다는 신호.
    matched_keywords = {v.get("keyword") for v in alerted_state.values() if v.get("keyword")}
    platform_city_hit = bool(matched_keywords & set(ALERT_KEYWORDS))

    if platform_city_notice:
        housing_type = platform_city_notice.get("housing_type")
        if housing_type == "민영":
            return ConcernItem(
                name="플랫폼시티 민영 분류 위험",
                urgency=URGENT,
                status=f"공고 확인됨 — '{platform_city_notice.get('name')}'가 민영(民營)으로 분류됨",
                recommendation="소득요건 무관하나 청약저축 순위제(민영) 규칙으로 즉시 재검토 — "
                "이 프레임워크(국민주택 소득요건)는 적용 안 됨, 별도 전략 필요",
                detail=[f"데이터 출처: {platform_city_notice.get('source', 'N/A')}"],
            )
        return ConcernItem(
            name="플랫폼시티 민영 분류 위험",
            urgency=URGENT,
            status=f"공고 확인됨 — '{platform_city_notice.get('name')}' (국민주택)",
            recommendation="즉시 income_analysis.py로 소득요건/60㎡초과 여부 분석 후 청약 여부 결정",
        )

    if platform_city_hit:
        return ConcernItem(
            name="플랫폼시티 민영 분류 위험",
            urgency=REVISE,
            status="실시간 감시(subscription-monitor.yml)에서 관련 키워드 매칭 이력 있음, 공고 상세는 아직 수동 미입력",
            recommendation="alerted_state.json/GitHub Issue 확인 후 data/manual_inputs/subscription_notices.yaml에 등록",
        )

    return ConcernItem(
        name="플랫폼시티 민영 분류 위험",
        urgency=WATCH,
        status=f"'{target}' 공고 아직 미발표 — 대기 중 (역사적으로 민영 분류 사례만 존재)",
        recommendation="공고 없음. subscription-monitor.yml이 5~30분마다 자동 감시 중, 조치 불필요",
        detail=[
            "과거 사례: 라온프라이빗 아르디에·e편한세상 용인역 플랫폼시티 → 전부 민영 분류",
            "2026-09-02 웹 검색 확인(공식 미확정, wiki/concepts/yongin-platform-city-project-facts.md 참고): "
            "공공주택은 A1~A4 블록(국민임대·영구임대 약 3,500세대 + 공공분양 약 1,500세대), "
            "공공분양 예상 시기 2026년 하반기~2027년 초 — 정식 공고일은 아직 어디서도 확정 발표 안 됨",
            f"실시간 감시 키워드: {', '.join(ALERT_KEYWORDS)}",
        ],
    )


def _check_moveout_deadline(profile: dict, today: date) -> ConcernItem:
    deadline_str = profile.get("housing", {}).get("moveout_deadline")
    if not deadline_str:
        return ConcernItem(
            name="전세 계약 만료 임박",
            urgency=WATCH,
            status="moveout_deadline 미설정",
            recommendation="config/user.yaml housing.moveout_deadline 확인 필요",
        )

    deadline = date.fromisoformat(deadline_str)
    days_left = (deadline - today).days

    if days_left < 0:
        urgency, note = URGENT, f"기한 이미 경과 (D+{-days_left})"
    elif days_left <= 90:
        urgency, note = URGENT, f"D-{days_left} — 3개월 이내"
    elif days_left <= 180:
        urgency, note = REVISE, f"D-{days_left} — 6개월 이내, 임시거주 계획 구체화 시점"
    else:
        urgency, note = WATCH, f"D-{days_left} — 아직 여유"

    recommendation = {
        URGENT: "임시 거주(재계약/신규 임차) 계약을 즉시 진행할 것 — 갱신청구권 이미 소진, 대안 없음",
        REVISE: "청약 타겟 2건(플랫폼시티/원천동)의 입주 시기와 이 기한을 대조해 임시거주 갭이 있는지 계산할 것",
        WATCH: "정기 확인만 유지",
    }[urgency]

    return ConcernItem(
        name="전세 계약 만료 임박",
        urgency=urgency,
        status=f"만료일 {deadline_str} ({note})",
        recommendation=recommendation,
        detail=["갱신청구권 이미 사용 — 재연장 불가, 반드시 새 거처로 이동해야 함"],
    )


def _check_school_commute_constraint(profile: dict) -> ConcernItem:
    housing = profile.get("housing", {})
    target = housing.get("target_complex", "")
    notices = manual_collectors.fetch_subscription_notices()
    non_platform_targets = [n for n in notices if not n.get("is_platform_city") and n.get("region")]

    far_targets = [n for n in non_platform_targets if "용인" not in (n.get("region") or "")]

    if far_targets:
        names = ", ".join(f"{n.get('name')}({n.get('region')})" for n in far_targets)
        return ConcernItem(
            name="자녀 통학거리 제약",
            urgency=REVISE,
            status=f"현재 학군(용인 수지구 문정중·풍천초) 밖 후보지 존재 — {names}",
            recommendation="해당 후보지가 실제 통학 가능 범위인지, 전학이 불가피한지 사전 결정 필요",
        )

    return ConcernItem(
        name="자녀 통학거리 제약",
        urgency=WATCH,
        status=f"등록된 후보 공고 없음 (메인 타겟 '{target}'은 현재 거주지와 동일 생활권)",
        recommendation="조치 불필요 — 새 후보지 등록 시 이 항목 재평가",
    )


def _check_funding_gap(payload: dict, portfolio: dict) -> ConcernItem:
    exposure = payload.get("exposure")
    sub_savings = portfolio.get("subscription_savings", {})
    savings_balance = sub_savings.get("balance_krw")

    detail = []
    if savings_balance:
        detail.append(f"청약통장 잔액: {savings_balance / 100_000_000:.3f}억원")
    if exposure is not None:
        detail.append(f"가용 현금(현금성+매각가능): {exposure.deployable_cash / 100_000_000:.2f}억원")

    return ConcernItem(
        name="자금조달 갭 & 경쟁률 불확실성",
        urgency=WATCH,
        status="양 타겟(플랫폼시티/원천동) 모두 공고 전 — 분양가·경쟁률 미정이라 갭을 계산할 근거 자체가 없음",
        recommendation="추측 금액 산정 금지 (7.9 원칙). 공고 확정 즉시 이 항목이 자동으로 재계산되도록 "
        "engine/personal/housing.py의 funding_gap_krw 로직이 이미 대기 중",
        detail=detail,
    )


def compute_subscription_concerns(payload: dict) -> SubscriptionConcernReport:
    """전체 5개 우려사항을 평가해 종합 판정을 낸다.

    payload는 build_report_payload()가 만드는 것과 동일한 dict — exposure
    모델(Section 0)이 이미 계산돼 있어야 자금조달 갭 항목이 완전해진다.
    """
    profile = user_profile()
    portfolio = portfolio_config()
    alerted_state = _load_alerted_state()
    today = date.today()

    concerns = [
        _check_income_cap_risk(profile),
        _check_platform_city_privatization_risk(profile, alerted_state),
        _check_moveout_deadline(profile, today),
        _check_school_commute_constraint(profile),
        _check_funding_gap(payload, portfolio),
    ]

    urgent = [c for c in concerns if c.urgency == URGENT]
    revise = [c for c in concerns if c.urgency == REVISE]

    if urgent:
        overall = URGENT
        headline = f"🔴 긴급 대응 {len(urgent)}건: " + ", ".join(c.name for c in urgent)
    elif revise:
        overall = REVISE
        headline = f"🟡 전략재검토 {len(revise)}건: " + ", ".join(c.name for c in revise)
    else:
        overall = WATCH
        headline = "5개 우려사항 모두 관망 단계 — 오늘은 긴급 조치 불필요"

    return SubscriptionConcernReport(concerns=concerns, overall_urgency=overall, headline=headline)
