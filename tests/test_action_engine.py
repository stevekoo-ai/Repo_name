from engine.action import conflict, engine as action_engine, generators


def test_priority_grade_bands():
    assert action_engine.priority_grade(90) == 5
    assert action_engine.priority_grade(85) == 5
    assert action_engine.priority_grade(75) == 4
    assert action_engine.priority_grade(60) == 3
    assert action_engine.priority_grade(45) == 2
    assert action_engine.priority_grade(10) == 1


def test_bond_action_uses_spec_example_text_when_favorable():
    actions = generators.from_bond({"bond_score": 70, "data_status": "ok"})
    assert actions[0]["title"] == "채권 비중 추가 확대 여부를 검토한다"
    assert "물가 둔화 확인이 추가로 필요" in actions[0]["reason"]
    assert actions[0]["invalid_condition"] == "CPI 재가속 또는 장기금리 급등 시 보류."


def test_conflict_resolver_suppresses_aggressive_buy_when_liquidity_need_active():
    """15.6: 반도체 강세이더라도 청약 자금 확보가 우선이면 공격적 매수 확대를 억제."""
    candidates = [
        {"title": "주식/ETF 비중 확대 검토", "category": "investment_opportunity",
         "factors": {"user_relevance": 80, "risk_level": 40, "time_urgency": 40,
                     "portfolio_impact": 80, "event_significance": 50}},
        {"title": "청약 자금 확보 계획 수립", "category": "liquidity_survival",
         "factors": {"user_relevance": 90, "risk_level": 60, "time_urgency": 70,
                     "portfolio_impact": 85, "event_significance": 50}},
    ]
    resolved = conflict.resolve_conflicts(candidates)
    stock_action = next(c for c in resolved if c["category"] == "investment_opportunity")
    assert "conflict_note" in stock_action
    assert stock_action["factors"]["portfolio_impact"] == 60  # 80 - 20 suppression


def test_category_rank_orders_liquidity_first():
    assert conflict.category_rank("liquidity_survival") < conflict.category_rank("macro_risk")
    assert conflict.category_rank("macro_risk") < conflict.category_rank("investment_opportunity")
    assert conflict.category_rank("investment_opportunity") < conflict.category_rank("travel_discretionary")
