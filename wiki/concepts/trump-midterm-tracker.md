---
title: 트럼프 2026 중간선거 트래커
created: 2026-07-30
updated: 2026-07-30
tags: [politics, us-midterm, trump, daily-tracking, macro]
---

2026년 11월 미국 중간선거를 앞두고, 트럼프 대통령이 승리하는 데 유리한
요인과 불리한 요인을 5개 카테고리로 나눠 매일 추적하는 페이지. SK하이닉스
투자와의 접점은 간접적이다 — 의회 구도 변화는 관세·대중국 정책·재정정책의
지속가능성에 영향을 주고, 중동·이민 이슈는 [거시국면(G/I/L)](macro-regime-history.md)의
유가·인플레이션 트랙과 겹친다. 다만 이 페이지 자체는 SK하이닉스 체크포인트나
HBM Cycle Score와는 **독립적인 트랙**으로 관리한다.

## 추적 방식

**기본 표기는 3단계**: 🟢유리 / ⚪중립·불명확 / 🔴불리, 그리고 전일 대비
추세를 함께 표기: ↗개선중 / →횡보 / ↘악화중.

**단, 큰 이슈나 변화가 있을 때는 기호만으로 끝내지 않고 반드시 구체적인
내용(사건, 수치, 날짜, 출처)을 함께 서술한다** — 이게 이 페이지의 핵심
원칙이다. 기호는 한눈에 보기 위한 요약일 뿐, 실제 판단 근거는 항상 텍스트로
남긴다.

데이터 소스는 전부 웹검색(GitHub Actions 자동화 대상 아님) — 여론조사
기관(Emerson, Quinnipiac, Harvard CAPS/Harris, CBS News, AP-NORC 등)의
최신 발표를 우선하고, 여러 여론조사가 갈리면 범위(range)로 병기한다.
숫자를 지어내지 않는다는 원칙은 이 페이지에도 동일하게 적용된다.

## 5개 카테고리 & 세부 항목

### 1. 🏛️ 정치
- 국정 지지율(approval rating) 추이 — **현재: 32~39% 범위**(조사기관마다 편차 큼, 아래 스코어보드 참고), 집권 2기 들어 지속 하락세
- 제네릭 밸럿(공화당 vs 민주당 지지율 격차) — **현재: 민주당 D+6~D+11 우위**(조사마다 편차)
- 당내 결속 vs 이탈 — 공화당 이견 의원 재선 전망, 경선 개입 성과 — **현재: 이번 체크까지 구체 사례 미확인**
- 사법 리스크·스캔들 — **현재: 이번 체크까지 구체 사례 미확인**
- 개인 리스크(건강·나이 등, 이슈화될 때만) — **현재: 특이사항 없음**

### 2. 💰 경제
- 체감 물가(CPI, 특히 식료품·에너지) — **현재: 정부 셧다운으로 10월 통계 자체가 불확실**(아래 참고), 개별 수치는 미확인
- 고용지표(실업률, 신규고용) — **현재: 셧다운 여파로 데이터 공백 우려, 실측치는 미확인**
- 증시 성과(S&P500·다우) — **현재: 이번 체크에서 별도 확인 안 함**(SK하이닉스 체크 쪽 데이터와 중복되므로 다음 체크에서 필요시 보완)
- 관세정책 실질효과 논쟁(물가상승 vs 제조업 고용효과) — **현재: 대법원이 트럼프의 IEEPA발 관세를 위헌 판결(6-3, 2026-02) → 트럼프가 "새 관세도 사실상 동일 효과"라며 대체 관세 재추진 중(2026-07-28 발언), 환급 규모 $1,000~1,300억 추산**
- Fed와의 마찰(금리 정책 갈등) — **현재: 7/30 FOMC 매파적 동결(해맥·카시카리·로건 인상 소수의견) — 마찰은 있으나 격화 조짐은 아직 없음. [OPINION, 김광석 교수 전망]** 중간선거를 앞두고는 통화정책보다 **재정정책에 의한 유동성 공급**이 시장의 핵심 변수가 될 것이라는 시각(정부의 적극적 재정 투입 전망) — 검증된 사실 아닌 예측, 다음 체크에서 실제 재정지출 동향으로 확인 필요. [macro-regime-history.md](macro-regime-history.md)의 1968-01형 애널로그(재정발 유동성 확대) 논의와 교차연동
- **(2026-07-30 발견) 정부 셧다운發 통계 공백** — 10월 노동시장·물가
  데이터가 셧다운으로 수집되지 않아 "영구적으로 발표 안 될 수 있다"는
  백악관 발표 — 경제 성적표 자체를 판단하기 어렵게 만드는 이례적 리스크,
  별도 하위항목으로 계속 추적

### 3. ⚔️ 전쟁/외교
- 중동(이란-이스라엘) 긴장도 — [거시국면 유가 트랙](macro-regime-history.md)과 교차연동 — **현재: 7월 휴전 종료·재격화, 후티 반군 홍해 항행금지 선언(7/20) — 불리 방향 지속**
- 우크라이나 전쟁 관련 미국 역할 성과/평가 — **현재: 미-우크라이나가 새 평화안 조율 중, 젤렌스키-위트코프/커슈너 협의, 트럼프-젤렌스키 회동 가능성(7/28 그레이엄 상원의원 장례식 계기), 크렘린(페스코프)도 "협상 개방적"(7/23 발언) — 중동과 달리 이 축은 오히려 개선 조짐**
- 대중국 관계(무역전쟁·대만 등) — SK하이닉스 체크포인트⑦과 접점 — **현재: 정치적 차원의 확인된 신규 이슈는 없음. [OPINION, 김광석 교수 전망(2026-07-30 INGEST)]** 9월 미중 정상회담을 앞두고 양국이 "약속대련" 식의 평화 국면("디센트 피스")을 11월 중간선거까지 유지할 것이라는 전망 제기 — 중국산 생필품 수입 확대가 미국 물가 안정에 기여할 가능성도 함께 언급. 아직 검증된 사실이 아니라 한 전문가의 예측이므로 [FACT]로 승격하지 않고 다음 체크에서 실제 정상회담 일정·관세 동향으로 교차확인할 것 (상세: [sources/kim-kwangsuk-2026h2-outlook-2026-07-30.md](../../sources/kim-kwangsuk-2026h2-outlook-2026-07-30.md))
- 해외 군사개입 관련 여론(사상자·장기화 피로감) — **현재: 별도 수치 미확인**

### 4. 🛂 이민
- 국경 통제 성과 지표(정부 발표 불법입국 건수 등) — **현재: 취임 후 누적 강제추방 60만+, 자진출국 190만+(합계 250만+ 출국), ICE 인력 1만→2.2만 명으로 증원**
- 강경 단속의 부작용(인도적 논란·강제추방 이슈) — **현재: 메인주에서 ICE 요원의 콜롬비아 국적자 총격 사망 사건 이후 일시적으로 차량검문 중단 조치, 트럼프가 며칠 만에 번복해 재개 — 소말리아·베네수엘라·아이티 등 TPS(임시보호신분) 종료 조치도 병행**
- 이민 이슈의 실제 표심 영향(여론조사) — **현재: 강한 반대 49%로 급등(전년 대비 +10%p+), 강한 지지 27%로 하락 — 핵심 치적 이슈에서도 침식**

### 5. 🥊 경쟁구도
- 공화당 경선 개입 성과(지지후보 승/패) — **현재: 이번 체크까지 구체 사례 미확인**
- 민주당 전략·후보 경쟁력 — **현재: 이번 체크까지 구체 사례 미확인**
- 경합주(swing state)별 판세 — **현재: NYT/Siena 여론조사 기준 공화당 현역 상원의석 중 위스콘신(D+8, 론 존슨 최다 열세)·노스캐롤라이나(D+6)·펜실베이니아(D+4)·오하이오(D+4)가 민주당 우위 — 민주당은 상원 과반(51석)까지 순증 4석 필요(50-50 동률시 부통령 밴스가 캐스팅보트). 하원은 435석 중 66석이 경합, 쿡폴리티컬리포트 기준 완전 토스업 17석(애리조나·캘리포니아·펜실베이니아·워싱턴 포함)**
- 무당파·중도층 동향 — **현재: 여성 유권자 민주 56% vs 공화 39%(27%p 격차)로 특히 크게 벌어짐(정치 카테고리 항목과 연동)**

## 오늘의 스코어보드 (2026-07-30, 프레임 최초 도입)

| 카테고리 | 상태 | 추세 | 근거(큰 이슈는 구체적으로) |
| --- | --- | --- | --- |
| 🏛️ 정치 | 🔴 불리 | ↘ 악화중 | Quinnipiac 여론조사 지지율 **32%로 집권 2기 최저치** 경신(7/27). Emerson 39%·순지지율 -19, 다른 집계는 순지지율 -17~-22. **제네릭 밸럿 민주당 우위 D+7~D+11**(Emerson: 민주 53%·공화 42%). 여성 유권자는 민주 56% vs 공화 39%(27%p 격차)로 특히 크게 벌어짐 |
| 💰 경제 | 🔴 불리 (부분 미확인) | ⏳ 판정 보류 | **정부 셧다운으로 10월 노동시장·물가 통계가 영구 결측될 수 있다고 백악관이 공식 경고**(캐롤라인 레빗 대변인, "permanent damage") — 실업률·CPI 실측 수치 자체는 이번 검색에서 확인 못해 미확인, 다음 체크에서 보완. 관세를 트럼프 본인은 "중간선거 압승 요인"으로 자평하나 공화당 일각에서도 대통령의 관세 권한을 제한하려는 법안이 나오는 등 당내 이견 존재 |
| ⚔️ 전쟁/외교 | 🔴 불리 | ↘ 악화중 | 미국-이란 **휴전이 종료되고 충돌이 재격화**(7월 기준). 7/20 후티 반군이 사우디아라비아 관련 선박의 **홍해 항행금지 선언**. 이스라엘-이란 국지 충돌 확대 중 — WaPo-Ipsos 여론조사는 지지율 부진 요인으로 "이란·경제에 대한 비관론"을 명시적으로 지목 |
| 🛂 이민 | 🔴 불리 | ↘ 악화중 | **핵심 치적 이슈에서도 침식 발생** — 연방 이민단속요원이 미국인 2명을 사살한 사건(2026년 초) 이후 이민정책에 대한 강한 반대가 **49%로 급등**(전년 여름 대비 +10%p 이상), 강한 지지는 **27%로 하락**. "너무 나갔다"는 여론이 확산 중(AP-NORC) |
| 🥊 경쟁구도 | ⏳ 초기 미평가 | ⏳ | 경선 개입 구체 사례·경합주별 판세는 이번 체크에서 확인 못함 — 다음 체크에서 보완 |

**오늘의 주요 이슈 3줄 요약**: ①지지율이 32%까지 떨어지며 집권 2기 최저치를
경신했고 ②그의 핵심 승부수였던 이민 정책조차 실탄 사용 사건 이후 지지가
무너지는 중이며 ③중동은 휴전이 깨지고 재격화되는 중 — 5개 카테고리 중
확인된 4개가 전부 불리한 방향, 유일하게 유리한 신호는 이번 체크에서 발견
되지 않았다. 다만 이건 오늘 하루의 스냅샷이고, 11월까지 넉 달 가까이
남아 있어 추세 반전 여지는 충분하다.

### 🔎 심층 갱신 (2026-07-30 밤, 사용자 요청 — 경쟁구도 최초 실측 + 항목별 구체 서술 보강)

| 카테고리 | 상태 | 추세 | 근거(구체) |
| --- | --- | --- | --- |
| 🏛️ 정치 | 🔴 불리 | ↘ 악화중 | **CNN 여론조사(7/29) 지지율 34%**로 Quinnipiac 32%(7/27)보다는 소폭 높으나 여전히 최저권. Emerson(7/19-20)은 39%로 조사기관별 편차 5~7%p — **범위 32~39%로 병기**. 유권자의 42%가 "트럼프에 반대하는 투표"를 하겠다고 응답(22%는 지지 투표) |
| 💰 경제 | 🔴 불리(부분 구체화) | ↘ 악화 | **관세 축 신규 확인**: 대법원이 2026-02 IEEPA 관세를 6-3으로 위헌 판결, 정부는 $1,000~1,300억 환급 압박에 직면. 트럼프는 7/28 "새 관세도 실질적으로 같은 효과"라며 대체 관세 재추진 발언 — 무역 전문가들은 **"중간선거 이후로 시행 시점을 늦출 가능성"**을 지목(선거 전 물가 자극 회피 의도로 해석). 통계 공백 이슈는 어제와 동일 유지 |
| ⚔️ 전쟁/외교 | 🔴 불리(혼재로 세분화) | → 혼재 | **중동은 악화 유지**(휴전 종료·재격화, 후티 홍해 봉쇄), 그러나 **우크라이나 축은 개선 조짐** — 미-우크라이나가 신규 평화안 조율 중, 젤렌스키·위트코프·커슈너 협의, 크렘린 페스코프가 "협상 개방적"(7/23) 발언, 트럼프-젤렌스키 회동 가능성(7/28). 두 전선이 반대 방향으로 움직여 카테고리 전체는 "혼재"로 세분화 |
| 🛂 이민 | 🔴 불리 | ↘ 악화중 | **구체 수치 신규 확보**: 강제추방 60만+ · 자진출국(Project Homecoming 등) 190만+ = 누적 250만+ 출국, ICE 인력 1만→2.2만 증원. 다만 메인주 ICE 총격 사망 사건으로 한때 차량검문 중단(트럼프가 며칠 만에 번복·재개) — 집행 강도는 세지는데 부작용 논란도 같이 확대되는 패턴 |
| 🥊 경쟁구도 | 🔴 불리(최초 실측) | ⏳ 신규 | **NYT/Siena 여론조사**: 공화당 현역 상원 의석 중 위스콘신(D+8)·노스캐롤라이나(D+6)·펜실베이니아(D+4)·오하이오(D+4)에서 민주당 우위 — 민주당은 상원 과반(51석)까지 순증 4석 필요(50-50 동률시 부통령 밴스 캐스팅보트로 공화당 방어). 하원은 435석 중 66석 경합, 쿡폴리티컬리포트 기준 완전 토스업 17석(애리조나·캘리포니아·펜실베이니아·워싱턴) — **처음으로 정량 판세 확보, 공화당에 불리한 방향으로 시작** |

## 체크 이력

| 날짜 | 정치 | 경제 | 전쟁/외교 | 이민 | 경쟁구도 | 오늘의 주요 이슈 |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-30(프레임 신설) | 🔴↘ | 🔴⏳ | 🔴↘ | 🔴↘ | ⏳ | 지지율 32%(최저치 경신), 이민 정책 지지 붕괴(사살 사건 여파), 이란 휴전 종료·재격화, 셧다운發 통계 영구결측 우려 — 5개 중 4개 확인, 전부 불리 |
| 2026-07-30 19:xx(저녁, 본격 갱신) | 🔴↘(변화없음) | 🔴⏳(변화없음) | 🔴↘(변화없음) | 🔴↘(변화없음) | ⏳(변화없음) | **오늘 저녁 체크에서는 신규 정치 뉴스가 검색되지 않음 — 오전 확인분과 변화 없음**으로 판정. SK하이닉스 이슈(CXMT·삼성 실적)에 리서치가 집중된 하루라 트래커 자체의 진전은 제한적이었음을 투명하게 기록 — 다음 체크(7/31)에서 재조사 |
| **2026-07-30 밤(심층 갱신, 사용자 요청)** | 🔴↘(범위 32~39%로 정교화) | 🔴↘(관세 축 구체화) | 🔴→(중동↘·우크라이나↗ 혼재로 세분화) | 🔴↘(구체 수치 확보) | **🔴⏳(최초 실측)** | 경쟁구도가 처음으로 정량 판세 확보(민주당 상원 4석 우위 지역 확인, 하원 토스업 17석) — 대법원 관세 위헌 판결 후 트럼프의 대체관세 재추진, 우크라이나 평화협상은 오히려 진전 조짐이라 5개 카테고리 전체가 단순 악화 일변도는 아님을 이번 심층조사로 확인 |
| 2026-07-31 07:xx(아침, 간략 재사용) | 🔴↘(변화없음) | 🔴↘(변화없음) | 🔴→(변화없음) | 🔴↘(변화없음) | 🔴⏳(변화없음) | 어젯밤 확정치 그대로 재사용 — 간밤 큰 뉴스 확인 안 됨. 지지율 재검색 결과 CNN 34%·AP-NORC 33%·Quinnipiac 32%·Verasight 39%·Reuters/Ipsos 37% 등 **기존 범위(32~39%)와 정합**, 순지지율 -17.4~-22로 재확인(큰 변화 아니라 5개 카테고리 판정에는 영향 없음) |

## Sources

- [July 2026 National Poll: Democrats with 11-Point Generic Ballot Advantage - Emerson Polling](https://emersoncollegepolling.com/july-2026-national-poll-democrats-with-11-point-generic-ballot-advantage/)
- [Trump Approval Rating Tumbles To 32% In Quinnipiac Poll—Hitting New Low - Forbes](https://www.forbes.com/sites/saradorn/2026/07/27/trump-approval-rating-below-40-in-latest-string-of-polls/)
- [Trump Approval Rating Falls Even More: Reaches 34% In Latest CNN Poll - Forbes](https://www.forbes.com/sites/saradorn/2026/07/29/trump-approval-rating-falls-even-more-reaches-34-inlatest-cnn-poll/)
- [July 8-13, 2026, Washington Post-Ipsos poll - The Washington Post](https://www.washingtonpost.com/tablet/2026/07/15/july-8-13-2026-washington-post-ipsos-poll/)
- [Trump's Numbers, July 2026 Update - FactCheck.org](https://www.factcheck.org/2026/07/trumps-numbers-july-2026-update/)
- [Donald Trump's Popularity Falls As Shutdown Drags On - AOL](https://www.aol.com/finance/donald-trumps-popularity-falls-shutdown-193435392.html)
- [미 정부 최장 셧다운, 세계 최대 경제의 '통계 공백' 초래](https://www.nvp.co.kr/news/articleView.html?idxno=316468)
- [Poll: Trump's ratings on immigration tumble - NBC News](https://www.nbcnews.com/politics/trump-administration/poll-trumps-ratings-immigration-tumble-americans-lose-confidence-top-i-rcna258159)
- [Many Americans say Trump has gone too far on immigration - AP-NORC/PBS](https://www.pbs.org/newshour/politics/many-americans-say-trump-has-gone-too-far-on-immigration-but-remains-his-strongest-issue-ap-norc-poll-finds)
- [2026년 중동 위기 - 나무위키](https://namu.wiki/w/2026%EB%85%84%20%EC%A4%91%EB%8F%99%20%EC%9C%84%EA%B8%B0)
- [트럼프 "관세 덕분에 2026년 중간선거에서 공화당 '압승' 할 것" - Benzinga Korea](https://kr.benzinga.com/news/usa/othermarkets/%ED%8A%B8%EB%9F%BC%ED%94%84-2026%EB%85%84-%EC%A4%91%EA%B0%84-%EC%84%A0%EA%B1%B0%EC%97%90%EC%84%9C-%EA%B1%B0%EB%8C%80%ED%95%98%EA%B3%A0-%EC%B2%9C%EB%91%A5%EC%B9%98%EB%8A%94-%EC%8A%B9%EB%A6%AC/)
- [Supreme Court strikes down tariffs - SCOTUSblog](https://www.scotusblog.com/2026/02/supreme-court-strikes-down-tariffs/)
- [Trump: New tariffs "doing the same thing" as ones struck down by Supreme Court - CNBC](https://www.cnbc.com/2026/07/28/trump-usmca-canada-mexico-trade-deal.html)
- [Ukraine, US align on new peace push as officials hope Russia accepts air truce - Kyiv Independent](https://kyivindependent.com/ukraine-us-align-on-new-peace-push-as-officials-say-russia-may-accept-air-ceasefire/)
- [Trump deportation push falters after fatal ICE encounters - The Washington Post](https://www.washingtonpost.com/politics/2026/07/15/trump-deportation-push-falters-after-fatal-ice-encounters/)
- [ICE nears 600,000 deportations since Trump took office - Washington Times](https://www.washingtontimes.com/news/2026/jul/23/ice-nears-600000-deportations-since-trump-took-office/)
- [How Trump's "self-deportation" machine has ramped up - Axios](https://www.axios.com/2026/07/28/trump-self-deportation-ice)
- [With just a few primary elections to go, the competitive Senate map keeps shifting - NPR](https://www.npr.org/2026/07/27/nx-s1-5907379/2026-midterm-election-senate-races)
- [GOP holds edge in Senate swing-state races: New York Times polls - The Hill](https://thehill.com/homenews/campaign/5949463-texas-maine-iowa-ohio-alaska-senate-races/)
- [macro-regime-history.md](macro-regime-history.md) (유가·거시국면 교차연동)
