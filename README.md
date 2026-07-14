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

`config/schedule.yaml`에 권장 실행 주기(18.3)가 정의되어 있습니다. 기존 daily-clock GitHub Actions 워크플로우
(`.github/workflows/daily-clock-report.yml`)는 유지되며, `python -m engine.report.run`을 월간 워크플로우로
추가하면 매월 자동 리포트 생성이 가능합니다 (아직 워크플로우 파일 자체는 추가하지 않았습니다 — 필요하시면 알려주세요).

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
