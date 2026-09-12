"""scripts/portfolio_holdings.py 채권 수집(CTSC8407R) — 조용한 실패 방지 테스트.

## 왜 이 테스트가 필요한가

2026-09-12에 사용자가 "ISA 계좌에 만기 2027-01-18 채권 3천만원이 있다"고
했는데 `sources/portfolio-holdings.csv` 어디에도 없었다. 원인은 버그가
아니라 **주식잔고 TR(TTTC8434R)이 채권을 아예 안 준다**는 것이었다 —
즉 "데이터가 없다"와 "조회 경로가 없다"를 구분하지 못해 보유 자산을
없는 것으로 취급할 뻔했다.

같은 사고를 코드 레벨에서 막는다. 이 파일이 고정하는 계약:

1. 응답에 `output` 키 자체가 없으면 → **죽는다**(빈 결과로 넘어가지 않음)
2. 필드명이 하나라도 다르면 → **죽는다**(0건으로 조용히 넘어가지 않음)
3. 진짜로 채권이 없으면 → 빈 리스트(정상)
4. 잔고 0인 행은 제외
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import portfolio_holdings as PH  # noqa: E402


def _row(**over):
    """KIS CTSC8407R 응답 1행의 정상 형태 — 필드명은 open-trading-api
    examples_llm/domestic_bond/inquire_balance/chk_inquire_balance.py의
    COLUMN_MAPPING에서 그대로 가져왔다(추측 아님)."""
    base = {
        "pdno": "KR6095081C94",
        "buy_dt": "20260415",
        "buy_sqno": "1",
        "cblc_qty": "30000",
        "agrx_qty": "0",
        "sprx_qty": "0",
        "exdt": "20270118",
        "buy_erng_rt": "5.35",
        "buy_unpr": "10000",
        "buy_amt": "30000000",
        "ord_psbl_qty": "30000",
    }
    base.update(over)
    return base


# ── 계약 1: output 키가 없으면 죽는다 ────────────────────────

def test_missing_output_key_exits_instead_of_returning_empty():
    """응답 구조가 바뀌었는데 '채권 없음'으로 보고하면 최악이다."""
    with pytest.raises(SystemExit) as e:
        PH._parse_bonds({"rt_cd": "0", "msg1": "정상처리"})
    assert "output" in str(e.value)


# ── 계약 2: 필드명이 다르면 죽는다 ───────────────────────────

def test_renamed_field_exits_and_names_the_missing_field():
    broken = _row()
    broken["expire_dt"] = broken.pop("exdt")  # 만기일 필드명이 바뀐 상황
    with pytest.raises(SystemExit) as e:
        PH._parse_bonds({"output": [broken]})
    assert "exdt" in str(e.value), "어느 필드가 없는지 이름을 알려줘야 고칠 수 있다"


# ── 계약 3: 진짜 미보유는 정상 ───────────────────────────────

def test_empty_list_is_normal_not_an_error():
    assert PH._parse_bonds({"output": []}) == []


def test_single_dict_response_is_wrapped():
    """output이 리스트가 아니라 단일 객체로 오는 경우도 있다."""
    got = PH._parse_bonds({"output": _row()})
    assert len(got) == 1


# ── 계약 4: 정상 파싱 ────────────────────────────────────────

def test_parses_maturity_and_yield_which_the_ladder_needs():
    got = PH._parse_bonds({"output": [_row()]})
    assert len(got) == 1
    b = got[0]
    assert b["maturity"] == "20270118", "만기 사다리 설계의 핵심 필드"
    assert b["buy_yield"] == "5.35"
    assert b["buy_amount"] == "30000000"
    assert b["ticker"] == "KR6095081C94"


def test_zero_quantity_rows_are_dropped():
    got = PH._parse_bonds({"output": [_row(), _row(cblc_qty="0", pdno="KR000000000")]})
    assert len(got) == 1
    assert got[0]["ticker"] == "KR6095081C94"


def test_non_numeric_quantity_is_treated_as_zero_not_crash():
    got = PH._parse_bonds({"output": [_row(cblc_qty="")]})
    assert got == []


# ── TR·필드 상수가 조사 결과와 일치하는지 고정 ────────────────

def test_tr_id_matches_official_example():
    assert PH.BOND_BALANCE_TR == "CTSC8407R"


def test_bond_fields_cover_what_the_ladder_design_needs():
    for need in ("maturity", "buy_yield", "quantity", "buy_amount"):
        assert need in PH.BOND_FIELDS
