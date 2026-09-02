---
title: "Dell — 고객 미팅 누적 이력"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, by-customer, dell, poweredge, ai-pooling, formfactor]
entity: dell
relation: customer
---

# Dell — 미팅 누적 이력

> **상대방별 누적 뷰** — Dell이 등장한 모든 미팅의 요약 + 현재 관계 상태.
> 미팅별 전문은 `../meetings/` (날짜키).
> CXL DRAFT 연결: 폼팩터(AIC vs E3) / AI 풀링 섀시 설계 / RAS

---

## 현재 관계 상태 (최신 미팅 기준)

- **관계**: 고객 (DELL TDF, CXL Next Gen 스펙 논의, 2026-05-27)
- **단계**: 1차 스펙 미팅 완료 → **별도 Tech. meeting 요청됨, 후속 setup 예정**
- **핵심**: Dell은 현재 PowerEdge = AIC align. 단, 수십~수백 TB **AI 풀링** = 전용 최적화 섀시 원점 재설계 의향. 폼팩터(AIC vs E3) 최종 결정은 SK hynix 내부 진행 중.

## 핵심 팩트 (누적)
- **PowerEdge 현재 AIC align**: 고용량 달성 시 SDP 어렵고 2H/4H Stack보다 AIC expansion이 경제적 (현재는 작은 시장).
- **AI 풀링 입장 변화**: 수십~수백 TB AI 풀링 = 현재 플랫폼 아닌 usecase 최적화 설계 의향. 전면/후면 PCIe·CXL 레인 제약 없이 섀시 레벨 최적 폼팩터 탐색.
- **E3 관심**: E3.S + E3 Long(스토리지 제품) 지원. AIC 대안 E3 Long 검토 시 기획 방향 변화 가능성 질의.
- **RAS 우려**: 고용량 모듈(2TB+) fail 시 가용성·대형 장애 확산 리스크 제기 → 모듈 수 2배인 E3가 더 안전할 수 있다는 견해.
- **써멀 관점**: AIC 후면 배치 = Preheat 열악 환경 (Dell 분석). E3 전면 배치 열적 우세.
- **섀시 공간**: FHHL = 3U, E3 = 2U stack. Dell 17G FHHL은 Riser cards 사용.
- **참석자 (Dell 측)**: Stuart Berke, Raju Mishra.

## 후속 액션 / 미해결
- [ ] **별도 Tech. meeting** setup (Dell 요청, 일정 미정)
- [ ] AI 풀링 적정 용량 사이즈 → SK hynix 내부 산정 후 Dell 공유
- [ ] AIC vs E3 최종 택일 (3세대 CXL) — SK hynix 내부 결정
- [ ] AIC 후면 thermal impact 검증 (풀링 전면 배치 가정)

## 미팅 이력 (역시간순)

### 2026-05-27 — DELL TDF CXL Next Gen 스펙 미팅
- **참석**: 심응보 팀장님 / 구병호 TL / Jerry Shim(SK hynix) // Stuart Berke / Raju Mishra(Dell)
- CMM AX 컨트롤러(Marvell+Xcena 공동개발, Structure A), AIC vs E3 트레이드오프(8개 Q&A), RAS 대응(SDDC+ ECC, 패리티), Dell AI 풀링 전용 재설계 의향, ref. design 부재(Switchless Multi Head FPGA 프로토타입).
- 전문: [../meetings/2026-05-27-dell-tdf-cxl-nextgen.md](../meetings/2026-05-27-dell-tdf-cxl-nextgen.md)
- ★ (DRAFT 폼팩터·AI 풀링·RAS 챕터 반영 대기)
