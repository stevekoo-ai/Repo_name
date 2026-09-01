"""하이퍼스케일러 CapEx + AI 밸류체인 변두리 실측 리더 (SEC EDGAR XBRL 수집분).

2026-08-06/07 신설, **2026-08-27 daily_report.py에서 공유 모듈로 추출**
(scripts/hbm_cycle_score.py와 같은 이유 — PEOS 엔진도 같은 실측 숫자를
쓰려면 로직을 복붙해야 했다). 순수 CSV 리더라 investor_flow.py 같은 다른
scripts/ 모듈에 의존하지 않음 — stdlib(csv/datetime/pathlib)뿐이라 어느
호출 컨텍스트(사이블링/패키지)에서든 그대로 import된다.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path

KST = timezone(timedelta(hours=9))
_REPO_ROOT = Path(__file__).resolve().parent.parent
HYPERSCALER_CAPEX_CSV_PATH = _REPO_ROOT / "sources" / "hyperscaler-capex.csv"
HYPERSCALER_CAPEX_STALE_DAYS = 150  # 분기 실적은 보통 분기말+30~45일 내 공시 — 5개월 이상 지나면 스테일로 취급
AI_PERIPHERY_CSV_PATH = _REPO_ROOT / "sources" / "ai-periphery-fundamentals.csv"
AI_PERIPHERY_STALE_DAYS = 150  # 위와 동일 기준(분기 공시 주기)


def read_hyperscaler_capex():
    """sources/hyperscaler-capex.csv(scripts/sec_edgar_capex.py, SEC EDGAR XBRL)에서
    회사별 최신 분기 CapEx + 직전 분기 대비 QoQ%를 계산. 2026-08-06 신설 —
    HBM Cycle Score "고객재고" 축(10점, 지금까지 전적으로 어닝콜 논조 해석)에
    실측 CapEx 숫자를 보조 근거로 붙인다(축 자체를 자동채점하진 않음 — 논조
    판단은 여전히 사람/Claude 몫, 여기선 "숫자가 실제로 얼마였나"만 제공).

    ⚠ 2026-08-06 데이터 정합성 버그 발견·수정: SEC companyconcept API가 같은
    분기(end_date)를 서로 다른 fiscal_year/fiscal_period로 중복 보고하는
    경우가 있어(나중 필링의 "전년동기 비교치"로 재수록될 때) 예전 코드가
    이를 별개 분기처럼 저장했었다 — end_date 기준으로 재정리하도록 고쳤다
    (scripts/sec_edgar_capex.py 참고). 값 자체가 충돌하는 경우(MSFT 사례
    확인됨)는 CSV `note` 컬럼에 남겨두고 여기서도 그대로 노출한다 — 조용히
    하나를 버리지 않는다.
    스테일 판정: 최신 end_date가 오늘로부터 HYPERSCALER_CAPEX_STALE_DAYS일
    이상 지났으면 "확인됐지만 오래된 값"으로 명시 표기(최신인 것처럼 꾸미지
    않는다)."""
    if not HYPERSCALER_CAPEX_CSV_PATH.exists():
        return None
    with HYPERSCALER_CAPEX_CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return None

    by_ticker = {}
    for r in rows:
        by_ticker.setdefault(r["ticker"], []).append(r)

    today = datetime.now(KST).date()
    out = {}
    for ticker, company_rows in by_ticker.items():
        company_rows.sort(key=lambda r: r["end_date"])
        latest = company_rows[-1]
        end_date = datetime.strptime(latest["end_date"], "%Y-%m-%d").date()
        days_stale = (today - end_date).days
        qoq_pct = None
        if len(company_rows) >= 2:
            prev_val = float(company_rows[-2]["value_usd"])
            if prev_val:
                qoq_pct = (float(latest["value_usd"]) - prev_val) / prev_val * 100
        out[ticker] = {
            "company": latest["company"], "end_date": latest["end_date"],
            "value_usd": float(latest["value_usd"]), "qoq_pct": qoq_pct,
            "days_stale": days_stale, "is_stale": days_stale >= HYPERSCALER_CAPEX_STALE_DAYS,
            "note": latest.get("note", ""),
        }
    return out


def read_ai_periphery():
    """sources/ai-periphery-fundamentals.csv(scripts/sec_edgar_periphery.py 수집)에서
    변두리 기업별 최신 분기 매출·백로그와 직전분기 대비 증감을 계산.
    2026-08-07 신설 — wiki/concepts/ai-value-chain-periphery-monitor.md 운영지침 ⓐ.

    **이 섹션의 존재 이유**: HBM Cycle Score 6축은 전부 주도주(SK하이닉스)
    자신의 지표라 "주도주가 이미 흔들린 뒤"에야 신호가 뜬다. 백로그(이미
    계약된 미래 매출)는 주문이 끊길 때 **가장 먼저** 꺾이는 자리라 조기경보로
    쓴다 — 그래서 아래 판정에서 backlog 감소를 revenue 감소보다 무겁게 본다.

    데이터가 없으면 None(섹션 자체 생략) — 억지로 만들지 않는다."""
    if not AI_PERIPHERY_CSV_PATH.exists():
        return None
    with AI_PERIPHERY_CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return None

    series = {}
    for r in rows:
        series.setdefault((r["ticker"], r["metric"]), []).append(r)

    today = datetime.now(KST).date()
    out = {}
    for (tk, metric), rs in series.items():
        rs.sort(key=lambda r: r["end_date"])
        latest = rs[-1]
        qoq = None
        if len(rs) >= 2:
            prev = float(rs[-2]["value_usd"])
            if prev:
                qoq = (float(latest["value_usd"]) - prev) / prev * 100
        end_date = datetime.strptime(latest["end_date"], "%Y-%m-%d").date()
        days_stale = (today - end_date).days
        out.setdefault(tk, {"company": latest["company"], "layer": latest["layer"], "metrics": {}})
        out[tk]["metrics"][metric] = {
            "end_date": latest["end_date"], "value_usd": float(latest["value_usd"]),
            "qoq_pct": qoq, "days_stale": days_stale,
            "is_stale": days_stale >= AI_PERIPHERY_STALE_DAYS, "note": latest.get("note", ""),
        }
    return out
