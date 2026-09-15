---
title: 데이터 수집 헬스 Close-Loop 시스템
created: 2026-09-15
updated: 2026-09-15
tags: [infrastructure, data-quality, monitoring, concept, framework]
---

**신설 계기**: 사용자 지적 — *"데이터 수집 블럭 API 자동 수집 포함, 정상
작동 중인지 센싱하고, 신선도와 내용에 비정상이 확인되면 이것을 제어하는
기능을 추가해서 feedback이 있는 close-loop system을 만들자. 보고서가
항상 마음에 안들어!"*

**일일 추적**: [monitoring/data-health-status.md](../monitoring/data-health-status.md)

---

## 왜 지금까지 "마음에 안 들었나" — 조사로 확인된 것

이 저장소는 이미 여러 차례 "우연히 발견한" 데이터 사고를 하나씩
고쳐왔다 — 채권 누락(TR이 채권을 안 줌), 브리핑-거시수집 경쟁조건,
휴장갭 판정 버그, "해당 뉴스 없음"이 미검색과 안 구분됨. **패턴은
항상 같았다: 사고가 이미 일어난 뒤 누군가 물어봐야 발견됐다.**

구축 착수 전 전수 조사에서 그 패턴이 **지금도 진행 중**이라는 게
드러났다:

> `scripts/data_freshness_audit.py`(232개 정규화 시리즈의 발표주기별
> 신선도 판정기)는 이미 존재했고 이미 작동하고 있었다. 그런데 그 결과가
> `core10-collect.yml` 안에서 `::warning::` 한 줄로만 GitHub Actions
> 로그에 남고, **누구도 그 로그를 열어보지 않았다.** 2026-09-15 첫 실행
> 결과: **DEAD 22개 · stale 18개** — 일부는 622일(imf_* 4종), 심지어
> 1,049일(fred_kr_cpi_oecd) 동안 죽어 있었다.

sensing은 있었다. acting이 없었다. 이 시스템은 그 나머지 절반이다.

---

## 설계 원칙

### 1. 재사용 우선 — 새로 만들지 않는다

| 필요한 것 | 이미 있던 것 | 한 일 |
|---|---|---|
| 232개 정규화 시리즈 신선도 판정 | `scripts/data_freshness_audit.py` | 그대로 호출해 흡수(재구현 안 함) |
| 워크플로 실행 성공 이력 | `sources/automation-run-log.csv`(6개 워크플로가 이미 기록 중) | RUN_LOG 모드로 그대로 조회 |
| 임계 돌파 시 1회 알림 + 회복 리셋 | `collectors/subscription_monitor`의 `health_state.json` 패턴 | 그 설계를 그대로 일반화(`engine/health/control.py`) |
| 알림 발송 채널 | `core.notify`(scripts/send_report_email.py가 쓰는 것) | 그대로 재사용 |

### 2. 판정 불가 ≠ 이상 (R3)

데이터를 못 구했으면 `MISSING`이지 `STALE`이 아니다. 없는 걸 "이상"으로
단정하면 오탐이 쌓여 결국 무시당한다.

### 3. mtime을 쓰지 않는다

GitHub Actions의 `actions/checkout`은 매번 새로 체크아웃하고, 그 순간
모든 파일의 mtime이 "체크아웃 시각"으로 재설정된다 — `os.path.getmtime()`은
이 환경에서 "언제 실제로 수집됐는가"를 전혀 말해주지 않는다. 그래서
콘텐츠 안에 시각을 남기는 방식(`fetched_at` 컬럼, run-log)만 쓴다.

### 4. 거래일 예외

시장 데이터는 휴장일엔 새 데이터가 없는 게 정상이다. "오늘이 휴장이면
마지막 거래일 데이터까지는 왔는가"만 확인한다(`engine.briefing.calendar`
재사용). 주말마다 우는 시스템은 곧 무시당한다.

### 5. 알림은 임계 돌파 시 딱 한 번만

`CONSECUTIVE_THRESHOLD = 3`(헬스체크가 2시간마다 도니 최소 4~6시간
지속돼야 알림). 매번 알리면 소음, 한 번도 안 알리면 조용히 죽는다 —
subscription_monitor가 이미 검증한 균형점을 그대로 썼다.

---

## 구조

```
engine/health/
  registry.py    SourceSpec 목록 — "점(point) 소스" 18개(개별 파일)
  freshness.py   4가지 신선도 모드 계산 (CSV_FETCHED_AT / CSV_LATEST_DATE
                 / RUN_LOG / DATED_FILE_GLOB) + 거래일 예외
  content.py     구조적 이상(필수 컬럼 누락, 최소 행수 미달)
  check.py       판정만 한다. registry.SOURCES + data_freshness_audit()
                 스윕을 합쳐 하나의 HealthReport로 조립
  control.py     상태 지속(data/health/state.json) + 임계 판정 + 알림
                 (core.notify 재사용) — sensing과 acting을 분리

scripts/data_health_check.py   CLI (--no-alerts, --check-only)
.github/workflows/data-health-check.yml   2시간마다 실행 + 상태 커밋

data/health/
  state.json           per-slug {consecutive_bad, alerted}
  latest_report.json   브리핑·PEOS 리포트가 읽는 스냅샷
  latest_report.md     사람이 읽는 요약
```

### 두 계층의 소스

1. **점(point) 소스** (`registry.SOURCES`, 18개) — 개별 파일 단위로
   등록. macro-series, 하이닉스 시세·수급, 포트폴리오, SEC EDGAR CapEx,
   부동산 실거래, 청약 모니터(자체 감시 대조 표시), 일일 리포트 산출물.
2. **정규화 시리즈 스윕** (`data/normalized/*.csv`, 232개) — 개별
   등록하지 않는다. `check_normalized_series()`가 `data_freshness_audit.
   audit()`을 직접 호출해 결과를 흡수한다. 이미 있던, 더 정교한(발표
   주기 자동 추론) 판정 로직을 중복 구현하지 않기 위해서다.

### 신선도 판정 4가지 모드

| 모드 | 대상 | 예 |
|---|---|---|
| `CSV_FETCHED_AT` | CSV에 `fetched_at` 컬럼 있음 | macro-series.csv, 하이닉스 시세 |
| `CSV_LATEST_DATE` | `date`만 있음, 데이터 시차를 잰다 | (정규화 스윕이 대신 처리) |
| `RUN_LOG` | 파일 자체엔 시각 없음, automation-run-log.csv 조회 | 투자자별 매매동향, 부동산 실거래 |
| `DATED_FILE_GLOB` | 파일명에 날짜가 박힘, 존재 여부가 신선도 | 일일 리포트(`report/{date}.md`) |

---

## ⚠️ 등록 자체가 틀릴 수 있다 — 실제로 한 번 틀렸다

구축 중 `us-labor-outlook`을 `RUN_LOG` 모드로 등록했는데, 실제로는 그
워크플로가 `automation-run-log.csv`에 자기 행을 쓰지 않는다는 걸
**`--check-only`를 직접 돌려보고서야** 발견했다(영구 MISSING으로 떴다).
`CSV_LATEST_DATE`로 정정했고, 같은 사고가 조용히 반복되지 않도록
테스트(`test_every_run_log_source_has_appeared_at_least_once`)가
**모든 RUN_LOG 등록이 실제 로그에 한 번이라도 나타난 적 있는지**를
회귀로 고정한다 — 레지스트리 자신도 검증 대상이다.

---

## 게이트 통합 — critical에도 "조용한 날" 예외를 또 뒀다

브리핑 게이트(`evaluate_gate`)는 critical 데이터 이상이 있으면 조용한
날이어도 강제 발행하도록 연결했다. **단 `normalized:*` 스윕 결과는
제외했다** — 최초 점검에서 이미 22개가 DEAD였는데(예: imf_* 622일),
그걸 매일 강제 발행 사유로 쓰면 "조용한 날" 개념 자체가 영구히
사라진다. 브리핑이 실제로 매일 의존하는 핵심 소스(registry.SOURCES에
개별 등록된 것)만 강제 발행 트리거로 쓴다 — 그 소스들은 매일 갱신이
정상이라 critical이 뜨는 것 자체가 진짜 이상이기 때문이다.

## 보고서 통합 — "보고서가 항상 마음에 안 든다"에 대한 직접 대응

- 브리핑 팩: **블록 ⓪** (모든 블록보다 먼저)
- PEOS 리포트: **Section -1** (`_exposure_section`보다 먼저 — 그 섹션이
  스스로를 "매크로가 다 죽어도 유효한 유일한 섹션"이라 설명하는데, 정작
  "매크로가 죽었는지"를 알려주는 섹션이 없었다. 이 배너가 그 빈자리다)

둘 다 `data/health/latest_report.json` 스냅샷만 읽는다 — 렌더링 때마다
250개 소스를 재검사하지 않는다(헬스체크는 이미 2시간마다 별도로 돈다).

---

## 하지 않은 것 (의도적, 문서화)

- **daily-clock-report / briefing-email 자체는 등록하지 않음** — 전자는
  부차 기능, 후자는 이미 push 성공 확인 절차가 프롬프트에 박혀 있다.
  필요해지면 추가.
- **값의 "의미" 검증은 하지 않는다** — 가격이 음수인지, 급변이 말이
  되는지 같은 판정은 소스마다 달라 일반화하면 오탐이 늘어난다. 구조적
  이상(컬럼·행수)까지만 본다.
- **자동 재수집(retry) 트리거는 없다** — 이상을 감지하고 알리는 것까지가
  이 시스템의 책임이다. 워크플로를 강제로 재실행하려면 GitHub Actions
  `workflow_dispatch` API 호출 권한(`actions: write`)이 추가로 필요한데,
  그건 "판정을 사람에게 정확히 전달하는 것"이라는 이번 요청의 핵심에서
  벗어난 별도 결정이라 포함하지 않았다.
- ~~22개 DEAD·18개 stale 시리즈를 지금 고치지 않았다~~ **→ 2026-09-15
  같은 날 사용자 지시("모두 다, 순서를 생각해보고 다 고쳐")로 전수
  수리했다.** 자세한 원인·조치는
  [monitoring/data-health-status.md](../monitoring/data-health-status.md)
  참고 — **critical 22건이 전부 오진 또는 재분류였다**(진짜 죽은
  수집기는 0개). GitHub Actions 실제 job 로그로 하나하나 대조했다:
  - **16개**: 감사 도구가 "annual"(연 1회 발표) 빈도 버킷이 없어서
    IMF WEO 연간 시리즈가 전부 오판정됐다 — 버킷 신설로 해결
  - **2개**: `fred_kr_cpi_oecd`·`fred_kr_industrial_production_oecd` —
    수집은 매번 성공하지만 OECD 미러 자체가 상류에서 단종
    (`us_dollar_index_major`/DTWEXM과 같은 계열) — 숨기지 않고
    `KNOWN_DEAD_BY_DESIGN`으로 이유와 함께 재분류
  - **5개**: `daily-peos-report.yml` 삭제(2026-08-11)로 호출 경로를
    잃은 고아 시리즈(motie_* 3개, kosis_semiconductor_* 2개) — 이미
    매일 도는 워크플로(correlation_analysis.py, collect_core10.py)에
    재연결
  - **KOSIS 타임아웃**: 실제 connect timeout(10초, 2회 재시도)을
    실측 확인, 20초·4회로 증가
  - **나머지**: 진짜 "정상 발표 지연"이었다 — 손대지 않고 "stale"
    (경고, 비알림)로 정확하게 남겼다
  이 과정에서 제어 루프 자체의 설계 결함도 발견해 고쳤다: severity
  구분 없이 3회 연속이면 알리던 걸 **critical만 알리게** 바꿨다 —
  안 그러면 "영구적으로 약간 오래된 게 정상"인 시리즈가 6시간마다
  이메일을 영원히 쏘게 된다.

---

## 검증

`tests/test_data_health.py` 24건, `tests/test_data_freshness_audit.py`
10건(annual 버킷, dead_by_design 재분류, 저장소 회귀), `tests/
test_kosis_retry_config.py` 4건(타임아웃·재시도·고아 키 재연결·좌표
존재) — 판정 불가/이상 구분, 거래일 예외 양방향, 레지스트리 자기 검증,
제어 루프(critical만 알림·회복 리셋·미설정 채널 무해 처리·warning은
아무리 오래 지속돼도 비알림), 정규화 스윕 중복 미등록.

## 관련

- `scripts/data_freshness_audit.py` — 232개 정규화 시리즈 신선도(재사용)
- `collectors/subscription_monitor/compose.py` — 이 시스템의 제어 패턴 원본
- `wiki/architecture/briefing-system-design.md` — 브리핑 팩 블록 구조
