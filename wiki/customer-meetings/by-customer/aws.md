---
title: "AWS — 고객 미팅 누적 이력"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, by-customer, aws, kv-cache, imdb, 1dpc, tco]
entity: aws
relation: customer
---

# AWS — 미팅 누적 이력

> **상대방별 누적 뷰** — AWS가 등장한 모든 미팅의 요약 + 현재 관계 상태.
> 미팅별 전문은 `../meetings/` (날짜키).
> CXL DRAFT 연결: 11장 시장 인텔리전스 / KV Cache 중간 Tier (자사 발의 축 기원) / IMDB

---

## 현재 관계 상태 (최신 미팅 기준)

- **관계**: 고객 (CXL KV Cache 중간 Tier 제안, 2026-02-10)
- **단계**: **PoC 검증 단계** — AWS 대규모 채택 가능성 낮음, 단 KV Cache 문제 심화 시 중장기 재부상 가능성
- **핵심**: 자사가 AWS에 CXL Memory **중간 Tier** 제안 (KV Cache spill 해결). AWS는 Capacity expansion 유효 후보로 보나 **Killer Use case 안 보임** + Latency/SW 복잡도/1DPC 선호 제약. **성능·비용·응용 동시 만족 + 명확한 TCO 개선 필요**.
- **★ 자사 발의 KV Cache 제안의 가장 이른 기록** (03-12 NVIDIA 질의보다 1개월 이전). 자사 발의 축의 기원.

## 핵심 팩트 (누적)
- **KV Cache 문제 배경**: AI 확산 → KV Cache 폭증. HBM→Main memory→Storage 계층에서 **Storage spillover 시 성능 급락** (모든 KV Cache 논의의 공통 배경).
- **자사 제안**: main Memory ↔ Storage 사이 **CXL Memory 중간 Tier** 도입 (02-10).
- **AWS 반응**: Capacity expansion **유효 후보**, AI·IMDB 논의 중, 내부 평가 수행 중.
- **AWS 제약 (4개)**: Latency 증가 / Memory tier 관리 복잡성 / **1DPC 선호** / **명확한 Killer Use case 안 보임**. 성능·비용·응용 동시 만족 필요.
- **주요 Use-case**: **AI Service 가장 유력** (KV Cache spill 해결, Storage 대비 성능 우위 분명). **IMDB 범용 서비스 확대 계획 아직 없음**.
- **고용량 관점**: AWS High memory platform = 일반 서버와 동일 view → **"용량만 확장"** 방향 유지.
- **Roadmap**: 대규모 채택 가능성 낮음, PoC 유지. KV Cache 문제 심화 시 CXL **재부상 가능**(중장기). **명확한 TCO 개선 필요**.
- **AWS 참석자 (02-10)**: Ashiq Reza(Principal, Technology Strategy) / David Derrick(Sr. Manager SW Development) / Bhavi Bhadviya / Sunhwa Jung / Jongwon Lee / Andrew Chau — 6명, 다부문(Technology Strategy·SW·HW·TPM·Manufacturing).

## 후속 액션 / 미해결
- [ ] **명확한 Killer Use case** 정의 (AWS 제약 "안 보임" 해소)
- [ ] Latency 증가 완화 (CXL 중간 Tier 성능 검증)
- [ ] Memory tier 관리 복잡성 해소 (SW)
- [ ] **1DPC 선호** 대응 (CXL 구성 옵션)
- [ ] 성능·비용·응용 3축 동시 만족 시나리오
- [ ] 명확한 TCO 개선 수치 (고객 체감)
- [ ] AI Service Use-case 구체화 (KV Cache spill 해결 정량)

## 미팅 이력 (역시간순)

### 2026-02-10 — AWS CXL KV Cache 중간 Tier 미팅 (AWS 최초 CXL 접촉, 자사 발의 KV Cache 기원)
- **참석**: 강욱성 / 심응보 팀장님 / 구병호 TL(자사) // Ashiq Reza(Principal, Technology Strategy) / David Derrick(Sr. Mgr SW Dev) / Bhavi Bhadviya / Sunhwa Jung / Jongwon Lee / Andrew Chau(AWS, 6명)
- **AWS 최초 CXL 접촉**. 자사 CXL Memory 중간 Tier 제안(KV Cache spill 해결). AWS Capacity expansion 유효 후보, 단 Killer Use case 안 보임 + Latency/SW 복잡도/1DPC 선호 제약. AI Service 가장 유력, IMDB 확대 미정. 대규모 채택 낮음, PoC 유지, KV Cache 심화 시 중장기 재부상. TCO 개선 필요.
- 전문: [../meetings/2026-02-10-aws-cxl-kv-cache.md](../meetings/2026-02-10-aws-cxl-kv-cache.md)
- ★★★ (DRAFT 11장 시장 — KV Cache 자사 발의 축 기원 + Killer Use case/1DPC 제약 반영 대기, 핵심)
