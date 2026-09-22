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


# T1 완료 상태 — 앞당김 테스트의 전제(2026-09-14 순차 제약 이후,
# 앞선 tranche가 끝나야 뒤가 열린다)
_T1_DONE = [{"date": "2026-10-05", "tranche_id": "T1", "shares": "20",
             "price_krw": "1812000", "amount_krw": "36240000", "note": ""}]


def test_price_accelerator_opens_tranche_before_its_window(plan, fake_price):
    """T2는 11/4 시작이지만 2,000,000원을 넘으면 앞당길 수 있어야 한다.
    단 순차 제약이 있으므로 T1이 끝나 있어야 한다."""
    fake_price(2_100_000)
    st = EP.evaluate(date(2026, 10, 15), plan=plan, log=_T1_DONE)
    t2 = next(t for t in st.tranches if t.id == "T2")
    assert t2.state == "ACCELERATED"
    assert "앞당김" in t2.note


def test_accelerator_does_not_fire_below_threshold(plan, fake_price):
    """차례가 왔어도(T1 완료) 가격이 임계 아래면 열리지 않는다 —
    순차 제약 때문에 우연히 통과하는 게 아니라 가격 조건 자체로 막혀야 한다."""
    fake_price(1_800_000)
    st = EP.evaluate(date(2026, 10, 15), plan=plan, log=_T1_DONE)
    t2 = next(t for t in st.tranches if t.id == "T2")
    assert t2.state == "PENDING"
    assert "앞당김 조건은 충족" not in t2.note, "가격 미달인데 '조건 충족'으로 적히면 안 된다"


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


# ── 계약 6: 조용한 날에도 CDP는 사장님께 도달해야 한다 ───────────
# CDP 중에는 몇 주에 걸쳐 서서히 이탈하는 것이 있다(us_10y 같은). 그런 날은
# 시장이 조용해 게이트가 닫히는데, 그러면 블록 ⑧이 발행되지 않아 경고가
# 도달하지 못한다 — "계속 trace한다"가 그 순간 깨진다.

def test_fired_cdp_forces_publish_on_an_otherwise_quiet_day(monkeypatch):
    from engine.briefing import context as CTX

    monkeypatch.setattr(CTX, "detect_triggers", lambda d: (set(), []))
    monkeypatch.setattr(CTX, "_series_map", lambda: {})      # 시장 조용
    monkeypatch.setattr(L, "open_predictions", lambda d: [])  # 도래 예측 없음

    base = EP.evaluate
    monkeypatch.setattr(L, "_lookup",
                        lambda k, on: 1_300_000.0 if k == "hynix_close" else None)
    gate = CTX.evaluate_gate(date(2026, 9, 12), set(), [])
    assert gate.publish is True, "CDP가 발동했는데 '조용한 날'로 닫히면 경고가 유실된다"
    assert any("CDP" in r for r in gate.reasons)
    assert base is EP.evaluate


def test_due_tranche_forces_publish_on_a_quiet_day(monkeypatch):
    from engine.briefing import context as CTX

    monkeypatch.setattr(CTX, "detect_triggers", lambda d: (set(), []))
    monkeypatch.setattr(CTX, "_series_map", lambda: {})
    monkeypatch.setattr(L, "open_predictions", lambda d: [])
    gate = CTX.evaluate_gate(date(2026, 10, 31), set(), [])   # T1 하한선 도래일
    assert gate.publish is True
    assert any("tranche" in r for r in gate.reasons)


def test_gate_survives_a_broken_execution_plan(monkeypatch):
    """부가 기능이 깨져도 브리핑 본체는 나가야 한다."""
    from engine.briefing import context as CTX

    monkeypatch.setattr(EP, "evaluate", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    gate = CTX.evaluate_gate(date(2026, 9, 12), {"x"}, ["시장 변동"])
    assert gate.publish is True


# ── 계약 7: 앞당김은 한 번에 하나씩 (분할 전환 보호) ─────────────
# 이전 구현은 가격이 임계를 넘으면 그 임계를 넘는 모든 미래 tranche를
# 동시에 열었다 — 2,500,000원이면 T2·T3·T4가 같은 날 전부 열려 사실상
# "오늘 전량 매도 가능"이 됐다. 급등 하루에 분할 전환 원칙이 무너지고,
# 그 가격이 고점이 아니라 통과점이었다면 나머지를 전부 싸게 판 셈이 된다.

def test_surge_does_not_open_every_future_tranche_at_once(plan, fake_price):
    fake_price(2_500_000)          # T2(2.0M)·T3(2.2M)·T4(2.4M) 임계 전부 초과
    st = EP.evaluate(date(2026, 10, 20), plan=plan, log=[])
    accelerated = [t.id for t in st.tranches if t.state == "ACCELERATED"]
    assert accelerated == [], \
        f"앞선 T1이 미완료인데 뒤 tranche가 열렸다: {accelerated}"


def test_acceleration_unlocks_one_at_a_time_as_earlier_tranches_complete(plan, fake_price):
    fake_price(2_500_000)
    log = [{"date": "2026-10-05", "tranche_id": "T1", "shares": "15",
            "price_krw": "2500000", "amount_krw": "37500000", "note": ""}]
    st = EP.evaluate(date(2026, 10, 20), plan=plan, log=log)
    states = {t.id: t.state for t in st.tranches}
    assert states["T1"] == "DONE"
    assert states["T2"] == "ACCELERATED", "앞선 tranche가 끝나면 다음이 열려야 한다"
    assert states["T3"] == "PENDING", "그 다음 것까지 같이 열리면 제약이 무의미하다"
    assert states["T4"] == "PENDING"


def test_blocked_acceleration_explains_itself(plan, fake_price):
    """조건은 맞는데 안 열렸다는 사실을 숨기면 사람이 이유를 알 수 없다."""
    fake_price(2_500_000)
    st = EP.evaluate(date(2026, 10, 20), plan=plan, log=[])
    t2 = next(t for t in st.tranches if t.id == "T2")
    assert "앞당김 조건은 충족" in t2.note
    assert "대기" in t2.note


def test_due_is_never_blocked_by_the_sequential_rule(plan, fake_price):
    """일정이 밀려 만회해야 하는 상황까지 막으면 데드라인을 놓친다.
    앞당김(기회 포착)은 순서대로, 만회(기한 방어)는 제한 없이."""
    fake_price(1_812_000)
    st = EP.evaluate(date(2026, 12, 15), plan=plan, log=[])   # T1·T2 창 이미 종료
    states = {t.id: t.state for t in st.tranches}
    assert states["T1"] == "DUE"
    assert states["T2"] == "DUE", "밀린 tranche는 순차 제약과 무관하게 DUE로 떠야 한다"
    assert states["T3"] == "OPEN"     # 12/15는 T3 창 안 + floor_by(12/31) 이전 → OPEN


def test_briefing_block_surfaces_waiting_tranches(fake_price):
    """CDP5가 '급등 기회'라고 떴는데 열린 tranche가 없으면, 왜 그런지
    브리핑에 나와야 한다."""
    from engine.briefing import context as CTX
    fake_price(2_500_000)
    body = CTX.build_execution_block(date(2026, 10, 20)).body
    assert "앞당김 대기" in body
    assert "T2" in body and "T3" in body and "T4" in body


def test_cdp5_action_text_matches_the_sequential_rule(plan):
    """계획서 문구가 '일괄 실행'이면 코드와 모순된다 — 문서 드리프트 방지."""
    cdp5 = next(c for c in plan["critical_decision_points"] if c["id"] == "CDP5")
    assert "일괄" not in cdp5["action"]
    assert "하나씩" in cdp5["action"]


# ── 사전 경보(Early Warning) — 2026-09-22 신설 ────────────────────
#
# 사용자 요청: "점검 포인트가 나타나면 내가 알 수 있도록 알람을 줘야지!
# 그리고 다음 판단 블록이 검토해서 액션 아이템과 플랜B가 가동되어야지!"
#
# CDP는 임계를 **넘은 뒤** 발동한다. 그것만으로는 "깨진 날 처음 아는" 구조라
# 손 쓸 시간이 없다. 이 경보는 접근·이탈 중일 때 미리 뜬다.

def _fake_macro(monkeypatch, **vals):
    """특정 거시 키만 갈아끼운다(실제 CSV가 자라도 테스트가 안 깨지게)."""
    real = L._lookup
    monkeypatch.setattr(
        L, "_lookup",
        lambda k, on: float(vals[k]) if k in vals else real(k, on))


def test_approach_warning_fires_before_the_threshold_breaks(monkeypatch):
    """EW1의 존재 이유 — 원/달러 1,383.8원일 때 CDP4(1,500)는 '발동 없음'인데
    CP5 마지노선(1,400)까지는 16원뿐이었다. CDP만 보면 안전해 보인다."""
    _fake_macro(monkeypatch, kr_usdkrw=1383.8)
    st = EP.evaluate(date(2026, 9, 22))
    ew1 = next(w for w in st.early_warnings if w.id == "EW1")
    assert ew1.fired is True
    assert ew1.distance == pytest.approx(16.2, abs=0.01)
    cdp4 = next(c for c in st.cdps if c.id == "CDP4")
    assert cdp4.fired is False, "CDP는 아직 조용한데 사전경보만 떠야 이 기능이 의미가 있다"


def test_approach_warning_stays_quiet_when_there_is_real_room(monkeypatch):
    """여유가 충분하면 안 떠야 한다 — 매일 뜨는 경고는 소음이 되어 무시된다
    (데이터 헬스 제어 루프에서 이미 배운 원칙)."""
    _fake_macro(monkeypatch, kr_usdkrw=1200.0)
    st = EP.evaluate(date(2026, 9, 22))
    assert next(w for w in st.early_warnings if w.id == "EW1").fired is False


def test_premise_drift_warning_fires_before_the_checkpoint_date(monkeypatch):
    """EW2 — CP2 확인일(11/3) 전인데 VIX가 전제(≥22)에서 크게 벌어진 상태."""
    _fake_macro(monkeypatch, us_vix=14.81)
    st = EP.evaluate(date(2026, 9, 22))
    ew2 = next(w for w in st.early_warnings if w.id == "EW2")
    assert ew2.fired is True
    assert ew2.distance == pytest.approx(7.19, abs=0.01)


def test_premise_drift_stops_once_the_checkpoint_date_has_passed(monkeypatch):
    """확인일이 지나면 CP 본판정의 몫이다 — 사전경보가 계속 뜨면 중복이다."""
    _fake_macro(monkeypatch, us_vix=14.81)
    st = EP.evaluate(date(2026, 12, 1))
    assert next(w for w in st.early_warnings if w.id == "EW2").fired is False


def test_companion_axis_escalates_severity_when_the_linked_digest_turns_red(monkeypatch, tmp_path):
    """복합 조건 — 원화(EW1)와 엔캐리 청산은 같은 축이다. 엔캐리가 시나리오 B로
    넘어가면 원화 압력이 빨라지므로 등급을 올린다."""
    _fake_macro(monkeypatch, kr_usdkrw=1383.8)
    digest_dir = tmp_path / "data" / "wiki_digest"
    digest_dir.mkdir(parents=True)
    (digest_dir / "yen-carry-trade-unwind.yaml").write_text(
        'slug: yen-carry-trade-unwind\nstatus_label: "🔴 시나리오 B 진입"\n',
        encoding="utf-8")
    monkeypatch.setattr(EP, "REPO", tmp_path)
    st = EP.evaluate(date(2026, 9, 22))
    ew1 = next(w for w in st.early_warnings if w.id == "EW1")
    assert ew1.severity == "critical", "🟠 warning → 🔴 critical로 승격돼야 한다"
    assert ew1.escalated_by == "yen-carry-trade-unwind"


def test_missing_data_is_unjudged_not_safe(monkeypatch):
    """R3 — 값을 못 구하면 '안전'이 아니라 '판정 불가'다."""
    real = L._lookup
    monkeypatch.setattr(L, "_lookup",
                        lambda k, on: None if k == "kr_usdkrw" else real(k, on))
    st = EP.evaluate(date(2026, 9, 22))
    ew1 = next(w for w in st.early_warnings if w.id == "EW1")
    assert ew1.fired is None
    assert ew1 not in st.fired_early_warnings


def test_every_early_warning_carries_an_action_and_a_plan_b(plan):
    """경보만 뜨고 할 일이 없으면 다음 판단 블록이 움직일 수 없다 —
    '경보가 뜬 날 급하게 생각하는' 상황 자체를 막는 게 목적이다."""
    warnings = plan.get("early_warnings", [])
    assert warnings, "사전 경보가 하나도 없으면 이 기능이 죽은 것이다"
    for w in warnings:
        assert w.get("action", "").strip(), f"{w['id']}에 액션 아이템이 없다"
        assert w.get("plan_b", "").strip(), f"{w['id']}에 플랜B가 없다"
        assert w.get("linked"), f"{w['id']}가 어떤 CP/CDP와 연결되는지 없다"
