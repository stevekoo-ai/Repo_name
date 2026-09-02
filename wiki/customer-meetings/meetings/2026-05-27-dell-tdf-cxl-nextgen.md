# DELL TDF — CXL Next Gen 스펙 미팅 (2026-05-27)

> **Source**: [sources/dell-tdf-cxl-nextgen-meeting-2026-05-27.md](../../../sources/dell-tdf-cxl-nextgen-meeting-2026-05-27.md) (불변 원문)
> **작성자**: 구병호(KOO BYEONG HO) DRAM Solution
> **날짜**: 2026-05-27
> **자사 참석자**: 심응보 팀장님, 구병호 TL, Jerry Shim (SK hynix)
> **상대방 참석자**: Stuart Berke, Raju Mishra (Dell)
> **관계**: Dell = customer · Marvell = partner (CMM AX co-working) · Xcena = partner (CMM AX co-working)
> **후속**: 별도 Tech. meeting 요청됨, 후속 meeting setup 예정

---

## 핵심 요약

| # | 주제 | 결론 / 핵심 팩트 |
|---|------|------------------|
| 1 | CMM AX 컨트롤러 | Marvell + Xcena와 공동개발, "Structure A" 구조, Evaluation Card 개발 중 |
| 2 | 폼팩터 전략 | 3세대 CXL은 AIC 또는 E3 **둘 중 하나** 택일 — 내부 논의 중 |
| 3 | 써멀 | E3(EDSFF)는 전면 배치→ AIC보다 열적 우세. 단, 풀링 시스템에서는 AIC도 전면 배치 가능 → 열적 역전 가능성 |
| 4 | E3 Long | 최대 1.5TB vs AIC FHHL 2TB(최대 3TB 확장) → 용량은 AIC 우세 |
| 5 | 섀시 공간 | E3 = 2U stack 가능, AIC = 3U/4U 필요. Dell 17G FHHL은 Riser cards 사용 |
| 6 | RAS | AIC 2TB 고용량 fail 리스크 → SK hynix SDDC+급 ECC, LPDDR6 카빙아웃 패리티, Die 내부 패리티 디바이스로 대응 |
| 7 | Dell 폼팩터 입장 | PowerEdge는 현재 AIC align. 단, 수십~수백 TB AI 풀링 = 전용 최적화 섀시 원점 재설계 의향 |
| 8 | 레퍼런스 디자인 | 현재 없음. Switchless Multi Head FPGA 프로토타입(실리콘 아님). AI 풀링 적정 용량 미확정 |

---

## AIC vs E3 트레이드오프 (본 미팅 도출)

| 항목 | AIC FHHL | E3.L / E3.S |
|------|----------|-------------|
| 단일 모듈 용량 | 2TB (Die당 최대 3TB) | 1.0~1.5TB |
| 배치 위치 | 후면(일반 서버) / 전면(풀링 시스템) | 전면 (EDSFF) |
| 써멀 | 일반 서버 후면→ 열악. 풀링 전면→ 역전 가능 | 전면 배치→ 열적 우세 |
| 섀시 높이 | 3U / 4U | 2U (stack 가능) |
| TCO | 고용량→ TCO 우세 | 용량 한계→ TCO 열세 |
| 유지보수 / Serviceability | 데이터 마이그레이션 솔루션 부재 | Hot-plug + 기계적 swapping 우수, granularity 장점 |
| 신뢰성(RAS) | 2TB 고용량 fail 리스크 → SDDC+ ECC / 패리티 강화 필요 | 모듈 수 2배 → fail 영향 국소화 유리 |

---

## 8개 Q&A 상세

### 1. CMM AX 컨트롤러 개발 방식 및 협력사
- **Q (Raju Mishra)**: CMM AX는 자체 컨트롤러인가, 파트너십인가?
- **A (Jerry Shim)**: Marvell + Xcena와 Co-working 중. "Structure A" 구조로 Evaluation Card 개발 중.

### 2. 향후 폼팩터 출시 계획 (AIC vs E3)
- **Q**: E3와 AIC 둘 다 진행할 계획인가?
- **A**: 3세대 CXL 제품은 **둘 중 하나**를 택해야 한다고 판단. 내부 논의 중.

### 3. 발열(Thermal) 영향
- **Q (Stuart Berke)**: AIC는 후면 배치→ Preheat 열악 환경. 분석에 중요 요소인가?
- **A (Jerry Shim)**: EDSFF(=E3)는 전면 배치→ AIC보다 열적 우세 인정. 단, **풀링 시스템에서는 AIC도 전면 배치** → 열적 역전 가능성 제시. 풀링 시스템 후면 AIC thermal impact는 미검증.

### 4. E3 Long 규격 비교
- **Q (Stuart Berke)**: E3 Long 적용 시 기획 방향 변화?
- **A (Jerry Shim)**: E3 Long 최대 1.5TB vs AIC FHHL 기본 2TB(Die 용량 따라 최대 3TB). 용량은 AIC 우세.

### 5. 폼팩터별 섀시 공간 효율성
- **Q (Stuart Berke)**: FHHL은 3U, E3는 2U. Dedicated appliance 재설계 시 최적화할 것.
- **A (Jerry Shim)**: Dell 17G 서버 FHHL은 Riser cards 사용. EDSFF는 2U, AIC FHHL은 3U/4U 필요에 동의.

### 6. 대용량 메모리 Fail 리스크 (RAS)
- **Q (Stuart Berke)**: 고용량 모듈 fail 시 가용성 리스크. 모듈 수가 2배 많은 E3가 더 나을 수도.
- **A (Jerry Shim)**:
  - AIC 2TB 초고용량 → 고객 안정성 우려 가능 → **SDDC 레벨 이상** 성능 제공 계획
  - LPDDR6 Carving-out 옵션에서 추가 Parity 확보 → Advance capability
  - Die 내부 Parity device 탑재
  - Trade-off 인정: E3 = 더 작은 granularity + 유지보수 우세. 단 E3.S는 용량 제한→ TCO 절감 어려움
  - Hot-plug 지원하나 **데이터 마이그레이션 솔루션 부재**

### 7. Use Case별 폼팩터 선호도
- **Q (SK hynix → Stuart)**: Dell은 AIC에 더 관심인데, 풀링 시스템에서는 E3도 관심 있는가?
- **A (Stuart Berke — Dell 입장 상세)**:
  - **현재 PowerEdge 플랫폼 = AIC align** (현재는 작은 시장, 고용량 달성 위해 SDP 어렵고 2H/4H DRAM Stack보다 AIC expansion이 경제적)
  - **단, 수십~수백 TB AI 풀링** = 다른 trade-off. 현재 플랫폼 아닌 **해당 usecase 최적화 설계** 의향. 전면/후면 PCIe·CXL 레인 제약 없이 섀시 레벨 최적 모듈 폼팩터 탐색.

### 8. 레퍼런스 디자인 보유 여부 + AI 풀링 적정 용량
- **Q (Stuart Berke)**: Pooled memory ref. design 있는가? Chassis당 10개 AIC=20TB가 AI 시스템 풀링으로 충분한가?
- **A (Jerry Shim)**:
  - **현재 ref. design 없음**
  - Switchless Multi Head system 기반 CXL Pooled memory FPGA 프로토타입 1개 (실리콘 아님)
  - 향후 ref. design 진행 계획, 현재 AI 애플리케이션 적합 아키텍처 내부 논의 중
  - 20TB 적정 여부 = 좋은 질문이나 데이터 부족. SK hynix도 AI 적정 용량 파악 중.

---

## 4개 요약 섹션 (원문 후반)

### ① CMM AX 컨트롤러 개발 현황 및 글로벌 협력 체계
- 실리콘 내부 코어/로드 프로세서 탑재 구조(Structure A) 첫 Evaluation Card 개발 중
- Marvell(글로벌) + Xcena(국내) 공동개발 체계 구축

### ② 폼팩터 규격 이원화 분석 및 트레이드오프 (AIC vs E3)
- **AIC FHHL (SKH 집중)**: 2TB~3TB 고용량, TCO 절감 우세, 단 3U/4U 섀시 + 발열 관리 필요
- **E3.L/S (Dell 제약 검토)**: 전면 배치→ 방열·유지보수 우수, 단 용량 한계(1.0~1.5TB)→ TCO 걸림돌

### ③ 고용량 모듈 신뢰성(RAS) 우려 기술 대응
- Dell 우려: 2TB+ 고용량 모듈 fail → 시스템 가용성·대형 장애 확산 리스크
- SK hynix 대응: SDDC 이상 고급 ECC, LPDDR6 카빙아웃 추가 패리티, Die 내부 패리티 디바이스

### ④ AI 풀링 시장 대응 전용 아키텍처 협력
- Dell 입장 변화: 기존 CXL AIC 구조 넘어 수십~수백 TB AI 풀링 전용 최적화 섀시 원점 재설계 의향
- SK hynix 과제: 섀시당 10개 AIC=20TB가 AI 요구 충족 여부 적정 풀 용량 내부 산정 후 Dell 공유 예정

---

## 후속 액션 / 미해결

- [ ] **별도 Tech. meeting** setup (Dell 요청, 일정 미정)
- [ ] AI 풀링 적정 용량 사이즈 내부 산정 (SK hynix struggling 중) → Dell 공유
- [ ] AI 애플리케이션 적합 아키텍처 타입 내부 논의 결론 도출
- [ ] AIC vs E3 최종 택일 결정 (3세대 CXL)
- [ ] CXL Memory Pooling ref. design 향후 진행
- [ ] AIC 후면 thermal impact 검증 필요 (풀링 시스템 전면 배치 가정)

## 관련
- 2026-08-11 미팅(CXL 메모리 풀링): [2026-08-11-cxl-pooling.md](2026-08-11-cxl-pooling.md) — 이 미팅(05-27)의 후속 맥락. CMM AX 컨트롤러 논의가 AIC vs E3 트레이드오프로 확장됨.
- by-customer: [dell.md](../by-customer/dell.md), [marvell.md](../by-customer/marvell.md), [xcena.md](../by-customer/xcena.md)
