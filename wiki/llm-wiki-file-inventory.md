# LLM Wiki 운영 파일·소스 목록

이 저장소에는 **LLM Wiki 본체**와, 그 안에서 데이터 소스로만 참조되는
**별도의 PEOS/Investment Clock 자동화 시스템**이 함께 있다. 헷갈리지
않게 구분해서 정리한다.

## 1. 스키마·규칙 (뼈대)

| 파일 | 역할 |
|---|---|
| `CLAUDE.md` | 위키의 스키마 정의서 — 레이어 구조(sources/wiki), 페이지 규칙, Ingest/Query/Lint 워크플로를 규정. **모든 작업의 출발점** |
| `SYSTEM-OVERVIEW.md` | 이 LLM Wiki 패턴 자체를 다른 AI 도구에도 재현 가능하도록 설명하는 기술 요약 |
| `USAGE.md` | 처음 쓰는 사람 대상 사용설명서 (Claude Code·GitHub 조작법) |

## 2. `sources/` — 원본 데이터 (불변, 154개 파일)

| 유형 | 역할 |
|---|---|
| `*.md` (77개) | 사용자가 붙여넣은 강의요약·뉴스·리포트 원문 (INGEST 결과물) |
| `*.html` (50개) | 매일 발행되는 Daily Monitor 리포트 스냅샷(아침/장초반/저녁), 참고용 시각자료 |
| `sk-hynix-investor-flow.csv` | GitHub Actions가 KIS API로 수집한 투자자별 매매동향 — **웹검색보다 항상 우선** |
| `sk-hynix-adr-quote.csv` | 〃, ADR(SKHY) 시세 |
| `sk-hynix-price-snapshot.csv` | 〃, 본주 현재가·외국인보유율·250일 최고가 |
| `portfolio-holdings.csv` | 〃, 계좌별(GEN/ISA/IRP/DC) 보유종목 |
| `macro-series.csv` | FRED/ECOS API로 수집한 거시지표 시계열 |
| `*.png/.jpeg` (20개) | 사용자가 제공한 차트 스크린샷 |

## 3. `wiki/` — 지식베이스 (LLM이 유지·관리)

| 파일/폴더 | 역할 |
|---|---|
| `wiki/index.md` | 전체 페이지 카탈로그 — 폴더별로 한 줄씩, 검색 진입점 |
| `wiki/log.md` | append-only 이벤트 로그 (INGEST/QUERY/자동체크 기록) |
| `wiki/summaries/` (7개) | 소스 1건을 압축한 노트, 소스와 거의 1:1 |
| `wiki/entities/` (3개) | `sk-hynix.md`(종목), `my-portfolio.md`(포트폴리오), `user-profile.md`(사용자) — 지속 갱신되는 "사물" 페이지 |
| `wiki/concepts/` (15개) | 반복 등장하는 개념 페이지 — 아래 표 |

### `wiki/concepts/` 세부 (이 프로젝트의 핵심 분석 프레임들)

| 파일 | 역할 |
|---|---|
| `sk-hynix-analyst-thesis-checkpoints.md` | 9개 체크포인트 스코어보드 + 목표가 스펙트럼 — 매일 3회 갱신되는 메인 허브 |
| `hbm-cycle-score.md` | HBM Cycle Score 6축 산정(100점 만점) + 붕괴조건 4개 |
| `macro-regime-history.md` | G/I/L 거시국면 계산 + 역사적 유사시기 매칭, PEOS/Investment Clock 병기 원칙 |
| `panic-recovery-signals.md` | 패닉 회복 신호 프레임(Tier1~3) + 국제매체 교차검증 |
| `market-cycles-leverage-risk.md` | 단기 급락 원인 분석, 찐반등 4대 신호 판별 |
| `trump-midterm-tracker.md` | 트럼프 2026 중간선거 5개 카테고리 트래커 + 카테고리별 타임라인 |
| `cxl-next-gen-memory.md` | CXL 차세대 메모리 트랙 (개인 관심사) |
| `us-china-tech-competition-hbm.md` | 미중 기술경쟁·HBM 시장 구도 |
| `roic-as-investment-criterion.md` / `rally-justification-analysis.md` / `fundamentals-vs-sentiment-derating.md` | 투자 판단 프레임들 |
| `portfolio-rebalancing-strategy.md` | 리밸런싱 전략 |
| `stock-market-essence.md` | 주식시장 본질론 |
| `macro-indicators.md` | 거시지표 정의 모음 |
| `market-holidays.md` | 한·미 증시 휴장일 캘린더 (자동체크가 매번 대조) |

## 4. `scripts/` — 데이터 수집·리포트 생성 코드

| 파일 | 역할 |
|---|---|
| `daily_report.py` | 1차 자동 리포트(.md) 생성 |
| `investor_flow.py` | KIS API — 투자자매매동향·ADR·현재가 수집 |
| `portfolio_holdings.py` | KIS API — 계좌별 보유종목 동기화 |
| `macro_data.py` / `ecos_lookup.py` / `kosis_lookup.py` | FRED/ECOS/KOSIS 거시지표 조회 |
| `regime_engine.py` | G/I/L 계산 + 역사적 애널로그 매칭 엔진 |

## 5. `.github/workflows/` — 자동화 파이프라인 (위키 관련분만)

| 파일 | 역할 |
|---|---|
| `portfolio-holdings-sync.yml` | 19:10 KST 포트폴리오 동기화 (현재 PR #35로 버그 수정 대기중) |
| `macro-data-sync.yml`, `ecos-lookup.yml`, `kosis-lookup.yml` | 거시지표 수집 |

이 3~4개 워크플로가 CSV를 `sources/`에 커밋하면, 매일 3회 Claude
Routine(트리거)이 그걸 읽어 `wiki/`를 갱신하고 HTML 리포트를 Artifact로
발행하는 구조다.

## 6. 이 위키가 참조만 하는 별도 시스템 (같은 저장소, 다른 프로젝트)

`collectors/`, `config/`, `core/`, `data/`, `docs/`, `engine/`,
`report/`, `src/`, `tests/`, `README.md`, `GUIDE.md`와
`daily-clock-report.yml`/`daily-peos-report.yml` 등은
**PEOS(개인 경제 운영체제)/Investment Clock**이라는 완전히 독립된
자동화 시스템이다. 위키는 `report/<날짜>.md`와 `docs/index.html`만
읽어서 참고용으로 병기할 뿐, 이 파일들을 직접 관리하지 않는다.
