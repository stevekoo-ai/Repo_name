"""Comprehensive Crisis Index (CCI) scoring engine — 9 modules consolidated.

Modules A-I evaluate global macro state and output 0-100 score:
- 0-30 (GREEN): Expansion, capital injection
- 31-55 (YELLOW): Deceleration, capital hedging
- 56-100 (RED): Systemic breakdown, capital evacuation

Fallback strategy:
- Primary data source → FRED alternative → cached/stale data → synthetic calculation → 0
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from collectors import base as collector_base
from collectors import fred, ecos, kosis
from core.logger import log_event
from core import cache as cache_mod


@dataclass
class CCIDetail:
    """Comprehensive Crisis Index scoring breakdown."""
    sahm_score: int
    yield_curve_score: int
    harvey_score: int
    copper_gold_score: int
    credit_score: int
    buffett_score: int
    rule20_score: int
    k_sahm_score: int
    semiconductor_score: int
    total_score: int

    # Raw values
    ur_ma3: Optional[float] = None
    ur_min_12m: Optional[float] = None
    spread_10y2y: Optional[float] = None
    spread_10y3m: Optional[float] = None
    copper_gold_ratio: Optional[float] = None
    hy_oas: Optional[float] = None
    buffett_ratio: Optional[float] = None
    rule20_value: Optional[float] = None
    k_emp_yoy: Optional[float] = None
    semi_cycle_index: Optional[float] = None

    # 2026-09-01 신설 — 사용자 지적: "데이터 신선도가 표시가 없네! 특히 몇점이고
    # 판단만 하는 항목은 믿을 수가 없네!". 모듈명 -> {quality, series, as_of,
    # days_stale}. PRIMARY(1순위 시리즈 실측) / FALLBACK(대체 시리즈로 계산) /
    # NO_DATA(둘 다 없음) 3단계 — 리포트가 "이 점수, 오늘 데이터야 아니면 몇 달
    # 전 값이야?"를 항상 답할 수 있게 한다. _module_data_quality() 참고.
    data_quality: dict = field(default_factory=dict)

    @property
    def state(self) -> str:
        if self.total_score <= 30:
            return "GREEN"
        elif self.total_score <= 55:
            return "YELLOW"
        else:
            return "RED"


def _get_latest(series_id: str, days_back: int = 1, fallback_series: Optional[str] = None) -> Optional[float]:
    """Fetch latest value from normalized collector data, with fallback to alternate series."""
    df = collector_base.read_normalized(series_id)
    if not df.empty:
        latest = df.sort_values("date").iloc[-1]
        value = latest["value"] if latest["value"] is not None else None
        if value is not None:
            return float(value)

    if fallback_series:
        df_fallback = collector_base.read_normalized(fallback_series)
        if not df_fallback.empty:
            latest = df_fallback.sort_values("date").iloc[-1]
            value = latest["value"] if latest["value"] is not None else None
            if value is not None:
                return float(value)

    return None


def _get_series_window(series_id: str, days: int) -> list[float]:
    """Get all values in N-day window, newest first."""
    df = collector_base.read_normalized(series_id)
    if df.empty:
        return []
    df = df.sort_values("date")
    # read_normalized returns "date" as datetime.date objects
    cutoff = (datetime.now() - timedelta(days=days)).date()
    window_df = df[df["date"] >= cutoff]
    return window_df["value"].dropna().tolist()[::-1]


def _moving_avg(series_id: str, window: int = 3) -> Optional[float]:
    """N-period moving average of latest values."""
    values = _get_series_window(series_id, window * 30)
    if len(values) < window:
        return None
    return sum(values[:window]) / window


def _min_window(series_id: str, months: int = 12) -> Optional[float]:
    """Minimum value over N months."""
    values = _get_series_window(series_id, months * 30)
    return min(values) if values else None


def _series_as_of(series_id: str) -> tuple[Optional[float], Optional[str], Optional[int]]:
    """최신 데이터 포인트의 값·날짜·오늘 기준 며칠 지났는지를 그대로 반환 —
    _get_series_window()와 달리 신선도 컷오프를 걸지 않는다.

    2026-09-01 이 불일치 자체가 실제 버그의 원인이었다: _get_series_window(id, 60)은
    60일 넘은 값을 조용히 빈 리스트로 걸러내는데, _get_latest()는 그 값이 아무리
    오래됐어도 아무 경고 없이 "최신값"으로 반환해왔다. fred_us_industrial_production이
    (월간 시리즈, ~2개월 지연) 62일 지연 상태였던 게 이 불일치를 실측으로 드러냈고,
    그 결과 반도체 산업사이클 폴백이 "값은 있는데 window()만 텅 비어" 조용히
    데이터없음으로 떨어졌다. 이 함수는 오직 "지금 시점 데이터 상태"를 있는 그대로
    보고하기 위한 것 — 판정 로직(_get_series_window 기반)은 그대로 둔다."""
    df = collector_base.read_normalized(series_id)
    if df.empty:
        return None, None, None
    latest = df.sort_values("date").iloc[-1]
    value = latest["value"]
    if value is None:
        return None, None, None
    as_of = latest["date"]
    as_of_str = as_of.isoformat() if hasattr(as_of, "isoformat") else str(as_of)
    try:
        days_stale = (datetime.now().date() - as_of).days
    except TypeError:
        days_stale = None
    return float(value), as_of_str, days_stale


# 모듈명 -> 그 모듈이 실제로 참조하는 시리즈들(우선순위 순, score_*() 내부
# 폴백 순서와 일치해야 함). calculate_cci()가 각 score_*() 호출과 별개로 이
# 표를 참고해 "이 점수가 실측 최신 데이터에서 나왔는지, 지연된 대체 시리즈에서
# 나왔는지, 아예 데이터가 없는지"를 리포트에 노출한다 — score_*()의 반환
# 시그니처는 바꾸지 않는다(tests/test_cci_fallback.py가 위치 기반으로 언패킹
# 하므로). rule20/buffett은 2026-09-01부로 아래에서 영구 비활성화됐으니
# 참조 시리즈를 남겨두지 않는다(값을 지어내지 않는다는 원칙과 동일선상 —
# "신선도는 있는데 계산은 가짜"인 상태를 만들지 않기 위함).
_MODULE_SERIES = {
    "sahm": ["fred_us_unemployment"],
    "yield_curve": ["fred_us_10y_treasury"],
    "harvey": ["fred_us_yield_curve_10y2y"],
    "copper_gold": ["fred_us_industrial_production"],
    "credit_oas": ["fred_hy_oas"],
    "buffett": [],
    "rule_of_20": [],
    "k_sahm": ["kosis_k_employed_yoy", "fred_kr_unemployment_oecd"],
    "semiconductor": ["kosis_semiconductor_shipment_index", "fred_us_industrial_production"],
}


def _module_data_quality(module: str) -> dict:
    """모듈이 실제로 쓴(또는 못 쓴) 시리즈의 신선도 — PRIMARY(1순위 시리즈 사용)/
    FALLBACK(대체 시리즈 사용)/NO_DATA(참조 시리즈가 없거나 전부 비어 있음) 3단계."""
    series_list = _MODULE_SERIES.get(module, [])
    for i, series_id in enumerate(series_list):
        value, as_of, days_stale = _series_as_of(series_id)
        if value is not None:
            return {
                "quality": "PRIMARY" if i == 0 else "FALLBACK",
                "series": series_id, "as_of": as_of, "days_stale": days_stale,
            }
    return {"quality": "NO_DATA", "series": None, "as_of": None, "days_stale": None}


def score_sahm() -> tuple[int, Optional[float], Optional[float]]:
    """Module A: Sahm Rule (US unemployment momentum).

    Primary: FRED US unemployment → Fallback: cached data → OECD-via-FRED proxy

    Returns: (score, ma3, min_12m)
    """
    ur_data = fred.fetch_series("us_unemployment")
    series_id = "fred_us_unemployment"

    if ur_data.value is None:
        ma3 = _moving_avg(series_id, window=3)
        if ma3 is None:
            log_event("cci.sahm.fallback", source="none_available")
            return 0, None, None

    ma3 = _moving_avg(series_id, window=3)
    min_12m = _min_window(series_id, months=12)

    if ma3 is None or min_12m is None:
        log_event("cci.sahm.partial", ma3=ma3, min_12m=min_12m)
        return 0, ma3, min_12m

    diff = ma3 - min_12m
    if diff >= 0.5:
        score = 20
    elif diff >= 0.3:
        score = 10
    else:
        score = 0

    return score, ma3, min_12m


def score_yield_curve() -> tuple[int, Optional[float], Optional[float], int]:
    """Module B: Yield Curve Inversion (10Y-2Y, 10Y-3M spreads).

    Returns: (score, spread_10y2y, spread_10y3m, consecutive_inverted_days)
    """
    y10y = _get_latest("fred_us_10y_treasury")
    y2y = _get_latest("fred_us_2y_treasury")
    y3m = _get_latest("fred_us_3m_treasury") or _get_latest("fred_us_treasury_3m")

    if y10y is None or y2y is None:
        return 0, None, None, 0

    spread_10y2y = y10y - y2y
    spread_10y3m = y10y - (y3m or y2y)

    # Count consecutive inverted days (simplified: check last 10 days)
    history_10y2y = _get_series_window("fred_us_yield_curve_10y2y", 10)
    consecutive_inverted = sum(1 for v in history_10y2y if v < 0)

    if spread_10y2y < 0 or spread_10y3m < 0:
        score = 15 if consecutive_inverted >= 10 else 5
    else:
        score = 0

    return score, spread_10y2y, spread_10y3m, consecutive_inverted


def score_harvey() -> tuple[int, int]:
    """Module C: Campbell Harvey's Inversion Filter (3+ months inverted).

    Returns: (score, consecutive_inverted_months)
    """
    # Simplified: check if last 3 monthly values of 10Y-3M spread < 0
    history = _get_series_window("fred_us_yield_curve_10y2y", 90)
    if len(history) < 3:
        return 0, 0

    recent_3m = history[:3]
    inverted_months = sum(1 for v in recent_3m if v < 0)

    score = 15 if inverted_months >= 3 else 0
    return score, inverted_months


def score_copper_gold() -> tuple[int, Optional[float]]:
    """Module D: Copper-to-Gold Ratio (industrial demand vs safe-haven).

    Fallback: use industrial production vs USD index as proxy for risk appetite.

    Returns: (score, ratio)
    """
    us_indpro = _get_latest("fred_us_industrial_production")
    us_dollar = _get_latest("fred_us_dollar_index")

    if us_indpro is None or us_dollar is None:
        log_event("cci.copper_gold.fallback", source="data_unavailable")
        return 0, None

    indpro_history = _get_series_window("fred_us_industrial_production", 60)
    dollar_history = _get_series_window("fred_us_dollar_index", 60)

    if not indpro_history or not dollar_history or len(indpro_history) < 2:
        return 0, None

    indpro_change = (indpro_history[0] - indpro_history[-1]) / indpro_history[-1]
    dollar_change = (dollar_history[0] - dollar_history[-1]) / dollar_history[-1]

    ratio = indpro_change / (dollar_change + 0.001) if dollar_change != 0 else indpro_change

    if ratio < -0.03:
        score = 8
    elif ratio < -0.01:
        score = 3
    else:
        score = 0

    return score, ratio


def score_credit_oas() -> tuple[int, Optional[float]]:
    """Module E: High-Yield Bond OAS (credit crunch & liquidity).

    Primary: FRED HY OAS → Fallback: cached/stale data → synthetic spread calculation

    Returns: (score, hy_oas_percent)
    """
    hy_oas_data = fred.fetch_series("hy_oas")
    hy_oas = hy_oas_data.value

    if hy_oas is None:
        hy_oas = _get_latest("fred_hy_oas")

    if hy_oas is None:
        stale = cache_mod.get_stale("fred:BAMLH0A0HYM2")
        if stale:
            import pandas as pd
            df = pd.DataFrame(stale)
            if not df.empty:
                hy_oas = float(df.sort_values("date").iloc[-1]["value"])
                log_event("cci.credit_oas.fallback", source="stale_cache")

    if hy_oas is None:
        log_event("cci.credit_oas.fallback", source="none_available")
        return 0, None

    if hy_oas >= 6.5:
        score = 15
    elif hy_oas >= 4.5:
        score = 5
    else:
        score = 0

    return score, hy_oas


def score_buffett() -> tuple[int, Optional[float]]:
    """Module F: Buffett Indicator — 정의상 미국 전체 상장 시가총액 / GDP 비율
    (통상 100~200% 레인지, 180%↑면 고평가 경고)이다.

    2026-09-01 영구 비활성화(사용자 지적: "위기지수 분석의 기타항목에 5는 뭐야?
    왜 계속 같은 값이야?" 조사 중 발견) — 이 저장소엔 시가총액 데이터 소스가
    전혀 없다(grep 확인: market_cap/시가총액 계열 시리즈 0건). 실제로 돌아가던
    코드는 us_gdp_qoq(분기 GDP 성장률, 통상 -5%~+5%)를 2배 해 150/180과
    비교하고 있었는데, 분기 성장률은 정의상 150을 절대 넘을 수 없다(그러려면
    분기 GDP가 전분기 대비 75배로 뛰어야 함) — 즉 이 조건은 항상 거짓,
    score_buffett()은 데이터가 있든 없든 구조적으로 영원히 0점이었다(반대
    극단이지만 Rule of 20과 같은 버그 클래스 — 성장률 스케일 값을 레벨 스케일
    임계값과 비교). 진짜 Buffett Indicator에 필요한 시가총액/GDP 데이터가
    이 저장소에 추가되기 전까지, 값을 지어내지 않고 판정하지 않는다(R3).

    Returns: (score, buffett_ratio) — 항상 (0, None).
    """
    log_event("cci.buffett.disabled", reason="no market-cap/GDP ratio data source in this repo — wiki/log.md 2026-09-01")
    return 0, None


def score_rule_of_20() -> tuple[int, Optional[float]]:
    """Module G: Rule of 20 — 정의상 S&P500 PER + CPI YoY 인플레이션율의 합이
    20을 넘으면 고평가 경고다.

    2026-09-01 영구 비활성화(사용자 지적: "위기지수 분석의 기타항목에 5는 뭐야?
    왜 계속 같은 값이야?") — 이 저장소엔 PER 데이터 소스가 전혀 없다(grep 확인:
    PER/Shiller 계열 시리즈 0건). "PER 데이터 없으면 CPI만으로 대체"라던 이
    docstring도 사실과 달랐다 — PER을 시도하는 코드 자체가 없어 폴백이 아니라
    유일한 경로였다. 게다가 그 유일한 경로가 fred_us_cpi(CPI **지수 레벨**,
    기준연도=100 스케일이라 늘 300 안팎)를 그대로 20과 비교하고 있어서, 이
    조건은 데이터가 있는 한 항상 참 — 매일 5/5 만점이 구조적으로 고정된
    상태였다(CPI가 20 밑으로 가려면 기준연도 대비 94% 디플레이션이 나야 함).
    실제 인플레이션율(YoY %)도, PER도 아닌 값을 판정에 쓰고 있었던 것 — 진짜
    Rule of 20에 필요한 PER 데이터가 이 저장소에 추가되기 전까지, 값을 지어내지
    않고 판정하지 않는다(R3).

    Returns: (score, rule20_value) — 항상 (0, None).
    """
    log_event("cci.rule_of_20.disabled", reason="no PER data source in this repo — wiki/log.md 2026-09-01")
    return 0, None


def score_k_sahm() -> tuple[int, Optional[float]]:
    """Module H: K-Sahm Rule — KOSIS 고용 YoY(%) 시계열이 3개월 연속 마이너스면
    약세로 판정한다.

    Primary: KOSIS K employment YoY → Fallback: FRED OECD 한국 실업률(정보용만)

    2026-09-01 버그 수정(사용자 지적: "데이터 신선도가 표시가 없네! 특히 몇점이고
    판단만 하는 항목은 믿을 수가 없네!" 조사 중 발견) — 예전 코드는 KOSIS 시리즈가
    없으면 FRED 실업률(단위: %, 통상 2~4)로 대체하고, 그 값을
    `weak_months = v < 100000` 같은 KOSIS 고용증가율(YoY %) 전용 임계값과 그대로
    비교했다. 실업률이든 고용증가율이든 현실적인 값은 전부 100000보다 작아서,
    폴백 히스토리가 3개 이상 쌓이는 순간 이 조건은 사실상 항상 참 — 지금까지는
    폴백 히스토리가 우연히 1개뿐이라 0점으로 안전했을 뿐인, 데이터가 쌓이면
    언제든 터질 수 있던 잠복 버그였다. 서로 다른 지표(고용증가율 vs 실업률)를
    같은 임계값으로 섞지 않는다 — KOSIS 원 시리즈가 없으면 점수는 계산하지 않고
    FRED 값은 참고용 원자료로만 반환한다(R3).

    Returns: (score, k_emp_yoy_or_unemployment_rate_for_reference_only)
    """
    k_emp_data = kosis.fetch_series("k_employed_yoy")
    k_emp = k_emp_data.value
    history = _get_series_window("kosis_k_employed_yoy", 90)

    if k_emp is not None and history:
        weak_months = sum(1 for v in history[:3] if v < 0)  # YoY 고용증가율 마이너스(감소) 3개월
        score = 5 if weak_months >= 3 else 0
        return score, k_emp

    # KOSIS 시리즈가 없다 — FRED 실업률은 다른 지표라 이 점수를 계산하는 데
    # 쓰지 않는다(창작 금지). 원시값은 참고용으로만 반환.
    fallback = _get_latest("fred_kr_unemployment_oecd")
    if fallback is not None:
        log_event("cci.k_sahm.fallback_info_only", source="fred_oecd_unemployment", value=fallback)
        return 0, fallback

    return 0, None


def score_semiconductor_cycle() -> tuple[int, Optional[float]]:
    """Module I: Semiconductor Inventory Cycle (restocking vs decumulation).

    Primary: KOSIS semiconductor data → Fallback: US industrial production proxy

    Returns: (score, cycle_index)
    """
    ship = _get_latest("kosis_semiconductor_shipment_index")
    inv = _get_latest("kosis_semiconductor_inventory_index")

    if ship is None or inv is None:
        us_indpro = _get_latest("fred_us_industrial_production")
        if us_indpro is None:
            log_event("cci.semiconductor.fallback", source="none_available")
            return 0, None

        indpro_history = _get_series_window("fred_us_industrial_production", 60)
        if indpro_history and len(indpro_history) >= 2:
            cycle_index = (indpro_history[0] - indpro_history[-1]) / indpro_history[-1]
            log_event("cci.semiconductor.fallback", source="us_industrial_production", cycle_index=cycle_index)

            if cycle_index < 0:
                score = 5
            else:
                score = 0
            return score, cycle_index
        return 0, None

    ship_history = _get_series_window("kosis_semiconductor_shipment_index", 60)
    inv_history = _get_series_window("kosis_semiconductor_inventory_index", 60)

    if not ship_history or not inv_history:
        return 0, None

    ship_change = (ship_history[0] - ship_history[-1]) / ship_history[-1] if ship_history else 0
    inv_change = (inv_history[0] - inv_history[-1]) / inv_history[-1] if inv_history else 0

    cycle_index = ship_change - inv_change

    if cycle_index < 0 and inv_change > 0:
        score = 10
    else:
        score = 0

    return score, cycle_index


def calculate_cci() -> CCIDetail:
    """Calculate comprehensive CCI score (0-100).

    Aggregates all 9 modules and returns detailed breakdown.
    """
    sahm_score, ur_ma3, ur_min_12m = score_sahm()
    yield_score, spread_10y2y, spread_10y3m, _ = score_yield_curve()
    harvey_score, _ = score_harvey()
    copper_score, copper_gold = score_copper_gold()
    credit_score, hy_oas = score_credit_oas()
    buffett_score, buffett = score_buffett()
    rule20_score, rule20 = score_rule_of_20()
    k_sahm_score, k_emp = score_k_sahm()
    semi_score, semi_cycle = score_semiconductor_cycle()

    total = min(100, sahm_score + yield_score + harvey_score + copper_score +
                credit_score + buffett_score + rule20_score + k_sahm_score + semi_score)

    log_event("cci.calculated", total_score=total, sahm=sahm_score, yield_curve=yield_score,
              state="GREEN" if total <= 30 else ("YELLOW" if total <= 55 else "RED"))

    data_quality = {module: _module_data_quality(module) for module in _MODULE_SERIES}

    return CCIDetail(
        sahm_score=sahm_score,
        yield_curve_score=yield_score,
        harvey_score=harvey_score,
        copper_gold_score=copper_score,
        credit_score=credit_score,
        buffett_score=buffett_score,
        rule20_score=rule20_score,
        k_sahm_score=k_sahm_score,
        semiconductor_score=semi_score,
        total_score=total,
        ur_ma3=ur_ma3,
        ur_min_12m=ur_min_12m,
        spread_10y2y=spread_10y2y,
        spread_10y3m=spread_10y3m,
        copper_gold_ratio=copper_gold,
        hy_oas=hy_oas,
        buffett_ratio=buffett,
        rule20_value=rule20,
        k_emp_yoy=k_emp,
        semi_cycle_index=semi_cycle,
        data_quality=data_quality,
    )


def get_sk_hynix_action(cci: CCIDetail) -> dict:
    """Translate CCI state into SK Hynix position management.

    Returns action dict with portfolio guidance.
    """
    if cci.state == "GREEN":
        return {
            "state": "GREEN",
            "action": "적극 매수 (Long)",
            "max_weight": 25,
            "description": "거시 유동성 안정. 고용시장 확장세. 반도체 재고 확충 진행 중.",
            "signal": "공급망발 조정 구간에서 분할매수(DCA) 실행. CCI 30 돌파 전까지 보유.",
        }
    elif cci.state == "YELLOW":
        return {
            "state": "YELLOW",
            "action": "방어적 비중 축소",
            "max_weight": 10,
            "description": "장단기 금리 역전 관찰됨. 밸류에이션 확장. 모멘텀 둔화 중.",
            "signal": "체계적으로 이익 실현. 채권/달러 현금성 자산으로 재배분.",
        }
    else:  # RED
        return {
            "state": "RED",
            "action": "전량 청산 및 헤지",
            "max_weight": 0,
            "description": "Sahm Rule 발동. 신용경색 확인. 반도체 재고 누적 심화.",
            "signal": "경기순환 성장주 롱 포지션 전량 매도. 인버스 ETF로 숏 포지션 개시.",
        }
