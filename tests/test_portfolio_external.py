"""API 없는 증권사(하나증권) 보유 — 수동 수량·평단 + 자동 가격 기록(2026-10-01)."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import portfolio_holdings as P  # noqa: E402


def _setup(tmp_path, monkeypatch, kis_price=None):
    monkeypatch.setattr(P, "CSV_PATH", tmp_path / "holdings.csv")
    ext = tmp_path / "ext.yaml"
    ext.write_text(
        f'as_of: "{datetime.now(timezone.utc).date()}"\n'
        "holdings:\n  - {broker: 하나증권, ticker: \"000660\", name: SK하이닉스, quantity: 110, avg_price: 613558}\n",
        encoding="utf-8")
    monkeypatch.setattr(P, "EXTERNAL_YAML", ext)
    snap = tmp_path / "snap.csv"
    snap.write_text("date,ticker,close\n2026-09-30,000660,1783000\n", encoding="utf-8")
    monkeypatch.setattr(P, "PRICE_SNAPSHOT", snap)
    if kis_price:
        P.upsert_holdings("일반", [{"ticker": "000660", "name": "SK하이닉스", "quantity": 120,
                                   "avg_price": 291783, "current_price": kis_price, "eval_amount": 0,
                                   "profit_loss": 0, "profit_loss_pct": 0}])


def test_external_row_uses_todays_kis_price_and_manual_qty(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, kis_price=1776000)
    assert P.sync_external() == 1
    row = [r for k, r in P._read_csv().items() if k[1] == "하나증권(수동)"][0]
    assert int(row["quantity"]) == 110 and float(row["current_price"]) == 1776000
    assert int(row["eval_amount"]) == 110 * 1776000
    assert row["source"] == "manual_qty+kis_price"


def test_external_falls_back_to_price_snapshot(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert P.sync_external() == 1
    row = [r for k, r in P._read_csv().items() if k[1] == "하나증권(수동)"][0]
    assert float(row["current_price"]) == 1783000


def test_real_external_file_is_consistent_with_lock():
    # 수량은 매도(T1~)로 바뀌므로 고정값 대신 불변 조건만 검사한다
    import yaml
    ext = yaml.safe_load(P.EXTERNAL_YAML.read_text(encoding="utf-8"))
    plan = yaml.safe_load((REPO / "data/manual_inputs/execution_plan.yaml").read_text(encoding="utf-8"))
    locked = next(v["locked_shares"] for v in plan.values() if isinstance(v, dict) and "locked_shares" in v)
    for h in ext["holdings"]:
        assert h["quantity"] > 0 and h["avg_price"] > 0
        if "locked_quantity" in h:
            assert h["locked_quantity"] + h["free_quantity"] == h["quantity"]
            assert h["locked_quantity"] == locked     # 락업은 하나증권 67주(execution_plan)
