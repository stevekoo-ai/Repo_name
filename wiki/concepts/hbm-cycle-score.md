---
title: HBM Cycle Score & 선행지표 조기경보 (HSEWS) — Framework Definition
created: 2026-07-24
updated: 2026-08-08
tags: [hbm, cycle-score, concept, framework, early-warning]
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
목표. 이 점수가 "가설이 깨지는 조건"을 추적한다면, 반대 방향(패닉이
풀리는 조건)은 [패닉 회복 신호 추적 프레임](panic-recovery-signals.md)이
담당 — 2026-07-30 신설, 매일 함께 확인할 것.

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
| 공급 확대 위험(경쟁사 캐파 증설, 수요증가율 대비) | 10 | 체크포인트 [⑦CXMT](sk-hynix-analyst-thesis-checkpoints.md)·⑧마이크론과 연동. **🔴 2026-08-04 신규 리스크 반영 필요**: UBS가 2027년 HBM 점유율을 삼성 41%·SK하이닉스 39%·마이크론 20%로 전망(SK하이닉스 1위 상실) — CXMT(범용 D램)와는 다른 **동급 경쟁사 기술 추격** 리스크, [체크포인트②](sk-hynix-analyst-thesis-checkpoints.md) 참고. 점수는 예측치 1건만으로 즉시 반영하지 않고 다음 체크에서 추가 검증 후 조정 여부 판단 |
| 고객사 재고 센티먼트(하이퍼스케일러 실적콜 키워드) | 10 | [하이퍼스케일러 고객 동향](sk-hynix-analyst-thesis-checkpoints.md) 섹션과 연동. **🆕 2026-08-06**: `scripts/daily_report.py`가 `sources/hyperscaler-capex.csv`(SEC EDGAR 실측)를 매일 인용하기 시작 — 단 논조(어닝콜 센티먼트) 판단 자체는 여전히 자동화 대상 아님, "CapEx가 실제로 얼마였나"라는 보조 숫자만 제공. ⚠ 이 CSV에서 end_date 기준 최신 분기가 GOOGL 310일·MSFT 218일·AMZN 3,415일·META 402일 전으로 확인돼(2026-08-06 점검) **전부 스테일** — SEC 라이브 접속이 이 세션에서 막혀 있어 직접 재검증 못 함, GitHub Actions 재실행으로 최신화 필요(상세: [automation-vs-ai-narrative-roadmap.md "SEC EDGAR 데이터 정합성 버그"](automation-vs-ai-narrative-roadmap.md)) |

**판정 기준**: 80점 이상 = 강세 유지 / 60~80점 = 경계 / 60점 미만 = 사이클
꺾임 경고.

**⚠️ 이 스코어의 구조적 사각지대 (2026-08-07 신설)**: 위 6축은 **전부
SK하이닉스 자신 또는 직접 고객의 지표**다 — 즉 "주도주가 이미 흔들린
뒤"에야 신호가 뜬다. 사용자 지적("펀더멘털 붕괴는 주도주에서 가장 늦게
나타난다")대로 이건 조기경보로서 한계가 명확하다. 그 공백은
**[AI 밸류체인 변두리 모니터](ai-value-chain-periphery-monitor.md)**가
담당한다 — 전력·냉각·기판·광통신·후공정 등 체인 최말단의 백로그·수주잔고를
추적해 **주도주보다 먼저 꺾이는지**를 본다. 2026-08-07 전수 조사 결과
변두리는 오히려 전부 강했고(균열 없음), 대신 **데이터센터 착공률**(2026
계획 12~16GW 대비 실착공 5GW)이라는 새로운 감시 지표가 발견됐다.

**🎯 외국인수급 축(15점) 가중치는 국면에 따라 달라져야 한다 (2026-08-04
발견, [market-cycles-leverage-risk.md 1-4-2](market-cycles-leverage-risk.md)
정량 분석)**: 실제 3.6년 데이터로 계산한 결과, 외국인 지분율과 주가의
상관계수가 국면마다 정반대로 뒤집힌다 — 2023~2024년 랠리 초입 r=+0.93
(동행), 2024년 하반기~2026년 상반기 랠리 후반부 r=-0.98(역상관, 개인
레버리지 매수가 주도한 걸로 추정), **2026년 7월 급락~반등 국면
r=+0.84(동행 복귀)**. 즉 이 축의 배점(15점)이 항상 같은 무게로
움직인다고 가정하면 안 된다 — **"랠리 후반부·탈동조화" 체제에서는
외국인 매도가 나와도 가격에 큰 영향이 없을 수 있지만, 지금처럼
"급락~회복" 체제에서는 외국인 수급이 다시 가격을 강하게 좌우하는
1차 변수가 된다.** 현재(2026-08 초)는 아직 회복 국면 진행 중이라
이 축을 다른 시기보다 더 무겁게 볼 것 — 특히 붕괴조건④(외국인
20일 누적 순매도 전환)이 이 국면에서는 다른 국면보다 신뢰도 높은
경고로 봐야 한다는 뜻.

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

### 최신 확인 사항 (2026-07-24)

- **[FACT] TSMC CoWoS 수요 2년새 3배 증가**: 2024년 약 37만장 → 2025년
  약 67만장 → 2026년 약 100만장 전망. CoWoS-S·CoWoS-L 모두 완전매진,
  리드타임 52~78주. TSMC는 월 생산능력을 7.5~8만장에서 2026년말
  12~13만WPM까지 증설 중이나 그래도 예약 초과 상태.
- **[FACT] 엔비디아가 CoWoS의 절대 다수를 확보**: 2026~2027년 신규
  증설분의 절반 이상(약 80~85만장), 전체 CoWoS의 약 60%(약 60만장),
  CoWoS-L만 놓고 보면 70%+ 사실상 독점. GB300 NVL72(CoWoS-L 기반)가
  2026년 양산 출하의 중심.
- **판정: Bullish** — 주문 축소·지연 관련 부정 뉴스는 이번 체크에서
  검색되지 않음. 다음 체크에서 계속 추적, 특히 CoWoS 활용률이 95%
  이하로 내려가는지가 붕괴조건③의 핵심 감시 지점.

## 3. 가설이 깨지는 조건 (0~5, 사용자 제안 그대로 채택 + ⑤ 2026-08-05 추가)

"SK하이닉스 HBM 투자 가설 [유지]"가 깨지는 하드 트리거 — 리포트
맨 아래 진단 직전에 항상 표기:

| # | 조건 |
| --- | --- |
| ① | HBM ASP 5% 이상 하락 |
| ② | 엔비디아 주문 -10% |
| ③ | CoWoS 활용률 95% 이하 |
| ④ | 외국인 20일 누적 순매도 전환 |
| ⑤ | 🆕 한국 반도체 수출 YoY 증가율 10% 미만으로 하락 |

**⑤ 신설 배경(2026-08-05, 사용자 요청 "'반도체 수출 증가율'을 daily
report에 추가해줘! 증가율이 10% 밑으로 꺾이면 경고가 필요해")**: 산업통상부/관세청이
매월 1일(영업일) 발표하는 한국 반도체 수출액 YoY 증가율 — HBM Cycle
Score의 다른 5축(외국인수급·보유율·ASP·엔비디아&CoWoS·공급확대·고객재고)이
전부 SK하이닉스 종목 단위 또는 개별 고객사 단위 지표인 것과 달리, 이
지표는 **한국 반도체 산업 전체의 실물 수요를 정부 통계로 매달 확인하는
유일한 축**이라 붕괴조건에 추가할 가치가 있다고 판단. 자세한 추적은
[macro-indicators.md "반도체 수출 증가율 추적"](macro-indicators.md#반도체-수출-증가율-추적-신설-2026-08-05)
참고 — **월간 통계라 매일 갱신되지 않음**, 새 발표월 데이터가 나올
때만 이 조건이 재판정됨. 기준선: **2026-07 +178.8% YoY**(410억
달러, 14개월 연속 역대 최고) — 10% 문턱까지 크게 여유 있어 현재
미충족.

**2026-07-31 19:xx 저녁 체크(하루 최종 확정치) 기준 충족 개수: 🔴 1/5** —
④(외국인 20일 누적 순매도 전환)가 20일 누적 -5조 2,994억원으로 여전히
충족(단, 오늘 하루 외국인 순매수 +3조 5,883억원으로 20일 적자폭이
하루 만에 절반 가까이 축소). ①ASP·②엔비디아주문·③CoWoS·⑤수출증가율은
미충족 유지. **총점은 63→69/100** — 본주가 상한가(+29.95%, 17년 만)를 기록한
날의 확정치. 자세한 내용은 아래 체크 이력과 [1-4-1](market-cycles-leverage-risk.md) 참고.
(⑤는 2026-08-05 신설이라 이 시점 체크 이력 행에는 소급 반영되지 않음 —
신설 이후 행부터 5개 분모로 표기)

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

## Daily Tracking & Historical Check Log

**Framework definition only. For daily status and check history, see:**
**[📊 Monitoring: HBM Cycle Score Status](../monitoring/hbm-cycle-score-status.md)**

All dated check entries (2026-07-24 onward) are maintained in the monitoring page as an append-only audit trail.
This page contains framework definition only — score definition, axes, methodology, collapse conditions, and automation guidelines.

---

## 자동화

**2026-07-24 신설**: 아침·장초반·저녁 모든 Routine에 반영. 리포트 최상단에
"🚨 HBM Cycle Score" 섹션(점수+등급+붕괴조건 0/4)을 신규 추가, 별도로
"⚡ 선행지표: 엔비디아 주문 & CoWoS" 독립 섹션 신설. 실행 빈도는 하루
3회(07/10/19시 KST) 그대로 유지하기로 결정 — 매시간 실행은 웹검색
소스(TrendForce·DigiTimes 등) 자체가 시간 단위로 갱신되지 않아 비용 대비
정보 이득이 작다고 판단. Telegram/Slack/Discord 발송 제안은 채택하지
않음 — 기존 이메일 발송 체계(run_once_at 자동발동)가 이미 안정적으로
작동 중이라 별도 채널 구축의 실익이 낮음.

**2026-07-28 추가(PR #34)**: ①"공급확대" 축과 관련해 오래 방치돼 있던
버그 하나도 같이 발견·수정했다 — 브렌트/WTI 유가 프리셋(`us_brent`/
`us_wti`)을 7/26에 추가했다고 기록했지만 실은 작업 브랜치에만 있었고
`main`(Actions가 실제로 실행하는 브랜치)에는 반영된 적이 없어 한 번도
동기화되지 않았다. ②`sk-hynix-adr-quote.csv`도 생성 이래 비어 있었는데
원인은 KIS 해외주식 API의 필드명(`diff`/`rate`)이 실제 응답과 달랐던
것 — `|| true`가 이 실패를 조용히 삼키고 있었다. 둘 다 이번에 고쳐
main에 반영했고, 실제 계정으로 2회 검증(디버그 raw 조회 1회 + 전체
파이프라인 실행 1회)까지 마쳤다. 외국인 수급 축은 이제 (a) 20일 누적
순매도(investor-flow.csv) (b) 당일 보유율(price-snapshot.csv, 신설)
두 소스를 모두 KIS API로 확보한다.

## Sources

- [패닉 회복 신호 추적 프레임](panic-recovery-signals.md)
- 사용자가 제시한 HBM Supercycle Early Warning System(HSEWS) 설계
  (2026-07-24 채팅)
- [SK하이닉스 목표주가 근거 체크리스트](sk-hynix-analyst-thesis-checkpoints.md)
- [반도체 시장의 단기 수급 싸이클 vs 장기 펀더멘털](market-cycles-leverage-risk.md)
- [CXL & 차세대 메모리 트랙](cxl-next-gen-memory.md)
- [매크로 지표 트렌드 추적 — 반도체 수출 증가율](macro-indicators.md) (붕괴조건⑤, 2026-08-05 신설)
- [AI 밸류체인 변두리 모니터](ai-value-chain-periphery-monitor.md) (이 스코어의 조기경보 사각지대를 메우는 페이지, 2026-08-07 신설)
- [미중 기술경쟁 & HBM](us-china-tech-competition-hbm.md) (CXMT HBM3 재확인, 2026-08-06)
