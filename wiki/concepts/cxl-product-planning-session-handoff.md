---
title: "CXL 상품기획 프로젝트 — 세션 핸드오프"
created: 2026-08-04
updated: 2026-08-06
tags: [cxl, product-planning, handoff, session-context, daily-update]
---

# CXL 상품기획 프로젝트 — 세션 핸드오프

> 이 문서는 다음 세션에서 "CXL 관련 보고서 이야기를 계속하자"고 하면 즉시 작업을 이어가기 위한 맥락 저장용. 새 세션에서 이 파일을 가장 먼저 읽으면 전체 맥락이 복원됨.

---

## 1. 프로젝트 개요

**목표**: CXL 기반 차세대 메모리 상품기획 논의용 종합 기반 자료 작성 + 매일 Daily Update 보고서 발행.

**시작**: 2026-08-03. 사용자가 무질서하게 나열한 CXL 관련 주제들을 카테고리화 → 조사 → DRAFT → HTML 보고서 → Daily Update 체계로 발전.

---

## 2. 산출물 파일 목록 (둘 다 확인 필수)

| 파일 | 용도 | 상태 |
|---|---|---|
| `wiki/concepts/cxl-memory-product-planning-draft.md` | **메인 DRAFT v0.5 + 0장** (12장 구조, Daily Update 1호 delta 7건 + 2호 delta 8건 반영) | 완료 (v0.5) |
| `wiki/cxl-memory-product-planning-report-2026-08-04-0906.html` | 경영진용 HTML 보고서 (0장 포함) | 완료 |
| `wiki/daily-updates/cxl-daily-update-2026-08-04.md` | Daily Update 1호 (delta + insight) | 완료 (1호) |
| `wiki/cxl-daily-report-2026-08-04-0926.html` | Daily Update 1호 HTML | 완료 (1호) |
| `wiki/daily-updates/cxl-daily-update-2026-08-06.md` | **Daily Update 2호** (12카테고리 전수, delta 8건: Montage CXL 3.2/FMS 2026 하드웨어/HBM 3사 실적/CapEx 상세/KV cache 정량) | 완료 (2호) |
| `wiki/cxl-daily-report-2026-08-06-0240.html` | **Daily Update 2호 HTML** | 완료 (2호) |
| `sources/cxl-daily-raw-2026-08-06.md` | 2호 원시 데이터 (12카테고리 WebFetch 발췌) | 완료 |
| `wiki/index.md` | 인덱스 (cxl-memory-product-planning-draft + Daily Update 2호 등록됨) | 업데이트됨 |
| `wiki/log.md` | 이벤트 로그 (모든 작업 기록됨) | 업데이트됨 |

---

## 3. DRAFT 구조 (12장 + 0장)

```
0. 최신 업데이트 (2026-08-03/04 훑어보기) — 신설
1. 요약 & 핵심 쟁점
2. CXL 표준 & 디바이스 레벨 기술
3. CXL 컨트롤러/칩셋 벤더 동향 ★핵심 (7개 벤더: Panmnesia/XCENA/ScaleFlux/Marvell/Montage/Astera/Microchip)
4. CXL 풀링 SW/어플라이언스 생태 (4.7 풀링 심층 포함)
5. CPU/GPU 벤더 CXL 지원 & POR 메모리 조합 ★핵심
6. AI 패브릭 진영 대치
7. Main Memory ↔ CXL 미디어 연관성
8. AI Rack 메모리 계층 & KV offload 응용
9. 수치 모델링: LLM × Context × TPS × TCO
10. 메모리 가격 & 시장 사이클
11. 시장 인텔리전스
12. 차세대 상품기획 방향 (종합 제언)
```

---

## 4. Daily Update 운영 방식 (사용자 확정)

- **주기**: 매일 전수 조사 + 심층 분석 (방향 잡힐 때까지)
- **구조**: 각 delta별 `[변경]/[영향]/[액션]` 3단
  - **[액션] 규칙 (2026-08-06 강화)**: "DRAFT X장에 반영" 같은 단순 표현 금지. **① 기준 보고서+chapter 명시**(DRAFT vX.X(일자) X절, 또는 Daily Update N호 delta-N) + **② 기존내용 → 변경내용 diff**(`기존: "..." → 변경: "..."`). 신규 추가 시 `기존: (해당 없음)`. 복수 위치는 각각 별도 diff. 상세는 시스템 프롬프트 `.claude/prompts/cxl-daily-update.md` "delta 식별 + Daily Update 작성" 절 참조.
- **포맷**: HTML + MD 동시 발행
- **발행**: 변동 없어도 1줄 최소
- **파일명 규칙** (CLAUDE.md 보고서 버저닝 준수):
  - MD: `wiki/daily-updates/cxl-daily-update-YYYY-MM-DD.md`
  - HTML: `wiki/cxl-daily-report-YYYY-MM-DD-HHMM.html`
  - **HHMM은 24시간 형식(00~23시)**. 예: 07:00 KST→`0700`, 14:05→`1405`. 12시간 표기 금지.
- **기준선**: 직전 DRAFT 버전 + 가장 최근 0장/Daily Update

### 매일 조사 카테고리 (12개)
1. CXL 스펙/표준  2. CXL 디바이스/미디어  3. 컨트롤러 벤더(7개)  4. 풀링 SW/어플라이언스  5. 서버 OEM  6. CPU/GPU CXL  7. AI 패브릭  8. Main Memory  9. AI Rack/KV offload  10. LLM TCO 모델  11. 메모리 가격/실적  12. 시장/CSP

---

## 5. 현재 상태 & 미해결 사항

> **2026-08-06 업데이트**: Daily Update 2호 delta 8건을 DRAFT 본문에 모두 반영 → **DRAFT v0.5 완료**. 2호는 12개 카테고리 전수 WebFetch(메인 루프 직접, DuckDuckGo HTML 폴백). ★★★ Montage CXL 3.2 MXC 업계 최초 trial production, ★★ FMS 2026 하드웨어(Marvell 48TB/Liqid 160TB+PNNL/Panmnesia ISCA)/HBM 3사 실적+HBM4/CapEx 상세+전력 60%+, ★ DRAM 둔화/KV cache 정량. 1호에서 이미 기재된 사실의 상세 정밀화 위주 + KV cache 정량·전력 60%+·HBM4 ramping 등 신규 사실. 남은 미해결 agenda: #21(UALink 2.0 세부 스펙), #22(Mooncake 정량 메트릭), #25(메모리사 가이던스), #34-36(2호 신규: Montage 양산 전환/HBM4 램프/전력 60% 교차검증).

> **2026-08-04 히스토리**: Daily Update 1호 delta 7건 반영 → DRAFT v0.4 완료. Ultra Ethernet vs CXL 4.0 심층 조사(#20)는 2026-08-04 완료(ai-fabric-3way-rivalry-and-cxl-layer.md, "다른 레이어" 결론).

### 완료된 정정 (중요 — 반복 검증된 사실)
- **Intel Emerald Rapids = CXL 1.1** (2.0 아님, 핵심 개선은 Type 3 공식 인증)
- **Intel Diamond Rapids = mid-2027 지연** (2026→2027)
- **AMD Turin = CXL 2.0** (3.0 아님). 2026.08 기준 CXL 3.0 구현한 AMD EPYC 없음
- **AMD Venice CXL 3.x = 미확정** (후보, AMD 공식 미확인)
- **"Axaina" → XCENA(액시나)** 정정 완료: RISC-V 수천 코어 컴퓨테이셔널 메모리 컨트롤러, CXL 3.2, KV cache 오프로드, Intel 협력, 2026 양산

### Daily Update 1호에서 식별된 delta (2026-08-04)
- ★★★ UALink 2.0(2026.04) + AI 패브릭 3-way rivalry(UALink/NVIDIA/Ultra Ethernet)
- ★★★ JEDEC DDR6/LPDDR6 CAMM2 표준화 확정, 기존 레이아웃 폐지
- ★★★ HBM 점유율: SK 62/Micron 21/Samsung 17, Samsung 내년 30%+ 목표
- ★★ Q3 DRAM 13~18% 상승, 초기 DDR6/CAMM2 "천문학적 가격"
- ★★ Hyperscaler 합산 2026 AI 인프라 $600-770B
- ★★ Vera Rubin 88-core+336B, Blackwell 대비 5배 추론 성능
- ★★ FMS 2026(8/4 산타클라라 개막), Marvell "Agentic AI Inference" 프레임
- ★ Mooncake+vLLM 메트릭

### 미해결 / 후속 DRAFT 보강 agenda (Daily Update 1호에서 명시)
- [x] DRAFT 6장: UALink 2.0 + Ultra Ethernet 3-way rivalry 추가 ✅ v0.4
- [x] DRAFT 7장: JEDEC CAMM2 표준화 일정 + Q3 가격 13~18% + "천문학적 가격" 경고 ✅ v0.4
- [x] DRAFT 10장/11.3장: HBM 점유율(62/21/17) + Samsung 30%+ + 16-layer 로드맵 ✅ v0.4
- [x] DRAFT 11.2장: hyperscaler 합산 $600-770B ✅ v0.4
- [x] DRAFT 0장/9장: Vera Rubin 5배 추론 성능 수치 ✅ v0.4
- [x] DRAFT 3장/4장: FMS 2026 + Marvell "Agentic AI Inference" 프레임 ✅ v0.4
- [x] DRAFT 8.3장: Mooncake+vLLM 메트릭 ✅ v0.4
- [x] Ultra Ethernet vs CXL 4.0 패브릭 관계 심층 조사 (신규 agenda) ✅ 완료 — concepts/ai-fabric-3way-rivalry-and-cxl-layer.md 신규 작성. 결론: 다른 레이어(메모리 풀 vs 네트워크 패브릭), 보완·공존

### 미해결 / 후속 DRAFT 보강 agenda (Daily Update 2호에서 명시, 2026-08-06)
- [x] DRAFT 3장 Montage: CXL 3.2 MXC M88MX6852 업계 최초 trial production + 벤더별 세대 분화 ✅ v0.5
- [x] DRAFT 3장/4장/2장: FMS 2026 CXL 하드웨어(Marvell 48TB/Kioxia XL1/ScaleFlux MC600/XCENA 20TB+KV 데모) ✅ v0.5
- [x] DRAFT 3장 Panmnesia: ISCA 2026 next-stage controller + fabric switch ✅ v0.5
- [x] DRAFT 4장: Liqid EX-5410C 160TB+ pool @ PNNL + 2026 CXL 생태 맵 ✅ v0.5
- [x] DRAFT 10장: HBM 3사 실적 + HBM output +62% + HBM4 ramping + 점유율 범위 표기 ✅ v0.5
- [x] DRAFT 11장: CapEx 상세 분해 + 전력 60%+ + Q1 $130B ✅ v0.5
- [x] DRAFT 10장: DRAM 가격 이중 추세(소비자 둔화 + AI/서버 지속) ✅ v0.5
- [x] DRAFT 8장/12장: KV cache 정량(70B/32K=128GB, FP8 -50%, 4~40x 압축) + 풀 용량 산정 기준 ✅ v0.5
- [ ] (신규 #34) Montage trial production → 양산 전환 시점 추적
- [ ] (신규 #35) HBM4 양산 램프 상세(SK/Samsung/Micron HBM4 타임라인) 추적
- [ ] (신규 #36) "전력 60%+" 1차 출처 교차검증 + CXL 풀링의 전력/랙 효율 정량화
- [ ] (계속) UALink 2.0 세부 스펙(#21), Mooncake 정량 메트릭(#22), 메모리사 가이던스(#25)

---

## 6. 핵심 인사이트 (상품기획 시사점, 반복 금지용)

1. **AI 패브릭 3-way 경쟁** → CXL "진영 중립적 메모리 풀" 포지셔닝(12.2 옵션4) 가치 상승. 3개 진영 모두에 부착 가능한 유일한 메모리 레이어
2. **CAMM2 표준화 + Q3 가격 13~18% 상승** → CXL 풀링 overprovisioning 절감 가치 강화. 단, 초기 DDR6/CAMM2 고가 → CXL 비용 프리미엄 단기 확대 가능
3. **Samsung HBM 역공(17%→30%+)** + NVIDIA 16-layer 요청 → HBM 경쟁 심화 → 가격 하방. SK하이닉스는 점유율 방어 + CXL 차별화 동시 추진 필요
4. **Hyperscaler $600-770B 자본** → CXL 풀링 채택 자본 여력 압도적
5. **Vera Rubin 5배 추론 성능** → KV cache 요구 폭증 → CXL KV cache 풀(cleanest win) 수요 확정적 증가
6. **NVIDIA-SK Hynix $500B 동맹** (Vera Rubin HBM 장기 공급) → SK하이닉스 CXL 전략을 NVIDIA 생태와 정렬 필요
7. **XCENA** = 신제품 컨셉 핵심 반영 대상 (컴퓨테이셔널 메모리 + KV cache 오프로드)
8. **풀링 use case cleanest win**: AI KV cache / Redis / Spark shuffle. **회피**: OLTP(레이턴시 민감, local DDR5 우위)
9. **레이턴시 트레이드오프**: remote CXL = 로컬 대비 2.2~4x 지연. latency-sensitive는 local DDR5 우위. 풀링은 용량/탄력 이점 필요 워크로드에 적합
10. **CXL 3.x 시대는 2027년 이후** (양사 모두 보수적: Intel Diamond Rapids mid-2027, AMD Venice 미확정)

---

## 7. 다음 세션에서 즉시 이어가는 방법

사용자가 "CXL 관련 보고서 이야기를 계속하자"라고 하면:

1. **이 파일을 가장 먼저 읽을 것** (`wiki/concepts/cxl-product-planning-session-handoff.md`)
2. 메인 DRAFT 읽기: `wiki/concepts/cxl-memory-product-planning-draft.md`
3. 가장 최근 Daily Update 읽기: `wiki/daily-updates/cxl-daily-update-2026-08-06.md` (2호)
4. log.md 마지막 항목 확인해 진행 상황 파악
5. 사용자에게 현재 상태 요약 + 다음 액션 제안
6. 작업 유형별 대응:
   - "Daily Update 발행해" → Daily Update 3호 발행 절차
   - "DRAFT 보강해" → 5절의 미해결 agenda 처리
   - "특정 주제 깊이 파" → 해당 카테고리 심층 조사
   - "상품기획 논의하자" → 12장 제언 기반 논의 진행

### 다음 Daily Update(3호) 발행 절차
1. `date`로 현재 KST 확인 (KST=UTC+9)
2. 12개 카테고리 WebFetch 전수 조사 (한 번에 2-3개씩, 429 회피; Google Search 차단 시 DuckDuckGo HTML 폴백)
3. 기준선(DRAFT v0.5 + 8/6 Daily Update 2호) 대비 delta 식별
4. 각 delta별 [변경]/[영향]/[액션] 작성
5. `wiki/daily-updates/cxl-daily-update-YYYY-MM-DD.md` + `wiki/cxl-daily-report-YYYY-MM-DD-HHMM.html` 발행 (HHMM=24시간 형식, 00~23시)
6. 원시 데이터 `sources/cxl-daily-raw-YYYY-MM-DD.md` 보존
7. ★★★/★★ delta를 DRAFT 본문에 반영 → DRAFT 버전 승격
8. index.md/log.md 업데이트

> **2호(2026-08-06) 회고**: 메인 루프 직접 WebFetch(8절 노하우 준수)로 12카테고리 안정 수집. DuckDuckGo HTML 폴백으로 Google Search 차단 우회. delta 8건(★★★1/★★5/★2). 핵심: 1호에서 이미 기재된 사실의 **상세 정밀화** 위주 + **KV cache 정량(128GB/request)·전력 60%+·HBM4 ramping** 등 완전 신규 사실. DRAFT v0.4→v0.5 반영 완료.

---

## 8. 운영 노하우 (429/오류 회피)

- **WebSearch API 백엔드 장애** (tool_choice 검증 오류) → WebFetch + DuckDuckGo HTML 경유로 대체
- **429 속도제한**: 한 번에 에이전트 9개 동시 실행 금지. WebFetch는 한 번에 2-3개 병렬, 그 이상은 순차
- **에이전트보다 메인 루프 직접 WebFetch가 안정적** (이미 검증)
- **DuckDuckGo HTML 경유 패턴**: `https://html.duckduckgo.com/html/?q=...`
- **다중 WebFetch 호출 JSON 묶음 에러**: 한 번에 하나씩만 호출 (묶으면 인코딩 에러)
- **백슬래시 인코딩**: 편집 시 `\` 문자 주의 (한국어/경로 혼합 시 깨짐). 줄 단위 편집으로 우회
