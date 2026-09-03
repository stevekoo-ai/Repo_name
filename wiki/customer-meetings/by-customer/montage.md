---
title: "Montage — 미팅·시장情报 누적 이력"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, by-customer, montage, controller, gen2, cxl32, competitor]
entity: montage
relation: competitor
---

# Montage — 미팅·시장情报 누적 이력

> **상대방별 누적 뷰** — Montage가 등장한 모든 미팅·시장 신호의 요약 + 현재 관계 상태.
> 미팅별 전문은 `../meetings/` (날짜키).
> CXL DRAFT 연결: 3장 컨트롤러 (CMM AX 경쟁 — Gen2 third party / CXL 3.2 MXC)

> **주의**: Montage는 SK hynix CMM AX(Marvell+Xcena 공동개발)와 같은 컨트롤러 IP 카테고리의 경쟁사.
> 단, HPE Gen2 플랫폼에서는 SK hynix 메모리가 장착되는 CXL 컨트롤러 서플라이어(제3자)로도 작용 — 맥락에 따라 경쟁·협력 양면. 본 페이지는 컨트롤러 IP 경쟁 관점에서 competitor로 분류.

---

## 현재 관계 상태 (최신 기준)

- **관계**: 경쟁사 (CXL 컨트롤러 IP — CMM AX 경쟁), 2026-08-11
- **단계**: CXL 3.2 MXC 업계 최초 시료생산(2026-07-31, Newsroom 1호 ★★★) — CXL 3.x가 IP/RTL 검증 넘어 실리콘 검증 단계로 이행. Gen2(2026-05 시점)에서는 HPE 플랫폼 제3자 컨트롤러.
- **핵심**: Montage = **CXL 컨트롤러 IP 리더**. Gen2 third party(2026-05-07 HPE 미팅 확인) → CXL 3.2 MXC 업계 최초 시료생산(2026-08-11 Newsroom). 자사 CMM AX(Structure A, Marvell+Xcena 공동개발, Evaluation Card)의 주요 경쟁 벤치마크.

## 핵심 팩트 (누적)
- **Gen2 CXL 컨트롤러 = Third party Montage** (재확인, 2026-05-07 HPE 미팅 — 김의현 TL 메모). HPE Gen2 플랫폼의 CXL 컨트롤러 서플라이어.
- **CXL 3.2 MXC 시료생산** (2026-07-31, 업계 최초 — Newsroom 1호 2026-08-11 ★★★). CXL 3.x가 IP/RTL 검증 단계 넘어 실리콘 검증 단계로 이행한 업계 최초 사례.
- **경쟁 구도**: 자사 CMM AX(Structure A, Marvell+Xcena 공동개발, Evaluation Card 개발 중, 2026-05-27 Dell 미팅) vs Montage MXC(CXL 3.2 시료생산 완료) — 자사 CMM AX가 Evaluation Card 단계인 동안 Montage는 이미 CXL 3.2 실리콘 시료생산 완료. **타이밍 격차 주목 필요**.
- **★ MHD(Multi-Head Device) HA 경로 (2026-03-11 Oracle 미팅)**: Oracle이 Switchless Pooling 시도 중 Montage 언급. MHD = 2포트 → 2호스트 → SPOF 없음 → HA(단일 CXL switch = SPOF). Jay "기업 환경에서 true pooling solution". 단, **MHD = 8CH or 2CH? "true solution" 의미? = Jay도 모름 → Montage 직접 문의 필요(미해결 Q2)**. 자사 2세대 CXL CMM 2포트(2호스트)와 Montage MHD의 관계 미확정 — 동일/경쟁/참조?
- (참고) Montage는 중국 CXMT 계열 메모리 인터페이스 칩 생태계 — CXL 컨트롤러 외에도 DDR5 등 메모리 인터페이스 영역.

## 후속 액션 / 미해결
- [ ] Montage CXL 3.2 MXC 스펙·고객 확보 현황 추적 (Newsroom 2호 보완 대상)
- [ ] 자사 CMM AX(Structure A) vs Montage MXC 기능·타이밍 격차 정량 비교
- [ ] HPE Gen2에서 Montage 컨트롤러 + 자사 메모리 결합 여부 확인 (Gen2 → Gen3 전환 시 컨트롤러 교체 가능성)
- [ ] Montage가 CXL 3.2에서 확보한 고객/플랫폼 파악 (자사 CMM AX 타겟 고객 중첩 여부)

## 미팅·신호 이력 (역시간순)

### 2026-08-11 — CXL Newsroom Update 1호 (Montage CXL 3.2 MXC 시료생산)
- Montage CXL 3.2 MXC 시료생산(2026-07-31, 업계 최초) — HERO 헤드라인 ★★★.
- 출처: [../daily-updates/cxl-newsroom-update-2026-08-11.md](../daily-updates/cxl-newsroom-update-2026-08-11.md) (Newsroom Collector 1호)
- ★★★ (DRAFT 3장 컨트롤러 — 경쟁 벤치마크 핵심 반영 대기)

### 2026-05-07 — HPE CXL Gen2 미팅 (Montage 간접 등장)
- **참석**: 김의현 TL(자사) // HPE
- Montage 직접 참석 아님. 김의현 TL이 HPE Gen2 CXL 컨트롤러가 Third party = Montage임을 재확인. 2027-06 Venice(SP7/SP8) Launch 목표, 자사 2월 sample acceptable.
- 전문: [../meetings/2026-05-07-hpe-cxl-gen2.md](../meetings/2026-05-07-hpe-cxl-gen2.md) §Gen2 컨트롤러)
- ★ (DRAFT 3장 컨트롤러 — Gen2 third party 맥락 반영 대기)

### 2026-03-11 — Oracle OCI CXL Pooling 미팅 (Montage 간접 등장 — MHD HA 경로)
- **참석**: SANTOSH KUMAR / SEUNGJU HAN / Donghyeok Park(자사) // JEBA SUNDRARAJ(Jay) / Somu Krishnasamy(Oracle)
- Montage 직접 참석 아님. Oracle이 Switchless Pooling 시도 중 Montage 언급. **MHD(Multi-Head Device, 자사 2세대 CXL CMM) = 2포트 → 2호스트 → SPOF 없음 → HA** 경로. Jay "기업 환경에서 true pooling solution" 발언. 단 Jay가 8CH/2CH 디테일 모름 → Montage 직접 문의 필요(미해결).
- 전문: [../meetings/2026-03-11-oracle-oci-cxl.md](../meetings/2026-03-11-oracle-oci-cxl.md) §5)
- ★★ (DRAFT 3장 컨트롤러 — MHD HA 경로 + 미해결 Q2 반영 대기)

> **교차검증 대기**:
> 1. Montage MXC(CXL 3.2 시료생산, 2026-08-11) ↔ HPE Gen2에서 Montage 컨트롤러 사용(2026-05-07). HPE가 Gen2→Gen3(CXL 3.x) 전환 시 Montage MXC 채택 여부 = 자사 CMM AX의 HPE 진입 가능성에 직결.
> 2. **Montage MHD = 8CH or 2CH? "true solution" 의미?** (Oracle 03-11 Jay 미해결 Q2) → Montage 직접 문의 필요. 자사 2세대 CXL CMM 2포트(2호스트)와 Montage MHD의 관계 — 동일/경쟁/참조?
