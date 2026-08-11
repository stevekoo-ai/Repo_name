---
title: 자동화 인프라 — GitHub Actions 워크플로우 & 시크릿 인벤토리
created: 2026-07-31
updated: 2026-08-09
tags: [infrastructure, secrets, github-actions, automation, real-estate]
---

이 저장소(`stevekoo-ai/Repo_name`)에는 데이터 수집/모니터링 GitHub
Actions 워크플로우들이 돌아간다. 새 세션이 매번 로그를 뒤져 재구성하지
않도록, 여기 한 페이지에 "무엇이 있고 어떤 시크릿을 쓰는지"만 정리한다.
**시크릿 값은 GitHub이 절대 다시 보여주지 않는다** — Settings → Secrets
화면은 이름만 표시하고, 소유자 본인도 값을 조회할 수 없다(write-only).
이 페이지도 이름과 용도만 기록하고 값은 어디에도 적지 않는다.

> 아래는 **데이터 수집/모니터링** 워크플로우만 기록한다. 보고서는
> 로컬에서 HTML로 생성하며 GitHub로 전송하지 않는다.

## 워크플로우 목록 (데이터 수집/모니터링만)

| 워크플로우 파일 | 주기 | 시스템 | 사용 시크릿 |
| --- | --- | --- | --- |
| `macro-data-sync.yml` | 매일 07:10 KST | SK하이닉스 모니터링 | `FRED_API_KEY`, `ECOS_API_KEY` |
| **`real-estate-sync.yml`** | **매일 03:00 KST** | **PEOS 부동산 모니터링** | **`DATA_GO_KR_KEY`** |
| `portfolio-holdings-sync.yml` | 매일 19:10 KST | SK하이닉스 모니터링 | `KIS_APP_KEY`(+`_ISP`/`_IRP` 계좌별 오버라이드), `KIS_APP_SECRET`(+`_ISP`/`_IRP`), `KIS_ACCOUNT_GEN`/`_ISP`/`_DC`/`_IRP` |
| `subscription-monitor.yml` | 5분마다 | SK하이닉스 모니터링(청약 알림) | `DATA_GO_KR_KEY`, `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD` |
| `subscription-schema-probe.yml` | 수동 | SK하이닉스 모니터링 | `DATA_GO_KR_KEY` |
| `ecos-lookup.yml` / `kosis-lookup.yml` | 수동 | 공용 유틸(통계표 코드 조회) | `ECOS_API_KEY` / `KOSIS_API_KEY` |
| `network-diagnostic.yml` | 수동 | 진단용 | 없음 |

## 시크릿 인벤토리 (이름 + 용도만 — 값 없음)

**데이터 수집용 API 키**
- `DATA_GO_KR_KEY` — data.go.kr 공공데이터포털 통합 인증키. [`collectors/molit.py`](../../collectors/molit.py)(국토부 아파트 실거래가)와 청약 모니터링 양쪽에서 재사용. ⚠ data.go.kr은 활용신청이 **API 상품 단위**라 같은 키라도 상품별 별도 승인이 필요 — 승인 안 된 상품 호출 시 JSON이 아닌 XML 에러 응답이 온다([`collectors/molit.py`](../../collectors/molit.py)의 `_fetch_region_month` 참고).
- `ECOS_API_KEY` — 한국은행 ECOS API 키.
- `KOSIS_API_KEY` — 국가통계포털(KOSIS) API 키.
- `FRED_API_KEY` — 세인트루이스 연은 FRED API 키 (미국 지표 + OECD 경유 한국 지표 폴백).
- `BLS_API_KEY` — 미국 노동통계국(BLS) API 키.

**한국투자증권(KIS) 브로커리지 API** — 실계좌 연동, [나의 투자 포트폴리오](my-portfolio.md) 참고
- `KIS_APP_KEY` / `KIS_APP_SECRET` — 기본 앱키(GEN/일반 계좌용, 시세조회 공용).
- `KIS_APP_KEY_ISP` / `KIS_APP_SECRET_ISP` — ISA 계좌 전용 앱키.
- `KIS_APP_KEY_IRP` / `KIS_APP_SECRET_IRP` — IRP 계좌 전용 앱키.
- `KIS_ACCOUNT_GEN` / `KIS_ACCOUNT_ISP` / `KIS_ACCOUNT_DC` / `KIS_ACCOUNT_IRP` — 계좌별 "CANO,상품코드" 형식 계좌번호.
- 🔴 핵심 제약: KIS 앱키는 **계좌번호 단위로 발급**된다 — 계좌마다 전용 앱키가 없으면 "output1 없음" 에러가 난다(자세한 경위는 [나의 투자 포트폴리오](my-portfolio.md) 참고). DC(퇴직연금) 계좌는 API 자체가 공식 미지원.

**알림 발송 (청약 모니터만 사용 — 유지 대상)**
- `GMAIL_ADDRESS` / `GMAIL_APP_PASSWORD` — `subscription-monitor.yml`(청약 알림)이 사용하는 알림 메일 발신용 Gmail 계정(앱 비밀번호 인증).
- `GITHUB_TOKEN` — 청약 알림에서 GitHub Issue 자동 생성용(워크플로우 기본 제공 토큰, 별도 등록 불필요).

## `real-estate-sync.yml` (2026-08-09 신규 추가)

MOLIT(국토교통부) 부동산 실거래가 데이터 자동 수집. 다음 4개 카테고리 매일 자동 수집:

- **아파트 매매 실거래가** (`collectors.molit.fetch_and_store()`)
  - 저장 위치: `data/normalized/molit_*.csv`, `sources/molit_apartment_*.csv`
  - 지표: 월 중 위치별 중간거래가(만원/평), 거래건수

- **아파트 전월세(전세+월세)** (`collectors.molit_rent.fetch_and_store()`)
  - 저장 위치: `data/normalized/molit_rent_*.csv`, `sources/molit_rent_*.csv`
  - 지표: 월 중 위치별 중간거래가, 거래건수

- **연립다세대/빌라 매매** (`collectors.molit_villa.fetch_and_store()`)
  - 저장 위치: `data/normalized/molit_villa_*.csv`, `sources/molit_villa_*.csv`

- **오피스텔 매매** (`collectors.molit_officetel.fetch_and_store()`)
  - 저장 위치: `data/normalized/molit_officetel_*.csv`, `sources/molit_officetel_*.csv`

**스케줄:** 매일 03:00 KST(18:00 UTC) — MOLIT 데이터는 당월 또는 이전월 기준 누적이므로 매일 체크 필요
**git 처리:** 데이터 변경 시 자동 commit+push, push 충돌 시 rebase 재시도(5회 지수백오프)
**데이터 검증:** CSV 파일 존재 및 형식 확인 스텝 포함 → 수집 성공/실패 자동 로깅

**핵심 제약:** data.go.kr은 활용신청이 API 상품 단위이므로, 각 4개 MOLIT 상품(매매/전월세/빌라/오피스텔)이 별도 승인되어야 한다. 승인 안 된 상품 호출 시 XML 에러 응답이 온다([`collectors/molit.py`](../../collectors/molit.py) 참고).

**사용 사례:** PEOS 부동산 시장 판단(경기판단) → 금리·거시국면·전세가 추이와 함께 경제 모니터링의 필수 입력.

## 알아둘 것

- 모든 시크릿은 **Repository secrets**(조직 단위 아님) — `stevekoo-ai/Repo_name` 워크플로우에서만 쓸 수 있고, 다른 저장소의 세션은 이름을 알아도 접근할 수 없다.
- 이 저장소는 **Public**으로 의도적으로 유지 중(2026-07-25 사용자 확인, [log](../log.md) 참고) — 코드/설정은 누구나 보지만 시크릿 값은 위 이유로 노출되지 않는다.
- 새 시크릿을 추가하거나 이름을 바꿨다면 이 페이지를 갱신할 것 — 워크플로우 파일이 진짜 소스지만, 여기가 "한눈에 보는" 진입점 역할을 한다.

## Sources

- `.github/workflows/*.yml` (데이터 수집/모니터링 워크플로우)
- [`core/notify.py`](../../core/notify.py)
- [`collectors/molit.py`](../../collectors/molit.py)
- [`scripts/portfolio_holdings.py`](../../scripts/portfolio_holdings.py), [`scripts/investor_flow.py`](../../scripts/investor_flow.py)
- [`collectors/subscription_monitor/alerts.py`](../../collectors/subscription_monitor/alerts.py)
- [나의 투자 포트폴리오](my-portfolio.md)
- [wiki/log.md](../log.md) 2026-07-24~25 항목 (KIS 앱키 발급 경위 원본 기록)
