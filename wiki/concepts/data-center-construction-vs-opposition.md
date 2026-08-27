---
title: 미국 데이터센터 건설 반대 vs 착공 실적 — 두 신호의 긴장 관계
created: 2026-08-27
updated: 2026-08-27
tags: [ai-infra, data-center, hbm-cycle-score, concept, us-politics]
---

# 미국 데이터센터 건설 반대 vs 착공 실적

## 왜 이 개념이 필요한가

[HBM Cycle Score](hbm-cycle-score.md)의 "고객재고" 축은 SK하이닉스의
직접 고객(하이퍼스케일러)이 AI 인프라 수요를 실제로 지속하고 있는지를
본다. 지금까지는 SEC EDGAR CapEx 실측(발표된 지출액)만 봤는데, **CapEx는
"약속"에 가깝고 실제로 땅 위에 지어지고 있는지는 별도로 확인해야 한다**
— Bricks & Bytes 지적대로 "빅테크가 약속한 6,500억 달러 중 상당수는
아직 실제로 지어지지 않았다"는 보도가 있다. 이 개념 페이지는 그 간극을
메우는 두 개의 상충하는 신호를 다룬다.

## 신호 ①: 건설 반대가 빠르게 심각해지고 있다

- **[FACT]** Data Center Watch(10a Labs 자금 지원 — 경미한 이해상충
  가능성 유의) 집계: ~2025-03 기준 누적 $64B 규모 프로젝트가 차단/지연.
  **2026년 1분기 단독으로 $130B**가 차단/지연 — 2025년 전체와 맞먹는
  규모를 한 분기 만에 기록.
- **[FACT]** 텍사스: Abbott 주지사가 ERCOT/PUCT에 전체 신규 데이터센터
  계통연계 감사·일시중단 지시 (474GW 대기열, ~248개 프로젝트 — 텍사스는
  버지니아 다음 미국 2위 데이터센터 허브).
- **[FACT]** 메릴랜드: 24개 카운티 중 13개가 모라토리엄 채택.
- **[FACT]** 2026-07-18 하루 동안 42개 주에서 142건의 항의 시위,
  24개 주 142개 활동가 그룹.
- **[FACT]** 여론조사: 반대 75% / 찬성 15%. 초당적 — 영향권 지역구
  기준 공화당 55% / 민주당 45% 반대.
- **[FACT]** Brookings: 데이터센터 반대가 **2026 중간선거의 핵심
  이슈 중 하나**로 지목됨 — [트럼프 2026 중간선거 트래커](trump-midterm-tracker.md)와
  교차 연동.

## 신호 ②: 그런데 착공 실적은 사상 최고치다

- **[FACT]** ConstructConnect "Data Center Report"(월간, 2020-01부터
  Dodge Data & Analytics와 비교 가능한 방법론으로 착공액 집계):
  - 2026년 1월 $25.5B — **역대 최고 단월 기록**
  - 2026년 2월 $11.5B — 역대 6위
  - **2026년 상반기 누적 $81.5B** — 이미 2025년 전체($72.5B, 그 자체로
    2024년 전체 대비 3배 이상)를 초과
- **[미검증]** $22.3B 수치가 6월 또는 8월 중 어느 달 것인지 소스 간
  표기가 엇갈림 — 다음 갱신 시 재확인 필요, FACT 승격 보류.

## 두 신호가 왜 동시에 참일 수 있는가 (가설, 미해소)

1. **가설 A — 지역 편중**: 반대는 텍사스·메릴랜드 등 특정 주에
   집중되고, 버지니아 등 기존 허브는 계속 무저항으로 건설 중일 수
   있다.
2. **가설 B — 관성 지연 효과**: 이미 인허가를 받은 프로젝트는 계속
   진행되고, 신규 반대는 **미래의 신규 승인**을 막는 효과가 커서
   실제 감속은 2027년 착공 데이터에서야 나타날 수 있다.

어느 쪽이 맞는지는 **아직 검증되지 않았다** — 다음 달 착공 데이터에서
증가세가 꺾이는지가 첫 시험대다.

## 이 페이지가 리포트에 통합되는 방식

- **의도적으로 점수화하지 않는다.** 위 두 신호를 하나의 숫자로 합성할
  신뢰할 만한 방법론이 없어(Concept Before Conclusion), 자동 일일
  리포트(`engine/report/markdown.py::_data_center_construction_section`)는
  원자료만 그대로 노출하고 해석은 이 페이지에서 사람이 갱신한다.
- 원자료 소스: `data/manual_inputs/data_center_construction.yaml`
  (7.3 예외 정책 — ConstructConnect·Data Center Watch 모두 공개 API
  없음, 매달 수동 갱신 필요).
- PEOS 일일 리포트 "2.6 미국 데이터센터 건설 반대 vs 착공 실적"
  섹션으로 자동 렌더링됨 (2026-08-27 신설).

## Sources

- ConstructConnect "Data Center Report" (월간)
- Data Center Watch (10a Labs)
- Brookings — 2026 중간선거 이슈 분석
- Bricks & Bytes — 빅테크 CapEx 약속 vs 실착공 간극
- 세션 내 WebSearch 조사 (2026-08-27)
- [HBM Cycle Score](hbm-cycle-score.md) — 고객재고 축
- [AI 밸류체인 변두리 모니터](ai-value-chain-periphery-monitor.md)
- [트럼프 2026 중간선거 트래커](trump-midterm-tracker.md)
