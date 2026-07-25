from engine.personal import bond as bond_mod


def test_inflation_slowdown_score_both_improving():
    macro_payload = {"changes": [
        {"indicator": "cpi", "direction": "improve"},
        {"indicator": "ppi", "direction": "improve"},
    ], "downgrade_signals": []}
    assert bond_mod._inflation_slowdown_score(macro_payload) == 90.0


def test_inflation_slowdown_score_reaccelerating():
    macro_payload = {"changes": [], "downgrade_signals": ["cpi_reaccelerating"]}
    assert bond_mod._inflation_slowdown_score(macro_payload) == 20.0


def test_inflation_slowdown_score_no_signal_is_none():
    macro_payload = {"changes": [], "downgrade_signals": []}
    assert bond_mod._inflation_slowdown_score(macro_payload) is None


def test_compute_bond_score_rises_with_rate_cut_expectation_and_cpi_slowdown(monkeypatch):
    """21.4 case 4: 금리 하락 기대 + CPI 둔화 -> Bond Score 상승."""
    monkeypatch.setattr(
        "engine.personal.market_conditions.rate_direction_score", lambda: (90.0, {"kr_3y_yield_change_bp_3m": -80})
    )
    monkeypatch.setattr(
        "engine.personal.market_conditions.real_rate_score", lambda base, cpi: (70.0, {"real_rate_pct": 1.0})
    )
    monkeypatch.setattr("engine.personal.market_conditions.macro_score_normalized", lambda payload: 40.0)

    macro_payload = {"changes": [
        {"indicator": "cpi", "direction": "improve"}, {"indicator": "ppi", "direction": "improve"},
    ], "downgrade_signals": []}

    result = bond_mod.compute_bond_score(macro_payload, base_rate=3.0, cpi_yoy=2.0)
    assert result["data_status"] == "ok"
    assert result["bond_score"] > 55  # favorable rate/inflation backdrop should score well above neutral
