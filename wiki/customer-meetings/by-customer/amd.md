---
title: "AMD — 고객·파트너 미팅 누적 이력"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, by-customer, amd, host]
entity: amd
relation: partner
---

# AMD — 미팅 누적 이력

> **상대방별 누적 뷰** — AMD가 등장한 모든 미팅의 요약 + 현재 관계 상태.
> 미팅별 전문은 `../meetings/` (날짜키).
> CXL DRAFT 연결: 5장 CPU/GPU 벤더 / 9장 KV offload (Dynamo)

---

## 현재 관계 상태 (최신 미팅 기준)

- **관계**: 파트너 (White Paper 공동 작성 합의, 2026-08-11)
- **단계**: 공동 평가 결과 → Supercomputing 학회 목표 White Paper 작성
- **핵심**: **Dynamo Inference SW Framework** 언급 (NVIDIA tiering SW와 동일 이름 — 교차검증 필요)

## 핵심 팩트 (누적)
- 자사 Pooled 전략 공유. **White Paper 작성이 발표보다 효과적** 공감 → 공동 평가 결과 **Supercomputing 학회 목표** 작성.
- **Dynamo Inference SW Framework 외 AMD 보유 SW로 자사 SW 마이그레이션 방안** 검토.

## 후속 액션 / 미해결
- [ ] 공동 White Paper 작성 (Supercomputing 학회)
- [ ] AMD SW로 자사 SW 마이그레이션 방안
- [ ] **Dynamo 교차검증**: NVIDIA tiering SW와 동일 이름 — 동일 SW인지 (DRAFT 9장, NVIDIA by-customer와 쌍)

## 미팅 이력 (역시간순)

### 2026-08-11 — CXL 메모리 풀링 미팅
- **참석**: Rita(CXL Arch, Fellow) / Ketan(SK hynix Account Manager)
- White Paper 공동 작성(Supercomputing). Dynamo Inference SW Framework + AMD SW 마이그레이션.
- 전문: [../meetings/2026-08-11-cxl-pooling.md](../meetings/2026-08-11-cxl-pooling.md) §파트너 5) AMD
- ★ (DRAFT 5장 반영 대기)

### 2026-03-11 — Oracle OCI CXL Pooling 미팅 (AMD 간접 등장 — DIMM ch 확장)
- **참석**: SANTOSH KUMAR / SEUNGJU HAN / Donghyeok Park(자사) // JEBA SUNDRARAJ(Jay) / Somu Krishnasamy(Oracle)
- AMD 직접 참석 아님. Jay 발언: **AMD 12→16 DIMM ch 확장** → CXL 추가 가치 없어짐. Oracle DB 팀 tiered memory → TCO 무의미 + DIMM ch 확장이 나음 → 계획 중단의 근거.
- 전문: [../meetings/2026-03-11-oracle-oci-cxl.md](../meetings/2026-03-11-oracle-oci-cxl.md) §2·4)
- ★★ (DRAFT — Local CXL 사업성 악화 신호, CPU 채널 확장 트렌드 반영 대기)

### 2026-02-05 — Google DRAM/MRDIMM 미팅 (AMD 간접 등장 — Venice/ARM4/Florence 플랫폼, 비-CXL)
- **참석**: AMD 직접 참석 아님. Google(Brian Morris-Platform Architect 외 5명) / SK hynix(강선국 외 6명).
- AMD 플랫폼 3개 간접 등장: **Venice**(High Performance, MRDIMM 필수/POR — BW/Core, RDIMM 전환 시 System balance 붕괴) / **ARM4**(Value Proposition, RDIMM 8800 백업, 64/128GB) / **Florence**(Gen4 지원, Gen3 대비 Q2~3 느림 → AMD Gen4 지원 여부/시점 핵심).
- **LP MRDIMM 지원 여부 = 핵심** → 자사가 Google에 AMD 설득 요청. 동일 Platform Gen3→Gen4 트랜지션 선호, 256GB 필요.
- 전문: [../meetings/2026-02-05-google-dram-mrdimm.md](../meetings/2026-02-05-google-dram-mrdimm.md) §4·5)
- ★★ (DRAFT 5장 반영 대기 — AMD 서버 플랫폼 로드맵 Venice/ARM4/Florence + MRDIMM Gen3/Gen4/LP, 비-CXL DRAM 관점)

> **교차검증 대기**: AMD DIMM 12→16ch 확장(03-11 Oracle 간접) = Local CXL 가치 훼손 신호. AMD 08-11 미팅(White Paper, Dynamo)은 Pooled/AI 관점 — Local 부정(03-11) ↔ Pooled 긍정(08-11)이 AMD CXL 입장의 양면. **AMD Venice = Google 02-05(MRDIMM 필수, DRAM) ↔ HPE 02-12("Gen13 Venice" CXL Post-Launch)** — 동일 AMD Venice 플랫폼이 DRAM(MRDIMM) 관점(Google)과 CXL 관점(HPE) 양쪽에서 교차 등장.
