---
title: "IBM (International Business Machines) — Power Future CXL"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer, ibm, power, sap-hana, imdb, kv-cache, form-factor, hmsdk, pqc]
entity: IBM
relation: customer
first_contact: 2026-02-06
meetings: 1
---

# IBM — Power Future CXL (customer)

> IBM Power 서버 차세대(Power Future @2028) CXL 적용. SAP HANA IMDB $/GB 절감 핵심 제안.
> 단일 출처(구병호 TL 작성 2026-02-06), 외부 교차검증 미수행.

---

## 현재 관계 상태 (2026-02-06 기준)

- **단계**: 이번 분기 내 CXL 적용 방식 결정 시점. 자사 제안 타이밍 임계.
- **핵심 제안**: SAP HANA IMDB **$/GB 절감** (BW보다 낮은 가격 대용량화). Power10 Cybertron/Ratchet OpenCAPI-to-CXL 어댑터 PoC 중 → **Power Future(@2028) 최초 Native-CXL 2.0**.
- **폼팩터**: 2028 High End = **x16 HHHL AIC only** → 2029 Mid Range/Scale Out = **HHHL AIC + E3.S 2T** (512GB+ via EDSFF 슬롯).
- **용량 갭**: HHHL AIC 한계 256GB vs IBM 기대 512GB+ → 자사 **LPD5/FHHL cover 전략 검토**.
- **Latency**: 자사 2nd Gen 300ns → **IBM 목표 200~250ns** (Switch-based, 국내 IP·스위치 공급사와 평가 중).
- **Pooling**: IBM 직접 개발 안 함 → 외부 업체 PoC, 2028~2029 외부 appliance 도입 가능성 높음.
- **HMSDK**: 관심 표명 → 추가 정보 제공 시 내부 팀 논의. SW 협력 가능성.
- **ES 타이밍**: 자사 12월@'26 ES = Power Future 평가 시작 align.
- **상태**: PoC/검토 단계, Action 4건(지연시간·HHHL 고용량·PQC·HMSDK) 대기.

---

## 핵심 팩트 (누적)

### 제품 / 로드맵
- **Power Future** = IBM Power 차세대 하이엔드, **2028 출시 예정**.
- 2028 Power Future = PCIe Gen 5 → **CXL 2.0** (IBM Power 라인업 **최초 Native-CXL**).
- 이전: Power10에서 Cybertron/Ratchet **OpenCAPI-to-CXL 어댑터 카드** PoC (Native 아님).
- **이번 분기 내 CXL 적용 방식 결정** 시점.

### Use Case
- **SAP HANA IMDB** $/GB 절감 = 핵심. vPMEM array 대역폭·지연·용량 충족.
- CXL = **2nd tier memory** (Local main memory 보조).
- IBM-SAP 결합 강도 높음 (Gary: "Power 포트폴리오 전반 SAP 진입 높고 계속될 것") → CXL 도입 동인.
- **KV-Cache**: Gen6(차세대) 전제 "다른 기회" — 용량·대역폭 중요, NVMe 대비 워크로드 성능 향상. 2028(CXL 2.0)엔 Gen6 아님 → 장기 기회.

### 폼팩터
- **2028 High End**: x16 HHHL AIC only (~256GB).
- **2029 Mid Range/Scale Out**: HHHL AIC + x4/x8 E3.S 2T (EDSFF 슬롯 → 512GB+).
- **IBM 특이점**: AIC에서 출발 (Oracle 03-11 "AIC 너무 큼"과 대조) → 2029 E3.S 2T 확장은 Dell/HPE 옹호 방향 일치.
- 자사 대응: **LPD5 + FHHL cover 전략 검토** (HHHL 고용량 갭 회피).

### 성능 / TCO
- Latency: 자사 2nd Gen 300ns → IBM 목표 **200~250ns**.
- Bandwidth: 2nd Gen CMM 최대 80GB/s, 절반 동작 수준 (PCIe 5.0 한계).
- **TCO**: 속도 낮춰 TCO 개선 검토 + 2nd Tier 용량·비용 균형. $/GB 절감 = 핵심 제안.
- TCO thread **6개 고객** 중 하나 (AWS·Oracle·MSFT·Dell·HPE·IBM).

### Pooling / Appliance
- IBM 직접 풀링 개발 안 함 → 외부 업체 PoC.
- 2028~2029 **외부 appliance 도입 가능성 높음** (CXL 어플라이언스 막 검토 시작).
- → 자사 CMM Appliance / 파트너 appliance 경쟁 기회.

### SW / HMSDK
- 자사 HMSDK(Linux 커널 contribution, Meta 협력 AI Workload) → **IBM 내부 검토 중, 추가 정보 요청**.
- Action 4: HMSDK 상세 문서·커널 기여 내용 공유.

### 보안 / PQC
- PQC(Post-Quantum Cryptography) 계획: 참석자 모름 → IBM 보안 담당자 확인 후 공유 예정.
- HPE 05-07 "유럽 Dec'27 PQC FU 필수"와 맥락 유사 (보안 규제 대응 트렌드).

### 참석자
- SK hynix: 심응보 팀장, 전선광 TL, 구병호 TL, DK Park TL
- IBM: Patrick Breen, David Cadigan, Gary

---

## Follow-up Actions (대기)

- [ ] Action 1: 풀링 지연 시간 200~250ns 개선 계획 공유
- [ ] Action 2: HHHL 폼팩터 고용량(LPD) 적용 계획 공유
- [ ] Action 3: PQC 보안 상세 스펙·적용 계획 공유 (장표)
- [ ] Action 4: HMSDK 상세 문서·Linux 커널 기여 내용 공유 (장표)

---

## 미팅 이력 (역순)

### ★ 2026-02-06 — IBM Power Future CXL 미팅 ★★★ (최초, 말뭉치 내 최초 미팅)

- **전문**: [meetings/2026-02-06-ibm-power-future.md](../meetings/2026-02-06-ibm-power-future.md)
- **참석**: SK hynix(심응보 팀장·전선광 TL·구병호 TL·DK Park TL) / IBM(Patrick Breen·David Cadigan·Gary)
- **핵심**: Power Future(@2028) 최초 Native-CXL 2.0. SAP HANA IMDB $/GB 절감. 2028 AIC only → 2029 AIC+E3.S 2T. HHHL 256GB 갭 → LPD5/FHHL 검토. Latency 300→200~250ns. **KV-Cache "다른 기회" 독립 인지(Gen6 전제)**. HMSDK 관심. ES 12월@'26 align.
- **DRAFT 연결**: 7장 Main Memory(2nd tier $/GB) · 9장 KV offload(Gen6 KV-Cache 기회, 자사 발의/NVIDIA 발의 축과 별개 독립 인지) · 11장 시장 인텔리전스(IBM Power CXL) · 5장 CPU/IBM Power.
