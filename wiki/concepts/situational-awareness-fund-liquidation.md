---
title: Situational Awareness LP 강제청산 — 7월 급락·급반등의 숨은 원인
created: 2026-08-02
updated: 2026-08-02
tags: [hedge-fund, leverage, margin-call, citadel, sk-hynix, market-mechanics, daily-tracking]
---

## 핵심 요약

**⚠️ 2026-08-02 밤 규모 재검증 후 수정**: 이 사건은 사실관계 자체는
다수 독립 매체로 확인됐지만, 최초 작성 시 "SK하이닉스·코스피·삼성전자
전체의 급등을 이 헤지펀드가 설명한다"는 식으로 인과의 크기를
**과대평가**했다. 사용자의 지적(펀드의 SK하이닉스 보유 규모가 시가총액
대비 몇 %냐는 질문)으로 실제 계산해보니, SA의 SK하이닉스 특정 포지션은
SK하이닉스 시가총액의 **1% 미만**이고 코스피 전체·삼성전자(SA 비보유
종목) 시가총액 대비로는 **반올림 오차 수준**이다. 즉 이 펀드의 포지션
크기가 "기계적으로" 코스피·삼성전자 랠리까지 일으켰다는 설명은
**성립하지 않는다** — 근거는 아래 "규모 재검증" 섹션 참고. 이 사건은
SK하이닉스 자체의 단기 변동성에 기여했을 가능성이 있는 **여러 요인 중
하나**로, 이 위키가 지금까지 추적해온 [CXMT 공포](us-china-tech-competition-hbm.md)·
[빅테크 CapEx 확정](sk-hynix-analyst-thesis-checkpoints.md) 같은
펀더멘털 서사를 대체하지 않는다. 사용자가 시청한 유튜브 영상 요약을
계기로 웹서치 교차검증(CNBC·Bloomberg·TechTimes·SpotGamma·Yahoo
Finance·Forbes·Benzinga·CNN 등 다수 독립 매체 일치)해 사건 자체는
사실로 확인했다.

## 사건 개요

**Situational Awareness LP(SA)** — OpenAI 슈퍼얼라인먼트팀 출신
24~25세 리오폴드 아셴브레너(Leopold Aschenbrenner)가 2024년 9월 설립한
AI 전문 헤지펀드. 2026년 6월까지 누적 수익률 약 **+439%~1,500%+**,
운용자산 **약 $45B**까지 성장 — 단 **약 4배 레버리지**로 달성한 수치.

### 타임라인

| 시점 | 사건 |
| --- | --- |
| 2024-09 | SA 설립, 초기자본 약 $225M |
| ~2026-06월말 | 누적수익률 +439%(수수료 후), AUM $45B로 성장 |
| **2026-07-29(수)** | 나스닥 -1.7~2.1%. 촉발: **SK하이닉스 2분기 실적 컨센서스 미달**(이 위키가 이미 추적 중이던 사건, [체크포인트⑨](sk-hynix-analyst-thesis-checkpoints.md) 참고) + 유가 급등 + 매파적 FOMC 서프라이즈 |
| 2026-07(한달간) | SA 집중 보유종목(**SK하이닉스**·CoreWeave·Nebius·Micron·Bloom Energy)이 **35~47% 하락**, Adobe 등 소프트웨어 숏포지션도 역방향으로 손실 — 4배 레버리지 구조에서 담보가치 붕괴 |
| **2026-07-29~30** | 3개 프라임브로커(골드만삭스·JP모건·BofA) 동시 마진콜 발동, 24시간 긴급 협상 |
| **2026-07-30** | SA가 전체 공개주식 포트폴리오를 **켄 그리핀의 시타델(Citadel)에 통째로 매각** — 규모 약 **$16B**, **월가 역사상 최대 긴급 블록딜**. SA는 앤트로픽 비상장 지분($5B) 등을 남기고 소형 사모 비히클로 축소(AUM $45B→약 $10B) |
| **2026-07-31** | 강제매도 공포(overhang)가 해소되며 **SOX +8.19%, 코스피 +17.91%(역대최고), 삼성전자 +27%, SK하이닉스(국내) +29.95%(17년만 상한가)** — SA가 보유했던 종목들이 정확히 이 방향으로 가장 강하게 반등 |

### SK하이닉스와의 직접 연결고리

SA는 미국 상장(ADR)된 SK하이닉스를 **명시적으로 집중 보유**하고 있었다
— CoreWeave·Nebius·Micron·Bloom Energy와 함께 "AI 인프라" 테마의 핵심
포지션 중 하나였다. 7월 한 달간 이들 종목이 35~47% 하락하며 SA의
레버리지 담보가 무너진 것 — 즉 **SK하이닉스 자체가 이 헤지펀드 붕괴의
당사자 종목 중 하나**였다.

## ⚠️ 규모 재검증 (2026-08-02 밤, 사용자 지적으로 진행)

사용자 질문: "그가 청산해야할 돈의 규모가 하이닉스 주가총액의 몇퍼센트나
되는거야? 그게 반도주 전체에 영향을 줬다고? 너무 과대해석하는 거
아닌가?" — 결론부터: **정확한 지적이었다.** 계산 없이 "그럴듯한 서사"에
넘어갔던 것이 최초 버전의 오류다.

**입력값**(사용자 제공 스크린샷 기준):
- SK하이닉스 시가총액 ≈ 1,254.98조원 ÷ 1,450원/달러 ≈ **$865.5B**
- SA 전체 블록딜(모든 종목 합산) = **$16B**

**SK하이닉스가 이 $16B 중 차지했을 비중별 시산**(SA의 집중종목은
SK하이닉스·CoreWeave·Nebius·Micron·Bloom Energy 5개 정도로 보도됨,
정확한 종목별 비중은 미공개):

| SK하이닉스 가정 비중 | SK하이닉스 특정 포지션 | SK하이닉스 시총 대비 |
| --- | --- | --- |
| 15% | $2.40B | 0.28% |
| 20% | $3.20B | 0.37% |
| 30%(가장 후하게 잡아도) | $4.80B | 0.56% |

**결론 1 — 코스피/삼성전자 전체 랠리 설명력: 없음.** 코스피 전체
시가총액(수조 달러 규모)이나 삼성전자 단독 시가총액(SA는 삼성전자를
보유하지도 않았음) 대비로는 $2.4~4.8B는 반올림 오차 수준이다. "SA
포지션 크기가 삼성전자 +27%·코스피 +17.91%를 기계적으로 일으켰다"는
설명은 **규모상 성립하지 않는다** — 최초 버전이 과대해석한 지점.

**결론 2 — SK하이닉스 자체 변동성 설명력: 제한적으로 가능.** 시가총액이
아니라 **일평균 거래대금**과 비교하면 얘기가 다르다. SK하이닉스
일평균 거래대금이 통상 수천억~1조원대(추정, 정밀 확인 안 됨)라면,
$2.4~4.8B(약 3.5~7조원) 규모를 하루이틀 안에 강제매도했다는 것은 **정상
거래대금의 여러 배**에 해당할 수 있다 — 이 경우 SK하이닉스 "개별
종목의" 단기 가격 변동(7/29~31 구간)에는 유의미하게 기여했을 가능성이
남는다. 다만 이것도 정밀 검증(SK하이닉스 ADR·국내 거래대금 실측치)
없이는 확정할 수 없는 **가설**이다.

**결론 3 — 그렇다면 코스피·삼성전자 랠리는 뭘로 설명하나?** 이 펀드
사건과는 별개의 메커니즘으로 봐야 한다: (a) 이 위키가 이미 추적 중인
독립적 펀더멘털 호재(아마존·MS CapEx 확정, 삼성 공급부족 가이던스),
(b) "레버리지 낀 AI 펀드가 무너질 수 있다"는 공포가 7/29~30에 AI
테마 전반의 **심리적 디레버리징**(위험자산 전반 회피)을 유발했다가,
시타델 인수로 그 공포가 풀리며 **동일 테마 전반의 안도 랠리**로
번졌을 가능성 — 이건 SA의 포지션 "크기"가 아니라 **사건이 만든
공포/안도라는 심리적 전염**이 메커니즘이라는 뜻이다. 크기로 설명되는
인과와 심리 전염으로 설명되는 인과는 증거 기준이 다르며, 후자는 정성적
정황(타이밍 일치)일 뿐 정량적으로 입증되지 않았다.

**요컨대**: SA 사건은 실제로 일어났고 SK하이닉스가 관련 종목 중
하나였다는 사실(fact)과, 그 사건이 코스피·삼성전자까지 포함한 시장
전체 랠리의 규모를 "기계적으로" 설명한다는 해석(interpretation)은
분리해야 한다. 전자는 확인됨, 후자는 **과대해석이었고 지금 철회한다.**

## 이 위키의 기존 프레임에 주는 함의

### 1. 급락(7/28~30)의 원인 재해석

기존 추적: CXMT IPO 쇼크 + 실적 컨센서스 미달 + 중국 노광장비 국산화
공포(전부 사실, [us-china-tech-competition-hbm.md](us-china-tech-competition-hbm.md)·
[checkpoints.md](sk-hynix-analyst-thesis-checkpoints.md) 참고).

**추가된 축**: SK하이닉스의 7/29 실적 미달이 나스닥 전체를 흔들었고, 그
낙폭이 SA의 4배 레버리지 담보를 무너뜨려 **다른 종목(CoreWeave·Nebius
등)의 강제매도까지 SK하이닉스와 한 묶음으로 얽혔다** — SK하이닉스
개별 악재가 SK하이닉스 스스로의 낙폭보다 훨씬 큰 시장 전체 충격으로
증폭된 경로 중 하나가 바로 이 레버리지 사슬이었을 가능성이 있다.

### 2. 급반등(7/31)의 원인 재해석 — 가장 중요한 발견

기존 추적: 아마존·MS CapEx 확정 + 삼성 "2028년까지 공급부족" 가이던스
(전부 사실, 독립적으로 검증된 진짜 호재).

**추가된 축**: 시타델이 SA의 전체 포지션을 하루 만에 흡수하면서
**"조만간 시장에 강제로 쏟아질 매물"이라는 공포(overhang) 자체가
사라졌다** — 이는 수요가 늘어난 게 아니라 **비정상적인 잠재 매도
압력이 제거된 것**이다. 두 가지는 시장에 같은 방향(급등)으로 나타나지만
의미가 다르다:
- 펀더멘털 호재(CapEx·공급부족 가이던스) → **지속 가능한 재평가**
- 강제매도 overhang 해소 → **일회성 안도 랠리(relief rally)**, 매도자가
  없어졌다는 것이지 매수 수요가 새로 생겼다는 뜻은 아님

7/31 랠리는 이 둘이 **같은 날 겹쳐서 증폭**된 것으로 보인다 — 어느
쪽이 얼마나 기여했는지는 정량적으로 분리하기 어렵다. 단, 위 "규모
재검증" 섹션 기준으로는 overhang 해소가 **SK하이닉스 자체 가격**에는
유의미했을 수 있어도, **코스피·삼성전자 전체 랠리의 크기**를 설명하는
비중은 크지 않았을 것으로 본다 — 후자는 펀더멘털 호재 쪽 비중을 더
높게 잡는 것이 타당하다.

### 3. [찐반등 신호③(외국인 귀환)](market-cycles-leverage-risk.md) 재해석 필요

7/31 외국인 순매수 **+3조 5,883억원**(KIS API 수집 이래 단일 최대)을
지금까지 "외국인 수요 복귀"의 초기 신호로 추적해왔다. **이 중 일부는
시타델 블록딜 주변의 포지션 리밸런싱·차익거래일 가능성**이 있다 —
시타델 같은 대형 마켓메이커/헤지펀드가 급하게 인수한 포지션을 정리·
헤지하는 과정에서 관련국 시장(한국)의 파생·현물 수급에도 영향을 줬을
수 있다. 이 가설은 **검증되지 않았다** — 다만 "20일 지속 기준 미충족"
이라는 기존의 신중한 판정(1일 데이터로 확정하지 않음)이 결과적으로
옳은 접근이었음을 재확인한다.

### 4. [패닉 회복 신호](panic-recovery-signals.md) "회복 초입" 판정 — 신중론 강화

기존 "회복 초입" 승격 근거(Tier1 6건 확인 + 가격 동반 반응)는 여전히
유효하다. 다만 이 사건은 **가격 반응의 상당 부분이 "SA 매물 소화"라는
일회성 요인**일 수 있다는 신중론을 추가한다 — 신용융자잔고發 신중론
(8/1 발견)에 이은 **두 번째 신중 요인**. "회복 진행중"으로의 추가
승격은 이 일회성 효과가 빠진 이후에도 강세가 유지되는지로 판단해야
한다.

### 5. [HBM Cycle Score](hbm-cycle-score.md) 외국인수급 축 해석 주의

축 자체의 점수 산정 방식(20일 누적 순매수 금액)은 그대로 두되, 향후
"외국인수급" 축이 급변할 때는 **이런 일회성 대형 거래(블록딜·마진콜
청산)가 배경에 있는지 먼저 확인**하는 습관을 들일 것 — 원인 구분 없이
숫자만 보면 "펀더멘털 수요 개선"으로 오독할 위험이 있다.

## 월요일(8/3) 전망에 주는 시사점

- SA의 overhang이 시타델 인수로 **완전히 해소**됐다면, 8/3 이후로는 이
  요인이 더 이상 매도 압력으로 작용하지 않는다 — 긍정적
- 다만 시타델 자신이 인수한 $16B 규모 포지션을 **자체 리스크 관리
  차원에서 점진적으로 재조정(헤지·일부 매도)할 가능성**은 남아있다 —
  이 경우 8/3 이후에도 간헐적 매물 출회 가능성 배제 불가, 확정 사실
  아님이라 추적 필요
- SK하이닉스의 진짜 펀더멘털(HBM 수요·CapEx 확정·CXMT 약세)은 이
  사건과 무관하게 그대로 유효 — 7/31 SK하이닉스 개별 급등폭 중 일부를
  펀더멘털만으로 해석하면 과대평가할 위험은 남아있음(규모상 소폭)
- 반대로 **코스피·삼성전자 전체 랠리를 이 헤지펀드 사건으로 설명하는
  것은 규모상 근거가 없다** — 이 부분은 펀더멘털(CapEx·공급부족
  가이던스)과 심리적 전염(정성적, 미검증)으로 봐야 한다. 이게 8/2 밤
  규모 재검증 이후의 핵심 교훈이며, 최초 버전의 과대해석을 정정한
  내용이다

## Sources

- [CNBC — Leopold Aschenbrenner Situational Awareness fund: $45B to fire sale](https://www.cnbc.com/2026/07/31/leopold-aschenbrenner-situational-awareness-fund-fire-sale.html)
- [CNBC — AI investor forced to unwind all public stock positions](https://www.cnbc.com/2026/07/30/leopold-aschenbrenners-hedge-fund-is-facing-steep-ai-losses.html)
- [Bloomberg — Aschenbrenner Hedge Fund Situational Awareness Unwinding Trades](https://www.bloomberg.com/news/articles/2026-07-30/aschenbrenner-hedge-fund-situational-awareness-seeks-capital-after-loss-ft-says)
- [TechTimes — Citadel Buys Situational Awareness Portfolio as 4x Leverage Ends AI Fund's 1,000% Run](https://www.techtimes.com/articles/322285/20260730/citadel-buys-situational-awareness-portfolio-4x-leverage-ends-ai-funds-1000-run.htm)
- [SpotGamma — Anatomy of a Margin Call: How Situational Awareness LP Unwound a $20 Billion AI Book in One Trade](https://spotgamma.com/situational-awareness-unwind-margin-call-ai/)
- [Benzinga — Wonder Boy Blowup Sparks Massive Semiconductor Rally, Korea Up 18%](https://www.benzinga.com/Opinion/26/07/60851764/wonder-boy-blowup-sparks-massive-semiconductor-rally-korea-up-18-amazon-helps-apple-disappoints)
- [CNN Business — The market's big AI doubts are exposing the riskiest players](https://www.cnn.com/2026/07/31/business/situational-awareness-citadel-ai-trade)
- [Yahoo Finance — AI wizkid Leopold Aschenbrenner forced to sell entire portfolio after rout](https://finance.yahoo.com/technology/ai/articles/ai-wizkid-leopold-aschenbrenner-seeks-113210756.html)
- [Forbes — AI Stocks Face A New Risk As Hedge Fund Leverage Unwinds](https://www.forbes.com/sites/jimosman/2026/07/30/ai-stocks-face-a-new-risk-as-hedge-fund-leverage-unwinds/)
- [market-cycles-leverage-risk.md](market-cycles-leverage-risk.md) (찐반등 신호③ 재해석 대상)
- [panic-recovery-signals.md](panic-recovery-signals.md) ("회복 초입" 판정 신중론 병기)
- [hbm-cycle-score.md](hbm-cycle-score.md) (외국인수급 축 해석 주의)
- [entities/sk-hynix.md](../entities/sk-hynix.md)
