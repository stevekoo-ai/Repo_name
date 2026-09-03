# AWS — CXL KV Cache 중간 Tier 미팅 (2026-02-10)

> **Source**: [sources/aws-cxl-kv-cache-meeting-2026-02-10.md](../../../sources/aws-cxl-kv-cache-meeting-2026-02-10.md) (불변 원문)
> **작성자**: 구병호(KOO BYEONG HO) DRAM Solution (last updated 2026-03-09)
> **날짜**: 2026-02-10
> **자사 참석자**: 강욱성 담당님, 심응보 팀장님, 구병호 TL
> **AWS 참석자**: Ashiq Reza (Principal, Technology Strategy), David Derrick (Sr. Manager SW Development), Bhavi Bhadviya (Sr. HW Development Engineer), Sunhwa Jung (Sr. Technical Program Manager), Jongwon Lee (Sr. HW Development Engineer), Andrew Chau (Sr. Manufacturing Engineer)
> **관계**: AWS = customer
> **성격**: 자사가 AWS에 **KV Cache 중간 Tier 제안** — **자사 발의 KV Cache 제안의 가장 이른 기록** (03-12 NVIDIA 질의보다 1개월 이전, 04-30 MSFT 제안보다 2개월 이전). KV Cache thread의 자사 발의 평행 축 기원.

---

## 핵심 요약

| # | 주제 | 결론 / 핵심 팩트 |
|---|------|------------------|
| 1 | AWS CXL 입장 | 검토 중인 옵션, 단 **아직 필수 아님**. AI·IMDB 잠재 가치 있으나 Latency·SW 복잡도·TCO 명확해야 채택 |
| 2 | KV Cache 문제 | AI 확산 → KV Cache 폭증. HBM→Main memory→Storage 계층에서 **Storage spillover 시 성능 급락** |
| 3 | 자사 제안 | main Memory ↔ Storage 사이 **CXL Memory 중간 Tier** 도입 제안 |
| 4 | AWS 반응 | Capacity expansion **유효 후보**, AI·IMDB 논의 중, 내부 평가 수행 중 |
| 5 | AWS 제약 | Latency 증가 / Memory tier 관리 복잡성 / **1DPC 선호** / **명확한 Killer Use case 안 보임** / 성능·비용·응용 동시 만족 필요 |
| 6 | 주요 Use-case | **AI Service 가장 유력** (KV Cache spill 해결, Storage 대비 성능 우위 분명). IMDB 범용 서비스 확대 계획은 아직 없음 |
| 7 | 고용량 관점 | AWS High memory platform = 일반 서버와 동일 view → **"용량만 확장"** 방향 유지 |
| 8 | Roadmap | AWS **대규모 채택 가능성 낮음**, PoC 검증 단계 유지. KV Cache 문제 심화 시 CXL **재부상 가능**(중장기 관심). **명확한 TCO 개선 필요** |

---

## 상세 정리

### 1) CXL 기반 메모리 확장 + AI/고용량 워크로드 적용 가능성

**a) KV Cache 문제 배경**
- AI 확산 → **KV Cache 폭증**
- 기존 계층: HBM → Main memory → Storage
- **Storage spillover 발생 시 성능 급락** (핵심 pain point)

**b) 자사 제안 — CXL Memory 중간 Tier**
- main Memory와 Storage 사이에 **CXL Memory 중간 Tier** 도입 제안
- **AWS 반응**: Capacity expansion의 **유효한 후보**. AI·IMDB향 전반 논의 중. 내부 평가 수행 중.
- **AWS 제약 (4개)**:
  - Latency 증가
  - Memory tier 관리 복잡성
  - **단일 구성(1DPC) 선호**
  - **명확한 Killer Use case 안 보임**
  - → **성능·비용·응용 동시 만족** 시 채택 가능

**c) 주요 Use-case**
- **AI Service = 가장 유력**: KV Cache spill 문제 해결, Storage 대비 성능 우위 분명
- IMDB향 **범용 서비스 확대 계획은 아직 없음** (IMDB는 가능성만, 확대 미정)

**d) 고용량 메모리 관점**
- AWS = High memory platform도 **속도·구성이 일반 서버와 동일 view**
- → **"용량만 확장"** 방향 유지 (성능 희생 없는 용량 확장)

### 2) Roadmap
- AWS **대규모 채택 가능성 낮음** — PoC 검증 단계 유지
- **KV Cache 문제 심화 시 CXL 재부상 가능** — 중장기 관점 관심 유지
- **고객 체감 명확한 TCO 개선 필요**

---

## ★★ 핵심 인사이트 — KV Cache thread 재정립 (자사 발의 축 기원)

> **본 02-10 AWS 미팅이 자사 발의 KV Cache 제안의 가장 이른 기록.** 이전 정리(NVIDIA 03-12 기원)에 더해, **자사가 먼저 고객에 제안한 평행 축**이 02-10에 존재.

**KV Cache CXL thread = 두 개 평행 축**:
1. **자사 발의 축**: AWS 02-10(중간 Tier 제안) → MSFT 04-30(CXL DM Pooling 제안). 자사가 고객에 먼저 제안.
2. **NVIDIA 발의 축**: NVIDIA 03-12(FMTA 질의) → NVIDIA 08-11(관심 전환). NVIDIA가 자사에 먼저 질의.

- 02-10 자사 AWS 제안(중간 Tier, KV Cache spill) ↔ 04-30 자사 MSFT 제안(CXL DM Pooling, SSD/RDMA 비교) — 동일 자사 발의 패턴, 2개월 간격.
- 02-10 "KV Cache 폭증 + Storage spillover 성능 급락" = 이후 모든 KV Cache 논의의 공통 배경 (MSFT 04-30, NVIDIA 03-12·08-11).

---

## 후속 액션 / 미해결

- [ ] **명확한 Killer Use case** 정의 (AWS 제약 — "안 보임" 해소)
- [ ] Latency 증가 완화 방안 (CXL 중간 Tier 성능 검증)
- [ ] Memory tier 관리 복잡성 해소 (SW)
- [ ] **1DPC 선호** 대응 (CXL 구성 옵션)
- [ ] 성능·비용·응용 3축 동시 만족 시나리오 구체화
- [ ] 명확한 TCO 개선 수치 (고객 체감)
- [ ] AI Service Use-case 구체화 (KV Cache spill 해결 정량)

## 관련 — KV Cache thread 시계열 (★ 재정립)

- **2026-02-10 (본 미팅, 자사 발의 축 기원)**: 자사가 AWS에 CXL Memory 중간 Tier 제안 (KV Cache spill 해결). 자사 발의 KV Cache 제안의 가장 이른 기록.
- 2026-03-12 FMTA: [2026-03-12-fmta-cxl.md](2026-03-12-fmta-cxl.md) — NVIDIA가 자사에 KV Cache 의견 질의 (NVIDIA 발의 축 기원).
- 2026-04-30 MSFT: [2026-04-30-msft-cxl-kv-cache.md](2026-04-30-msft-cxl-kv-cache.md) — 자사가 MSFT에 CXL DM Pooling 제안 (자사 발의 축, 본 02-10 AWS 제안의 연장).
- 2026-08-11 풀링: [2026-08-11-cxl-pooling.md](2026-08-11-cxl-pooling.md) — NVIDIA KV cache CXL 관심 전환(★★★). 두 축이 08-11에서 수렴.
- by-customer: [aws.md](../by-customer/aws.md)

## 관련 — 폼팩터 / IMDB thread

- 02-10 AWS "1DPC 선호" + "용량만 확장" ↔ 02-12 HPE "IMDB 고객 Main:CXL=1:1 + E3.S slot/PCIe lane 제약 → CMM x4" ↔ 04-30 MSFT "AIC 표준FF 유연성" ↔ 03-11 Oracle "AIC 너무 큼". AWS 1DPC 선호 = 폼팩터 thread 신규 축 (단일 구성 선호 = 고밀도 다 module 구성보다 1DPC).
- 02-10 "IMDB 범용 서비스 확대 계획 아직 없음" ↔ 02-12 HPE "IMDB NVMe→CXL 성능+용량 우수". IMDB use case = HPE 긍정 ↔ AWS 보수.
