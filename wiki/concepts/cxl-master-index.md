---
title: CXL 마스터 인덱스 — 전체 카테고리 및 서사 매핑
created: 2026-08-21
updated: 2026-08-21
tags: [cxl, master-index, taxonomy, summary, sk-hynix, next-gen]
---

CXL(Compute Express Link) 관련 모든 서사를 카테고리별로 정리한
**단일 진입점 페이지**.

> **사용법**: 이 페이지를 먼저 읽고 관심 카테고리로 들어가세요.
> 각 카테고리의 요약 + 관련 파일 링크를 제공합니다.

---

## 전체 구조

```
wiki/concepts/cxl-master-index.md ← 이 파일 (진입점)
│
├── 1. 프레임워크 & 개념 정의
├── 2. GPU Direct Memory (Dynamo · NIXL · CUDA)
├── 3. CXL 일간 업데이트 (Daily Update)
├── 4. 일일 리포트 (HTML)
├── 5. 고객 미팅 Intelligence
├── 6. 뉴스룸 수집 & 조사
├── 7. 상품기획 DRAFT & 프로젝트
├── 8. 관련 개념 (CXL 간접 언급)
└── 9. 핵심 인사이트 요약 (전 카테고리 통합)
```

---

## 1. 프레임워크 & 개념 정의 (Framework & Definitions)

CXL 기술의 기본 개념, 표준화 현황, SK하이닉스 밸류에이션과의 연관성.

### 1-1. CXL & 차세대 메모리 트랙

- **파일**: [cxl-next-gen-memory.md](cxl-next-gen-memory.md)
- **작성일**: 2026-07-24 (최종수정 2026-08-06)
- **역할**: CXL 트랙의 **최상위 정의 페이지** — 왜 추적하는지, 추적 프레임,
  표준화/AI 산업 이벤트/CXMT 경쟁사/컨트롤러 벤더/하이퍼스케일러/컨소시엄 6대 카테고리
- **핵심**: "HBM은 이미 시장이 반영, CXL은 초기 단계 — 다음 촉매 후보"
- **중요 개념**:
  - CXL = CPU-메모리 인터커넥트 표준, 메모리 풀링·가상화 가능
  - SK하이닉스의 CXL 컨트롤러/모듈 자사화 진행률이 HBM 이후 두 번째 성장 엔진
  - Daily Update → DRAFT v1.2 → CXL Newsroom Report → Deep Dive 코너 → 메인 리포트

### 1-2. AI 패브릭 3-way 경쟁과 CXL의 레이어 분담

- **파일**: [ai-fabric-3way-rivalry-and-cxl-layer.md](ai-fabric-3way-rivalry-and-cxl-layer.md)
- **작성일**: 2026-08-04
- **역할**: UALink/NVLink/Ultra Ethernet vs CXL 4.0 비교
- **핵심 결론**: **다른 레이어다** — 경쟁이 아니라 공존·보완
  - NVLink/UALink/UEC = GPU/XPU **스케일업·스케일아웃 패브릭**
  - CXL 4.0 = **메모리 풀링/disaggregation 레이어**

---

## 2. GPU Direct Memory (Dynamo · NIXL · CUDA Direct CXL)

### 2-1. CXL GPU Direct Memory 아키텍처

- **파일**: [cxl-gpu-direct-memory.md](cxl-gpu-direct-memory.md)
- **작성일**: 2026-08-21 (신규)
- **역할**: GPU ↔ CXL 메모리 direct 연결의 **전체 스택 분석**
- **핵심 내용**:
  - **Dynamo**: 오케스트레이터 (offloading, KV cache 관리) — CXL 직접 지원 아님
  - **NIXL**: NVIDIA Inference Xfer Library (전송 레이어) — GPU↔CXL 고속 전송
  - **CUDA Direct CXL**: 물리적 direct 접근 가능하게 하는 드라이버/OS 기능
  - **CXL Shared Memory Library**: SW stack — 공유 메모리 추상화
  - **CXL 2.0 vs 3.0**: Directed TLP 기능 추가 (GPU ↔ CXL 직접 라우팅 가능)
  - **3 층 모두 필요**: SW stack + CUDA Direct CXL + CXL 3.0
  - **Overhead 분석**: cudaMemcpy, lock, allocator, latency — 모두 분석됨
- **핵심 결론**:
  > Dynamo 는 CXL 을 직접 타겟팅하지 않음.
  > CXL 메모리가 OS 에 투명하게 맵핑되면 우연히 포함될 수 있지만 보장 X.
  > GPU→CXL Direct 는 CPU DMA 경유가 필수 (현재 상용 GPU 는 CXL 네이티브 아님).

### 2-2. 관련: GPU Inference Economics

- **파일**: [../reference/gpu-inference-economics.md](reference/gpu-inference-economics.md)
- **역할**: H100/B200/B300 스펙 검증 — TFLOPS/POPS, HBM 용량/대역폭, TDP
- **연계**: CXL offloading 의 물리적 기반 (GPU ↔ 메모리 대역폭)

---

## 3. CXL 일간 업데이트 (Daily Update)

매일 발행되는 CXL 뉴스 delta 요약. 2026-08-04 ~ 2026-08-21.

### 업데이트 로그

| 번호 | 날짜 | 카테고리 | Delta | 주요 신호 |
|---|---|---|---|---|
| 1호 | 08-04 | 12카테고리 전수 | 7건 | DRAFT v0.5 시작 |
| 2호 | 08-06 | 12카테고리 전수 | 8건 | Montage CXL 3.2, FMS 2026 하드웨어 |
| 3호 | 08-10 (구) | 8건 | SK Hynix ₩54.3T 팹, hyperscaler $595B CapEx |
| 4호 | 08-10 | 7-layer 개정 | 5건 | Samsung HBM4 수율 80%, Meta CXL 풀링, Winbond/Adata |
| 5호 | 08-12 | | SK Hynix 노사분쟁 중단, Intel CEO pet project, AMD MI350X |
| 6호 | 08-14 | | AMD MI350X 512GB HBM3e, Intel GPU 메모리, SK Hynix 노사재개 |
| 7호 | 08-15 | | SK Hynix 노사재개, Meta CXL 3.2 |
| 8호 | 08-16 | | Meta CXL 3.2, Samsung HBM 수율, SK Hynix 노사재개, Meta CXL 디코디 |
| 9호 | 08-18 | | Samsung Foundry +15%, AMD TPU H200, CXL 메모리 풀링 |
| 10호 | 08-19 | | AMD Q2 2026 Data Center 2배 급성장, Intel CEO 새 메모리 아키텍처, Samsung/SK Hynix H1 CapEx +35% |
| 11호 | 08-20 | | Samsung foundry +15%, Google AMD TPU H200, Coherent SiC |
| 11호-b | 08-20 (재조사) | | AMD MI455X 432GB HBM4 23.3TB/s ★★, TrendForce AI 5배, CXL 9,600TB/rack |
| 12호 | 08-21 | | 최신 (매일 갱신) |

### 파일 목록

- [cxl-daily-update-2026-08-04.md](../daily-updates/cxl-daily-update-2026-08-04.md)
- [cxl-daily-update-2026-08-06.md](../daily-updates/cxl-daily-update-2026-08-06.md)
- [cxl-daily-update-2026-08-12.md](../daily-updates/cxl-daily-update-2026-08-12.md)
- [cxl-daily-update-2026-08-14.md](../daily-updates/cxl-daily-update-2026-08-14.md)
- [cxl-daily-update-2026-08-15.md](../daily-updates/cxl-daily-update-2026-08-15.md)
- [cxl-daily-update-2026-08-16.md](../daily-updates/cxl-daily-update-2026-08-16.md)
- [cxl-daily-update-2026-08-18.md](../daily-updates/cxl-daily-update-2026-08-18.md)
- [cxl-daily-update-2026-08-19.md](../daily-updates/cxl-daily-update-2026-08-19.md)
- [cxl-daily-update-2026-08-20.md](../daily-updates/cxl-daily-update-2026-08-20.md)
- [cxl-daily-update-2026-08-20b.md](../daily-updates/cxl-daily-update-2026-08-20b.md)
- [cxl-daily-update-2026-08-21.md](../daily-updates/cxl-daily-update-2026-08-21.md)

### 구조 설명

**Full-Stack 7-Layer 개정** (4호부터 적용):

```
Daily Update 1호
  ↓ delta 누적 반영
DRAFT v1.0 → v1.2
  ↓
CXL Newsroom Report (매주 1회)
  ↓
Daily Brief Deep Dive 코너 (매일 메인 리포트 하단)
```

---

## 4. 일일 리포트 (HTML)

DRAFT v1.0+ 기반의 경영진용 HTML 리포트.

| 날짜 | 파일 |
|---|---|
| 08-04 | [cxl-daily-report-2026-08-04-0926.html](../cxl-daily-report-2026-08-04-0926.html) |
| 08-06 | [cxl-daily-report-2026-08-06-0240.html](../cxl-daily-report-2026-08-06-0240.html) |
| 08-10 | [cxl-daily-report-2026-08-10-0730.html](../cxl-daily-report-2026-08-10-0730.html) |
| 08-12 | [cxl-daily-report-2026-08-12-0640.html](../cxl-daily-report-2026-08-12-0640.html) |
| 08-14 | [cxl-daily-report-2026-08-14-2030.html](../cxl-daily-report-2026-08-14-2030.html) |
| 08-15 | [cxl-daily-report-2026-08-15-0630.html](../cxl-daily-report-2026-08-15-0630.html) |
| 08-16 | [cxl-daily-report-2026-08-16-0630.html](../cxl-daily-report-2026-08-16-0630.html) |
| 08-18 | [cxl-daily-report-2026-08-18-1900.html](../cxl-daily-report-2026-08-18-1900.html) |
| 08-19 | [cxl-daily-report-2026-08-19-0400.html](../cxl-daily-report-2026-08-19-0400.html) |
| 08-20 | [cxl-daily-report-2026-08-20-0737.html](../cxl-daily-report-2026-08-20-0737.html) |
| 08-21 | [cxl-daily-report-2026-08-21-0700.html](../cxl-daily-report-2026-08-21-0700.html) |
| 08-21 | [cxl-daily-report-2026-08-21-0742.html](../cxl-daily-report-2026-08-21-0742.html) |

> 4호(full-stack 7-layer 개정)부터 품질 기준 변경. 3호 이전은 구 구조로 4호로 대체됨.

---

## 5. 고객 미팅 Intelligence (Customer Meetings — CXL 관련)

CXL 관련 주제가 다뤄진 고객 미팅 기록. 총 9개 미팅 파일.

### 5-1. 미팅 로그

| 날짜 | 고객 | 주제 | 파일 |
|---|---|---|---|
| 01-15 | Lenovo | CXL CMM (Compute Memory Module) | [2026-01-15-lenovo-cxl-cmm.md](../customer-meetings/meetings/2026-01-15-lenovo-cxl-cmm.md) |
| 02-10 | AWS | CXL KV Cache | [2026-02-10-aws-cxl-kv-cache.md](../customer-meetings/meetings/2026-02-10-aws-cxl-kv-cache.md) |
| 02-12 | HPE | CXL EVB (Engineering Validation Board) | [2026-02-12-hpe-cxl-evb.md](../customer-meetings/meetings/2026-02-12-hpe-cxl-evb.md) |
| 03-11 | Oracle | OCI CXL | [2026-03-11-oracle-oci-cxl.md](../customer-meetings/meetings/2026-03-11-oracle-oci-cxl.md) |
| 03-12 | FMTA | CXL | [2026-03-12-fmta-cxl.md](../customer-meetings/meetings/2026-03-12-fmta-cxl.md) |
| 04-30 | Microsoft | CXL KV Cache | [2026-04-30-msft-cxl-kv-cache.md](../customer-meetings/meetings/2026-04-30-msft-cxl-kv-cache.md) |
| 05-07 | HPE | CXL Gen2 | [2026-05-07-hpe-cxl-gen2.md](../customer-meetings/meetings/2026-05-07-hpe-cxl-gen2.md) |
| 05-27 | Dell | TDF CXL NextGen | [2026-05-27-dell-tdf-cxl-nextgen.md](../customer-meetings/meetings/2026-05-27-dell-tdf-cxl-nextgen.md) |
| 08-11 | (그룹) | CXL Pooling | [2026-08-11-cxl-pooling.md](../customer-meetings/meetings/2026-08-11-cxl-pooling.md) |

### 5-2. 관련 고객 프로필

| 고객 | CXL 관련성 | 파일 |
|---|---|---|
| AWS | CXL KV Cache — 하이퍼스케일러 CXL 채택 선도 | [aws.md](../customer-meetings/by-customer/aws.md) |
| HPE | CXL EVB/Gen2 — CXL 하드웨어 검증 보드 | [hpe.md](../customer-meetings/by-customer/hpe.md) |
| Microsoft | CXL KV Cache — Azure HPC | [msft.md](../customer-meetings/by-customer/msft.md) |
| Oracle | OCI CXL — 데이터센터 메모리 확장 | [oracle.md](../customer-meetings/by-customer/oracle.md) |
| Dell | TDF (Thermal Design Force) CXL — 차세대 CXL | [dell.md](../customer-meetings/by-customer/dell.md) |
| Lenovo | CXL CMM — 메모리 모듈 플랫폼 | [lenovo.md](../customer-meetings/by-customer/lenovo.md) |

---

## 6. 뉴스룸 수집 & 조사 (Newsroom)

### 6-1. CXL Ecosystem Newsroom Landscape

- **파일**: [cxl-newsroom-landscape.md](cxl-newsroom-landscape.md)
- **작성일**: 2026-08-10
- **역할**: 30개 CXL 생태계 기업의 공식 newsroom 채널 전수 조사
- **핵심 결과**:
  - WebFetch 직접 수집 가능: 18/30
  - CXL 직접 신호 밀집: 9개사 (컨트롤러·IP·메모리·검사장비 벤더)
  - Host/Hyperscaler 9개사는 CXL 직접 언급 0건

### 6-2. CXL Newsroom 검색 방법론

- **파일**: [cxl-newsroom-search-methodology.md](cxl-newsroom-search-methodology.md)
- **역할**: Bing RSS (Tier 1) + IR 페이지 WebFetch (Tier 2) 검색 전략
- **핵심 규칙**: 한국 기업 = 한글 쿼리, 영어 기업 = 영문 쿼리

### 6-3. CXL Newsroom Report

- **파일**: [cxl-newsroom-report-2026-08-11-1200.md](../cxl-newsroom-report-2026-08-11-1200.md)
- **역할**: Newsroom 수집 결과를 정리한 주간 리포트

---

## 7. 상품기획 DRAFT & 프로젝트

### 7-1. 상품기획 DRAFT

- **파일**: [cxl-memory-product-planning-draft - 복사본.txt](cxl-memory-product-planning-draft%20-%20복사본.txt)
- **상태**: DRAFT v0.5 + 0장 (12장 구조)
- **내용**: 컨트롤러 벤더 7개 use case·pain point 매핑 → 신제품 컨셉 제언
- **참고**: 정규 .md 경로 현재 미존재, `.txt 복사본`만 있음 — 경로 복구 필요

### 7-2. 상품기획 프로젝트 핸드오프

- **파일**: [cxl-product-planning-session-handoff.md](cxl-product-planning-session-handoff.md)
- **작성일**: 2026-08-04
- **역할**: 다음 세션에서 "CXL 보고서 계속하자" 시 즉시 이어서 작업하기 위한
  세션 컨텍스트 저장

### 7-3. 상품기획 리포트

- **파일**: [cxl-memory-product-planning-report-2026-08-04-0906.html](../cxl-memory-product-planning-report-2026-08-04-0906.html)
- **역할**: 경영진용 HTML 리포트 (0장 포함)

---

## 8. 관련 개념 (CXL 간접 언급)

CXL 을 직접 다루지는 않지만 관련 맥락에서 언급된 개념.

| 개념 | 연관성 | 파일 |
|---|---|---|
| HBM Cycle Score | HBM → CXL 로의 확장 (차세대 메모리) | [hbm-cycle-score.md](hbm-cycle-score.md) |
| SK하이닉스 분석가 의견 | CXL 컨트롤러 자사화 진전률 | [sk-hynix-analyst-thesis-checkpoints.md](sk-hynix-analyst-thesis-checkpoints.md) |
| HBM4 공급 | HBM4 → HBM3E → CXL 메모리 연계 | [sk-hynix-analyst-thesis-checkpoints.md](sk-hynix-analyst-thesis-checkpoints.md) |
| GPU Inference Verification | GPU-Memory 대역폭 → CXL offloading 기반 | [gpu-inference-chart-verification.md](../reference/gpu-inference-chart-verification.md) |
| SK하이닉스 엔티티 | CXL 관련 투자/개발 현황 | [../entities/sk-hynix.md](../entities/sk-hynix.md) |

---

## 9. 핵심 인사이트 요약 (Cross-Category)

전 카테고리에서 도출된 공통 인사이트.

### 9-1. CXL 시장 상태

- **표준화**: CXL 3.2 발표, CXL 4.0 스펙, PCIe 7.0 연계 대역폭 확장 중
- **하이퍼스케일러 채택**: AWS/Microsoft/Google/Meta 모두 CXL KV Cache 실험 중
  - AWS, Microsoft: KV Cache offload 목적 (메모리 비용 절감)
  - Meta: CXL 메모리 풀링 (실제 디코딩 워크로드 적용)
- **SK하이닉스**: CXL 컨트롤러/모듈 자사화 진행 중 — HBM 이후 두 번째 성장 엔진

### 9-2. SK하이닉스 밸류에이션 관점

| 항목 | 상태 | 신호 |
|---|---|---|
| HBM | 시장 반영 완료 | 멀티플 상승 제한 |
| CXL 컨트롤러/모듈 | 초기 단계 | **다음 촉매**, 자사화 진행률 확인 필요 |
| 노사분쟁 | 08-12 중단, 08-14 재개 | ⚠️ 단기 리스크 |
| CapEx | 1H +35% YoY | ✅ 긍정적 |

### 9-3. 기술적 인사이트

| 질문 | 결론 |
|---|---|
| GPU ↔ CXL Direct 가능? | ❌ CPU DMA 경유 필수 (현재) |
| CXL 3.0 Directed TLP 로 해결? | ⚠️ GPU 가 CXL 네이티브여야 함 (현재 미지원) |
| Dynamo 가 CXL 지원? | ❌ CPU RAM + SSD 만 표기, CXL 우연 포함 가능 |
| SW stack 이 offload 관리? | ✅ CXL Shared Memory Library 가 추상화 관리 |
| Overhead 는? | ⚠️ 있음 — cudaMemcpy, lock, allocator, latency |

### 9-4. CXL 컨트롤러 벤더 7개 핵심

| 벤더 | 포지션 | AI/LLM 강조 |
|---|---|---|
| Panmnesia | Switch/Retimer/Endpoint/IP | 매우 강함 |
| Marvell | Memory controller/Switch/Near-mem | 강함 |
| Astera Labs | Switch/Retimer/Memory controller | 매우 강함 |
| Montage | MXC Controller/Jintide | 강함 |
| Microchip | SMC 2000/2100/Retimer | 강함 |
| ScaleFlux | MC500/MC600/FC6116 | 매우 강함 (KV cache) |
| Rambus/Synopsys | Controller IP | 강함 |

---

## 파일 통계

| 카테고리 | 파일 수 |
|---|---|
| 개념 정의 (Framework) | 2 |
| GPU Direct Memory | 2 |
| Daily Update (MD) | 11 |
| 일일 리포트 (HTML) | 12 |
| 고객 미팅 (CXL) | 9 |
| 뉴스룸 조사 | 3 |
| 상품기획 (DRAFT/프로젝트) | 3 |
| 관련 개념 | 5 |
| **합계** | **47** |

---

**생성일**: 2026-08-21
**검증**: 모든 CXL 관련 파일 탐색 완료 (105개 파일에서 47개 관련 파일 매핑)
**다음 작업**: 필요시 카테고리별 심화 요약 생성
