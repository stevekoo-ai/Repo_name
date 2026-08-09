---
title: KOSPI Forward PE 근사 추적 — 일일 상태
created: 2026-08-09
updated: 2026-08-09
tags: [kospi, valuation, per, monitoring, daily-tracking, append-only]
---

# KOSPI Forward PE 근사 추적 — 일일 상태

**Framework**: [SK하이닉스 주가 상승의 정당성 분석 §코스피 지수 전체 밸류에이션 맥락](../concepts/rally-justification-analysis.md)

이 페이지는 append-only 일일 체크 기록입니다. 방법론·한계·앵커 정의는
framework 문서를 참고하세요.

## Latest Status (2026-08-08 기준)

**근사 forward PE**: 5.36배 (**-1SD(8.8배) 완전히 이탈**)

**20년 평균(10.0배) 대비**: -46.43%

**앵커(6.65배, 2026-07-02) 대비**: -19.44%

**해석**: 2026-07-02 Goldman Sachs 차트가 찍힌 "GFC 이후 최저" 순간
이후로도 KOSPI 지수가 추가로 더 빠지면서(7,769→6,259, 약 -19%), forward
EPS가 그대로라는 가정 하에서는 밸류에이션이 그 시점보다도 더 저평가된
구간으로 이동했습니다. **단, 이 구간에 SK하이닉스 등 주요 기업의 2Q
실적 발표(7/29)가 껴 있어 실제 컨센서스 EPS가 리비전됐을 가능성이
있고, 그 경우 이 근사치의 오차는 커집니다** — 방향성 참고용으로만
사용할 것.

---

## Daily Tracking (자동 계산: `scripts/kospi_valuation_tracker.py`)

| 날짜 | KOSPI | 근사 Forward PE | 밴드 위치 | 20년평균 대비 | 앵커(7/2) 대비 |
| --- | --- | --- | --- | --- | --- |
| 2026-07-31 | 6,595.45 | 5.65배 | -1SD 미만 | -43.55% | -15.11% |
| 2026-08-01 | 6,595.45 | 5.65배 | -1SD 미만 | -43.55% | -15.11% |
| 2026-08-02 | 6,595.45 | 5.65배 | -1SD 미만 | -43.55% | -15.11% |
| 2026-08-03 | 6,257.45 | 5.36배 | -1SD 미만 | -46.44% | -19.46% |
| 2026-08-04 | 6,358.95 | 5.44배 | -1SD 미만 | -45.57% | -18.15% |
| 2026-08-05 | 6,598.26 | 5.65배 | -1SD 미만 | -43.52% | -15.07% |
| 2026-08-06 | 6,296.38 | 5.39배 | -1SD 미만 | -46.11% | -18.96% |
| 2026-08-07 | 6,258.77 | 5.36배 | -1SD 미만 | -46.43% | -19.44% |
| 2026-08-08 | 6,258.77 | 5.36배 | -1SD 미만 | -46.43% | -19.44% |

원자료: [sources/kospi-forward-pe-approx.csv](../../sources/kospi-forward-pe-approx.csv)
(스크립트가 매번 이 표를 재계산 — `sources/kr-index-quote.csv`의 KIS API
일일 수집치가 갱신될 때마다 `python3 scripts/kospi_valuation_tracker.py
update` 재실행 필요, 아직 GitHub Actions 워크플로우 자동 연동은 안 됨).

**참고**: 7/31~8/2는 KOSPI 값이 동일(6595.45 반복) — 원본
`kr-index-quote.csv`에 8/1·8/2 신규 실측이 없어 직전값이 이월된 것으로
보임(자동화 데이터 갭 가능성, 실제 무변동인지 데이터 미수집인지 미확인).

---

## Check History (Reverse-chronological)

| 날짜 | 근사 Forward PE | 밴드 위치 | 비고 |
| --- | --- | --- | --- |
| **2026-08-09 (최초 설정)** | 5.36배(8/8 기준) | -1SD 미만 | 사용자 제보 차트(Goldman Sachs/Quantiwise, 앵커 6.65배 @7/2) 인제스트 후 `scripts/kospi_valuation_tracker.py` 신설, `kr-index-quote.csv`(7/31~8/8, 9영업일) 기반 최초 계산. 앵커 자체가 장중 스냅샷(종가 아님)이라는 한계와 어닝시즌 이후 EPS 리비전 미반영 한계를 명시하고 시작 |

---

## 시각화

꺾은선 그래프로 앵커 대비 트렌드를 보는 리포트(인터랙티브, 크로스헤어
툴팁 포함): https://claude.ai/code/artifact/abdae139-1b39-49fc-a4d9-7e5218cf81fc
(2026-08-09 발행, dataviz 팔레트 검증 완료)

## Sources

- [SK하이닉스 주가 상승의 정당성 분석](../concepts/rally-justification-analysis.md) — framework, 앵커 정의
- [sources/kospi-forward-per-band-chart-2026-08-09.md](../../sources/kospi-forward-per-band-chart-2026-08-09.md) — 원본 차트 인제스트 기록
- [sources/kospi-forward-pe-approx.csv](../../sources/kospi-forward-pe-approx.csv) — 계산 결과 원자료
- [sources/kr-index-quote.csv](../../sources/kr-index-quote.csv) — KOSPI 지수 일일 실측(KIS API)
- `scripts/kospi_valuation_tracker.py` — 계산 스크립트
