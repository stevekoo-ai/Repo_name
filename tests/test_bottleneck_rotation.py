"""병목 이동 추적(engine/bottleneck/rotation.py) — 네트워크 없이 합성 데이터로.

사용자 요청(2026-09-24): 다음 병목이 확정되기 전에 해당 섹터 대장주·ETF를
단계별로 사 두는 전략을 리포트가 제안하게. 여기서 고정하는 건 "틀린 제안을
하지 않는 조건"들이다 — 하루 튄 주가로 승격하지 않기, 모르는 걸 아는 척
하지 않기, 메모리가 여전히 병목이면 헤지를 끝까지 채우지 않기.
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

from engine.bottleneck import rotation as R

REPO = Path(__file__).resolve().parents[1]
AS_OF = date(2026, 9, 24)


def _series(end: date, n: int, start_px: float, end_px: float) -> list[tuple[date, float]]:
    """end까지 n일(주말 포함 단순화) 선형 가격."""
    step = (end_px - start_px) / (n - 1)
    return [(end - timedelta(days=n - 1 - i), start_px + step * i) for i in range(n)]


def _prices(up: list[str], down: list[str], end: date = AS_OF) -> dict:
    p = {t: _series(end, 200, 100, 200) for t in up}
    p.update({t: _series(end, 200, 200, 100) for t in down})
    return p


def _fund(ticker, metric, pairs, filed_lag=40):
    """pairs: [(end_date_iso, value)] → fundamentals rows."""
    return [{"ticker": ticker, "metric": metric, "end_date": e,
             "filed_date": (date.fromisoformat(e) + timedelta(days=filed_lag)).isoformat(),
             "value_usd": str(v)} for e, v in pairs]


# 두 분기 YoY: 2026-06 +50%, 2026-03 +30% → 수준·가속 둘 다 성립
ACCEL = [("2025-03-31", 100), ("2025-06-30", 100), ("2026-03-31", 130), ("2026-06-30", 150)]


def _cfg(**over):
    cfg = {
        "meta": {"hedge_budget_krw": 10_000_000, "persistence_days": 7,
                 "fundamental_stale_days": 200, "price_stale_days": 7,
                 "anchor_date": "2027-04-01", "anchor_label": "테스트"},
        "incumbent": {"name": "HBM", "signals": [
            {"id": "I2", "desc": "하이닉스 이평 하회", "type": "ma_position",
             "basket": ["HX"], "window": 120, "position": "below"},
        ]},
        "candidates": [
            {"id": "B1", "name": "전력", "role": "hedge", "budget_weight": 1.0,
             "instruments": {"etf": [{"ticker": "ETF1", "name": "전력ETF"}], "leaders": []},
             "signals": [
                 {"id": "F1", "kind": "fundamental", "desc": "", "type": "yoy_level",
                  "metric": "backlog", "tickers": ["PW"], "min_pct": 20},
                 {"id": "F2", "kind": "fundamental", "desc": "", "type": "yoy_accel",
                  "metric": "backlog", "tickers": ["PW"]},
                 {"id": "M1", "kind": "market", "desc": "", "type": "rel_return",
                  "basket": ["PW"], "vs": "HX", "days": 63, "op": ">", "value": 0},
                 {"id": "M2", "kind": "market", "desc": "", "type": "ma_position",
                  "basket": ["PW"], "window": 120, "position": "above"},
             ]},
        ],
        "stages": [
            {"stage": 1, "name": "정찰", "min_score": 2, "require_both_kinds": True, "min_incumbent": 0, "cum_pct": 25},
            {"stage": 2, "name": "구축", "min_score": 3, "require_both_kinds": True, "min_incumbent": 1, "cum_pct": 60},
            {"stage": 3, "name": "확정", "min_score": 4, "require_both_kinds": True, "min_incumbent": 2, "cum_pct": 100},
        ],
        "unwind": {"max_score": 1},
    }
    cfg.update(over)
    return cfg


def _b1(st):
    return next(c for c in st.candidates if c.id == "B1")


# ── 단계 판정 ──────────────────────────────────────────────────

def test_fundamentals_alone_never_reach_scout_stage():
    """펀더멘털이 아무리 좋아도 시장(주가)이 아직 안 움직이면 사지 않는다."""
    st = R.evaluate(AS_OF, _cfg(), prices=_prices(up=["HX"], down=["PW"]),
                    fundamentals=_fund("PW", "backlog", ACCEL), log=[])
    b1 = _b1(st)
    assert b1.score == 2 and b1.stage == 0
    assert "주가 신호" in b1.next_hint


def test_full_signals_with_incumbent_easing_reaches_build_and_proposes_gap():
    st = R.evaluate(AS_OF, _cfg(), prices=_prices(up=["PW"], down=["HX"]),
                    fundamentals=_fund("PW", "backlog", ACCEL), log=[])
    b1 = _b1(st)
    assert b1.score == 4 and st.incumbent_easing == 1
    assert b1.stage == 2, "약화 신호 1개뿐이라 확정(3)이 아니라 구축(2)까지만"
    assert b1.target_krw == 6_000_000 and b1.gap_krw == 6_000_000


def test_hedge_without_incumbent_easing_stays_at_scout():
    """후보가 아무리 강해도 현재 병목(HBM)이 멀쩡하면 헤지를 크게 늘리지 않는다."""
    st = R.evaluate(AS_OF, _cfg(), prices=_prices(up=["PW", "HX"], down=[]),
                    fundamentals=_fund("PW", "backlog", ACCEL), log=[])
    b1 = _b1(st)
    assert st.incumbent_easing == 0
    assert b1.stage == 1


def test_executed_purchases_reduce_the_proposed_gap():
    log = [{"date": "2026-09-01", "candidate": "B1", "ticker": "ETF1", "amount_krw": "2500000"}]
    st = R.evaluate(AS_OF, _cfg(), prices=_prices(up=["PW"], down=["HX"]),
                    fundamentals=_fund("PW", "backlog", ACCEL), log=log)
    assert _b1(st).gap_krw == 6_000_000 - 2_500_000


def test_falling_less_than_hynix_is_not_rotation():
    """2026-09-24 첫 실데이터 오탐 재현 — AI 섹터 전체가 빠지는데 전력이
    하이닉스보다 '덜 빠졌다'고 매수(2단계 900만원)를 제안했다. min_abs가 있으면
    후보 바스켓 자체가 플러스여야 순환매로 인정한다."""
    cfg = _cfg()
    cfg["candidates"][0]["signals"][2]["min_abs"] = 0
    prices = {"PW": _series(AS_OF, 200, 200, 150),   # -25%
              "HX": _series(AS_OF, 200, 200, 100)}   # -50%
    st = R.evaluate(AS_OF, cfg, prices=prices, fundamentals=_fund("PW", "backlog", ACCEL), log=[])
    m1 = next(s for s in _b1(st).signals if s.id == "M1")
    assert m1.ok is False and "동반 하락" in m1.detail
    assert _b1(st).stage == 0 and _b1(st).gap_krw == 0


def test_real_config_guards_every_candidate_relative_strength_with_min_abs():
    cfg = R.load_config()
    for c in cfg["candidates"]:
        for s in c["signals"]:
            if s["type"] == "rel_return":
                assert "min_abs" in s, f"{c['id']} {s['id']}: 동반 하락을 순환매로 오판할 수 있다"


# ── 지속성·R3 ──────────────────────────────────────────────────

def test_one_week_old_reversal_counts_as_forming_not_confirmed():
    """1주 전엔 하락 추세였다가 최근에만 뛰었으면 '형성 중'이지 확정 신호가 아니다."""
    base = _series(AS_OF - timedelta(days=5), 195, 200, 100)       # 5일 전까지 하락
    jump = [(AS_OF - timedelta(days=4 - i), 100 + 60 * (i + 1)) for i in range(5)]  # 최근 급등
    prices = {"PW": base + jump, "HX": _series(AS_OF, 200, 100, 100.5)}
    st = R.evaluate(AS_OF, _cfg(), prices=prices, fundamentals=[], log=[])
    m1 = next(s for s in _b1(st).signals if s.id == "M1")
    assert m1.ok is False and m1.forming


def test_missing_price_data_is_unknown_not_false_and_blocks_nothing_silently():
    st = R.evaluate(AS_OF, _cfg(), prices={}, fundamentals=_fund("PW", "backlog", ACCEL), log=[])
    b1 = _b1(st)
    assert {s.id for s in b1.unknown} == {"M1", "M2"}
    assert b1.stage == 0
    assert "판정 불가" in R.render_markdown(st)


def test_stale_fundamentals_are_excluded():
    """AMKR·LITE 백로그처럼 2021년에 멈춘 값으로 오늘을 판정하지 않는다."""
    old = [("2020-03-31", 100), ("2020-06-30", 100), ("2021-03-31", 150), ("2021-06-30", 200)]
    st = R.evaluate(AS_OF, _cfg(), prices={}, fundamentals=_fund("PW", "backlog", old), log=[])
    f1 = next(s for s in _b1(st).signals if s.id == "F1")
    assert f1.ok is None


def test_values_filed_after_as_of_are_not_used():
    rows = _fund("PW", "backlog", ACCEL)
    rows[-1]["filed_date"] = "2026-10-30"  # 2026-06-30분이 as_of 이후에야 공시됐다고 가정
    st = R.evaluate(AS_OF, _cfg(), prices={}, fundamentals=rows, log=[])
    f1 = next(s for s in _b1(st).signals if s.id == "F1")
    assert "+30%" in f1.detail and "+50%" not in f1.detail


def test_stale_prices_are_unknown():
    old_end = AS_OF - timedelta(days=30)
    st = R.evaluate(AS_OF, _cfg(), prices=_prices(up=["PW"], down=["HX"], end=old_end),
                    fundamentals=[], log=[])
    assert all(s.ok is None for s in _b1(st).signals if s.kind == "market")


# ── 메모리 연장 상한·철회 ───────────────────────────────────────

def test_strong_memory_capacity_bottleneck_caps_hedge_stage():
    cfg = _cfg()
    cfg["candidates"].append({
        "id": "B2", "name": "메모리 용량", "role": "extension",
        "signals": [
            {"id": "MF1", "kind": "fundamental", "desc": "", "type": "yoy_level",
             "metric": "revenue", "tickers": ["ND"], "min_pct": 20},
            {"id": "MF2", "kind": "fundamental", "desc": "", "type": "yoy_accel",
             "metric": "revenue", "tickers": ["ND"]},
            {"id": "MM1", "kind": "market", "desc": "", "type": "ma_position",
             "basket": ["ND"], "window": 120, "position": "above"},
        ]})
    cfg["incumbent"]["signals"].append(
        {"id": "I3", "desc": "", "type": "rel_return", "basket": ["HX"], "vs": "PW",
         "days": 63, "op": "<", "value": 0})
    cfg["extension_caps_hedge"] = {"when_extension_stage_at_least": 2, "hedge_max_stage": 2}
    fund = _fund("PW", "backlog", ACCEL) + _fund("ND", "revenue", ACCEL)
    st = R.evaluate(AS_OF, cfg, prices=_prices(up=["PW", "ND"], down=["HX"]), fundamentals=fund, log=[])
    b1 = _b1(st)
    assert st.incumbent_easing == 2, "상한이 없었다면 3단계 조건 충족"
    assert b1.stage == 2 and b1.capped_by


def test_unwind_when_holding_but_signals_dead_for_a_week():
    log = [{"date": "2026-08-01", "candidate": "B1", "ticker": "ETF1", "amount_krw": "1000000"}]
    st = R.evaluate(AS_OF, _cfg(), prices=_prices(up=["HX"], down=["PW"]), fundamentals=[], log=log)
    b1 = _b1(st)
    assert b1.unwind
    assert "철회 검토" in R.render_markdown(st)


def test_digest_collapse_parses_hbm_status_label(tmp_path, monkeypatch):
    (tmp_path / "hbm-cycle-score.yaml").write_text(
        'as_of: "2026-09-21"\nstatus_label: "🔴 붕괴조건 3/5 충족"\n', encoding="utf-8")
    monkeypatch.setattr(R, "DIGEST_DIR", tmp_path)
    assert R._digest_collapse("hbm-cycle-score", 2)[0] is True
    assert R._digest_collapse("없는-다이제스트", 2)[0] is None


# ── 실제 설정 파일 무결성 ─────────────────────────────────────

def test_real_config_is_internally_consistent():
    cfg = R.load_config()
    hedges = [c for c in cfg["candidates"] if c["role"] == "hedge"]
    assert abs(sum(c["budget_weight"] for c in hedges) - 1.0) < 1e-9, "헤지 예산 비중 합은 1"
    known = {"yoy_level", "yoy_accel", "rel_return", "ma_position", "digest_collapse"}
    for c in cfg["candidates"]:
        for s in c["signals"]:
            assert s["type"] in known and s["kind"] in ("fundamental", "market")
    # 실제 파일로 끝까지 돌아가야 한다(데이터가 없으면 판정 불가로라도)
    R.render_markdown(R.evaluate(AS_OF))


def test_price_collector_covers_every_ticker_the_engine_reads():
    sys.path.insert(0, str(REPO / "scripts"))
    import bottleneck_prices as BP
    cfg = R.load_config()
    collected = set(BP.tickers_from_config(cfg))
    for c in cfg["candidates"]:
        for s in c["signals"]:
            if s["type"] in ("rel_return", "ma_position"):
                assert set(s["basket"]) <= collected
                if s.get("vs"):
                    assert s["vs"] in collected


def test_report_never_issues_hynix_sell_directive():
    """R4 — 하이닉스 매매 지시는 sk_hynix_decision 단일 출처."""
    st = R.evaluate(AS_OF, _cfg(), prices=_prices(up=["PW"], down=["HX"]),
                    fundamentals=_fund("PW", "backlog", ACCEL), log=[])
    md = R.render_markdown(st)
    assert "하이닉스 매도" not in md.replace("하이닉스 자체의 매도 지시는", "")
    assert "R4" in md
