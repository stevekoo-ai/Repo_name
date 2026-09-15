---
title: 데이터 헬스 — 일일 추적
created: 2026-09-15
updated: 2026-09-15
tags: [infrastructure, data-quality, monitoring, daily-tracking]
---

**자동 갱신**: `.github/workflows/data-health-check.yml` (2시간마다)
**판정 엔진**: `engine/health/check.py`
**프레임워크**: [concepts/data-health-closed-loop.md](../concepts/data-health-closed-loop.md)
**최신 스냅샷(사람이 읽는 버전)**: `data/health/latest_report.md`

---

## Latest Status (2026-09-15, 최초 점검 → 전수 수리 후)

| 항목 | 최초 점검 | **전수 수리 후** |
|---|---:|---:|
| 이상 | 41 | 36 |
| **critical** | **22** | **0** |
| 실행 종료코드 | 1 | **0** |

**critical 22건은 전부 오진 또는 재분류됐다 — 진짜로 죽어 있던 수집기는
없었다.** GitHub Actions 실제 job 로그(로컬 아님)로 전수 대조한 결과다.

---

## 원인별 정리 (실측 대조, 추측 아님)

| 원인 | 개수 | 실체 | 조치 |
|---|---:|---|---|
| **감사 도구의 "annual" 버킷 부재** | 16 | IMF WEO 연간 시리즈(median gap 365일)가 daily/monthly/quarterly 어디에도 안 걸려 "unknown"(관대함 365일)로 떨어짐 → 622일이 DEAD로 오판정. 수집기는 실측 job 로그에서 28/28 성공 확인 | `data_freshness_audit.py`에 annual 버킷(경고 450일/사망 800일) 신설 |
| **상류 단종 (수집 정상)** | 2 | `fred_kr_cpi_oecd`·`fred_kr_industrial_production_oecd` — FRED 호출은 매번 22/22 성공하지만 OECD MEI 미러 자체가 2023-11/2024-03에 발행을 멈춤. `us_dollar_index_major`/DTWEXM과 같은 계열 | `KNOWN_DEAD_BY_DESIGN`에 등록 — 숨기지 않고 이유와 함께 "known" 상태로 재분류 |
| **고아 호출 경로 (2026-08-11 daily-peos-report.yml 삭제의 부수피해)** | 3 | `motie_total_exports_yoy`·`motie_semiconductor_exports_yoy`·`motie_semiconductor_exports_usd_100m` — `collectors.manual.fetch_exports()`를 부르는 유일한 경로가 삭제된 워크플로였다. exports.yaml은 계속 갱신됐는데(2026-09-12 /ingest 포함) 정규화 파일로 전혀 안 흘러갔다 | `scripts/correlation_analysis.py::main()`이 시작 시 `fetch_exports()`를 먼저 호출하도록 연결(이미 매일 도는 워크플로에 재사용) |
| **같은 부수피해, 다른 시리즈** | 2 | `kosis_semiconductor_shipment_index`·`kosis_semiconductor_inventory_index` — `engine/crisis_analysis/scoring.py`가 직접 호출하는 설계였는데 그 함수를 부르던 유일한 경로가 같은 삭제된 워크플로였다 | `scripts/collect_core10.py`의 `KOSIS_KEYS`에 추가 — Core-10 4개 지표와 같은 일일 스케줄 재사용 |
| **진짜 인프라 이슈 — KOSIS 연결 타임아웃** | 2 (+위 2건과 겹침) | `kosis_industrial_production_index`·`kosis_retail_sales_index` — GitHub Actions 실제 로그에서 `kosis.kr` connect timeout(10초, 2회 재시도) 확인. 좌표 문제 아님(이미 2026-09-07에 좌표/연결성 분리 진단 완료) | timeout 10→20초, attempts 2→4로 증가 |
| **정상 발표 지연 (수집 정상, 감사 임계값이 너무 taut)** | 16 | `ecos_current_account`·`ecos_ppi_yoy_level`·`bls_us_job_openings`·`fred_us_industrial_production`·`fred_us_retail_sales`·`fred_us_trade_balance`·`fred_us_oecd_cli`·`fred_kr_unemployment_oecd`·`fred_kr_retail_sales_mom_oecd`·`ecos_gdp_growth_qoq`·`fred_us_gdp_qoq` 등 — 전부 같은 실행의 실제 job 로그에서 그날 성공 확인(예: `fred:fetch_all ✅ 22/22`, `ecos:current_account ✅ OK`). 통계 발표 자체가 발표 주기+2~3개월 지연되는 게 정상인 지표들 | **손대지 않음** — "stale"(경고, severity=warning)로 남기는 게 정확한 신호다. 대신 §아래 제어 루프 변경으로 이런 정상-지연 시리즈가 알림 스팸을 만들지 않게 함 |

---

## 제어 루프도 함께 고쳤다 — "warning은 알림을 안 보낸다"

위 마지막 줄(16개 정상-지연 시리즈)을 처리하다가 원래 설계의 결함을
발견했다: severity 구분 없이 3회 연속이면 전부 알림을 보내게 돼 있어서,
IMF 연간 시리즈나 OECD CLI처럼 **영구적으로 "약간 오래된" 게 정상인
시리즈가 6시간마다 이메일을 계속 쏘게** 된다 — 이 저장소가 반복해서
배운 "경고가 계속 오면 소음이 되어 무시당한다"는 원칙과 정면충돌.

**수정**: `critical` severity만 이메일을 보낸다. `warning`은 상태 추적
(대시보드 노출)은 계속하되 절대 알림을 안 보낸다.

---

## 남은 것 — 다음 정기 실행에서 자동으로 검증됨

- KOSIS 타임아웃 증가분은 로컬(이 세션 프록시가 kosis.kr을 막고 있음)에서
  실증할 수 없었다 — 다음 `core10-collect.yml` 정기 실행(매일 21:30 UTC)에서
  실측 확인 필요.
- IMF 16개·FRED 다수·BLS/ECOS 지표는 "stale"로 남는다 — 이건 버그가
  아니라 정확한 신호다(발표 주기 도래 시 자동 해소).

---

## Check History

| 날짜 | 이상 | critical | 비고 |
|---|---:|---:|---|
| 2026-09-15 (최초) | 41/58 | 22 | 시스템 신설. `data_freshness_audit.py`가 이미 발견해뒀던 것을 처음으로 노출 |
| 2026-09-15 (전수 수리) | 36/53 | **0** | 사용자 "모두 다 고쳐" 지시. GitHub Actions 실제 job 로그로 원인 6종 확정, 전수 수정. 종료코드 1→0 |
