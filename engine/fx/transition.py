"""FRS 출력 B — 국면 전환 경고.

설계 §3. 점수 레벨이 아니라 **과거 국면의 종료 패턴을 코드화한 감지기 4종**이다.
"지금 점수가 높다/낮다"가 아니라 "지금 국면이 곧 끝날 조짐인가"를 묻는다.

## trigger_kind 를 함께 내는 이유 (설계 §6.5.2)

경고를 켜는 것만으로는 부족하다. [환율 국면과 달러 자산]
(../../wiki/concepts/fx-episode-dollar-assets.md) §4의 실측 —
국면 종료 직후 진입한 10년물의 12개월 수익 중앙값은 −0.3%로 무조건 진입
(+3.9%)보다 4.2%p 나쁘다. **단, 유일한 예외 ④(2018-10, +16.2%)는 종료
원인이 미국 긴축이 아니라 무역전쟁이었고 연준이 오히려 완화로 돌아섰다.**

즉 같은 "종료 경고"라도 원인이 `US_TIGHTENING`이냐 `NON_US_SHOCK`이냐에
따라 장기채 함의가 정반대다. 그래서 감지기는 종류를 반드시 함께 낸다.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum

from engine.fx import series as S
from engine.fx.regime_score import (
    MAX_AGE_DAYS, FRSDetail, calculate_frs, ma36_gap,
)

# usdkrw-below-ma36-episodes.md — 3개월 이상 하회 구간 7회의 지속기간 중앙값
HISTORICAL_MEDIAN_MONTHS = 11

# 이격 극단 임계 — 과거 최대 이격이 -11.9%(2011-07)였고, 그 근처에서 평균회귀가
# 시작됐다. 8%를 "극단"의 문턱으로 잡는다(설계 §3).
GAP_EXTREME_PCT = 8.0


# ─────────────────────────────────────────────────────────────
# 2026-09-10 백테스트로 **측정된** 감지기별 예측력 (설계 §6 합격 기준 2·3)
#
# 2008-01~2026-09 하회 국면 83개월에서, "종료 N개월 이내"를 맞히는 정밀도를
# 기저율로 나눈 값(리프트). 1.0 = 아무 정보 없음.
#
#   감지기            3개월    6개월   12개월
#   경과 개월          2.31x   1.98x   1.43x   ← 단기 예측력 최강(정밀도 83%)
#   이격 극단          0.00x   0.00x   1.43x   ← 장기 선행. 단기엔 무용
#   종료 트리거         0.92x   1.19x   0.95x   ← 미약
#   모멘텀 반전         0.30x   0.85x   1.02x   ← 모든 창에서 ~1.0 = 정보 없음
#
# ⚠ 표본은 국면 5개뿐이다. 성적이 나쁜 감지기를 지우지 **않는** 이유가 그것 —
# 5개로 지우면 그것도 과적합이다. 대신 측정값을 여기 남기고 리포트가 네 개를
# 동등하게 취급하지 못하게 한다. 종료 트리거는 리프트가 낮아도 별도 가치가
# 있다 — 켜진 원인(trigger_kind)이 장기채 함의를 가르는 유일한 정보다
# (2018-03·2021-02에 정확히 발화했다).
DETECTOR_EVIDENCE: dict[str, dict] = {
    "duration": {"lift_3m": 2.31, "lift_6m": 1.98, "lift_12m": 1.43,
                 "verdict": "검증됨 — 단기 예측력 최강"},
    "gap_extreme": {"lift_3m": 0.00, "lift_6m": 0.00, "lift_12m": 1.43,
                    "verdict": "장기(12개월) 선행 — 단기 판단엔 쓰지 말 것"},
    "exit_trigger": {"lift_3m": 0.92, "lift_6m": 1.19, "lift_12m": 0.95,
                     "verdict": "예측력 미약 — 다만 원인(trigger_kind) 제공이 본 가치"},
    "momentum_reversal": {"lift_3m": 0.30, "lift_6m": 0.85, "lift_12m": 1.02,
                          "verdict": "⚠ 이번 표본에서 예측력 확인 안 됨"},
}


def evidence_for(key: str) -> dict:
    """감지기의 측정된 예측력. 리포트가 경고를 표기할 때 함께 보여준다 —
    "경고가 켜졌다"만 보여주고 그게 얼마나 믿을 만한지 안 보여주면
    R4(근거만 제공)의 취지에 어긋난다."""
    return DETECTOR_EVIDENCE.get(key, {"verdict": "미측정"})


class TriggerKind(Enum):
    """무엇이 국면을 끝내려 하는가. 장기채 함의가 정반대라 반드시 구분한다."""
    US_TIGHTENING = "미국 긴축 전환"      # 금리 상승 → 장기채 평가손 경계
    NON_US_SHOCK = "미국 외 충격"         # 오히려 완화로 돌아설 수 있음
    FUEL_EXHAUSTION = "연료 소진"         # 경상·수출 둔화. 금리 방향은 중립
    UNKNOWN = "원인 미상"


@dataclass(frozen=True)
class Warning_:
    key: str
    label: str
    fired: bool
    kind: TriggerKind
    detail: str


@dataclass(frozen=True)
class TransitionReport:
    as_of: date
    warnings: list[Warning_] = field(default_factory=list)

    @property
    def fired(self) -> list[Warning_]:
        return [w for w in self.warnings if w.fired]

    @property
    def count(self) -> int:
        return len(self.fired)

    @property
    def level(self) -> str:
        """설계 §3 — 켜진 개수로 3단계."""
        if self.count >= 3:
            return "🔴 전환임박"
        if self.count == 2:
            return "🟡 전환주의"
        return "🟢 안정"

    @property
    def credible_fired(self) -> list[Warning_]:
        """켜진 경고 중 **예측력이 확인된 것만**(리프트 6개월 또는 3개월 > 1.2).

        전부를 같은 무게로 보여주면 정보 없는 감지기가 판단을 흐린다."""
        return [w for w in self.fired
                if max(evidence_for(w.key).get("lift_3m", 0),
                       evidence_for(w.key).get("lift_6m", 0)) > 1.2]

    @property
    def trigger_kind(self) -> TriggerKind:
        """켜진 경고들의 원인 중 대표값.

        US_TIGHTENING이 하나라도 있으면 그걸 우선한다 — 장기채 경계가 필요한
        경우를 놓치는 쪽이, 불필요하게 경계하는 쪽보다 비싸기 때문이다."""
        kinds = [w.kind for w in self.fired]
        for preferred in (TriggerKind.US_TIGHTENING, TriggerKind.NON_US_SHOCK,
                          TriggerKind.FUEL_EXHAUSTION):
            if preferred in kinds:
                return preferred
        return TriggerKind.UNKNOWN


# ─────────────────────────────────────────────────────────────
# 감지기 1 — 모멘텀 반전
# ─────────────────────────────────────────────────────────────
def detect_momentum_reversal(as_of: date, risk_events: dict | None = None) -> Warning_:
    """FRS 점수의 3개월 추세가 방향을 바꿨는가.

    국면이 끝날 때는 환율이 먼저 움직이는 게 아니라 **압력이 먼저 돌아선다**.
    지금 점수가 여전히 (+)여도 3개월째 내리막이면 그게 신호다."""
    scores = []
    for back in (3, 2, 1, 0):
        d = _as_of_months_back(as_of, back)
        detail = calculate_frs(d, risk_events)
        scores.append(detail.score)
    if any(s is None for s in scores):
        return Warning_("momentum_reversal", "모멘텀 반전", False, TriggerKind.UNKNOWN,
                        "미판정(3개월 이력 부족)")
    early_slope = scores[1] - scores[0]
    late_slope = scores[3] - scores[2]
    # 부호가 뒤집혔고, 최근 기울기가 의미 있는 크기여야 한다 —
    # 미세한 흔들림까지 잡으면 매달 경보가 켜진다.
    fired = early_slope > 0 > late_slope and abs(late_slope) >= 3.0
    return Warning_("momentum_reversal", "모멘텀 반전", fired, TriggerKind.UNKNOWN,
                    f"FRS {scores[0]:+.0f}→{scores[1]:+.0f}→{scores[2]:+.0f}→{scores[3]:+.0f} "
                    f"(최근 기울기 {late_slope:+.1f})")


# ─────────────────────────────────────────────────────────────
# 감지기 2 — 종료 트리거 매칭 (4개 하위 패턴)
# ─────────────────────────────────────────────────────────────
def detect_exit_triggers(as_of: date, risk_events: dict | None = None) -> list[Warning_]:
    """과거 국면을 실제로 끝낸 4가지 패턴을 각각 본다."""
    return [
        _trigger_rate_reversal(as_of),
        _trigger_long_rate_spike(as_of),
        _trigger_fuel_exhaustion(as_of),
        _trigger_geopolitical_spike(as_of, risk_events),
    ]


def _trigger_rate_reversal(as_of: date) -> Warning_:
    """ⓐ 2018형 — 한미 금리차가 좁혀지다가 **다시 벌어지기 시작**했는가.

    ④2017 국면은 연준이 한국을 추월한 2018-03 바로 그 달부터 꺾였다.
    지금 국면 ⑥의 엔진이 '금리차 축소'이므로, 그 축소가 멈추고 되돌면
    같은 일이 반복된다."""
    def spread(d: date):
        kr = S.value_as_of("kr_base_rate", d, MAX_AGE_DAYS["kr_base_rate"])
        us = S.value_as_of("us_fed_funds", d, MAX_AGE_DAYS["us_fed_funds"])
        return None if kr is None or us is None else kr - us

    now = spread(as_of)
    m3 = spread(_as_of_months_back(as_of, 3))
    m6 = spread(_as_of_months_back(as_of, 6))
    if None in (now, m3, m6):
        return Warning_("rate_reversal", "금리차 재확대(2018형)", False,
                        TriggerKind.US_TIGHTENING, "미판정(금리 이력 부족)")
    prev_change, recent_change = m3 - m6, now - m3
    # 직전 3개월엔 한국에 유리하게 움직였는데 최근 3개월엔 반대로 —
    # 0.10%p를 잡음 문턱으로 둔다(기준금리는 0.25%p 단위로 움직인다).
    fired = prev_change > 0 and recent_change < -0.10
    return Warning_("rate_reversal", "금리차 재확대(2018형)", fired,
                    TriggerKind.US_TIGHTENING,
                    f"금리차 {m6:+.2f}→{m3:+.2f}→{now:+.2f}%p "
                    f"(직전 {prev_change:+.2f}, 최근 {recent_change:+.2f})")


def _trigger_long_rate_spike(as_of: date) -> Warning_:
    """ⓑ 2021형 — 미 10년물이 3개월간 +50bp 이상 급등했는가.

    ⑤2020 국면은 금리차가 그대로인데 10년물이 0.93→1.74%로 뛰면서 끝났다.
    **레벨이 아니라 속도**가 끝냈다는 게 이 패턴의 핵심이다."""
    now = S.value_as_of("us_10y", as_of, MAX_AGE_DAYS["us_10y"])
    before = S.value_n_months_before("us_10y", as_of, 3, MAX_AGE_DAYS["us_10y"])
    if now is None or before is None:
        return Warning_("long_rate_spike", "미 장기금리 급등(2021형)", False,
                        TriggerKind.US_TIGHTENING, "미판정(10년물 이력 부족)")
    chg = now - before
    return Warning_("long_rate_spike", "미 장기금리 급등(2021형)", chg >= 0.50,
                    TriggerKind.US_TIGHTENING,
                    f"10년물 {before:.2f}→{now:.2f}% (3개월 {chg:+.2f}%p, 임계 +0.50)")


def _trigger_fuel_exhaustion(as_of: date) -> Warning_:
    """ⓒ 연료 소진 — 경상흑자·수출 증가세가 꺾였는가.

    모든 국면의 지속 연료가 '한국으로 실제 달러가 들어오는 것'이었다.
    유입이 줄면 국면을 떠받칠 힘이 빠진다. 금리 방향과는 무관하므로
    장기채 함의도 중립이다(FUEL_EXHAUSTION)."""
    from engine.fx.regime_score import score_current_account, score_exports

    now_ca = score_current_account(as_of)
    now_ex = score_exports(as_of)
    prev = _as_of_months_back(as_of, 6)
    prev_ca = score_current_account(prev)
    prev_ex = score_exports(prev)
    pairs = [(now_ca, prev_ca), (now_ex, prev_ex)]
    usable = [(a, b) for a, b in pairs if a.available and b.available]
    if not usable:
        return Warning_("fuel_exhaustion", "연료 소진(경상·수출 둔화)", False,
                        TriggerKind.FUEL_EXHAUSTION, "미판정(경상·수출 이력 부족)")
    drops = [a.normalized - b.normalized for a, b in usable]
    # 두 축이 모두 있으면 둘 다, 하나뿐이면 그 하나가 크게 꺾여야 한다 —
    # 한 축만 보고 경보를 켜면 분기 발표 잡음에 끌려다닌다.
    threshold = -0.30 if len(usable) == 2 else -0.50
    fired = all(d <= threshold for d in drops)
    parts = [f"{a.label} {b.normalized:+.2f}→{a.normalized:+.2f}" for a, b in usable]
    return Warning_("fuel_exhaustion", "연료 소진(경상·수출 둔화)", fired,
                    TriggerKind.FUEL_EXHAUSTION,
                    f"6개월 전 대비 {', '.join(parts)} (임계 {threshold:+.2f})")


def _trigger_geopolitical_spike(as_of: date, risk_events: dict | None) -> Warning_:
    """ⓓ 2011·2026형 — 지정학 위험이 급등했는가.

    ①2010 국면을 끝낸 건 미국 신용등급 강등 + 유럽 재정위기였다.
    안전자산 선호는 미국 긴축과 정반대로 **금리를 끌어내리는** 충격이므로
    NON_US_SHOCK으로 분류한다 — ④2018-10과 같은 계열이다."""
    from engine.fx.regime_score import _events_are_from_the_future

    if not risk_events or not risk_events.get("signals"):
        return Warning_("geopolitical_spike", "지정학 급등(2011형)", False,
                        TriggerKind.NON_US_SHOCK, "미판정(fx_risk_events.yaml 없음)")
    if _events_are_from_the_future(risk_events, as_of):
        return Warning_("geopolitical_spike", "지정학 급등(2011형)", False,
                        TriggerKind.NON_US_SHOCK,
                        f"미판정(판단 시점 {risk_events.get('as_of')}이 as_of 이후)")
    sig = risk_events["signals"]
    keys = ("geopolitical_risk", "pandemic_risk", "trade_policy_risk", "financial_stress")
    vals = [float(sig[k]) for k in keys if isinstance(sig.get(k), (int, float))]
    if not vals:
        return Warning_("geopolitical_spike", "지정학 급등(2011형)", False,
                        TriggerKind.NON_US_SHOCK, "미판정(인식 가능한 신호 없음)")
    peak = max(vals)
    return Warning_("geopolitical_spike", "지정학 급등(2011형)", peak >= 0.7,
                    TriggerKind.NON_US_SHOCK,
                    f"최고 위험 {peak:.2f}/1.00 (임계 0.70)")


# ─────────────────────────────────────────────────────────────
# 감지기 3 — 이격 극단
# ─────────────────────────────────────────────────────────────
def detect_gap_extreme(as_of: date) -> Warning_:
    """MA36 대비 ±8% 이상 벌어졌는가 — 평균회귀 압력.

    과거 최대 이격이 2011-07의 −11.9%였고 그 직후 국면이 끝났다."""
    g = ma36_gap(as_of)
    if g is None:
        return Warning_("gap_extreme", "이격 극단", False, TriggerKind.UNKNOWN,
                        "미판정(36개월 이력 부족)")
    _, _, gap = g
    return Warning_("gap_extreme", "이격 극단", abs(gap) >= GAP_EXTREME_PCT,
                    TriggerKind.UNKNOWN,
                    f"MA36 이격 {gap:+.1f}% (임계 ±{GAP_EXTREME_PCT:.0f}%)")


# ─────────────────────────────────────────────────────────────
# 감지기 4 — 경과 개월
# ─────────────────────────────────────────────────────────────
def current_episode_months(as_of: date) -> int | None:
    """지금 하회 국면이 몇 개월째인가. 하회 중이 아니면 None."""
    monthly = S.monthly_last("kr_usdkrw", as_of) or S.monthly_last("kr_usdkrw_fred", as_of)
    if len(monthly) < 36:
        return None
    count = 0
    for i in range(len(monthly) - 1, 34, -1):
        window = [v for _, v in monthly[i - 35:i + 1]]
        ma = sum(window) / 36
        if monthly[i][1] < ma:
            count += 1
        else:
            break
    return count or None


def detect_duration(as_of: date) -> Warning_:
    """과거 중앙값 11개월을 넘겼는가 — 오래된 국면일수록 끝날 때가 가깝다."""
    months = current_episode_months(as_of)
    if months is None:
        return Warning_("duration", "경과 개월", False, TriggerKind.UNKNOWN,
                        "하회 국면 아님(또는 이력 부족)")
    return Warning_("duration", "경과 개월", months >= HISTORICAL_MEDIAN_MONTHS,
                    TriggerKind.UNKNOWN,
                    f"{months}개월째 (과거 중앙값 {HISTORICAL_MEDIAN_MONTHS}개월)")


# ─────────────────────────────────────────────────────────────
def evaluate(as_of: date, risk_events: dict | None = None) -> TransitionReport:
    """감지기 전체를 돌려 경고 리포트를 만든다.

    ⚠ 종료 트리거 4개는 **하나의 감지기**로 묶어 센다(설계 §3의 "감지기 4종").
    각각을 따로 세면 4개짜리 카테고리 하나가 3단계 문턱을 혼자 넘겨버린다."""
    exit_triggers = detect_exit_triggers(as_of, risk_events)
    fired_exits = [w for w in exit_triggers if w.fired]
    combined_exit = Warning_(
        "exit_trigger", "종료 트리거 매칭",
        bool(fired_exits),
        fired_exits[0].kind if fired_exits else TriggerKind.UNKNOWN,
        "; ".join(w.label for w in fired_exits) if fired_exits
        else "해당 없음 (" + ", ".join(
            w.label.split("(")[0].strip() for w in exit_triggers) + " 전부 미발화)",
    )
    warnings = [
        detect_momentum_reversal(as_of, risk_events),
        combined_exit,
        detect_gap_extreme(as_of),
        detect_duration(as_of),
    ]
    return TransitionReport(as_of=as_of, warnings=warnings)


def evaluate_verbose(as_of: date, risk_events: dict | None = None
                     ) -> tuple[TransitionReport, list[Warning_]]:
    """리포트 + 종료 트리거 4개의 개별 판정(리포트 렌더·디버깅용)."""
    return evaluate(as_of, risk_events), detect_exit_triggers(as_of, risk_events)


def _as_of_months_back(as_of: date, months: int) -> date:
    if months == 0:
        return as_of
    y, m = as_of.year, as_of.month - months
    while m <= 0:
        m += 12
        y -= 1
    return date(y, m, min(as_of.day, 28))
