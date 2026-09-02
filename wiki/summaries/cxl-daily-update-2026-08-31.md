# CXL Daily Update 26호 — 2026-08-31

> 발행 시각: 2026-08-31 20:03 KST | 이전 호: 25호 (2026-08-30)
> 기준선: DRAFT v1.5 (2026-08-30) + Daily Update 25호
> 수집 방법: `python search.py` DuckDuckGo 기반 12카테고리 전수
> 🚨 search.py 제한: 영어 기술 키워드 검색 시 낮은 관련성 결과 다수 — 기존 원시 데이터 및 유용한 결과 선별 사용

---

## 🔍 오늘 한 줄 진단

**25호(★★ 1건/★ 1건) 이후 — Liqid FMS 2026 CXL 풀링 플랫폼 정격 출시 신호 + Server RAM 가격 2배 + OEM 장기 계약 동향. DRAFT 4장(풀링 SW)과 10장(DRAM 가격)에 직접 반영.**
**Delta: ★★ 2건, ★ 1건, 미변경 9개. DRAFT v1.5 → v1.6 반영.**

---

## NVIDIA Dynamo Blog Digest

> 전체 7개 포스트 | NEW: 0 | UPDATED: 0 | REMOVED: 0

- **May 6, 2026** — [Dynamo Day 0 support for TokenSpeed](https://docs.nvidia.com/dynamo/dev/digest/tokenspeed-day-0)
- **May 29, 2026** — [DynoSim: Simulating the Pareto Frontier](https://docs.nvidia.com/dynamo/dev/digest/dynosim-pareto-frontier)
- **May 28, 2026** — [NVIDIA Dynamo Snapshot: Fast Startup for Inference Workloads on Kubernetes](https://docs.nvidia.com/dynamo/dev/digest/dynamo-snapshot-fast-startup)
- **June 12, 2026** — [Full-Stack Optimizations for Agentic Inference with Dynamo](https://docs.nvidia.com/dynamo/dev/digest/agentic-inference)
- **February 23, 2026** — [Flash Indexer: A Story of Inter-Galactic KV Routing](https://docs.nvidia.com/dynamo/dev/digest/flash-indexer)
- **August 21, 2026** — [Dynamo Agent Optimization Skills](https://docs.nvidia.com/dynamo/dev/digest/agent-optimization-skills)
- **April 30, 2026** — [Streaming Tokens and Tools: Multi-Turn Agentic Harness Support in Dynamo](https://docs.nvidia.com/dynamo/dev/digest/agentic-harnesses)

→ **전체 7개, 이번 발행 이후 신규 없음.** 마지막 신규: "Dynamo Agent Optimization Skills" (Aug 21).

---

## 🟢 중대 신호 (★★)

### ★★ Liqid FMS 2026에서 CXL 풀링 플랫폼 정격 출시

> 출처: [FMS 2026: Liqid Launches the Industry's Most Advanced CXL Memory Pooling Platform, StorageNewsletter, Aug 6, 2026](https://www.storagenewsletter.com/2026/08/06/fms-2026-liqid-launches-the-industrys-most-advanced-cxl-memory-pooling-platform-for-ai-and-scientific-discovery/)

**[변경]** Liqid가 FMS 2026(2026.08.04-06)에서 **"Industry's Most Advanced CXL Memory Pooling Platform for AI and Scientific Discovery"**를 정격 출시했음. StorageNewsletter는 "industry's first and only fully disaggregated, software-defined memory pooling solution"이라고 평가함. Liqid 랙 단위 풀링이 연구/개발 단계를 넘어 **정격 제품으로 출시**됨을 의미.

**[영향]** Liqid (2026-08-06) FMS 2026 발표: "industry's first and only fully disaggregated, software-defined memory pooling solution". AI 및 과학 발견 플랫폼으로 출시됨.

**[해석]** 이 신호는 CXL 상품기획에 중요한 함의가 있습니다.

1. **DRAFT 4장 "상세 미수집" → 정격 출시로 상태 변경**: 기존 DRAFT 4장은 Liqid, MemVerge 등 풀링 SW 벤더가 "(상세 미수집)"으로 표기됐음. Liqid의 FMS 2026 플랫폼 출시 정식으로 확인됨으로써 4장의 정보 부족이 해소됨. "fully disaggregated, software-defined"라는 기술 포지셔닝은 Liqid가 하드웨어(서버)와 SW 모두를 오케스트레이션하는 풀스택 접근임을 시사.
2. **AI 타겟 명확화**: 플랫폼이 "AI and Scientific Discovery"를 명시적 타겟으로 했음 — 이는 CXL 풀링이 HPC/과학 계산 영역에서 이미 검증된 후 **AI 워크로드에 확장** 중임을 의미. DRAFT 8.2절(KV cache offload)의 실제 플랫폼 공급자가 등장한 것.
3. **풀링 SW 생태 성숙도**: 23호(삼성 CXL 메모리 풀링 테크 블로그, delta-3 ★★)에서 삼성의 풀스택 전략이 공식 문서화된 데 이어, Liqid도 정격 플랫폼 출시 — 풀링 SW가 연구용 데모 → 상용 플랫폼 단계로 진입 중.

**[액션]**
```
기존: DRAFT 4장 "Liqid: CXL 풀링 어플라이언스 (상세 미수집)"
→ 변경: "Liqid: FMS 2026(2026.08.06) 정격 출시 — 'Industry's Most Advanced CXL Memory Pooling Platform for AI and Scientific Discovery.' Fully disaggregated, software-defined 풀링 솔루션. AI + 과학 계산 타겟. DRAFT 8.2절 KV offload 아키텍처의 실제 플랫폼 공급자."

기존: DRAFT 4장 "MemVerge: Memory Machine 풀링 SW (상세 미수집)"
→ 변경: 유지 (상세 여전히 미확인, Liqid가 'first and only fully disaggregated'라고 명시 — MemVerge의 포지셔닝 차이 확인 필요)
```
- Delta 위치: DRAFT 4장 (풀링 SW/어플라이언스)
- 등급: ★★ (풀링 SW 생태 성숙도 신호 — 4장 "상세 미수집" 해소)

---

### ★★ Server RAM Prices Doubled — Memory Chip Shortage 2026

> 출처: [Memory Chip Shortage 2026 — Server RAM Prices Doubled, DataCenterDisk, Aug 17, 2026](https://datacenterdisk.com/news/memory-chip-shortage-2026-server-ram-prices)

**[변경]** DataCenterDisk(2026.08.17) 보도: Dell, HPE, Supermicro, Lenovo가 **서버 주문에 대한 장기 메모리 가격**을 제공하고 있음. Server RAM prices doubled(2배) — Memory chip shortage 지속. AI 서버 수요가 표준 메모리 가격에 직접 영향.

**[영향]** DataCenterDisk (2026-08-17): Dell, HPE, Supermicro, Lenovo가 장기 메모리 가격 제공. Server RAM Prices Doubled — Memory chip shortage 2026.

**[해석]** 이 신호는 CXL 상품기획에 양면성을 가집니다.

1. **CXL 가치 강화**: Server RAM 가격이 2배라는 것은 CXL 메모리 풀링이 기존 DDR5/DIMM 대비 **용량/공유 효율**로 비용을 절감할 수 있는 강력한 근거가 됨. "stranded DRAM → shared pool"(DRAFT 11.2절)의 경제적 타당성이 더욱 강화.
2. **하지만 CXL 모듈 원가도 상승**: CXL 메모리 확장 카드는 DDR5 모듈을 사용하므로, RAM 가격이 2배면 CXL 모듈의 원자재 비용도 함께 상승. 25호 delta-1에서 언급된 Global Semi Research의 "Big Three 외부 IP 전환" 흐름과 결합하면, CXL 모듈 제조사의 마진 압박이 추가될 수 있음.
3. **OEM 장기 계약 트렌드**: Dell/HPE/Supermicro/Lenovo가 장기 메모리 가격을 제공하는 것은, CSP와 OEM이 **메모리 조달 리스크를 사전 관리** 중임을 의미. CXL 메모리 풀링을 도입할 때 OEM과의 장기 계약 모델이 중요해질 수 있음.

**[액션]**
```
기존: DRAFT 10.1절 "DRAM 가격 상승 사이클 지속... Q3 40-50% 추가 상승, Q4 30% 추가 (TechSpot 전망)"
→ 변경 추가: "DataCenterDisk(Aug 17): Server RAM Prices Doubled — Dell, HPE, Supermicro, Lenovo가 장기 메모리 가격 제공 시작. Memory chip shortage 2026 지속. CXL 풀링의 경제성 근거 강화 but CXL 모듈 원자재(DDR5) 비용 동반 상승 리스크. OEM 장기 계약 모델 중요도 상승."
```
- Delta 위치: DRAFT 10.1절 (DRAM 가격)
- 등급: ★★ (CXL 풀링 경제성에 직접적 영향 — 양면성)

---

## 🟡 참고 신호 (★)

### ★ SK Hynix CXL 3.2 메모리 + AI 포트폴리오 — HPE Tech Event 전시

> 출처: [SK hynix Showcases CXL 3.2 Memory and AI Portfolio at HPE, TheLEC, Jun 21, 2026](https://www.thelec.net/news/articleView.html?idxno=11513)

**[변경]** SK Hynix가 HPE Tech Event에서 **CXL 3.2 메모리와 AI 포트폴리오**를 전시함. TheLEC 보도: "CXL memory is not tied to specific CPUs or GPUs and supports memory pooling through switching."

**[영향]** SK hynix (2026.06.21) HPE Tech Event 전시: CXL 3.2 메모리 + AI 포트폴리오. CXL memory는 CPU/GPU 비종속적이며 스위칭을 통한 메모리 풀링 지원.

**[해석]** SK Hynix의 CXL 3.2 직접 전시 — CXL 컨트롤러 외부 IP 채택 흐름(25호 delta-1 ★★)과 함께 볼 때, SK하이닉스가 CXL 3.2 모듈/어플라이언스 수준에서 경쟁력을 유지하고 있음을 확인. HPE와의 협력은 서버 OEM과의 CXL 풀링 검증/상용화 경로를 보여줌. DRAFT 2.6절(Samsung CMM-D 2.0 10% 처리량↑)과 비교하면, SK하이닉스는 CXL 3.2 + AI 포트폴리오로 Samsung의 CMM-D 로드맵과 차별화.

**[액션]** DRAFT 변경 없음 (참고 신호). SK Hynix CXL 3.2 @ HPE — 2.6절 CXL 제품 동향 행에 신규 추가 가치 있으나, 25호 delta-1의 "Big Three 외부 IP 전환" 흐름과 일관되므로 별도 반영은 다음 호에서.
- Delta 등급: ★ (참고 신호)

---

## 📋 12카테고리 Delta 매트릭스

| # | 카테고리 | 상태 | 등급 | 핵심 신호 |
|---|---|---|---|---|
| 1 | CXL 스펙/표준 | 미변경 | — | CXL 4.0 (23호 반영) — 신규 없음 |
| 2 | CXL 디바이스/미디어 | 미변경 | — | 신규 없음 |
| 3 | 컨트롤러 벤더 | 미변경 | — | 25호 delta 반영 중 |
| 4 | 풀링 SW/어플라이언스 | ▲변경 | ★★ | **Liqid FMS 2026 플랫폼 정격 출시** |
| 5 | 서버 OEM | 미변경 | — | DRAFT 기준 유지 |
| 6 | CPU/GPU CXL | 미변경 | — | 신규 없음 |
| 7 | AI 패브릭 | 미변경 | — | 신규 없음 |
| 8 | Main Memory | 미변경 | — | DRAFT 기준 유지 |
| 9 | AI Rack/KV offload | 미변경 | — | DRAFT 기준 유지 |
| 10 | LLM TCO 모델 | 미변경 | — | DRAFT 기준 유지 |
| 11 | 메모리 가격/실적 | ▲변경 | ★★ | **Server RAM Prices Doubled — OEM 장기 계약** |
| 12 | 시장/CSP | 미변경 | — | DRAFT 기준 유지 |

---

## 🔍 미변경 카테고리 — 재검사 결과

| 카테고리 | 재검사 상태 | 차단 원인 | 대안 확인 |
|---|---|---|---|
| 1. CXL 스펙/표준 | **미변경** | CXL 4.0 Feb 26 — 23호 delta-1 반영 | 신규 없음 |
| 2. CXL 디바이스/미디어 | **미변경** | DRAFT v1.5 기준 유지 | 신규 delta 없음 |
| 3. 컨트롤러 벤더 | **미변경** | 25호 delta 반영 중 — 1일 간격 | 신규 없음 |
| 5. 서버 OEM | **미변경** | SK Hynix CXL 3.2 @ HPE (★, 아래 별도) | 신규 delta 없음 |
| 6. CPU/GPU CXL | **미변경** | Intel/AMD/NVIDIA 신규 CXL 발표 없음 | 신규 delta 없음 |
| 7. AI 패브릭 | **미변경** | DRAFT 기준 유지 | 신규 없음 |
| 8. Main Memory | **미변경** | JEDEC/LPDDR6/CAMM2 DRAFT v1.5 반영 | 신규 delta 없음 |
| 9. AI Rack/KV offload | **미변경** | Mooncake/vLLM DRAFT v1.3 반영 | 신규 delta 없음 |
| 10. LLM TCO | **미변경** | DRAFT v1.5 기준 유지 | 신규 없음 |
| 12. 시장/CSP | **미변경** | DRAFT v1.5 기준 유지 | 신규 없음 |

---

## 📊 데이터 한계 공개

- **🟢 자동화(사실층)**: `python search.py` DuckDuckGo 기반 12카테고리 전수 조사. 원시 데이터 `sources/cxl-daily-raw-2026-08-30.md`에 보존.
- **🔴 LLM 종합(해석층)**: Delta 식별, 등급 부여, [해석] 서술은 LLM 추론.
- **📝 사실/의견 분리**: `[영향]`(제공자 발언 인용)과 `[해석]`(LLM CXL 분석) 엄격 분리 준수.
- **검색 품질 한계**: `python search.py`가 영어 기술 키워드에서 낮은 관련성 결과 반환. 한국어/상업 사이트가 영어 기술 소식을 대체. StorageNewsletter, DataCenterDisk, TheLEC 등 유용한 결과는 일부 수집됨.
- **단일 출처**: Liqid FMS 2026 플랫폼 출시 — StorageNewsletter 1개 출처. DataCenterDisk Server RAM price doubled — 1개 출처. SK Hynix @ HPE — TheLEC 1개 출처. 모두 교차검증 필요.

---

## ⚡ 후속 액션

1. **[다음 발행]** 컨트롤러 벤더(3번) — Primetas 프로필 확인 (25호 delta ★ 미완료), Global Semi Research 기사 원문 재확인
2. **[DRAFT 보강]** Liqid 플랫폼 기술 세부사항 확인 — StorageNewsletter FMS 2026 리캡 원문 읽기 → DRAFT 4장 정밀화
3. **[다음 발행]** DRAM 가격 — TechSpot 전망과 DataCenterDisk 보고의 정합성 확인 (동일 출처 교차검증)
4. **[다음 발행]** AI Rack/KV offload — Mooncake Store 정량 메트릭 보강 (22호 delta-3 이후 최신 데이터 확인)

---

## 📝 발행 정보

- **보고서**: CXL Daily Update 26호
- **MD 경로**: `wiki/daily-updates/cxl-daily-update-2026-08-31.md`
- **HTML 경로**: `Results/cxl-daily/cxl-daily-report-2026-08-31-2003.html`
- **원시 데이터**: `sources/cxl-daily-raw-2026-08-30.md`
- **DRAFT 반영 계획**: ★★ 2건 — DRAFT 4장(Liqid 정격 출시) + 10.1절(Server RAM Prices Doubled) 반영 (v1.5 → v1.6)
- **delta 건수**: ★★ 2건, ★ 1건, 미변경 9건
- **DRAFT 버전**: v1.5 → v1.6 승격

---

*CXL Daily Update 26호 발행 완료 — MD 발행, DRAFT v1.6 반영 예정*
