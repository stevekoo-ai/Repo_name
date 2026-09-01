---
title: 반도체수출 정점-둔화 관찰 — 다시 전고점을 향해갈 조건 — Framework Definition
created: 2026-08-17
updated: 2026-08-17
tags: [exports, semiconductor, hbm, concept, framework, watch-list]
---

2026-08-17 사용자 질문("왜!!! 반도체 수출이 줄어들지? 원인이 뭐야?")에서
출발. 반도체수출(및 총수출)이 2026-06 정점을 찍고 07월부터 꺾였고, 08월
1~10일 잠정치도 추가 둔화를 가리킨다 — 이게 "일시적 노이즈"인지 "추세
전환의 시작"인지는 이 시점에 확정할 수 없다. 이 페이지는 그 판단을
매 10일/20일 관세청 잠정치가 나올 때마다 갱신 가능한 **체크리스트**로
만든 것 — 결론이 아니라 "무엇을 보면 판단이 바뀌는가"의 틀이다.

**일일 추적은 [monitoring/semiconductor-export-peak-recovery-status.md](../monitoring/semiconductor-export-peak-recovery-status.md).**
자동 갱신 경로는 §4 참고.

---

## 1. 관찰된 패턴 (실측, data/manual_inputs/exports.yaml +
   data/manual_inputs/exports_preliminary.yaml)

| 월 | 총수출 (억 달러) | 총수출 %YoY | 반도체수출 (억 달러) | 반도체수출 %YoY |
|---|---|---|---|---|
| 2026-04 | 858.9 | +48.0% | 319.0 | +173.5% |
| 2026-05 | 877.5 | +53.2% | 371.6 | +169.4% |
| 2026-06 | **1,022.5 (정점)** | +70.9% | **448.2 (정점)** | +199.5% |
| 2026-07 | 988.9 | +62.8% | 410.1 | +178.8% |
| 2026-08 (1~10일 잠정) | — | +45.3% | — | +155.4% |

**핵심**: 반도체수출은 6월 $44.8B에서 7월 $41.0B로 절대금액 자체가
줄었다(-8.5% MoM) — YoY 둔화(199.5%→178.8%)뿐 아니라 레벨(원 단위)로도
실제 하락. 8월 10일 잠정치(+155.4%)도 계속 둔화 방향. 총수출도 같은
모양(6월 정점 → 7월 하락)이며, 반도체가 7월 총수출의 41.5%
(410.1/988.9)를 차지해 총수출 둔화의 주 원인이 반도체다.

차트: [exports-price-levels-trend-2023-zoom.png](../../monitoring/exports-price-levels-trend-2023-zoom.png)
(레벨), [exports-price-correlation-2023-zoom.png](../../monitoring/exports-price-correlation-2023-zoom.png)
(%YoY) — 둘 다 이 정점→하락 모양을 보여준다.

---

## 2. 설명 가설 (경합 중 — 아직 하나로 확정되지 않음)

### 가설 A — 캘린더·타이밍 노이즈 (현재 언론·애널리스트 컨센서스에 가까움)

- **조업일수**: 7월 조업일수 24일, 전년 동월(25일)보다 하루 적음 — 일평균
  기준으로는 여전히 강한 성장이라고 산업통상부가 밝힘
  ([헤럴드경제](https://biz.heraldcorp.com/article/10827713)).
- **제품 믹스 변화(고가 메모리 비중 감소)**: 2026-06 D램 kg당 수출단가가
  9개월 만에 처음 하락했는데, 같은 달 D램 모듈 가격은 +11%, HBM 가격은
  +12% **올랐다** — 개별 제품 가격은 오르는데 평균단가가 내린 건 고가
  (HBM 등) 비중이 줄고 범용 제품 비중이 늘어난 믹스 효과라는 뜻
  ([서울경제](https://www.sedaily.com/article/20063718),
  [서울경제](https://www.sedaily.com/article/20063620)).
- **회사 자인**: SK하이닉스가 2026-07-29 실적발표에서 "일부 제품의 출하
  시점과 포트폴리오 구성이 혼합평균판매가격(ASP)에 영향을 줬다"고 밝혔고
  "하반기엔 이 요인이 점차 완화될 것"이라고 언급
  ([뉴스핌](https://www.newspim.com/news/view/20260729000286)).
- **수요 위축 신호 부재(반증)**: 8Gb DDR 고정가는 4월 $16 → 5월 $20 → 6월
  $21 → 7월 $24로 계속 상승 중, 128Gb 낸드도 동반 상승
  ([Investing.com](https://kr.investing.com/news/economy-news/article-2040445)).
  7월까지 7개월 연속 전년비 100%+ 성장 유지
  ([ZDNet](https://zdnet.co.kr/view/?no=20260814105900)). 한화투자증권은
  "물량·단가로 보면 수요 위축 조짐은 미약"하며 "하반기에도 200%+ 성장
  예상"이라고 코멘트
  ([파이낸셜뉴스](https://www.fnnews.com/news/202608110630440392)).

### 가설 B — 수요 자체가 줄었을 가능성 (2026-08-17 사용자 제기, 미검증 리스크 시나리오)

사용자 제기: **"수요가 줄어서 수출량이 줄었을 수 있다"**, **"반도체가
비싸져서 엔드단(서버·기기) 매출이 줄어든 영향이 있을 수 있다"** — 즉
가격 급등(8Gb DDR $16→$24, +50%/4개월) 자체가 다운스트림 수요를 파괴하는
경로. 가설 A를 뒷받침하는 이번 조사에서는 이 가설을 직접 뒷받침하는
증거를 찾지 못했다(오히려 고정가·물량 둘 다 상승 중이라는 반대 방향
기사가 다수) — **그러나 배제된 것은 아니다.** 아직 확정치가 아닌
상반월/월 단위 관찰 1~2개월만으로는 두 가설을 통계적으로 구분할 표본이
부족하다.

**이 가설을 지지/반증할 데이터**(§3 체크리스트에 반영):
- 엔비디아·하이퍼스케일러 주문 축소·연기 (HBM Cycle Score 붕괴조건②③과
  동일 지표, [hbm-cycle-score.md](hbm-cycle-score.md) 참고)
- 서버 OEM·스마트폰·PC 완제품 출하량 둔화 (다운스트림 판매 데이터 —
  이 저장소에 아직 자동 수집 경로 없음, 수동 확인 필요)
- 하이퍼스케일러 CapEx 가이던스 하향 (`sources/hyperscaler-capex.csv`,
  SEC EDGAR 자동수집 기존 인프라 재사용 가능)
- 고객사 채널 재고 급증 (HBM Cycle Score 축 "고객사 재고 센티먼트"와 동일)
- ASP(고정가) 자체가 하락 전환 — 지금까지는 계속 상승 중이라 이 신호는
  아직 안 켜짐

---

## 3. "다시 전고점을 향해갈 조건" — 매 10일/20일 발표마다 체크

| # | 체크 항목 | 회복 신호 | 추가 둔화(가설 B 강화) 신호 |
|---|---|---|---|
| 1 | 반도체수출 절대금액(레벨)이 전월 대비 반등했는가 | 전월보다 상승 | 3개월 연속 하락 |
| 2 | YoY 둔화 속도(2차 미분)가 줄어드는가 | 둔화 폭 축소 | 둔화 가속 |
| 3 | 6월 정점($44.8B) 재돌파 여부 | 재돌파 | $41B 밑으로 추가 하락 |
| 4 | 8Gb DDR·HBM 고정가 추이 | 계속 상승 | 하락 전환(적신호) |
| 5 | 하이퍼스케일러 CapEx 가이던스 | 유지·상향 | 하향 조정 |
| 6 | HBM Cycle Score 붕괴조건⑤(반도체수출 YoY<10%) | 여유 있게 미충족 | 근접·충족 |

**판정 원칙**: 1~2개 신호만으로 가설을 바꾸지 않는다
([concept-lifecycle-maturity.md](concept-lifecycle-maturity.md)의 4-condition
원칙과 동일 — 3회+ 반복, 기존 가정 위반, 신변수, 통계적 유의성이 함께
갖춰져야 가설 전환). 08-21(1~20일 잠정치)·09-01(7월 확정치)이 표본을
2배 이상 늘리는 다음 관찰점.

---

## 4. 자동 갱신 경로

`scripts/correlation_analysis.py`의 `render_markdown()`/
`render_levels_markdown()`이 매번 파이프라인 실행 시 "관찰 포인트" 문단을
**데이터에서 계산해서** 생성한다(전월 대비 방향, 6월 정점 대비 거리) —
하드코딩된 서술이 아니라 최신 `data/manual_inputs/exports.yaml` +
`exports_preliminary.yaml` 값에서 매번 다시 계산되므로 새 잠정치가
들어올 때마다 자동으로 갱신된다.

이 재계산은 관세청 10일/20일 잠정치 자동 갱신 Routine(매월 11일·21일
13:00 KST 발동, `data/manual_inputs/exports_preliminary.yaml` 갱신 →
`python -m scripts.correlation_analysis` 재실행 → 커밋)이 이미 매번
트리거한다 — 별도 스케줄을 새로 만들 필요 없이 기존 자동화에 얹었다.

---

## 관련

- [HBM Cycle Score](hbm-cycle-score.md) — 붕괴조건⑤가 이 페이지의 반도체수출
  YoY와 같은 지표를 다른 임계값(10%)으로 사용
- [monitoring/exports-price-levels-trend.md](../../monitoring/exports-price-levels-trend.md) —
  레벨(달러) 차트·표
- [monitoring/exports-price-correlation.md](../../monitoring/exports-price-correlation.md) —
  %YoY 차트·표, 진행 중인 달 잠정치 섹션
- [monitoring/semiconductor-export-peak-recovery-status.md](../monitoring/semiconductor-export-peak-recovery-status.md) —
  이 프레임워크의 일일/발표일 체크 이력(append-only)
