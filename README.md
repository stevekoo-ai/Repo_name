# PEOS (Personal Economic Operating System)

공식 데이터를 수집·검증하고, 거시경제와 반도체 산업 사이클을 해석한 뒤, 사용자의 직업·자산·목표에 맞춰
**"이번 달 무엇을 해야 하는가"**를 제안하는 개인 경제 의사결정 시스템입니다.
`docs/PEOS_ClaudeCode_Master_Instruction.md`(작업지시서)를 단일 기준 문서로 구현되었습니다.

```
공식 데이터 수집 → 검증/정규화 → 지표 생성 → Rule Engine → Macro/Domain 분석 → 개인화 매핑 → Action Plan → Markdown 리포트
```

## 빠른 실행

```bash
pip install -r requirements.txt
python -m engine.report.run --month 2026-07   # report/2026-07.md, report/2026-07.json 생성
python -m pytest tests/ -q
```

API 키가 없어도 실행됩니다 — 키가 필요한 소스는 `Pending`으로 표시되고, `data/manual_inputs/*.yaml`의
예시(EXAMPLE) 데이터로 나머지 파이프라인(반도체/투자/채권/환율/청약/캘린더/액션 엔진)이 끝까지 동작합니다.
샘플 리포트: [`report/2026-07.md`](report/2026-07.md).

## 아키텍처

```
core/        설정 로더, 로깅, 캐시, 공통 데이터 모델
collectors/  공식 데이터 수집기 (FRED/ECOS/KOSIS) + 수동 입력 로더 (motie/반도체/청약/출장/캘린더)
engine/
  rule/      YAML 기반 규칙 평가기 (10)
  scoring/   가중합/스타등급 공용 유틸
  macro/     Core-10 지표, Regime 판정, Confidence, Change Detection, Macro Snapshot (11)
  semiconductor/   Memory Cycle / AI Infra / Semiconductor Score (12)
  personal/  Investment/ETF, Bond, FX, Housing(+플랫폼시티), Travel, Calendar, Asset Impact (13, 14)
  action/    Action 후보 생성 + 우선순위 + Conflict Resolver (15)
  report/    구조화 payload + Markdown 렌더러 + PDF/Excel 확장 지점 (16, 20, 25)
config/      rules.yaml / thresholds.yaml / api.yaml / user.yaml / portfolio.yaml / schedule.yaml / report.yaml
data/        raw(불변 원본, gitignored) → normalized → snapshots(월간, 추적됨) → manual_inputs(추적됨)
tests/       pytest 단위/통합 테스트
```

모든 Rule/Threshold/가중치는 `config/*.yaml`에 있습니다 — 코드에는 하드코딩된 판단 기준이 없습니다.

## 필요한 설정 (선택)

`.env.example`을 `.env`로 복사해 보유한 키만 채우세요. 없는 키는 해당 소스가 `Pending`으로 표시될 뿐,
파이프라인은 끝까지 동작합니다.

| 소스 | 키 | 무료 발급 | 비고 |
|---|---|---|---|
| FRED (미국/글로벌) | `FRED_API_KEY` | [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html) | 키 없이도 CSV로 동작, 키는 폴백용 |
| 한국은행 ECOS | `ECOS_API_KEY` | [ecos.bok.or.kr](https://ecos.bok.or.kr) | GDP/PPI/경상수지/기준금리/환율 |
| 통계청 KOSIS | `KOSIS_API_KEY` | [kosis.kr/openapi](https://kosis.kr/openapi) | CPI/실업률/산업생산/소매판매 |

`ECOS_API_KEY`/`KOSIS_API_KEY`가 등록된 통계표 코드는 `collectors/ecos.py`/`collectors/kosis.py`의
`ECOS_SERIES`/`KOSIS_SERIES` 딕셔너리에 있습니다 — 이 샌드박스는 아웃바운드 네트워크가 정책상 차단되어
실제 API 호출로 검증하지 못했으므로, 최초 실전 사용 전 ECOS/KOSIS 통계표 검색 콘솔에서 코드가 맞는지
한 번 확인해 주세요(코드 내 주석에 표시됨).

수동 입력이 필요한 항목(공식 API가 없는 반도체 가격·청약 공고·출장/여행 일정·경제 캘린더)은
`data/manual_inputs/*.yaml`에서 EXAMPLE 값을 실제 값으로 바꾸면 됩니다:

- `exports.yaml` — 총수출/반도체수출 YoY (산업통상자원부 보도자료 기준)
- `semiconductor.yaml` — DRAM/NAND/HBM/CSP CapEx 등 신호 (기업 IR, TrendForce 등)
- `subscription_notices.yaml` — 청약홈/LH/GH/SH 공고 (플랫폼시티 포함)
- `trips.yaml` — 출장/여행 일정
- `calendar.yaml` — 경제 캘린더

개인 프로필/보유자산은 `config/user.yaml`, `config/portfolio.yaml`에 있습니다 (현재 EXAMPLE 플레이스홀더).

## 구현 범위 (MVP)

- ✅ Raw/Normalized/Indicator/Analysis/Snapshot 계층 분리 저장, 메타데이터·검증 규칙(Null/중복/이상치/최신성)
- ✅ Macro Core-10 가중 스코어링, Regime 상태기계(강등/경고/상향), Confidence Score, 월간 Change Detection
- ✅ Semiconductor / Investment·ETF / Bond / FX / Housing(+플랫폼시티) / Travel / Calendar 도메인 엔진
- ✅ Personal Mapping, Action Priority Engine, Conflict Resolver
- ✅ 구조화 JSON payload + Markdown 리포트 (Executive Summary ~ Appendix, 12개 섹션)
- ⏳ IMF/OECD/BLS 전용 수집기, Streamlit 대시보드, PDF/Excel export — `engine/report/exporters.py`에
  확장 지점만 마련(24.4 플러그인 구조 지향). 필요 시 다음 세션에서 추가 가능합니다.

## 자동화

### PEOS Daily Report (매일 06:00~08:00)

`.github/workflows/daily-peos-report.yml` — 매일 23:00 UTC 자동 실행:
1. **06:00 시작**: 데이터 수집 개시 (ECOS, KOSIS, FRED 등)
2. **08:00 완료**: 웹페이지 생성 + 이메일 발송
   - `python -m engine.report.run --daily`
   - 출력: `report/daily.json` (웹페이지 렌더링용)
   - 알림: GMAIL_ADDRESS/GMAIL_APP_PASSWORD 시크릿(Gmail SMTP, stevekoo.kr@gmail.com)으로 이메일 발송

### PEOS Monthly Report (거시경제 심층 분석)

`.github/workflows/monthly-peos-report.yml` — 매월 5일 08:00 KST 자동 실행:
- `python -m engine.report.run --monthly` (또는 수동 `--month YYYY-MM`)
- 출력: `report/<YYYY-MM>.html`, `report/<YYYY-MM>.md`, `report/<YYYY-MM>.json`
- 용도: 월별 거시경제 지표 발표 이후 전략 재점검, 시나리오 분석

### Investment Clock (기존 유지)

`.github/workflows/daily-clock-report.yml` — 매일 08:00 KST 자동 실행:
- `python -m src.clock.main`
- 출력: `docs/clock.png`, `docs/index.html` (인터랙티브 대시보드)
- 용도: 미국 거시경제 4국면 판정, 자산배분 전술

## 테스트

```bash
python -m pytest tests/ -q
```

Rule Engine, Macro Score/Regime 전이(강등·경고·상향), Semiconductor Score, Bond/Housing 시나리오,
Action Priority/Conflict Resolver, 전체 파이프라인 통합까지 포함합니다 (21.4의 5개 시뮬레이션 케이스 반영).

---

## Legacy: Macro Investment Clock (`src/clock/`)

기존에 구현되어 있던 미국 거시경제 4국면(Investment Clock) 모델입니다. 사용자 결정에 따라 **삭제하지 않고
PEOS의 미국/글로벌 입력 소스로 흡수**했습니다: `engine/macro/us_clock.py`가 이 모듈의 `data_sources`/`model`을
그대로 재사용해 Investment Clock 국면을 계산하고, PEOS 월간 리포트의 "경기 판정" 섹션에 참고 컨텍스트로
표시합니다(`macro.us_investment_clock`). 기존 일일 GitHub Actions 대시보드(`docs/index.html`)는 그대로 유지됩니다.

- FRED 공개 CSV 엔드포인트에서 API 키 없이 수집 (`USALOLITOAASTSAM`, `CPIAUCSL`, `T10Y2Y`, `UNRATE` 등)
- 매일 08:00 KST 자동 실행 → `docs/` 정적 대시보드 갱신 → 자동 커밋
- 상세 로직/한계는 `GUIDE.md` 참고

```bash
python -m src.clock.main   # 단독 실행
```

## 지식베이스 (Wiki) — 여러 세션·프로젝트가 공유하는 정보 풀

이 저장소는 [Andrej Karpathy의 "LLM Wiki" 패턴](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)도
함께 운영합니다: 사람이 원본 자료(뉴스, 메모, 스크린샷, 프로필 등)를 `sources/`에 넣으면, LLM이 그걸 읽고
`wiki/`에 지속적으로 갱신되는 지식베이스를 만듭니다. **PEOS의 `config/user.yaml`이 엔진이 소비하는
"기계가 읽는" 프로필이라면, 이 위키는 사람이 읽고 검색하는 "서술형" 프로필/리서치 노트**입니다 —
같은 사실이 양쪽에 있을 수 있으니 새 사실은 두 곳 다 갱신하거나, 최소한 위키에 어느 쪽이 최신인지
남겨두세요.

- `CLAUDE.md` — 스키마/워크플로우 정의 (구조를 바꿀 때만 사람이 직접 수정)
- `sources/` — 원본, 불변 (뉴스 요약, 계좌 스냅샷, 프로필 등)
- `wiki/index.md` — 전체 페이지 카탈로그, `wiki/entities/user-profile.md`에 사용자 프로필
- 사용법: `/ingest <자료>`, `/query <질문>`, `/lint` (3개 슬래시 커맨드). 처음 쓰신다면 [USAGE.md](USAGE.md) 참고,
  다른 AI 도구로 이 구조를 옮기고 싶다면 [SYSTEM-OVERVIEW.md](SYSTEM-OVERVIEW.md) 참고.

> **주의**: `sources/`, `wiki/`에는 실명 수준은 아니지만 주소·자녀 학교·계좌 잔액 등 민감정보가
> 평문으로 들어있고, 이 저장소는 public입니다 (2026-07-15 사용자 확인·승인됨).
