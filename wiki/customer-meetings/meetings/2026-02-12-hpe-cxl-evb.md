# HPE — CXL EVB / Gen13 Venice 미팅 (2026-02-12)

> **Source**: [sources/hpe-cxl-evb-meeting-2026-02-12.md](../../../sources/hpe-cxl-evb-meeting-2026-02-12.md) (불변 원문)
> **작성자**: 구병호(KOO BYEONG HO) DRAM Solution (last updated 2026-02-25)
> **날짜**: 2026-02-12
> **자사 참석자**: 심응보 팀장, 구병호 TL, 이상돈 TL
> **HPE 참석자**: Pope Eric (Advanced Technology), Benedict Malvin, Bryan Lee (+ 공식 회의록 확보 후 update 예정)
> **관계**: HPE = customer
> **성격**: EVB(8pcs, 2025-12 제공) CXL 2.0 테스트 현황 + Gen13 Venice Post-Launch CXL 적용 + MRDIMM+CXL 조합 + HMSDK 소개 — **2026-05-07 HPE Gen2 미팅의 전신 (EVB→Launch 일정의 기원)**

---

## 핵심 요약

| # | 주제 | 결론 / 핵심 팩트 |
|---|------|------------------|
| 1 | EVB 8pcs 현황 | 작년 12월 HPE 제공, 이전 platform CXL 2.0 테스트, **초기 평가 문제 없음**, 곧 **CXL 3.0 평가 계획** |
| 2 | Gen13 Venice CXL | **Post-Launch**로 진행 예정. 샘플 일정 = Venice RDIMM과 일치하지 않을 수 있음 |
| 3 | MRDIMM + CXL 조합 | CXL = Capacity 확장용. IMDB 응용 NVMe 대비 성능 우수 + 용량 확장 benefit |
| 4 | AI 응용 + Memory sharing | NVMe→CXL 대체 가능. **Memory sharing** = 특정 workload 강점 |
| 5 | IMDB 1:1 용량 + CMM | IMDB 고객 Main:CXL = 1:1 원함. **E3.S slot 수 + PCIe lane 제약** → **CMM 고용량 + x4 모드**(NVMe backplane 호환, 유연 구성) |
| 6 | HMSDK — 4-port interleaving | PCIe 4 device P0-P3 interleaving 질의 → 내부 평가 2 port, 단 **4 port sub-port interleaving 가능** 설명 |
| 7 | HMSDK — OS | **Linux 동작** 설명 |
| 8 | Action | EVB CXL 3.0 평가 결과 / Gen13 Post-Launch 개발·샘플 일정 / MRDIMM+CXL 성능+용량 "두 마리 토끼" 조합 제안 |

---

## 상세 정리

### 1. EVB 8pcs — CXL 2.0 → 3.0 평가
- 작년 12월(2025-12) HPE에 **EVB 8pcs 제공**
- 이전 platform 상에서 **CXL 2.0 테스트** 진행
- **초기 평가 문제 없음**
- 곧 **CXL 3.0 평가** 계획 중

### 2. Gen13 Venice — Post-Launch CXL 적용
- HPE **Gen13 server (Venice)** 에 CXL 적용 = **Post-Launch** 진행 예정
- 샘플 일정 = **Venice 향 RDIMM과 일치하지 않을 수 있음** (CXL이 RDIMM보다 지연 가능)
- = 05-07 미팅 "2027-06 Venice Launch"의 전신 맥락 — 단, 본 02-12에선 CXL이 Post-Launch(= Venice Launch 후)로 명시. 05-07 "자사 2월 sample acceptable"과 02-12 "샘플 일정 RDIMM과 불일치 가능" 교차.

### 3. MRDIMM + CXL 모듈 조합
- CXL = **Capacity 확장용**
- **IMDB(In-Memory DB) 응용**: NVMe 대비 CXL 성능 우수 + 용량 확장 benefit
- **AI 응용**: NVMe→CXL 대체 가능. **Memory sharing 기능** = 특정 workload 강점

### 4. IMDB 고객 요구 + CMM (핵심)
- IMDB 운영 고객 = **Main Memory : CXL memory = 1:1 용량** 사용 원함
- 단, **E3.S slot 수 + PCIe lane 수 제약**
- → **CMM 고용량 필요** + **x4 모드 지원** → **NVMe backplane 호환성** + 유연한 구성 가능 (의견 확인)
- = CMM(AIC 고용량)이 E3.S slot/PCIe lane 제약을 우회하는 경로

### 5. HMSDK 소개
1. **4-port sub-port interleaving**: PCIe에 4 device 결합 시 P0·P1·P2·P3 같이 interleaving 동작? → 내부 평가는 2 port, 단 **4 port sub-port interleaving 가능** 설명
2. **OS**: **Linux 동작** 설명

### Action Items
- EVB CXL 3.0 평가 결과 확인
- Gen13 Post-Launch 개발 일정 + 샘플 제공 일정 확인
- **MRDIMM + CXL 조합 = 성능 + 용량 "두 마리 토끼" 잡는 조합 제안**

---

## 후속 액션 / 미해결

- [ ] **EVB CXL 3.0 평가 결과** 확인 (02-12에서 계획 → 05-07 시점 결과?)
- [ ] Gen13 Post-Launch 개발 일정 + 샘플 일정 확인 (→ 05-07 "2027-06 Venice Launch")
- [ ] **MRDIMM + CXL 조합** "두 마리 토끼"(성능+용량) 제안
- [ ] HPE 참석자 공식 회의록 확보 후 update (02-12 시점 미완)
- [ ] IMDB 고객 1:1 용량 요구 + E3.S/PCIe lane 제약 → CMM 고용량+x4 모드 제안 구체화

## 관련 — HPE 시계열 (★ 핵심 인사이트)

> **본 02-12 미팅은 HPE CXL 접촉의 기원.** EVB 8pcs(2025-12 제공) → 02-12 CXL 2.0 평가/3.0 계획 + Gen13 Venice Post-Launch → 05-07 Gen2 컨트롤러=Montage, 2027-06 Venice Launch, 자사 2월 sample acceptable.

- **2026-02-12 (본 미팅)**: EVB 8pcs CXL 2.0 평가(문제 없음) → CXL 3.0 계획. Gen13 Venice = **Post-Launch**. MRDIMM+CXL 조합. CMM 고용량+x4 모드(NVMe backplane 호환). HMSDK 4-port sub-port interleaving, Linux.
- 2026-05-07 HPE: [2026-05-07-hpe-cxl-gen2.md](2026-05-07-hpe-cxl-gen2.md) — Gen2 컨트롤러=Montage, **2027-06 Venice(SP7/SP8) Launch**, 자사 2월 sample acceptable, AIC Acceptance→E3.S 주, 유럽 PQC FU.
  - **★ Venice 일정 교차**: 02-12 "CXL = Post-Launch(= Venice Launch 후)" ↔ 05-07 "2027-06 Venice Launch, 자사 2월 sample acceptable". 02-12의 CXL 지연(Post-Launch)이 05-07에서 Launch 일정(2027-06)으로 구체화. 자사 2월 sample = 본 02-12 미팅 직후 제공?
- by-customer: [hpe.md](../by-customer/hpe.md)

## 관련 — 폼팩터 thread 교차

- 02-12 본: **E3.S slot + PCIe lane 제약** → CMM 고용량 + x4 모드(NVMe backplane 호환). E3.S 제약 명시.
- 03-12 FMTA: Liquid Cooling엔 E1.S 적합, E3.S 큼.
- 05-07 HPE: AIC Acceptance → E3.S 주(main).
- 03-11 Oracle: AIC 너무 큼 + Liquid 불가.
- → E3.S는 slot/PCIe lane 제약(02-12) + 크기(03-12) + serviceability 우세(05-07) 양면. CMM(AIC)은 E3.S 제약 우회 경로(02-12).
