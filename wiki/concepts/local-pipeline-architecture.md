---
title: 로컬 파이프라인 구조 — POET / CXL (Task Scheduler)
created: 2026-08-27
updated: 2026-08-27
tags: [architecture, automation, local, task-scheduler, must-read]
---

# 로컬 파이프라인 구조 — POET / CXL

> GitHub Actions(PEOS)가 아닌 **로컬 Windows Task Scheduler로 도는
> 두 파이프라인**의 단일 출처. 운영 원칙은
> [automation-strategy-and-delivery-boundary.md §8](automation-strategy-and-delivery-boundary.md#8-로컬-파이프라인-원칙-2026-08-27-신설)를
> 먼저 읽을 것. 이 문서는 구조와 파일 매핑을 다룬다.

---

## 0. 왜 별도 문서인가

이 저장소의 자동화는 두 세계로 나뉜다:

| | GitHub Actions (PEOS) | 로컬 Task Scheduler (POET/CXL) |
|---|---|---|
| 실행 환경 | ubuntu-latest | Windows 회사망 + 사내 vLLM |
| 동기화 | checkout이 매번 fresh | **명시적 git pull 필요** (§8.1) |
| LLM | 없음(순수 Python) | Claude Code `-p` (사내 게이트웨이) |
| 업로드 | GitHub 커밋 + 이메일 | **로컬 파일 생성만, push 금지** |
| 저장 | `report/` | `Results/<리포트명>/` |

두 세계의 원칙이 다르므로, 로컬 쪽을 이 문서에서 다룬다.

---

## 1. 파이프라인 개요

### POET (`run_daily.bat`) — 7단계 (2026-08-28 개편)
```
P0:   git fetch + pull --rebase (최신 위키/CSV 동기화)
P0.5: python poet_direct_collect.py → SEC EDGAR 직접수집 (봇 멈춤 보충)
        SEC_EDGAR_INSECURE=1 (회사망 MITM 우회 — 로컬 only)
        SEC_EDGAR_CONTACT (User-Agent email)
P1:   python poet_phase1_extract.py → poet-macro.json
P2:   python poet_phase2_extract.py → poet-hynix.json
P3:   python poet_phase3_extract.py → poet-decisions.json
P3.5: python poet_data_freshness.py → poet-freshness.json
        (시간/요일/미국시차/USD-KRW/데이터 기준일+지연/직접수집 내역)
P4:   3분할 순차 — prep (hbm-only + 3 scopes web fetch) + 4a/4b/4c
        4a: macro-YYYY-MM-DD.html    (macro.json + poet-web-macro.md + freshness)
        4b: semis-YYYY-MM-DD.html     (hynix.json + hbm-only + poet-web-semis.md + freshness)
        4c: strategy-YYYY-MM-DD.html  (decisions.json + poet-web-strategy.md + freshness)
        → Results/poet-daily/
```

**데이터 신선도 원칙 (2026-08-28 신설):**
- 봇 pull → 직접수집 보충 → freshness 투명 표시 → 보고서에 기준일 명시
- "잡이 exit 0인 것은 데이터 도착 증거가 아니다" — artifact 날짜로 측정
- 모든 숫자 옆에 as-of(기준일) 부착, 지연 큰 항목(AMKR 1767일 등) 명시 경고

### CXL (`run_cxl_daily.bat`) — 2단계
```
Step 1: git fetch + pull --rebase (위키 동기화)
Step 2: claude -p (search.py + fetch_urls.py → MD/HTML)
    → Results/cxl-daily/cxl-daily-report-YYYY-MM-DD-HHMM.html
```

---

## 2. 파일 매핑 (Execute/ 통합 후)

2026-08-26 리팩토링으로 BAT/PS1이 흩어져 있던 것을 `Execute/`로 통합.
상세는 [execution-layers-consolidation.md](execution-layers-consolidation.md).

### POET 구성요소
| 파일 | 역할 |
|---|---|
| `Execute/run_daily.bat` | Task Scheduler 진입점. P0-P4 순서 제어 |
| `Execute/run_poet_claude_bounded.ps1` | P4 Claude 실행 래퍼(hang-fix, timeout) |
| `scripts/poet_phase1_extract.py` | P1: 거시 국면/투자시계/지표 7종 → JSON |
| `scripts/poet_phase2_extract.py` | P2: SKH/CapEx/AI변두리/Valuation → JSON |
| `scripts/poet_phase3_extract.py` | P3: HBM/Panic/CXL/부동산/Trump → JSON |
| `prompts/poet-phase4-headless.txt` | P4 Claude 프롬프트 (저장 경로·구조·무결성 원칙) |
| `.claude/tmp/poet-{macro,hynix,decisions}.json` | 중간 산출물 (Phase 1-3 결과) |

### CXL 구성요소
| 파일 | 역할 |
|---|---|
| `Execute/run_cxl_daily.bat` | Task Scheduler 진입점. 2단계 제어 |
| `Execute/run_cxl_claude_bounded.ps1` | Claude 실행 래퍼 (프롬프트 경로 hard-coded) |
| `prompts/cxl-daily-update-headless.txt` | Claude 프롬프트 (저장 경로 포함) |
| `scripts/cxl_fetch_urls.py` | DuckDuckGo search + HTML fetch → MD |
| `scripts/search.py` | 검색 우회 (사내 vLLM web_search 오류 대응) |

### 레거시 (참고용, 스케줄러 대상 아님)
- `Execute/cxl_daily_routine.bat` — 과거 산출물. 헤더에 "실제 실행은
  run_cxl_daily.bat" 명시. 수정 시 run_cxl_daily.bat 쪽을 고칠 것.
- `Execute/cxl_daily_v2_routine.bat` — 더 옛날 버전.

---

## 3. JSON 스키마 (Phase 1-3 산출물)

Phase 4 프롬프트와 Phase 1-3 스크립트가 공유하는 계약. **이 스키마가
바뀌면 양쪽을 같이 고쳐야 한다** (한쪽만 고치면 깨진 데이터/보고서).

### poet-macro.json
- `macro_regime`: 이 페이지(G/I/L) 대표 국면 (예: "stagflation")
- `macro_regimes_all`: 세 시스템 판정 dict (PEOS는 제외 — 별도 파이프라인)
- `investment_clock`: `{phase, favor_asset, updated}` (docs/index.html에서 추출)
- `macro_series`: 7종 시계열 (kr_base_rate, kr_usdkrw, us_fed_funds,
  us_cpi, us_unemployment, us_brent, us_gdp_real) 각 latest/prev/history(2)

### poet-hynix.json
- `sk_hynix_checkpoints`: `{foreign_20d, adr_mismatch, hold_rate_pct}`
- `capex`: 4개사 (AMZN/GOOGL/META/MSFT) 각 company/quarter/capex_usd/filed_date
- `ai_periphery`: 8개사 (Vertiv/GE Vernova/Amkor/Astera Labs/Credo/Coherent/
  Lumentum/Supermicro) 각 revenue_usd/backlog_rpo/layer
- `valuation`: `{latest: {date, pe, kospi, vs_20y_mean, band, caveat}, anchor_date}`

### poet-decisions.json
- `hbm_cycle`: `{total_score, collapse_conditions, collapse_total}` — **axes 없음**
- `panic_signals`: `{status, tier1}`
- `cxl_signals`: `{HBF, CXL, CMM, recent_ingest?}`
- `real_estate`: `{latest_price, latest_volume}`
- `trump_tracker`: 5개 카테고리 (정치/경제/전쟁/외교/이민/경쟁구도)

---

## 4. 데이터 추출 규칙 (Phase 1-3)

> **절대 원칙**: 위키/HTML/CSV **실제 구조를 확인하고 정규식을 작성**한다.
> "아마 이런 패턴일 것"이라는 추측으로 정규식을 만들지 않는다
> (CLAUDE.md "외부 파라미터 작성 전 docs 먼저 읽기 — 추측 금지").

2026-08-27 이전 버그 (전부 추측 기반 정규식이 원인):
| 필드 | 버그 | 원인 |
|---|---|---|
| `macro_regime` | `"00"` (쓰레기) | 개행 제외 안 해 front matter까지 매칭 |
| `investment_clock.phase` | `N/A` | `<h3>` 구조라고 가정했으나 실제는 `<div class="phase-banner">` |
| AI periphery | 5개사 누락 | 회사명을 "Amkor Technology" 등 긴 형태로 가정, 실제는 "Amkor" |
| `backlog_rpo` | 전부 빔 | `Receivable`/`DeferredRevenue` 태그 가정, 실제는 `RevenueRemainingPerformanceObligation` |
| `hbm_cycle.axes` | 한글 깨짐 | 산문형 위키에서 무리하게 축별 점수 추출 → **제거 결정** |
| `trump_tracker` | 4개 "미확인" | 섹션 본문 기호 매칭, 실제는 스코어보드 표에 기호 있음 |

**교훈**: 추출 스크립트를 고치기 전에 반드시 원본 파일의 실제 구조를
`python -c`로 확인하고 정규식을 테스트할 것.

---

## 5. 보고서 생성 규칙 (Phase 4 프롬프트)

### 5.1 3분할 구조 (2026-08-28 신설 — 이전 단일 보고서에서 3개로 분할)

**배경**: 단일 보고서(`poet-phase4-headless.txt`)는 Haiku 컨텍스트 압박으로
depth·분량이 얕아지는 문제가 있었다. 해결책으로 **입력 JSON을 1/3로
줄여 3개 보고서로 분할** + 모델 Haiku→Sonnet 승격 + "뼈대(JSON)+살(웹서치)"
구조 도입.

**3개 보고서 (의미 단위 분할 — 데이터 출처 경계 = 의미 경계):**

| # | 보고서 | 프롬프트 | 입력 JSON | 웹서치 MD | 신선도 | 산출물 |
|---|--------|---------|-----------|-----------|--------|--------|
| 4a | 📊 거시 브리프 | `prompts/poet-phase4a-macro.txt` | `poet-macro.json` | `poet-web-macro.md` | `poet-freshness.json` | `macro-YYYY-MM-DD.html` |
| 4b | 💾 반도체 브리프 | `prompts/poet-phase4b-semis.txt` | `poet-hynix.json` + `poet-hbm-only.json` | `poet-web-semis.md` | `poet-freshness.json` | `semis-YYYY-MM-DD.html` |
| 4c | 🎯 전략 브리프 | `prompts/poet-phase4c-strategy.txt` | `poet-decisions.json` (panic/cxl/real_estate/trump) | `poet-web-strategy.md` | `poet-freshness.json` | `strategy-YYYY-MM-DD.html` |

**hbm_cycle 키는 보고서2(반도체) 전용** — `decisions.json` 전체가 겹치지
않도록 `scripts/poet_extract_hbm_only.py`로 `hbm_cycle`만 빼서
`poet-hbm-only.json` 생성. 보고서3은 `hbm_cycle`을 경계 참조용으로만 쓰고
상세는 보고서2에 위임.

### 5.2 "뼈대 + 살" 구조 (이 보고서의 핵심 차별점)

- **뼈대**: Phase 1-3 JSON (정량, 무결성 대상)
- **살**: `scripts/poet_fetch_urls.py`가 DuckDuckGo search → HTML fetch →
  MD 변환. 각 scope별 쿼리 세트 내장 (macro/semis/strategy 각 12쿼리 +
  주말 전용 2쿼리/scope — 2026-08-28 확장).
- **토큰 예산 관리 (2026-08-31 교정)**: 쿼리 12개 × 기사 5개 × 본문 8000자
  = 480K자 → 128K 컨텍스트 초과(`ContextWindowExceededError`). 따라서
  **기사당 상위 3개만 fetch** + **본문 3500자 절단**(핵심 앞부분).
  결과: 각 scope MD ~15-18K 토큰으로 안정. **교훈: 토큰 예산 문제는
  "입력 줄이기"로 해결 — "입력 늘리기"(쿼리 확장)는 depth가 아니라
  컨텍스트 초과 실패를 부름.**
- **회사망 SSL 우회**: `requests.get(..., verify=False)` — 회사망 프록시
  MITM 인증서 때문에 verify=True면 전부 실패 (2026-08-28 확인). 이전
  `cxl_fetch_urls.py`는 verify 안 달아서 기사 본문을 못 가져오고 있었음.
- **subprocess 인코딩**: `poet_fetch_urls.py`의 `subprocess.run`에
  `encoding='utf-8', errors='replace'` 명시 필수 — BAT 환경에서
  `PYTHONIOENCODING`이 자식으로 안 넘어가 cp949 디코딩 실패 → 0건 사고.
- **이전 보고서 diff**: 각 보고서는 "지난 발행 대비 변화" 섹션 포함 —
  이전 `macro-*.html`/`semis-*.html`/`strategy-*.html` (또는 구
  `daily-brief-*.html`)을 Read하여 변화 강조.

### 5.2.1-a 렌더링 주체: 자식 에이전트 → 메인 세션 직접 (2026-08-31 전환)

**문제**: `claude -p --dangerously-skip-permissions` 자식 에이전트는
128K 컨텍스트에서 시스템 프롬프트 + 도구 정의 + CLAUDE.md ≈ 50K가
고정으로 차지. 입력(웹 MD 15-18K + JSON)을 줄여도 **64K 입력 한계**
(`ContextWindowExceededError`)에 도달 — "정적 분석" 쓰레기 보고서 양산.

**검증된 해결 (2026-08-31)**: **메인 세션이 HTML을 직접 작성**.
- 메인 세션은 시스템 오버헤드가 이미 로드된 상태 — 추가 입력만큼만 토큰 소비
- decisions.json(695B) + freshness.json(4KB) + 3 웹 MD(20-50KB) = 약 80KB
  입력을 메인 컨텍스트가 충분히 흡수 → 3개 HTML(40-136KB) 품질 산출 성공
- 일일 3-split(약 30K 출력)은 128K 윈도우 안에 여유 — 세션 길어지면
  컨텍스트 압축 발생하므로 **"매번 새 세션에서 파일 기반 맥락" 원칙** 유지

**자동화 구조** (`scripts/poet_run_pipeline.py`가 1단계 무인 수행):
```
[1단계 — 무인 Python] poet_run_pipeline.py
  P0.5 direct_collect → P1 phase1/2/3 extract → P1.5 hbm_only
  → P3.5 freshness → P4 fetch_urls (3 scopes, 30s 쿨다운)
  → 준비물 8개 비축 (.claude/tmp/poet-*.json + poet-web-*.md)
[2단계 — 메인 세션 직접] .claude/prompts/poet-daily-render.md
  메인 세션이 8개 준비물 Read → strategy/semis/macro HTML 직접 작성
  → 자식 에이전트 64K 한계 회피, 품질 보장
```

**작성 순서 (토큰 집약도 역순)**: strategy(§7 3문단 포함) → semis → macro.
**원칙**: "데이터 비축"까지 무인, "HTML 작성"은 메인 세션 직접 — 품질 우선.

### 5.2.1 시간·요일·미국시차 컨텍스트 + "의견 및 해석" (2026-08-28 신설)

**사용자 피드백 "별로 가치가 안 느껴진다"에 대한 구조 개선:**

1. **시간 컨텍스트** (freshness.json → HERO 헤더):
   - 오늘 요일/주말 여부 — 주말이면 "데이터 갱신 둔화, 주간 정리 관점" 안내
   - 미국 시차 (KST 13시간 선행) — 미국 데이터는 전일 장 마감분
   - USD/KRW 환율 — 달러 금액 옆에 원화 환산 병기 (예: `$173B (≈ 244조 원)`)
2. **데이터 신선도 투명 표시**: 모든 숫자 옆에 as-of(기준일) 부착,
   지연 큰 항목(AMKR 1767일, MSFT 124일 등) 경고 라벨.
3. **"의견 및 해석" 섹션** (각 보고서의 핵심 차별 섹션):
   - 3단락: (1) 인과 사슬 해석 (2) 데이터 신선도 한계 + 직접수집 보충 (3) 개인 의견
   - 단순 데이터 나열이 아닌 **분석가 해석** — 콜아웃박스로 분리
   - "필자 의견" 명시 — 사실과 분리

### 5.3 데이터 무결성 절대 원칙 (각 프롬프트 최상단)

1. **JSON에 없는 숫자는 절대 지어내지 않는다.**
2. **`hbm_cycle.axes`는 없다** — 축별 점수표 금지, 총점/붕괴조건만.
3. **CCI/위기지수는 없다** — N/A 또는 칸 제거. 숫자 만들지 마라.
4. **SKH 주가/수출 실측치는 JSON에 없다** — "SKH 가격 X원" 지어내기 금지.
5. **Amazon CapEx 2017년이면 ⚠️ 경고 라벨** — "최신 분기 미수집" 솔직 표시.
6. **backlog 빈 회사는 `공시 미태깅`** — 0이나 임의 숫자 금지.
7. **Trump "미확인"은 "미확인"으로** — "중립" 해석 금지.
8. **웹서치 숫자는 출처 부착** — `[출처: 기사명](URL)` 형식. 출처 없는
   숫자 = 지어낸 것 = 금지. (3분할 신설 규칙)

### 5.4 프롬프트가 곧 저장 위치 (BAT는 경로를 모른다)

- POET: `Results/poet-daily/{macro,semis,strategy}-YYYY-MM-DD.html`
- CXL: `Results/cxl-daily/cxl-daily-report-YYYY-MM-DD-HHMM.html`

**레거시**: `prompts/poet-phase4-headless.txt` (단일 보고서용, 3분할 전)
는 deprecated — `daily-brief-YYYY-MM-DD.html` 생성. 스케줄러는 더 이상
이 프롬프트를 호출하지 않는다.

---

## 6. Task Scheduler 등록

태스크가 소멸하면 아침 자동 실행이 안 된다 (2026-08-27 발견 — PEOS는
GitHub Actions이라 살아있었지만 POET/CXL 로컬 태스크가 전멸했음).

```cmd
:: POET (06:00 KST) — run_daily.bat
schtasks /create /tn "Steve_Daily_POET" /tr "C:\Users\2053437\Execute\run_daily.bat" /sc daily /st 06:00 /ru SYSTEM /f

:: CXL (06:30 KST) — run_cxl_daily.bat
schtasks /create /tn "Steve_CXL_Daily_Update" /tr "C:\Users\2053437\Execute\run_cxl_daily.bat" /sc daily /st 06:30 /ru SYSTEM /f
```

**PEOS는 GitHub Actions (`daily-peos-report.yml`, 21:00 UTC = 06:00 KST)
이므로 로컬 태스크 불필요.**

---

## 7. 로그와 진단

- 실행 로그: `.claude/logs/poet-daily-{STAMP}.log`, `cxl-daily-{STAMP}.log`
- latest 포인터: `.claude/logs/poet-daily-latest.log`, `cxl-daily-latest.log`
- retention: 최근 30개 보관, 이후 자동 삭제
- **성공 확인은 로그가 아니라 산출물 날짜** (§8.1 / §2 원칙):
  `ls -la Results/poet-daily/{macro,semis,strategy}-$(date +%Y-%m-%d).html`
  (3개 모두 오늘 날짜여야 성공 — 1개라도 빠지면 부분 실패)

---

## 관련 문서

- [automation-strategy-and-delivery-boundary.md §8](automation-strategy-and-delivery-boundary.md#8-로컬-파이프라인-원칙-2026-08-27-신설) — 로컬 파이프라인 운영 원칙 (데이터 신선도·무결성·저장경로)
- [execution-layers-consolidation.md](execution-layers-consolidation.md) — Execute/ 폴더 통합 내역
- `wiki/architecture/reporting-framework.md` — 리포트 구조 (GitHub Actions 쪽)
- `prompts/poet-phase4-headless.txt` / `prompts/cxl-daily-update-headless.txt` — 실제 프롬프트
