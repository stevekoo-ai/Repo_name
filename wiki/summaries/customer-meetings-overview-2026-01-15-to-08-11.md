---
title: "Customer-Meetings Overview — 11개 미팅 수집 완료 (2026-01-15 ~ 2026-08-11)"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, dram, customer-meeting, summary, overview, intelligence]
---

# Customer-Meetings Overview — 11개 미팅 수집 완료

> 2026-01-15 ~ 2026-08-11 (약 7개월) 수집된 1차 현장 인텔리전스 11개 미팅의
> 시계열·고객별·thread별 매트릭스. 이벤트/관찰 레벨 기록 (knowledge-model Summary).
> 재사용 가능한 운영 패턴은 [concepts/customer-meetings-intelligence.md](../concepts/customer-meetings-intelligence.md),
> thread별 현재 상태 추적은 [monitoring/customer-meetings-thread-tracker-status.md](../monitoring/customer-meetings-thread-tracker-status.md),
> 전문·상대방별 누적은 [customer-meetings/](../customer-meetings/).

---

## 1. 시계열 (11개 미팅, 최신→과거)

| # | 날짜 | 미팅 | 고객(주) | 유형 | 비고 |
|---|------|------|----------|------|------|
| 1 | 2026-08-11 | CXL 메모리 풀링 | MSFT·Oracle·NVIDIA + 파트너7·경쟁3 | CXL | Neo-Cloud, NVIDIA KV cache 전환 |
| 2 | 2026-05-27 | Dell TDF CXL Next Gen | Dell | CXL | AIC vs E3, CMM AX(Marvell+Xcena) |
| 3 | 2026-05-07 | HPE CXL Gen2 | HPE | CXL | E3.S 주, Gen2=Montage, Venice 2027-06 |
| 4 | 2026-04-30 | MSFT CXL KV Cache | MSFT | CXL | 자사 발의 KV Cache 제안(Phyllis) |
| 5 | 2026-03-12 | FMTA CXL | NVIDIA | CXL | NVIDIA 발의 KV Cache 질의 기원 |
| 6 | 2026-03-11 | Oracle OCI CXL Pooling | Oracle | CXL | Switch 경쟁, HA, AIC 너무 큼 |
| 7 | 2026-02-12 | HPE CXL EVB / Gen13 Venice | HPE | CXL | HPE 기원, Venice Post-Launch, MRDIMM+CXL |
| 8 | 2026-02-10 | AWS CXL KV Cache 중간 Tier | AWS | CXL | 자사 발의 KV Cache 축 기원, 1DPC |
| 9 | 2026-02-06 | IBM Power Future | IBM | CXL | Native-CXL 2.0, KV-Cache 독립 인지 |
| 10 | 2026-02-05 | Google DRAM/MRDIMM | Google | **DRAM(비-CXL)** | 첫 비-CXL, Venice MRD 필수, Intel DMR |
| 11 | 2026-01-15 | Lenovo CXL CMM | Lenovo | CXL | 말뭉치 최초, CMM 가격>RDIMM, 3rd Gen FF |

**총 11개**: CXL 10건 + DRAM 1건(Google). **말뭉치 최초** = Lenovo 01-15.

---

## 2. 고객별 (customer 8명 + partner 11 + competitor 4 = 23 by-customer 페이지)

### customer (8명)
| 고객 | 미팅수 | 최초 접촉 | 핵심 |
|------|--------|----------|------|
| Lenovo | 1 | 2026-01-15 | CMM 가격>RDIMM→sales 부진, 컨트롤러 지연, 3rd Gen FF |
| Google | 1 | 2026-02-05 | DRAM 로드맵(비-CXL), Venice MRD 필수, Intel DMR 48→64GB, PRAC 미지원 |
| IBM | 1 | 2026-02-06 | Power Future Native-CXL 2.0, SAP HANA IMDB $/GB, KV-Cache 독립 인지 |
| AWS | 1 | 2026-02-10 | 자사 발의 KV Cache 중간 Tier, 1DPC, Killer Use case 안 보임 |
| HPE | 2 | 2026-02-12 | HPE 기원(EVB→Gen2), Venice Post-Launch→2027-06, MRDIMM+CXL |
| Oracle | 2 | 2026-03-11 | Switch 경쟁, HA, AIC 너무 큼→Sang Park 이직으로 반전 |
| NVIDIA | 2 | 2026-03-12 | NVIDIA 발의 KV Cache 질의→08-11 관심 전환 |
| MSFT | 2 | 2026-04-30 | pathfinding, KV Cache 제안(자사 발의)→Pooled Appliance |
| Dell | 1 | 2026-05-27 | AIC vs E3.L/S, CMM AX 공동개발, AI 풀링 전용 재설계 |

### partner (11) — 간접 등장 다수
Marvell(CMM AX 공동개발, switch 인수)·Xcena(CMM AX 공동개발)·Xconn(switch, 인수 대상)·Liqid·Intel(DMR/EMR/Ghostfish)·AMD(Venice/ARM4/Florence, 12→16ch)·Qualcomm·ScaleFlux·Panmnesia·Primemas·Penguin

### competitor (4)
Montage(MXC 시료생산, MHD HA)·Broadcom("switch 시장 없다")·Micron(Abaco 3.0)·Samsung(CXL3 PoC)·Kioxia

---

## 3. 교차 thread 매트릭스 (thread × 고객)

> 상세·현재 상태는 [monitoring/customer-meetings-thread-tracker-status.md](../monitoring/customer-meetings-thread-tracker-status.md).

| Thread | 관련 고객(날짜) | 상태 |
|--------|-----------------|------|
| **KV Cache CXL (3 출처)** | IBM(02-06 독립 인지)·AWS(02-10 자사 발의)·NVIDIA(03-12 발의)·MSFT(04-30·08-11) | 정정 4회 → 3출처 확정 |
| **TCO/가격 (7 고객)** | Lenovo(01-15 가격 장벽)·IBM(02-06 $/GB)·AWS(02-10)·Oracle(03-11 DIMM 수준)·MSFT(04-30)·HPE(05-07)·Dell(05-27) | 7고객 공통, Lenovo 가장 직접적 |
| **폼팩터 (7-way)** | Lenovo(01-15 3rd Gen FF)·IBM(02-06 AIC→E3.S 2T)·AWS(02-10 1DPC)·HPE(02-12 slot 제약)·Oracle(03-11 AIC 큼)·HPE(05-07 E3.S 주)·Dell(05-27 AIC vs E3) | 7-way, Oracle 가장 제약 강함 |
| **3rd Gen FF 전환기** | Lenovo(01-15)·IBM(02-06)·Dell(05-27) | 3고객 전환기 논의 |
| **CMM 컨트롤러 납기 지연** | Lenovo(01-15 공유 컨트롤러) + Marvell CMM AX/Montage MXC | 컨트롤러 IP 타이밍→샘플 일정 |
| **CXL switch 경쟁** | Oracle(03-11) + Marvell/Broadcom/Xconn | Marvell vs Broadcom vs Xconn |
| **AMD Venice 플랫폼 교차** | Google(02-05 DRAM MRD 필수)·HPE(02-12 CXL Post-Launch) | 동일 플랫폼 다른 페이즈 |
| **Intel DMR 플랫폼 교차** | Google(02-05 DRAM 48→64GB)·Intel(08-11 CXL Co-enabling) | DRAM→CXL 확장 |
| **MRDIMM** | Google(02-05 비-CXL)·HPE(02-12 CXL) | DRAM 단독 vs CXL 결합 |
| **IMDB/Memory sharing** | HPE(02-12)·MSFT(04-30)·Oracle(03-11)·IBM(02-06) | 4고객, IBM 가장 명시적 |
| **Local CXL 가치 훼손** | Oracle(03-11)·AMD(12→16ch 간접) | Local 부정≠Pooled 부정 |
| **Oracle HA/AIC 반전** | Oracle(03-11→08-11) | 담당자 이동→5개월 반전 |

---

## 4. 시계열 누적 정제 패턴 (KV Cache thread 기원 정정 4회)

> 이 패턴 자체를 재사용 가능 개념으로 정리: [concepts/customer-meetings-intelligence.md](../concepts/customer-meetings-intelligence.md) §시계열 누적 정제

| 정정 회차 | 기원 결론 | 발견 계기 |
|-----------|----------|----------|
| 1차 (MSFT 04-30 ingest) | MSFT 04-30 = 기원 | 최초 ingest |
| 2차 (FMTA 03-12 ingest) | NVIDIA 03-12 = 기원 (NVIDIA 먼저 질의) | 더 이른 미팅 발견 |
| 3차 (AWS 02-10 ingest) | 자사 발의(AWS 02-10) + NVIDIA 발의(03-12) 두 축 | 더 이른 자사 발의 발견 |
| 4차 (IBM 02-06 ingest) | + IBM 02-06 독립 인지(3번째 출처) | 더 이른 고객 인지 발견 |

**패턴**: 새 미팅이 기존 "기원" 결론을 번복하는 누적 정제. 2-tier 구조(meetings/ 단일 출처 + by-customer/ 누적)가 이를 가능케 함.

---

## 5. 분류 범위 확장 (첫 비-CXL 미팅)

- 2026-02-05 Google 미팅까지 9건은 전부 CXL. Google 10번째로 **첫 비-CXL(DRAM) 미팅** 추가.
- customer-meetings/ 2-tier 구조가 CXL뿐 아니라 DRAM DIMM 로드맵(RDIMM/MRDIMM/DDR5 PRAC/DDR6)까지 커버함 확인.
- README "고객·파트너 미팅 인텔리전스" 범위가 실제로 CXL+DRAM 모두 포함.

---

## 6. 데이터 한계 (공개 원칙)

- 11개 미팅 전부 **단일 출처**(구병호 TL 작성 8건 + 김의현 TL 1건 + 포럼 요약 2건). 외부 교차검증 미수행.
- 추정·정정은 각 by-customer/ 전문에 "(추정)"/"정정 이력" 명시.
- 상대방 직책 미기재 cases(Lenovo 4명 등)는 발언 부분 매핑만, 개별 직책 비매핑 명시.

---

## Related

- 전문·상대방별: [customer-meetings/](../customer-meetings/) (README + index + meetings/ + by-customer/)
- 운영 패턴(재사용 개념): [concepts/customer-meetings-intelligence.md](../concepts/customer-meetings-intelligence.md)
- thread별 현재 상태 추적: [monitoring/customer-meetings-thread-tracker-status.md](../monitoring/customer-meetings-thread-tracker-status.md)
- CXL 벤더 풍경도(웹 조사): [concepts/cxl-controller-vendor-landscape.md](../concepts/cxl-controller-vendor-landscape.md)
- CXL 트랙: [concepts/cxl-next-gen-memory.md](../concepts/cxl-next-gen-memory.md)
