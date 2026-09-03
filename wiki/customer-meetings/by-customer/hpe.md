---
title: "HPE — 고객 미팅 누적 이력"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, by-customer, hpe, gen2, formfactor, pqc, venice]
entity: hpe
relation: customer
---

# HPE — 미팅 누적 이력

> **상대방별 누적 뷰** — HPE가 등장한 모든 미팅의 요약 + 현재 관계 상태.
> 미팅별 전문은 `../meetings/` (날짜키).
> CXL DRAFT 연결: 폼팩터(AIC→E3.S 진화) / Gen2 컨트롤러(Montage) / 유럽 PQC / DDR6

---

## 현재 관계 상태 (최신 미팅 기준)

- **관계**: 고객 (CXL Gen2 논의, 2026-05-07)
- **단계**: Gen2 샘플 align 진행 중 — X8 backplane 대기 → X4에서 자사 sample test → 2027-06 Venice Launch 목표
- **핵심**: HPE는 AIC에 controller 탑재(DIMM socket/Solder down) 시 1TB급 확장 유연성 inform. Serviceability 고려 시 E3.S 더 확장 전망. 유럽 Dec'27 PQC 규정 → 자사 PQC FU 필수(미해결).
- **★ 시계열 기원 (02-12 → 05-07)**: HPE CXL 접촉의 기원 = 02-12. EVB 8pcs(2025-12 제공) CXL 2.0 평가(문제 없음) → CXL 3.0 계획 + Gen13 Venice **Post-Launch**. 05-07에 Gen2 컨트롤러=Montage + 2027-06 Venice Launch로 구체화. 02-12 "CXL Post-Launch(지연)" ↔ 05-07 "2027-06 Launch" 교차. 자사 2월 sample = 02-12 미팅 직후 제공 추정.

## 핵심 팩트 (누적)
- **메모리 Shortage = CXL 도입 가속 촉매**: Shortage가 오히려 채택 앞당김. 고객 메모리 Reuse 목적 AIC 채택 문의 지속 → 초기 Acceptance 역할.
- **FF 진화 경로 (김의현 TL, 05-07)**: AIC(초기, Serviceability 열세) → 고객 Training 후 개선 FF로 자연 이동. 장기 AIC+E3.S 필요, **E3.S가 주(main)** 전망.
- **512GB 확보 (05-07)**: E3.S 한계 → E3.L 필요 시 Back-plane Longer 고려.
- **DDR6 (05-07)**: 지금부터 논의 필요 (타이밍 중요).
- **HPE 제안 (05-07)**: AIC + controller → DIMM socket / Solder down → 1TB급 확장 유연.
- **Gen2 CXL 컨트롤러 (05-07)**: Third party = **Montage** 재확인.
- **Gen2 샘플 일정 (05-07)**: X8 backplane 대기(next couple months) → X4에서 자사 sample test → **2027-06 Launch**(Venice SP7/SP8). 자사 2월 sample acceptable.
- **유럽 PQC (05-07)**: Dec'27 규정 변경 → 자사 PQC FU 필수 → status 확인 후 HPE inform (미해결).
- **★ EVB 8pcs (02-12)**: 2025-12 HPE 제공. 이전 platform CXL 2.0 테스트, **초기 평가 문제 없음** → 곧 **CXL 3.0 평가 계획**. HPE CXL 접촉의 물리적 기원.
- **★ Gen13 Venice Post-Launch (02-12)**: CXL 적용 = **Post-Launch**(= Venice Launch 후). 샘플 일정 = Venice RDIMM과 **불일치 가능**(CXL 지연).
- **★ MRDIMM + CXL 조합 (02-12)**: CXL = Capacity 확장용. IMDB 응용 NVMe 대비 성능 우수 + 용량 확장. AI 응용 NVMe→CXL 대체 가능. **Memory sharing** = 특정 workload 강점.
- **★ CMM 고용량 + x4 모드 (02-12)**: IMDB 고객 Main:CXL = **1:1 용량** 원함. E3.S slot + PCIe lane 제약 → **CMM 고용량 + x4 모드** = NVMe backplane 호환 + 유연 구성. CMM(AIC)이 E3.S 제약 우회 경로.
- **★ HMSDK (02-12)**: **4-port sub-port interleaving**(P0-P3, 내부 평가는 2 port 단 4 port 가능 설명). **Linux 동작**.

## 후속 액션 / 미해결
- [ ] **자사 PQC FU status 확인 → HPE inform** (Dec'27 유럽 규정, 시급)
- [ ] DDR6 논의 착수 (지금부터)
- [ ] Gen2 X8 backplane 도착 후 X4 자사 sample test
- [ ] 2027-06 Venice SP7/SP8 Launch 준비
- [ ] 512GB 확보 E3.L / Back-plane Longer 검토
- [ ] AIC → E3.S 전환 trigger / Training 시점 상세화
- [ ] **EVB CXL 3.0 평가 결과** 확인 (02-12 계획 → 05-07 시점 결과?)
- [ ] Gen13 Post-Launch 개발·샘플 일정 확인
- [ ] **MRDIMM + CXL 조합** "두 마리 토끼"(성능+용량) 제안
- [ ] HPE 참석자 공식 회의록 확보 후 update (02-12 미완)

## 미팅 이력 (역시간순)

### 2026-05-07 — HPE CXL Gen2 미팅
- **참석**: 김의현 TL(ETHAN KIM, 자사 DRAM Enterprise Engineering) // HPE(명 미기재)
- 메모리 Shortage→CXL 가속, AIC Acceptance→FF 진화(E3.S 주), HPE AIC+controller 1TB 제안, Gen2 컨트롤러=Montage, 2027-06 Venice Launch, 유럽 Dec'27 PQC FU 필수.
- 전문: [../meetings/2026-05-07-hpe-cxl-gen2.md](../meetings/2026-05-07-hpe-cxl-gen2.md)
- ★ (DRAFT 폼팩터·Gen2·PQC 챕터 반영 대기)

### 2026-02-12 — HPE CXL EVB / Gen13 Venice 미팅 (HPE 최초 CXL 접촉)
- **참석**: 심응보 팀장 / 구병호 TL / 이상돈 TL(자사) // Pope Eric(Advanced Technology) / Benedict Malvin / Bryan Lee(HPE, 공식 회의록 확보 후 update 예정)
- **HPE 최초 CXL 접촉**. EVB 8pcs(2025-12 제공) CXL 2.0 평가(문제 없음) → CXL 3.0 계획. Gen13 Venice = **Post-Launch**(샘플 RDIMM과 불일치 가능). MRDIMM+CXL 조합(IMDB NVMe 대비 성능+용량, AI NVMe→CXL 대체, Memory sharing 강점). IMDB 고객 1:1 용량 + E3.S slot/PCIe lane 제약 → **CMM 고용량 + x4 모드**(NVMe backplane 호환). HMSDK 4-port sub-port interleaving, Linux.
- Action: EVB CXL 3.0 평가 결과 / Gen13 Post-Launch 일정 / MRDIMM+CXL 두 마리 토끼 제안.
- 전문: [../meetings/2026-02-12-hpe-cxl-evb.md](../meetings/2026-02-12-hpe-cxl-evb.md)
- ★★ (DRAFT 폼팩터·Gen2·CMM·HMSDK 챕터 반영 대기, HPE 기원)
