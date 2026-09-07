"""BLS 미국 노동시장 + IMF 전망을 리포트용으로 읽어오는 모듈.

2026-09-07 신설. 두 소스 다 이날 새로 붙인 것이고(collectors/bls.py,
collectors/imf.py), 이 모듈은 **네트워크를 쓰지 않는다** — 주 1회
us-labor-outlook-sync.yml이 쌓아둔 data/normalized/ CSV만 읽는다.
리포트 파이프라인은 결정론적이어야 하고 수집 실패가 리포트를 막으면
안 되기 때문이다.

**왜 미국 노동시장이 이 리포트에 필요한가**: 이 저장소의 판단 사슬은
결국 두 갈래로 흐른다 —
  미국 고용·임금 → 연준 금리 경로 → 미 10년물 → 원/달러 → 하이닉스 외국인 수급
  미국 금리 → 한국 기준금리 → 주담대 금리 → 부동산 진입 판단
그 맨 앞단이 미국 고용·임금인데, 지금까지 CPI와 실업률 두 개로만 보고
있었다. 물가가 내려가도 **임금이 안 꺾이면 연준은 못 내린다** — 그 축이
빠져 있었다.

**IMF 전망을 쓰는 규칙**: IMF는 이 저장소에서 유일하게 미래 값을 주는
소스다. 실측(`imf_*.csv`)과 전망(`imf_*_forecast.csv`)은 수집 단계에서
이미 분리돼 있고, 이 모듈은 그 분리를 그대로 유지해 렌더러에 넘긴다.
리포트는 전망을 반드시 "전망"이라고 말해야 한다 — 실측인 척하면
R1(실측 우선)을 정면으로 어긴다.

**R4 준수**: 여기서 나오는 어떤 값도 매매 지시가 아니다. HOLD/BUY/SELL은
여전히 결정 엔진 하나만 낸다. 이 모듈은 근거만 제공한다.
"""
from __future__ import annotations

from collectors import base

# (정규화 계열 id, 표시 이름, 단위, 소수 자릿수)
_BLS_VIEW: list[tuple[str, str, str, int]] = [
    ("bls_us_avg_hourly_earnings", "시간당 평균임금", "달러", 2),
    ("bls_us_unemployment", "실업률", "%", 1),
    ("bls_us_job_openings", "JOLTS 구인건수", "천건", 0),
    ("bls_us_labor_participation", "경제활동참가율", "%", 1),
]

# IMF는 국가 비교가 핵심이라 지표 하나(성장률)를 4개국으로 나란히 본다.
_IMF_COUNTRIES: list[tuple[str, str]] = [
    ("kor", "한국"), ("usa", "미국"), ("chn", "중국"), ("jpn", "일본"),
]


def _latest_two(series_id: str) -> tuple[dict | None, dict | None]:
    """정규화 계열의 (최신, 직전) 행. 없으면 (None, None) — 값을 지어내지 않는다(R3)."""
    df = base.read_normalized(series_id)
    if df.empty:
        return None, None
    df = df.sort_values("date")
    rows = [{"date": str(r.date), "value": float(r.value)} for r in df.itertuples()]
    if len(rows) == 1:
        return rows[-1], None
    return rows[-1], rows[-2]


def build_us_labor() -> dict | None:
    """BLS 노동시장 지표 최신값 + 전월 대비. 데이터가 하나도 없으면 None."""
    items = []
    for series_id, label, unit, digits in _BLS_VIEW:
        latest, prev = _latest_two(series_id)
        if latest is None:
            continue   # 수집 안 된 항목은 생략 — "미수집"을 0으로 렌더하지 않는다
        change = None
        if prev is not None:
            change = latest["value"] - prev["value"]
        items.append({
            "label": label, "unit": unit, "digits": digits,
            "as_of": latest["date"], "value": latest["value"],
            "change": change,
        })
    if not items:
        return None
    return {"items": items, "as_of": max(i["as_of"] for i in items)}


def build_imf_outlook(series_key: str = "gdp_growth") -> dict | None:
    """4개국 실측 최신 + 전망 2년치. 실측과 전망을 섞지 않고 따로 담는다."""
    rows = []
    for code, name in _IMF_COUNTRIES:
        latest, _ = _latest_two(f"imf_{series_key}_{code}")
        if latest is None:
            continue
        fc_df = base.read_normalized(f"imf_{series_key}_{code}_forecast")
        forecast = []
        if not fc_df.empty:
            fc = fc_df.sort_values("date")
            forecast = [{"date": str(r.date), "value": float(r.value)} for r in fc.itertuples()][:2]
        rows.append({
            "country": name,
            "actual_year": latest["date"][:4],
            "actual": latest["value"],
            "forecast": forecast,
        })
    if not rows:
        return None
    return {"series_key": series_key, "rows": rows}
