---
title: 트럼프 2026 중간선거 트래커
created: 2026-07-30
updated: 2026-08-01
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
- 대중국 관계(무역전쟁·대만 등) — SK하이닉스 체크포인트⑦과 접점 — **현재: 정치적 차원의 확인된 신규 이슈는 없음. [OPINION, 김광석 교수 전망(2026-07-30 INGEST)]** 9월 미중 정상회담을 앞두고 양국이 "약속대련" 식의 평화 국면("디센트 피스")을 11월 중간선거까지 유지할 것이라는 전망 제기 — 중국산 생필품 수입 확대가 미국 물가 안정에 기여할 가능성도 함께 언급. 아직 검증된 사실이 아니라 한 전문가의 예측이므로 [FACT]로 승격하지 않고 다음 체크에서 실제 정상회담 일정·관세 동향으로 교차확인할 것 (상세: [sources/kim-kwangsuk-2026h2-outlook-2026-07-30.md](../../sources/kim-kwangsuk-2026h2-outlook-2026-07-30.md)). **[2026-08-02 재확인]** 같은 교수의 8월 특강("디스앤피스Dis & Peace"로 재표기, 같은 개념)이 이 전망을 반복 — 새 근거는 아니고 같은 예측의 재확인, 검증 상태(미확인)도 그대로 유지 ([sources/kim-kwangsuk-august-2026-market-outlook-lecture.md](../../sources/kim-kwangsuk-august-2026-market-outlook-lecture.md))
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

## 카테고리별 타임라인 (2026-07-31 신설 — x축=날짜, 각 항목이 선거일까지 어떻게 변해가는지 추적)

**로그 로테이션(2026-08-04 도입)**: 이 6개 표(5개 카테고리 타임라인 +
아래 "체크 이력") 모두 이전 달 행이
[trump-midterm-tracker-history/2026-07.md](trump-midterm-tracker-history/2026-07.md)로
이관된다 — [CLAUDE.md 로그 로테이션 규칙](../../CLAUDE.md) 참고. 매월
첫 세션이 지난달 몫을 옮긴다.

**목적**: 위 "체크 이력"(날짜별 5개 카테고리 스냅샷)은 하루 단위로 무슨 일이
있었는지 훑기엔 좋지만, **하나의 카테고리가 시간에 따라 어느 방향으로
가고 있는지**는 여러 행을 오가며 읽어야 한다. 이 섹션은 같은 데이터를
**카테고리 기준으로 재배열**해 각 항목의 추이를 세로로 한눈에 볼 수 있게
한다 — 11월 중간선거일까지 매일 한 줄씩 쌓인다. (매일 체크마다 이 5개
표 + 위 "체크 이력" 표를 **함께** 갱신할 것 — 둘 다 같은 원자료의 다른
뷰이므로 항상 동시에 갱신.)

### 🏛️ 정치 — 타임라인
| 날짜 | 상태 | 비고 |
| --- | --- | --- |
| 2026-08-01/02(주말) | 🔴↘(변화없음) | 재검색해도 새 여론조사 없음(주말) — AP-NORC 33%·순지지율 -20.6 등 기존 범위 안 |
| 2026-08-02 저녁 | 🔴↘(변화없음) | FiftyPlusOne 집계 39.0%·순지지율-19, 다른 집계 37%(불승인58%). 제네릭밸럿 민주 49%·공화41%(D+8, gelliottmorris) — 기존 범위(32~39%, D+7~11) 내, 큰 변화 아님 |

### 💰 경제 — 타임라인
| 날짜 | 상태 | 비고 |
| --- | --- | --- |
| 2026-08-01 | 🔴↘ | **신규 관세 14개국 발효**(한국·일본 포함) — 말레이시아25%·인도네시아32%·캄보디아36%·라오스40% 등, 한국向 관세가 이 트래커에 처음 구체적으로 잡힘(대미 반도체 수출 영향은 다음 체크에서 확인) |
| 2026-08-02 저녁 | 🔴↘(변화없음) | 재검색해도 신규 경제지표·관세 소식 없음(주말) — 관세 발효 국면·통계결측 우려 그대로 유지 |

### ⚔️ 전쟁/외교 — 타임라인
| 날짜 | 상태 | 비고 |
| --- | --- | --- |
| 2026-08-01/02 | 🔴🔴↘↘ | **급격 악화** — 트럼프 "이란 매우 세게 타격" 예고(7/31), 국무부 중동 전역 여행경보("지금 떠나라"), 쿠웨이트 이란발 드론공격 보고(8/1 새벽). 이스라엘 최고경계이나 참전여부는 혼재보도. 단 가자 평화안(하마스 무장해제·이스라엘 철수)은 별도로 진전 — 중동 내에서도 이란축↘·가자축↗로 갈림 |
| 2026-08-02 저녁 | 🔴🔴↘↘(규모 재인식) | **[중요 정정] "8/1 새벽 단발성 공격"이 아니라 2026-02말부터 이어진 지속 무력충돌**임을 확인 — Al Jazeera가 이를 "US-Israel war on Iran"으로 명명, 위키피디아에 "2026 Iranian strikes on Kuwait"·"2026 Kuwait International Airport drone strikes"·"2026 Port Shuaiba drone attack" 등 별도 문서가 존재할 정도로 장기화된 분쟁. 3/1 포트슈아이바 공격은 미군 6명 사망·30명+ 부상 확인 — 이 트래커가 지금까지 "7월말 급격 재격화"로 프레이밍한 것은 최근 뉴스 재유통만 본 결과였고, 실제로는 **2월 말부터 이미 미국-이스라엘-이란 무력충돌이 진행 중이었다**는 것이 더 정확한 배경. 등급·추세는 유지하되 서술을 보정 |
| 2026-08-05 저녁 | 🔴🟡↗(개선 조짐, 이 축 최초) | **호르무즈 해협 개방 협상 "매우 진전된 단계"** — 미-이란-오만 3자, 카타르 중재로 합의 초안 회람 중(진입선박=이란 항로, 출항선박=오만 항로, 통행료 부과안). 베선트 재무장관 "오늘·내일 타결 가능" 낙관 vs 루비오 국무장관 "최종 타결 아님, 위험한 선례" 신중론 — 정부 내 온도차 존재. 최종 타결 전까진 "혼재"로만 격상. 시장 반응은 즉각적: 유가 -5%대, SOX+6.55%, 코스피·SK하이닉스 동반 급등(간접 경로로 SK하이닉스 주가에 실제 영향을 준 첫 사례) |

### 🛂 이민 — 타임라인
| 날짜 | 상태 | 비고 |
| --- | --- | --- |
| 2026-08-01/02 | 🔴↘(변화없음) | 재검색해도 신규 수치·사건 미확인 — 기존 구체 수치(강제추방 60만+ 등) 유지 |
| 2026-08-02 저녁 | 🔴↘(변화없음) | 신규 사건·수치 미확인, 기존 범위 유지 |

### 🥊 경쟁구도 — 타임라인
| 날짜 | 상태 | 비고 |
| --- | --- | --- |
| 2026-08-01/02 | 🔴⏳ | **[미검증, 예정 일정]** 미시간·버지니아 8/4 예비선거 예정 — 매사추세츠 마키(현역) vs 몰튼(도전) 경선, 미네소타 클로버샤 등 경합 확인. 아직 결과는 아니고 일정 확인 수준 |
| 2026-08-02 저녁 | 🔴⏳(변화없음) | 8/4 예비선거 D-2, 신규 정보 없음 — 화요일 결과가 다음 실측 시점 |

## 체크 이력

| 날짜 | 정치 | 경제 | 전쟁/외교 | 이민 | 경쟁구도 | 오늘의 주요 이슈 |
| --- | --- | --- | --- | --- | --- | --- |
| **2026-08-01/02 주말 체크(일요일, 사용자 요청 — 월요일 개장 대비)** | 🔴↘(변화없음) | 🔴↘(관세 신규 확인) | 🔴🔴↘↘(급격 악화 — 최대 이슈) | 🔴↘(변화없음) | 🔴⏳(구체 사례 신규 확인) | **[FACT] 이란 신규 공습이 이번 주말 임박** — 트럼프가 7/31 "매우 세게 타격하겠다(hitting them very hard)"고 예고, 국무부가 중동 전역 미국인에 "지금 떠나라" 여행경보 발령, 쿠웨이트에서 8/1 새벽 이란발 드론 공격 보고(CNN). 이스라엘은 "최고 경계"이나 자체 참전 결정은 미확인이라며 부인 보도도 혼재. 다만 같은 기간 **가자 평화안(하마스 무장해제·이스라엘 철수) 진전은 별도로 보도**돼 중동 내에서도 이란 축과 가자 축이 반대로 움직임. **[FACT] 신규 관세 발효(8/1)**: 한국·일본 포함 14개국에 새 관세율 발효(말레이시아 25%·인도네시아 32%·캄보디아 36%·라오스 40% 등) — 한국 관련 관세가 이 트래커에 처음 구체적으로 잡힘, SK하이닉스 대미 수출과의 접점은 다음 체크에서 확인 필요. **[미검증] 경쟁구도**: 미시간·버지니아 8/4 예비선거 예정(매사추세츠 마키 vs 몰튼, 미네소타 클로버샤 등 경합 확인) — 아직 결과 아닌 예정 일정. 지지율(정치)·이민 항목은 기존 범위·수치에서 변화 없음 |
| **2026-08-02 19:xx 저녁(하루 최종 확정치)** | 🔴↘(변화없음, FiftyPlusOne39%/D+8) | 🔴↘(변화없음) | 🔴🔴↘↘(**중요 정정**) | 🔴↘(변화없음) | 🔴⏳(변화없음) | 5개 카테고리 등급·추세 자체는 전부 유지, 신규 여론조사도 기존 범위 안(승인율 37~39%, 제네릭밸럿 D+7~8). **가장 중요한 발견은 전쟁/외교 서술 정정**: 이란-쿠웨이트 충돌이 8/1 새벽의 고립된 사건이 아니라 **2026-02말부터 이어진 지속 무력충돌**(Al Jazeera "US-Israel war on Iran" 명명, 위키피디아 개별 문서 3건 존재 — 3/1 포트슈아이바 공격 미군 6명 사망 확인)임을 확인, 트래커 서술을 그에 맞춰 보정. 5개 카테고리 세부 항목 타임라인도 전부 동시 갱신 완료 |
| **2026-08-05 19:xx 저녁(수, 하루 최종 확정치 — 8/3·8/4는 세션 공백으로 스킵, 전쟁/외교 축 개선 조짐 신규 포착)** | 🔴↘(변화없음, 신규 여론조사 미확인) | 🔴⏳(변화없음, 신규 확인 없음) | 🔴🟡**혼재→개선 조짐**(중동 이란 축 최초 개선 신호) | 🔴↘(변화없음) | 🔴⏳(변화없음) | **⚔️ 전쟁/외교 신규 발견**: 미국-이란-오만 3자가 **호르무즈 해협 개방 협상에서 "매우 진전된 단계"** 진입 — 카타르가 중재해 잠재적 합의 초안이 관계국 간 회람 중, 페르시아만 진입선박은 이란 통제항로·출항선박은 오만 통제항로를 이용하고 통행료를 부과하는 방안 논의 중([뉴데일리](https://www.newdaily.co.kr/site/data/html/2026/08/05/2026080500155.html), [한국일보](https://www.hankookilbo.com/news/article/A2026080508190001050), [Axios](https://www.axios.com/2026/08/05/us-iran-strait-of-hormuz-deal-nears)). 베선트 재무장관은 "오늘·내일 중 합의 가능"이라 낙관한 반면, 루비오 국무장관은 "진전은 있으나 최종 타결 아님, 이란에 해협 통제권을 주는 건 위험한 선례"라며 신중론 — **이 트래커 추적 이래 이란 축에서 처음 나온 명확한 개선 신호**(그동안은 2월 말부터 계속 악화 일변도였음), 다만 최종 타결 전까지는 "혼재"로만 격상하고 "개선"으로 완전히 넘기지 않음. **시장 연쇄효과**: 이 협상 진전 기대로 국제유가 5%대 급락 → 리스크온 전환 → 간밤 SOX+6.55% 급등 → 오늘 코스피·SK하이닉스 동반 급등([market-cycles-leverage-risk.md](market-cycles-leverage-risk.md), [hbm-cycle-score.md](hbm-cycle-score.md) 참고) — 정치 트래커의 움직임이 SK하이닉스 가격에 직접 파급된 드문 사례. 나머지 4개 카테고리는 8/3~8/4 세션 공백 기간 신규 확인 못해 8/2 확정치 그대로 이월 |

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
- [Democrats lead the U.S. House generic ballot by 8 - G. Elliott Morris](https://www.gelliottmorris.com/p/democrats-lead-the-us-house-generic)
- [Iran war live: Kuwait downs Iranian drones targeting vital facilities - Al Jazeera](https://www.aljazeera.com/news/liveblog/2026/7/31/iran-war-live-iran-says-it-has-a-plan-to-respond-to-any-us-attacks)
- [2026 Iranian strikes on Kuwait - Wikipedia](https://en.wikipedia.org/wiki/2026_Iranian_strikes_on_Kuwait)
- [2026 Port Shuaiba drone attack - Wikipedia](https://en.wikipedia.org/wiki/2026_Port_Shuaiba_drone_attack)
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
- [Live updates: US-Iran war news; State Department warns citizens across the Middle East - CNN](https://www.cnn.com/2026/08/01/world/live-news/iran-war-trump)
- [Trump touts progress on Gaza peace effort as war with Iran drags on - CNN (7/31)](https://www.cnn.com/2026/07/31/world/live-news/iran-war-trump)
- [Israel assesses Iran will fire missiles even without joining new US offensive - Times of Israel](https://www.timesofisrael.com/liveblog-august-01-2026/)
- [Fact Sheet: Trump Imposes Additional Tariffs on Canada - White House (7월)](https://www.whitehouse.gov/fact-sheets/2026/07/fact-sheet-president-donald-j-trump-imposes-additional-tariffs-on-canada/)
- [Trump 2.0 tariff tracker - Trade Compliance Resource Hub](https://www.tradecomplianceresourcehub.com/2026/07/27/trump-2-0-tariff-tracker/)
- [Michigan's August 2026 primary election guide - wzzm13](https://www.wzzm13.com/article/news/politics/elections/michigan-august-2026-primary-election-guide/69-d2214353-b92b-4f78-b1aa-d6a4007fc11f)
- [Virginia voter guide: Parties nominate candidates for Congress - WTOP](https://wtop.com/virginia-election/2026/07/virginia-voter-guide-parties-nominate-candidates-for-congress-local-offices-ahead-of-2026-midterms/)
