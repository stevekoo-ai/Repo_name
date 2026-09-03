---
title: "IBM Power Future CXL 미팅 — 2026-02-06"
date: 2026-02-06
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, ibm, power, sap-hana, imdb, kv-cache, form-factor, hmsdk, pqc]
attendees:
  sk_hynix: ["심응보 팀장", "전선광 TL", "구병호 TL", "DK Park TL"]
  ibm: ["Patrick Breen", "David Cadigan", "Gary"]
source: sources/ibm-power-future-cxl-meeting-2026-02-06.md
relation: customer
significance: "★★★"
---

# IBM Power Future CXL 미팅 — 2026-02-06

> **현재 말뭉치 내 최초 미팅** (2026-02-06, AWS 02-10보다 4일 앞선).
> IBM Power 포트폴리오 차세대(Power Future @2028)에 CXL 적용 방식 이번 분기 내 결정 시점의 1차 현장 인텔리전스.
> 단일 출처(구병호 TL 작성), 외부 교차검증 미수행.

---

## 0. 핵심 요약 (8개)

| # | 핵심 | 영향도 |
|---|------|--------|
| 1 | **IBM Power Future(@2028) 최초 Native-CXL 2.0 지원** — 이번 분기 내 CXL 적용 방식 결정 시점 | ★★★ |
| 2 | **핵심 제안 = SAP HANA IMDB $/GB 절감** (BW보다 낮은 가격의 대용량화) — Power10에서 Cybertron/Ratchet OpenCAPI-to-CXL 어댑터 카드 PoC 중 | ★★★ |
| 3 | **폼팩터 로드맵 분리**: 2028 High End = **x16 HHHL AIC만** / 2029 Mid Range·Scale Out = **HHHL AIC + x4/x8 E3.S 2T 둘 다** (EDSFF 슬롯 확대 → 512GB+ 가능) | ★★★ |
| 4 | **HHHL AIC 용량 한계(256GB) vs IBM 기대(512GB+) 갭** → **LPD5/FHHL cover 전략 검토** (자사 대응) | ★★ |
| 5 | **Latency 300ns(자사 2nd Gen) → 200~250ns(IBM 목표)** — Switch-based latency 개선 요구, 국내 IP·스위치 공급사와 성능 평가 중 | ★★ |
| 6 | **KV-Cache = "다른 기회" 독립 인지** — Gen6 지원 시 KV-Cache 응용에서 용량·대역폭 중요, NVMe 대비 워크로드 성능 향상 → "이 분야에도 여전히 기회" (IBM 측 발언) | ★★★ |
| 7 | **TCO 관점**: 속도 낮춰 TCO 개선 가능성 검토 + 2nd Tier memory로 용량·비용 균형. 2nd Gen CMM 최대 80GB/s이나 절반 수준 동작 | ★★ |
| 8 | **HMSDK 관심** — 자사 CXL 메모리 관리 SW 스택(Linux 커널 contribution, Meta 협력 AI Workload) → IBM 내부 검토, 추가 정보 제공 시 내부 팀 논의 | ★★ |

---

## 1. 배경 — Power Future CXL 적용 결정 시점

- **Power Future** = IBM Power 서버 차세대 하이엔드 제품, **2028년 출시 예정**.
- **2028 Power Future = PCIe Gen 5 → CXL 2.0** 지원. IBM Power 라인업 **최초 Native-CXL** 도입.
- 현재 Power10에서는 **Cybertron/Ratchet OpenCAPI-to-CXL 어댑터 카드**로 PoC 테스트 중 (Native 아님).
- **이번 분기 내** CXL 적용 방식 결정해야 하는 시점 — 자사엔 샘플/스펙 제안 타이밍 임계.

---

## 2. 핵심 제안 — SAP HANA IMDB $/GB 절감

- IBM Power의 CXL 목적 = **SAP HANA 및 기타 application에 대해 $/GB를 낮춘 POWER system 제공**.
- BW 측면보다 **낮은 가격의 대용량화** 방향. CXL = **2nd tier memory** (Local main memory 보조).
- SAP HANA = **IMDB(In-Memory DB)** 과제. vPMEM array 요구 대역폭·지연·용량 충족 필요.
- Gary: "IBM Power 포트폴리오 전반에 걸쳐 SAP에 높은 수준으로 진입되어 있고 이후도 계속될 것" — **IBM-SAP 결합 강도 = CXL 도입 동인**.

---

## 3. 폼팩터 로드맵 (2028 vs 2029 분리) ★★★

| 시점 | 제품 | 지원 폼팩터 | 용량 한계 |
|------|------|------------|----------|
| 2028 (High End) | Power Future 초기 release | **x16 HHHL AIC only** | ~256GB (size 한계) |
| 2029 (Mid Range / Scale Out) | 후속 release | **HHHL AIC + x4/x8 E3.S 2T** (둘 다) | EDSFF 슬롯 확대 → **512GB+** 가능 |

- **갭 인식**: IBM은 512GB+ 기대하나 HHHL AIC는 256GB 한계 → **고민 포인트**.
- **자사 대응**: **LPD5 + FHHL cover 전략 검토 중** (HHHL 고용량 회피 경로).
- 2029 E3.S 2T 추가 = EDSFF 슬롯 확대 전제 → Oracle/Dell의 E3.S 옹호와 같은 방향. 단 IBM은 2028엔 AIC only (Oracle 03-11 "AIC 너무 큼"과 대조 — IBM은 AIC에서 출발).

---

## 4. Latency / Bandwidth / TCO

- **Latency**: 자사 2nd Gen = 300ns. **IBM 목표 = 200~250ns** (Switch-based에서 latency 축소 관심).
  - 국내 IP 및 스위치 공급사와 협력 성능 평가 중.
- **Bandwidth**: 2nd Gen CMM 최대 80GB/s, 절반 정도 동작 수준. IBM POWER = CXL 2.0 PCIe 5.0 한계.
- **TCO 관점 (2 방향)**:
  - (a) SAP HANA 지원 위해 일정 대역폭 필요 — 단 PCIe 5.0 한계로 절반 동작.
  - (b) **속도 낮춰 TCO 개선** 가능성 검토 — 2nd Tier memory로 용량·비용 균형.
- **Gen6 케이스 = 별개 기회** (아래 §5).

---

## 5. ★★★ KV-Cache "다른 기회" 독립 인지

> **KV Cache CXL thread의 세 번째 독립 출현** — 자사 발의(AWS 02-10)/NVIDIA 발의(03-12)와는 별개로 **IBM이 고객 측에서 독립적으로 KV-Cache 기회 인지**.

- "Gen6 지원 가능한 케이스에서 **KV-Cache 같은 응용**에서 용량과 대역폭이 매우 중요한 **다른 기회**가 있고"
- "지연 시간 측면에서 NVMe보다 워크로드 성능을 크게 향상시켜 줄 수 있어 **이 분야에도 여전히 기회**가 있다고 생각함"
- 단 2028 Power Future(CXL 2.0/PCIe 5.0)에는 Gen6 아님 — **KV-Cache 기회는 Gen6(차세대) 전제의 장기 기회**. 2028 SAP HANA IMDB가 근기 applied use case.
- **의미**: KV Cache가 자사·NVIDIA 양 축 외에 **고객(IBM) 측에서도 독립적으로 인지된 기회** → 배경 인식의 보편성 확인. AWS 02-10 "Storage spillover 성능 급락" 명시보다 4일 앞선 **가장 이른 KV Cache 기회 언급 기록**.

---

## 6. PQC / Pooling / HMSDK

- **PQC(Post-Quantum Cryptography)**: 참석자들 정확한 계획 모름 → IBM 보안 담당자에게 확인 후 공유 예정. (HPE 05-07 "유럽 Dec'27 PQC FU 필수"와 맥락 유사 — 보안 규제 대응.)
- **CXL Memory Pooling**: IBM 직접 개발 안 함 → **외부 업체와 PoC 진행 중, 2028~2029 외부 appliance 도입 가능성 높음**. (CXL 어플라이언스 도입도 막 검토 시작.)
- **HMSDK**: 자사 CXL 메모리 관리 SW 스택(Linux 커널 contribution, Meta 협력 AI Workload 최적화). IBM 내부 검토 중 → **추가 정보 제공 시 내부 팀과 논의**. SW 측면 협력 가능성.

---

## 7. 샘플 공급 Align

- 자사 **ES 12월@'26 공급 계획** = Power Future 평가 시작 시점과 **잘 align**되어 있다고 함.
- 2028 출시 → 2026-12 ES → 2027 평가 → 2028 GA 경로. 자사 ES 타이밍 적절.

---

## 8. Action Items

| # | Action | 목표/내용 |
|---|--------|----------|
| 1 | CXL 풀링 시스템 **지연 시간 개선 계획 공유** | 200~250ns 목표 |
| 2 | **HHHL 폼팩터 고용량 적용 계획** 공유 update | LPD 적용 전략 |
| 3 | **PQC 보안 기능 상세 스펙 및 적용 계획** 공유 | 미팅 장표 공유 |
| 4 | **HMSDK 상세 문서 및 Linux 커널 기여 내용** 공유 | 미팅 장표 공유 |

---

## Follow-up Actions

- [ ] Action 1: 풀링 지연 시간 200~250ns 개선 계획 자사 준비 → IBM 공유
- [ ] Action 2: HHHL 고용량(LPD5/FHHL) 전략 정리 → IBM 공유
- [ ] Action 3: PQC 보안 스펙 장표 준비 → IBM 보안 담당자 확인 후 공유
- [ ] Action 4: HMSDK 상세 문서 + Linux 커널 기여 내용 장표 → IBM 내부 팀 논의 지원
- [ ] 후속 미팅: 이번 분기 내 CXL 적용 방식 결정 → 자사 제안 타이밍 임계

---

## Related

- 상대방별 누적: [by-customer/ibm.md](../by-customer/ibm.md)
- KV Cache thread (두 평행 축 + IBM 독립 인지): [index.md §3](../index.md)
- 폼팩터 thread (HHHL AIC + E3.S 2T 분리 로드맵 추가): [index.md §3](../index.md)
- TCO thread (6개 고객 확장): [index.md §3](../index.md)
- IMDB use case thread (HPE 02-12 + MSFT 04-30 + Oracle 03-11 + IBM 02-06): [index.md §3](../index.md)
- 관련 미팅 (시계열): AWS 02-10(자사 발의 KV Cache 축 기원) · HPE 02-12(HPE 기원, 6일 후) · FMTA 03-12(NVIDIA 발의 축)

---

## Timeline 교차 (현재까지 최초 미팅)

| 날짜 | 미팅 | 본 미팅과의 관계 |
|------|------|------------------|
| **2026-02-06** | **IBM Power Future (본 미팅)** | **말뭉치 최초**. KV Cache 독립 인지, AIC→E3.S 2T 분리 로드맵, HMSDK 관심 |
| 2026-02-10 | AWS KV Cache 중간 Tier | 자사 발의 KV Cache 축 기원 (IBM 4일 후) |
| 2026-02-12 | HPE EVB / Venice | HPE 기원 (IBM 6일 후) |
| 2026-03-11 | Oracle OCI Pooling | AIC 너무 큼 (IBM AIC 출발과 대조) |
| 2026-03-12 | FMTA / NVIDIA | NVIDIA 발의 KV Cache 축 기원 |
