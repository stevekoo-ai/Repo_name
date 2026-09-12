"""engine/execution/plan.py — 자금 조달 실행 계획 일일 판정.

## 이 테스트가 고정하는 계약

사용자 요청은 "매도 전략을 세우고, 근거가 실제로 맞아가는지 판단 포스트를
두고, Critical decision point를 계속 trace하는 daily 점검"이었다.
그 요청에서 **틀리면 돈이 날아가는 부분**만 골라 고정한다:

1. **금액 기반이지 주수 기반이 아니다** — 주가가 오르면 필요 주수가 줄어야
   한다. 주수를 고정하면 상승분을 스스로 버린다.
2. **시간 하한선은 반드시 발동한다** — 창이 지났는데 조용히 넘어가면
   데드라인에 몰려 아무 가격에나 던지게 된다.
3. **CDP는 데이터가 없을 때 '미발동'이 아니라 'UNKNOWN'이다** — 없는 걸
   "안전하다"로 읽으면 감시가 조용히 죽는다(R3).
4. **자동으로 팔지 않는다** — 이 모듈에 주문 경로가 있으면 안 된다.
"""
from datetime import date
from pathlib import Path

import pytest
import yaml

from engine.briefing import ledger as L
from engine.execution import plan as EP


@pytest.fixture
def plan():
    return EP.load_plan()


@pytest.fixture
def fake_price(monkeypatch):
    """가격만 갈아끼운다 — 나머지 거시 계열은 실제 파일을 그대로 쓴다."""
    def _set(price):
        real = L._lookup
        monkeypatch.setattr(
            L, "_lookup",
            lambda k, on: float(price) if k == "hynix_close" else real(k, on))
    return _set


# ── 계약 1: 금액 기반 — 주가가 오르면 필요 주수가 준다 ──────────

def test_required_shares_fall_as_price_rises(fake_price):
    fake_price(1_400_000)
    low = EP.evaluate(date(2026, 9, 12)).shares_remaining
    fake_price(2_400_000)
    high = EP.evaluate(date(2026, 9, 12)).shares_remaining
    assert low > high, "주가가 오르면 같은 금액을 더 적은 주수로 조달해야 한다"


def test_shares_for_rounds_up_never_short():
    """1주 모자라면 목표 미달이다. 내림은 허용하지 않는다."""
    assert EP.shares_for(1_000_000, 300_000) == 4      # 3.33 → 4
    assert EP.shares_for(900_000, 300_000) == 3        # 정확히 나누어떨어짐


def test_shares_for_returns_none_without_price():
    """가격을 모르면 추정치를 만들지 않는다."""
    assert EP.shares_for(1_000_000, None) is None
    assert EP.shares_for(1_000_000, 0) is None


# ── 계약 2: 시간 하한선은 반드시 발동한다 ────────────────────────

def test_tranche_is_open_inside_its_window(plan):
    st = EP.evaluate(date(2026, 10, 15), plan=plan, log=[])
    t1 = next(t for t in st.tranches if t.id == "T1")
    assert t1.state == "OPEN"


def test_tranche_becomes_due_at_floor_date_when_nothing_raised(plan):
    """하한선 날짜가 왔는데 조달이 0이면 DUE(강제 실행)여야 한다."""
    st = EP.evaluate(date(2026, 10, 31), plan=plan, log=[])
    t1 = next(t for t in st.tranches if t.id == "T1")
    assert t1.state == "DUE"
    assert "강제" in t1.note


def test_missed_window_is_flagged_not_silently_skipped(plan):
    """창이 지났는데 미실행이면 조용히 PENDING으로 남으면 안 된다."""
    st = EP.evaluate(date(2026, 11, 15), plan=plan, log=[])
    t1 = next(t for t in st.tranches if t.id == "T1")
    assert t1.state == "DUE", "지나간 tranche가 조용히 묻히면 데드라인에 몰린다"


def test_tranche_marked_done_once_cumulative_floor_met(plan):
    log = [{"date": "2026-10-05", "tranche_id": "T1", "shares": "20",
            "price_krw": "1812000", "amount_krw": "36240000", "note": ""}]
    st = EP.evaluate(date(2026, 10, 31), plan=plan, log=log)
    t1 = next(t for t in st.tranches if t.id == "T1")
    assert t1.state == "DONE"


def test_price_accelerator_opens_tranche_before_its_window(plan, fake_price):
    """T2는 11/4 시작이지만 2,000,000원을 넘으면 앞당길 수 있어야 한다."""
    fake_price(2_100_000)
    st = EP.evaluate(date(2026, 10, 15), plan=plan, log=[])
    t2 = next(t for t in st.tranches if t.id == "T2")
    assert t2.state == "ACCELERATED"
    assert "앞당김" in t2.note


def test_accelerator_does_not_fire_below_threshold(plan, fake_price):
    fake_price(1_800_000)
    st = EP.evaluate(date(2026, 10, 15), plan=plan, log=[])
    t2 = next(t for t in st.tranches if t.id == "T2")
    assert t2.state == "PENDING"


# ── 계약 3: CDP — 데이터 없음은 '안전'이 아니다 ──────────────────

def test_cdp_fires_on_price_collapse(plan, fake_price):
    fake_price(1_300_000)
    st = EP.evaluate(date(2026, 9, 12), plan=plan, log=[])
    cdp1 = next(c for c in st.cdps if c.id == "CDP1")
    assert cdp1.fired is True
    assert cdp1.severity == "critical"
    assert st.fired_cdps, "발동한 CDP는 fired_cdps에 잡혀야 브리핑 상단에 올라간다"


def test_cdp_fires_on_price_surge_as_opportunity(plan, fake_price):
    fake_price(2_500_000)
    st = EP.evaluate(date(2026, 9, 12), plan=plan, log=[])
    cdp5 = next(c for c in st.cdps if c.id == "CDP5")
    assert cdp5.fired is True
    assert cdp5.severity == "opportunity", "상승도 판단 지점이다 — 경고만 감시하면 절반만 본다"


def test_missing_data_is_unknown_not_safe(plan, monkeypatch):
    """데이터를 못 구했을 때 fired=False로 만들면 감시가 조용히 죽는다."""
    monkeypatch.setattr(L, "_lookup", lambda k, on: None)
    st = EP.evaluate(date(2026, 9, 12), plan=plan, log=[])
    assert all(c.fired is None for c in st.cdps)
    assert len(st.unknown_cdps) == len(st.cdps)
    assert not st.fired_cdps


def test_every_cdp_key_is_actually_resolvable_today(plan):
    """계획에 적은 감시 키가 실제 데이터에 없으면 그 CDP는 처음부터
    죽어 있는 것이다. 계획과 데이터의 연결을 고정한다."""
    st = EP.evaluate(date(2026, 9, 12), plan=plan, log=[])
    dead = [c.id for c in st.cdps if c.actual is None]
    assert not dead, f"실측 불가능한 CDP가 있다(감시 사각지대): {dead}"


# ── 계약 4: 판단 포스트 ──────────────────────────────────────────

def test_future_checkpoint_is_pending_not_scored(plan):
    st = EP.evaluate(date(2026, 9, 12), plan=plan, log=[])
    assert all(c.status == "PENDING" for c in st.checkpoints)


def test_checkpoint_scores_after_its_date(plan, fake_price):
    fake_price(1_500_000)                      # CP1 기준 1,900,000 미달
    st = EP.evaluate(date(2026, 11, 1), plan=plan, log=[])
    cp1 = next(c for c in st.checkpoints if c.id == "CP1")
    assert cp1.status == "MISS"
    assert cp1.if_false, "전제가 틀렸으면 무엇을 해야 하는지가 붙어 있어야 한다"


def test_checkpoint_hit_when_thesis_holds(plan, fake_price):
    fake_price(2_000_000)
    st = EP.evaluate(date(2026, 11, 1), plan=plan, log=[])
    cp1 = next(c for c in st.checkpoints if c.id == "CP1")
    assert cp1.status == "HIT"


def test_every_checkpoint_key_is_resolvable(plan, fake_price):
    fake_price(1_812_000)
    st = EP.evaluate(date(2027, 3, 1), plan=plan, log=[])   # 전부 검증일 경과
    dead = [c.id for c in st.checkpoints if c.status == "UNKNOWN"]
    assert not dead, f"실측 불가능한 판단 포스트: {dead}"


# ── 계약 5: 자동 매도 금지 ───────────────────────────────────────

def test_module_has_no_order_path():
    """판정 엔진에 주문 경로가 생기면 사고가 난다. 소스에서 직접 막는다."""
    src = (Path(EP.__file__)).read_text(encoding="utf-8")
    for forbidden in ("order", "requests.post", "httpx", "sell("):
        assert forbidden not in src.lower().replace("orderable", ""), \
            f"실행 계획 엔진에 주문 관련 코드가 있으면 안 된다: {forbidden}"


# ── 계획 데이터 자체의 정합성 ────────────────────────────────────

def test_tranche_amounts_sum_to_target(plan):
    total = sum(t["amount_krw"] for t in plan["tranches"])
    assert total == plan["target"]["amount_krw"], \
        f"tranche 합계 {total:,} != 목표 {plan['target']['amount_krw']:,}"


def test_cumulative_floors_are_monotonic(plan):
    floors = [t["cumulative_floor_krw"] for t in plan["tranches"]]
    assert floors == sorted(floors), "누적 하한선이 뒤로 갈수록 줄어들면 안 된다"


def test_last_floor_date_is_before_deadline(plan):
    assert plan["tranches"][-1]["floor_by"] <= plan["target"]["deadline"]


def test_locked_shares_are_not_counted_as_free(plan):
    pos = plan["position"]
    assert pos["free_shares"] == pos["total_shares"] - pos["locked_shares"]


def test_target_is_reachable_with_free_shares_at_current_price(plan):
    """락업 67주를 빼고도 목표 조달이 가능해야 한다 — 안 되면 계획이
    마크업 8,791,650원 포기를 전제로 깔고 있다는 뜻이다."""
    st = EP.evaluate(date(2026, 9, 12), plan=plan, log=[])
    assert st.shares_remaining <= plan["position"]["free_shares"]
