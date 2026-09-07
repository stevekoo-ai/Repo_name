"""US Bureau of Labor Statistics (BLS) collector — 미국 고용·물가 원천 데이터.

2026-09-07 신설. 배경: BLS_API_KEY가 daily-peos-report.yml과
monthly-peos-report.yml 두 워크플로에 주입되고 config/api.yaml에도 등록돼
있었는데, **저장소 전체에 이를 쓰는 코드가 한 줄도 없었다**. API 전수
프로브(scripts/api_probe.py)를 만들다 발견해서 실제로 채우는 모듈.

FRED와 겹치지 않나? 일부는 겹친다(CPI/실업률/비농업고용은 FRED에도 있고
FRED가 BLS를 미러링한다). 그래서 이 모듈은 **겹치는 걸 대체하려는 게 아니라
FRED가 잘 안 주는 축**에 집중한다:

- **시간당 평균임금(CES0500000003)** — 인플레이션의 지속성을 가르는 축.
  물가가 내려가도 임금이 안 꺾이면 연준은 못 내린다. 금리 경로 판단에
  직접 들어가는 값인데 지금 이 저장소엔 없다.
- **JOLTS 구인건수(JTS...JOL)** — 노동시장 타이트니스. 실업률은 후행하지만
  구인건수는 먼저 꺾인다.
- **경제활동참가율(LNS11300000)** — 실업률 하락이 '취업 증가'인지 '구직
  포기'인지 구분해준다. 실업률만 보면 두 경우가 똑같이 보인다.

왜 이게 이 저장소에 중요한가: 연준 금리 경로 → 미국 10년물 → 원/달러 →
SK하이닉스 외국인 수급, 그리고 한국 기준금리 → 부동산 대출금리로 이어지는
사슬의 **맨 앞단**이 미국 고용·임금이다. 지금은 그 맨 앞단을 CPI와 실업률
두 개로만 보고 있다.

인증: v2 API는 **키 없이도 동작한다**(일 25회 제한). 키가 있으면 일 500회로
올라간다 — 2026-09-07 프로브에서 키 없이 CPI-U 19개월치 수신 확인.
그래서 키가 없어도 PENDING으로 죽지 않고 그냥 호출한다(7.9의 "키 없으면
PENDING"은 키가 *필수*인 소스에 적용되는 규칙이다).

주의(실측): 응답의 period 필드는 "M01"~"M12"가 월이고 **"M13"은 연평균**이다.
이걸 안 거르면 매년 12월 뒤에 엉뚱한 13번째 데이터포인트가 끼어 시계열이
오염된다.
"""
from __future__ import annotations

from datetime import date, datetime

import requests

from core import cache as cache_mod
from core.config import api_config, get_api_key
from core.logger import log_event
from core.models import DataPoint, DataStatus, Frequency, Metadata
from . import base

_HISTORY_YEARS = 10   # BLS v2는 요청당 최대 20년 — 10년이면 충분하고 응답도 가볍다
_TIMEOUT_SECONDS = 20

# series_key -> (BLS series_id, 설명, 단위)
# series_id는 BLS 공식 문서의 표준 ID. 바꾸려면 여기만 고치면 된다(24.1 모듈성).
BLS_SERIES: dict[str, tuple[str, str, str]] = {
    # FRED와 겹치지만 원천이라 발표가 더 빠른 것들 — 교차검증용
    "us_cpi_all": ("CUUR0000SA0", "소비자물가지수 CPI-U 전체(도시)", "1982-84=100"),
    "us_cpi_core": ("CUUR0000SA0L1E", "근원 CPI(식품·에너지 제외)", "1982-84=100"),
    "us_unemployment": ("LNS14000000", "실업률(계절조정)", "%"),
    "us_nonfarm_payroll": ("CES0000000001", "비농업부문 총고용", "천명"),

    # FRED가 잘 안 주는 축 — 이 모듈의 존재 이유
    "us_avg_hourly_earnings": ("CES0500000003", "민간 시간당 평균임금", "달러"),
    "us_labor_participation": ("LNS11300000", "경제활동참가율", "%"),
    "us_job_openings": ("JTS000000000000000JOL", "JOLTS 구인건수", "천건"),
    "us_ppi_final_demand": ("WPUFD4", "생산자물가 최종수요", "index"),
}


def _period_to_date(year: str, period: str) -> date | None:
    """BLS의 (year, period)를 날짜로. period "M13"(연평균)은 월 시계열이 아니므로 None."""
    if not period.startswith("M") or period == "M13":
        return None
    try:
        return date(int(year), int(period[1:]), 1)
    except ValueError:
        return None


def _fetch_raw(series_ids: list[str], api_key: str | None) -> dict:
    """BLS v2 시계열 조회. 한 번에 여러 series_id를 보낼 수 있어 호출 수를 아낀다
    (키 없이 일 25회 제한이라 이게 중요하다)."""
    url = api_config()["sources"]["bls"]["base_url"]
    today = datetime.utcnow()
    body: dict = {
        "seriesid": series_ids,
        "startyear": str(today.year - _HISTORY_YEARS),
        "endyear": str(today.year),
    }
    if api_key:
        body["registrationkey"] = api_key

    resp = requests.post(url, json=body, timeout=_TIMEOUT_SECONDS)
    base.raise_for_status(resp)
    payload = resp.json()
    status = payload.get("status")
    if status != "REQUEST_SUCCEEDED":
        # BLS는 한도 초과·잘못된 series_id를 200 OK에 실어 보낸다 — 상태 필드를
        # 확인하지 않으면 조용히 빈 결과가 되어 흘러간다.
        msgs = "; ".join(payload.get("message", [])) or "(메시지 없음)"
        raise RuntimeError(f"BLS 요청 실패 status={status}: {msgs}")
    return payload


def _rows_for(payload: dict, series_id: str) -> list[dict]:
    """응답에서 한 series_id의 (date, value) 행들을 날짜 오름차순으로."""
    for series in payload.get("Results", {}).get("series", []):
        if series.get("seriesID") != series_id:
            continue
        rows = []
        for d in series.get("data", []):
            dt = _period_to_date(d.get("year", ""), d.get("period", ""))
            if dt is None:
                continue
            try:
                value = float(d["value"])
            except (KeyError, ValueError, TypeError):
                continue
            rows.append({"date": dt.strftime("%Y-%m-%d"), "value": value})
        # BLS는 최신순으로 준다 — 이 저장소의 normalized는 날짜 오름차순이 관례.
        return sorted(rows, key=lambda r: r["date"])
    return []


def fetch_series(series_key: str) -> DataPoint:
    """BLS 시리즈 하나를 가져와 raw+normalized에 저장하고 최신 DataPoint를 반환."""
    series_id, label, unit = BLS_SERIES[series_key]
    api_key = get_api_key("bls")   # 없어도 됨 — v2는 키리스로 동작(일 25회)
    ttl = api_config()["cache_ttl_seconds"]["monthly_macro"]

    cached = cache_mod.get(f"bls:{series_id}", ttl)
    rows = cached
    if rows is None:
        payload = base.retry(lambda: _fetch_raw([series_id], api_key),
                             label=f"bls:{series_key}", attempts=2, backoff_seconds=2.0)
        rows = _rows_for(payload, series_id) if payload else None
        if rows:
            cache_mod.set(f"bls:{series_id}", rows)

    if not rows:
        stale = cache_mod.get_stale(f"bls:{series_id}")
        if stale:
            rows = stale
            log_event("collector.bls_served_stale", level="warning", series=series_key)
        else:
            return DataPoint(series_id=series_key, status=DataStatus.SOURCE_ERROR,
                             note=f"BLS 응답 없음, 캐시도 없음 ({label})")

    base.write_raw("bls", series_key, rows[-24:])
    base.append_normalized(f"bls_{series_key}", rows)

    latest = rows[-1]
    metadata = Metadata(
        source="US BLS",
        unit=unit,
        frequency=Frequency.MONTHLY,
        reliability_grade=5,
        official=True,
        reference_date=date.fromisoformat(latest["date"]),
        confidence=95.0,
    )
    return DataPoint(series_id=series_key, status=DataStatus.OK,
                     value=float(latest["value"]), metadata=metadata)


def fetch_all() -> dict[str, DataPoint]:
    """전체 시리즈를 **한 번의 호출로** 받아 나눠 담는다.

    fetch_series를 8번 부르면 호출도 8번이라 키리스 일 25회 한도를 금방
    태운다. BLS v2는 한 요청에 여러 series_id를 받으므로 한 번에 받는 게
    맞다 — 이게 이 함수가 fetch_series 반복이 아닌 이유.
    """
    api_key = get_api_key("bls")
    series_ids = [sid for sid, _, _ in BLS_SERIES.values()]
    payload = base.retry(lambda: _fetch_raw(series_ids, api_key),
                         label="bls:fetch_all", attempts=2, backoff_seconds=2.0)

    out: dict[str, DataPoint] = {}
    for series_key, (series_id, label, unit) in BLS_SERIES.items():
        rows = _rows_for(payload, series_id) if payload else []
        if not rows:
            out[series_key] = DataPoint(series_id=series_key, status=DataStatus.SOURCE_ERROR,
                                        note=f"BLS 응답에 {series_id} 없음 ({label})")
            continue
        cache_mod.set(f"bls:{series_id}", rows)
        base.write_raw("bls", series_key, rows[-24:])
        base.append_normalized(f"bls_{series_key}", rows)
        latest = rows[-1]
        out[series_key] = DataPoint(
            series_id=series_key, status=DataStatus.OK, value=float(latest["value"]),
            metadata=Metadata(source="US BLS", unit=unit, frequency=Frequency.MONTHLY,
                              reliability_grade=5, official=True,
                              reference_date=date.fromisoformat(latest["date"]), confidence=95.0),
        )
    return out
