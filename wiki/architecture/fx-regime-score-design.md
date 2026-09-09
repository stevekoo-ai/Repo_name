---
title: FX Regime Score (FRS) — 환율 국면 판단 엔진 설계
created: 2026-09-09
updated: 2026-09-09
tags: [fx, design, architecture, frs, regime, plan]
---

# FX Regime Score (FRS) 설계

사용자 요청(2026-09-09) — "앞서 5번의 패턴에 영향을 준 요인들을 항목으로 놓고
환율에 플러스 마이너스 수준을 weight에 따라 define해서, 트렌드가 변했는지 곧
국면이 바뀔 것이라는 경고를 줄 수 있도록". 근거는
[36개월선 하회 국면 전수분석](../concepts/usdkrw-below-ma36-episodes.md).

**확정된 결정 2건**
- **R4**: FX 섹션은 **근거만 제공**한다. "헤지하라/말라"는 지시를 내지 않는다
  (CCI가 '위험 환경 정보'로 격하되는 것과 같은 취급).
- **순서**: 계산 엔진과 백테스트를 **동시 진행** — 아래 §1의 설계 제약이 여기서 나온다.

## 1. ⚠️ 최우선 설계 제약 — 모든 점수 함수는 `as_of`를 받는다

"동시 진행"을 성립시키는 유일한 방법이다. 기존 CCI는 `_get_latest()`로 **항상
최신값만** 읽어서 **구조적으로 백테스트가 불가능**하다. FRS는 이 약점을 처음부터
막는다.

```python
def score_rate_differential(as_of: date) -> FactorScore: ...
def calculate_frs(as_of: date) -> FRSDetail: ...
```

- 오늘 리포트 = `calculate_frs(date.today())`
- 과거 5국면 백테스트 = `[calculate_frs(d) for d in 월말들]`

**같은 코드가 두 용도를 겸한다 → 백테스트가 별도 작업이 아니라 공짜로 따라온다.**
회귀 테스트로 "as_of를 과거로 주면 그 시점 이후 데이터를 절대 읽지 않는다"
(look-ahead bias 차단)를 고정한다.

## 2. 점수 체계

CCI(0~100 단방향)와 달리 **−100 ~ +100 양방향**. **(+) = 원화 강세 압력**.

각 요인은 `[-1, +1]`로 정규화 후 가중치를 곱한다. 미수집 요인은 0점이 아니라
**"미수집"으로 표기하고 가중치를 총점에서 제외한 뒤 재정규화**한다(R3 — 미수집을
중립으로 읽으면 안 된다).

| # | 요인 | 가중 | 데이터 | 실증 근거(어느 국면을 만들었나) |
|---|---|---:|---|---|
| 1 | 한미 정책금리차 | 25 | `ecos_base_rate` − `us_fed_funds` | ④2018 **역전된 그 달** 종료 / ⑥2026 시작 엔진 |
| 2 | 미 10년물 레벨·모멘텀 | 15 | `fred_us_10y_treasury` | ⑤2021 종료(0.93→1.74%) |
| 3 | 달러인덱스 방향 | 15 | `fred_us_dollar_index` | ④2017 시작(연 −10%), 전 국면 배경 |
| 4 | 경상수지 추세 | 15 | `ecos_current_account` | ②③ '차별화'의 근거, 전 국면 연료 |
| 5 | 수출·반도체 증가율 | 10 | `customs_export_dlr` + 반도체 수출 | ④2017 슈퍼사이클, ⑥2026 네고물량 |
| 6 | **지정학·위기 이벤트** | 10 | **`manual_inputs/fx_risk_events.yaml` (LLM)** | ①2011 유럽위기, ⑥2026 중동 |
| 7 | 유가(브렌트) | 5 | `us_brent` | ③2014 종료, 교역조건 |
| 8 | MA36 이격도 | 5 | `ecos_usdkrw` 파생 | 국면 라벨 + 극단시 평균회귀 압력 |

**요인 1이 최대 가중인 이유**: 5개 국면 중 시작 2회·종료 1회를 단독으로 설명한
유일한 요인. 레벨보다 **방향(3개월 변화)** 비중을 크게 잡는다(0.4 레벨 : 0.6 방향)
— 2018은 "역전"이라는 방향 전환이, 2026은 "축소"라는 방향이 트리거였지 절대
수준이 아니었다.

## 3. 두 개의 출력

### 출력 A — 현재 국면
`MA36 이격 부호` × `FRS 부호` 조합으로 라벨:
`원화 강세 국면 / 강세 진입 시도 / 중립 / 약세 진입 시도 / 원화 약세 국면`

### 출력 B — 국면 전환 경고 (요청의 핵심)
점수 레벨이 아니라 **과거 5회의 종료 패턴을 코드화한 감지기 4종**:

1. **모멘텀 반전** — FRS 3개월 추세 방향 전환
2. **종료 트리거 매칭** — ⓐ금리차 축소→확대 전환(2018형) ⓑ미10년물 3개월 +50bp
   급등(2021형) ⓒ경상·수출 증가율 둔화(연료 소진) ⓓ지정학 리스크 급등(2011·2026형)
3. **이격 극단** — MA36 대비 ±8% 이상(과거 평균회귀 지점)
4. **경과 개월** — 현재 국면 지속기간 vs 과거 중앙값 11개월

켜진 개수 → **🟢안정(0-1) / 🟡전환주의(2) / 🔴전환임박(3+)**

## 4. LLM 참여 — 기존 패턴 재사용

`data/manual_inputs/semiconductor.yaml`과 **동일 스키마**(신규 발명 없음):

```yaml
as_of: "2026-09-09"
reliability_grade: 3
signals:
  geopolitical_risk: 0.6   # 0~1, 높을수록 위험 → 원화 약세 압력으로 부호 반전
  pandemic_risk: 0.0
  trade_policy_risk: 0.4   # 관세·수출규제
  financial_stress: 0.1    # 신용경색·위기
notes: "중동 후티 사우디 공격, 유가 96달러 — 2026-06 스파이크 원인 미해소"
```

- **갱신 주체**: Claude가 뉴스 조사 후 기입(`/ingest` 흐름)
- **드리프트 방지**: 기존 `wiki_digest` as_of 검사와 동일 방식 — 오늘 실제로 그
  테스트가 누락을 잡아냈다(2026-09-09 log 참고)
- **R2 준수**: as_of가 오래되면 리포트에 "이 요인은 N일 전 판단" 명시

## 5. 파일 구조

```
engine/fx/
  __init__.py
  regime_score.py     # as_of 받는 8개 score_* + calculate_frs
  transition.py       # 전환 경고 감지기 4종
  backtest.py         # 과거 월말 순회 → 5국면 재현 검증
data/manual_inputs/fx_risk_events.yaml
tests/test_fx_regime_score.py
tests/test_fx_backtest.py          # look-ahead bias 차단 + 5국면 재현
```
리포트 섹션: **§1.7 환율 국면** (§1.5 미국 노동시장 뒤, §2 SK하이닉스 앞 —
거시 맥락이 포지션 판단으로 흘러가는 순서)

## 6. 합격 기준 (이게 안 되면 가중치를 다시 설계한다)

백테스트에서:
1. 과거 5개 국면의 **진입/이탈을 ±3개월 이내**로 잡는가
2. 전환 경고가 실제 전환 **이전에** 켜졌는가
3. 거짓 경보율이 감당 가능한가
4. look-ahead bias 0 (as_of 이후 데이터 미참조를 테스트로 고정)

## 7. 단계

- **Phase 1** `regime_score.py` — as_of 기반 8개 요인 + 총점(백테스트 하네스 동반)
- **Phase 2** `transition.py` — 경고 감지기 4종
- **Phase 3** `backtest.py` 실행 → 5국면 재현 검증 → **가중치 확정/수정**
- **Phase 4** 리포트 §1.7 렌더 + `fx_risk_events.yaml` + LLM 갱신 절차
- **Phase 5** 위키 프레임워크 페이지 + digest 연결 + 자동화(기존 일일 파이프라인 편입, 네트워크 미사용)

## Sources

- [원/달러가 36개월 이동평균을 하회한 국면들](../concepts/usdkrw-below-ma36-episodes.md) — 요인·가중치의 실증 근거
- `engine/crisis_analysis/scoring.py` — 재사용할 뼈대(모듈별 점수→가중합→상태) 및 반면교사(as_of 미지원)
- `engine/report/reconciliation.py` — R1~R5, 특히 기존 R1 환율 충돌 감지기와의 정합
- `data/manual_inputs/semiconductor.yaml` — LLM 신호 주입 스키마 원본
