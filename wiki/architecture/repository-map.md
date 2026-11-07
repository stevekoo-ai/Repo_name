---
title: 저장소 지도 — stevekoo-ai/Repo_name 전체 구성 (새 터미널 온보딩용)
created: 2026-11-07
updated: 2026-11-07
tags: [architecture, onboarding, repository-map, ops]
---

# 저장소 지도 (Repository Map)

**목적**: 이 저장소를 처음 여는 터미널이나 에이전트가 코드를 뒤지지 않고
10분 안에 다음을 알 수 있게 한다.
- 무엇이 어디에 있는가
- 무엇이 자동으로 돌고 있는가
- 지켜야 할 규칙은 무엇인가
- 지금 사용자가 무슨 일을 진행 중인가

**실측 기준**: 2026-11-07 main(`a3b250d7`)을 직접 조사했다. 파일 수는 이 시점 값이고, 이후 바뀐다.

**대체 관계**:
- [llm-wiki-file-inventory.md](../llm-wiki-file-inventory.md)는 sources를 154개 시점으로 기록한 옛 목록이다. 이 페이지가 최신이다.
- 자동화 상세(재시도, 실패 알림, 저장 위치)는 [automation-pipeline-reference.md](automation-pipeline-reference.md)가 단일 출처다. 단, 그 문서는 워크플로 17개 시점(2026-08-31)이라 **아래 7장의 26개 목록이 더 최신**이다.

---

## 0. 새 터미널이 읽는 순서 (5분)

1. 루트 [`CLAUDE.md`](../../CLAUDE.md): 최우선 정책(트랙 A/B), 작업 실행 프로토콜(계획 → 진행 표시 → 완료 보고), 금지 영역
2. [`wiki/CLAUDE.md`](../CLAUDE.md): 위키 스키마와 Ingest/Query/Lint 워크플로, main 직접 push 원칙
3. [`MessageBox.md`](../../MessageBox.md)와 [`wiki/messagebox.md`](../messagebox.md): 활성 경고와 인계 사항
4. [`wiki/log.md`](../log.md) 마지막 30줄: 최근 무슨 일이 있었나. **쓰기 전에 [log 운영 정책](../concepts/log-operating-policy.md)을 읽는다**
5. 이 페이지 10장 "진행 중인 사용자 과제"
6. 질문 주제에 맞는 `wiki/monitoring/*-status.md`의 Latest Status

---

## 1. 저장소 개요

- **이름**: `stevekoo-ai/Repo_name` (GitHub). 클라우드 세션의 작업 경로는 보통 `/home/user/Repo_name`이다.
- **소유자**: Steve. 한국어로 답한다.
- **브랜치**: **main이 유일한 공유 브랜치**다. 위키, 보고서, 코드 모두 main에 직접 커밋하고 `bash scripts/push_with_retry.sh main`으로 push한다. `claude/ai-agent-impl-002tip`은 2026-10-15 이후 방치된 죽은 브랜치라 쓰지 않는다.
- **한 저장소에 두 시스템이 있다**:
  1. **LLM Wiki**(Karpathy 패턴): `sources/`(불변 원자료) → `wiki/`(LLM이 유지하는 지식)
  2. **PEOS**(Personal Economic Operating System): `engine/`, `scripts/`, `config/`이 데이터를 수집해 보고서를 만들고 메일로 보낸다. 지시서는 [`docs/PEOS_ClaudeCode_Master_Instruction.md`](../../docs/PEOS_ClaudeCode_Master_Instruction.md)다.
  - 둘은 `data/wiki_digest/*.yaml`(위키 판단 → 보고서)과 `sources/*.csv`(수집 데이터 → 위키 근거)로 연결된다.
- **목적**: 사용자 개인 자산 판단이다. 다루는 영역은 SK하이닉스 보유분 매도·보유 판단, 거시, 주거·청약 자금 계획이다.

---

## 2. 최상위 폴더 지도

| 폴더·파일 | 파일 수 | 역할 |
|---|---|---|
| `CLAUDE.md` | - | 최상위 운영 정책. 트랙 A/B, 작업 프로토콜, 금지 영역, 세션 시작 체크리스트 |
| `MessageBox.md` | - | 세션 간 인계 게시판(PEOS 쪽) |
| `README.md`, `GUIDE.md`, `USAGE.md`, `SYSTEM-OVERVIEW.md` | - | 사람용 설명서. 일부는 오래됨 |
| `wiki/` | 347 | 지식베이스(3장) |
| `sources/` | 438 | 불변 원자료. 사용자 제공 요약, 자동 수집 CSV(4장) |
| `data/` | 602 | 엔진 입력과 중간 산출물. 원자료, 정규화, 수동 입력, 브리핑 팩, 예측 장부(5장) |
| `engine/` | 196 | PEOS 분석 엔진 Python 패키지(6장) |
| `scripts/` | 85 | 수집기, 보고서 생성기, 메일 발송, 분석 스크립트(6장) |
| `report/` | 574 | 생성된 보고서. 월간 PEOS, 브리핑, 주거 엑셀과 HTML(8장) |
| `docs/` | 133 | GitHub Pages 정적 사이트와 설계 문서(8장) |
| `config/` | 7 | PEOS 설정 YAML(9장) |
| `monitoring/` (루트) | 12 | 수출입·코스피 상관관계 차트와 표. 관세청 루틴이 갱신 |
| `tests/` | 136 | pytest(69개 모듈). 브리핑 루틴은 발행 전에 반드시 통과시켜야 한다 |
| `.github/workflows/` | 26 | GitHub Actions(7장) |
| `.claude/commands/` | 3 | `/ingest`, `/query`, `/lint` 슬래시 명령 |
| `.claude/skills/` | - | 이 저장소 전용 스킬. `steves-wiki-navigator` 포함(11장) |
| `collectors/`, `core/`, `src/`, `architecture/`, `calendar/`, `prompts/`, `logs/` | - | 초기 구조의 잔재 또는 보조 폴더. 새 작업은 `engine/`·`scripts/`에 둔다 |

---

## 3. `wiki/` 구조

| 하위 폴더 | 수 | 무엇이 있나 |
|---|---|---|
| `index.md` | 122줄 항목 | **모든 페이지 목록.** 새 페이지를 만들면 반드시 한 줄 추가한다 |
| `log.md` | - | append-only 이벤트 로그. `## 당일 log` 맨 아래에만 쓴다. 매일 00:20 KST에 자동 회전 |
| `log-archive/` | 24 | 회전된 과거 로그(월별·일별) |
| `entities/` | 5 | 현재 상태: `user-profile`(사용자, 청약통장, 주거), `my-portfolio`(보유 종목), `sk-hynix`, `automation-infrastructure` |
| `entity-journals/` | 1 | `sk-hynix-journal`: 하이닉스 역사 타임라인 |
| `concepts/` | 130 | 불변에 가까운 판단 프레임. 시나리오 플레이북, 레버리지 위험, 중간선거 역사, 오드리 브리핑 스타일, 플랫폼시티 사실 등 |
| `monitoring/` | 24 | 일일·주간 추적. `*-status.md`는 **Latest Status가 최신 판정**이다. AI CapEx, HBM 사이클, 금리, 광교 청약, 용인 전월세, 주거자금 실행 등 |
| `architecture/` | 11 | 시스템 설계: 지식 모델, 에이전트 워크플로, 보고 프레임, 결정 지능, 자동화 레퍼런스, 이 페이지 |
| `summaries/` | 28 | 소스 1건당 요약(초기 방식. 최근에는 기존 페이지 갱신을 우선) |
| `reference/` | 45 | 참고 자료. `textbook/`은 영어 회의 교재 |
| `reports/` | 9 | 위키 안 분석 보고서(젠슨 황 차트 등) |
| `tools/` | 2 | 웹검색 우회, 회의 녹취 파이프라인 |
| `customer-meetings/` | 38 | **트랙 B(회사 업무) 산출물.** 읽기만 하고 새로 올리거나 메일로 보내지 않는다 |
| `CLAUDE.md` | - | 위키 스키마 |

**자주 찾는 페이지**
- 하이닉스 매도·보유 판단: [시나리오 행동 플레이북](../concepts/scenario-action-playbook.md)(S1~S4 신호, 판정 기록), [레버리지 위험](../concepts/market-cycles-leverage-risk.md), [AI CapEx 둔화 추적](../monitoring/ai-capex-slowdown-status.md), [메모리 가격·가이던스](../monitoring/memory-price-hynix-guidance-status.md)
- 거시: [금리 시나리오](../monitoring/rate-outlook-scenario-status.md), [중간선거 플레이북](../concepts/midterm-history-playbook.md)
- 주거·청약: [광교 A17BL 청약 현황](../monitoring/gwanggyo-a17bl-application-status.md), [주거자금 실행](../monitoring/housing-funding-execution-status.md), [용인 수지 전월세](../monitoring/yongin-suji-rent-status.md), [플랫폼시티 사실](../concepts/yongin-platform-city-project-facts.md)
- 사용자 자체: [사용자 프로필](../entities/user-profile.md), [보유 종목](../entities/my-portfolio.md)
- 말투: [오드리 브리핑 스타일](../concepts/audrey-briefing-style.md). "오드리"라고 부르면 기호와 단락 없이, 귀로 듣는 글로 쓴다

---

## 4. `sources/` — 불변 원자료

**편집·삭제 금지.** 새 파일만 추가한다.

| 종류 | 수 | 내용 |
|---|---|---|
| `*.md` | 323 | 사용자가 붙여 넣은 영상·기사 요약, 웹검색 정리. 파일명 규칙: `주제-화자-YYYY-MM-DD.md` |
| `*.html` | 65 | 과거 일일 모니터 보고서 스냅샷 |
| `*.csv` | 21 | **자동 수집 데이터. 웹검색보다 항상 우선(R1).** |
| 이미지·pdf·xlsx | 약 25 | 사용자 제공 차트, 문서 |

**주요 CSV**

| 파일 | 내용 | 주의 |
|---|---|---|
| `sk-hynix-price-snapshot.csv` | 하이닉스 종가·등락·외국인 보유율·250일 고가 | ⚠️ **NXT 덮어쓰기 버그**: 저녁 수집분이 정규장 종가를 대체거래소 시세로 덮는다. 같은 날짜에 `fetched_at`이 07:xx UTC(16:xx KST)인 값이 정규장 종가다 |
| `sk-hynix-investor-flow.csv` | 투자자별 순매수(외국인·기관·개인, 수량·금액) | 체결 기준 |
| `sk-hynix-adr-quote.csv` | ADR(SKHY) 시세. 1 ADR = 본주 1/10주 | 프리미엄 30% 이상이 흔함 |
| `portfolio-holdings.csv` | 계좌별 보유(일반·ISA·IRP·하나증권 수동) | 19:10 KST 동기화 |
| `macro-series.csv` | FRED/ECOS 거시 시계열(미 금리, 환율, 브렌트, 선행지수 등) | `series` 열로 구분 |
| `monthly-price-history.csv`, `daily-price-history.csv` | 코스피 등 장기 가격 | 계절성·상관 계산에 사용 |
| 그 밖 | 신용잔고, 공매도, 분기 실적, 하이퍼스케일러 CapEx, 병목 가격, 실행 로그 | - |

---

## 5. `data/`

| 하위 | 역할 |
|---|---|
| `raw/`, `normalized/` | API 원자료와 정규화 결과(BLS, ECOS, FRED, KOSIS, OECD, IMF, MOTIE 등) |
| `manual_inputs/` | 자동 수집이 안 되는 값의 수동 입력. **`execution_log.csv`**(사용자 매도 체결 기록), `execution_plan.yaml`, `subscription_notices.yaml`(청약 공고), `economic_calendar_2026.yaml`, `market_holidays_2026.yaml`, `exports_preliminary.yaml`(관세청 잠정치) 등 |
| `wiki_digest/` | 위키 판단을 보고서에 싣는 브리지 YAML 16개. 위키 monitoring 판정이 바뀌면 같은 커밋에서 같이 갱신 |
| `briefing/` | 브리핑 팩(`pack_AM.md` 등)과 `compass.yaml`(추적 질문 T1~T6) |
| `predictions/` | 브리핑 예측 장부. ⚠️ 채점 버그(아래 12장) |
| `daily_signals/`, `peos_daily_history.csv`, `snapshots/` | PEOS 신호 이력과 월별 payload 스냅샷 |
| `health/`, `report_watchdog/` | 데이터 건강 점검, 보고서 감시 결과 |

---

## 6. 코드: `engine/`과 `scripts/`

**`engine/`** (PEOS 패키지, `PYTHONPATH=.`로 실행)

| 모듈 | 역할 |
|---|---|
| `report/` | 월간·일간 PEOS 보고서. `run.py` 진입점, `payload.py`, `markdown.py`와 `html_new.py`는 **렌더러가 둘**이라 섹션을 추가할 때 양쪽 다 고친다. `weekly_analysis.py`, `signal_recorder.py`는 **수정 금지 영역**(루트 CLAUDE.md) |
| `briefing/` | 아침·저녁·주말 브리핑 팩 생성. `scenario.py`(⑫ 시나리오 점검), `ledger.py`(예측 장부), `compass.py`(나침반), `calendar.py`, `midterm_levers.py` |
| `macro/`, `fx/`, `rate_analysis/` | 거시 국면, 환율 국면, 금리 |
| `valuation/` | `hynix_band.py`: P/E 밴드. **수정 금지**(log10 기반 의도적) |
| `real_estate/`, `personal/`, `exposure/`, `execution/` | 부동산, 개인 자금, 노출도, 실행 계획 |
| `health/`, `scoring/`, `rule/`, `action/` 등 | 데이터 건강, 점수, 규칙, 행동 엔진 |

**`scripts/`** 주요 파일
- 수집: `daily_report.py`(하이닉스 시세·수급), `portfolio_holdings.py`, `macro_data.py`, `investor_flow.py`, `collect_core10.py`, `sec_edgar_capex.py`, `collect_us_labor_outlook.py`
- 브리핑: `build_briefing.py --slot AM|PM|WEEKEND`, `compass.py`, `publish_briefing.py`, `send_pending_briefings.py`
- 메일: `send_report_email.py`, `send_subscription_report_email.py`(트랙 A, GitHub Secrets만 사용)
- 운영: `push_with_retry.sh`(**push는 항상 이것으로**), `safe-sync-main.sh`, `log_rotate.py`, `data_health_check.py`, `report_watchdog.py`
- 분석: `scripts/analysis/`(주거 엑셀 생성기 `build_housing_cashflow_plan.py`, 광교 일정표 `build_gwanggyo_application_schedule.py` 등), `correlation_analysis.py`, `hbm_cycle_score.py`, `regime_engine.py`

---

## 7. 자동화 — 무엇이 언제 도나 (KST)

### 7-1. GitHub Actions 스케줄 (cron은 UTC, 아래는 KST로 환산)

| 워크플로 | KST | 하는 일 |
|---|---|---|
| `subscription-monitor` | 매시 07분·37분 | 청약 공고 감시 |
| `report-watchdog` | 매시 23분 | 보고서 생성 실패 감시 |
| `data-health-check` | 홀수 시 20분(2시간마다) | 데이터 신선도 점검 |
| `log-rotate` | 00:20 | `wiki/log.md` 일자별 회전 |
| `real-estate-sync` | 03:00 | 부동산 실거래 등 |
| `macro-data-sync` | 05:15, 07:10 | 거시 시계열 |
| `core10-collect` | 06:30 | 핵심 10개 지표 |
| `sk-hynix-daily-report` | 07:00, 10:00, 19:00 | 하이닉스 시세·수급·ADR CSV와 자동 리포트 |
| `subscription-daily-report` | 07:10 | 청약 일일 보고서 메일 |
| `daily-peos-report` | 07:30 | PEOS 일일 보고서(HTML, 메일) |
| `daily-clock-report` | 08:00 | 투자시계 보고서 |
| `portfolio-holdings-sync` | 19:10 | 계좌 보유 동기화 |
| `exports-price-correlation` | 19:30 | 수출-주가 상관 차트 |
| `sec-edgar-capex` | 화 06:00 | 빅테크 CapEx 공시 |
| `us-labor-outlook-sync` | 월 07:00 | 미국 고용 전망 |

**push 트리거**: `briefing-email`. `report/briefing/*.md`가 main에 push되면 HTML을 만들어 메일로 보낸다.

**수동 실행 전용(workflow_dispatch)**: `api-probe`, `ecos-lookup`, `income-pattern-trace`, `kis-etf-pdf-probe`, `kosis-catalog`, `kosis-lookup`, `molit-diagnostic`, `monthly-peos-report`, `network-diagnostic`, `subscription-schema-probe`

### 7-2. Claude 예약 루틴 (클라우드 세션이 직접 작성)

| 루틴 | KST | 하는 일 |
|---|---|---|
| PEOS 아침 브리핑 v3 | 월~금 08:00 | `build_briefing.py --slot AM` → `report/briefing/YYYY-MM-DD-AM.md` 작성 → pytest → push → Actions가 메일 발송 |
| PEOS 저녁 브리핑 v3 | 월~금 19:40 | 같은 흐름, PM |
| PEOS 주간 전망 v3 | 토 07:30 | WEEKEND |
| 관세청 수출입 잠정치 | 매월 11일·21일 13:00~18:00 매시 | 웹검색 → `exports_preliminary.yaml` → 상관 차트 재생성 |

브리핑 루틴은 팩(`data/briefing/pack_*.md`)만 근거로 쓰고, 매수·매도 지시를 금지한다(R4). 추적 질문은 [briefing-compass](../concepts/briefing-compass.md)가 이어 준다.

### 7-3. 메일 흐름

루틴과 세션은 마크다운을 만들어 push까지만 한다. 메일은 GitHub Actions가 Secrets(`GMAIL_ADDRESS` 등)로 보낸다. **트랙 A만 해당**한다.

---

## 8. 산출물: `report/`와 `docs/`

- `report/YYYY-MM-DD.{html,json,md}`, `report/YYYY-MM.html`: PEOS 일간·월간 보고서
- `report/briefing/`(177개): 아침·저녁·주말 브리핑 마크다운과 HTML, `sent.log`(메일 발송 기록)
- `report/housing/`: 주거 자금 엑셀(`housing-cashflow-plan-2026-10-31.xlsx`), 광교 청약 일정표 엑셀, 청약 실행 가이드 HTML
- **HTML 보고서는 덮어쓰지 않는다.** 파일명에 날짜와 시간을 넣어 새로 만든다(wiki/CLAUDE.md 7-4)
- `docs/`: GitHub Pages(`report.html`, `peos-daily.html`, `real-estate-daily.html`, `subscription-monitor.html`, `reports-index.html`)와 설계 문서

---

## 9. `config/`

`user.yaml`(사용자 프로필, 이사 기한), `portfolio.yaml`(보유·청약통장), `rules.yaml`·`thresholds.yaml`(모든 점수 기준과 숫자), `report.yaml`(섹션 순서), `schedule.yaml`, `api.yaml`(데이터 소스 목록. 비밀값 없음, 환경변수 이름만)

---

## 10. 진행 중인 사용자 과제 (2026-11-07 기준, 바뀌면 갱신)

| 과제 | 상태 | 근거 페이지 |
|---|---|---|
| 하이닉스 매도 | T1 13주 + 연기분 12주 = **25주 미매도.** 11/5 S3 확정(종가 1,273,000), 11/6 서킷브레이커(종가 1,138,000). 실적 쪽 S3 신호는 0개. 사용자가 물타기를 언급했다. 오드리 권고: 공포 매도·물타기 모두 보류. 계약금은 당첨 시에만 필요하고 대출로 메울 수 있다 | [시나리오 플레이북](../concepts/scenario-action-playbook.md) |
| 광교 A17BL 청약 | **11/10(화) 일반공급 1순위** 84B, 거주구분 기타경기. 무주택 세대주와 3년 이상 무주택 확인됨(11/6). 남은 확인: 2024-10-30 이전부터 경기 계속 거주, 납입 인정 금액. 발표 11/17, 서류 11/19~24, 계약 12/21~23 | [광교 현황](../monitoring/gwanggyo-a17bl-application-status.md), [실행 가이드](https://claude.ai/artifact/XCJDUqAPArxhKMRR3z1tsh) |
| 2월 이사 | 현 전세 2027-02-22 만료. 전세(성원상떼빌 5.2억 권고)와 월세(하이브엘 2억/300만) 중 미결정 | [주거자금 실행](../monitoring/housing-funding-execution-status.md), [전월세](../monitoring/yongin-suji-rent-status.md) |
| 플랫폼시티 | 공공분양 공고는 빨라야 2028년 초(GH 게시판 선행지표, 신뢰도 중) | [플랫폼시티 사실](../concepts/yongin-platform-city-project-facts.md) |
| 고정 원칙 | IRP·DC 미사용, 하나증권 마크업 67주는 2027-02까지 보유, 하이닉스 추가 매수는 쓸 날짜 없는 돈으로만 | [사용자 프로필](../entities/user-profile.md) |

---

## 11. 반드시 지킬 규칙 요약

- **트랙 A/B**
  - 트랙 A: 경제판단, 개인 자산. GitHub 업로드와 메일 허용.
  - 트랙 B: 회사 업무. 업로드·메일 금지. 애매하면 B로 본다. `dispatch.sh`, `upload_*.py`, CXL 산출물은 재도입 금지.
- **작업 프로토콜**: 계획을 먼저 보이고, 진행 단계를 표시하고, 단위마다 완료를 보고한다.
- **R1** 실측 우선(KIS CSV > 사용자 데이터 > 웹검색). **R3** 데이터가 없으면 "판단 불가"이고 안전한 것이 아니다. **R4** 엔진 신호가 공식이다. Claude는 의견을 표시해서 말하고, 결정은 사용자가 한다.
- **확인하지 않은 사실을 단정하지 않는다.** 사용자는 "이건 확인된 거야?"라고 자주 묻는다.
- **sources/는 불변.** 위키 페이지는 새로 만들기보다 기존 페이지 갱신을 우선한다. 새 페이지는 index.md에 등록한다.
- **log.md는 맨 아래 append만.** 충돌이 나면 두 줄을 모두 보존한다.
- **push는 main에, `bash scripts/push_with_retry.sh main`으로.** 다른 세션의 자동 커밋이 수시로 들어오므로 작업 전 `git pull --rebase origin main`을 한다.
- **답변 스타일**: 한국어, 깊이 조사하되 간결하게. "오드리" 호출 시에는 [오드리 브리핑 스타일](../concepts/audrey-briefing-style.md)을 따른다.
- **수정 금지 영역**(루트 CLAUDE.md): `engine/valuation/hynix_band.py`, `engine/report/signal_recorder.py`, `engine/report/weekly_analysis.py`, PEOS 섹션 순서

---

## 12. 알려진 문제 (미해결, 사용자 승인 대기 포함)

1. **NXT 덮어쓰기**: 시세 수집이 저녁에 정규장 종가를 대체거래소 시세로 덮는다(11/3, 11/4, 11/5 재발). 수정 승인 대기.
2. **예측 채점 버그**: `engine/briefing/ledger.py`의 `resolve_due`가 검증일 장 전에 전일 값으로 채점한다. P0126·P0128 재채점이 필요하다. 승인 대기.
3. **S4 판정 방식**: 블루 스윕을 결과가 아니라 시장 반응(10년물 5.3%, VIX 30, 브렌트 120)으로 판정하도록 바꾸는 안이 승인 대기 중이다.
4. **문서 드리프트**: `automation-pipeline-reference.md`(워크플로 17개 시점)와 `llm-wiki-file-inventory.md`(sources 154개 시점)가 오래됐다. 이 페이지가 최신이다.
5. `wiki/Jensen Huang Graph/`라는 빈 폴더가 있다. 공백이 들어간 폴더 이름이라 스크립트가 깨질 수 있다.

---

## Sources

- 2026-11-07 main 직접 조사(`ls`, `find`, `.github/workflows/*.yml` cron 추출, Claude 예약 루틴 목록 조회)
- [automation-pipeline-reference.md](automation-pipeline-reference.md), [llm-wiki-file-inventory.md](../llm-wiki-file-inventory.md), [log-operating-policy.md](../concepts/log-operating-policy.md), [automation-strategy-and-delivery-boundary.md](../concepts/automation-strategy-and-delivery-boundary.md)
- 루트 `CLAUDE.md`, `wiki/CLAUDE.md`
