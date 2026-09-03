---
title: "Intel — 고객·파트너 미팅 누적 이력"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, by-customer, intel, gpu, host]
entity: intel
relation: partner
---

# Intel — 미팅 누적 이력

> **상대방별 누적 뷰** — Intel이 등장한 모든 미팅의 요약 + 현재 관계 상태.
> 미팅별 전문은 `../meetings/` (날짜키).
> CXL DRAFT 연결: 5장 CPU/GPU 벤더 / 9장 KV offload (Intel GPU Server KV Cache 경로 신규)

---

## 현재 관계 상태 (최신 미팅 기준)

- **관계**: 파트너 (Pooled Validation 내부 논의 필요, 2026-08-11)
- **단계**: 자사·고객 모두 Pooled 관심 → Validation 방법 내부 논의 중
- **핵심 신규**: Intel GPU Server–CXL Pooled 기반 **KV Cache 협력 경로** 제안

## 핵심 팩트 (누적)
- 자사 Pooled 전략 공유. Intel은 자사·고객 모두 Pooled 관심 → Validation 내부 논의 필요 입장.
- 자사 제안: Intel DMR POC **Sharing** Co-enabling·Validation + **Intel GPU Server–CXL Pooled 기반 KV Cache 협력·성능 향상 평가** → Intel 내부 검토 후 피드백.
- US Testbed 협력: CXL Eco-system Enabling Team 내부 입장 미정리 → 확인 후 피드백.

## 후속 액션 / 미해결
- [ ] Intel DMR Sharing Co-enabling/Validation 피드백
- [ ] Intel GPU Server–CXL Pooled KV Cache 협력 피드백
- [ ] US Testbed 입장 정리

## 미팅 이력 (역시간순)

### 2026-08-11 — CXL 메모리 풀링 미팅
- **참석**: Richelle(Sr. Director) / Jenni(Manager, CXL Eco-system Enabling Team)
- Pooled Validation 내부 논의. DMR Sharing Co-enabling + Intel GPU Server KV Cache 협력 제안. US Testbed 미정리.
- 전문: [../meetings/2026-08-11-cxl-pooling.md](../meetings/2026-08-11-cxl-pooling.md) §파트너 4) Intel
- ★ (DRAFT 5장/9장 반영 대기 — Intel GPU KV Cache 경로 신규)

### 2026-02-05 — Google DRAM/MRDIMM 미팅 (Intel 간접 등장 — DMR/EMR/Ghostfish, 비-CXL)
- **참석**: Intel 직접 참석 아님. Google(Brian Morris-Platform Architect 외 5명) / SK hynix(강선국 외 6명).
- Intel 플랫폼 간접 등장: **DMR**(POR 48→64GB 변경 검토, EVT 64GB 검증 후 최종, **(Confidential) GA @27년 1~2월**) / **EMR**·**Ghostfish Enabling**(64GB 7200Mbps 샘플 필요, 현재 5600Mbps 운용).
- 자사 1cnm 96GB 4개월 당겨 DMR NPI Intercept + ARM3 Sustain Qual 제안 → Google 기술팀 "문제 없음".
- 전문: [../meetings/2026-02-05-google-dram-mrdimm.md](../meetings/2026-02-05-google-dram-mrdimm.md) §2·6)
- ★★ (DRAFT 7장/5장 반영 대기 — Intel DMR 48→64GB 전환 + GA 27년 1~2월 + EMR/Ghostfish, 비-CXL DRAM 관점. 08-11 "DMR Sharing Co-enabling"의 전신 맥락)

> **교차검증**: Intel DMR이 Google 02-05(DRAM, 48→64GB, GA 27년 1~2월) ↔ Intel 08-11(CXL, DMR Sharing Co-enabling) 양쪽에서 등장 — 동일 DMR 플랫폼이 DRAM(Google) 관점과 CXL(Intel 직접) 관점 양쪽 교차.
