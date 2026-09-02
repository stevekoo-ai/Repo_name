---
title: "Lenovo CXL CMM 미팅 — 2026-01-15"
date: 2026-01-15
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, lenovo, cmm, sample-timing, controller-delay, pricing, form-factor, graded-memory]
attendees:
  sk_hynix: ["구병호 (KOO BYEONG HO) DRAM Solution", "심응보 (SHIM EUNGBO) DRAM Solution"]
  lenovo: ["Sumanta", "SJ Park", "Fred", "Joymoon"]
source: sources/lenovo-cxl-cmm-meeting-2026-01-15.md
relation: customer
significance: "★★"
---

# Lenovo CXL CMM 미팅 — 2026-01-15

> **현재 말뭉치 내 최초 미팅** (2026-01-15, Google 02-05보다 3주 앞선).
> CXL CMM 2세대 샘플 일정 + 컨트롤러 납기 지연 + CMM 가격(RDIMM 대비) + 폼팩터/용량 전략.
> 단일 출처(구병호 TL 작성), 외부 교차검증 미수행.

---

## 0. 핵심 요약 (5개)

| # | 핵심 | 영향도 |
|---|------|--------|
| 1 | **공유 컨트롤러 납기 지연 → 2세대 제품 일정 영향** — ES 샘플 26년 9월 말, CS 샘플 2027년 2월 말 | ★★ |
| 2 | **SIT(System Integration Test)부터 CS 샘플 필수** (Lenovo 강력 요구, SIT 시점 align 필요 Jan '27). ES=FW만 다른 동일 샘플이나 품질 인증 확보되야 CS | ★★ |
| 3 | **Early-ES(ES-1개월) BBFV 투입 + 엔지니어 파견** → BBFV 진행 속도 향상 제안 (자사) | ★ |
| 4 | **CMM sales 부진 = CMM 가격이 RDIMM보다 비싸** → **저등급(Graded memory) DRAM 활용 저가 CMM 개발 필요** (Sumanta) | ★★★ |
| 5 | **2nd Gen 512GB 계획 취소 여부 + 3rd Gen 기타 FF 고려 문의** (SJ Park) | ★★ |

---

## 1. 배경 — CXL CMM 2세대 샘플 일정

- Lenovo = CXL CMM 채택 고객. 본 미팅 = 2세대 CMM 샘플 제공 일정 + 컨트롤러 납기 지연 대응.
- 자사 2명(구병호·심응보 DRAM Solution) / Lenovo 4명(Sumanta·SJ Park·Fred·Joymoon).
- **공유 컨트롤러(= CMM 컨트롤러) 납기 지연** → 2세대 제품 일정 영향 → 공급 계획 delay.

---

## 2. 샘플 일정 지연 및 대응

| 샘플 | 시점 | 비고 |
|------|------|------|
| Early-ES | ES -1개월 | BBFV(Board Bring-up & Functional Validation) 투입 제안 |
| **ES** | **2026년 9월 말** | (delay) |
| **CS** | **2027년 2월 말** | (delay) SIT부터 필수 |

- 자사 제안: **Early-ES 샘플을 BBFV 단계에 투입 + 주요 엔지니어 파견** → BBFV 진행 속도 향상 (일정 지연 회피).
- Lenovo: BBFV용 Early-ES/ES 제공 시점엔 진행 가능. 단 **SIT부터는 CS 샘플 필수**, 일정 맞출 것 요구.
- 자사 대응: 내부 논의 통해 일정 최대한 당기겠다고 대응.

### ES vs CS 기술적 차이
- ES·CS = **동일 샘플, FW version만 다름**.
- 단 내부 품질 인증 확보되어야 CS 제공 가능 → ES·CS 사이 gap 발생.
- **SIT 단계 = 최증 인증된 샘플만 허용** → ES로는 SIT 진행 불가 (by Fred).

---

## 3. ★★★ CMM Biz — 가격 vs RDIMM (TCO thread 7번째 고객)

- 현시점 **Lenovo CMM sales 부진** → 원인 = **CMM 가격이 RDIMM보다 비싼 것** (Sumanta 판단).
- 제안: **저등급(Graded memory) DRAM 활용한 저가 CMM 개발 필요** (by Sumanta).
- → CMM 가격 경쟁력 = CXL CMM 사업화 핵심 장애. RDIMM 대비 프리미엄이 판매 저해.
- TCO thread **7번째 고객** (AWS·Oracle·MSFT·Dell·HPE·IBM + **Lenovo**). 단 Lenovo는 "가격 자체가 장애" — 가장 직접적 cost 장벽 명시.

---

## 4. 용량 / 폼팩터 전략 문의

- **2nd Gen 512GB 계획 취소 여부** 문의 (by SJ Park).
- **3rd Gen 기타 form factor 고려** 문의 (by SJ Park).
- → 폼팩터 thread에 "2nd Gen 512GB 취소 가능성 + 3rd Gen FF 확장" 이슈 추가. Dell 05-27 "AIC vs E3.L/S 트레이드오프"·IBM 02-06 "2028 AIC→2029 E3.S 2T"와 함께 3rd Gen FF 논의 축.

---

## 5. Action Items

| # | Action | 내용 |
|---|--------|------|
| 1 | **CS 샘플 일정 재검토** | Lenovo 강력 요구, 내부 검토 필요 (SIT 시점 align, Jan '27) |
| 2 | **ES 샘플로 BBFV 검증 진행 준비** | on time, Early-ES 제공 + 엔지니어 파견 포함 |

---

## Follow-up Actions

- [ ] Action 1: CS 샘플 일정 재검토 (내부, SIT Jan '27 align)
- [ ] Action 2: Early-ES BBFV 투입 + 엔지니어 파견 준비 (on time)
- [ ] 저등급(Graded memory) DRAM 활용 저가 CMM 개발 — 자사 내부 검토 (Sumanta 제안)
- [ ] 2nd Gen 512GB 계획 취소 여부 + 3rd Gen FF 전략 내부 정리 후 회신 (SJ Park 문의)

---

## Related

- 상대방별 누적: [by-customer/lenovo.md](../by-customer/lenovo.md)
- TCO thread (7개 고객, Lenovo = 가격 자체 장애 가장 직접적): [index.md §3](../index.md)
- 폼팩터 thread (2nd Gen 512GB 취소 + 3rd Gen FF): [index.md §3](../index.md)
- 컨트롤러 thread (공유 컨트롤러 납기 지연 → 2세대 일정 영향): Marvell CMM AX / Montage MXC 교차 — [index.md §3](../index.md)
- 시계열: 본 미팅(01-15, 최초) → Google 02-05(3주 후) → IBM 02-06 → AWS 02-10

---

## Timeline 교차 (현재까지 최초 미팅)

| 날짜 | 미팅 | 본 미팅과의 관계 |
|------|------|------------------|
| **2026-01-15** | **Lenovo CXL CMM (본 미팅)** | **말뭉치 최초 미팅**. CMM 가격 vs RDIMM, 컨트롤러 납기 지연, 2nd Gen 512GB 취소 문의 |
| 2026-02-05 | Google DRAM/MRDIMM | 3주 후 (DRAM 비-CXL) |
| 2026-02-06 | IBM Power Future | CXL CMM 가격/TCO 맥락 교차 |
| 2026-05-27 | Dell TDF | 3rd Gen FF (AIC vs E3) 논의 교차 |
