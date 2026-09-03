# CXL Daily Update 25호 — 2026-08-30

> 발행 시각: 2026-08-30 05:01 KST | 이전 호: 24호 (2026-08-29)
> 기준선: DRAFT v1.4 (2026-08-28) + Daily Update 24호
> 수집 방법: `python search.py` DuckDuckGo 기반 12카테고리 전수
> 🚨 search.py 제한: 영어 기술 키워드 검색 시 낮은 관련성 결과 다수 — 기존 원시 데이터 및 유용한 결과 선별 사용

---

## 🔍 오늘 한 줄 진단

**24호(★ 2건) 이후 — 3장 컨트롤러 벤더에서 중대한 구조 신호: Big Three 메모리 3사 모두 자체 컨트롤러 포기 + Primemas 신규 진출.**
24호에서 Panmnesia FMS 불참을 기록했는데, 같은 FMS 2026 맥락에서 Primemas 등장. **Delta: ★★ 1건, ★ 1건, 미변경 10개. DRAFT v1.4→v1.5 반영.**

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

### ★★ Big Three Memory Makers Pull Back from In-House CXL Controllers (Global Semi Research, 2026-07-20)

> 출처: [As the Big Three Memory Makers Pull Back from In-House CXL Controllers, Global Semi Research, Jul 20, 2026](https://globalsemiresearch.substack.com/p/as-the-big-three-memory-makers-pull)

**[변경]** Global Semi Research는 삼성·SK하이닉스·마이크론이 모두 **자체 CXL 컨트롤러 개발을 포기**하고 외부 벤더(Astera Labs, Marvell, Montage, etc.) 솔루션을 채택하는 방향으로 전환 중이라고 보도함. 핵심 인용: **"The switch roadmaps of Astera Labs, Marvell, Montage, and other suppliers will determine whether CXL remains an open standard or fragments."**
이 분석은 3사가 기존에 자체 컨트롤러 인하우스 개발을 검토/시도했던 방향(삼성 CMM-H 인하우스, SK하이닉스 인하우스 CXL 컨트롤러 도입 계획)과 정반대의 흐름.

**[영향]** Global Semi Research (2026-07-20)는 삼성, SK하이닉스, 마이크론이 모두 자체 CXL 컨트롤러 개발을 중단하고 외부 벤더 솔루션으로 전환 중이라고 보도함.

**[해석]** 이 신호는 CXL 상품기획에 중대한 함의를 가집니다.

1. **DRAFT 3장 컨트롤러 벤더 맵핑 강화 증거**: 삼성/SK/Micron이 자체 컨트롤러를 포기한다는 것은 Panmnesia, Montage, Astera, ScaleFlux 등 독립 컨트롤러/IP 벤더의 시장 지위가 더욱 공고해짐을 의미. 상품기획에서 "자체 컨트롤러 vs 외부 IP" 전략의 기준선이 명확해짐.
2. **CXL 표준 통합 vs 단편화 리스크**: 분석은 "Astera/Marvell/Montage의 switch 로드맵이 CXL을 개방형 표준으로 유지할지 단편화될지 결정할 것"이라고 전망. CXL 4.0(128 GT/s) 시대에 3개 이상 벤더가 switch/control로 분할되면 상호운용성 문제가 발생할 수 있음.
3. **SK하이닉스 상품기획 시사점**: SK하이닉스가 "인하우스 컨트롤러 도입" 계획(DRAFT 2.6, 11.3장)을 유지할지 재검토 필요. Big Three 모두 외부 IP로 전환하는 흐름에서 SK하이닉스의 인하우스 시도가 실패할 경우, 컨트롤러 IP 진입 장벽이 높아져 경쟁사 대비 약점. 반면, SK하이닉스/Naver Cloud PIM 결합(CXL+PIM) 같은 차별화 use case에서는 인하우스 컨트롤러가 여전히 가치 있을 수 있음.
4. **DRAFT 12.1 신제품 컨셉 매핑 영향**: "컨트롤러/IP 전문" 포지션(Panmnesia/Montage식)이 산업 표준으로 정립되면, SK하이닉스가 컨트롤러/IP 공급자보다는 모듈/어플라이언스 통합자에 집중하는 것이 현실적 경로.

**[액션]**
```
기존: DRAFT 2.6 "SK Hynix 96GB CMM-DDR5 (24Gb/1a nm) 2025.04 검증, 인하우스 CXL 컨트롤러 도입 예정"
→ 변경: "SK Hynix 96GB CMM-DDR5 (24Gb/1a nm) 2025.04 검증. 단, Global Semi Research(2026-07)는 Samsung/SK Hynix/Micron 모두 자체 컨트롤러 개발 축소, 외부 IP(Astera/Montage/Synopsys) 채택으로 전환 중이라고 분석. SK하이닉스 인하우스 컨트롤러 계획의 진전 상황 추가 확인 필요."

기존: DRAFT 11.3 "삼성/SK하이닉스/마이크론 3사 모두 HBM/DRAM 확장 재정적 여유 충분"
→ 변경 추가: "Global Semi Research(2026-07)는 3사가 자체 CXL 컨트롤러 개발을 포기하고 외부 IP로 전환 중이라고 분석 — 컨트롤러 IP 생태가 Montage/Astera/Marvell/Synopsys 등 독립 벤더로 집중되는 구조적 변화."
```
- Delta 위치: DRAFT 2.6절 (SK Hynix 컨트롤러 계획) + 11.3장 (메모리 3사)
- 등급: ★★ (구조적 신호 — 컨트롤러 벤더 생태 재편)

---

## 🟡 참고 신호 (★)

### ★ Primemas — FMS 2026 신규 참가자 (StorageNewsletter, 2026-08-25)

> 출처: [Recap FMS 2026, StorageNewsletter, Aug 25, 2026](https://www.storagenewsletter.com/2026/08/25/recap-fms-2026/)

**[변경]** StorageNewsletter FMS 2026 리캡에서 **Primemas**가 신규 참가자로 등장. Phison, Swissbit, Panmnesia는 "notable absence". Intel 주최, Intel 협력사 다수参展.

**[영향]** StorageNewsletter (2026-08-25) 리캡: Primemas가 FMS 2026에 신규 참가, Phison/Swissbit/Panmnesia 부재.

**[해석]** Primemas 신규 참가 — FMS 2026에 새로 등장한 벤더 이름. 정확한 프로필(CXL 컨트롤러? NAND? 폼팩터?)은 현재 미확인. Panmnesia 불참(24호 delta)과 대비되어 CXL 컨트롤러 벤더 생태에서 기존 참가자 이탈 + 신규 진입 동시 발생. DRAFT에 직접 반영하기에는 Primemas 정보가 부족하므로 참고 신호로만 기록.

**[액션]** DRAFT 변경 없음. Primemas 정보 수집 → DRAFT 3장 컨트롤러 벤더 맵핑에 반영 예정.
- Delta 등급: ★ (참고 신호, 정보 부족)

---

## 📋 12카테고리 Delta 매트릭스

| # | 카테고리 | 상태 | 등급 | 핵심 신호 |
|---|---|---|---|---|
| 1 | CXL 스펙/표준 | 미변경 | — | CXL 4.0 (Feb 26) — Synopsys CXL 4.0 IP 추가 신호 있으나 23호 delta-2 이미 반영 |
| 2 | CXL 디바이스/미디어 | 미변경 | — | 신규 없음 |
| 3 | 컨트롤러 벤더 | ▲변경 | ★★+★ | **Big Three 인하우스 컨트롤러 포기** (★★) / **Primemas 신규 진출** (★) / Panmnesia 불참/ScaleFlux-NVIDIA joint keynote (24호) |
| 4 | 풀링 SW/어플라이언스 | 미변경 | — | DRAFT v1.4 기준 유지 |
| 5 | 서버 OEM | 미변경 | — | 신규 없음 |
| 6 | CPU/GPU CXL | 미변경 | — | 신규 없음 |
| 7 | AI 패브릭 | 미변경 | — | 신규 없음 |
| 8 | Main Memory | 미변경 | — | DRAFT v1.4 기준 유지 |
| 9 | AI Rack/KV offload | 미변경 | — | DRAFT v1.4 기준 유지 |
| 10 | LLM TCO 모델 | 미변경 | — | DRAFT v1.4 기준 유지 |
| 11 | 메모리 가격/실적 | 미변경 | — | DRAFT v1.4 기준 유지 |
| 12 | 시장/CSP | 미변경 | — | DRAFT v1.4 기준 유지 |

---

## 🔍 미변경 카테고리 — 재검사 결과

| 카테고리 | 재검사 상태 | 차단 원인 | 대안 확인 |
|---|---|---|---|
| 1. CXL 스펙/표준 | **미변경** | CXL 4.0 Feb 26 — Synopsys CXL 4.0 IP (23호 delta-2 반영) | 신규 없음 |
| 2. CXL 디바이스/미디어 | **미변경** | DRAFT v1.4 기준 유지 | 신규 delta 없음 |
| 4. 풀링 SW/어플라이언스 | **미변경** | 삼성 블로그 (23호 반영) | 신규 없음 |
| 5. 서버 OEM | **미변경** | Dell/HPE/Supermicro 신규 CXL 발표 없음 | 신규 delta 없음 |
| 6. CPU/GPU CXL | **미변경** | Intel/AMD/NVIDIA 신규 CXL 발표 없음 | 신규 delta 없음 |
| 7. AI 패브릭 | **미변경** | DRAFT 기준 유지 | 신규 없음 |
| 8. Main Memory | **미변경** | DRAFT v1.4 기준 유지 | 신규 delta 없음 |
| 9. AI Rack/KV offload | **미변경** | Mooncake/vLLM DRAFT v1.3 반영 | 신규 delta 없음 |
| 10. LLM TCO | **미변경** | DRAFT v1.4 기준 유지 | 신규 delta 없음 |
| 11. 메모리 가격 | **미변경** | DRAFT v1.4 기준 유지 | 신규 delta 없음 |
| 12. 시장/CSP | **미변경** | DRAFT v1.4 기준 유지 | 신규 delta 없음 |

---

## 📊 데이터 한계 공개

- **🟢 자동화(사실층)**: `python search.py` DuckDuckGo 기반 12카테고리 전수 조사. 원시 데이터 `sources/cxl-daily-raw-2026-08-29.md`에 보존.
- **🔴 LLM 종합(해석층)**: Delta 식별, 등급 부여, [해석] 서술은 LLM 추론.
- **📝 사실/의견 분리**: `[영향]`(제공자 발언 인용)과 `[해석]`(LLM CXL 분석) 엄격 분리 준수.
- **검색 품질 한계**: `python search.py`가 영어 기술 키워드에서 낮은 관련성 결과 반환. 한국어/프랑스어/일본어 결과가 영어 기술 소식을 대체. Global Semi Research, StorageNewsletter, Synopsys Blog, computeexpresslink.org 등 유용한 결과는 일부 수집됨.
- **단일 출처**: Big Three 인하우스 컨트롤러 포기 — Global Semi Research 1개 출처. 교차검증 필요. Primemas 정보 부족 — 출처 1개, 프로필 미확인.

---

## ⚡ 후속 액션

1. **[다음 발행]** 컨트롤러 벤더(3번) — Primetas 프로필 확인 (FMS 2026 신규 참가자). Global Semi Research 기사 원문 재확인 (Big Three in-house controllers 포기)
2. **[DRAFT 보강]** Global Semi Research 기사 원문 읽기 — Big Three가 각각 어떤 컨트롤러를 포기했는지, 외부 벤더와 어떤 계약을 체결했는지 상세 확인 → DRAFT 3장/11.3장 정밀화
3. **[다음 발행]** DRAM 가격/수급 — SK Hynix/Samsung/Micron 최신 실적/가이던스 재시도

---

## 📝 발행 정보

- **보고서**: CXL Daily Update 25호
- **MD 경로**: `wiki/daily-updates/cxl-daily-update-2026-08-30.md`
- **HTML 경로**: `Results/cxl-daily/cxl-daily-report-2026-08-30-0501.html`
- **원시 데이터**: `sources/cxl-daily-raw-2026-08-29.md`
- **DRAFT 반영 계획**: ★★ 1건 — DRAFT 2.6절 + 11.3장 반영 (v1.4 → v1.5)
- **delta 건수**: ★★ 1건, ★ 1건, 미변경 10건
- **DRAFT 버전**: v1.4 → v1.5 승격

---

*CXL Daily Update 25호 발행 완료 — MD 발행, DRAFT v1.5 반영 예정*
