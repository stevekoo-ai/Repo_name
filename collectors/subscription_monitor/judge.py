"""
Step 2 of the subscription-monitor autonomous pipeline: JUDGE.

Given fetched listing rows + my subscription-savings account profile, produce a
deterministic verdict per listing (eligibility, competitiveness, priority,
recommended action). Pure rule-based — same input always yields the same output,
no LLM, no network, no token cost.

The scoring rules are transcribed from docs/SUBSCRIPTION_SYSTEM.md (the
human-edited scoring rubric) so this file and that doc stay in sync. My profile
constants live here as the single source of truth and are re-exported for
fetch_and_render.py to import (see CLAUDE.md "single source of information" note
in user-profile.md).
"""

from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))

# --- My subscription-savings profile (single source of truth) ---------------
# Mirrors wiki/entities/user-profile.md "청약통장 상세" table + config/portfolio.yaml.
# fetch_and_render.py imports these instead of keeping its own copy.
MY_SAVINGS_TOTAL = 28_050_000
MY_SAVINGS_ROUNDS = 249
MY_JOIN_DATE = "2005-11-03"          # 2005-11-03 (confirmed vs PEOS portfolio.yaml)
MY_MONTHLY_DEPOSIT = 250_000         # 최고액 납입 (납입인정 최고금액)
MY_REGION = "경기"                    # 현재 거주: 용인 수지구 → 경기
MY_TARGET_KEYWORDS_REGIONS = {"서울", "경기"}  # 관심 지역 (fetch 필터와 동일)

# Keyword matches that mark a listing as personally relevant (플랫폼시티/광교신도시).
# Kept here so compose.py and fetch_and_render.py share one definition.
ALERT_KEYWORDS = ["플랫폼시티", "광교", "원천동"]

# --- Scoring bands (from docs/SUBSCRIPTION_SYSTEM.md §3.2) -------------------
# 청약통장 점수 (만점 40). My profile saturates every band → 40/40 (confirmed).
SCORE_JOIN_TERM_MAX = 15   # 20년 이상 → 15점 (나: 20년 8개월)
SCORE_ROUNDS_MAX = 15       # 240회 이상 → 15점 (나: 249회)
SCORE_DEPOSIT_MAX = 10      # 최고액(25만원) 납입 → 10점 (나: 25만원)
MY_ACCOUNT_SCORE = SCORE_JOIN_TERM_MAX + SCORE_ROUNDS_MAX + SCORE_DEPOSIT_MAX  # = 40

# --- Priority bands ----------------------------------------------------------
DAYS_IMMINENT = 1     # 접수 시작 D-1 이내 → 우선순위 1단계 상승
DAYS_SOON = 3         # 접수 시작 D-3 이내 → "접수 임박" 분류


def _id(r: dict) -> str:
    """Stable identifier for a listing (matches alerts.py key choice)."""
    return r.get("HOUSE_MANAGE_NO") or r.get("PBLANC_NO") or ""


def _days_to_open(r: dict, now_kst: datetime) -> int | None:
    """Days from now until the listing's general-supply reception start date.
    Returns None if the date is missing/unparseable."""
    bgn = r.get("RCEPT_BGNDE")
    if not bgn:
        return None
    try:
        d = datetime.strptime(bgn, "%Y-%m-%d").replace(tzinfo=KST)
    except ValueError:
        return None
    return (d.date() - now_kst.date()).days


def _is_newlywed(r: dict) -> bool:
    return "신혼희망타운" in (r.get("HOUSE_NM") or "")


def find_keyword(r: dict, extra_keyword: str | None = None) -> str | None:
    """Which alert keyword (if any) appears in this listing's name or address."""
    haystack = f"{r.get('HOUSE_NM', '')} {r.get('HSSPLY_ADRES', '')}"
    keywords = list(ALERT_KEYWORDS)
    if extra_keyword:
        keywords.append(extra_keyword)
    return next((kw for kw in keywords if kw in haystack), None)


def judge_one(r: dict, now_kst: datetime, extra_keyword: str | None = None) -> dict:
    """Judge a single listing. Deterministic."""
    keyword = find_keyword(r, extra_keyword)
    region = r.get("SUBSCRPT_AREA_CODE_NM") or ""
    days = _days_to_open(r, now_kst)
    newlywed = _is_newlywed(r)

    # Eligibility: only listings in our target regions and with a future/present
    # reception window are eligible (fetch already filters by RCEPT_ENDDE>=today
    # and region, but judge defensively re-checks region).
    eligible = region in MY_TARGET_KEYWORDS_REGIONS

    # Competitiveness from account score — my account is maxed (40/40), so any
    # eligible 순차제 listing is HIGH competitiveness. 신혼희망타운 uses separate
    # criteria so we cap at MED with a caveat.
    if not eligible:
        competitiveness = "LOW"
    elif newlywed:
        competitiveness = "MED"
    else:
        competitiveness = "HIGH"

    # Base priority from keyword match + competitiveness.
    if keyword:
        base = "HIGH"
    elif competitiveness == "HIGH":
        base = "MED"
    else:
        base = "LOW"

    # Imminence bump: reception opening within D-1 lifts priority one tier.
    priority = base
    if days is not None and days <= DAYS_IMMINENT and priority != "HIGH":
        priority = "HIGH" if priority == "MED" else "MED"

    # 신혼희망타운 never above MED (separate criteria, caveat).
    if newlywed and priority == "HIGH":
        priority = "MED"

    # Recommended action wording.
    action_map = {
        "HIGH": "지원 강력 권장",
        "MED": "검토 권장",
        "LOW": "참고만",
    }
    recommended_action = action_map[priority]

    # Human-readable reason (deterministic composition, not LLM prose).
    parts = []
    if keyword:
        parts.append(f"{keyword} 매칭")
    parts.append(f"통장점수 {MY_ACCOUNT_SCORE}/40")
    if competitiveness == "HIGH":
        parts.append("순차제 유리")
    if newlywed:
        parts.append("신혼희망타운(별도기준, 캐비엣)")
    if days is not None:
        if days < 0:
            parts.append(f"접수 중(D-day {abs(days)}일 경과)")
        elif days == 0:
            parts.append("접수 오늘 시작")
        elif days <= DAYS_SOON:
            parts.append(f"접수 D-{days}")
        else:
            parts.append(f"접수 D-{days}")
    reason = " · ".join(parts) if parts else "해당 없음"

    return {
        "id": _id(r),
        "name": r.get("HOUSE_NM") or "(이름없음)",
        "region": region,
        "eligible": eligible,
        "match_keyword": keyword,
        "competitiveness": competitiveness,
        "score": MY_ACCOUNT_SCORE,
        "days_to_open": days,
        "priority": priority,
        "reason": reason,
        "recommended_action": recommended_action,
        "is_newlywed": newlywed,
        "row": r,  # keep the raw row so compose.py can render details without re-fetching
    }


def judge_listings(rows: list[dict], now_kst: datetime, extra_keyword: str | None = None) -> list[dict]:
    """Judge every row. Returns verdicts sorted by priority (HIGH→MED→LOW) then
    by days_to_open ascending (soonest first)."""
    verdicts = [judge_one(r, now_kst, extra_keyword) for r in rows]
    order = {"HIGH": 0, "MED": 1, "LOW": 2}
    verdicts.sort(
        key=lambda v: (
            order.get(v["priority"], 9),
            v["days_to_open"] if v["days_to_open"] is not None else 9999,
        )
    )
    return verdicts


def summarize(verdicts: list[dict]) -> dict:
    """Aggregate counts for the daily digest."""
    def count(p: str) -> int:
        return sum(1 for v in verdicts if v["priority"] == p)
    imminent = [v for v in verdicts if v["days_to_open"] is not None and v["days_to_open"] <= DAYS_SOON]
    return {
        "total": len(verdicts),
        "high": count("HIGH"),
        "med": count("MED"),
        "low": count("LOW"),
        "imminent": imminent,  # 접수 임박(D-3 이내) 매물 목록
        "imminent_count": len(imminent),
    }
