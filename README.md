# Wiki-Driven LLM Report Generation & Distribution Platform

공식 데이터와 웹 리서치를 수집·합성한 **영속 지식베이스(wiki)** 를 기반으로, 
**구조화된 보고서를 자동생성·배포하는 LLM 시스템**입니다.

다음 보고서들을 자동 생성하고 스테이크홀더에게 전송합니다:
- 📊 **거시경제·금융 시장 분석** (매월 리포트)
- 💾 **반도체·AI 인프라 시장 모니터링** (주기적 업데이트)
- 📈 **개별 종목 팩트체크 & 재평가** (사건 기반 동적 보고서)
- 🔗 **AI 가치사슬 주변사 조사** (공급망 리스크 조기 경보)
- 📉 **시장 신호 패턴 분석** (패닉 회복, 레버리지 사이클 추적)

**핵심 아키텍처:**
```
sources/          → 원본 자료 (뉴스, 메모, 웹 스크린샷, 수치)
wiki/             → LLM 유지 지식베이스 (entities, concepts, summaries)
scripts/          → 데이터 수집 (CSV, SEC EDGAR, API) + 지표 계산
reports/          → 생성 보고서 (Markdown, HTML, JSON)
.github/workflows/→ 자동 스케줄 (매일/주간/월간 실행)
```

## 보고서 사례 & 생성 방식

| 보고서 유형 | 생성 빈도 | 저장 위치 | 예시 |
|---|---|---|---|
| SK하이닉스 팩트체크 & 재평가 | 사건 기반 | `sources/`, `wiki/entities/` | [8/7 반등 시나리오](sources/sk-hynix-factcheck-rebound-2026-08-07.html) |
| AI 공급망 주변사 조사 | 주간 | `wiki/concepts/` | [AI 가치사슬 모니터링](wiki/concepts/ai-value-chain-periphery-monitor.md) |
| 시장 신호 분석 | 월간 | `docs/report.html` | GitHub Pages 정적 리포트 |
| SEC EDGAR 자동 수집 | 일간 | `data/normalized/` | CapEx, 10-K/Q filings 추출 |

**생성 파이프라인:**
```
데이터 수집            CSV + Web + SEC EDGAR API
   ↓
Wiki 합성             entity/concept 페이지 통합 분석
   ↓
지표 계산             Z-score, 신호 감지, 시계열 추적
   ↓
보고서 렌더링         Markdown, HTML 구성 & 스타일
   ↓
배포                   Email, GitHub Archive, Artifact
```

## 시스템 구조

**1. 데이터 수집 계층 (Multi-Source)**
```
scripts/
  daily_report.py           → CSV 분석, Z-score 스케일링, 신호 감지
  sec_edgar_periphery.py    → SEC XBRL 자동 수집 (AI 공급망 분석)
  
data/
  raw/                      → API 응답, 웹 스크린샷 (gitignored)
  normalized/               → 정규화된 CSV, JSON (추적됨)
```

**2. Wiki 지식베이스 (LLM 유지)**
```
sources/                   → 원본 자료 (불변)
wiki/
  entities/               → 개인/기업/상품 프로필 (SK하이닉스, CXMT 등)
  concepts/               → 반복되는 주제/신호 (시장사이클, 공급망, 신호 패턴)
  summaries/              → 출처별 요약
  index.md / log.md       → 카탈로그 & 작업 로그
```

**3. 보고서 생성 & 배포**
```
.github/workflows/
  daily-report.yml        → 매일 자동 실행
  sec-edgar-capex.yml     → 주간 SEC 데이터 수집
  
reports/ / docs/          → 생성된 보고서 (HTML, Markdown, JSON)
```

**핵심 특징:**
- ✅ **Wiki-First Design**: 모든 분석의 기반은 지속 갱신되는 wiki
- ✅ **Multi-Terminal Sync**: append-first 설계로 mobile/desktop 동시 작업 충돌 방지
- ✅ **Autonomous Report Generation**: 스케줄 기반 자동 생성 + 사건 기반 동적 생성
- ✅ **Evidence Transparency**: FACT/OPINION 태깅으로 출처 구분
- ✅ **Zero-Fabrication**: 객관적 데이터만 사용, 추측/가설 명시 표시

## 설정 & 배포

### 보고서 배포 채널
| 채널 | 설정 | 설명 |
|---|---|---|
| **GitHub Actions** | `.github/workflows/` | 자동 스케줄 (매일 06:00 KST) |
| **GitHub Pages** | `docs/report.html` | 정적 리포트 (GitHub.com에서 열람 가능) |
| **Email** | `SMTP_HOST`, `GMAIL_APP_PASSWORD` | 스테이크홀더 자동 발송 |
| **GitHub Archive** | `sources/`, `wiki/` | 보고서 원본 저장 (버전 추적) |

### API 키 (선택, 없으면 제한된 기능만 동작)
`.env.example` → `.env`로 복사, 보유한 키만 등록:

| 소스 | 환경변수 | 용도 | 필수 여부 |
|---|---|---|---|
| SEC EDGAR | (사용자 계정만 필요) | AI 공급망 주변사 CapEx 수집 | 선택 |
| GitHub Actions Secrets | 설정에 따름 | workflow 배포 채널 | 선택 |

자세한 설정은 [wiki/entities/automation-infrastructure.md](wiki/entities/automation-infrastructure.md) 참고.

## 구현 현황

**✅ 완성된 기능:**
- Wiki-LLM 패턴 구현 (entities, concepts, summaries, log-rotation 자동화)
- 다중 데이터 소스 수집 (CSV, SEC EDGAR XBRL, 웹 스크린샷)
- 신호 감지 & Z-score 스케일링 (시장 신호 분석)
- 팩트체크 & 재평가 보고서 생성 (개별 종목, 공급망)
- HTML 리포트 렌더링 (스타일 완성, 증거 태깅)
- GitHub Actions 자동 스케줄 (daily, weekly, monthly)
- multi-terminal sync 프로토콜 (append-first 동시 편집 안전성)

**⏳ 계획 중:**
- 고급 시나리오 시뮬레이션 (확률론적 리스크 모델)
- 실시간 대시보드 (vs. 정적 리포트)
- 추가 공급망 소스 (카드사 거래액 추적, 외환거래 신호)

## 자동화 & 배포

### 스케줄된 보고서
| 보고서 | 실행 시간 | 빈도 | 생성 내용 |
|---|---|---|---|
| 시장 신호 분석 | 06:00 KST | 매일 | Z-score 신호, 거시경제 지표, 반도체 동향 |
| AI 공급망 모니터링 | 21:00 UTC (목요일) | 주간 | SEC EDGAR CapEx 수집, 주변사 리스크 |
| 팩트체크 리포트 | 사건 기반 | 필요시 | 개별 종목 재평가, 시나리오 분석 |

### 배포 채널
**Pull 방식 (GitHub Pages):**
- `docs/report.html` — 웹에서 즉시 열람 가능

**Push 방식 (Email/Slack):**
- GitHub Secrets 설정 시 자동 발송 (`SMTP_*` 또는 `GMAIL_*`)
- 스테이크홀더 이메일 목록: `NOTIFY_EMAIL_TO` (GitHub Secrets)

**Archive 방식 (Git 버전 추적):**
- 생성된 보고서 → `sources/` 커밋 (영구 보관)
- Wiki 업데이트 → `wiki/` 커밋 (분석 이력 추적)

자세한 설정은 [wiki/entities/automation-infrastructure.md](wiki/entities/automation-infrastructure.md) 참고.

## 데이터 품질 & 검증

### Wiki 검증
```bash
# wiki/ 전체 일관성 검사 (링크, 태그, 중복 등)
/lint
```

### 신호 품질 테스트
- Z-score 계산 정확도 (이상치 감지)
- 신호 감지 재현성 (같은 조건 → 같은 신호)
- 보고서 렌더링 정확도 (HTML, Markdown 포맷)

### 데이터 소스 상태
- ✅ SEC EDGAR API — 정상 수집 (매주 목요일)
- ✅ GitHub Actions workflow — 자동 실행 검증 됨
- ⏳ 사용자 제공 CSV — 필요시 `data/normalized/` 추가

---

## 빠른 시작: Wiki 작업

### 문서 수집 & 분석 (`/ingest`)
```bash
# 웹 기사, 메모, 스크린샷을 sources/에 추가하면 자동 처리
/ingest sources/some-article.md
# → wiki/entities/ 또는 wiki/concepts/에 LLM이 자동 기록
```

### 질문 및 분석 (`/query`)
```bash
# 현재까지 수집된 정보로 질문 응답
/query "SK하이닉스 HBM 점유율 추세는?"
# → 관련 wiki 페이지 자동 인용 & 업데이트
```

### 일관성 검사 (`/lint`)
```bash
# Wiki 전체 링크/태그/중복 검사
/lint
# → 깨진 링크, 고아 페이지, 모순 발견
```

자세한 사용법: [USAGE.md](USAGE.md) (또는 [SYSTEM-OVERVIEW.md](SYSTEM-OVERVIEW.md) 타 도구 이동시)

## 핵심: Wiki-LLM 기반 보고서 생성

이 시스템의 중심은 [Andrej Karpathy의 "LLM Wiki" 패턴](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)입니다.

**워크플로우:**
1. 사람이 원본 자료(뉴스, 메모, 웹 스크린샷)를 `sources/`에 추가
2. LLM이 읽고 `wiki/`에 entity/concept 페이지로 합성
3. wiki 페이지들이 서로 연결되면서 **지식 그래프** 형성
4. 보고서 생성 시 이 wiki 그래프를 기반으로 **구조화된 분석** 작성
5. 생성된 보고서 → email/GitHub으로 자동 배포

**구조:**
```
CLAUDE.md              ← 스키마 & 워크플로우 정의 (사람이 수정)
sources/               ← 원본 자료 (불변, 버전 추적)
wiki/
  ├─ entities/        ← 개인/기업/상품 프로필 (SK하이닉스, CXMT, ...)
  ├─ concepts/        ← 반복 주제 (시장사이클, 신호 패턴, 공급망 위험, ...)
  ├─ summaries/       ← 출처별 요약
  ├─ index.md         ← 전체 카탈로그
  ├─ log.md           ← 작업 로그 (자동 로테이션, 월별 요약)
  └─ log-archive/     ← 과거 로그 (콜드 스토리지)
```

**사용자 인터페이스:**
- `/ingest <자료>` — 새로운 원본 추가
- `/query <질문>` — wiki 기반 답변 + 자동 기록
- `/lint` — 링크/태그 검증

> ⚠️ **민감정보 주의**: `sources/`, `wiki/`에 회사 전략, 포트폴리오 세부사항 등이 평문 저장되며, 
> 이 저장소는 **public**입니다. 2026-07-15 사용자 승인됨.
