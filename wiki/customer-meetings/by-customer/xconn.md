---
title: "Xconn — 미팅·시장情报 누적 이력"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, by-customer, xconn, cxl-switch, marvell-acquisition]
entity: xconn
relation: partner
---

# Xconn — 미팅·시장情报 누적 이력

> **상대방별 누적 뷰** — Xconn이 등장한 모든 미팅·시장 신호의 요약 + 현재 관계 상태.
> 미팅별 전문은 `../meetings/` (날짜키).
> CXL DRAFT 연결: CXL switch 벤더 — Marvell 인수 대상

> **분류 근거**: Xconn = CXL switch 벤더. SK hynix 풀링 솔루션의 switch 서플라이어로 Oracle pooling 일정 좌우. Marvell 인수 대상 — 현재 Marvell 산하로 추정. partner(서플라이어) 분류.

---

## 현재 관계 상태 (최신 기준)

- **관계**: (추정) Marvell 산하 — CXL switch 벤더 (2026-03-11 Oracle 미팅에서 Jay 발언)
- **단계**: Oracle-Xconn 협의 → Marvell 인수로 중단 → **4월 Oracle이 Xconn/Marvell과 재논의 예정** (2026-03-11 시점)
- **핵심**: Xconn = Oracle CXL pooling 일정의 **bottleneck**. switch 일정 문제로 Oracle pooling slow down. Marvell이 Broadcom 경쟁 위해 인수.

## 핵심 팩트 (누적)
- **Oracle-Xconn 협의(2026-03-11)**: Oracle이 switch 기반 pooling 위해 Xconn과 협의 중이었으나, Marvell 인수 후 논의 중단. 4월 Oracle이 Xconn/Marvell과 재논의 예정.
- **일정 지연**: Xconn 일정 문제로 Oracle pooling 진행 slow down (2026-03-11 팀장 보고).
- **Marvell 인수 의도**: Broadcom과 경쟁하기 위해 Marvell이 Xconn(switch) 인수 (Jay 발언, 2026-03-11).
- (참고) Xconn = CXL switch 전문 벤더. 자사 CMM AX(Multi-Head, Switchless 경로)와는 switch 기반 풀링 아키텍처에서 경쟁/대안 관계.

## 후속 액션 / 미해결
- [ ] **4월 Oracle ↔ Xconn/Marvell 재논의** 결과 확인 (2026-03-11에서 예정)
- [ ] Xconn 인수 완료 여부 + Marvell 산하 통합 상태
- [ ] Xconn CXL switch 로드맵 / 샘플 일정 (Oracle pooling bottleneck 해소 시점)
- [ ] Switch 기반 풀링(switch) vs Switchless(Montage MHD / 자사 CMM 2포트) — Oracle이 최종 선택할 아키텍처

## 미팅·신호 이력 (역시간순)

### 2026-03-11 — Oracle OCI CXL Pooling 미팅 (Xconn 간접 등장)
- **참석**: SANTOSH KUMAR / SEUNGJU HAN / Donghyeok Park(자사) // JEBA SUNDRARAJ(Jay) / Somu Krishnasamy(Oracle)
- Xconn 직접 참석 아님. Jay 발언: Oracle은 Xconn과 협의 중이었으나 Marvell 인수 후 중단. 4월 Oracle이 Xconn/Marvell과 재논의 예정. Marvell은 Broadcom 경쟁 위해 switch 인수.
- 팀장 보고: Xconn 일정 문제로 Oracle pooling slow down.
- 전문: [../meetings/2026-03-11-oracle-oci-cxl.md](../meetings/2026-03-11-oracle-oci-cxl.md) §1·4)
- ★★ (DRAFT — CXL switch 공급망·일정 리스크 반영 대기)

> **교차검증 대기**: Xconn(Marvell 인수, switch 기반) vs Montage MHD(Switchless, 2호스트 HA) vs 자사 CMM 2포트(Switchless) — Oracle이 4대 서버 풀을 위해 최종 선택할 아키텍처. 6월 Oracle sync-up에서 확인 예정.
