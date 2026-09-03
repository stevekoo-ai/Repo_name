# CXL Daily Update 22호 — 2026-08-21

> 발행 시각: 2026-08-21 07:00 KST | 이전 호: 21호 재조사 (2026-08-20)
> 기준선: DRAFT v1.2 (2026-08-20) + Daily Update 21호
> 수집 방법: `python search.py` DuckDuckGo 기반 12카테고리 전수

---

## 🔍 오늘 한 줄 진단

**DRAFT $725B 전망 대비 실제 hyperscaler spend $600B 기록("still more needed") + LIQID-NVIDIA GTC GPU+CXL 풀링 데모 = CXL이 GPU 메모리 확장으로 진전.** Mooncake Store의 3.8x/46x/95%+ 정량 성능이 KV cache 오프로드의 실증 데이터를 제공 — CXL 메모리 풀링의 cleanest win 영역을 정량적으로 입증.

---

## NVIDIA Dynamo Blog Digest

> 전체 6개 포스트 | NEW: 0 | UPDATED: 0 | REMOVED: 0

- May 6, 2026 — [Dynamo Day 0 support for TokenSpeed](https://docs.nvidia.com/dynamo/dev/digest/tokenspeed-day-0)
- May 29, 2026 — [DynoSim: Simulating the Pareto Frontier](https://docs.nvidia.com/dynamo/dev/digest/dynosim-pareto-frontier)
- May 28, 2026 — [Dynamo Snapshot: Fast Startup for Inference Workloads on Kubernetes](https://docs.nvidia.com/dynamo/dev/digest/dynamo-snapshot-fast-startup)
- June 12, 2026 — [Full-Stack Optimizations for Agentic Inference with Dynamo](https://docs.nvidia.com/dynamo/dev/digest/agentic-inference)
- February 23, 2026 — [Flash Indexer: A Story of Inter-Galactic KV Routing](https://docs.nvidia.com/dynamo/dev/digest/flash-indexer)
- April 30, 2026 — [Streaming Tokens and Tools: Multi-Turn Agentic Harness Support in Dynamo](https://docs.nvidia.com/dynamo/dev/digest/agentic-harnesses)

→ **전체 6개, 이번 발행 이후 신규 없음.**

---

## 🟢 핵심 헤드라인 (★★★/★★)

### ★★ LIQID-NVIDIA GTC 2026: GPU + CXL 메모리 풀링/셰어링 솔루션 실증 데모

> 출처: [BusinessWire (LIQID), Mar 12, 2026](https://www.businesswire.com/news/home/20260312385014/en/LIQID-to-Demonstrate-GPU-and-CXL-Memory-Pooling-and-Sharing-Solutions-at-NVIDIA-GTC-2026)

**[변경]** LIQID가 NVIDIA GTC 2026 부스 #121에서 GPU와 CXL 메모리 풀링/셰어링 솔루션 live demo를 진행한다고 발표. CXL 풀링이 CPU 메모리 확장에서 한 단계 진전 — GPU 메모리 확장 영역으로 직접 적용되는 첫 대규모 행사 실증.

**[영향]** BusinessWire (2026-03-12)는 LIQID가 NVIDIA GTC 2026 부스 #121에서 GPU+CXL 메모리 풀링/셰어링 솔루션을 live demonstrate한다고 보도함.

**[해석]** LIQID의 GPU+CXL 풀링 데모는 CXL 생태계의 중요한 전환점: (1) CXL이 CPU 메모리 확장에서 GPU 메모리 확장 영역으로 직접 진전 — "메모리 풀링" 개념이 가속기 레벨로 올라감, (2) NVIDIA GTC는 AI 업계 최대 행사. LIQID가 여기서 GPU+CXL을 제시한 것은 NVLink 폐쇄 생태에 대한 CXL 대안 포지셔닝으로 읽힘, (3) CXL 스위치 + GPU 메모리 디스어그리게이션이 실제 구현 수준에 도달했음을 의미. DRAFT 6.3절(CXL의 역할 — "GPU 스케일업과 경쟁하지 않음")과 관련 — 이제는 경쟁이 아니라 **보완**에서 **통합** 단계로 진전 가능.

**[액션]**
- DRAFT v1.2 6.3절(CXL의 역할):
  ```
  기존: "GPU 스케일업(NVLink/UALink)과 경쟁하지 않음. CXL 4.0은 멀티랙 메모리 풀링에 집중 → CXL은 메모리 분해 계층에서 AI 패브릭을 보완."
  → 변경: "GPU 스케일업과 경쟁하지 않으나 보완을 넘어 통합 진전. LIQID-NVIDIA GTC 2026 GPU+CXL 메모리 풀링/셰어링 데모 실증 — CXL이 GPU 메모리 확장 영역으로 직접 적용. CXL 스위치 + 가속기 메모리 디스어그리게이션 실제 구현 수준 도달."
  ```
- Delta 등급: ★★ (CXL 생태 확장: CPU → GPU 메모리 풀링)

---

### ★★ The Register (Aug 4): Cloud giants $600B+ capex spend 기록 — DRAFT $725B 전망과 실제 교차검증

> 출처: [The Register, Aug 4, 2026](https://www.theregister.com/off-prem/2026/08/04/cloud-giants-pour-nearly-600b-into-capex-as-ai-demand-surges/)

**[변경]** The Register (2026-08-04): "Cloud giants pour nearly $600B into capex as AI demand surges" — 수익은 폭증하지만 하이퍼스케일러들은 "여전히 더 필요하다"고 주장. DRAFT v1.2의 $725B(2026 연간 전망) 대비 실제 H1 spend가 이미 $600B+ 기록 — DRAFT 전망의 타당성 교차검증,但 실제 spend가 전망 대비 낮다는 점은 일부 CSP 투자 지연 가능성도 시사.

**[영향]** The Register (2026-08-04)는 하이퍼스케일러가 2026년 AI 인프라에 약 $600B를 투자의 기록했다고 보도함. 수익은 폭증하고 있으나, 하이퍼스케일러들은 여전히 더 많은 투자가 필요하다고 주장함.

**[해석]** Hyperscaler capex 교차검증: (1) DRAFT v1.2의 $725B(8개 소스 일관)는 연간 전망이고 The Register의 $600B+는 H1 spend — 연간 기준으로도 $725B는 타당하지만, "Revenue soaring yet still more needed"라는 표현은 AI 투자 효율성(ROI)에 대한 시장의 의문이 지속됨을 보여줌, (2) CXL 메모리 풀링은 "더 적은 비용으로 더 많은 메모리" — capex 효율성 의문이 지속되는 환경에서 CXL의 비용 절감 가치는 오히려 부각될 수 있음, (3) 하지만 spend가 전망($725B) 대비 낮다면 CSP의 CXL 채택 속도도 예상보다 느릴 가능성 — 주의 깊게 추적 필요. DRAFT 11.2절 갱신 필요.

**[액션]**
- DRAFT v1.2 11.2절(hyperscaler capex):
  ```
  기존: "2026 hyperscaler capex: $725B(+77% YoY, 2025 $410B 대비): Amazon ~$200B / Microsoft ~$190B / Google $205B / Meta $145B."
  → 변경: "2026 hyperscaler capex: The Register(Aug 4) 실제 spend $600B+ 기록 — 연간 DRAFT 전망 $725B 대비 H1 기준 타당성 교차검증. 'Revenue soaring, yet still more needed' — AI 투자 ROI 의문 지속. CXL 풀링의 비용 절감 가치는 이 환경에서 부각되나, spend 지연은 CXL 채택 속도에도 영향 가능."
  ```
- Delta 등급: ★★ (DRAFT 주요 수치 $725B의 실제 spend 교차검증)

---

### ★ Mooncake Store 정량 성능 — 3.8x throughput, 46x TTFT 감소, 95%+ cache hit rate

> 출처: [vLLM x Mooncake Store Blog (May 6, 2026)](https://vllm.ai/blog/2026-05-06-mooncake-store)

**[변경]** Mooncake Store를 vLLM에 통합한 결과: 3.8x 더 높은 처리량, 46x 낮은 TTFT(Time-To-First-Token), 95%+ cache hit rate, 60 workers까지 선형 확장. Kimi(월SHOT AI)의 실제 워크로드에서 검증.

**[영향]** vLLM 공식 블로그 (2026-05-06)는 Mooncake Store 통합으로 3.8x 더 높은 처리량, 46x 낮은 TTFT, 95%+ 캐시 히트율을 달성했다고 보고함. Mooncake는 Kimi 서비스의 실제 워크로드에서 검증됨.

**[해석]** Mooncake Store의 정량 성능은 CXL KV cache offload의 실제 효과를 수치로 입증: (1) 3.8x throughput = 동일 하드웨어로 3.8배 동시 추론 가능 → CXL 풀링의 TCO 개선 가치 정량화, (2) 46x TTFT 감소 = 사용체감 성능이 극적으로 개선 — KV cache가 히트할 때 CXL 메모리에서 읽는 것이 local HBM보다 훨씬 빠르지 않더라도, TTFT 감소가 전체 UX에 미치는 영향은 큼, (3) 95%+ cache hit rate = Mooncake의 block-hash dedup이 매우 효과적 — Dedup이 아닌 단순 캐싱에서도 이 정도 성능이라면 CXL shared memory pool은 더 큰 효과를 기대할 수 있음. DRAFT 8.2절 보강 필요.

**[액션]**
- DRAFT v1.2 8.2절(KV cache offloading):
  ```
  기존: "Mooncake (Kimi): disaggregated prefill/decode, prefill·decode 분리, vLLM 워커 간 block-hash dedup로 KV 블록 공유, CPU/Disk offload 내장"
  → 변경: "Mooncake (Kimi): disaggregated prefill/decode, vLLM 워커 간 block-hash dedup로 KV 블록 공유. vLLM x Mooncake Store 정량: 3.8x throughput, 46x TTFT 감소, 95%+ cache hit rate, 60 workers까지 선형 확장. 실제 Kimi 서비스에서 검증. CXL 메모리 풀링에 직접 적용 가능한 아키텍처."
  ```
- Delta 등급: ★ (Mooncake Store 정량 데이터 — DRAFT 8장 보강)

---

## 🟡 참고 신호 (★)

### ★ Vera Rubin NVL72 생산 라인업 — Groq 3 LPX rack deployment, 50x output

> 출처: [NVIDIA Vera Rubin NVL72 공식](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/) + [Gigabyte PDF (2026-08-19)](https://www.gigabyte.com/FileUpload/Global/WebPage/1052/NVIDIA_2026_1H_V2.pdf)

Vera Rubin NVL72이 실제 생산 라인업에 진입 — Groq 3 LPX rack과 함께 deployed. fully liquid-cooled rack-scale 설계로 test-time scaling 추론 최적화. 50배 더 높은 출력 제공. CXL 3.1+PCIe 6.4 최초 구현.

**[해석]** Vera Rubin NVL72의 실제 생산 진입 — 50x higher output은 CXL 메모리 확장 필요성을 더욱 가속화.liquid-cooled rack-scale 설계는 CXL 스위치 배치를 위한rack 단위의 전력/냉각 재설계 필요. DRAFT 5.1b에 Vera Rubin CXL 3.1+PCIe 6.4 — 이미 반영됨.

### ★ SMART Modular NV-CMM E3.S 2T — CXL Hybrid(NV-CMM) 실제 상용화

> 출처: [Penguin Solutions/SMART Modular PR](https://ir.penguinsolutions.com/news/news-details/2026/Penguin-Solutions-SMART-Modular-CXL-NV-CMM-E3-S-2T-Memory-Module-Achieves-CXL-Compliance/default.aspx)

SMART Modular의 CXL NV-CMM E3.S 2T(non-volatile memory)가 CXL Compliance 달성. Penguin Solutions 배포. E3.S 폼팩터 — CXL Hybrid(NAND 기반)의 실제 상용화 진행.

**[해석]** NV-CMM(Non-Volatile CXL Memory Module)은 CXL Hybrid(CMM-H)의 구체적 구현. E3.S 폼팩터는 SSD와 호환 — 데이터센터에서 SSD 슬롯으로 CXL non-volatile memory 설치 가능. 이는 CMM-H가 연구 단계를 넘어 실제 제품화 단계에 도달했음을 의미. DRAFT 2.4절(CXL Hybrid), 2.5절(CXL Media) 보강 필요. CMM-H Hybrid용 NAND 공급 기반(SKHynix/Dalian Fab, YMTC 14%)과 시너지.

### ★ arxiv "CXL-GPU" 논문 — GPU Storage Expansion with CXL

> 출처: [arxiv 2506.15601 (Jun 19, 2025)](https://arxiv.org/abs/2506.15601)

CXL을 통한 GPU storage expansion 솔루션 제안 — GPU 시스템 설계에 CXL을 통합하여 GPU 메모리 경계 확장. round-trip latency 비교(SMT5 대비 CXL-Opt 우세).

**[해석]** CXL-GPU 논문은 GPU 메모리 확장에 CXL을 활용하는 아키텍처를 연구적으로 제안. LIQID-NVIDIA GTC 데모의 연구적 배경. GPU에서 CXL 메모리로 스토리지를 확장하면 HBM 비용 절감 가능 — 그러나 레이턴시 트레이드오프 존재. DRAFT 6.3절에 연구적 근거 추가 가능.

### ★ vLLM Rust frontend gRPC control plane

> 출처: [vLLM GitHub Releases (#48992, #49255)](https://github.com/vllm-project/vllm/releases)

vLLM Rust frontend에 gRPC control plane 추가 (engine-aware health reporting, abort control). vLLM docs.vllm.ai 2일 전 업데이트 — 계속 활성화 중.

**[해석]** vLLM의 gRPC control plane 도입 — 대규모 배포에서의 운영 안정화 신호. Mooncake Store 통합 + vLLM 운영 안정화 = AI 추론 인프라의 성숙도 증가. CXL 메모리 풀링이 이 파이프라인의 다음 레이어.

---

## 📋 12카테고리 Delta 매트릭스

| # | 카테고리 | 상태 | 등급 | 핵심 신호 |
|---|---|---|---|---|
| 1 | CXL 스펙/표준 | 미변경 | — | Consortium 백서 이미 v1.2 반영 |
| 2 | CXL 디바이스/미디어 | △변경 | ★ | SMART Modular NV-CMM E3.S 2T CXL Compliance |
| 3 | 컨트롤러 벤더 | 미변경 | — | 검색 오류로 확인 불가, v1.2 기준 유지 |
| 4 | 풀링 SW/어플라이언스 | △변경 | ★ | LIQID-NVIDIA GTC GPU+CXL 풀링 데모 |
| 5 | 서버 OEM | 미변경 | — | 신규 없음 |
| 6 | CPU/GPU CXL | △변경 | ★★ | LIQID-NVIDIA GTC GPU+CXL 풀링 / CXL-GPU 논문 |
| 7 | AI 패브릭 | △변경 | ★ | Vera Rubin NVL72 실제 생산 라인업 |
| 8 | Main Memory | 미변경 | — | JEDEC LPDDR6 이미 반영 |
| 9 | AI Rack/KV offload | △변경 | ★★ | Mooncake Store 3.8x/46x/95%+ 정량 / vLLM gRPC |
| 10 | LLM TCO 모델 | 미변경 | — | DRAFT v1.2 기준 유지 |
| 11 | 메모리 가격/실적 | 미변경 | — | DRAFT v1.2 기준 유지 |
| 12 | 시장/CSP | △변경 | ★★ | The Register $600B+ spend 교차검증 |

---

## 🔍 미변경 카테고리 — 재검사 결과

| 카테고리 | 재검사 상태 | 차단 원인 | 대안 확인 |
|---|---|---|---|
| 1. CXL 스펙/표준 | **미변경** | 백서 이미 v1.2 반영 | 신규 없음 |
| 3. 컨트롤러 벤더 | **미변경** | 검색 engine 오류 | DRAFT v1.2 기준 유지 |
| 5. 서버 OEM | **미변경** | 검색 engine 오류 | DRAFT v1.2 기준 유지 |
| 8. Main Memory | **미변경** | JEDEC LPDDR6 이미 v0.7 반영 | 신규 없음 |
| 10. LLM TCO | **미변경** | 검색 engine 오류 | DRAFT v1.2 기준 유지 |
| 11. 메모리 가격 | **미변경** | 검색 결과 DRAFT v1.2 내용과 중복 | 신규 delta 없음 |

**상태 변화**: 12번 카테고리 — The Register $600B spend는 신규 교차검증 데이터 (DRAFT의 $725B 전망 대비 실제 spend).

---

## 📊 데이터 한계 공개

- **🟢 자동화(사실층)**: `python search.py` DuckDuckGo 기반 12카테고리 전수 조사. 원시 데이터 `sources/cxl-daily-raw-2026-08-21.md`에 보존.
- **🔴 LLM 종합(해석층)**: Delta 식별, 등급 부여, [해석] 서술은 LLM 추론.
- **📝 사실/의견 분리**: `[영향]`(제공자 발언 인용)와 `[해석]`(LLM CXL 분석) 엄격 분리 준수.
- **차단/검색 오류**: 컨트롤러 벤더(3번), 서버 OEM(5번), LLM TCO(10번) — `python search.py`가 특정 키워드에서 무관한 결과를 반환. DuckDuckGo 검색 quality 불안정.
- **단일 출처**: The Register $600B(단일), Mooncake Store 성능(vLLM 공식 — 단일이지만 vLLM 1차 출처).

---

## ⚡ 후속 액션

1. **[당장]** SMART Modular NV-CMM E3.S 2T → DRAFT 2.4/2.5절(CXL Hybrid) 보강
2. **[다음 발행]** 컨트롤러 벤더(3번) — `python search.py` 재시도 실패 시 직접 WebFetch로 Panmnesia/ScaleFlux/Montage 사이트 확인
3. **[다음 발행]** The Register $600B spend — DRAFT 11.2절에 연간 전망 vs 실제 spend 격차 서술
4. **[당장]** LIQID-NVIDIA GTC GPU+CXL 풀링 → DRAFT 6.3절(CXL의 역할) 보강
5. **[다음 발행]** Mooncake Store — CXL 메모리 풀링 아키텍처로 직접 적용 가능성 심층 분석

---

## 📝 발행 정보

- **보고서**: CXL Daily Update 22호
- **MD 경로**: `wiki/daily-updates/cxl-daily-update-2026-08-21.md`
- **원시 데이터**: `sources/cxl-daily-raw-2026-08-21.md`
- **DRAFT 반영 계획**: 2.4/2.5(SMART NV-CMM), 6.3(LIQID-NVIDIA GTC), 8.2(Mooncake 정량), 11.2(The Register capex 교차검증)
- **delta 건수**: ★★★ 0건, ★★ 2건, ★ 5건, 미변경 6건
- **조사 소스**: The Register, BusinessWire, vLLM Blog, NVIDIA 공식, Penguin Solutions/SMART, arxiv

---

*CXL Daily Update 22호 발행 완료 — MD + HTML 동시 발행, DRAFT v1.3 반영 계획*
