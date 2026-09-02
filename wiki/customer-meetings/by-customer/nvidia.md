---
title: "NVIDIA — 고객·파트너 미팅 누적 이력"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, by-customer, nvidia, gpu, ai-fabric]
entity: nvidia
relation: customer
---

# NVIDIA — 미팅 누적 이력

> **상대방별 누적 뷰** — NVIDIA가 등장한 모든 미팅의 요약 + 현재 관계 상태.
> 미팅별 전문은 `../meetings/` (날짜키). 본 페이지는 고객별로 쌓이는 단일 출처.
> CXL DRAFT 연결: 6장 AI 패브릭 / 9장 KV offload (NVIDIA CXL 관심 전환 = 핵심 보강)

---

## 현재 관계 상태 (최신 미팅 기준)

- **관계**: 고객 (CXL F2F 미팅 셋업, 2026-08-11)
- **단계**: 초기 / KV cache off-loading 목적 CXL 메모리 풀링 관심 전환 확인
- **핵심 정정**: 기존 인지 "NVIDIA는 CXL 무관심" → **뒤집힘** (Liqid 발언 + 별도 센싱 교차 지지)
- **★ 시계열 재정립 (2026-03-12 발견)**: NVIDIA의 KV Cache CXL 관심은 **08-11 신규가 아니라 03-12 FMTA에서 먼저 질의**된 것. 08-11 "관심 전환" = 03-12 질의가 5개월 만에 구체화. "NVIDIA 무관심" 인지는 03-12~08-11 사이 일시적이었음.
- **보류**: GPU Rack ↔ CXL Pooled 효과성 = NVIDIA 내부 논의 후 피드백 대기 / 한국 FMTA(7월/10-11월)에서 KV Cache offloading update 확인 예정

## 핵심 팩트 (누적)
- NVIDIA, KV cache off-loading 목적 CXL 메모리 풀링 관심. tiering 운영 SW **Dynamo**에 반영 중 (별도 센싱, Liqid 발언 지지).
- 자사 제공 CXL 샘플 = **Vera의 CXL IP 검증용** (08-11) — 단 03-12에 "CXL Vera에서 CMM 지원 가능하나 platform 계획 없음" 확인. Vera CXL IP 검증(08-11) ↔ CMM platform 계획 부재(03-12) 교차.
- F2F 미팅 참석 = 메모리 디바이스 담당자 중심 (Barry/Derek/Ameet) → AI 연결 논의 미진 (구조적 한계).
- 시뮬레이션 자료(KV cache Pooling 가치) → NVIDIA 사내 AI 전문가 공유 후 피드백 진행.
- **★ NVIDIA KV Cache 질의 기원 (2026-03-12 FMTA)**: NVIDIA가 SK hynix에 "LLM KV Cache에 CXL 활용" 의견 질의. = KV Cache CXL thread의 진짜 시작. → 04-30 SK hynix가 MSFT에 CXL DM Pooling 제안 → 08-11 NVIDIA 관심 전환.

## 후속 액션 / 미해결
- [ ] NVIDIA 사내 AI 전문가 피드백 (KV cache Pooling 시뮬레이션)
- [ ] GPU Rack ↔ CXL Pooled 효과성 내부 논의 결과
- [ ] **Dynamo 교차검증**: NVIDIA tiering SW + AMD "Dynamo Inference SW Framework" 양쪽 언급 → 동일 SW인지 (DRAFT 9장)

## 미팅 이력 (역시간순, 최신→과거)

### 2026-08-11 — CXL 메모리 풀링 미팅
- **참석**: Barry(Director) / Derek(CXL Boards) / Ameet(CXL Validation)
- AI Application ↔ CXL Pooled 연결 논의 미진 (참석 인원 메모리 디바이스 중심).
- AI 전문가에게 자사 자료 공유 → 피드백 협의.
- 자사 CXL 샘플 = Vera CXL IP 검증용. GPU Rack↔CXL Pooled 효과성 = 내부 논의 후 피드백.
- 전문: [../meetings/2026-08-11-cxl-pooling.md](../meetings/2026-08-11-cxl-pooling.md) §고객 3) NVIDIA
- ★★★ (DRAFT 6장/9장 반영 대기)

### 2026-03-12 — FMTA CXL 미팅 (NVIDIA 최초 CXL 접촉 — KV Cache thread 기원)
- **포럼**: FMTA(Future Memory Tech. Alignment, 구 TTR). 2026-03-11 미국 F2F. 7월/10-11월 한국 예정.
- **참석**: 법인 F2F (NVIDIA 참석 — 명 미기재)
- **★ 핵심**: **NVIDIA가 SK hynix에 "LLM KV Cache에 CXL 활용" 의견 질의** = KV Cache CXL thread 진짜 기원. SK hynix가 제안한 게 아니라 NVIDIA가 먼저 물어봄.
- 기타: CXL Vera CMM 지원 가능하나 platform 계획 없음 / Liquid Cooling엔 E3.S 크고 E1.S 적합 / CXL 제품 방향 지속 보고.
- 후속: 한국 FMTA에서 KV Cache offloading update 확인 계획.
- 전문: [../meetings/2026-03-12-fmta-cxl.md](../meetings/2026-03-12-fmta-cxl.md)
- ★★★ (DRAFT 6장/9장 — KV Cache thread 기원 반영 대기, 핵심)
