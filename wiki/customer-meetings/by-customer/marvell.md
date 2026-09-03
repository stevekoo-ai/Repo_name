---
title: "Marvell — 고객·파트너 미팅 누적 이력"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, by-customer, marvell, controller, photonics, asic]
entity: marvell
relation: partner
---

# Marvell — 미팅 누적 이력

> **상대방별 누적 뷰** — Marvell이 등장한 모든 미팅의 요약 + 현재 관계 상태.
> 미팅별 전문은 `../meetings/` (날짜키).
> CXL DRAFT 연결: 3장 컨트롤러 / 2장 기술 (Photonics) / 7장 Main Memory (3D stacked) / 4장 풀링

---

## 현재 관계 상태 (최신 미팅 기준)

- **관계**: 파트너 (CXL-PNM 백서 공동 발간 + Photonics Pooled 협력 + CMM AX 공동개발, 2026-08-11)
- **단계**: 백서 완료 + Photonics Pooled Silicon 연내 이용 가능 → 후속 미팅 예정. CMM AX Evaluation Card 개발 중(Structure A, 2026-05부터).
- **핵심**: Marvell = **Density AI의 ASIC Partner** + **CMM AX 컨트롤러 공동개발사** (Xcena와 함께). Photonics 기반 Pooled Controller **연말 ES**.

## 핵심 팩트 (누적)
- **CXL-PNM 백서** 공동 발간 (FMS). Oracle PNM 관심 → Top Level 적극 지원.
- 자사 Pooled 계획 공유, 요소 기술(CXL Switch, Photonics) 협력 지속.
- GPU Rack 공간 부족 → Pooled 별도 Rack 시 Rack 간 인터커넥트 = Pain Point → **Marvell Photonics Pooled Silicon 연내 이용 가능**.
- 3D Stack: 자사 전략 + **TSMC 협력 모델 긍정 피드백**.
- **Photonics Pooled Controller 연말 ES**: Pod-scale, **RDMA 대비 저지연**, PCIe Copper 대비 장거리·고대역·저지연. **Memory as a Service(메모리 랙) 필수 요소**. Appliance Maker = **Penguin**.
- **CMM AX 컨트롤러 공동개발** (2026-05-27 Dell 미팅에서 Jerry Shim 발언): Marvell + Xcena와 Co-working. "Structure A" 구조, Evaluation Card 개발 중.
- **★ Switch 인수 경쟁 (2026-03-11 Oracle 미팅에서 Jay 발언)**: Marvell = **Broadcom과 경쟁하기 위해 CXL switch 인수** 의도. Xconn(스위치 벤더) 인수 대상 — Oracle-Xconn 협의가 Marvell 인수로 중단됨. 4월 Oracle이 Xconn/Marvell과 재논의 예정. Marvell의 CXL 전략 = 컨트롤러(CMM AX) + 스위치(인수) 양면.

## 후속 액션 / 미해결
- [ ] Photonics Pooled Silicon 후속 미팅 (Rack 간 인터커넥트 Pain Point 해소)
- [ ] 3D Stack 자사 Spec 후속 미팅
- [ ] Density AI 자사 Spec 후속

## 미팅 이력 (역시간순)

### 2026-08-11 — CXL 메모리 풀링 미팅
- **참석**: Will Chu(GM) / Khurram(VP) // Ravi(PM) / Steve(Sales)
- (CXL & 3D stacked) CXL-PNM 백서, Oracle PNM top-down 지원, Pooled 요소기술 협력, Rack 간 인터커넥트 Pain Point → Photonics 연내, 3D Stack TSMC 긍정, Density AI ASIC Partner 확인.
- (Photonics Pooled) 연말 ES, RDMA 대비 저지연, Memory as a Service 필수, Penguin 협업.
- 전문: [../meetings/2026-08-11-cxl-pooling.md](../meetings/2026-08-11-cxl-pooling.md) §파트너 1)·2)
- ★★ (DRAFT 2·3·4·7장 반영 대기)

### 2026-05-27 — DELL TDF CXL Next Gen 스펙 미팅 (Marvell 간접 등장)
- **참석**: 심응보 팀장님 / 구병호 TL / Jerry Shim(SK hynix) // Stuart Berke / Raju Mishra(Dell)
- Marvell 직접 참석 아님. Jerry Shim이 CMM AX 컨트롤러 개발 협력사로 Xcena와 함께 Marvell 명시. "Structure A" 구조 Evaluation Card 공동개발 중.
- 전문: [../meetings/2026-05-27-dell-tdf-cxl-nextgen.md](../meetings/2026-05-27-dell-tdf-cxl-nextgen.md) §1)
- ★ (DRAFT 3장 컨트롤러 챕터 반영 대기)

### 2026-03-11 — Oracle OCI CXL Pooling 미팅 (Marvell 간접 등장 — switch 인수 경쟁)
- **참석**: SANTOSH KUMAR / SEUNGJU HAN / Donghyeok Park(자사) // JEBA SUNDRARAJ(Jay) / Somu Krishnasamy(Oracle)
- Marvell 직접 참석 아님. Jay가 "Marvell은 Broadcom과 경쟁하기 위해 switch 인수" 발언. Xconn(스위치 벤더) 인수 대상, Oracle-Xconn 협의가 Marvell 인수로 중단 → 4월 Oracle이 Xconn/Marvell과 재논의 예정.
- 전문: [../meetings/2026-03-11-oracle-oci-cxl.md](../meetings/2026-03-11-oracle-oci-cxl.md) §4)
- ★★ (DRAFT — CXL switch 경쟁 구도 반영 대기)
