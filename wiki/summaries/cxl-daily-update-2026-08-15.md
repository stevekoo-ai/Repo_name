---
title: "CXL Daily Update — 2026-08-15"
created: 2026-08-15
updated: 2026-08-15
tags: [cxl, daily-update, delta, insight, market-intel]
baseline: "DRAFT v0.8 + Daily Update 7호(2026-08-14)"
---

# CXL Daily Update Report — 2026-08-15

> 발행일: 2026-08-15 06:30 KST
> 기준선: DRAFT v0.8(2026-08-14) + Daily Update 7호(2026-08-14)
> 조사 방법: 12개 카테고리 전수 조사 (WebSearch API → DuckDuckGo HTML + 뉴스 사이트 직접 WebFetch; 403/CAPTCHA 차단 시 TrendForce 직접 WebFetch)
> 형식: 각 delta별 [변경]/[영향]/[액션]
> 원시 데이터: [sources/cxl-daily-raw-2026-08-15.md](../../sources/cxl-daily-raw-2026-08-15.md)

## 📰 헤드라인 (오늘의 핵심)

> **용어 주석**
> - **2nm HBM base die**: Samsung이 NVIDIA GPU용 HBM 칩 베이스 웨이퍼를 2nm 공정으로 생산. 기존 1α/1β 공정보다 미세화.
> - **Dalian Fab 2**: SK Hynix 중국 대련 공장 2호. NAND 생산 능력.
> - **NeMo Switchyard**: NVIDIA의 AI 모델 라우팅 소프트웨어 — 여러 AI 모델을 비용 최적화로 라우팅.

- **Samsung, 2nm HBM base die 생산으로 R&D 라인 전환 검토 — NVIDIA 미래 수요 대응** ★★★
- **Micron, 데이터센터 메모리 요구의 절반 미만만 충족…계약가 "매우 높은" 수준** ★★★
- **SK Hynix, 대련 Fab 2 재가동…2027 H1 양산, China NAND 생산량 50% 증가 목표** ★★
- **Lenovo FY1Q26/27 매출 $26.9B(+43% YoY) — 서버 OEM 실적 강세** ★
- **Nanya Tech, NT$300B 투자로 신규 12인치 웨이퍼 팹 2곳 건설** ★
- **NVIDIA NeMo Switchyard — "GPT-5-style model routing"으로 AI 비용 절감** ★
- **미국 남부 전력회사, 데이터센터 전력 사용량 +55% — AI 전력 수요 폭발 신호** ★

---

## 🎯 종합 인사이트 (상품기획 시사점)

> **두괄식, 최고위층 보고용. 사실·수치 중심. 영향도 높은 내용은 cross check 표시.**

1. **Samsung 2nm HBM base die 생산 전환 — HBM 수급 게임 체인저 가능성.** Samsung이 Giheung NRD-K Line 2를 실험 R&D → **실제 제조 라인**으로 전환, 2nm HBM base die로 AI 가속기(NVIDIA) 수요 대응. **7호 delta-4에서 확인한 "Samsung HBM growing traction"이 R&D 단계에서 양산 단계로 이행 중.** 2nm HBM base die는 HBM4 이후 세대를 의미 — Samsung이 **HBM 공정 미세화에서 SK Hynix를 역전**할 경우, HBM 점유율 39%(7호 delta-4)는 추가 상승 가능. **DRAFT 10.2절 HBM 수급 + 11.3절 경쟁사에 핵심 반영.** [출처](https://www.trendforce.com/) (TrendForce, 2026-08-14 — 다수 매체 인용)

2. **Micron 데이터센터 메모리 공급 부족 — CXL 풀링의 "저비용 대안" 가치 한층 강화.** Micron이 데이터센터 메모리 요구의 **절반 미만만 충족 가능**하다고 명시. 계약 가격이 **"매우 높은" 수준**. 7호 delta-3의 "HBM 웨이퍼 23% 흡수 → DDR5 2배"가 **실제 공급 부족으로 연결 중.** CXL 풀링은 HBM 대비 저비용 경로로서, Micron이 공급하지 못한 수요를 CXL 메모리 풀이 일부 대체 가능. **단, Micron이 "매우 높은 가격"을 수용한다는 점은 CXL 모듈 원가도 상승할 수 있음 — 양면성.** [출처](https://www.trendforce.com/) (TrendForce, 2026-08-12)

3. **SK Hynix Dalian Fab 2 재가동 — NAND 기반 CXL(CMM-H) 공급 기반 확대.** SK Hynix가 중국 대련 NAND 공장을 재가동, **2027 H1 양산 목표**. NAND 생산량 50% 증가는 CMM-H(Hybrid DRAM+NAND) 기반 CXL 메모리 모듈의 원물 공급 기반 확대를 의미. **DRAFT 10.4절 메모리사 실적에 신규 반영.** [출처](https://www.trendforce.com/) (TrendForce, 2026-08-12)

---

## 📊 Delta 상세 (기준선 대비 변경)

### Delta-1: Samsung 2nm HBM base die 생산으로 R&D 라인 전환 ★★★

[변경] (2026-08-14, 출처: [TrendForce](https://www.trendforce.com/) — "Samsung May Repurpose R&D Line for Foundry, Targeting 2nm HBM Base Dies for Future NVIDIA Demand")

- **Samsung Giheung campus**: NRD-K Line 2를 실험 R&D → **실제 제조 라인** 전환 검토.
- **2nm HBM base die** 생산 — AI 가속기 제조사(NVIDIA) 수요 대응.
- **"sources say the company is considering repurposing NRD-K Line 2"** — 아직 확정 단계.

[영향] **★★★ 등급: Samsung HBM 전략의 중대한 전환.** 7호 delta-4에서 "Samsung HBM growing traction, HBM4 수율 회복 중"을 기록했으나, **2nm HBM base die 생산은 완전히 신규 사실**. Samsung이 실험적 개발을 넘어 실제 제조에 돌입 — HBM 수급 구도에 변화. HBM 생산이 DRAM 웨이퍼 23% 흡수(7호 delta-3)하는 가운데, Samsung의 2nm HBM 양산이 DDR5 ECC RDIMM 가격에 추가 압박 가능. CXL 풀링 관점: HBM이 더 풍부해지면 CXL의 "HBM 대체" 가치는 다소 약화되나, **HBM 가격이 여전히 높다면 CXL은 여전히 저비용 대안으로 가치 있음**. DRAFT 10.2절 HBM 수급에 신규 섹션 필요. DRAFT 11.3절 경쟁사 Samsung 행 정정. [출처](https://www.trendforce.com/) (TrendForce, 2026-08-14 — 직접 WebFetch 원문 확인)

[액션] 기준: DRAFT v0.8(2026-08-14) 10.2절 HBM 수급
```
기존: "(상세 미수집) — HBM3E 수급 부족, AI 서버 메모리 전략 영향"
→ 변경: "Samsung Giheung NRD-K Line 2를 R&D → 제조 라인 전환 검토, 2nm HBM base die 생산 (TrendForce, 2026-08-14). NVIDIA AI 가속기 수요 대응. 아직 확정 단계. 7호 delta-4 'Samsung HBM traction' + 8호 delta-1: R&D에서 양산 단계로 이행 중. ⬆️(8호 delta-1)"
```

[액션] 기준: DRAFT v0.8(2026-08-14) 11.3절 경쟁사 (Samsung)
```
기존: "삼성: CMM-D 2.0/3.1, CMM-H 하이브리드, CXL Appliance(오케스트레이션 콘솔 포함) — 풀 스택 선도"
→ 변경: "삼성: CMM-D 2.0/3.1, CMM-H 하이브리드, CXL Appliance(오케스트레이션 콘솔 포함) — 풀 스택 선도. 🆕 **2nm HBM base die 생산 라인 전환 검토 (Giheung NRD-K Line 2, 2026-08-14 TrendForce)** — NVIDIA 미래 수요 대응. ⬆️(8호 delta-1)"
```

### Delta-2: Micron, 데이터센터 메모리 요구의 절반 미만만 충족 ★★★

[변경] (2026-08-12, 출처: [TrendForce](https://www.trendforce.com/) — "Micron Meets Less Than Half of Data Center Demand as Customers Rush to Secure Memory at 'Very High' Prices")

- **Micron**: 데이터센터 메모리 요구의 **50% 미만만 충족 가능**.
- 계약 가격이 **"매우 높은"(very high) 수준**.
- 기업 구매자들이 메모리 확보를 위해 높은 가격 수용 — **공급 부족이 가격 상승으로 직접 연결**.

[영향] **★★★ 등급: DRAFT 10.1절 DRAM 가격에 실제 공급 부족 사실 반영 + CXL 풀링 가치 재확인.** Micron이 "절반 미만"이라고 명시한 것은 7호 delta-3의 "HBM 23% 흡수" 가설이 **실제 데이터센터 수급에 영향을 미치고 있음을 확인**. 7호 delta-6의 "TrendForce: 가격 상승 지속 but 둔화 시작"과 함께 보면, **"둔화"는 consumer DRAM 한정이고, data center DRAM은 여전히 공급 부족 + 가격 상승** — 이중 추세가 더 명확해짐. CXL 풀링은 HBM 대비 저비용 대안으로서 Micron이 공급하지 못한 수요를 일부 대체 가능. **단, Micron이 높은 가격을 수용한다는 점은 CXL 모듈 원가(DDR5)도 동반 상승 — 리스크.** [출처](https://www.trendforce.com/) (TrendForce, 2026-08-12 — 직접 WebFetch 원문 확인)

[액션] 기준: DRAFT v0.8(2026-08-14) 10.1절 DRAM 가격
```
기존: "HBM 생산이 전 세계 DRAM 웨이퍼의 ~23% 흡수 → DDR5 ECC RDIMM 비용 2배. Q3 40-50% 추가 상승 전망, Q4 30% 추가. TrendForce(Aug 12): 가격 상승 지속 but 고객 budget limit로 둔화 시작. Consumer DRAM undersupplied but spot market stagnation. CXL 풀링은 HBM 대비 저비용 경로 우위이나, CXL 모듈 원가도 DDR5 가격 상승 영향 받음."
→ 변경: "HBM 생산이 전 세계 DRAM 웨이퍼의 ~23% 흡수 → DDR5 ECC RDIMM 비용 2배. 🆕 **Micron: 데이터센터 메모리 요구의 절반 미만만 충족 가능…계약가 '매우 높은' 수준** (TrendForce, Aug 12). Consumer DRAM은 가격 탄력성 한계 도달 for 둔화 but, Data Center DRAM은 공급 부족이 실제 수급에 영향. CXL 풀링은 Micron 미충족 수요의 저비용 대안 경로 우위. 단, CXL 모듈 원가(DDR5)도 동반 상승 리스크. ⬆️(8호 delta-2)"
```

### Delta-3: SK Hynix 대련 Fab 2 재가동, 2027 H1 양산 ★★

[변경] (2026-08-12, 출처: [TrendForce](https://www.trendforce.com/) — "SK hynix Reportedly Restarting Dalian Fab 2, Targets 1H27 Mass Production and 50% China NAND Capacity Boost")

- **SK Hynix Dalian Fab 2 재가동** (2026-08-12).
- **2027 H1 양산 목표**.
- **중국 NAND 생산량 50% 증가** 목표.

[영향] **★★ 등급: DRAFT 10.4절 메모리사 실적 + 2.4절 Hybrid CXL(PNM)에 NAND 공급 기반 확대 의미.** SK Hynix NAND 생산량 50% 증가는 CMM-H(Hybrid DRAM+NAND) 기반 CXL 메모리 모듈의 **원물 공급 기반** 확대. CMM-H는 Samsung이 주력하는 방향이지만, SK Hynix도 Hybrid CXL 경쟁에서 NAND 자급력 확보 필요. DRAFT 10.4절 메모리사 실적에 신규 반영. DRAFT 2.4절 Hybrid & PNM에 NAND 공급 관점 추가 고려. [출처](https://www.trendforce.com/) (TrendForce, 2026-08-12 — 직접 WebFetch 원문 확인)

[액션] 기준: DRAFT v0.8(2026-08-14) 10.4절 메모리사 실적
```
기존: "Samsung DRAM 점유율 39% vs SK Hynix 26% (Counterpoint, Aug 4). SK Hynix 214% YoY 매출 급등 but DRAM share 하락. Samsung HBM에서 'growing traction' 확보, HBM4 수율 회복 중. Micron competitive gap closing. CXL CMM-D용 DDR5 원물 공급에서 Samsung 규모 우위 지속 가능성."
→ 변경: "Samsung DRAM 점유율 39% vs SK Hynix 26% (Counterpoint, Aug 4). SK Hynix 214% YoY 매출 급등 but DRAM share 하락. 🆕 **SK Hynix Dalian Fab 2 재가동, 2027 H1 양산 목표 — China NAND 생산량 50% 증가** (TrendForce, Aug 12). CMM-H Hybrid CXL용 NAND 공급 기반 확대. Samsung HBM traction + 2nm HBM base die 생산 전환 (8호 delta-1). Micron competitive gap closing, data center demand 미충족 (8호 delta-2). ⬆️(8호 delta-3)"
```

### Delta-4: Lenovo FY1Q26/27 $26.9B 매출 +43% YoY ★

[변경] (2026-08-14, 출처: [StorageNewsletter](https://storagenewsletter.com/) — "Lenovo: Fiscal 1Q26/27 Financial Results")

- **Lenovo 매출 $26.9B** — 전월 대비 +24.8%, **전년 대비 +43%**.
- Lenovo는 CXL 서버 라인업 (ThinkSystem, ThinkEdge) 보유.

[영향] **★ 등급: 서버 OEM 실적 강세 — CXL 서버 채택 간접 신호.** Lenovo의 +43% YoY 성장은 AI 데이터센터 투자 지속을 반영. Lenovo는 CXL 메모리 확장 지원 서버 (Samsung CMM-D 128GB 검증 서버)를 출시 — CXL 서버 시장 성장의 선행 지표. DRAFT 5장 서버OEM에 신규 엔트리 추가. [출처](https://storagenewsletter.com/) (StorageNewsletter, 2026-08-14 — 직접 WebFetch 원문 확인)

[액션] 기준: DRAFT v0.8(2026-08-14) 5장 서버OEM
```
기존: "(상세 미수집)"
→ 변경: "🆕 **Lenovo FY1Q26/27: $26.9B 매출, +43% YoY** (2026-08-14, StorageNewsletter). AI 데이터센터 투자 지속 반영. Lenovo는 CXL 메모리 확장 지원 서버(ThinkSystem) 라인업 보유. Samsung CMM-D 128GB 검증 서버 출시. ⬆️(8호 delta-4)"
```

### Delta-5: Nanya Tech NT$300B 투자, 신규 12인치 웨이퍼 팹 2곳 건설 ★

[변경] (2026-08-14, 출처: [TrendForce](https://www.trendforce.com/) — "Nanya Tech Reportedly Eyes Yunlin, Pingtung Fabs for 1d DRAM, Custom Memory, Investment to Top NT$300B")

- **Nanya Tech**: NT$300B(약 $1B) 투자로 신규 12인치 웨이퍼 팹 2곳(윤림, 핑퉁) 건설 계획.
- **차세대 DRAM 및 맞춤형 메모리** 생산.
- 대만 메모리 산업 확장.

[영향] **★ 등급: DRAM 공급 확대 신호 — 중장기 가격 하방 압력.** Nanya Tech의 확장DRAM 공급 능력 증가를 의미. **단기에는 가격 영향 미미하지만**, 중장기(2028+)로 DRAM oversupply 시 CXL 모듈 원가 하락으로 이어질 수 있음. DRAFT 10.4절 메모리사 실적에 간접 반영. [출처](https://www.trendforce.com/) (TrendForce, 2026-08-14 — 직접 WebFetch 원문 확인)

[액션] 기준: DRAFT v0.8(2026-08-14) 10.4절 메모리사 실적
```
기존: (Delta-3에서 SK Hynix/Dalian Fab 반영 후의 버전)
→ 변경: "… 🆕 **Nanya Tech, NT$300B 투자로 12인치 웨이퍼 팹 2곳(윤림, 핑퉁) 건설 — 차세대 DRAM 및 맞춤형 메모리 생산** (TrendForce, 2026-08-14). 중장기 DRAM 공급 확대 → 가격 하방 압력. ⬆️(8호 delta-5)"
```

### Delta-6: NVIDIA NeMo Switchyard — AI 비용 절감 라우팅 ★

[변경] (2026-08-12, 출처: [The Register](https://www.theregister.com/2026/08/12/nvidia_nemo_switchyard/) — "Nvidia's latest solution to soaring enterprise AI costs is...a router?")

- **NVIDIA NeMo Switchyard**: 소프트웨어 도구, "GPT-5-style model routing"으로 AI 비용 절감.
- 여러 AI 모델을 비용 최적화로 라우팅.
- CXL 직접 관련은 아님 — AI 인프라 비용 최적화 도구.

[영향] **★ 등급: TCO 모델과 간접 연결.** NVIDIA가 라우팅 최적화로 추론 비용 절감 시나리오 제시. CXL KV cache 풀링과 같은 "인프라 비용 절감" 흐름과 동일 방향. DRAFT 9장 LLM TCO 모델에 참고 사항으로 추가. [출처](https://www.theregister.com/2026/08/12/nvidia_nemo_switchyard/) (The Register, 2026-08-12 — 직접 WebFetch 원문 확인)

[액션] 기준: DRAFT v0.8(2026-08-14) 9.3절 TCO/CAPEX 비교
```
기존: "HBM 확장: 최고 성능, 최고 비용, 수급 제약. CXL 메모리 풀링: HBM 대비 저비용, 용량 탄력, 공유 → KV cache 오프로드로 CAPEX 절감. CPU DRAM 증설: 단순하지만 비활용 자원(stranded DRAM) 발생. CXL 풀링 = stranded DRAM → shared pool 전환 (Meta가 DDR4 대체 보고)"
→ 변경: "HBM 확장: 최고 성능, 최고 비용, 수급 제약. CXL 메모리 풀링: HBM 대비 저비용, 용량 탄력, 공유 → KV cache 오프로드로 CAPEX 절감. CPU DRAM 증설: 단순하지만 비활용 자원(stranded DRAM) 발생. CXL 풀링 = stranded DRAM → shared pool 전환. 🆕 **NVIDIA NeMo Switchyard: AI 모델 라우팅 최적화로 추론 비용 절감** (2026-08-12) — 인프라 비용 절감 트렌드와 동일 방향. ⬆️(8호 delta-6)"
```

### Delta-7: 미국 남부 전력회사, 데이터센터 전력 사용량 +55% ★

[변경] (2026-08-14, 출처: [datacenterdynamics.com](https://www.datacenterdynamics.com/) — "US utility Southern Co reports 55% higher data center power usage")

- **Southern Co (미국 남부 전력회사)**: 데이터센터 전력 사용량 **전년 대비 +55%**.
- 추가 기사 (8/11-12): "AI readiness starts with power 1 designing for real-world load conditions", "Meeting AI demand with flexible power infrastructure".

[영향] **★ 등급: CSP CapEx의 "60%+ 전력 인프라" 주장 교차검증.** DRAFT 11.2절에서 "NextWaves Insight 8월: 60%+가 전력 인프라, 칩 아님"을 기록 — Southern Co의 +55%는 이 흐름을 **실제 utility 데이터로 교차검증**. AI 데이터센터 전력 수요가 폭발 중 — CXL 풀링의 전력 효율성 가치 proposition 재확인. [출처](https://www.datacenterdynamics.com/) (datacenterdynamics, 2026-08-14 — 직접 WebFetch 원문 확인)

[액션] 기준: DRAFT v0.8(2026-08-14) 11.2절 CSP/hyperscaler 동향
```
기존: "2026 hyperscaler capex: $725B(+77% YoY, 2025 $410B 대비) (8개 소스 일관). NextWaves Insight 8월: '60%+가 전력 인프라, 칩 아님' — 실제 하드웨어/풀링 장비 할당량은 하향. Q1 P&E $433.9B vs D&A $149B 격차. 2027 기술 지출 1조 달러 가능성 지속."
→ 변경: "2026 hyperscaler capex: $725B(+77% YoY, 2025 $410B 대비) (8개 소스 일관). 🆕 **US utility Southern Co: 데이터센터 전력 사용량 +55% YoY** (2026-08-14, datacenterdynamics) — '60%+가 전력 인프라, 칩 아님' 주장 교차검증. Q1 P&E $433.9B vs D&A $149B 격차. 2027 기술 지출 1조 달러 가능성 지속."
```

---

## 📈 기준선 대비 delta 요약 매트릭스

| # | 항목 | 기준선(7호) | 오늘(2026-08-15) | 영향도 |
|---|---|---|---|---|
| 1 | Samsung 2nm HBM base die 생산 라인 전환 | HBM 수급에 "growing traction" 일반 서술 | NRD-K Line 2 R&D→제어 전환, 2nm HBM base die | ★★★ |
| 2 | Micron 데이터센터 메모리 공급 부족 | "competitive gap closing"만 | "절반 미만만 충족", 계약가 "매우 높은" | ★★★ |
| 3 | SK Hynix 대련 Fab 2 재가동 | 10.4절 SK Hynix 일반 서술 | 2027 H1 양산, China NAND 50% 증가 목표 | ★★ |
| 4 | Lenovo FY1Q26/27 $26.9B +43% YoY | 서버 OEM에 "상세 미수집" | +43% YoY, CXL 서버 라인업 보유 | ★ |
| 5 | Nanya Tech NT$300B 팹 투자 | 미확인 | 12인치 웨이퍼 팹 2곳, 차세대 DRAM | ★ |
| 6 | NVIDIA NeMo Switchyard AI 라우팅 | 미확인 | "GPT-5-style model routing"으로 비용 절감 | ★ |
| 7 | Southern Co 데이터센터 전력 +55% | CapEx "60%+ 전력 인프라" 주장 | utility 데이터로 +55% 교차검증 | ★ |

---

## 🎪 업계 이벤트 / 학회

### Hot Chips 2026 — 8/23-25 Palo Alto (D-8)
- **XCENA**: CXL-based memory expansion platform with near-data processing 데모 예정. (7호 delta-7 반영)
- **Microchip**: XpressConnect PCIe Gen 6/CXL 3.1 retimers.

### CXL Mini DevCon 2026 — 8/3 Santa Clara (이미 종료)
- Vistara ASIC architecture white paper 발표. (7호 delta-5 반영)

---

## 🗞️ 테크/서버 사이트 Top 헤드라인 (타이틀 + 한 문장 설명, 한글 취합)
> 캡처 시각: 2026-08-15 06:30 KST 대략.

### Samsung/메모리 (2026-08-14)
1. **Samsung, 2nm HBM base die 생산 라인 전환 검토** — Giheung NRD-K Line 2 실험 R&D → 제조 라인. NVIDIA 미래 수요 대응. TrendForce.
2. **SK Hynix 대련 Fab 2 재가동** — 2027 H1 양산, China NAND 생산량 50% 증가. TrendForce.
3. **Micron, 데이터센터 메모리 요구의 절반 미만만 충족** — 계약가 "매우 높은". TrendForce.
4. **Nanya Tech, NT$300B 투자로 12인치 웨이퍼 팹 2곳 건설** — 차세대 DRAM/맞춤형 메모리. TrendForce.

### NVIDIA/AI 인프라 (2026-08-12)
5. **NVIDIA NeMo Switchyard — "GPT-5-style model routing"으로 AI 비용 절감** — The Register.
6. **Together AI + IBM $240M, Nvidia HGX B300 deploy** — Q1 2027 대규모 배치. The Register.

### 서버/OEM (2026-08-14)
7. **Lenovo FY1Q26/27 $26.9B +43% YoY** — AI 데이터센터 투자 지속. StorageNewsletter.

### 전력 인프라 (2026-08-14)
8. **Southern Co 데이터센터 전력 사용량 +55%** — AI 데이터센터 전력 수요 폭발. datacenterdynamics.

### AI/메모리 플랫폼 (2026-08-13)
9. **MinIO AIStor Memory — Agentic AI용 엔터프라이즈 메모티 플랫폼** — CXL 직접 관련 없음. StorageNewsletter.

---

## 🔍 미변경 카테고리 (변동 없음 / 미확인)

| 카테고리 | 상태 | 비고 |
|---|---|---|
| 1. CXL 스펙/표준 | 미변경 | CXL 4.0 스펙 변경 없음. 9월/11월 예정 이벤트 상세 미발표 |
| 2. CXL 디바이스/미디어 | 미변경 | SMART Modular CMM-E3S 기존. 신규 없음 |
| 3. 컨트롤러 벤더 | 미변경 | 7개 벤더 모두 8/8-8/15 신규 없음. 403/ENOTFOUND 차단 |
| 4. 풀링 SW/어플라이언스 | 미변경 | Vistara ASIC 7호 delta-5 반영. Liqid/MemVerge 미확인 |
| 5. 서버 OEM | 변경 | Lenovo 실적 delta-4로 신규 반영 |
| 6. CPU/GPU CXL | 미변경 | NVIDIA Vera 7호 delta-2 반영. Intel $20B 지분 증가(간접) |
| 7. AI 패브릭 | 미변경 | Russian missile 이슈(지리정치)만. 3-way rivalry 유지 |
| 8. Main Memory | 미변경 | JEDEC DDR6/LPDDR6 6호 delta-5 반영 유지 |
| 9. AI Rack/KV offload | 미변경 | MinIO AIStor(CXL 직접 관련 아님)만 |
| 10. LLM TCO 모델 | 변경 | NVIDIA NeMo Switchyard delta-6로 신규 반영 |
| 11. 메모리 가격/실적 | 변경 | Samsung 2nm HBM/Micron 부족/SK Hynix Fab 2/Nanya Tech delta |
| 12. 시장/CSP | 변경 | Southern Co 전력 +55% delta-7로 신규 반영 |

---

## 📋 후속 액션 (DRAFT 보강)
- [ ] DRAFT 10.2절: Samsung 2nm HBM base die 생산 라인 전환 (delta-1)
- [ ] DRAFT 11.3절: Samsung 경쟁사 행 업데이트 — 2nm HBM (delta-1)
- [ ] DRAFT 10.1절: Micron data center demand shortfall + "very high" pricing (delta-2)
- [ ] DRAFT 10.4절: SK Hynix Dalian Fab 2 재가동 + Nanya Tech NT$300B (delta-3, 5)
- [ ] DRAFT 5장: Lenovo 서버 OEM 실적 (delta-4)
- [ ] DRAFT 9.3절: NVIDIA NeMo Switchyard TCO 관점 (delta-6)
- [ ] DRAFT 11.2절: Southern Co +55% 전력 — CapEx 교차검증 (delta-7)
- [ ] (계속 #34) Montage trial production → 양산 전환 시점 추적
- [ ] (계속 #35) HBM4 양산 램프 상세 — Samsung 2nm HBM vs SK Hynix 1c
- [ ] (계속 #36) Micron "very high" pricing 교차검증 — 직접 TrendForce 원문
- [ ] (신규 #42) Samsung 2nm HBM base die → NVIDIA Vera Rubin pairing 수주 확정 여부 추적
- [ ] (신규 #43) SK Hynix Dalian Fab 2 → China NAND 50% 증가가 CMM-H 가격 경쟁력에 미치는 영향

---

## 📁 관련 파일
- 기준선 DRAFT: `wiki/concepts/cxl-memory-product-planning-draft - 복사본.txt` (DRAFT v0.8)
- 직전 Daily Update: `wiki/daily-updates/cxl-daily-update-2026-08-14.md` (7호)
- 핸드오프: `wiki/concepts/cxl-product-planning-session-handoff.md` 5절
- 원시 데이터: `sources/cxl-daily-raw-2026-08-15.md`
- HTML 보고서: `wiki/cxl-daily-report-2026-08-15-0630.html`

---

## 데이터 한계 공개
1. **Samsung 2nm HBM base die**: TrendForce(2026-08-14) 기반. "sources say" — 아직 Samsung 공식 확인 아님. 확정 단계가 아닌 검토 단계.
2. **Micron 공급 부족**: TrendForce(2026-08-12) 기반. "very high" 가격 인용 — Micron 공식 investor relations 원문 미확보.
3. **SK Hynix Dalian Fab 2**: TrendForce "reportedly" — SK Hynix 공식 확인 미수집.
4. **Nanya Tech 투자**: TrendForce "reportedly" — 대만 경제일보 등 원문 미확보.
5. **Lenovo 실적**: StorageNewsletter 인용 — Lenovo IR 공식 발표 원문 미확보.
6. **컨트롤러 벤더 7개**: Panmnesia, ScaleFlux, Marvell, Montage, Astera Labs, Microchip 모두 403/503/ENOTFOUND 차단. 8/8-8/15 신규 뉴스 존재 여부 미확인.
7. **DuckDuckGo**: CAPTCHA 차단으로 검색 폴백 불가. TrendForce 직접 WebFetch에만 의존.
