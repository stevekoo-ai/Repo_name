---
title: 미국 데이터센터 건설 반대 vs 착공 실적 — 일일 상태
created: 2026-08-27
updated: 2026-08-27
tags: [ai-infra, data-center, hbm-cycle-score, daily-tracking, monitoring, append-only]
---

# Latest Status

**2026-08-27(신설)** — 세션 내 조사 기반 최초 기록
- **착공 실적**: 🟢 사상 최고 — 2026 상반기 누적 $81.5B(2025년 전체
  $72.5B 이미 초과), 1월 $25.5B 역대 최고 단월.
- **건설 반대**: 🔴 급격히 악화 — 2026 1분기 $130B 차단/지연(2025년
  전체와 맞먹음), 텍사스 ERCOT/PUCT 전체 감사·중단, 메릴랜드 13/24
  카운티 모라토리엄, 여론 반대 75%.
- **종합 해석**: 두 신호가 상충 — 점수화하지 않고 원자료만 리포트에
  노출(월간 갱신). 다음 갱신에서 착공 실적 증가세가 꺾이는지가 첫
  시험대.
- 상세: [concepts/data-center-construction-vs-opposition.md](../concepts/data-center-construction-vs-opposition.md)
- 자동화: `engine/report/markdown.py`의 PEOS 리포트 "2.6" 섹션으로
  매일 원자료 노출 시작(2026-08-27) — 단 `data/manual_inputs/data_center_construction.yaml`
  자체는 **월간 수동 갱신** 필요(ConstructConnect·Data Center Watch
  모두 공개 API 없음, 7.3 예외).

---

## Check History (Reverse-chronological)

| 날짜 | 착공 실적 | 건설 반대 | 오늘의 요약 |
| --- | --- | --- | --- |
| **2026-08-27(신설)** | 🟢 2026 H1 $81.5B(사상 최고) | 🔴 2026 Q1 $130B 차단(급증) | 최초 기록 — 두 신호 상충, 점수화 보류. 다음 달 착공 데이터 증가세 지속 여부가 관건. |

---

## Sources

- [Framework Definition](../concepts/data-center-construction-vs-opposition.md)
- [HBM Cycle Score](../concepts/hbm-cycle-score.md)
- [트럼프 2026 중간선거 트래커](../concepts/trump-midterm-tracker.md)
- `data/manual_inputs/data_center_construction.yaml` (월간 수동 갱신 필요)
