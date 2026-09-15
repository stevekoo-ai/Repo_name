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

## Latest Status (2026-09-15, 최초 점검)

| 항목 | 값 |
|---|---:|
| 전체 소스 | 58개 (점 소스 18 + 정규화 스윕 40건 이상 항목 + 요약 1) |
| 이상 | 41개 |
| **critical** | **22개** (전부 `data/normalized/*.csv` 장기 미갱신) |
| warning | 19개 |

### 최초 점검에서 발견된 것 — 전부 사전 존재, 이번에 처음 가시화됨

`scripts/data_freshness_audit.py`는 이미 있었지만 결과가 GitHub Actions
로그의 `::warning::` 한 줄로만 남고 있었다(아무도 안 읽음). 이 시스템이
그 결과를 처음으로 리포트·브리핑에 노출시켰다.

| 등급 | 개수 | 예시 |
|---|---:|---|
| DEAD (critical) | 22 | `imf_current_account_*`(4종, 622일), `fred_kr_cpi_oecd`(1,049일), `fred_kr_industrial_production_oecd`(928일) |
| stale (warning) | 18 | `motie_semiconductor_exports_*`(76일 — 직전 /ingest에서 `exports.yaml`은 갱신했으나 `correlation_analysis.py` 재실행 전이라 정규화본은 아직 반영 전), `kosis_*`(76일) |

**점 소스 18개는 전부 정상**이었다(macro-series, 하이닉스 시세·수급,
포트폴리오, SEC EDGAR CapEx, 부동산 실거래, 청약 모니터, 일일 리포트).

---

## 다음 확인할 것

1. `imf_*` 4종(622일)과 `fred_kr_cpi_oecd`(1,049일) — 원인 진단
   (`data_freshness_audit.py`가 제안하는 순서: ①시리즈 스펙 대조
   ②페이지네이션 절단 ③워크플로가 default 브랜치에 살아있는지)
2. `motie_*`/`kosis_*` 18건 — 다음 `exports-price-correlation.yml`
   정기 실행이 자동으로 따라잡는지 확인
3. 알림 임계(3회 연속, 약 4~6시간) 첫 실발동 확인

---

## Check History

| 날짜 | 이상 | critical | 비고 |
|---|---:|---:|---|
| 2026-09-15 | 41/58 | 22 | 시스템 신설. 기준선 기록 — `scripts/data_freshness_audit.py`가 이미 발견해뒀던 것을 처음으로 노출 |
