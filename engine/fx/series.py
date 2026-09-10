"""FRS 전용 시계열 접근 계층 — **as_of 시점까지의 데이터만** 돌려준다.

## 왜 이 모듈이 따로 있나

FRS 설계의 최우선 제약이 "모든 점수 함수는 as_of를 받는다"이다
([설계](../../wiki/architecture/fx-regime-score-design.md) §1). 그 제약은
점수 함수가 아니라 **데이터를 읽는 지점**에서 지켜져야 한다 — 점수 함수가
아무리 as_of를 받아도 내부에서 "최신값"을 읽으면 look-ahead가 새어든다.
기존 CCI(`engine/crisis_analysis/scoring.py`)의 `_get_latest()`가 정확히 그
구조라 구조적으로 백테스트가 불가능했다. 여기서는 그 통로 자체를 막는다.

## 두 개의 저장소를 다 읽는다

2026-09-10에 이 저장소에 FRED 시리즈 레지스트리가 **두 벌** 있다는 걸
발견했다([분석](../../wiki/concepts/fx-episode-dollar-assets.md) §7):

- `collectors/*.py` → `data/normalized/<series_id>.csv` (미 10년물 1962~ 등 장기)
- `scripts/macro_data.py` PRESETS → `sources/macro-series.csv` (원/달러 2005~ 등)

같은 지표가 이름만 다르게 양쪽에 있고(`us_2y` vs `us_2y_treasury`), 어느 쪽이
더 긴지는 지표마다 다르다. 두 레지스트리를 통합하는 건 별도 작업이라, 이
계층이 **양쪽을 다 읽고 더 긴 쪽을 쓰도록** 흡수한다. 통합이 끝나면 이
모듈의 SOURCES 표만 지우면 된다.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

_REPO = Path(__file__).resolve().parents[2]
_NORMALIZED = _REPO / "data" / "normalized"
_MACRO_CSV = _REPO / "sources" / "macro-series.csv"

# 논리적 지표 이름 → (normalized series_id, macro-series.csv series 이름)
# 둘 다 있으면 합쳐서 더 긴 이력을 얻는다. 한쪽만 있으면 None.
SOURCES: dict[str, tuple[str | None, str | None]] = {
    "kr_base_rate":     ("ecos_base_rate", "kr_base_rate"),
    "kr_usdkrw":        ("ecos_usdkrw", "kr_usdkrw"),
    "kr_usdkrw_fred":   (None, "usd_krw_fred"),
    "kr_current_account": ("ecos_current_account", None),
    "kr_exports":       ("customs_export_dlr", None),
    "kr_semi_exports_yoy": ("motie_semiconductor_exports_yoy", None),
    "us_fed_funds":     ("fred_us_fed_funds_rate", "us_fed_funds"),
    "us_10y":           ("fred_us_10y_treasury", "us_10y"),
    "us_dollar_index":  ("fred_us_dollar_index", "us_dollar_index"),
    "us_brent":         (None, "us_brent"),
    # 2026-09-10 추가 — 리포트 §1.7-B "달러 자산 맥락"의 재료. 점수 계산엔
    # 안 쓰이고 사실 표기 전용이다(설계 §6.5.3 — 자산배분 점수는 만들지 않는다).
    # us_3m이 특히 중요하다: 과거 5개 국면 중 4개는 미국이 제로금리라
    # "환전 후 대기"가 무수익이었는데 지금은 아니라는 게 시대 차이의 핵심.
    "us_3m":            ("fred_us_3m_treasury", "us_3m"),
    "us_2y":            ("fred_us_2y_treasury", "us_2y"),
    "us_hy_oas":        ("fred_hy_oas", "us_hy_oas"),
    "us_vix":           (None, "us_vix"),
    "us_nasdaq":        (None, "us_nasdaq"),
}


@dataclass(frozen=True)
class Observation:
    date: date
    value: float


def _read_normalized(series_id: str) -> list[Observation]:
    path = _NORMALIZED / f"{series_id}.csv"
    if not path.exists():
        return []
    out: list[Observation] = []
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                out.append(Observation(date.fromisoformat(row["date"][:10]), float(row["value"])))
            except (ValueError, TypeError, KeyError):
                continue  # 빈 값·헤더 변형은 조용히 건너뛴다(R3: 없는 건 없는 것)
    return out


def _read_macro_csv(series_name: str) -> list[Observation]:
    if not _MACRO_CSV.exists():
        return []
    out: list[Observation] = []
    with _MACRO_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("series") != series_name:
                continue
            try:
                out.append(Observation(date.fromisoformat(row["date"][:10]), float(row["value"])))
            except (ValueError, TypeError, KeyError):
                continue
    return out


def _merge(primary: Iterable[Observation], secondary: Iterable[Observation]) -> list[Observation]:
    """같은 날짜가 양쪽에 있으면 primary(normalized)를 채택한다.

    normalized 쪽이 각 수집기의 정식 출력이라 R1(실측 우선)에서 더 가깝다.
    macro-series.csv는 이력을 넓히는 보조로만 쓴다."""
    merged: dict[date, float] = {o.date: o.value for o in secondary}
    merged.update({o.date: o.value for o in primary})
    return [Observation(d, merged[d]) for d in sorted(merged)]


_cache: dict[str, list[Observation]] = {}


def load_series(name: str) -> list[Observation]:
    """지표 전체 이력(날짜 오름차순). as_of 필터는 하지 않는다 — 내부용."""
    if name in _cache:
        return _cache[name]
    if name not in SOURCES:
        raise KeyError(f"알 수 없는 지표: {name} (engine/fx/series.py SOURCES 참조)")
    norm_id, macro_id = SOURCES[name]
    rows = _merge(
        _read_normalized(norm_id) if norm_id else [],
        _read_macro_csv(macro_id) if macro_id else [],
    )
    _cache[name] = rows
    return rows


def clear_cache() -> None:
    """테스트에서 파일을 바꿔가며 검증할 때 쓴다."""
    _cache.clear()


def series_as_of(name: str, as_of: date) -> list[Observation]:
    """**as_of 이하 날짜만** 돌려준다. FRS의 모든 데이터 접근은 여기를 통과한다.

    미래 데이터를 절대 흘리지 않는 게 이 함수의 유일한 계약이고,
    tests/test_fx_series.py가 그걸 고정한다."""
    return [o for o in load_series(name) if o.date <= as_of]


def latest_as_of(name: str, as_of: date, max_age_days: int | None = None):
    """as_of 시점에서 가장 최근 관측치. 없으면 None.

    max_age_days를 주면 그보다 오래된 값은 **None으로 떨어뜨린다** — 오래된
    값을 조용히 "최신"으로 쓰다가 사고가 났던 게 CCI의 실패 사례라
    (engine/crisis_analysis/scoring.py 117~122행 주석), 여기선 나이를
    명시적으로 다룬다. R3: 미수집은 판정이 아니다."""
    rows = series_as_of(name, as_of)
    if not rows:
        return None
    last = rows[-1]
    if max_age_days is not None and (as_of - last.date).days > max_age_days:
        return None
    return last


def value_as_of(name: str, as_of: date, max_age_days: int | None = None) -> float | None:
    obs = latest_as_of(name, as_of, max_age_days)
    return None if obs is None else obs.value


def value_n_months_before(name: str, as_of: date, months: int,
                          max_age_days: int | None = None) -> float | None:
    """as_of에서 months개월 전 시점의 값 — 모멘텀(방향) 계산용."""
    y, m = as_of.year, as_of.month - months
    while m <= 0:
        m += 12
        y -= 1
    day = min(as_of.day, 28)
    return value_as_of(name, date(y, m, day), max_age_days)


def monthly_last(name: str, as_of: date) -> list[tuple[str, float]]:
    """월말 마지막 관측치 [(YYYY-MM, value)] — 이동평균·추세 계산용."""
    out: dict[str, float] = {}
    for o in series_as_of(name, as_of):
        out[f"{o.date.year:04d}-{o.date.month:02d}"] = o.value
    return sorted(out.items())
