"""오피스텔 매매 실거래가 트렌드 — collectors/molit_officetel.py 집계 결과를 읽어 계산.

구조는 engine/real_estate/market_trend.py(아파트 매매)와 동일 — market_trend.compute_sale_trend
공용 함수를 collectors/molit_officetel.py로만 바인딩한 얇은 래퍼.
"""
from __future__ import annotations

from collectors import molit_officetel
from . import market_trend


def compute_officetel_trend() -> dict:
    return market_trend.compute_sale_trend(molit_officetel.fetch_and_store, molit_officetel.SERIES_PREFIX)
