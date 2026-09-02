---
title: "MSFT (Microsoft) — 고객·파트너 미팅 누적 이력"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, by-customer, msft, microsoft]
entity: msft
relation: customer
---

# MSFT (Microsoft) — 미팅 누적 이력

> **상대방별 누적 뷰** — MSFT가 등장한 모든 미팅의 요약 + 현재 관계 상태.
> 미팅별 전문은 `../meetings/` (날짜키).
> CXL DRAFT 연결: 11장 시장 인텔리전스 / 2장 기술 (Optic+CXL SSD)

---

## 현재 관계 상태 (최신 미팅 기준)

- **관계**: 고객 (Pooled 협업 지속, 2026-08-11)
- **단계**: pathfinding — AI 응용 데이터 부족(초기) → 자사와 협업 연속
- **협력 조건**: Pooled Appliance 제공 시 협력 가능
- **연속성**: 04-30 KV Cache 오프로딩 제안 → 08-11 pathfinding 단계 유지. 04-30 Action(Terry·Amanda·Rajesh 추가 by Phyllis) → 08-11 Terry·Adam(System Architect) 참석으로 이행.

## 핵심 팩트 (누적)
- Local CXL: TCO 최우선, **MDS**(저비용 미디어) 선호.
- Pooled: 현재 pathfinding 단계, AI 응용 데이터 부족.
- Samir(System Architect): Rack 간 인터커넥트로 **Optic + CXL SSD** 중요성 강조 (Optical I/F 인사이트와 연결).
- **KV Cache 오프로딩 제안 (2026-04-30)**: SK hynix CXL DM Pooling 아키텍처. SSD 대비 10~100배 빠름 / RDMA 대비 지연 90% 감소(레이어 바이패스) / 비용 ~66% 효율. Phyllis **검토 동의**. — 08-11 pathfinding·Neo-Cloud 풀링 고객 맥락의 기원.
- **우려사항 (2026-04-30)**: Multi-sourcing 리스크 / TCO 검증 필요("Competitive TCO" 상세 분석). — 08-11 "Pooled Appliance 시 협력" 조건과 연속.
- **AIC 장점 인식 (2026-04-30)**: AIC = 서버 기구/열 설계 맞춤 카드 설계 가능 → 표준 FF 얽매이지 않아 유리 (Phyllis).

## 후속 액션 / 미해결
- [ ] Pooled Appliance 제공 방안 논의
- [ ] MSFT Azure 상용배포 현황 (cxl-next-gen-memory.md에 "MS Azure 상용배포 확인" 기존 — 본 미팅과 교차)

## 미팅 이력 (역시간순)

### 2026-08-11 — CXL 메모리 풀링 미팅
- **참석**: Phyllis(Sr. Director, Roadmap & Strategy) / Samir·Terry·Adam(System Architect)
- Local=TCO+MDS, Pooled=상황 다르다. pathfinding 단계, AI 데이터 부족 → 협업 연속.
- Pooled Appliance 시 협력 가능. Samir: Optic+CXL SSD 강조.
- 전문: [../meetings/2026-08-11-cxl-pooling.md](../meetings/2026-08-11-cxl-pooling.md) §고객 1) MSFT

### 2026-04-30 — CXL KV Cache 미팅 (MSFT 최초 CXL 접촉)
- **참석**: 강욱성 / 심응보 팀장님 / 이상돈 TL / 구병호 TL(자사) // Phyllis Ng(MSFT)
- **최초 CXL 접촉**. KV Cache 이슈에 SK hynix CXL DM Pooling 제안(SSD 대비 10~100배 / RDMA 대비 지연 90% 감소 / 비용 66% 효율). Phyllis pathfinding 단계, SW path-finding 집중(메모리 쉐어링/동적·정적 할당). AIC vs LPDDR AIC 비교 제시.
- 긍정: 저전력 관심, **KV Cache 오프로딩 실험 결과 공유 검토 동의**.
- 우려: **Multi-sourcing 리스크** / AIC=표준 FF 얽매이지 않아 유리 / **TCO 검증 필요**("Competitive TCO" 상세 분석).
- Action: MSFT 전문가 **Terry·Amanda·Rajesh** 추가(by Phyllis) → KV Cache Usage-Scenario + TCO follow-up.
- 전문: [../meetings/2026-04-30-msft-cxl-kv-cache.md](../meetings/2026-04-30-msft-cxl-kv-cache.md)
- ★★ (DRAFT 11장 시장 인텔리전스 / KV Cache 오프로딩 기원 반영 대기)
