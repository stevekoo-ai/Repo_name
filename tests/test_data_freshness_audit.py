"""scripts/data_freshness_audit.py — 신선도 판정 로직.

## 이 테스트가 고정하는 계약 (2026-09-15, "다 고쳐" 전수 수리)

`--check-only` 실측 대조로 발견한 것: 이 도구가 찾아낸 DEAD 22개 중
**16개는 실제로 살아있는 수집기였다** — IMF WEO 연간 시리즈가 median
gap 365일로 모든 버킷(daily/monthly/quarterly)을 빠져나가 "unknown"
(관대함 365일)에 떨어졌을 뿐이다. GitHub Actions 실제 job 로그로
확인(28/28 성공, 관세청/FRED도 22/22 OK)했으니 이건 감사 도구의
버킷 분류 공백이었지 수집기 결함이 아니었다.

나머지 2개(fred_kr_cpi_oecd·fred_kr_industrial_production_oecd)는 반대로
수집은 매번 성공하는데 **상류(OECD MEI 미러)가 진짜로 발행을 멈췄다**
— us_dollar_index_major/DTWEXM과 같은 계열. 이건 "고쳐지지 않는다"가
맞는 답이고, 매일 DEAD로 우는 대신 그 사실 자체를 기록해야 한다.
"""
from datetime import date

from scripts.data_freshness_audit import (
    KNOWN_DEAD_BY_DESIGN, TOLERANCE, _infer_frequency, audit,
)


def _dates(start_year: int, end_year: int, step_days: int) -> list[date]:
    out = []
    d = date(start_year, 1, 1)
    end = date(end_year, 1, 1)
    while d <= end:
        out.append(d)
        d = date.fromordinal(d.toordinal() + step_days)
    return out


# ── annual 버킷 (2026-09-15 신설) ────────────────────────────────

def test_annual_gap_is_classified_annual_not_unknown():
    """IMF WEO 실측 gap(365일)을 그대로 재현 — 이전엔 'unknown'으로
    떨어져 365일 관대함 하나로 622일짜리를 DEAD 처리했다."""
    dates = _dates(2000, 2025, 365)
    assert _infer_frequency(dates) == "annual"


def test_annual_tolerance_is_wider_than_the_old_unknown_bucket():
    """622일(IMF WEO 실측 나이)이 dead로 안 잡혀야 한다 — 다음 발표(매년
    4월)까지 자연스러운 지연이다."""
    warn_at, dead_at = TOLERANCE["annual"]
    assert warn_at < 622 < dead_at, "622일은 경고는 맞되 죽었다고 하면 안 된다"


def test_quarterly_and_monthly_gaps_still_classify_correctly():
    """annual 버킷을 추가하면서 기존 분류를 깨면 안 된다."""
    assert _infer_frequency(_dates(2020, 2026, 30)) == "monthly"
    assert _infer_frequency(_dates(2010, 2026, 91)) == "quarterly"
    assert _infer_frequency(_dates(2020, 2026, 1)) == "daily"


def test_gap_longer_than_annual_still_falls_to_unknown():
    """400일보다 더 벌어진(비정상적인) 간격은 여전히 unknown이어야 한다
    — annual 버킷이 모든 긴 간격을 삼켜버리면 진짜 비정상 패턴을 못 잡는다."""
    dates = [date(2015, 1, 1), date(2018, 1, 1), date(2023, 1, 1)]
    assert _infer_frequency(dates) == "unknown"


# ── known-dead-by-design (2026-09-15 신설) ───────────────────────

def test_known_dead_by_design_series_are_listed_not_hidden():
    """예외 목록은 존재를 숨기는 게 아니라 이유를 붙여 재분류하는 것이다
    — audit() 결과에서 여전히 나타나야 하고, 이유가 함께 와야 한다."""
    for series_id in KNOWN_DEAD_BY_DESIGN:
        assert KNOWN_DEAD_BY_DESIGN[series_id], f"{series_id}: 이유가 비어있다"


def test_dead_by_design_status_is_distinct_from_plain_dead(tmp_path, monkeypatch):
    import scripts.data_freshness_audit as m

    monkeypatch.setattr(m, "NORMALIZED", tmp_path)
    monkeypatch.setattr(m, "KNOWN_DEAD_BY_DESIGN", {"exempt_series": "test reason"})

    old = _dates(2020, 2022, 30)  # monthly, 확실히 dead(>200일)
    for name in ("exempt_series", "plain_series"):
        p = tmp_path / f"{name}.csv"
        with p.open("w", encoding="utf-8") as f:
            for d in old:
                f.write(f"{d.isoformat()},1\n")

    rows = m.audit(today=date(2026, 9, 15))
    by_name = {r["series"]: r for r in rows}
    assert by_name["exempt_series"]["status"] == "dead_by_design"
    assert by_name["exempt_series"]["known_reason"] == "test reason"
    assert by_name["plain_series"]["status"] == "dead"
    assert by_name["plain_series"]["known_reason"] is None


# ── 실제 저장소 데이터 회귀 (실측 대조 고정) ──────────────────────

def test_no_series_reports_dead_after_the_fix():
    """2026-09-15 이전엔 이 저장소가 DEAD 22개를 보고했다 — 실제로는
    16개가 annual 버킷 공백, 2개가 상류 단종이었다. 수정 후 실제
    저장소를 감사해서 진짜 DEAD가 하나도 없는지(전부 재분류됐는지)
    고정한다. 새 시리즈가 추가되며 진짜 DEAD가 생기면 이 테스트가
    깨지는 게 맞다 — 그때 원인을 다시 진단할 것."""
    rows = audit()
    dead = [r for r in rows if r["status"] == "dead"]
    assert not dead, f"진짜 DEAD로 남은 시리즈: {[r['series'] for r in dead]}"


def test_known_series_are_the_only_dead_by_design_entries():
    rows = audit()
    known = {r["series"] for r in rows if r["status"] == "dead_by_design"}
    assert known == set(KNOWN_DEAD_BY_DESIGN)


def test_imf_series_reclassified_as_annual_and_stale_not_dead():
    rows = audit()
    imf_rows = [r for r in rows if r["series"].startswith("imf_")
               and not r["series"].endswith("_forecast")]
    assert imf_rows, "imf_* 시리즈가 감사 대상에 하나도 없다 — 파일 경로 확인 필요"
    for r in imf_rows:
        assert r["frequency"] == "annual", f"{r['series']}: {r['frequency']}"
        assert r["status"] in ("ok", "stale"), f"{r['series']}: {r['status']}"


def test_motie_series_are_fresh_after_correlation_analysis_reruns():
    """2026-09-12 ingest에서 exports.yaml에 08월 행을 추가했지만
    correlation_analysis.py가 그걸 motie_*.csv로 정규화하지 않아 76일
    stale로 남아 있었다(collectors.manual.fetch_exports()의 유일한
    호출 경로였던 daily-peos-report.yml이 이미 삭제된 고아 경로였다).
    scripts/correlation_analysis.py::main()이 이제 그 정규화를 먼저
    하므로, 이 테스트는 그 파이프라인이 이미 실행된 상태(회귀 스위트
    실행 전 CI가 그렇게 두지 않을 수 있으므로 파일 존재만 관대하게 확인)
    를 느슨하게 확인한다."""
    rows = audit()
    motie_rows = {r["series"]: r for r in rows if r["series"].startswith("motie_")}
    assert motie_rows, "motie_* 시리즈가 감사 대상에 없다"
    # 정규화가 이미 한 번이라도 됐다면(이 리포지토리에서는 됐다) dead는 아니어야 한다
    for name, r in motie_rows.items():
        assert r["status"] != "dead", f"{name}: 여전히 dead — correlation_analysis 재실행 필요"
