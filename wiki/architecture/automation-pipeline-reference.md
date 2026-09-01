# 자동화 파이프라인 레퍼런스 (GitHub Actions + Claude Routine)

**목적**: 이 저장소에서 지금 실제로 돌고 있는 모든 자동 데이터 업데이트 —
어떤 워크플로/트리거가 언제(KST) 무엇을 수집해서 어디에 저장하는지 —
를 한 곳에 정리한 레퍼런스. 어떤 LLM이든 이 문서 하나만 읽으면 "지금
이 저장소에서 뭐가 자동으로 돌고 있고, 그 산출물이 어디 있는지"를
코드를 뒤지지 않고 파악할 수 있는 것이 목표다.

**생성**: 2026-08-31 (사용자 요청) · **최신 확인**: 2026-08-31 — 아래 표는
이 날짜에 `.github/workflows/*.yml` 17개 파일과 4개 Claude Routine 트리거를
직접 읽고 검증한 결과다. 이후 워크플로 파일이나 트리거가 바뀌면 이 문서도
같이 갱신해야 한다(자동 동기화 없음 — 수동 문서, 드리프트 가능).

**관련 문서**: 리포트 자체의 구조는
[reporting-framework.md](reporting-framework.md), 위키 갱신 원칙은
[log-operating-policy.md](../concepts/log-operating-policy.md),
데이터 재수집 없이 판단형 지식을 리포트에 연결하는 방식은
[data/wiki_digest/README.md](../../data/wiki_digest/README.md) 참고.

---

# 1. 두 개의 서로 다른 자동화 층

이 저장소는 **완전히 다른 두 메커니즘**으로 자동 갱신된다 — 헷갈리기 쉬우니
먼저 구분한다.

| | **GitHub Actions** | **Claude Routine (Claude Code Remote)** |
|---|---|---|
| 실행 주체 | GitHub의 CI 러너, 순수 Python 스크립트 | Claude(LLM) 세션이 매번 새로 뜸 |
| 판단 방식 | 결정론적 — 같은 입력엔 항상 같은 출력, LLM 없음 | WebSearch·뉴스 해석 등 진짜 판단 필요한 일 |
| 정의 위치 | `.github/workflows/*.yml` (이 저장소에 커밋된 파일) | Claude Code Remote 플랫폼에 저장(이 저장소엔 정의 파일 없음, `mcp__Claude_Code_Remote__list_triggers`로만 조회 가능) |
| 최소 실행 간격 | 제약 없음(분 단위 cron 가능) | **1시간**(플랫폼 제약) |
| 실패 시 재시도 | 6장 참고 — 워크플로 내부 bash 루프(10분 간격, 최대 6시간) | 트리거 프롬프트 안에 "0단계 환경 검증" 로직으로 자체 방어(4장 참고) |
| 커밋 주체 | 각 워크플로가 지정한 bot 이름(예: `peos-bot`, `sk-hynix-auto-report-bot`) | Claude 세션 자신의 git identity |
| 산출물 | CSV/JSON(구조화 데이터), 리포트 .md/.html | wiki/monitoring/*.md 자유문 텍스트(사람이 읽는 판단·해석) |

**왜 나뉘어 있나**: "숫자를 실제로 조회하는 일"(가격, 지표, 실거래가)은
GitHub Actions가 매일/매시간 흔들림 없이 처리하고, "이게 무슨 의미인지
해석하는 일"(오늘 뉴스가 체크포인트에 영향을 주는지, 애널리스트 리포트를
어떻게 반영할지)은 LLM 판단이 필요해서 Claude Routine이 맡는다. 이 둘을
다시 연결하는 다리가 `data/wiki_digest/*.yaml`이다(5장 참고).

---

# 2. GitHub Actions 워크플로 전체 목록

cron은 UTC 기준으로 저장돼 있다 — 아래 표의 KST는 이미 변환된 값(UTC+9).

## 2-1. 데이터 수집 (스케줄 실행, 매일/매주)

| 워크플로 파일 | 이름 | 스케줄(KST) | 무엇을 수집하나 | 주 스크립트 |
|---|---|---|---|---|
| `core10-collect.yml` | Core-10 지표 수집 | 매일 06:30 | KOSIS·ECOS·FRED 핵심 10개 거시지표 | `scripts.collect_core10` |
| `macro-data-sync.yml` | 거시지표 자동 수집 | 매일 07:10 | 한국 10Y 국고채·미국 10Y Treasury·기준금리·GDP 등 | `scripts/macro_data.py sync` |
| `sk-hynix-daily-report.yml` | SK하이닉스 자동 1차 리포트 | 매일 07:00 / 10:00 / 19:00 (**1일 3회**) | SK하이닉스 실시간 시세·투자자매매동향(외국인/기관/개인)·신용융자·공매도·ADR·ETF NAV, HBM Cycle Score 자동채점, 하이퍼스케일러 CapEx 인용 | `scripts/daily_report.py` (내부에서 `investor_flow.py`, `hbm_cycle_score.py` 호출) |
| `portfolio-holdings-sync.yml` | 포트폴리오 보유종목 자동 수집 | 매일 19:10(장마감 후) | KIS 4개 계좌(일반/ISA/DC/IRP) 보유종목·평가금액 | `scripts/portfolio_holdings.py sync` |
| `real-estate-sync.yml` | 부동산 실거래가 자동 수집 | 매일 03:00 | 국토부 실거래가 — 아파트 매매/전월세, 연립다세대(빌라) 매매, 오피스텔 매매 (4개 수집기) | `collectors.molit`, `molit_rent`, `molit_villa`, `molit_officetel` |
| `sec-edgar-capex.yml` | SEC EDGAR CapEx & AI 변두리 | 매주 화요일 06:00 | 하이퍼스케일러(GOOGL/MSFT/AMZN/META) CapEx + AI 밸류체인 변두리 8개사(Vertiv·GE Vernova·Astera Labs 등) 매출·백로그 | `scripts/sec_edgar_capex.py`, `scripts/sec_edgar_periphery.py` |
| `exports-price-correlation.yml` | 수출입동향×주가 상관관계 갱신 | 매일 19:30 | 관세청 총수출/총수입 실측(1990~) + KIS 월봉/일봉(하이닉스·코스피) → 상관관계 차트 재생성 | `collectors.customs_trade`, `scripts/investor_flow.py`, `scripts.correlation_analysis` |
| `subscription-monitor.yml` | 청약(공공분양) 모니터 | **30분마다**(매시 07/37분) | 서울/경기 국민주택 청약공고 신규/변경 감지 | `collectors/subscription_monitor/fetch_and_render.py` |

## 2-2. 리포트 생성 (수집된 데이터를 조합해 리포트 산출)

| 워크플로 파일 | 이름 | 스케줄(KST) | 산출물 | 비고 |
|---|---|---|---|---|
| `daily-peos-report.yml` | Daily PEOS Report | 매일 06:00 | `report/<월>.{md,html,json}` + `report/<날짜>.{md,html,json}`(일별 아카이브) | **이 저장소의 "메인" 일일 리포트.** `engine/report/run.py` 실행 — Track A(경제판단) 전용, 이메일 발송·GitHub Pages(`docs/report.html`) 게시 포함 |
| `monthly-peos-report.yml` | Monthly PEOS Report | **workflow_dispatch 전용**(스케줄 없음) | 위와 동일 | daily-peos-report.yml이 매일 이미 월간분도 갱신하므로 상시 스케줄은 불필요 — 수동 재실행용으로만 유지 |
| `daily-clock-report.yml` | Daily Investment Clock Report | 매일 08:00 | `docs/index.html`("거시경제 투자 시계") + `data/history.csv` | `src/clock/main.py` — 국면(Overheat/Reflation 등) 판정 |

## 2-3. 상태 확인·진단 도구 (전부 workflow_dispatch 전용, 스케줄 없음 — 사람이 직접 실행)

| 워크플로 파일 | 용도 |
|---|---|
| `ecos-lookup.yml` | ECOS 통계표 코드/항목 검색(한국은행 API) |
| `kosis-lookup.yml` | KOSIS 통계표 코드/항목 검색 |
| `molit-diagnostic.yml` | 국토부 실거래가 API 원본 응답 확인(필드명 점검용) |
| `network-diagnostic.yml` | 구독(청약) 수집기 소스의 네트워크 접근성 점검 |
| `subscription-schema-probe.yml` | 청약 API 응답 스키마 변경 감지(`push` 트리거, 특정 브랜치 전용) |

이 5개는 사람이 기다리는 동안 결과를 봐야 해서 재시도가 가볍다(3회, 20초
간격) — 아래 6장의 "6시간 재시도"와는 다른 정책.

## 2-4. 인프라 유지보수

| 워크플로 파일 | 이름 | 스케줄(KST) | 하는 일 |
|---|---|---|---|
| `log-rotate.yml` | Log Rotate | 매일 00:20 | `wiki/log.md`의 어제 날짜 항목을 `wiki/log-archive/YYYY-MM/YYYY-MM-DD.md`로 이관(append-only 로그가 무한히 커지는 것 방지). 월말엔 전월 일별 아카이브를 월 아카이브로 병합. LLM 없음, 순수 Python(`scripts/log_rotate.py`) |

---

# 3. 각 워크플로의 실행 조건 상세

## 3-1. `permissions`와 `concurrency`

전체 17개 워크플로 모두 `permissions: contents: write`(리포지토리에 직접
커밋하기 위함). 데이터를 쓰는 워크플로는 전부 `concurrency: group: <워크플로명>`
을 갖고 있어 **같은 워크플로가 겹쳐 돌지 않는다**(재시도 창이 다음 스케줄
실행과 부딪히는 걸 방지) — 단 `daily-peos-report.yml`만
`cancel-in-progress: false`(진행 중인 걸 취소하지 않고 대기열에 쌓음, 나머지는
`cancel-in-progress: true`로 새 실행이 오래된 실행을 대체).

## 3-2. `workflow_dispatch` (수동 재실행)

스케줄이 있는 워크플로도 전부 `workflow_dispatch`를 같이 갖고 있어
GitHub Actions UI나 API(`mcp__github__actions_run_trigger`, method
`run_workflow`)로 즉시 재실행할 수 있다. 일부는 입력 파라미터를 받는다:
- `daily-peos-report.yml` / `monthly-peos-report.yml`: `month`(YYYY-MM, 비우면 이번 달)
- `real-estate-sync.yml`: `only_apartment`(true면 아파트 매매만, 빠른 테스트용)
- `sec-edgar-capex.yml`: `raw`(진단 모드, CSV 저장 안 함), `company`(GOOGL/MSFT/AMZN/META로 한정)
- `sk-hynix-daily-report.yml`: `debug_raw`(true면 원본 API 응답만 로그에 찍고 종료, 커밋/이메일 없음)

---

# 4. Claude Routine 트리거 (GitHub Actions가 아님)

`mcp__Claude_Code_Remote__list_triggers`로 조회 가능. 2026-08-31 기준 **4개
활성** — 전부 `enabled: true`, 최근 실행 전부 `SUCCEEDED`.

| Trigger ID | 이름 | cron(UTC) → KST | 담당 |
|---|---|---|---|
| `trig_01Bda27Tv6i4CPJBuzmG7Ppd` | SK하이닉스 아침 체크포인트 점검 | `0 22 * * *` → 매일 07:00 | 9개 체크포인트 전체 재검증 + 미국장 총평(고정 섹션) |
| `trig_013tusejpCGbL7Sa3RUdDcCt` | SK하이닉스 장초반 개장 데이터 체크 | `0 1 * * *` → 매일 10:00 | 개장 직후 가격·수급 스냅샷만(±5% 이상 변동시에만 기록) |
| `trig_01QFcMFhCoE3MAzKavYvxMH5` | SK하이닉스 저녁 신규 근거 스캔 | `0 10 * * *` → 매일 19:00 | 5개 트래커(체크포인트/HBM Cycle Score/패닉회복신호/찐반등4대신호/트럼프트래커) 중 오늘 새 소식 있는 것만 갱신 |
| `trig_012mx9wqwgmnrkYGwWrqScUW` | 관세청 수출입 잠정치 자동 갱신 | `0 4-9 11,21 * *` → 매월 11일·21일 13:00~18:00 KST 매시(총 6회) | 관세청 10일/20일 단위 수출입 잠정치를 WebSearch로 찾아 `data/manual_inputs/exports_preliminary.yaml` 갱신 |

**공통 설계 원칙(전부 프롬프트에 명시)**:
- **매번 새 세션** — 이전 대화 기억 없음, 파일(`wiki/monitoring/*-status.md`의
  "Latest Status" 섹션만)에서만 맥락을 얻는다. 대화가 계속 이어붙는 방식은
  2026-08-19에 폐기됨(5주간 캐시비용 폭증, cache_read 1억 1,700만 토큰 사례).
- **0단계 환경 검증**(2026-08-24 추가) — `git status` 실패 시 clone 시도,
  그래도 실패하면 나머지 단계를 건너뛰고 사용자에게 실패를 알린 뒤 종료.
  이건 "변화 없으면 조용히 종료" 규칙의 명시적 예외다.
- **push 후 해시 비교 검증**(2026-08-24 추가) — `git push` 후
  로컬 HEAD와 `origin/main` HEAD 해시를 비교, 다르면 push 실패로 간주하고
  사용자에게 알림.
- **변화 없으면 조용히 종료** — 매번 전체 트래커를 다 갱신하려 하지 않는다
  (노이즈 방지). 단, 위 두 예외는 항상 알림.

**Claude Routine 관리 도구**: `mcp__Claude_Code_Remote__list_triggers`(목록),
`update_trigger`(프롬프트/스케줄 수정), `fire_trigger`(즉시 강제 실행 —
진단용), `delete_trigger`.

---

# 5. 위키 판단형 지식 브리지 — `data/wiki_digest/`

Claude Routine이 갱신하는 `wiki/monitoring/*-status.md`는 자유문 텍스트라
결정론적 파이프라인(`engine/report/`)이 직접 파싱할 수 없다. 대신
`data/wiki_digest/*.yaml`이 각 monitoring 페이지의 "Latest Status"를
구조화된 형태(상태배지 한 줄 + 한줄요약 + 링크)로 미러링하고,
`engine/report/wiki_digest.py`가 이걸 읽어 PEOS 리포트 "2.7 위키 추적
신호 요약" 섹션으로 렌더링한다.

**중요**: 이 YAML 파일은 **원천이 아니다** — 위키 monitoring 페이지가
갱신될 때(Claude Routine이든 `/ingest`든 사람 수동 편집이든) **같은 작업이
이 파일도 같이 갱신해야 한다**. `engine/report/wiki_digest.py::load_wiki_digests()`
가 매 리포트 생성 시 각 digest의 `as_of`와 대응 monitoring 페이지
frontmatter의 `updated:`를 비교해 drift(위키는 갱신됐는데 digest를 깜빡함)를
자동 감지한다. 상세: [data/wiki_digest/README.md](../../data/wiki_digest/README.md)

현재 6개 digest: `hbm-cycle-score`, `sk-hynix-analyst-thesis-checkpoints`,
`market-cycles-leverage-risk`, `trump-midterm-tracker`,
`data-center-construction-vs-opposition`, `semiconductor-export-peak-recovery`.

---

# 6. 실패 시 재시도·알림 메커니즘

## 6-1. 재시도(bash 루프, 워크플로 내부)

**6시간 재시도 창**(데이터 수집 5개 워크플로 — `sk-hynix-daily-report`,
`portfolio-holdings-sync`, `macro-data-sync`, `sec-edgar-capex`,
`real-estate-sync`): 실패하면 10분 간격으로 최대 36회(=6시간) 재시도한다.
패턴:
```bash
attempt=1; max_attempts=36
until <수집 명령>; do
  if [ "$attempt" -ge "$max_attempts" ]; then
    echo "::error::${max_attempts}회(6시간) 재시도했지만 실패"
    exit 1   # (real-estate-sync는 exit 1 대신 break — 4개 수집기 중 하나
             #  실패해도 나머지는 계속 진행하는 설계)
  fi
  attempt=$((attempt + 1)); sleep 600
done
```
**3회/20초 재시도**(진단 도구 5개 — `ecos-lookup`, `kosis-lookup`,
`molit-diagnostic` 등): 사람이 결과를 기다리므로 6시간 재시도는 부적절,
훨씬 가볍게.

**관세청 잠정치 Claude Routine**은 GitHub Actions가 아니라 플랫폼 최소
실행 간격(1시간) 제약 때문에 "매시 정각 6회"가 재시도 창 역할을 겸한다
(4장 참고).

## 6-2. 실패 알림(이메일)

`scripts/send_report_email.py --failure-alert "<메시지>"`를 `if: failure()`
스텝에서 호출 — 6시간 재시도가 전부 소진된 뒤에만 발동(중간 재시도 중엔
조용함). Track A(경제판단 리포트) 채널이라 GitHub Actions 시크릿을 통한
이메일 발송이 CLAUDE.md 정책상 허용됨. 이 알림이 있는 워크플로:
`core10-collect`, `daily-peos-report`, `sk-hynix-daily-report`,
`portfolio-holdings-sync`, `macro-data-sync`, `sec-edgar-capex`,
`real-estate-sync`(4개 수집기 중 실패한 것만 콕 집어 한 번에 알림,
`if: always()`).

**알림이 없는 워크플로**(2026-08-31 기준, 조용히 실패할 수 있음):
`daily-clock-report`, `exports-price-correlation`, `log-rotate`,
`subscription-monitor`, `subscription-schema-probe`, 5개 진단 도구,
`monthly-peos-report`(수동 실행 전용이라 사람이 결과를 바로 봄).

## 6-3. `sources/automation-run-log.csv` — 재시도가 실제로 발동됐는지 추적

2026-08-27 신설(`scripts/log_automation_run.py`). 위 6시간 재시도 루프를
가진 5개 워크플로가 각 재시도 대상 스텝의 성공/소진 여부를 이 CSV 한 줄로
남긴다 — 컬럼: `timestamp_utc,workflow,step,attempts_used,max_attempts,result`
(`result`는 `success` 또는 `exhausted`). **이 파일 하나만 grep하면
"자동수집이 실제로 도는지, 재시도가 발동된 적 있는지"를 GitHub Actions
run 이력을 뒤지지 않고 바로 확인할 수 있다** — 이게 이 파일이 만들어진
이유(과거엔 `mcp__github__actions_list`+`get_job_logs`로 수동 조사해야
했음). `attempts_used`가 1보다 크면 그 실행에서 실제로 재시도가 발동된
것이다.

---

# 7. 데이터 저장 위치 전체 맵

## 7-1. `sources/*.csv` — 원자료(append/upsert, 대부분 날짜별 1행)

| 파일 | 수집 워크플로 | 내용 |
|---|---|---|
| `sk-hynix-investor-flow.csv` | sk-hynix-daily-report | 투자자별(외국인/기관/개인) 일별 순매수 |
| `sk-hynix-price-snapshot.csv` | 〃 | 시세·외국인보유율·250일 최고가 |
| `sk-hynix-credit-balance.csv` | 〃 | 신용융자잔고 |
| `sk-hynix-short-sale.csv` | 〃 | 공매도 거래량·비중 |
| `sk-hynix-adr-quote.csv` | 〃 | ADR(SKHY, 나스닥) 시세 |
| `sk-hynix-quarterly-fundamentals.csv` | (수동) | 분기 실적(밸류에이션 밴드 P/E Z-score 계산용) |
| `kr-index-quote.csv` | sk-hynix-daily-report | 코스피/코스닥 지수 |
| `portfolio-etf-nav.csv` | 〃 | 보유 ETF NAV·괴리율 |
| `portfolio-holdings.csv` | portfolio-holdings-sync | 계좌별(일반/ISA/DC/IRP) 보유종목·평가금액 |
| `macro-series.csv` | macro-data-sync | 한국/미국 금리·GDP·환율 시계열 |
| `hyperscaler-capex.csv` | sec-edgar-capex | GOOGL/MSFT/AMZN/META 분기 CapEx(SEC EDGAR XBRL) |
| `ai-periphery-fundamentals.csv` | 〃 | AI 밸류체인 변두리 8개사 매출·백로그 |
| `daily-price-history.csv` / `monthly-price-history.csv` | exports-price-correlation | KIS 일봉/월봉(하이닉스·코스피) |
| `kospi-forward-pe-approx.csv` | (수동/보조) | 코스피 선행 P/E 근사치 |
| `automation-run-log.csv` | 6-3 참고 | 재시도 발동 이력 |

## 7-2. `sources/sk-hynix-auto-report-*.md` — SK하이닉스 자동 1차 리포트 본문

파일명 규칙 `sk-hynix-auto-report-YYYY-MM-DD-HHMM.md`, 1일 최대 3개(07:00·
10:00·19:00 KST). `scripts/daily_report.py`가 생성 — 규칙 기반, **LLM 미사용**.
이메일로도 발송됨.

## 7-3. `data/manual_inputs/*.yaml` — 자동 수집 불가능한 데이터의 수동 입력 (7.3 예외 정책)

무료 공식 API가 없는 데이터(경제캘린더, 반도체 애널리스트 신호, 청약공고
원문 해석 등)는 사람 또는 Claude가 손으로 채운다. 각 파일 상단에 왜
수동인지, 신뢰도 등급, 갱신 방법이 명시돼 있다.

| 파일 | 내용 | 갱신 방식 |
|---|---|---|
| `exports.yaml` / `exports_annual.yaml` | 산업통상부 월간 수출입동향(총수출/반도체수출 %YoY) | 수동(월간 보도자료 확인) |
| `exports_preliminary.yaml` | 관세청 10일/20일 단위 잠정치 | **관세청 Claude Routine**(4장)이 자동 갱신 |
| `semiconductor.yaml` | 반도체 애널리스트 신호(DRAM/NAND 가격추세, CSP CapEx 등) | 수동, 신뢰도 등급 3으로 캡 |
| `calendar.yaml` | 경제 캘린더 — **⚠️ 2026-08-31 기준 전부 EXAMPLE 플레이스홀더, 실데이터 아님**(무료 공개 경제캘린더 API 부재, `engine/report/economic_events.py` 참고) | 수동(현재 미유지보수 상태) |
| `data_center_construction.yaml` | 미국 데이터센터 건설 착공실적 vs 반대 여론 | 수동(월간, ConstructConnect/Data Center Watch 공개 API 없음) |
| `kospi_annual.yaml`, `subscription_notices.yaml`, `trips.yaml` | 코스피 연간 데이터, 청약공고, 개인 출장/여행 일정 | 수동 |

## 7-4. `data/wiki_digest/*.yaml` — 위키 판단형 지식 브리지 (5장 참고)

## 7-5. `data/normalized/`, `data/raw/` — 코드가 API에서 받아온 원자료

`data/raw/<소스>/<시리즈>__<타임스탬프>.json` — API 원본 응답 그대로(감사
추적용). `data/normalized/<시리즈id>.csv` — 표준화된 시계열(178개+ 파일,
KOSIS/ECOS/FRED/관세청/OECD/BLS/IMF 등 출처별). `collectors/base.py`의
`write_raw()`/`append_normalized()`가 모든 collector에서 공통으로 씀.

## 7-6. `data/snapshots/2026-08.json` 등 — 월별 전체 payload 스냅샷

`engine/report/payload.py::build_report_payload()`가 계산한 전체 결과(매크로
국면, 신뢰도, 각 지표 상태)를 월별로 통째로 저장 — 다음 실행이 "이월"할
근거가 되는 파일. **주의**: 로컬 테스트 환경에서 API 키 없이
`build_report_payload()`를 실행하면 이 파일이 열화된(fallback) 값으로
덮어써질 수 있음 — 항상 실제 CI 실행 결과만 커밋해야 한다.

## 7-7. `data/daily_signals/signal_YYYY-MM.csv`, `data/peos_daily_history.csv`

SK Hynix/부동산 의사결정 신호(HOLD/BUY/SELL, WAIT/ENTER)의 일별 기록 —
월별 롤링 윈도우(PEOS 리포트 Section 4/5) 계산용. `engine/report/signal_recorder.py`
가 하루 1행만 기록(재실행해도 중복 안 됨, idempotent).

## 7-8. `report/` — 생성된 리포트

- `report/<YYYY-MM>.{md,html,json}` — **최신 월간**(매 실행마다 덮어씀)
- `report/<YYYY-MM-DD>.{md,html,json}` — **일별 아카이브**(그날 실행 스냅샷,
  영구 보존)
- 그 외 일회성 파일(`daily-brief-*.html`, `subscription-desktop-*.html`,
  `peos-audit/full/morning-*.html` 등) — 초기 실험/수동 발행분

## 7-9. `docs/` — GitHub Pages로 서빙되는 정적 사이트

| 파일 | 내용 |
|---|---|
| `index.html` | 거시경제 투자 시계(daily-clock-report.yml이 갱신) |
| `report.html` | **최신 월간 PEOS 리포트**(daily-peos-report.yml이 매일 `report/<월>.html`을 복사) |
| `peos-daily.html` | PEOS Daily Dashboard |
| `subscription-monitor.html` | 청약 모니터 현황 |
| `reports-index.html` | **생성된 모든 리포트(.md/.html) 링크 목록**(2026-08-31 신설, 아래 참고) |
| `archive/` | `report/*.html` 전체 미러(일별+월간, `reports-index.html`의 HTML 링크가 여기를 가리킴) |

**`reports-index.html`은 `scripts/build_reports_index.py`가 생성** —
`daily-peos-report.yml`(1일 1회)과 `sk-hynix-daily-report.yml`(1일 3회)의
커밋 스텝 직전에 호출돼 항상 최신 상태를 유지한다. `.md` 파일은 GitHub이
자체 렌더링해주니 GitHub blob URL로, `.html` 파일은 GitHub blob 뷰가
소스코드로만 보여줘서 `docs/archive/`에 미러링한 뒤 Pages URL로 링크한다.

---

# 8. 빠른 참조 — "이걸 알고 싶으면 어디를 보나"

| 알고 싶은 것 | 확인 위치 |
|---|---|
| 오늘의 SK하이닉스 실시간 시세·수급 | `sources/sk-hynix-price-snapshot.csv`, `sources/sk-hynix-investor-flow.csv` (최신 행) |
| 오늘의 "메인" 종합 리포트 | `report/<오늘날짜>.md` 또는 `https://stevekoo-ai.github.io/Repo_name/report.html` |
| 지금까지 생성된 리포트 전체 목록 | `https://stevekoo-ai.github.io/Repo_name/reports-index.html` |
| 특정 워크플로가 최근 성공/실패했는지 | `mcp__github__actions_list`(method `list_workflow_runs`) 또는 `sources/automation-run-log.csv` |
| 재시도가 실제로 발동된 적 있는지 | `sources/automation-run-log.csv`에서 `attempts_used > 1`인 행 검색 |
| HBM Cycle Score·9체크포인트 등 판단형 지식의 최신 상태 | `data/wiki_digest/*.yaml`(압축 요약) 또는 `wiki/monitoring/*-status.md`(원문, "Latest Status" 섹션) |
| 특정 API 키가 어느 워크플로에 필요한지 | 이 문서 2장 표 + 각 워크플로 파일의 `secrets.*` 참조(2-1~2-3 섹션 조사 시 grep으로 확인 가능) |
| 데이터센터 건설 지표, CapEx 등 "예전에 조사한" 판단형 자료 | `wiki/concepts/*.md`(framework) + `wiki/monitoring/*-status.md`(일일 상태) |
| 경제 캘린더가 왜 이상한 데이터를 보여주는지 | 7-3장의 `calendar.yaml` 경고 참고 — 현재 플레이스홀더 상태, 미해결 |
