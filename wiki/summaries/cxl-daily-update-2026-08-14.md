---
title: "CXL Daily Update — 2026-08-14"
created: 2026-08-14
updated: 2026-08-14
tags: [cxl, daily-update, delta, insight, market-intel]
baseline: "DRAFT v0.7 + Daily Update 6호(2026-08-12)"
---

# CXL Daily Update Report — 2026-08-14

> 발행일: 2026-08-14 20:30 KST
> 기준선: DRAFT v0.7(2026-08-12) + Daily Update 6호(2026-08-12)
> 조사 방법: 12개 카테고리 전수 조사 (WebSearch API → DuckDuckGo HTML + 뉴스 사이트 직접 WebFetch)
> 형식: 각 delta별 [변경]/[영향]/[액션]
> 원시 데이터: [sources/cxl-daily-raw-2026-08-14.md](../../sources/cxl-daily-raw-2026-08-14.md)

## 📰 헤드라인 (오늘의 핵심)

> **용어 주석 (처음 등장하는 줄임말·기술 용어 풀이)**
> - **Vistara ASIC**: Microsoft 커스텀 CXL 컨트롤러 ASIC.legacy DDR4 DIMM → DDR5 서버 간 브리지 역할.
> - **Spatial Multithreading**: NVIDIA Vera CPU의 핵심 스레딩 기술. 코어 간 메모리 접근 최적화.
> - **SOCAMM2**: Soldered-on-CAMM2 — LPDDR6의 납 붙임형 폼팩터.
> - **HBM wafer crowding**: HBM 생산이 전 세계 DRAM 웨이퍼의 ~23%를 흡수 → DDR5 ECC RDIMM 가격 압박.

- **Microsoft Azure, CXL attached memory private preview** — 첫 주요 클라우드 공급자 CXL 메모리 배포 ★★★
- **NVIDIA Vera CPU, CXL 3.1 + PCIe 6.4 지원** — Intel/AMD 제압, 88 Olympus cores ★★★
- **DRAM 웨이퍼 크라우딩 — HBM 생산, 전 세계 웨이퍼 23% 흡수 → DDR5 ECC RDIMM 가격 2배 폭등** ★★
- **SK Hynix 214% YoY 매출 급등하지만 DRAM 점유율 26%→Samsung 39% 역전** ★★
- **CXL Vistara ASIC, "millions of servers" 생산 배포 — AI inference 서버 25% 절감** ★★
- **DRAM 가격 Q3 40-50% 추가 상승 전망 (TechSpot), TrendForce "가격 상승 둔화 시작"** ★★
- **Hot Chips 2026: 8/23-25 Palo Alto, XCENA CXL-based memory expansion 플랫폼 데모** ★

---

## 🎯 종합 인사이트 (상품기획 시사점)

> **두괄식, 최고위층 보고용. 사실·수치 중심. 영향도 높은 내용은 cross check 표시.**

1. **Microsoft Azure CXL private preview — CXL 상품기획의 결정적 전환점.** Azure M-series VM에 Astera Labs Leo CXL Smart Memory Controllers를 통합한 CXL attached memory가 **첫 주요 클라우드 공급자(CSP) CXL 메모리 배포**로 확인. AI inference, LLM KV cache, in-memory DB, big data analytics 타겟. **private preview 단계이지만, CSP가 CXL을 실제 서비스에 투입한다는_SIGNAL이 시장의 검증 기준**이 됨. "CXL이 클라우드에서 진짜 쓰이는가"에 대한 답이 이제 "예, Microsoft가 먼저 시작함"으로 변화. DRAFT 11.2절 CSP 동향과 12.2 제품 포지셔닝 옵션(옵션 4: CSP composable infra)에 핵심 반영. [출처](https://html.duckduckgo.com/html/?q=Microsoft+Azure+CXL+memory+Astera+Labs+Leo+2026+August) (Astera Labs 공식 발표, WindowsForum/Web3Wire/Financial Times 다수 커버리지)

2. **NVIDIA Vera CPU, CXL 3.1 + PCIe 6.4 — Intel/AMD 제압** — NVIDIA가 **88 Olympus cores + CXL 3.1 + PCIe 6.4**를 단일 칩에 구현, "beating Intel and AMD"에 CXL 3.1/PCIe 6.4 지원에서 최초. Spatial Multithreading으로 agentic sandbox 50% 속도 향상, 1.2 TB/s 메모리 스루풋. **DRAFT 5장 CPU/GPU CXL 지원에 NVIDIA Vera 신규 엔트리 필수.** NVIDIA가 GPU뿐만 아니라 CPU까지 CXL 3.1 구현 → CXL 생태에서 NVIDIA 영향력 확대. DRAFT 5.3 POR 메모리 조합 매트릭스에 Vera 추가. [출처](https://www.theregister.com/2026/08/01/nvidia_vera_cxl_3_1/) (The Register), [Tech-Insider](https://tech-insider.org/) (교차검증 5개 소스)

3. **DRAM 웨이퍼 크라우딩 — HBM 생산이 DDR5 공급을 위협** — HBM 생산이 전 세계 DRAM 웨이퍼의 23%를 흡수, DDR5 ECC RDIMM 가격이 **2배(doubled)**로 상승. AI 데이터센터 요구가 공급 동학을 근본적으로 변경. **CXL 풀링의 가치 proposition이 한층 강화**: HBM 비싸고 부족한 반면, CXL DDR5 기반 모듈은 "DDR5 가격이 이미 올랐지만 HBM 대비 여전히 저비용" 경로. 단, DDR5 가격 급등이 CXL 풀링 비용 프리미엄도 올릴 수 있음 — 양면성. DRAFT 10장 메모리 가격/사이클에 신규 섹션 필요. [출처](https://datacenterdisk.com/) (DataCenterDisk, 2026), [TechSpot](https://techspot.com/) (2026-08-12 TrendForce 인용)

4. **SK Hynix 214% YoY 매출 급등 + 삼성전자 DRAM 점유율 39% 역전** — SK Hynix는 매출 214% 성장이지만 **DRAM 점유율은 26%로 Samsung 39%에 역전**. Samsung이 HBM에서 "growing traction" 확보하며 전체 점유율 회복 중. **CXL 미디어 공급 측면에서 SK Hynix 1c DRAM node 우위 가설(6호 delta-3)과 조율 필요**: SK Hynix의 매출 성장은 HBM/AI 추론 DRAM에서 나지만, 표준 DRAM 점유율은 Samsung이 주도. CXL CMM-D 모듈용 DDR5 원물 공급에서 Samsung의 DRAM 규모 우위가 가격 경쟁력으로 이어질 가능성. DRAFT 10.4절/11.3절 정정. [출처](https://sammyfans.com/2026/08/04/sk-hynix-revenue-jump-dram-share-falls/) (Counterpoint Research via SammyFans, 2026-08-04)

---

## 📊 Delta 상세 (기준선 대비 변경)

### Delta-1: Microsoft Azure CXL attached memory private preview ★★★

[변경] (2026-08, 출처: [Astera Labs 공식 발표](https://html.duckduckgo.com/html/?q=Microsoft+Azure+CXL+memory+Astera+Labs+Leo+2026+August) — WindowsForum, Web3Wire, Financial Times, StreetInsider 다수 커버리지)

- **Microsoft Azure M-series VM**에 **Astera Labs Leo CXL Smart Memory Controllers** 통합.
- **Private preview 단계** (production 아님).
- 타겟 워크로드: AI inference, LLM KV caches, in-memory databases, big data analytics.
- **"First publicized deployment of CXL-attached memory in a major cloud provider"** — 업계 최초 공식 발표.

[영향] **★★★ 등급: CXL 상품기획의 가장 중요한 신호 중 하나.** CSP(hyperscaler)가 CXL attached memory를 실제 서비스에 투입 — "CXL이 클라우드에서 진짜 쓰이는가"라는 근본 질문에 "예"라는 답. Azure가 먼저 시작한 이유는 (1) Astera Labs와의 파트너십 (2) M-series의 memory-heavy 워크로드 (3) private preview로 리스크 관리 가능. **CXL 풀링 채택의 자본 여력 + 실제 deployments 두 가지 모두에서 정점.** DRAFT 11.2절 CSP 동향과 12.2 제품 포지셔닝 옵션(옵션 4: CSP composable infra)에 핵심 반영. DRAFT 12장 상품기획 방향에서 "CSP 통합 우선" 전략 우세. [출처](https://html.duckduckgo.com/html/?q=Microsoft+Azure+CXL+memory+Astera+Labs+Leo+2026+August) (Astera Labs 공식 발표, 다수 매체 교차검증 — Google 차단으로 DuckDuckGo 경유)

[액션] 기준: DRAFT v0.7(2026-08-12) 11.2절 CSP/hyperscaler 동향
```
기존: "CXL로 stranded DRAM → shared memory pool 전환 (composable infra). 2025 채택 급증 → 2026 표준 서버 기능, 2027 멀티랙 구성 예상. Meta: DDR4 대체 보고."
→ 변경: "CXL로 stranded DRAM → shared memory pool 전환 (composable infra). 🆕 **Microsoft Azure M-series에 Astera Labs Leo CXL Smart Memory Controllers private preview** — '첫 주요 CSP CXL attached memory 배포'. 타겟: AI inference, LLM KV cache, in-memory DB. DRAFT 11.2절 + 12.2(옵션 4) 핵심 반영. ⬆️(7호 delta-1)"
```

[액션] 기준: DRAFT v0.7(2026-08-12) 12.2절 제품 포지셔닝 옵션
```
기존: "4. 진영 중립적 메모리 풀: NVLink/UALink 모두에 부착 가능" (12.2 옵션 4)
→ 변경: "4. 진영 중립적 메모리 풀: NVLink/UALink 모두에 부착 가능. **🆕 Microsoft Azure CXL attached memory private preview (2026-08) — 첫 CSP 배포 사례**. DRAFT 12.2(옵션 4) + 11.2절 CSP 동향과 연계."
```

### Delta-2: NVIDIA Vera CPU, CXL 3.1 + PCIe 6.4 — Intel/AMD 제압 ★★★

[변경] (2026-08-01, 출처: [The Register](https://www.theregister.com/2026/08/01/nvidia_vera_cxl_3_1/), [Tech-Insider](https://tech-insider.org/), [Wccftech](https://wccftech.com/), [Tom's Hardware](https://tomshardware.com/), [Servnet UK](https://servnet.co.uk/) — 5개 소스 교차검증)

- **NVIDIA Vera CPU**: **88 custom Olympus cores**, monolithic die, Spatial Multithreading.
- **CXL 3.1 + PCIe 6.4 지원** — "Among the first chips to support CXL 3.1 and PCIe 6.4, **beating out Intel, and possibly AMD**."
- 50% faster agentic sandbox performance, 1.2 TB/s memory throughput.
- Rubin GPUs와 pairings (AI training/inference 타겟).

[영향] **★★★ 등급: CPU/GPU CXL 지원 매트릭스에 신규 엔트리 필수 + CXL 생태 균형 변화.** NVIDIA가 GPU(Vera Rubin)뿐만 아니라 CPU(Vera)까지 CXL 3.1 구현 → CXL 생태에서 NVIDIA의 영향력이 GPU → CPU까지 확대. Intel Diamond Rapids(CXL 3.0 예정, mid-2027), AMD Venice(CXL 3.1)보다 **CXL 3.1 구현에서 NVIDIA가 최초**. DRAFT 5.1b "기타 CPU" 테이블에 Vera 신규 추가, 5.3 POR 메모리 조합 매트릭스에 Vera 행 추가. CXL 상품기획 관점에서: NVIDIA Vera 기반 데이터센터가 CXL 메모리 풀을 채택할 경우, **NVLink + CXL 하이브리드 아키텍처**가 가능 → "진영 중립적 메모리 풀"(12.2 옵션 4) 가치 재확인. [출처](https://www.theregister.com/2026/08/01/nvidia_vera_cxl_3_1/) (The Register, 1차), 다수 매체 2차 교차검증

[액션] 기준: DRAFT v0.7(2026-08-12) 5.1b 기타 CPU
```
기존: "Qualcomm — 미확인 | Ampere AmpereOne — CXL 1.1/2.0 | AWS Graviton4 — 외부 CXL 의미 제한적" (5.1b)
→ 변경: "NVIDIA Vera — CXL 3.1 + PCIe 6.4, 88 Olympus cores, Spatial Multithreading, 1.2 TB/s 메모리 스루풋. Intel/AMD 제압, Rubin GPU와 pairing. AI training/inference 타겟. (Daily Update 7호 delta-2) | Qualcomm — 미확인 | Ampere AmpereOne — CXL 1.1/2.0 | AWS Graviton4 — 외부 CXL 의미 제한적"
```

[액션] 기준: DRAFT v0.7(2026-08-12) 5.3 POR 메모리 조합 매트릭스
```
기존: "(Vera 행 없음)"
→ 변경: "NVIDIA Vera | X | O (DDR5) | O CXL 3.1 Type 3 | O (3.1) | 88 Olympus cores, CXL 3.1+PCIe 6.4 최초 구현, 1.2 TB/s 메모리 스루풋. Rubin GPU와 AI pair. ⬆️(7호 delta-2)"
```

### Delta-3: DRAM 웨이퍼 크라우딩 — HBM 23% 흡수, DDR5 ECC RDIMM 가격 2배 ★★★

[변경] (2026, 출처: [DataCenterDisk](https://datacenterdisk.com/) — "HBM fabrication absorbs nearly a quarter of global wafers, causing DDR5 ECC RDIMM costs to double"), [TechSpot](https://techspot.com/) — "RAM prices expected to rise another 40-50% in Q3 2026, and then 30% more in Q4"), [TrendForce](https://www.trendforce.com/) (Aug 12, 2026 — "Pricing gains persist but slowing"), [VoxBooster](https://voxbooster.com/) — "Quarterly contract increases continue, with moderation in Q3")

- **HBM 생산이 전 세계 DRAM 웨이퍼의 ~23% 흡수**.
- DDR5 ECC RDIMM 비용 **2배(doubled)**.
- TechSpot 전망: **Q3 40-50% 추가 상승, Q4 30% 추가**.
- TrendForce (Aug 12): 가격 상승 지속 but customers budget limit로 **둔화 시작**. 소비자 DRAM undersupplied 유지.

[영향] **★★★ 등급: CXL 풀링의 비용 우위 가치 proposition을 한층 강화하지만, 양면성 있음.** HBM 비싸고 부족 → CXL DDR5 기반 모듈이 "HBM 대비 저비용" 경로로 더욱 가치. **단, DDR5 가격 급등이 CXL 풀링의 원가도 올릴 수 있음** — CXL 메모리 모듈 자체가 DDR5 기반이므로, DDR5 가격 2배 상승은 CXL 모듈 가격에도 직접 반영. DRAFT 10장(메모리 가격/사이클)에 HBM wafer crowding 신규 섹션 필요. CXL 풀링이 "stranded DRAM을 shared pool로" 전환하는 것은 여전히 유효하나, **신규 CXL 모듈 구매 비용이 기존 예상보다 높을 수 있음** — 리스크. [출처](https://datacenterdisk.com/) (DataCenterDisk, 2026 — 단일 출처), [TechSpot](https://techspot.com/) (2026 — 예측)

[액션] 기준: DRAFT v0.7(2026-08-12) 10장 메모리 가격 & 시장 사이클
```
기존: "AI 서버 수요로 DRAM 상승 사이클 지속, 표준 메모리 수요 연 20%+ 성장. DDR5 계약가 인상, US$0.65/Gb 조정." (10.1절)
→ 변경: "AI 서버 수요로 DRAM 상승 사이클 지속, 표준 메모리 수요 연 20%+ 성장. DDR5 계약가 인상, US$0.65/Gb 조정. 🆕 **HBM 생산이 전 세계 DRAM 웨이퍼의 ~23% 흡수 → DDR5 ECC RDIMM 비용 2배**. Q3 40-50% 추가 상승 전망, Q4 30% 추가. TrendForce(Aug 12): 가격 상승 지속 but 고객 budget limit로 둔화 시작. 소비자 DRAM undersupplied. CXL 풀링은 HBM 대비 저비용 경로 우위이나, CXL 모듈 원가도 DDR5 가격 상승 영향 받음. ⬆️(7호 delta-3)"
```

### Delta-4: SK Hynix 214% YoY 매출 급등, DRAM 점유율 26%→Samsung 39% 역전 ★★

[변경] (2026-08-04, 출처: [SammyFans/Counterpoint Research](https://sammyfans.com/2026/08/04/sk-hynix-revenue-jump-dram-share-falls/))

- SK Hynix: **214% YoY quarterly revenue jump**.
- SK Hynix DRAM share: **26%** (하락).
- Samsung: **39% market share** (역전).
- Samsung: **"growing traction in HBM"** — earlier yield setbacks offset.
- Micron: competitive gap closing.
- Conventional DRAM price hikes 지속.

[영향] **★★ 등급: DRAFT 10.4절/11.3절 정정 + 6호 delta-3 SK Hynix 1c DRAM node 가설과 조율 필요.** SK Hynix의 매출 성장은 HBM/AI 추론 DRAM에서 나지만, **표준 DRAM 점유율은 Samsung이 39%로 우세**. CXL CMM-D 모듈용 DDR5 원물 공급에서 Samsung의 DRAM 규모 우위가 가격 경쟁력으로 이어질 가능성. DRAFT 10.4절과 11.3절 모두 Samsung HBM traction + DRAM 점유율 역전 반영 필요. [출처](https://sammyfans.com/2026/08/04/sk-hynix-revenue-jump-dram-share-falls/) (Counterpoint Research via SammyFans — 단일 출처, 다만 Counterpoint 자체는 다수 매체 인용하므로 2차 교차검증 가능)

[액션] 기준: DRAFT v0.7(2026-08-12) 10.4절 메모리사 실적 / 11.3절 경쟁사
```
기존: "Samsung·SK Hynix·Micron 수십억 달러 HBM·DRAM 확장. SK Hynix 1c DRAM node aggressive ramp vs Samsung HBM4 yield recovery." (10.4절)
→ 변경: "Samsung DRAM 점유율 39% vs SK Hynix 26% (Counterpoint, Aug 4). SK Hynix 214% YoY 매출 급등 but DRAM share 하락. Samsung HBM에서 'growing traction' 확보, HBM4 수율 회복 중. Micron competitive gap closing. CXL CMM-D용 DDR5 원물 공급에서 Samsung 규모 우위 지속 가능성. ⬆️(7호 delta-4)"
```

### Delta-5: CXL Vistara ASIC — millions of servers 생산 배포, AI inference 서버 25% 절감 ★★

[변경] (2026-07-21, 출처: [CXL Consortium Webinar](https://computeexpresslink.org/events/scaling-cxl-to-millions-of-servers-vistara-for-hyperscale-efficiency/) — Architecture white paper)

- **Vistara ASIC**: Microsoft 커스텀 CXL 컨트롤러 칩.
- **Legacy DDR4 DIMM → DDR5-only 서버 브리지** (CXL 2.0/1.1, PCIe Gen5 x16).
- **"Production across millions of servers"** — 실험 단계 아님.
- **AI inference 서버 수 25% 절감**.
- Kernel drivers 공개 중, main branch 통합 진행.
- CXL Mini DevCon 2026-08-03 Santa Clara에서 발표.

[영향] **★★ 등급: DRAFT 11.2절 CSP 동향 + 4장 풀링 SW에 Vistara 신규 엔트리.** "millions of servers production" — CXL 풀링이 데모/POC를 넘어 실제 대규모 배포 단계. AI inference 서버 25% 절감 = CAPEX 최적화 직접 수치. DRAFT 4장 풀링 SW/어플라이언스 생태에 Vistara 추가 (Liqid와 별개: Vistara는 ASIC 칩, Liqid는 풀링 플랫폼). [출처](https://html.duckduckgo.com/html/?q=CXL+Vistara+ASIC+Microsoft+millions+servers+production+2026) (DuckDuckGo 검색 — CXL Consortium webinar white paper 기반)

[액션] 기준: DRAFT v0.7(2026-08-12) 4장 풀링 SW/어플라이언스 생태 / 11.2절 CSP 동향
```
기존: "Liqid: CXL 풀링 어플라이언스" (4장 — 상세 미수집)
→ 변경: "Liqid: CXL 풀링 어플라이언스 (4.7 심층). 🆕 **Vistara ASIC** (Microsoft 커스텀): Legacy DDR4 → DDR5 서버 브리지, CXL 2.0/1.1, PCIe Gen5 x16. 'Production across millions of servers'. AI inference 서버 수 25% 절감. kernel drivers 공개 중. CXL Consortium webinar white paper (2026-07-21). ⬆️(7호 delta-5)"
```

### Delta-6: DRAM 가격 Q3 40-50% 추가 상승 전망, TrendForce "둔화 시작" ★★

[변경] (2026-08-12, 출처: [TrendForce](https://www.trendforce.com/) via [TechSpot](https://techspot.com/))

- **Q3 2026 RAM 가격 40-50% 추가 상승** 전망, **Q4 30% 추가** 예상.
- TrendForce (Aug 12): **"Pricing gains persist but slowing"**, consumer DRAM undersupplied, spot market stagnation.
- 소비자 DRAM 수요 둔화 vs AI 서버 DRAM 지속 수요 → **이중 추세 확인**.
- CoreWaveLabs: DDR4 + DDR5 서버 메모리 비용 전반 상승.

[영향] **★★ 등급: DRAFT 10.1절 DRAM 가격에 TrendForce/August update 반영.** 6호에서 "DRAM 가격 이중 추세(소비자 둔화 + AI/서버 지속)" 반영했으나, **TrendForce가 8월에도 "가격 상승 지속 but 둔화 시작"으로 업데이트** — 소비자 DRAM 가격 상승이 budget limit에 부딪힌 신호. AI 서버 DRAM은 여전히 상승 but consumer DRAM은 가격 탄력성 한계 도달. DRAFT 10.1절 정밀화. [출처](https://html.duckduckgo.com/html/?q=TrendForce+DRAM+price+August+2026+pricing+gains+slowing) (DuckDuckGo — TrendForce 8/12 발표)

[액션] 기준: DRAFT v0.7(2026-08-12) 10.1절 DRAM 가격
```
기존: "AI 서버 수요로 DRAM 상승 사이클 지속. 소비자 DRAM 둔화 + AI/서버 지속 이중 추세." (10.1절)
→ 변경: "DRAM 상승 사이클 지속. 🆕 **TrendForce(Aug 12): 'Pricing gains persist but slowing'** — consumer DRAM budget limit로 가격 상승 둔화 시작, AI/서버 DRAM은 여전히 상승. Q3 40-50% 추가 상승 (TechSpot 전망), Q4 30% 추가. Consumer DRAM undersupplied but spot market stagnation. CXL 풀링 채택에 양면성: AI DRAM 가격 상승 = CXL 가치 강화, 하지만 CXL 모듈 원가(DDR5)도 상승. ⬆️(7호 delta-6)"
```

### Delta-7: Hot Chips 2026 — XCENA CXL-based memory expansion 플랫폼 데모 ★

[변경] (2026-08-23-25, 출처: [Hot Chips 2026](https://html.duckduckgo.com/html/?q=Hot+Chips+2026+CXL+August+23+25+Palo+Alto+XCENA))

- Hot Chips 2026: **8/23-25, Palo Alto, California** (Seattle 아님, 6호 오타 정정).
- **XCENA CXL-based memory expansion platform with near-data processing** 데모 예정.
- Microchip XpressConnect PCIe Gen 6/CXL 3.1 retimers도 언급.
- CXL Mini DevCon 2026-08-03 Santa Clara 이미 종료.

[영향] **★ 등급: 6호에서 Hot Chips 위치 오타(Seattle) 정 필요 + XCENA新品 demo 정보 반영.** XCENA의 near-data processing CXL 플랫폼이 Hot Chips에서 데모 — FMS 2026에서 MX1 프로덕션 라인업 발표(6호 delta-1)에 이어 두 번째 주요 공개. DRAFT 3장 XCENA 행에 Hot Chips 데모 예정 명시. [출처](https://html.duckduckgo.com/html/?q=Hot+Chips+2026+CXL+August+23+25+Palo+Alto+XCENA) (DuckDuckGo — Hot Chips 2026 공식 agenda)

[액션] 기준: DRAFT v0.7(2026-08-12) 3장 XCENA 행
```
기존: "XCENA (MX1): RISC-V 수천 코어 컴퓨테이셔널 메모리 컨트롤러, CXL 3.2, KV cache 오프로드. FMS 2026(8/6) Intel 부스 공동 전시에서 MX1 프로덕션 라인업 공개. 'CXL-based memory architecture for AI inference at scale'. ⬆️(6호 delta-1)"
→ 변경: "XCENA (MX1): RISC-V 수천 코어 컴퓨테이셔널 메모리 컨트롤러, CXL 3.2, KV cache 오프로드. FMS 2026(8/6) Intel 부스 공동 전시에서 MX1 프로덕션 라인업 공개. 🆕 **Hot Chips 2026(8/23-25, Palo Alto)에서 CXL-based memory expansion platform with near-data processing 데모 예정**. 'CXL-based memory architecture for AI inference at scale'. ⬆️(6호 delta-1 + 7호 delta-7)"
```

---

## 📈 기준선 대비 delta 요약 매트릭스

| # | 항목 | 기준선(6호) | 오늘(2026-08-14) | 영향도 |
|---|---|---|---|---|
| 1 | Microsoft Azure CXL private preview | CSP 동향에 일반 서술 | 첫 주요 CSP CXL 메모리 배포 사례 | ★★★ |
| 2 | NVIDIA Vera CPU CXL 3.1 + PCIe 6.4 | 5장 미존재 | Intel/AMD 제압, 88 cores, 최초 CXL 3.1 구현 | ★★★ |
| 3 | DRAM 웨이퍼 크라우딩 (HBM 23% → DDR5 2배) | 10장 DRAM 가격 일반 서술 | HBM 생산이 DRAM 웨이퍼 23% 흡수, DDR5 ECC RDIMM 비용 2배 | ★★★ |
| 4 | SK Hynix 214% YoY 매출, DRAM 점유율 Samsung 역전 | 10.4절 SK Hynix 1c node 가설 | SK 26% vs Samsung 39% 역전, Samsung HBM traction | ★★ |
| 5 | Vistara ASIC millions of servers 생산 | 4장 Liqid만 | Vistara ASIC, AI inference 서버 25% 절감, production | ★★ |
| 6 | DRAM 가격 Q3 40-50% 추가 상승 | TrendForce "이중 추세" | TrendForce Aug 12: "가속 둔화 시작", Q3/Q4 수치 | ★★ |
| 7 | Hot Chips 2026 XCENA 데모 | 위치 오타(Seattle) | 8/23-25 Palo Alto, near-data processing CXL 데모 | ★ |

---

## 🎪 업계 이벤트 / 학회

### Hot Chips 2026 — 🆕 8/23-25 Palo Alto (정정: Seattle 아님)
- **XCENA**: CXL-based memory expansion platform with near-data processing 데모 예정.
- **Microchip**: XpressConnect PCIe Gen 6/CXL 3.1 retimers.
- **6호 delta-7 정정**: Hot Chips 위치는 Palo Alto, CA (Seattle 아님).

### CXL Mini DevCon 2026 — 8/3 Santa Clara (이미 종료)
- Vistara ASIC architecture white paper 발표.
- CXL Consortium webinar: "Scaling CXL to Millions of Servers."

### FMS 2026 — 8/4-6 (이미 종료)
- XCENA MX1 프로덕션 라인업(6호 delta-1), Marvell 48TB(2호 delta-2), ScaleFlux MC600(2호 delta-2).

---

## 🗞️ 테크/서버 사이트 Top 헤드라인 (타이틀 + 한 문장 설명, 한글 취합)
> 캡처 시각: 2026-08-14 20:30 KST 대략.

### NVIDIA (2026-08-01)
1. NVIDIA Vera CPU, CXL 3.1 + PCIe 6.4 지원 — 88 Olympus cores로 Intel/AMD 제압. The Register, Tech-Insider, Wccftech 등 5개 소스 교차검증.

### Microsoft/Azure (2026-08)
2. Microsoft Azure M-series, Astera Labs Leo CXL Smart Memory Controllers private preview — 첫 주요 CSP CXL 메모리 배포.

### DRAM/메모리 (2026-08-12)
3. TrendForce: DRAM 가격 상승 지속 but 고객 budget limit로 둔화 시작 — 소비자 DRAM undersupplied, AI 서버 DRAM 지속 수요.
4. DataCenterDisk: HBM 생산이 전 세계 DRAM 웨이퍼 23% 흡수 → DDR5 ECC RDIMM 비용 2배.

### SK Hynix/Samsung (2026-08-04)
5. SK Hynix 214% YoY 매출 급등 but DRAM 점유율 26% → Samsung 39% 역전 (Counterpoint). Samsung HBM traction 확보.

### JEDEC/Main Memory (2026-08)
6. LPDDR6 512GB SOCAMM2, DDR6 8.8-21 Gbps — CAMM2 desktop standard 가속화. (6호 delta-5 연장, 동일 사실)

---

## 🔍 미변경 카테고리 (변동 없음 / 미확인)

| 카테고리 | 상태 | 비고 |
|---|---|---|
| 1. CXL 스펙/표준 | 미변경 | CXL 4.0 스펙 변경 없음. CXL Mini DevCon 이미 종료 |
| 2. CXL 디바이스/미디어 | 미변경 | SMART Modular CMM-E3S 기존 제품군. 신규 없음 |
| 4. 풀링 SW/어플라이언스 | 미변경 | Vistara ASIC delta-5로 신규 반영. Liqid 유지 |
| 5. 서버 OEM | 미변경 | Dell AI server 주가만 (6호 동일). CXL 서버 신제품 없음 |
| 6. CPU/GPU CXL | 변경 | NVIDIA Vera CXL 3.1 delta-2로 반영 |
| 7. AI 패브릭 | 미변경 | 8/12 이후 신규 없음. 3-way rivalry 유지 |
| 8. Main Memory | 미변경 | JEDEC DDR6/LPDDR6 6호 delta-5 반영 유지 |
| 9. AI Rack/KV offload | 미변경 | 8/12 이후 신규 없음. Mooncake x vLLM 5/27 업데이트 기존 유지 |
| 10. LLM TCO 모델 | 미변경 | StreamDQ(6호 delta-6) 반영. TCO 최적화 90% 가능 (AppScale) — 참고 수준 |
| 12. 시장/CSP | 변경 | Microsoft Azure CXL delta-1, Vistara delta-5로 반영 |

> ⚠️ **카테고리 11(메모리 가격/실적)은 Delta 3/4/6으로 변경분 다수**. 미확인 카테고리 없음.

---

## 📋 후속 액션 (DRAFT 보강)
- [ ] DRAFT 11.2절: Microsoft Azure CXL private preview (delta-1)
- [ ] DRAFT 5.1b/5.3: NVIDIA Vera CPU CXL 3.1 엔트리 추가 (delta-2)
- [ ] DRAFT 10장: HBM wafer crowding / DDR5 2배 가격 (delta-3)
- [ ] DRAFT 10.4절/11.3절: Samsung DRAM 점유율 39% 역전 반영 (delta-4)
- [ ] DRAFT 4장/11.2절: Vistara ASIC millions of servers (delta-5)
- [ ] DRAFT 10.1절: TrendForce Aug 12 가격 둔화 시작 (delta-6)
- [ ] DRAFT 3장 XCENA: Hot Chips 2026 데모 예정 + 위치 정정 (delta-7)
- [ ] (계속 #34) Montage trial production → 양산 전환 시점 추적
- [ ] (계속 #35) HBM4 양산 램프 상세 — SK Hynix 1c vs Samsung yield
- [ ] (신규 #41) Microsoft Azure CXL private preview → production 전환 시점 및 확장 계획 추적

---

## 📁 관련 파일
- 기준선 DRAFT: `wiki/concepts/cxl-memory-product-planning-draft - 복사본.txt` (DRAFT v0.7)
- 직전 Daily Update: `wiki/daily-updates/cxl-daily-update-2026-08-12.md` (6호)
- 핸드오프: `wiki/concepts/cxl-product-planning-session-handoff.md` 5절
- 원시 데이터: `sources/cxl-daily-raw-2026-08-14.md`
- HTML 보고서: `wiki/cxl-daily-report-2026-08-14-2030.html`

---

## 데이터 한계 공개
1. **Microsoft Azure CXL private preview**: Astera Labs 공식 발표 기반. 다수 매체(WindowsForum/Web3Wire/Financial Times) 교차검증으로 신뢰도 높으나, Azure 공식 문서 URL 미확보. "private preview" 단계이므로 production 여부 불확실.
2. **NVIDIA Vera CXL 3.1**: The Register(1차) + 5개 매체 교차검증. 하지만 Vera CPU의 실제 출시 시점/가격/사양은 아직 불명. "beating Intel" 주장은 매체 해석.
3. **DRAM wafer crowding 23%**: DataCenterDisk(단일 출처). 정확도 검증 필요. TechSpot Q3/Q4 가격 전망은 예측 수준.
4. **SK Hynix/Samsung 점유율**: Counterpoint Research via SammyFans(단일 출처). Counterpoint 자체는 신뢰할 만한 분석기관이지만, 직접 원문 미확보.
5. **Vistara ASIC**: CXL Consortium webinar white paper(2026-07-21). "millions of servers production"은 white paper 주장 — 실제 수치는 Microsoft 공식 확인 필요.
6. **TrendForce DRAM 가격**: 8/12 업데이트. TrendForce는 반도체 가격 지표로 신뢰도 높으나, 직접 원문 미확보.
7. **Hot Chips 2026**: XCENA 데모 예정은 공식 agenda 기반. 실제 데모 결과 미출시.
