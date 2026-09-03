---
title: "Customer-Meetings Thread Tracker — 교차검증 thread 현재 상태"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, dram, customer-meeting, monitoring, thread-tracker, cross-validation]
---

# Customer-Meetings Thread Tracker — 교차검증 thread 현재 상태

> 11개 미팅에서 발견된 교차 thread(여러 미팅에 걸쳐 등장하는 주제)의
> 현재 상태·미해결·확정 매핑. 4-layer 구조의 Monitoring 레이어(append-only 추적).
> Framework/운영 패턴: [concepts/customer-meetings-intelligence.md](../concepts/customer-meetings-intelligence.md).
> 이벤트 기록: [summaries/customer-meetings-overview-2026-01-15-to-08-11.md](../summaries/customer-meetings-overview-2026-01-15-to-08-11.md).
> 전문: [customer-meetings/](../customer-meetings/).

---

## Thread 상태 테이블

| # | Thread | 관련 고객/날짜 | 상태 | 미해결 |
|---|--------|----------------|------|--------|
| 1 | **KV Cache CXL (3 출처)** | IBM 02-06(독립 인지)·AWS 02-10(자사 발의)·NVIDIA 03-12(발의)·MSFT 04-30·08-11 | ✅ 3출처 확정(정정 4회 완료) | — |
| 2 | **TCO/가격 (7 고객)** | Lenovo 01-15·IBM 02-06·AWS 02-10·Oracle 03-11·MSFT 04-30·HPE 05-07·Dell 05-27 | ✅ 7고객 공통 확인 | 저가 CMM(Graded memory) 개발 가능성 미확정 |
| 3 | **폼팩터 (7-way)** | Lenovo 01-15·IBM 02-06·AWS 02-10·HPE 02-12·Oracle 03-11·HPE 05-07·Dell 05-27 | ✅ 7-way 분류 | 3rd Gen 최종 FF 미확정 |
| 4 | **3rd Gen FF 전환기** | Lenovo 01-15·IBM 02-06·Dell 05-27 | 🟡 3고객 논의 중 | Lenovo 2nd Gen 512GB 취소 여부 미확정 |
| 5 | **CMM 컨트롤러 납기 지연** | Lenovo 01-15(공유 컨트롤러) + Marvell CMM AX/Montage MXC | 🟡 지연 확인, 원인 벤더 미특정 | "공유 컨트롤러" = Marvell AX? Montage MXC? 미확인 |
| 6 | **CXL switch 경쟁** | Oracle 03-11 + Marvell/Broadcom/Xconn | ✅ 구도 정리 | Oracle 최종 아키텍처 선택 미확정 |
| 7 | **AMD Venice 플랫폼 교차** | Google 02-05(DRAM)·HPE 02-12(CXL) | ✅ 동일 플랫폼 2페이즈 확인 | Venice CXL GA 시점(HPE 2027-06?) |
| 8 | **Intel DMR 플랫폼 교차** | Google 02-05(DRAM)·Intel 08-11(CXL) | ✅ DRAM→CXL 확장 확인 | DMR GA 27년 1~2월(Confidential) |
| 9 | **MRDIMM** | Google 02-05(비-CXL)·HPE 02-12(CXL) | ✅ 2관점 확인 | 자사 Gen2 축소 vs Google Venice POR 긴장 미해결 |
| 10 | **IMDB/Memory sharing** | HPE 02-12·MSFT 04-30·Oracle 03-11·IBM 02-06 | ✅ 4고객 공통 | — |
| 11 | **Local CXL 가치 훼손** | Oracle 03-11·AMD 12→16ch(간접) | ✅ Local 부정≠Pooled 부정 | — |
| 12 | **Oracle HA 요구** | Oracle 03-11·Montage MHD | 🟡 HA 필수 합의 | Montage MHD = 8CH or 2CH? (Jay 모름→Montage 문의 필요) |
| 13 | **Oracle AIC 시계열 반전** | Oracle 03-11→08-11 | ✅ 5개월 반전 확인 | — |
| 14 | **HPE Venice 시계열** | HPE 02-12→05-07 | ✅ Post-Launch→2027-06 | — |
| 15 | **Dynamo 동일 SW?** | NVIDIA(tiering)·AMD(Inference SW) | 🟡 양쪽 언급 | 동일 SW인지 미확인 |
| 16 | **Montage MXC vs CMM AX** | Montage(시료생산)·자사 CMM AX(Eval Card) | 🟡 타이밍 격차 | Gen3 전환 시 경쟁 시점 미확정 |

---

## 미해결 항목 상세 (후속 미팅에서 확인 필요)

### 🔴 우선 — 컨트롤러/아키텍처 미확정

1. **"공유 컨트롤러" 정체** (Lenovo 01-15) — "공유 컨트롤러 납기 지연"의 구체 벤더.
   - 후보: Marvell CMM AX(공동개발, Eval Card 단계) / Montage MXC(시료생산) / 기타
   - 확인 경로: 자사 내부 CMM 컨트롤러 공급망
2. **Montage MHD = 8CH or 2CH?** (Oracle 03-11) — HA 경로 결정 key. Jay 모름.
   - 확인 경로: Montage 직접 문의
3. **Oracle 최종 아키텍처** (switch vs switchless) — 자사 CMM 경쟁력 직결.
   - 확인 경로: 6월 Oracle sync-up(예정)

### 🟡 중간 — 3rd Gen FF/용량

4. **Lenovo 2nd Gen 512GB 취소 여부** (SJ Park 문의) — 자사 회신 대기
5. **3rd Gen 최종 FF** — Lenovo(기타 FF)·Dell(AIC vs E3.L/S)·IBM(2029 E3.S 2T) 3고객 입장 분산
6. **자사 MRD Gen2 축소 vs Google Venice POR** — 전략적 긴장 미해결

### 🟢 정보성 — 일정/플랫폼

7. **Venice CXL GA 시점** — HPE 02-12 "Post-Launch" ↔ HPE 05-07 "2027-06 Launch" 교차
8. **Intel DMR GA 27년 1~2월** (Confidential) — Google 02-05 단일 출처
9. **Dynamo 동일 SW?** — NVIDIA/AMD 양쪽, 동일 SW인지 교차검증 미수행

---

## 교차검증 대기 (간접 등장만, 직접 미팅 없음)

- **Meta** — IBM 02-06 HMSDK 협력 파트너로 언급, 미팅 참석 아님 → by-customer/meta.md 미생성(README relation 범위 밖 자사 협력사)
- **SAP** — IBM 02-06 SAP HANA IMDB로 언급, 미팅 상대 아님 → 간접 참조만

---

## 업데이트 이력

- **2026-08-11 신설**: 11개 미팅 수집 완료 시점. 16개 thread 정리(✅9 / 🟡7). 미해결 9건 분류(🔴3 / 🟡3 / 🟢3).

---

## Related

- Framework: [concepts/customer-meetings-intelligence.md](../concepts/customer-meetings-intelligence.md)
- 이벤트 기록: [summaries/customer-meetings-overview-2026-01-15-to-08-11.md](../summaries/customer-meetings-overview-2026-01-15-to-08-11.md)
- 전문·교차표: [customer-meetings/index.md](../customer-meetings/index.md) §3
- CXL 벤더: [concepts/cxl-controller-vendor-landscape.md](../concepts/cxl-controller-vendor-landscape.md)
