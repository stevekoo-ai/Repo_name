---
title: 트럼프 2026 중간선거 트래커
created: 2026-07-30
updated: 2026-09-25
tags: [politics, us-midterm, trump, concept, framework]
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
- **(2026-08-26 INGEST, 후속) 재정발 유동성 전략이 통제 이탈 중이라는 시각** — [OPINION, 김광석 교수 전망, 출처 메타데이터 미상·저신뢰([sources/kim-kwangsuk-midterm-economic-outlook-2026-08.md](../../sources/kim-kwangsuk-midterm-economic-outlook-2026-08.md))] 위 "재정정책 유동성 공급" 전략(7/30 전망)이 실제로 시행됐으나(재무부 국채 바이백 20억→40억 달러 확대 — 이 부분은 이 위키가 8/20 이미 별도로 [FACT] 검증한 사실과 일치, [macro-indicators.md](macro-indicators.md) 참고) **시장 통제에는 실패**하고 있다는 후속 해석 — 30년물 국채금리가 5%대를 계속 상회(이 저장소가 8/18~21 추적한 "5.3%대, 2007년 이후 최고" 실측과 방향 일치), 모기지 연체율 상승(신규 주장, 미검증), 국가부채 40조달러·이자비용>국방비(신규 주장, 미검증)를 근거로 **"이번 재정 전략은 결국 중간선거용 임시방편이고 실제 선거 판세는 공화당에 불리할 것"**이라는 결론 제시. 위 정치 카테고리의 "지지율 32~39%, D+6~11" 실측과 방향은 일치하나, 이 소스 자체의 인용 신뢰도가 낮아([1]~[16] 각주는 있으나 참고문헌 목록 없음) [FACT]로 승격하지 않음 — 다음 체크에서 모기지 연체율·이자비용 수치를 별도 검증할 것
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


📊 **Daily tracking data moved to**: [monitoring/trump-midterm-tracker-status.md](../../monitoring/trump-midterm-tracker-status.md)

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

### 💰 경제 — 타임라인
| 날짜 | 상태 | 비고 |
| --- | --- | --- |

### ⚔️ 전쟁/외교 — 타임라인
| 날짜 | 상태 | 비고 |
| --- | --- | --- |

### 🛂 이민 — 타임라인
| 날짜 | 상태 | 비고 |
| --- | --- | --- |

### 🥊 경쟁구도 — 타임라인
| 날짜 | 상태 | 비고 |
| --- | --- | --- |

## 🧭 대통령 레버 & 심층 체크포인트 (2026-09-25 신설, 사용자 요청)

> "트래커에 대통령 레버 체크리스트 추가할 필요가 있다. 그러나 아직 좀
> 피상적이다. 좀 더 deep dive해서 심연에 흐르는 변화를 알 수 있는 어떤
> check point들이 아직 부족해보인다."

**설계 원칙**: 헤드라인("레버를 당겼다")만 보면 속는다. 레버 하나마다 네 가지를
따로 본다.
- ①**남은 탄약**: 또 당길 수 있나
- ②**전달 경로**: 유권자 지갑에 닿았나
- ③**표심 반응**: 실제로 표로 이어지나
- ④**청구서**: 선거 뒤 무엇이 돌아오나

아래 층위(L0~L4)는 이 순서를 따른다.

> 역사 공식(1946~2022 사례)·숫자로 안 잡히는 정치 기술·시대적 합의는
> [중간선거 역사 플레이북](midterm-history-playbook.md)에서 다룬다.

### 핵심 판단 (2026-09-25 실측 기준) — "레버 소진" 가설

**현직 대통령의 경제 레버 대부분이 이미 소진됐거나 거꾸로 돌고 있다.** 선거 전에
판세를 뒤집을 만한 레버는 사실상 **하나**다. **이란 종전과 호르무즈 재개**다.
- **유가 레버는 소진됐다.** 3월에 SPR 1.72억 배럴(사상 최대)을 이미 방출했다.
  SPR은 2.87억 배럴로 1983년 이후 최저다. 그런데도 휘발유는 $4.48로 오르는 중이다.
- **금리 레버는 반대로 돈다.** 워시 연준은 9/16에 **인상**했다(3.75~4.00%, 12:0).
  추가 인상도 거론된다. 모기지는 약 7~7.2%다. 자기가 임명한 의장이 유가발
  인플레이션을 이유로 조이고 있다.
- **재정 레버는 봉쇄됐다.** 관세 환급 수표는 의회 승인이 없고 재원 계산도 맞지
  않는다(추산 $4,500억 vs 관세수입의 약 절반). 임시예산(CR)은 12/11까지로,
  셧다운은 피했지만 부양책은 아니다.
- **당긴 레버는 미중 휴전뿐이다.** 9/24 백악관 정상회담에서 휴전을 연장했다
  (관세 인하, 희토류 수출통제 유예 유지). 다만 구체 성과는 적었다.
- 결과: 지지율 29~33%(ARG 29%, 두 임기 통틀어 첫 30% 하회), 경제 순지지 -29.
  예측시장은 하원 민주당 약 90%, 상원 51~60%, 민주당 싹쓸이 약 65.5%다.
- **함의**: 네가 처음 세운 "선거 전 돈풀기 → 위험자산 랠리" 가설은 약해졌다.
  남은 상승 촉매는 **종전 이벤트 하나에 몰린 이항(binary) 구조**다. 종전 →
  유가 하락 → 인플레이션 둔화 → 연준 인상 중단의 연쇄가 가능한 유일한 경로다.

### L0 — 레버 상태판 (발동 / 소진 / 봉쇄 / 미발동)

| 레버 | 상태 | 실측 근거 (2026-09-25) | 남은 탄약 |
| --- | --- | --- | --- |
| SPR 방출 | 🟥 소진 임박 | 3월 1.72억 배럴 방출, SPR 286.6백만 배럴(8/28, 1983년 이후 최저) | 거의 없음. 추가 방출은 "안보 비축 고갈" 역풍 |
| 이란 종전·호르무즈 재개 | 🟨 협상 중 | 호르무즈 통행 평시 10%, 9월 브렌트 $100선 재진입. 8월 이란-오만 항로 합의가 있었으나 미완 | **최대 레버**. 성사되면 유일한 게임체인저 |
| 연준 압박·금리 | 🟥 역방향 | 9/16 인상(3.75~4.00%), 추가 인상 전망 | 인사권은 이미 사용(워시). 독립성 역풍 |
| 재무부 발행·바이백 | 🟩 발동(효과 약함) | 바이백 20→40억 달러([FACT] 8/20), 그러나 모기지 7%대 | 발행 구성 조정 여지는 남음 |
| 가계 현금(관세 환급) | 🟥 봉쇄 | 의회 미승인, 재원 부족 | 의회 없이는 불가 |
| 예산 집행 앞당김·농가 지원 | ⬜ 미확인 | CR은 현 수준 유지. 농가 지원은 미중 대두 약속과 연동 | 행정 재량으로 가능. 체크 대상 |
| 미중 휴전 | 🟩 발동 | 9/24 연장(관세 인하, 희토류 통제 유예). 부산 합의(대두 연 2,500만 톤, 농산물 연 170억 달러) 이행은 들쭉날쭉 | 추가 카드: 엔비디아 등 수출통제 완화 |
| 반도체 232조 관세 | 🟨 보류(위협 유지) | 1/15부터 첨단 로직 일부에 25%. 러트닉: 미국 투자 안 하는 한국·대만 기업 최대 100% | **선거 후 청구서 후보**. 하이닉스 직결 |
| 셧다운 회피 | 🟩 발동 | CR 하원 370:48 통과, 12/11까지 | 12/11이 선거 후 첫 절벽 |
| 규제 완화·AI 인허가 | ⬜ 미확인 | — | 병목 추적 B1(전력)과 연결 |

### L1 — 전달 경로: 레버가 유권자 지갑에 닿았나

| 체크포인트 | 왜 "심연"인가 | 현재값 | 판단을 바꿀 신호 | 소스(자동화) |
| --- | --- | --- | --- | --- |
| **휘발유 전국 평균** | 지지율과 가장 직결된 가격. 원유보다 2~4주 늦게 따라온다 | **$4.48**(AAA 9/24), 9/8 $4.15 → 상승 중 | $4.00 아래로 2주 이상 = 종전 효과 전달 | AAA / FRED `GASREGW`(주간, 수집 중 2026-09-25~) |
| 30년 모기지 금리 | 바이백·발행전략이 주택 체감에 닿았나 | 약 7.0~7.19% | 6.5% 아래 = 금리 레버 부활 | FRED `MORTGAGE30US`(수집 중 2026-09-25~) |
| 식료품·체감물가 | "72%가 경제 악화"의 원인 | 미확인 | 미시간대 1년 기대인플레 하락 반전 | FRED `MICH`(수집 중 2026-09-25~) |
| 재무부 현금 지출 속도(TGA) | 재정이 **실제로** 풀리는가 (말이 아니라 돈) | 미확인 | 선거 전 8주 지출 전년 대비 급증 = 집행 앞당김 발동 | Daily Treasury Statement / FRED `WTREGEN`(수집 중 2026-09-25~) |
| 원유(브렌트·WTI) | 종전 레버의 1차 반응 | 약 $99~100(9월) | $85 아래 안착 | 이미 수집(`us_brent`) |

### L2 — 표심의 선행지표: 여론조사보다 먼저 움직이는 것

| 체크포인트 | 왜 "심연"인가 | 현재값 | 판단을 바꿀 신호 |
| --- | --- | --- | --- |
| **보궐선거 스윙(2024 대선 기준)** | 실제 표. 2018년 보궐 D+9.9 → 최종 제네릭 D+8.4로 적중 | 중간값 **D+10.4**, 9월 D+12 수준 | D+5 아래로 수렴 = 물결 약화 |
| 예측시장(칼시·폴리마켓) | 실제 돈이 걸린 확률. 매일 움직임 | 하원 D 약 90%, 상원 D 51~60%(최근 역전) | 상원 R 55% 재역전 = 판세 전환 |
| 경제 지지율 vs 전체 지지율 격차 | 경제가 정권을 끌어내리는가 | 경제 순지지 -29, 전체 29~33% | 경제 순지지 -15 위로 = 레버 효과 |
| 무당파·여성 이탈 | 스윙 유권자층 | 여성 민주 56:39(7월) | 격차 축소 |
| 공화당 하원 은퇴·경선 이탈 | 의원 본인들이 패배를 예상하나 | 미확인 | 추가 은퇴 발표 |
| 사전투표·우편투표 신청 당파 구성(10월~) | 투표율 엔진 | 10월부터 | 공화 등록 유권자 비중 증가 |

### L3 — 청구서와 제약: 선거 뒤에 돌아올 것

| 체크포인트 | 왜 "심연"인가 | 현재값 | 판단을 바꿀 신호 |
| --- | --- | --- | --- |
| **30년물 국채금리·국채 입찰 결과** | 재정 신뢰. 시장이 청구서를 먼저 매긴다 | 5%대(8월), 10년물은 잭슨홀 이후 +25bp | 30년물 5.5% 돌파 = 채권 자경단 |
| 5년 뒤 5년 기대인플레 | 연준 신뢰가 무너지나 | 미확인 | 급등 = 정치 압박에 연준이 밀린다는 신호 |
| 하이일드 스프레드·달러 | 위험 회피 / "미국 매도" | 이미 수집 | 스프레드 확대 + 달러 약세 동시 = 미국 자산 이탈 |
| **12/11 CR 만료** | 선거 후 첫 재정 절벽. 레임덕 의회 | 12/11 | 셧다운 위협 재부상 |
| 대체 관세·232조 반도체 관세 | 선거 전에 미룬 것이 한꺼번에 온다 | 전문가: "선거 후 시행" 전망 | 11/4 이후 관세 발표 |
| 관세 환급(IEEPA 위헌분) | $1,000~1,300억 재정 구멍 | 진행 중 | 환급 지급 일정 |

### L4 — "약속대련"의 진위: 외교 헤드라인이 진짜인가

| 체크포인트 | 왜 "심연"인가 | 현재값 | 판단을 바꿀 신호 |
| --- | --- | --- | --- |
| **중국의 미국산 대두 실제 선적** | 말이 아니라 배. 약속 연 2,500만 톤 | 이행 들쭉날쭉(CNBC 9/23) | USDA 주간 수출 판매가 약속 속도를 따라가나 |
| 희토류 수출 허가 흐름 | 중국의 최강 카드를 실제로 풀었나 | 통제 유예 연장(9/24) | 허가 지연 보도 = 휴전 형해화 |
| 보잉 주문 | 3대 약속 중 하나 | 진행 속도 상이 | — |
| 위안화 고시 | 인민은행이 협조 중인가 | `usd_cny` 이미 수집 | 급격한 위안 약세 = 협조 종료 |
| 대만해협 군사활동 | 휴전의 이면 | 미확인 | 대규모 훈련 = 휴전 이후 긴장 재개 |
| **호르무즈 유조선 통행량** | 종전 레버의 실물 | 평시 10% | 50% 이상 회복 = 유가 레버 부활 |

### 선거 전후 달력 (체크 시점)

| 날짜 | 이벤트 | 볼 것 |
| --- | --- | --- |
| 10월 | 사전투표 시작, 3분기 선거자금 보고(FEC) | 투표율 엔진, 자금 흐름 |
| 10월 말 FOMC | 추가 인상 여부 | 유가발 인플레이션 vs 정치 압박 |
| 11/3 | 중간선거 | 예측시장 대비 결과 |
| 11/4~ | **선거 후 청구서 창** | 관세 발표, 232조, 재정 |
| 12/11 | CR 만료 | 셧다운 위협 |

### 내 포지션과의 연결

- **SK하이닉스**: 금리 인상, 유가, 232조 관세 위협(선거 후)이 겹쳐 있다. 하이닉스는
  6/22 고점 대비 -36%다. 종전은 유일한 상방 촉매다(8/5 호르무즈 협상 진전 당시
  SOX +6.55% 선례).
- **자금 조달 계획**: EW2("선거 전 변동성 확대" 전제)는 VIX 14대라 이탈 중이다.
  종전이라는 이항 이벤트가 **선거 전에 변동성을 만들 수 있다.** T2(11/04~) 시점은
  **11/3 전에 결정한다.**
- **원/달러 EW1(1,400원)**: 유가 강세와 연준 인상은 달러 강세 요인이다. 미중
  휴전 연장은 원화 강세 요인이다. 둘이 상충한다.
- **자동 수집 후보**: 휘발유(`GASREGW`), 모기지(`MORTGAGE30US`), 기대인플레
  (`MICH`, `T5YIFR`), TGA(`WTREGEN`), 30년물(`DGS30`). 모두 FRED다. **2026-09-25 구현 완료** — `engine/briefing/midterm_levers.py`가
  L1·L3을 매일 판정해 브리핑 ⑩ 블록에 싣는다. 첫 판정: 휘발유 $4.48, 모기지 7.03%,
  30년물 5.40%(청구서 경보선 5.5%에 근접), 5y5y 2.33%(안정), 모두 미점등.

## 📊 Monitoring

일일 추적 현황: [monitoring/trump-midterm-tracker-status.md](../monitoring/trump-midterm-tracker-status.md)

## Sources
- 2026-09-25 심층 체크포인트 실측(WebSearch): [NBC — CR 12/11까지](https://www.nbcnews.com/politics/congress/senate-leaders-reach-deal-avert-shutdown-2026-elections-rcna590564), [NPR](https://www.npr.org/2026/09/01/nx-s1-5951536/house-government-funding-vote-midterms), [Covers 예측시장](https://www.covers.com/betting/prediction-sites/guides/midterm-election-odds-tracker), [Yahoo — 상원 역전](https://www.yahoo.com/news/articles/traders-flip-senate-control-bet-031157694.html), [AAA 휘발유](https://gasprices.aaa.com/news/), [Newsweek — 지지율 29%](https://www.newsweek.com/donald-trump-approval-rating-hits-all-time-low-12467727), [Forbes 9/23](https://forbes.com/sites/saradorn/2026/09/23/trumps-approval-rating-americans-views-of-the-economy-is-41-points-below-this-point-in-first-term), [CNBC — 대두·희토류 이행](https://www.cnbc.com/2026/09/23/trump-xi-summit-us-china-trade-rare-earth-soybean-plane.html), [Washington Times — 9/24 정상회담](https://www.washingtontimes.com/news/2026/sep/24/xi-jinping-trump-conclude-bilateral-meeting/), [CNBC 9/24](https://www.cnbc.com/2026/09/24/trump-xi-meeting-china-washington.html), [232조 반도체](https://www.chrobinson.com/en-us/resources/insights-and-advisories/client-advisories/2026q1/01-15-client-advisory-guidance-on-section-232-semiconductor-import-duties-for-2026/), [MultiState 보궐 스윙](https://www.multistate.us/elections/special-swing), [SPR — NBC](https://www.nbcnews.com/business/energy/gas-prices-trump-midterms-iran-rcna598523), [SPR — Wikipedia](https://en.wikipedia.org/wiki/Strategic_Petroleum_Reserve_(United_States)), [CNBC — 9/16 FOMC 인상](https://www.cnbc.com/2026/09/16/fed-rate-decision-september-2026.html), [관세 환급 현황](https://www.yahoo.com/news/articles/odds-were-getting-trump-tariff-093132571.html)

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
