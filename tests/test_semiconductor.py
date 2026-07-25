from engine.semiconductor import score as semi_score


def test_status_band_has_no_gap_at_float_boundaries():
    # Regression: 79.6 used to fall between "positive" (max 79) and
    # "strong_positive" (min 80) and return "unclassified".
    assert semi_score.status_band(79.6) == "positive"
    assert semi_score.status_band(80.0) == "strong_positive"
    assert semi_score.status_band(64.9) == "neutral_plus"
    assert semi_score.status_band(0.0) == "weak_risk"
    assert semi_score.status_band(100.0) == "strong_positive"


def test_compute_semiconductor_score_with_signals(monkeypatch):
    monkeypatch.setattr(
        "collectors.manual.get_semiconductor_signal_dict",
        lambda: {
            "dram_price_trend": 1.0, "nand_price_trend": 1.0, "guidance_signal": 1.0,
            "inventory_supply_signal": 1.0, "ai_leader_earnings": 1.0, "gpu_shipment": 1.0,
            "ai_server_shipment": 1.0, "csp_capex": 1.0, "hbm_signal": 1.0,
        },
    )
    result = semi_score.compute_semiconductor_score(semiconductor_exports_yoy=25.0)
    assert result["data_status"] == "ok"
    assert result["semiconductor_score"] > 80
    assert result["status_band"] == "strong_positive"


def test_compute_semiconductor_score_pending_without_signals(monkeypatch):
    monkeypatch.setattr("collectors.manual.get_semiconductor_signal_dict", lambda: None)
    result = semi_score.compute_semiconductor_score(semiconductor_exports_yoy=None)
    assert result["data_status"] == "pending"
