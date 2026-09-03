---
title: "Google DRAM/MRDIMM 미팅 — 2026-02-05"
date: 2026-02-05
created: 2026-08-11
updated: 2026-08-11
tags: [dram, customer-meeting, google, mrdimm, rdimmb, ddr5, ddr6, prac, amd-venice, amd-arm4, amd-florence, intel-dmr, intel-emr, lp-mrdimm]
attendees:
  sk_hynix: ["강선국", "주정수", "권정환", "김의현", "방준혁", "김찬희", "이현민"]
  google: ["Brian Morris (Platform Architect)", "Heidi Wei (HW Qual, PM)", "Nejar Kumar (HW Qual)", "Andy Kim (SQE, Quality)", "Krishna Nidugala (GCM, Sourcing)", "Jerry Lee (GCM, Sourcing)"]
source: sources/google-dram-mrdimm-meeting-2026-02-05.md
relation: customer
significance: "★★★"
---

# Google DRAM/MRDIMM 미팅 — 2026-02-05

> **현재 말뭉치 내 최초 미팅** (2026-02-05, IBM 02-06보다 하루 앞선).
> **첫 비-CXL 미팅** — DRAM DIMM 로드맵(RDIMM/MRDIMM/DDR5 PRAC/DDR6) 중심.
> Google Platform·HW Qual·SQE·GCM Sourcing 6명 + 자사 7명 다부문. 단일 출처(구병호 작성), 외부 교차검증 미수행.

---

## 0. 핵심 요약 (8개)

| # | 핵심 | 영향도 |
|---|------|--------|
| 1 | **Intel DMR POR 48→64GB 변경 검토** (EVT 64GB 검증 후 최종). **(Confidential) Intel DMR GA @27년 1~2월 계획** | ★★★ |
| 2 | **1cnm 96GB NPI/Sustain 인증 추진 동의** — ARM3 7200→8000 sustain, DMR 1cnm NPI Intercept 합의 | ★★★ |
| 3 | **DDR5 PRAC 지원 없음** (D5 16/24/32Gb Die 전부) — Google 수용. 단 PRAC = Google 중요 산업보안 사항 → **DDR6 등 미래 제품에서 지속 논의** | ★★★ |
| 4 | **AMD Venice = MRDIMM 필수** (BW/Core count 활용, MRD POR 유지, RDIMM 전환 시 System balance 붕괴). ARM4 = Value Proposition → RDIMM 8800 백업 플랜 가능(64/128GB) | ★★★ |
| 5 | **MRDIMM Gen3 = Google Default 요구** — 타 CSP가 Gen3 선택 시 경쟁력 위해 Gen3 adoption 필요. **AMD Florence Gen4 지원이 Gen3 대비 Q2~3 느림** → AMD Gen4 지원 여부/시점이 핵심 | ★★ |
| 6 | **LP MRDIMM** — AMD LPMRDIMM 지원 여부가 핵심, **자사가 Google에 AMD 설득 요청**. 메모리 **Sole vendor 불가** 입장. 256GB 지원 필요 | ★★ |
| 7 | **MRDIMM Gen2 라인업 축소 중** (자사) — 경쟁사 합리적 가격 제시, "Gen2 없이 Gen3/Gen4 고려 안 함" 언급. 단 Google은 Gen2 여전히 POR (Venice) | ★★ |
| 8 | **DDR6**: Google 30년 시점 64Gb 선호, 대용량 buffer solution 요구. **x6 Consolidation 반대**(2p3/2p6 각 장단점) → JEDEC 공식 입장 예정 | ★★ |

---

## 1. 배경 — Google DRAM Roadmap 정합

- Google = CSP 주요 고객. 본 미팅 = **DRAM DIMM 로드맵** (RDIMM/MRDIMM/DDR5/DDR6) 정합, **CXL 아님**.
- 자사 7명(강선국·주정수·권정환·김의현·방준혁·김찬희·이현민) vs Google 6명(Brian Morris-Platform Architect·Heidi Wei-HW Qual/PM·Nejar Kumar-HW Qual·Andy Kim-SQE/Quality·Krishna Nidugala-GCM/Sourcing·Jerry Lee-GCM/Sourcing).
- 시장: **23% CAGR 수요 대비 28년까지 공급 한정적**. 특히 48GB·7200Mbps = 시장 작아 Supportability 측면 다른 제품군 권장.

---

## 2. RDIMM / Intel DMR ★★★

- **Intel DMR POR 48GB → 64GB 변경 검토** — EVT 시 64GB 평가 검증 후 최종 변경.
- **1cnm 96GB NPI/Sustain 인증 추진 동의**:
  - ARM3 = 7200 → 8000 sustain 인증
  - DMR = 1cnm로 NPI Intercept 방안 수립 합의
- **(Confidential) Intel DMR GA @27년 1~2월 계획 중** — 자사 1c 96GB 4개월 당겨 DMR NPI Intercept + ARM3 Sustain Qual 제안 → 기술팀 "문제 없음". GCM팀 추가 논의 필요 (ARM3 7200Mbps 대비 Price Gap 합의).
- 자사 입장: **48GB RDIMM 양산 계획 없음** (공급 제약) → 64GB 전환 설득. Google 64GB·128GB EVT 지원 계획.

---

## 3. DDR5 PRAC — 지원 없음 합의 ★★★

- **향후 개발되는 모든 D5 16/24/32Gb Die PRAC 지원 없음** 공유 → **Google 수용**.
- 설득 경로: PRAC 미지원 R/M 발표 → 16/24Gb 지원 불가 → 32Gb 지원 의미 없음 Appeal → **비교적 쉽게 Consensus**.
- **단, PRAC = Google에게 중요한 산업보안 사항** → **미래 제품(DDR6 등)에서 지속 논의 요청**.
- 1cnm부터 32Gb = Bit per Wafer 관점에서 Efficient.
- SOC Validation Window 닫힐 경우 1cnm 전환 위해 양사 협업 합의 → Google이 AVL 필수인지 먼저 확인 예정.

---

## 4. MRDIMM Gen2 — Venice 필수 vs ARM4 백업 ★★★

| 플랫폼 | 포지션 | MRDIMM/RDIMM | Density |
|--------|--------|--------------|---------|
| **AMD Venice** | High Performance | **MRDIMM 필수** (BW/Core, POR 유지) | — |
| **AMD ARM4** | Value Proposition | RDIMM 8800 백업 플랜 가능 | 64/128GB 유지 |

- **Venice**: Google "MRD 필수적, RDIMM 전환 시 System 성능 Balance 깨짐" 강조. EVT 빌드 진행 중, **DVT CS샘플 곧 PO 발행 → 자사 사전 확보 요구**.
- **ARM4**: 64GB@7200Mbps 샘플 2026-04 pre-EVT 요청. MRD 프리미엄 과도 시 RD 전환 의향. 64/128GB = sweet-spot.
- 자사: MRDIMM Gen2 라인업 점차 축소 전달, RDIMM 전환 문의 → Google "MRD 여전히 POR, RD는 백업" 재차 강조.
- **경쟁사**: MRDIMM 합리적 가격 제시, "Gen2 없이 Gen3/Gen4 고려 안 함" 언급 → 자사 Gen2 축소 전략의 시험대.

---

## 5. MRDIMM Gen3 vs LP MRDIMM ★★

- **Gen3 = Google Default 요구** — CSP 경쟁사 일정경쟁 뒤쳐지면 안 됨. Consolidation 원할 경우 **Gen3 Solution과 동일 시기**.
- **AMD Florence의 Gen4 지원이 Gen3 대비 Q2~3 느림** → 타 CSP가 Gen3 선택 시 Google도 Gen3 adoption 필요. **AMD Gen4 지원 여부/시점 = 핵심**.
- 동일 Platform에서 **Gen3 → Gen4 트랜지션 선호**. AMD Core count 증가 고려 시 **256GB 지원 필요**.
- **LP MRDIMM**: AMD LPMRDIMM 지원 여부가 핵심 → **자사가 Google에 AMD 설득 요청**.
- **메모리 Sole vendor 불가** 입장 (Google).

---

## 6. EMR / Ghostfish (Intel)

- **Ghostfish(Intel) Enabling** 위해 64GB 7200Mbps 샘플 지원 필요.
- 현재 Google 해당 DIMM 5600Mbps 속도로 운용 중.

---

## 7. DDR6 장기 로드맵 ★★

- Google: **30년 시점 64Gb 있을 것 선호**. 없더라도 **대용량 해결 buffer solution 필요** 요구.
- **48Gb는 24Gb와 같은 상황 벌어지지 않기 원함** (48GB 공급 제약 반복 회피).
- **x6 Consolidation 반대** — 기존 2p3/2p6 각 Configuration이 장단점. 내부 리뷰 후 **JEDEC Committee에서 공식 입장 제시 예정**.
- LP 16Gb = Long Lifetime 가능, 32Gb = 시황에 따라 다름.

---

## 8. Action / Follow-up

- [ ] DMR 64GB EVT 검증 → 최종 48→64GB 변경 확정
- [ ] 1cnm 96GB NPI Intercept + ARM3 Sustain Qual — Google GCM팀 Price Gap 합의
- [ ] 자사 현실적 MRD Line-up Google Propose (Supportability·Price 감안)
- [ ] **Google이 AMD LPMRDIMM 지원 설득** (자사 요청)
- [ ] DVT Venice CS샘플 자사 사전 확보 (PO 발행 임박)
- [ ] ARM4 64GB@7200 pre-EVT 샘플 (2026-04)
- [ ] EMR/Ghostfish 64GB 7200Mbps 샘플 지원
- [ ] DDR6 PRAC·64Gb·buffer solution 논의 지속
- [ ] JEDEC x6 Consolidation Google 공식 입장 후속

---

## Related

- 상대방별 누적: [by-customer/google.md](../by-customer/google.md)
- 간접 등장: [by-customer/amd.md](../by-customer/amd.md) (Venice/ARM4/Florence platforms), [by-customer/intel.md](../by-customer/intel.md) (DMR/EMR/Ghostfish)
- MRDIMM thread (Google 02-05 비-CXL + HPE 02-12 MRDIMM+CXL): [index.md §3](../index.md)
- AMD Venice platform thread (Google 02-05 DRAM + HPE 02-12 "Gen13 Venice" CXL): [index.md §3](../index.md)
- 시계열: 본 미팅(02-05) → IBM 02-06(하루 후) → AWS 02-10 → HPE 02-12(Venice CXL 교차)

---

## Timeline 교차 (현재까지 최초 미팅)

| 날짜 | 미팅 | 본 미팅과의 관계 |
|------|------|------------------|
| **2026-02-05** | **Google DRAM/MRDIMM (본 미팅)** | **말뭉치 최초 + 첫 비-CXL(DRAM) 미팅**. AMD Venice MRDIMM 필수, Intel DMR, DDR5 PRAC, DDR6 |
| 2026-02-06 | IBM Power Future | 하루 후 (CXL) |
| 2026-02-10 | AWS KV Cache | 5일 후 (CXL) |
| 2026-02-12 | HPE EVB / Gen13 Venice | 7일 후 — **AMD Venice platform 교차** (Google 02-05 MRDIMM 필수 ↔ HPE 02-12 Gen13 Venice CXL Post-Launch) |
