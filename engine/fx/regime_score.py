"""FRS (FX Regime Score) — 원/달러 국면 점수 엔진.

설계: wiki/architecture/fx-regime-score-design.md
실증 근거: wiki/concepts/usdkrw-below-ma36-episodes.md (5개 국면)
자산 연동 한계: wiki/concepts/fx-episode-dollar-assets.md (§6.5 — 자산배분 점수를
                만들지 않는 이유)

## 규칙 세 가지

1. **모든 함수는 `as_of`를 받는다.** 데이터 접근은 전부 `series.py`를 통과하고,
   그 계층이 as_of 이후 데이터를 물리적으로 차단한다. 오늘 리포트와 과거
   백테스트가 **같은 코드**를 쓰므로 백테스트가 별도 작업이 아니다.
2. **점수는 −100 ~ +100 양방향. (+) = 원화 강세 압력.**
3. **미수집은 0점이 아니다(R3).** 값이 없는 요인은 `available=False`로 표기하고
   **가중치를 총점에서 빼고 재정규화**한다. 중립(0)으로 채우면 "모르는 것"이
   "중립이라는 판단"으로 둔갑한다.
"""
from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from datetime import date

from engine.fx import series as S

# 가중치 — 설계 §2. 5개 국면에서 역산했다.
WEIGHTS: dict[str, int] = {
    "rate_differential": 25,   # 한미 정책금리차
    "us_10y": 15,              # 미 10년물 레벨·모멘텀
    "dollar_index": 15,        # 달러인덱스 방향
    "current_account": 15,     # 경상수지 추세
    "exports": 10,             # 수출·반도체
    "geopolitical": 10,        # 지정학(LLM 주입)
    "oil": 5,                  # 유가
    "ma36_gap": 5,             # MA36 이격도
}

# 월 단위 시리즈는 발표 지연이 있다. 이 나이를 넘으면 "미수집"으로 떨어뜨린다
# (R3). CCI가 62일 지난 값을 조용히 "최신"으로 쓰다 사고 났던 걸 피한다.
MAX_AGE_DAYS = {
    "kr_base_rate": 120, "us_fed_funds": 120, "kr_current_account": 150,
    "kr_exports": 120, "us_10y": 30, "us_dollar_index": 30,
    "kr_usdkrw": 30, "kr_usdkrw_fred": 30, "us_brent": 30,
}


@dataclass(frozen=True)
class FactorScore:
    """한 요인의 판정. normalized는 [-1, +1], (+)가 원화 강세 압력."""
    key: str
    label: str
    normalized: float | None      # None = 미수집
    weight: int
    detail: str                   # 사람이 읽는 근거 한 줄

    @property
    def available(self) -> bool:
        return self.normalized is not None

    @property
    def contribution(self) -> float:
        return 0.0 if self.normalized is None else self.normalized * self.weight


@dataclass(frozen=True)
class FRSDetail:
    as_of: date
    score: float | None           # -100 ~ +100, 전부 미수집이면 None
    factors: list[FactorScore] = field(default_factory=list)
    covered_weight: int = 0       # 실제로 채점된 가중치 합

    @property
    def coverage(self) -> float:
        return self.covered_weight / sum(WEIGHTS.values())

    def factor(self, key: str) -> FactorScore | None:
        return next((f for f in self.factors if f.key == key), None)


def _clamp(x: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _completed_months(rows: list, as_of: date) -> list:
    """**아직 진행 중인 달을 잘라낸다.**

    2026-09-10 실측으로 잡은 함정 — `customs_export_dlr`의 2026-09 행이
    201억달러였는데 이건 9월 10일까지 누적된 부분치다. 작년 9월 전체
    (659억달러)와 나누면 YoY −69.5%라는 가짜 폭락이 나온다. 월간 누적으로
    발표되는 시리즈는 전부 같은 함정을 갖는다.

    as_of가 속한 달은 정의상 아직 안 끝났으므로 통째로 버린다. 과거 시점을
    넣는 백테스트에서도 같은 규칙이 적용돼야 look-ahead 없이 일관된다."""
    return [o for o in rows if (o.date.year, o.date.month) != (as_of.year, as_of.month)]


def _percentile_rank(value: float, population: list[float]) -> float:
    """population 안에서 value의 백분위(0~1). 단위를 모르는 시리즈를
    자기 이력에 상대적으로 정규화할 때 쓴다 — 경상수지처럼 절대 규모의
    기준점을 코드가 알 수 없는 경우."""
    if not population:
        return 0.5
    below = sum(1 for x in population if x < value)
    equal = sum(1 for x in population if x == value)
    return (below + equal / 2) / len(population)


def _blend(level: float | None, momentum: float | None,
           level_weight: float = 0.4) -> float | None:
    """레벨과 방향을 섞는다. 설계 §2 — 방향 비중을 더 크게 잡는 게 기본이다.

    2018은 '역전'이라는 방향 전환이, 2026은 '축소'라는 방향이 트리거였지
    절대 수준이 아니었다."""
    if level is None and momentum is None:
        return None
    if momentum is None:
        return _clamp(level)
    if level is None:
        return _clamp(momentum)
    return _clamp(level * level_weight + momentum * (1 - level_weight))


# ─────────────────────────────────────────────────────────────
# 요인 1 — 한미 정책금리차 (가중 25, 최대)
# ─────────────────────────────────────────────────────────────
def score_rate_differential(as_of: date) -> FactorScore:
    """한국 기준금리 − 미 연방기금금리. (+)면 원화에 유리.

    5개 국면 중 시작 2회·종료 1회를 단독으로 설명한 유일한 요인이다.
    ④2018은 금리차가 역전된 **바로 그 달**부터 국면이 꺾였고,
    ⑥2026은 한은 연속 인상으로 차이가 좁혀진 게 시작 엔진이었다."""
    kr = S.value_as_of("kr_base_rate", as_of, MAX_AGE_DAYS["kr_base_rate"])
    us = S.value_as_of("us_fed_funds", as_of, MAX_AGE_DAYS["us_fed_funds"])
    if kr is None or us is None:
        return FactorScore("rate_differential", "한미 정책금리차", None,
                           WEIGHTS["rate_differential"], "미수집(기준금리 또는 FF금리 없음)")
    spread = kr - us
    kr3 = S.value_n_months_before("kr_base_rate", as_of, 3, MAX_AGE_DAYS["kr_base_rate"])
    us3 = S.value_n_months_before("us_fed_funds", as_of, 3, MAX_AGE_DAYS["us_fed_funds"])

    # 레벨: ±1.5%p를 만점으로 본다(2018 역전폭 -0.69, 2026 +1.13 을 담는 범위)
    level = _clamp(spread / 1.5)
    momentum = None
    if kr3 is not None and us3 is not None:
        # 방향: 3개월간 금리차 변화. ±0.5%p를 만점으로 — 분기당 0.5%p면
        # 연속 인상/인하가 진행 중이라는 뜻이라 충분히 강한 신호다.
        momentum = _clamp((spread - (kr3 - us3)) / 0.5)
    value = _blend(level, momentum, level_weight=0.4)
    dir_txt = "정보없음" if momentum is None else f"3개월 {spread - (kr3 - us3):+.2f}%p"
    return FactorScore("rate_differential", "한미 정책금리차", value,
                       WEIGHTS["rate_differential"],
                       f"한국 {kr:.2f}% − 미국 {us:.2f}% = {spread:+.2f}%p ({dir_txt})")


# ─────────────────────────────────────────────────────────────
# 요인 2 — 미 10년물 (가중 15)
# ─────────────────────────────────────────────────────────────
def score_us_10y(as_of: date) -> FactorScore:
    """미 장기금리가 오르면 달러로 자금이 빨려 원화가 약해진다 → 부호 반전.

    ⑤2021 국면을 끝낸 게 정확히 이것 — 금리차는 그대로였는데 10년물이
    0.93%→1.74%로 급등하면서 달러가 되돌았다. 그래서 레벨보다 방향이 중요하다."""
    now = S.value_as_of("us_10y", as_of, MAX_AGE_DAYS["us_10y"])
    if now is None:
        return FactorScore("us_10y", "미 10년물", None, WEIGHTS["us_10y"], "미수집")
    before = S.value_n_months_before("us_10y", as_of, 3, MAX_AGE_DAYS["us_10y"])
    # 레벨: 3% 근방을 중립으로 두고 ±2%p를 만점. 금리가 높을수록 원화에 불리.
    level = _clamp(-(now - 3.0) / 2.0)
    momentum = None
    if before is not None:
        # 방향: 3개월 ±50bp를 만점(설계 §3의 2021형 트리거 임계와 같은 눈금).
        momentum = _clamp(-(now - before) / 0.5)
    value = _blend(level, momentum, level_weight=0.3)
    dir_txt = "정보없음" if before is None else f"3개월 {now - before:+.2f}%p"
    return FactorScore("us_10y", "미 10년물", value, WEIGHTS["us_10y"],
                       f"{now:.2f}% ({dir_txt})")


# ─────────────────────────────────────────────────────────────
# 요인 3 — 달러인덱스 (가중 15)
# ─────────────────────────────────────────────────────────────
def score_dollar_index(as_of: date) -> FactorScore:
    """달러가 전방위로 약해지면 원화도 같이 강해진다 → 부호 반전.

    ④2017 국면의 시작 배경이 달러인덱스 연 −10%였다. 레벨은 지수 기준점이
    시대마다 달라 비교가 어려우므로 **방향만** 본다."""
    now = S.value_as_of("us_dollar_index", as_of, MAX_AGE_DAYS["us_dollar_index"])
    before = S.value_n_months_before("us_dollar_index", as_of, 6,
                                     MAX_AGE_DAYS["us_dollar_index"])
    if now is None or before is None or before == 0:
        return FactorScore("dollar_index", "달러인덱스", None, WEIGHTS["dollar_index"],
                           "미수집(6개월 전 값 필요)")
    chg = (now / before - 1) * 100
    # 6개월 ±5%를 만점 — 2017년의 연 -10%가 반년 -5% 페이스였다.
    return FactorScore("dollar_index", "달러인덱스", _clamp(-chg / 5.0),
                       WEIGHTS["dollar_index"], f"{now:.1f} (6개월 {chg:+.1f}%)")


# ─────────────────────────────────────────────────────────────
# 요인 4 — 경상수지 (가중 15)
# ─────────────────────────────────────────────────────────────
def score_current_account(as_of: date) -> FactorScore:
    """한국으로 실제 달러가 들어오는가 — 모든 국면의 '연료'.

    ②③의 '차별화'(테이퍼 탠트럼 때 취약5개국과 분리된 것)를 만든 근거이기도 하다.

    ⚠ 절대 규모를 코드가 해석할 수 없다 — 이 시리즈의 단위가 무엇인지
    저장소 어디에도 명시돼 있지 않고, 시대에 따라 경제 규모 자체가 달라
    "얼마면 큰 흑자인가"의 기준점이 없다. 그래서 **자기 이력 안에서의
    백분위**(레벨)와 **직전 12개월 대비 증감**(방향)만 쓴다. 단위가 바뀌어도
    부호와 순위는 살아남는 설계다."""
    rows = _completed_months(S.series_as_of("kr_current_account", as_of), as_of)
    if len(rows) < 24:
        return FactorScore("current_account", "경상수지", None, WEIGHTS["current_account"],
                           f"미수집(24개월 필요, {len(rows)}개월 보유)")
    if (as_of - rows[-1].date).days > MAX_AGE_DAYS["kr_current_account"]:
        return FactorScore("current_account", "경상수지", None, WEIGHTS["current_account"],
                           f"발표 지연({rows[-1].date} 이후 없음)")

    values = [o.value for o in rows]
    windows = [sum(values[i:i + 12]) for i in range(len(values) - 11)]
    recent, prior = windows[-1], windows[-13] if len(windows) >= 13 else windows[0]

    # 레벨: 12개월 합이 자기 이력 안에서 어느 위치인가(0~1 → -1~+1)
    level = _clamp(_percentile_rank(recent, windows) * 2 - 1)
    # 방향: 직전 12개월 대비 ±30% 변화를 만점
    momentum = None
    if prior and prior != 0:
        momentum = _clamp((recent - prior) / abs(prior) / 0.3)
    value = _blend(level, momentum, level_weight=0.5)
    chg_txt = "정보없음" if momentum is None else f"{(recent - prior) / abs(prior) * 100:+.0f}%"
    return FactorScore("current_account", "경상수지", value, WEIGHTS["current_account"],
                       f"12개월 합 {recent:,.0f} (이력 백분위 {_percentile_rank(recent, windows)*100:.0f}%, 직전 12개월 대비 {chg_txt})")


# ─────────────────────────────────────────────────────────────
# 요인 5 — 수출·반도체 (가중 10)
# ─────────────────────────────────────────────────────────────
def score_exports(as_of: date) -> FactorScore:
    """수출이 늘면 네고 물량(달러 매도)이 늘어 원화가 강해진다.

    ④2017 반도체 슈퍼사이클과 ⑥2026 네고물량이 이 요인이다.
    반도체 전용 시리즈가 있으면 가중해 섞고, 없으면 총수출만 쓴다(R3)."""
    rows = _completed_months(S.series_as_of("kr_exports", as_of), as_of)
    if len(rows) < 13:
        return FactorScore("exports", "수출", None, WEIGHTS["exports"],
                           f"미수집(13개월 필요, {len(rows)}개월)")
    if (as_of - rows[-1].date).days > MAX_AGE_DAYS["kr_exports"]:
        return FactorScore("exports", "수출", None, WEIGHTS["exports"],
                           f"발표 지연({rows[-1].date} 이후 없음)")
    now, year_ago = rows[-1].value, rows[-13].value
    if year_ago == 0:
        return FactorScore("exports", "수출", None, WEIGHTS["exports"], "직전년 값 0")
    yoy = (now / year_ago - 1) * 100
    # 총수출 YoY ±20%를 만점 — 2017 슈퍼사이클이 +15~20% 대역이었다.
    value = _clamp(yoy / 20.0)
    detail = f"총수출 YoY {yoy:+.1f}%"
    semi = S.value_as_of("kr_semi_exports_yoy", as_of, 120)
    if semi is not None:
        # 반도체는 원화에 미치는 영향이 총수출보다 크지만 시리즈가 짧다
        # (2026-04~). 있으면 6:4로 섞고 없으면 총수출만 — 없다고 0으로
        # 끌어내리지 않는다.
        value = _clamp(value * 0.6 + _clamp(semi / 40.0) * 0.4)
        detail += f", 반도체 YoY {semi:+.1f}%"
    return FactorScore("exports", "수출", value, WEIGHTS["exports"], detail)


# ─────────────────────────────────────────────────────────────
# 요인 6 — 지정학 (가중 10, LLM 주입)
# ─────────────────────────────────────────────────────────────
def score_geopolitical(as_of: date, risk_events: dict | None = None) -> FactorScore:
    """전쟁·팬데믹·관세 같은 뉴스 의존 위험 — 코드가 계산할 수 없어 LLM이 채운다.

    ①2011 유럽 재정위기가 국면을 끝냈고, ⑥2026은 중동 충돌이 배경이다.
    데이터는 `data/manual_inputs/fx_risk_events.yaml`(semiconductor.yaml과 동일
    스키마). 위험이 높을수록 안전자산 선호 → 달러 강세 → **원화 약세**라
    부호를 뒤집는다."""
    if not risk_events or not risk_events.get("signals"):
        return FactorScore("geopolitical", "지정학·위기", None, WEIGHTS["geopolitical"],
                           "미수집(fx_risk_events.yaml 없음 또는 비어있음)")
    sig = risk_events["signals"]
    keys = ("geopolitical_risk", "pandemic_risk", "trade_policy_risk", "financial_stress")
    present = [(k, float(sig[k])) for k in keys if isinstance(sig.get(k), (int, float))]
    vals = [v for _, v in present]
    if not vals:
        return FactorScore("geopolitical", "지정학·위기", None, WEIGHTS["geopolitical"],
                           "미수집(인식 가능한 신호 없음)")
    risk = statistics.mean(vals)  # 0~1
    stale = ""
    ev_as_of = risk_events.get("as_of")
    if ev_as_of:
        try:
            age = (as_of - date.fromisoformat(str(ev_as_of))).days
            if age > 0:
                stale = f", {age}일 전 판단"   # R2: 신선도를 숨기지 않는다
        except ValueError:
            pass
    return FactorScore("geopolitical", "지정학·위기", _clamp(-risk * 2 + 1),
                       WEIGHTS["geopolitical"],
                       f"위험 {risk:.2f}/1.00 "
                       f"({', '.join(f'{k}={v:.2f}' for k, v in present)}{stale})")


# ─────────────────────────────────────────────────────────────
# 요인 7 — 유가 (가중 5)
# ─────────────────────────────────────────────────────────────
def score_oil(as_of: date) -> FactorScore:
    """한국은 원유 순수입국이라 유가가 오르면 교역조건이 나빠져 원화가 약해진다.

    ③2014 국면 종료의 세 요인 중 하나가 유가 붕괴(110→50달러)였는데,
    그건 원화에 **유리한** 방향이었다 — 그런데도 국면이 끝난 건 QE 종료와
    엔저가 더 컸기 때문. 가중치를 5로 낮게 잡은 이유다."""
    now = S.value_as_of("us_brent", as_of, MAX_AGE_DAYS["us_brent"])
    before = S.value_n_months_before("us_brent", as_of, 6, MAX_AGE_DAYS["us_brent"])
    if now is None or before is None or before == 0:
        return FactorScore("oil", "유가(브렌트)", None, WEIGHTS["oil"], "미수집")
    chg = (now / before - 1) * 100
    # 6개월 ±30%를 만점. 유가는 변동이 커서 다른 요인보다 눈금이 넓다.
    return FactorScore("oil", "유가(브렌트)", _clamp(-chg / 30.0), WEIGHTS["oil"],
                       f"${now:.1f} (6개월 {chg:+.1f}%)")


# ─────────────────────────────────────────────────────────────
# 요인 8 — MA36 이격도 (가중 5)
# ─────────────────────────────────────────────────────────────
def ma36_gap(as_of: date) -> tuple[float, float, float] | None:
    """(현재 환율, MA36, 이격 %) — 국면 라벨의 근거이자 요인 8의 입력.

    36개월 단순이동평균은 usdkrw-below-ma36-episodes.md의 국면 정의 그대로다.
    ECOS 고시가 있으면 그걸 쓰고(R1 실측 우선), 없으면 FRED로 떨어진다."""
    monthly = S.monthly_last("kr_usdkrw", as_of) or S.monthly_last("kr_usdkrw_fred", as_of)
    if len(monthly) < 36:
        return None
    values = [v for _, v in monthly[-36:]]
    ma = statistics.fmean(values)
    now = monthly[-1][1]
    return now, ma, (now / ma - 1) * 100


def score_ma36_gap(as_of: date) -> FactorScore:
    """이격이 크게 벌어질수록 평균회귀 압력 → **부호를 뒤집는다**.

    주의 — 이 요인은 "지금 원화가 강하다"를 말하는 게 아니라 "너무 강해서
    되돌릴 여지가 있다"를 말한다. 국면 라벨(출력 A)은 이격의 **부호**를
    쓰고, 이 점수는 이격의 **크기**를 쓴다. 둘을 헷갈리면 안 된다."""
    g = ma36_gap(as_of)
    if g is None:
        return FactorScore("ma36_gap", "MA36 이격", None, WEIGHTS["ma36_gap"],
                           "미수집(36개월 이력 필요)")
    now, ma, gap = g
    # 과거 국면의 최대 이격이 -11.9%였다. ±10%를 만점으로 잡는다.
    return FactorScore("ma36_gap", "MA36 이격", _clamp(gap / 10.0), WEIGHTS["ma36_gap"],
                       f"{now:,.1f}원 vs MA36 {ma:,.1f}원 ({gap:+.1f}%)")


# ─────────────────────────────────────────────────────────────
# 총점
# ─────────────────────────────────────────────────────────────
def calculate_frs(as_of: date, risk_events: dict | None = None) -> FRSDetail:
    """as_of 시점의 FRS 총점(−100~+100). (+) = 원화 강세 압력.

    미수집 요인의 가중치는 총점에서 빼고 **남은 가중치로 재정규화**한다 —
    0점으로 채우면 "모르는 것"이 "중립"으로 둔갑하기 때문(R3)."""
    factors = [
        score_rate_differential(as_of),
        score_us_10y(as_of),
        score_dollar_index(as_of),
        score_current_account(as_of),
        score_exports(as_of),
        score_geopolitical(as_of, risk_events),
        score_oil(as_of),
        score_ma36_gap(as_of),
    ]
    covered = sum(f.weight for f in factors if f.available)
    if covered == 0:
        return FRSDetail(as_of=as_of, score=None, factors=factors, covered_weight=0)
    raw = sum(f.contribution for f in factors)
    return FRSDetail(as_of=as_of, score=raw / covered * 100,
                     factors=factors, covered_weight=covered)


REGIME_LABELS = (
    "원화 강세 국면", "강세 진입 시도", "중립", "약세 진입 시도", "원화 약세 국면",
)


def regime_label(as_of: date, detail: FRSDetail | None = None) -> str:
    """출력 A — MA36 이격 **부호** × FRS **부호** 조합(설계 §3).

    이격이 하회(−)면서 점수도 강세(+)면 '국면', 둘이 엇갈리면 '진입 시도'다."""
    detail = detail or calculate_frs(as_of)
    g = ma36_gap(as_of)
    if detail.score is None or g is None:
        return "판정불가(데이터 부족)"
    gap, score = g[2], detail.score
    if abs(score) < 15:
        return "중립"
    below = gap < 0            # MA36 하회 = 원화가 3년 평균보다 강하다
    if below and score > 0:
        return "원화 강세 국면"
    if below and score < 0:
        return "약세 진입 시도"   # 아직 강한데 압력이 반대로 돌았다
    if not below and score > 0:
        return "강세 진입 시도"
    return "원화 약세 국면"
