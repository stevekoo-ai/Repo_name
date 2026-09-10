"""국채 금리(yield)에서 총수익(total return)을 합성한다.

왜 필요한가 — 사용자가 "환율 국면에서 채권은 어떻게 움직였나"를 물었을 때,
**금리 변화만으로는 답이 안 된다**. 금리가 오르면 보유 채권은 평가손이 나므로
"10년물 금리가 0.9%→1.7%로 올랐다"는 사실 자체가 투자 성과를 말해주지 않는다.

원래는 ICE BofA 총수익지수(BAMLCC0A0CMTRIV 등)를 쓰려 했으나, 2026-09-10
실측 결과 FRED가 라이선스 때문에 **최근 3년치만** 공개한다는 걸 확인했다
(scripts/macro_data.py PRESETS 주석 참조). 2010~2021 국면을 덮으려면 합성이
유일한 길이다.

방법 — 상수만기(constant maturity) 파(par)채권 롤링:
  1. t 시점: 만기 M년, 표면금리 = 그 시점 금리 y_t 인 파채권을 100에 산다.
  2. t+1개월: 만기가 M-1/12로 줄어든 그 채권을 새 금리 y_{t+1}로 재평가한다.
  3. 총수익 = (재평가가격 + 1개월치 경과이자) / 100 - 1
  4. 다음 달엔 다시 만기 M년짜리로 갈아탄다(상수만기 유지).

듀레이션 근사(-D×Δy)를 쓰지 않고 **현금흐름을 직접 할인**한다 — 금리가 크게
움직인 달(2020-03, 2022)에 근사식은 오차가 커지는데, 이 분석의 관심 구간이
바로 그런 달들이기 때문이다. 평평한 수익률곡선을 가정하는 한계는 남는다
(실제 곡선 기울기·롤다운 수익 미반영) — 그래서 결과는 "근사"로 표기한다.
"""
from __future__ import annotations


def par_bond_price(coupon_rate: float, ytm: float, maturity_years: float) -> float:
    """표면금리 coupon_rate, 만기수익률 ytm(둘 다 연 %), 잔존 maturity_years인
    채권의 액면 100 기준 **더티 가격**(경과이자 포함 = 남은 현금흐름의 현재가치).

    반기 쿠폰. 잔존기간 H(반기 단위) 안에서 쿠폰은 만기시점부터 거꾸로
    H, H-1, ..., 로 붙는다 — 만기가 반기의 배수가 아니면 첫 쿠폰까지의
    잔여기간(stub)이 1보다 작아지는데, 이 표현이 그 경우를 자동으로 처리한다.
    """
    if maturity_years <= 0:
        return 100.0
    if maturity_years < 0.5:
        # 반기 쿠폰 가정이 깨진다 — 잔존 6개월 미만이면 쿠폰이 1회뿐인데도
        # 반기치 전액을 얹게 돼 수익률이 부풀려진다(3개월물에 쓰면 월 1.3%가
        # 나온다). 단기물은 cash_total_return을 쓸 것.
        raise ValueError(
            f"잔존 {maturity_years:.3f}년: 6개월 미만엔 이 모델을 쓰지 말 것 "
            "— 단기물은 cash_total_return() 사용"
        )
    c = coupon_rate / 2.0            # 반기 쿠폰 금액(액면 100 기준)
    y = ytm / 200.0                  # 반기 할인율
    h = maturity_years * 2.0         # 잔존기간(반기 단위)
    n = int(-(-h // 1))              # 남은 쿠폰 횟수 = ceil(h)
    price = 100.0 / (1 + y) ** h     # 원금
    for k in range(n):
        price += c / (1 + y) ** (h - k)
    return price


def monthly_total_return(y_start: float, y_end: float, maturity_years: float) -> float:
    """상수만기 파채권을 한 달 보유했을 때의 총수익률(소수, 0.01 = +1%).

    y_start 시점에 표면금리 = y_start 인 파채권을 100(더티)에 사고, 한 달 뒤
    잔존 maturity_years - 1/12 을 새 금리 y_end로 재평가한다. 위 가격이
    더티(경과이자 포함)라 **경과이자를 따로 더하지 않는다** — 더하면 이중계상.
    """
    if y_start is None or y_end is None:
        return None
    price = par_bond_price(y_start, y_end, maturity_years - 1 / 12)
    return price / 100.0 - 1.0


def cumulative_total_return(monthly_yields: list[float], maturity_years: float) -> float:
    """월말 금리 시계열을 받아 구간 누적 총수익률(소수)을 돌려준다."""
    total = 1.0
    for a, b in zip(monthly_yields, monthly_yields[1:]):
        r = monthly_total_return(a, b, maturity_years)
        if r is None:
            return None
        total *= 1 + r
    return total - 1.0


def cash_total_return(monthly_yields: list[float]) -> float:
    """단기금리를 그대로 굴린 달러 현금(MMF·단기국채) 누적 수익률.

    가격변동이 없다고 보고 월할 이자만 복리로 쌓는다 — 3개월물은
    듀레이션이 0.25년이라 이 근사의 오차가 무시할 수준이다."""
    total = 1.0
    for y in monthly_yields[1:]:
        total *= 1 + y / 12 / 100
    return total - 1.0
