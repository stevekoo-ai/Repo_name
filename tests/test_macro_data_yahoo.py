"""scripts/macro_data.py의 yahoo 프로바이더 — ICE 달러지수(DXY) 수집.

2026-09-18 신설. FRED DTWEXBGS(연준 26개국 무역가중)가 원천 발표 지연으로
7일씩 비는 걸 사용자가 지적("API가 안 주면 다른 데서라도 가져와야 할 거
아냐")한 데서 출발했다. 조사 결과 **같은 지표를 주는 다른 API는 없고**,
매일 나오는 ICE DXY는 6개 통화만 쓰는 다른 바스켓이라 대체가 아니라
병기로만 쓴다 — 이 파일은 그 계약을 고정한다.

소스는 추측이 아니라 GitHub Actions 프로브(run 35338679955)로 정했다:
stooq 5개 심볼은 전부 HTTP 200 + 자바스크립트 봇 차단 챌린지(순진하게
파싱하면 조용히 깨진다), yahoo DX-Y.NYB만 정상.
"""
import json
from datetime import date

import pytest

from scripts import macro_data as M


class _FakeResp:
    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _chart_payload(rows):
    """(epoch, close) 목록 → yahoo chart API 응답 모양."""
    return json.dumps({
        "chart": {
            "result": [{
                "timestamp": [ts for ts, _ in rows],
                "indicators": {"quote": [{"close": [c for _, c in rows]}]},
            }],
            "error": None,
        }
    }).encode()


def test_dxy_preset_is_registered_as_a_separate_series_not_a_replacement():
    """DTWEXBGS를 덮어쓰면 안 된다 — 둘은 다른 바스켓이라 같은 계열에
    섞이는 순간 시계열이 조용히 불연속이 된다."""
    assert "us_dollar_index_dxy" in M.PRESETS
    assert "us_dollar_index" in M.PRESETS, "기존 FRED 계열은 그대로 남아야 한다"
    provider, symbol, desc, _ = M.PRESETS["us_dollar_index_dxy"]
    assert provider == "yahoo"
    assert symbol == "DX-Y.NYB", "Actions 프로브에서 유일하게 성공한 심볼"
    assert "참고" in desc, "대체가 아니라 참고용이라는 게 설명에 남아야 한다"


def test_yahoo_fetch_converts_timestamps_to_utc_trading_dates(monkeypatch):
    rows = [(1789531200, 100.31), (1789617600, 100.22), (1789704000, 100.439)]
    monkeypatch.setattr(M.urllib.request, "urlopen",
                        lambda *a, **k: _FakeResp(_chart_payload(rows)))
    out = M.yahoo_fetch("DX-Y.NYB", "2026-09-10", "2026-09-18")
    assert [d for d, _ in out] == ["2026-09-16", "2026-09-17", "2026-09-18"]
    assert out[-1][1] == "100.4390"


def test_yahoo_fetch_skips_null_closes_instead_of_writing_zero(monkeypatch):
    """휴장일은 close=null로 온다 — 0으로 적으면 변화율이 폭주한다(R3:
    없는 값은 없다고 하지, 지어내지 않는다)."""
    rows = [(1789531200, 100.31), (1789617600, None), (1789704000, 100.44)]
    monkeypatch.setattr(M.urllib.request, "urlopen",
                        lambda *a, **k: _FakeResp(_chart_payload(rows)))
    out = M.yahoo_fetch("DX-Y.NYB")
    assert [d for d, _ in out] == ["2026-09-16", "2026-09-18"]


def test_yahoo_fetch_fails_loudly_when_the_body_is_a_bot_challenge(monkeypatch):
    """stooq가 정확히 이렇게 돌려줬다 — HTTP 200인데 본문은 차단 페이지.
    status만 믿고 넘어가면 '수집 성공인데 데이터가 안 는다'가 된다."""
    monkeypatch.setattr(M.urllib.request, "urlopen",
                        lambda *a, **k: _FakeResp(b"<!DOCTYPE html><html>bot check</html>"))
    with pytest.raises(SystemExit):
        M.yahoo_fetch("DX-Y.NYB")


def test_yahoo_fetch_fails_loudly_when_every_close_is_null(monkeypatch):
    monkeypatch.setattr(M.urllib.request, "urlopen",
                        lambda *a, **k: _FakeResp(_chart_payload([(1789531200, None)])))
    with pytest.raises(SystemExit):
        M.yahoo_fetch("DX-Y.NYB")


def test_sync_formats_yahoo_dates_like_fred_not_like_ecos():
    """cmd_sync가 provider별로 날짜 표기를 다르게 만든다 — yahoo가 ecos
    분기로 새면 `_, _, cycle = spec`에서 ValueError로 죽는다."""
    import inspect
    src = inspect.getsource(M.cmd_sync)
    assert 'provider in ("fred", "yahoo")' in src


def test_dxy_is_shown_in_the_briefing_fact_sheet_with_a_reference_label():
    """브리핑 표에 나와야 의미가 있고, 라벨에 '참고'가 있어야 DTWEXBGS와
    섞어 읽지 않는다."""
    from engine.briefing import context as C

    entry = [e for e in C.FACT_SERIES if e[0] == "us_dollar_index_dxy"]
    assert entry, "팩트시트에 DXY가 등록돼야 한다"
    assert "참고" in entry[0][1]
    assert any(e[0] == "us_dollar_index" for e in C.FACT_SERIES), "FRED 계열도 유지"
