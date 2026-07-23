---
title: HBM Cycle Score & 선행지표 조기경보 (HSEWS)
created: 2026-07-24
updated: 2026-07-24
tags: [hbm, cycle-score, nvidia, cowos, early-warning, sk-hynix, daily-tracking]
---

사용자가 제시한 "HBM Supercycle Early Warning System(HSEWS)" 설계를 반영한
종합 트래킹 프레임. 목적은 뉴스 요약이 아니라 **"SK하이닉스 투자 판단을
가장 먼저 깨뜨릴 수 있는 선행지표를 탐지하는 것"** — 보유자산의 절대
비중이 SK하이닉스인 상황에서, 가장 위험한 시나리오는 실적 부진이 아니라
"HBM ASP 하락 → 엔비디아 주문 둔화 → 고객 재고 증가 → 공급과잉 기대
형성"이라는 연쇄가 시장에 먼저 반영되는 것이라는 문제의식에서 출발.

기존 [9개 체크포인트](sk-hynix-analyst-thesis-checkpoints.md)와
[찐반등 4대 신호](market-cycles-leverage-risk.md)는 그대로 유지하고, 이
페이지는 **그 위에 얹는 요약 레이어**다 — 매 체크 리포트 최상단에 "숫자
두 개"(HBM Cycle Score, 붕괴조건 충족 개수)만 봐도 판단 가능하게 하는 것이
목표.

## 1. HBM Cycle Score (0~100)

6개 축으로 구성. 원안(사용자 제시)은 외국인수급·보유율·ASP·엔비디아·재고
5개 항목만 100점에 배분했는데, 공급 확대(STEP4)가 "가장 위험한 항목"이라고
서술해놓고 정작 배점에서 빠져있어 — 이 페이지에서 공급 확대를 정식 축으로
넣어 재배분했다. 엔비디아 주문과 CoWoS 활용률은 둘 다 "선행지표" 성격이 같아
하나의 축으로 합산.

| 축 | 배점 | 데이터 출처 |
| --- | --- | --- |
| 외국인 수급(SK하이닉스 종목 순매수 1/5/20/60일 누적) | 15 | KRX, FnGuide, 네이버증권 |
| 외국인 보유율 변화(전일 대비 %p) | 15 | KRX, FnGuide |
| HBM ASP(주간 %변화) | 25 | TrendForce, DRAMeXchange, SemiAnalysis |
| 엔비디아 주문 & CoWoS 활용률 (§2 참고) | 25 | The Information, DigiTimes, SemiAnalysis, TSMC 발표 |
| 공급 확대 위험(경쟁사 캐파 증설, 수요증가율 대비) | 10 | 체크포인트 [⑦CXMT](sk-hynix-analyst-thesis-checkpoints.md)·⑧마이크론과 연동 |
| 고객사 재고 센티먼트(하이퍼스케일러 실적콜 키워드) | 10 | [하이퍼스케일러 고객 동향](sk-hynix-analyst-thesis-checkpoints.md) 섹션과 연동 |

**판정 기준**: 80점 이상 = 강세 유지 / 60~80점 = 경계 / 60점 미만 = 사이클
꺾임 경고.

축별 산정은 정성적 판단에 의존하는 구간이 많다(예: 재고 센티먼트는 실적콜
키워드를 AI가 감성분석). 숫자를 지어내지 않는다는 원칙상, 데이터가
불충분하면 해당 축은 "미확인 — 직전 값 유지"로 표기하고 총점 계산에서
제외하지 않되 근거를 리포트에 명시한다.

## 2. 선행지표: 엔비디아 주문 & TSMC CoWoS 활용률 (신규 Tier-1, 기존 미추적)

기존 위키에서 엔비디아는 체크포인트②(HBM4) 하위에서 "HBM4 출하량 20~30%
축소" 같은 개별 뉴스로만 산발적으로 잡혔다(2026-07-16 사례). CoWoS는
지금까지 전혀 추적되지 않았다. 이 둘을 하이퍼스케일러 섹션과 분리해
독립 Tier-1 섹션으로 승격한 이유는, 제안서 논리대로 **CoWoS 활용률 →
엔비디아 주문 → HBM 발주**로 이어지는 연쇄가 실제 최종 수요(하이퍼스케일러
CapEx)보다 먼저 꺾이기 때문 — 이미 확정된 CapEx 가이던스보다 한 단계 더
앞선 신호.

- **엔비디아 주문**: Blackwell/GB300 등 세대별 주문량·출하량 변화. 검색
  키워드: "Nvidia order cut", "Nvidia CoWoS reduction", "Nvidia GB300
  shipment", "Blackwell delay"
- **TSMC CoWoS 활용률**: 월별/분기별 capacity·utilization·expansion.
  출처: Digitimes, TrendForce, TSMC 실적발표

**개별 신호 판정**: Bullish(주문 유지·확대) / Neutral(변동 없음) /
Bearish(주문 축소·활용률 하락)

## 3. 가설이 깨지는 조건 (0~4, 사용자 제안 그대로 채택)

"SK하이닉스 HBM 투자 가설 [유지]"가 깨지는 하드 트리거 4개 — 리포트
맨 아래 진단 직전에 항상 표기:

| # | 조건 |
| --- | --- |
| ① | HBM ASP 5% 이상 하락 |
| ② | 엔비디아 주문 -10% |
| ③ | CoWoS 활용률 95% 이하 |
| ④ | 외국인 20일 누적 순매도 전환 |

**2026-07-24 기준 충족 개수: 0/4** (모두 최초 설정, 아직 실측 데이터
없음 — 다음 체크부터 채움)

## 4. 기존 트래킹과의 관계 (중복 방지)

- **외국인 수급 정량화**는 [market-cycles-leverage-risk.md "1-4-1"](market-cycles-leverage-risk.md)에서
  SK하이닉스 종목 기준으로 별도 추적 — 기존엔 코스피 전체 순매수를
  프록시로 썼는데, 이 갱신부터 종목 특정 수치를 우선한다.
- **HBM ASP**는 체크포인트①②에 이미 있는 방향성 판정에 주간 %수치와
  "3주 연속 하락 = 경고" 규칙만 추가 — 별도 페이지로 안 만듦.
- **공급 확대**는 체크포인트⑦(CXMT)·⑧(마이크론)·[CXL 경쟁사 뉴스룸](cxl-next-gen-memory.md)과
  동일한 소스를 재사용, "수요증가율 대비 공급증가율" 비교 프레임만 추가.
- **고객사 재고**는 [하이퍼스케일러 고객 동향](sk-hynix-analyst-thesis-checkpoints.md) 섹션에
  기업별 재고 센티먼트 점수(0~10)를 하위 필드로 추가.

## 체크 이력

(최초 설정, 2026-07-24 — 실측 데이터는 다음 체크부터)

## 자동화

**2026-07-24 신설**: 아침·장초반·저녁 모든 Routine에 반영. 리포트 최상단에
"🚨 HBM Cycle Score" 섹션(점수+등급+붕괴조건 0/4)을 신규 추가, 별도로
"⚡ 선행지표: 엔비디아 주문 & CoWoS" 독립 섹션 신설. 실행 빈도는 하루
3회(07/10/19시 KST) 그대로 유지하기로 결정 — 매시간 실행은 웹검색
소스(TrendForce·DigiTimes 등) 자체가 시간 단위로 갱신되지 않아 비용 대비
정보 이득이 작다고 판단. Telegram/Slack/Discord 발송 제안은 채택하지
않음 — 기존 이메일 발송 체계(run_once_at 자동발동)가 이미 안정적으로
작동 중이라 별도 채널 구축의 실익이 낮음.

## Sources

- 사용자가 제시한 HBM Supercycle Early Warning System(HSEWS) 설계
  (2026-07-24 채팅)
- [SK하이닉스 목표주가 근거 체크리스트](sk-hynix-analyst-thesis-checkpoints.md)
- [반도체 시장의 단기 수급 싸이클 vs 장기 펀더멘털](market-cycles-leverage-risk.md)
- [CXL & 차세대 메모리 트랙](cxl-next-gen-memory.md)
