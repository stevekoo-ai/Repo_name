"""Discussion Points — decision-focused prompts, not directives.

Per the user's explicit request: the report shouldn't just declare actions,
it should surface the handful of things that are genuinely the user's
judgment call, with the concrete numbers behind them, and invite a
response in conversation. Every point here is derived from data already
computed elsewhere in the pipeline (portfolio.yaml, housing engine,
user.yaml) — nothing here is invented or generic advice.
"""
from __future__ import annotations

from datetime import date, datetime

from core.config import portfolio_config, user_profile


def _stock_concentration() -> dict | None:
    stocks = portfolio_config().get("stocks", [])
    if not stocks:
        return None
    values = [(s["name"], s["quantity"] * s["avg_price"]) for s in stocks]
    total = sum(v for _, v in values)
    if total <= 0:
        return None
    top_name, top_value = max(values, key=lambda x: x[1])
    pct = top_value / total * 100
    return {"name": top_name, "pct": round(pct, 1), "total_cost_basis_krw": round(total)}


def _lockup_vs_moveout() -> dict | None:
    stocks = portfolio_config().get("stocks", [])
    housing = user_profile().get("housing", {})
    moveout = housing.get("moveout_deadline")
    if not moveout:
        return None
    for s in stocks:
        for lockup in s.get("lockups", []):
            lock_until = lockup.get("lock_until")
            if not lock_until:
                continue
            d1 = datetime.fromisoformat(lock_until).date()
            d2 = datetime.fromisoformat(moveout).date()
            return {
                "ticker_name": s["name"], "quantity": lockup["quantity"],
                "lock_until": lock_until, "markup_krw": lockup.get("markup_krw"),
                "moveout_deadline": moveout, "days_apart": abs((d2 - d1).days),
                "lock_after_moveout": d1 > d2,
            }
    return None


def _semiconductor_exposure_breadth(asset_impact: dict) -> dict | None:
    stocks = portfolio_config().get("stocks", [])
    etfs = portfolio_config().get("etf", [])
    semi_stock_names = [s["name"] for s in stocks if s.get("sector") == "semiconductor_memory"]
    semi_etf_names = [e["name"] for e in etfs if e.get("bucket") == "semiconductor"]
    if not semi_stock_names and not semi_etf_names:
        return None
    return {
        "semiconductor_stocks": semi_stock_names,
        "semiconductor_etfs": semi_etf_names,
        "total_holdings": len(stocks) + len(etfs),
        "semiconductor_related_count": len(semi_stock_names) + len(semi_etf_names),
    }


def _housing_funding_timeline(housing: dict) -> dict | None:
    housing_profile = user_profile().get("housing", {})
    moveout = housing_profile.get("moveout_deadline")
    for notice in housing.get("notices", []):
        pc = notice.get("platform_city_analysis")
        if pc and pc.get("funding_gap_krw") and pc["funding_gap_krw"] > 0:
            return {
                "notice_name": notice["name"], "funding_gap_krw": pc["funding_gap_krw"],
                "moveout_deadline": moveout, "application_start": notice.get("application_start"),
            }
    return None


def generate_discussion_points(personal: dict) -> list[dict]:
    points: list[dict] = []

    conc = _stock_concentration()
    if conc and conc["pct"] >= 60:
        points.append({
            "topic": "SK하이닉스 집중도",
            "context": (
                f"보유 주식의 매입원가 기준 {conc['pct']}%가 {conc['name']} 한 종목에 쏠려 있습니다 "
                f"(주식 계좌 총 매입원가 약 {conc['total_cost_basis_krw']:,}원 중)."
            ),
            "question": (
                "회사 배경과 업황을 잘 아는 종목이라 확신이 있으실 텐데, 그럼에도 이 정도 집중도를 "
                "계속 유지하실 건가요, 아니면 일부는 ETF나 다른 종목으로 분산할 계획이 있으신가요?"
            ),
        })

    lockup = _lockup_vs_moveout()
    if lockup:
        timing_note = (
            f"락업 만기({lockup['lock_until']})가 전세 만료({lockup['moveout_deadline']})보다 "
            f"{'늦습니다' if lockup['lock_after_moveout'] else '빠릅니다'} (약 {lockup['days_apart']}일 차이)."
        )
        points.append({
            "topic": "하나증권 락업주와 이사 시점",
            "context": (
                f"{lockup['ticker_name']} {lockup['quantity']}주는 {lockup['lock_until']}까지 보유해야 "
                f"{lockup['markup_krw']:,}원 마크업을 받습니다. {timing_note}"
            ),
            "question": (
                "전세 만료 이후 임시 거주(전세/월세) 자금이 필요할 수 있는데, 이 락업주는 자금 계획에서 "
                "제외하고 다른 재원으로 임시 거주 비용을 마련하는 쪽으로 생각하고 계신가요?"
            ),
        })

    funding = _housing_funding_timeline(personal.get("housing", {}))
    if funding:
        points.append({
            "topic": "청약 자금 갭과 이사 일정",
            "context": (
                f"{funding['notice_name']} 목표 자금 대비 약 {funding['funding_gap_krw']:,.0f}원이 부족한 상태이고, "
                f"전세 만료일은 {funding['moveout_deadline'] or '미입력'}입니다."
            ),
            "question": (
                "공공분양 입주 전까지 임시로 다시 전세/월세 계약이 필요한 상황인데, 그 임시 거주 자금과 "
                "청약 자금(계약금 등)을 같은 시기에 같이 마련해야 하는 건지, 임시 거주는 월세로 돌려서 "
                "목돈 지출을 늦추는 방안도 고려 중이신지 궁금합니다."
            ),
        })

    semi = _semiconductor_exposure_breadth(personal.get("asset_impact", {}))
    if semi and semi["semiconductor_related_count"] >= 3:
        points.append({
            "topic": "반도체/AI 익스포저 총량",
            "context": (
                f"주식 {', '.join(semi['semiconductor_stocks']) or '없음'}, "
                f"ETF {', '.join(semi['semiconductor_etfs']) or '없음'}까지 합치면 "
                f"보유 {semi['total_holdings']}개 종목/ETF 중 {semi['semiconductor_related_count']}개가 "
                "반도체 테마입니다."
            ),
            "question": (
                "업(業)과 투자가 같은 방향으로 겹쳐 있는 상태인데, 이 부분은 의도하신 대로(직업 지식을 "
                "활용한 확신 베팅) 유지하는 게 맞을까요, 아니면 커리어 리스크와 투자 리스크가 같이 움직이는 "
                "점이 신경 쓰이시나요?"
            ),
        })

    if portfolio_config().get("retirement_accounts"):
        points.append({
            "topic": "퇴직연금(IRP/DC) 자산의 역할",
            "context": (
                "IRP/DC 계좌는 퇴직 시까지 인출이 제한되어 있어, 현재 청약 자금이나 현금 유동성 계산에는 "
                "포함하지 않고 있습니다."
            ),
            "question": (
                "이 리포트의 '현금 유동성/자산 배분' 판단에서 퇴직연금은 계속 완전히 별도로 취급하면 될까요, "
                "아니면 은퇴 시점 목표(예: 조기은퇴 여부)에 따라 리밸런싱 조언에 포함시키길 원하시나요?"
            ),
        })

    return points
