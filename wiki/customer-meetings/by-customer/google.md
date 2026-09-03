---
title: "Google — DRAM/MRDIMM Roadmap (customer)"
created: 2026-08-11
updated: 2026-08-11
tags: [dram, customer, google, mrdimm, rdimmb, ddr5, ddr6, prac, amd-venice, intel-dmr]
entity: Google
relation: customer
first_contact: 2026-02-05
meetings: 1
---

# Google — DRAM/MRDIMM Roadmap (customer)

> Google = CSP 주요 고객. 본 접촉 = **DRAM DIMM 로드맵** (RDIMM/MRDIMM/DDR5/DDR6) 중심, **CXL 아님**.
> 단일 출처(구병호 작성 2026-02-05), 외부 교차검증 미수행.

---

## 현재 관계 상태 (2026-02-05 기준)

- **단계**: DRAM 로드맵 정합 활성. Platform·HW Qual·SQE·GCM Sourcing 6명 + 자사 7명 다부문 접촉.
- **핵심 합의**: DDR5 PRAC 미지원 Google 수용 / Intel DMR 48→64GB 전환 / 1cnm 96GB NPI Intercept + ARM3 Sustain.
- **MRDIMM**: **AMD Venice = MRD 필수(POR)** / ARM4 = RDIMM 8800 백업(64/128GB) / **Gen3 = Default 요구** / LP MRDIMM은 AMD 지원 여부에 좌우.
- **DDR6**: 30년 64Gb 선호, buffer solution 요구, x6 Consolidation 반대(JEDEC).
- **시장**: 23% CAGR 수요 대비 28년 공급 한정. 48GB·7200Mbps = 시장 작아 권장 안 함.

---

## 핵심 팩트 (누적)

### DRAM / RDIMM
- **Intel DMR POR 48→64GB 변경 검토** (EVT 64GB 검증 후 최종). **(Confidential) Intel DMR GA @27년 1~2월**.
- **1cnm 96GB NPI/Sustain 인증 추진 동의** — ARM3 7200→8000 sustain, DMR 1cnm NPI Intercept 합의. 자사 1c 96GB 4개월 당김.
- 48GB RDIMM 양산 계획 없음(자사) → 64GB 전환 설득. Google 64/128GB EVT 지원.
- EMR/Ghostfish(Intel): 64GB 7200Mbps 샘플 필요 (현재 5600Mbps 운용).

### DDR5 PRAC ★
- **D5 16/24/32Gb Die 전부 PRAC 지원 없음** → Google 수용.
- 설득: 16/24Gb 불가 → 32Gb 의미 없음 Appeal → Consensus.
- **PRAC = Google 중요 산업보안 사항** → DDR6 등 미래 제품에서 지속 논의.
- 1cnm 32Gb = Bit per Wafer 관점 Efficient.

### MRDIMM ★★
- **AMD Venice = MRD 필수** (BW/Core, POR 유지, RDIMM 전환 시 System balance 붕괴).
- **AMD ARM4** = Value Proposition → RDIMM 8800 백업(64/128GB sweet-spot).
- **Gen3 = Google Default 요구** — 타 CSP Gen3 선택 시 경쟁력 위해 adoption. **AMD Florence Gen4 = Gen3 대비 Q2~3 느림** → AMD Gen4 지원 여부/시점 핵심.
- 동일 Platform Gen3→Gen4 트랜지션 선호, **256GB 지원 필요**.
- **LP MRDIMM**: AMD LPMRDIMM 지원 여부 핵심 → **자사가 Google에 AMD 설득 요청**.
- **메모리 Sole vendor 불가** (Google).
- 자사: MRDIMM Gen2 라인업 축소 중 → 경쟁사 "Gen2 없이 Gen3/Gen4 고려 안 함" 언급.

### DDR6 ★
- Google 30년 시점 **64Gb 선호**, 대용량 buffer solution 요구.
- 48Gb = 24Gb 같은 상황 회피 원함.
- **x6 Consolidation 반대** (2p3/2p6 각 장단점) → JEDEC Committee 공식 입장 예정.

### 간접 등장 (플랫폼)
- **AMD**: Venice(MR DIMM 필수, High Performance) / ARM4(Value Proposition, RDIMM 백업) / Florence(Gen4, Gen3 대비 Q2~3 느림). → [amd.md](amd.md)
- **Intel**: DMR(POR 48→64GB, GA 27년 1~2월) / EMR / Ghostfish Enabling. → [intel.md](intel.md)

### 참석자
- SK hynix: 강선국·주정수·권정환·김의현·방준혁·김찬희·이현민 (7명)
- Google: Brian Morris(Platform Architect)·Heidi Wei(HW Qual/PM)·Nejar Kumar(HW Qual)·Andy Kim(SQE/Quality)·Krishna Nidugala(GCM/Sourcing)·Jerry Lee(GCM/Sourcing) (6명)

---

## Follow-up Actions (대기)

- [ ] DMR 64GB EVT 검증 → 48→64GB 최종 확정
- [ ] 1cnm 96GB NPI Intercept + ARM3 Sustain — GCM Price Gap 합의
- [ ] 자사 현실적 MRD Line-up Google Propose
- [ ] **Google이 AMD LPMRDIMM 지원 설득** (자사 요청)
- [ ] DVT Venice CS샘플 자사 사전 확보
- [ ] ARM4 64GB@7200 pre-EVT 샘플 (2026-04)
- [ ] EMR/Ghostfish 64GB 7200Mbps 샘플
- [ ] DDR6 PRAC·64Gb·buffer solution 논의 지속
- [ ] JEDEC x6 Consolidation 후속

---

## 미팅 이력 (역순)

### ★ 2026-02-05 — Google DRAM/MRDIMM 미팅 ★★★ (최초, 말뭉치 내 최초 미팅 + 첫 비-CXL)

- **전문**: [meetings/2026-02-05-google-dram-mrdimm.md](../meetings/2026-02-05-google-dram-mrdimm.md)
- **참석**: SK hynix(강선국·주정수·권정환·김의현·방준혁·김찬희·이현민) / Google(Brian Morris-Platform Architect·Heidi Wei-HW Qual/PM·Nejar Kumar-HW Qual·Andy Kim-SQE/Quality·Krishna Nidugala-GCM/Sourcing·Jerry Lee-GCM/Sourcing)
- **핵심**: DRAM DIMM 로드맵 정합(비-CXL). Intel DMR 48→64GB(GA 27년 1~2월). 1cnm 96GB NPI Intercept. **DDR5 PRAC 미지원 Google 수용**(DDR6서 지속 논의). **AMD Venice MRD 필수** / ARM4 RDIMM 8800 백업. **MRD Gen3 = Default**(AMD Florence Gen4 Q2~3 느림). LP MRDIMM = AMD 지원 여부 좌우(자사, Google에 AMD 설득 요청). 메모리 Sole vendor 불가. DDR6 64Gb·buffer solution·x6 Consolidation 반대(JEDEC).
- **DRAFT 연결**: 7장 Main Memory(MRDIMM Gen2/Gen3/Gen4, DDR6, Density) · 5장 CPU/AMD Venice·ARM4·Florence · 11장 시장 인텔리전스(Google CSP DRAM) · 12장 상품기획(MRD Line-up, PRAC, DDR6).
