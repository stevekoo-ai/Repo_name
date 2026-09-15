"""collectors/kosis.py 재시도 설정 + scripts/collect_core10.py KOSIS_KEYS.

2026-09-15 실제 GitHub Actions job 로그에서 core10-collect.yml의 KOSIS
4개 호출이 매번 connect timeout(10초, 재시도 2회)으로 죽는 걸 확인했다
— kosis.py 자체 docstring이 이미 "kosis.kr 연결이 간헐적으로 불안정
하다"고 적어뒀던 것과 일치. timeout 10→20초, attempts 2→4로 늘렸다.

같은 조사에서 kosis_semiconductor_shipment_index·
kosis_semiconductor_inventory_index가 고아 호출 경로(daily-peos-report.yml
삭제로 끊김)였다는 것도 발견 — collect_core10.py::KOSIS_KEYS에 추가해
기존 일일 스케줄에 태웠다.
"""
import inspect

from collectors import kosis
from scripts import collect_core10


def test_kosis_fetch_timeout_is_at_least_20_seconds():
    src = inspect.getsource(kosis._fetch_table)
    assert "timeout: int = 20" in src, (
        "10초 기본값으로 되돌아갔다 — kosis.kr은 20초짜리 timeout도 겪은 "
        "적이 있다고 이 파일 자신의 docstring이 기록해뒀다"
    )


def test_kosis_fetch_series_retries_at_least_four_times():
    src = inspect.getsource(kosis.fetch_series)
    assert "attempts=4" in src, "실측 connect timeout을 2회 재시도로는 못 넘긴다"


def test_semiconductor_kosis_keys_are_registered_in_core10():
    """이 두 시리즈는 daily-peos-report.yml 삭제로 호출 경로를 잃었던
    고아였다 — collect_core10.py의 일일 스케줄에 다시 연결됐는지 고정."""
    assert "semiconductor_shipment_index" in collect_core10.KOSIS_KEYS
    assert "semiconductor_inventory_index" in collect_core10.KOSIS_KEYS


def test_all_core10_kosis_keys_have_a_real_series_spec():
    """등록만 해놓고 실제 collectors.kosis.KOSIS_SERIES에 좌표가 없으면
    매번 KeyError로 죽는다 — us-labor-outlook을 RUN_LOG로 잘못 등록했던
    사고와 같은 계열의 자기검증."""
    for key in collect_core10.KOSIS_KEYS:
        assert key in kosis.KOSIS_SERIES, f"KOSIS_SERIES에 '{key}' 좌표가 없다"
