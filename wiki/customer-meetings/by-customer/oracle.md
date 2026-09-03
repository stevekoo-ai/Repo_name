---
title: "Oracle — 고객·파트너 미팅 누적 이력"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, by-customer, oracle]
entity: oracle
relation: customer
---

# Oracle — 미팅 누적 이력

> **상대방별 누적 뷰** — Oracle이 등장한 모든 미팅의 요약 + 현재 관계 상태.
> 미팅별 전문은 `../meetings/` (날짜키).
> CXL DRAFT 연결: 11장 시장 인텔리전스 / 3장 컨트롤러 (AIC PNM POC)

---

## 현재 관계 상태 (최신 미팅 기준)

- **관계**: 고객 (CXL 평가 프로젝트 재개, 2026-08-11)
- **단계**: POC 진행 중 — AIC 기반 PNM 샘플 전달 대기
- **핵심 변화**: Sang Park AWS→Oracle 이직으로 AIC 폼팩터 검토 포함, CXL 평가 재시작
- **우선순위**: Pooled 관심 유지하나 **NVIDIA/AMD GPU Rack Reference Design 협업 우선**이 핵심
- **★ 시계열 발전 (03-11 → 08-11)**: 03-11 "AIC 너무 큼 + liquid 불가 + SPOF 감당 불가 → HA 필수" → 08-11 "AIC PNM 검토 재개 (Sang Park 이직 계기)". AIC 거부(03-11)가 Sang Park 이직으로 재검토(08-11)로 반전. Jay(JEBA SUNDRARAJ)는 양쪽 미팅 공통 참석 — 일관된 담당자.

## 핵심 팩트 (누적)
- 기존 E3 폼팩터 선호(서버 형상) → AIC 폼팩터 검토 포함(이직 계기).
- 자사 POC **AIC 기반 PNM**이 Marvell 칩·폼팩터 크기 요건 충족 → 샘플 확보 시 전달.
- Oracle = SW 업체 → PNM Acceleration 기능 활용 자신.
- Marvell GM top-down 지원.
- **Pooling(03-11)**: Switch 기반 pooling → Xconn 일정 slow down. **TCO 최우선**(DIMM 수준 Cost 요구). 주 목적 = **Stranded memory 해결**(AI 아님, GP/Cloud service). **최소 4대 서버** ↔ CXL memory box.
- **HA 요구(03-11)**: **SPOF 감당 불가** → 풀링 시작하려면 HA 필수. Switch = SPOF. → **Switchless/Montage MHD 경로** 검토 (2포트→2호스트→SPOF 제거).
- **Local 부정(03-11)**: DB 팀 tiered memory → **TCO 이점 없음 + DIMM ch 확장이 나음 → 계획 중단**. **AMD 12→16ch** → CXL 추가 가치 없어짐.
- **OCI 채택 조건(03-11)**: DIMM보다 저렴 / latency는 싸면 감수 / **VM용(GPU/AI 추론 아님)**.
- **Switch 경쟁 구도(03-11)**: Marvell(Broadcom 경쟁 위해 switch 인수) vs Broadcom("CXL switch 시장 없다") vs Xconn(Marvell 인수 대상, 협의 중단 → 4월 재논의).

## 후속 액션 / 미해결
- [ ] AIC 기반 PNM 샘플 전달
- [ ] 차주 후속 미팅 결과
- [ ] **6월(late Q2) Oracle sync-up** 결과 — 03-11에서 예정됐던 follow-up. 08-11 POC 진행과 연결 확인 필요.
- [ ] **Montage MHD 상세** — 8CH or 2CH, "true solution" 의미 (Jay가 몰라 Montage 직접 문의 필요) → [montage.md](montage.md) 교차
- [ ] Oracle HA 요구 vs 자사 2세대 CMM 2포트(MHD) 매핑 — SPOF 제거 경로 구체화

## 미팅 이력 (역시간순)

### 2026-08-11 — CXL 메모리 풀링 미팅
- **참석**: Jay(Sr. HW PE) [= JEBA SUNDRARAJ, 03-11과 동일인]
- Sang Park AWS→Oracle 이직 → AIC 폼패터 검토, CXL 평가 재개.
- AIC PNM Marvell 칩·폼팩터 충족 → 샘플 전달 합의. 차주 후속. Marvell GM top-down 지원.
- Pooled 관심 유지, NVIDIA/AMD GPU Rack RD 협업 우선 공감.
- 전문: [../meetings/2026-08-11-cxl-pooling.md](../meetings/2026-08-11-cxl-pooling.md) §고객 2) Oracle
- ★★ (DRAFT 11장/3장 반영 대기)

### 2026-03-11 — Oracle OCI CXL Pooling 미팅 (Santa Clara F2F, Oracle 최초 CXL 접촉)
- **참석**: SANTOSH KUMAR / SEUNGJU HAN / Donghyeok Park(자사) // JEBA SUNDRARAJ(Jay, Sr. Principal HW PE) / Somu Krishnasamy(NPI HW Engineer, Oracle)
- **Oracle 최초 CXL 접촉**. Switch 기반 pooling OCI VM 준비, Xconn 일정 slow down. TCO 최우선(DIMM 수준). AIC 너무 큼. Liquid 불가. **SPOF 감당 불가 → HA 필수** → Switchless/Montage MHD 검토(초기). 최소 4서버 풀. Stranded memory 해결(목적). Local DB tiered → TCO 무의미 + AMD 12→16ch → 계획 중단. 4월 Xconn/Marvell 재논의, 6월 sync-up.
- Switch 경쟁: Marvell(Broadcom 경쟁, switch 인수) / Broadcom("CXL switch 시장 없다") / Xconn(인수 대상).
- Q2 미해결: Montage MHD = 8CH or 2CH, "true solution" 의미 (Jay 모름 → Montage 직접 문의).
- 전문: [../meetings/2026-03-11-oracle-oci-cxl.md](../meetings/2026-03-11-oracle-oci-cxl.md)
- ★★★ (DRAFT 11장 시장 — TCO/HA/Stranded memory/switch 경쟁 반영 대기, 핵심)
