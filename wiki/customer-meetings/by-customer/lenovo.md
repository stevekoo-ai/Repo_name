---
title: "Lenovo — CXL CMM (customer)"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer, lenovo, cmm, sample-timing, controller-delay, pricing, graded-memory, form-factor]
entity: Lenovo
relation: customer
first_contact: 2026-01-15
meetings: 1
---

# Lenovo — CXL CMM (customer)

> Lenovo = CXL CMM 채택 고객. 2세대 CMM 샘플 일정 + 컨트롤러 납기 지연 대응 + CMM 가격(RDIMM 대비) 장애.
> 단일 출처(구병호 TL 작성 2026-01-15), 외부 교차검증 미수행.

---

## 현재 관계 상태 (2026-01-15 기준)

- **단계**: 2세대 CMM 샘플 일정 조정 중. 컨트롤러 납기 지연으로 ES/CS delay.
- **샘플**: ES 2026-09 말 / CS 2027-02 말 (delay). SIT부터 CS 필수(Lenovo 강력 요구, Jan '27 align).
- **자사 제안**: Early-ES(ES-1개월) BBFV 투입 + 엔지니어 파견 → BBFV 속도 향상.
- **CMM sales**: 부진 — **CMM 가격이 RDIMM보다 비싸** → 저등급(Graded memory) DRAM 저가 CMM 개발 요구(Sumanta).
- **폼팩터/용량**: 2nd Gen 512GB 취소 여부 + 3rd Gen 기타 FF 문의(SJ Park) — 자사 회신 대기.
- **상태**: Action 2건(일정 재검토·BBFV 준비) + 저가 CMM/FF 전략 내부 검토 대기.

---

## 핵심 팩트 (누적)

### 샘플 / 일정
- **공유 컨트롤러(CMM 컨트롤러) 납기 지연** → 2세대 제품 일정 영향 → 공급 delay.
- ES 샘플 2026-09 말 / CS 샘플 2027-02 말.
- **SIT(System Integration Test)부터 CS 샘플 필수** — ES로는 SIT 불가(최증 인증된 샘플만 허용, by Fred).
- ES·CS = 동일 샘플, FW version만 다름. 내부 품질 인증 확보 시 CS 제공 → ES·CS gap.
- 자사 제안: **Early-ES(ES-1개월) BBFV 투입 + 엔지니어 파견** → BBFV 속도 향상.

### CMM 가격 / TCO ★★★
- **CMM sales 부진 = CMM 가격이 RDIMM보다 비싼 것**(Sumanta 판단).
- 제안: **저등급(Graded memory) DRAM 활용 저가 CMM 개발 필요**.
- → CMM 가격 경쟁력 = CXL CMM 사업화 핵심 장애. RDIMM 대비 프리미엄 = 판매 저해.
- TCO thread **7번째 고객**. Lenovo = "가격 자체가 장애" — 가장 직접적 cost 장벽 명시 (Oracle은 DIMM 수준, IBM은 $/GB 절감 명목, Lenovo는 sales 부진 원인).

### 폼팩터 / 용량
- **2nd Gen 512GB 계획 취소 여부** 문의 (SJ Park).
- **3rd Gen 기타 form factor 고려** 문의 (SJ Park).
- → 3rd Gen FF 전환기 논의. Dell 05-27(AIC vs E3.L/S)·IBM 02-06(2028 AIC→2029 E3.S 2T)과 함께 3rd Gen FF 축.

### 참석자
- SK hynix: 구병호(KOO BYEONG HO) DRAM Solution·심응보(SHIM EUNGBO) DRAM Solution (2명)
- Lenovo: Sumanta·SJ Park·Fred·Joymoon (4명)

---

## Follow-up Actions (대기)

- [ ] Action 1: CS 샘플 일정 재검토 (내부, SIT Jan '27 align)
- [ ] Action 2: Early-ES BBFV 투입 + 엔지니어 파견 준비 (on time)
- [ ] 저등급(Graded memory) DRAM 활용 저가 CMM 개발 — 자사 내부 검토
- [ ] 2nd Gen 512GB 취소 여부 + 3rd Gen FF 전략 내부 정리 후 회신

---

## 미팅 이력 (역순)

### ★ 2026-01-15 — Lenovo CXL CMM 미팅 ★★ (최초, 말뭉치 내 최초 미팅)

- **전문**: [meetings/2026-01-15-lenovo-cxl-cmm.md](../meetings/2026-01-15-lenovo-cxl-cmm.md)
- **참석**: SK hynix(구병호·심응보 DRAM Solution) / Lenovo(Sumanta·SJ Park·Fred·Joymoon)
- **핵심**: 2세대 CMM 샘플 일정(ES 26-09말/CS 27-02말, 공유 컨트롤러 납기 지연으로 delay). SIT부터 CS 필수. Early-ES BBFV 투입+엔지니어 파견 제안. **CMM sales 부진 = CMM 가격이 RDIMM보다 비싸** → 저등급(Graded memory) DRAM 저가 CMM 개발 요구(Sumanta). 2nd Gen 512GB 취소 여부 + 3rd Gen FF 문의(SJ Park).
- **DRAFT 연결**: 7장 Main Memory(CMM 가격 vs RDIMM, 저등급 DRAM 저가 CMM) · 4장 풀링(CMM 컨트롤러 납기 지연 → 2세대 일정) · 12장 상품기획(저가 CMM, 3rd Gen FF).
