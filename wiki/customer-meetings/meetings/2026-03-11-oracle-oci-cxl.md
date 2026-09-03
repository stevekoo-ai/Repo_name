# Oracle OCI — CXL Pooling 미팅 (2026-03-11, Santa Clara F2F)

> **Source**: [sources/oracle-oci-cxl-meeting-2026-03-11.md](../../../sources/oracle-oci-cxl-meeting-2026-03-11.md) (불변 원문)
> **작성자**: 구병호(KOO BYEONG HO) DRAM Solution (2026-03-12 작성, 4분 분량)
> **날짜**: 2026-03-11
> **장소**: Oracle Santa Clara (F2F)
> **자사 참석자**: SANTOSH KUMAR, SEUNGJU HAN (승주), Donghyeok Park (동혁)
> **Oracle 참석자**: JEBA SUNDRARAJ (Jay, Sr. Principal HW Engineer), Somu Krishnasamy (NPI HW Engineer)
> **관계**: Oracle = customer · Marvell = partner (switch 인수 경쟁) · Xconn = partner (CXL switch 벤더) · Montage = competitor (Multi-Head controller) · Broadcom = competitor (CXL switch 시장 부정) · AMD = partner (DIMM ch 확장)

---

## 핵심 요약

| # | 주제 | 결론 / 핵심 팩트 |
|---|------|------------------|
| 1 | Pooling 현황 | Switch 기반 pooling OCI VM 적용 준비 중, **Xconn 일정 문제로 slow down**. 6월 재체크. AI 아님(Cloud service, GP에 가까움). 주 목적 = **Stranded memory 해결** |
| 2 | TCO | **가장 중요**. DIMM과 같은 수준 Cost 요구 |
| 3 | AIC FF | Oracle에 **너무 큼** |
| 4 | Liquid Cooling | Oracle **사용 불가** |
| 5 | HA 요구 | **단일 실패 지점(SPOF) 감당 불가** → 풀링 시작하려면 HA 필수 → switch = SPOF |
| 6 | Switchless + Montage | 다른 벤더와 Switchless Pooling 시도(초기) → **Montage 언급**. MHD(2세대 CXL CMM) 2포트→2호스트→SPOF 없음→HA |
| 7 | 풀 구성 | **최소 4대 서버** ↔ CXL memory box |
| 8 | Xconn/Marvell | Xconn 협의 → Marvell 인수로 중단 → **4월 Oracle이 Xconn/Marvell과 재논의** |
| 9 | Marvell 스위치 의도 | **Broadcom과 경쟁** 위해 스위치 인수 |
| 10 | Broadcom 입장 | **"CXL 스위치 시장 없다"** 주장 |
| 11 | DB 팀 tiered memory | CXL을 tiered memory로 검토했으나 **TCO 이점 없음 + DIMM ch 확장이 나음 → 계획 중단** |
| 12 | AMD 영향 | **DIMM 12→16ch 확장** → CXL 추가 가치 없어짐 |
| 13 | OCI 채택 조건 | DIMM보다 저렴 / latency는 충분히 싸면 감수 / **VM용 (GPU/AI 추론 아님)** |
| 14 | 후속 | late Q2(6월) sync-up 재예정 |

---

## 상세 정리

### 1. Pooling 현황 (팀장 보고 요지)
- **Switch 기반 pooling**으로 OCI VM 적용 준비 중
- 단, **Xconn 일정 문제**로 진행 **slow down**
- **AI가 아님** — Cloud service 응용, GP(General Purpose)에 가까움
- 주 목적(추정): **Stranded memory 해결**
- **TCO가 가장 중요** — DIMM과 같은 수준의 Cost 요구
- **AIC FF = Oracle에 너무 큼**
- 6월경 진행사항 재체크 필요

### 2. Local (DB 응용) — CXL tiered memory 부정
- 기존 Oracle DB 응용에서 latency 문제 있었음
- CPU들이 ch 수를 늘려와 용량 확장 중 → **TCO 뒷받침 안 되면 play 어려움**
- DB 팀: CXL을 tiered memory로 검토했으나 **TCO 이점 없음** → 더 많은 DIMM 채널이 나음 → **계획 중단**
- **AMD 12→16 DIMM ch 확장** → CXL 추가 가치 없어짐

### 3. Oracle status update (구체)
- Oracle cloud DDR4 메모리 사용량 **매우 작음** (decommissioned DIMM 많지 않음)
- **AIC FF = 너무 큼**
- **Liquid cooling 사용 불가**
- Xconn과 협의 중이었으나 **Marvell 인수 후 중단**
- **SPOF 감당 불가** → 풀링 시작하려면 **HA 필수, SPOF 없어야 함**
- 다른 벤더와 **Switchless Pooling** 시도 (초기 단계) → **Montage 언급**
- **최소 4대 서버** ↔ CXL memory box = Oracle에 적합한 풀링

### 4. OCI CXL 메모리 채택 의견
- OCI = **DIMM보다 낮은 가격** 기대
- TCO 관점에서 Pooling 합리적 — VM에 메모리 **온디맨드 할당** 가능
- **충분히 저렴하면 latency 감수 의향**
- **VM 애플리케이션용 (GPU/AI 추론 아님)**
- Xconn 협의 → 인수로 중단 → **4월 Oracle이 Xconn/Marvell과 재논의**
- **Marvell = Broadcom 경쟁 위해 스위치 인수**
- **Broadcom = "CXL 스위치 시장 없다" 주장**

### 5. Montage Multi-Head Device (MHD) — HA 핵심
- **MHD (2세대 CXL CMM) = 2포트 지원 → 2호스트 연결**
- 서버 A 고장 → 서버 B가 메모리 접근 가능 → **SPOF 없음 → HA 구현**
- "기업 환경에서 진정한 풀링 솔루션(True pooling solution)" — Jay 발언
- 단, **Jay가 구체 디테일 없음** — Montage에 직접 reach-out 권함 (Q2 미해결)

### 6. Santosh 회의 요약 (영문)
- Oracle은 CXL pooling(OCI VM용)에 관심, 단 **CXL switch 부재**로 진행 지연
- Xconn/switch 논의 지연 (예상 초과) → 2-3개월 내 진전 예상, 6월 follow-up
- Oracle = enterprise-grade reliability 요구 → 4서버 + CXL switch 풀 구성 희망
- late Q2 sync-up 합의

### 7. 구병호 Q&A (Jay 답변)
- **Q1 (HA 의미)**: HA = High Availability. 단일 CXL switch 설계 시 switch = SPOF.
- **Q2 (Montage MH = 8CH or 2CH, true solution 의미)**: Jay 구체 디테일 없음 → Montage에 직접 문의 권함. **미해결**.

---

## 핵심 인사이트 (5개 미팅 통합 시계열 기준)

1. **★★ Oracle TCO + FF**: AIC 너무 큼(03-11) ↔ Dell AIC FHHL 2~3TB(05-27) ↔ HPE E3.S 주(05-07) ↔ FMTA E1.S liquid 적합(03-12). Oracle은 liquid 불가+AIC 큼 → 가장 폼팩터 제약 강한 고객.
2. **★★ Switch 경쟁 구도**: Marvell(Broadcom 경� 위해 switch 인수) vs Broadcom("CXL switch 시장 없다") vs Xconn(Marvell 인수 대상). Switch 벤더 경쟁이 Oracle pooling 일정 좌우.
3. **★★ Montage MHD = HA 경로**: 자사 2세대 CXL CMM 2포트 = SPOF 제거 = Oracle HA 요구 충족 가능 경로. 단, Jay가 구체 모름 → Montage 직접 문의 필요 (미해결, montage.md 교차).
4. **★ AMD 12→16ch**: Local CXL 가치 훼손 — DIMM ch 확장이 CXL 대체. Local CXL 사업성 악화 신호 (Dell 05-27 RAS, HPE 05-07 E3.S 주와 다른 축).
5. **★ Stranded memory**: Oracle pooling 주 목적(추정) = Stranded memory 해결. AI 아님, GP/Cloud service. 08-11 "주요 풀링 고객=Neo-Cloud" 맥락의 기원.

---

## 후속 액션 / 미해결

- [ ] **6월(late Q2) Oracle sync-up** — pooling 진행사항 재체크
- [ ] **4월 Oracle ↔ Xconn/Marvell 재논의** 결과 확인
- [ ] **Montage MHD 상세** — 8CH or 2CH, "true solution" 의미 (Jay가 몰라 직접 Montage 문의 필요) → montage.md 교차검증
- [ ] Oracle HA 요구 vs 자사 2세대 CMM 2포트(MHD) 매핑 — SPOF 제거 경로 구체화
- [ ] Oracle TCO 목표(DIMM 수준) 달성 방안
- [ ] AMD 12→16ch 확장이 Local CXL 사업성에 미치는 영향 정량

## 관련
- 2026-08-11 풀링 미팅: [2026-08-11-cxl-pooling.md](2026-08-11-cxl-pooling.md) — Oracle "POC, AIC PNM 샘플 전달 대기, 차주 후속". 본 03-11의 Xconn slow down → 5개월 후 POC 단계로 진전? 차주 후속(08-11) ↔ 6월 sync-up(03-11) 시계열 연속성 확인 필요.
- 2026-03-12 FMTA: [2026-03-12-fmta-cxl.md](2026-03-12-fmta-cxl.md) — 다음 날. NVIDIA KV Cache 질의 기원. Oracle 03-11과 FMTA 03-12는 같은 주 연속 미팅.
- by-customer: [oracle.md](../by-customer/oracle.md)·[marvell.md](../by-customer/marvell.md)·[montage.md](../by-customer/montage.md)·[amd.md](../by-customer/amd.md); 신규: [xconn.md](../by-customer/xconn.md)·[broadcom.md](../by-customer/broadcom.md)
