---
textbook_id: 08
meeting: Liqid (On-site Install, CXL Chassis, HPE Discover)
date: 2026-06-10
type: C (sample/schedule coordination)
partner: Liqid (Trent, Vincent, Daniel, Richmond, Dave, Thomas)
sk_side: Jungmin, Hyunjun, Seonjun, Steve, BY Hongjin
duration_words: 3544
audio: repo/webex-audio/2026-06-10 09 03 06_EN_Liqid-extracted.wav
transcript: repo/webex-audio/2026-06-10 09 03 06_EN_Liqid-extracted-rag-corrected.txt
created: 2026-09-02
tags: [textbook, english, liqid, cxl, on-site-install, hpe-discover, schedule-coordination, sample, firmware, type-c]
---

# Textbook 08 - Liqid On-site Install & HPE Discover Coordination (2026-06-10)

> **회의 유형**: C (sample/schedule coordination) - 현장 설치 일정 조율, 서버 출하 추적, 펌웨어 상태 공유, HPE Discover 샘플 조율
> **학습 가치**: 일정 협상, 샘플 수량 조율, 이슈 진단 보고, 액션 아이템 정리
> **Audrey 관점**: 이 회의는 "실행 조율" register다 - 제품 설명이 아니라 "누가 언제 어디서 무엇을 할지"를 맞추는 화법. Type C의 핵심은 timeline + sample + accountability 언어

---

## 1. 발화 아키텍처 - Trent의 조율 설계 (5단계)

Trent(Liqid 리드)가 회의를 5단계로 조율한다. 각 단계마다 **고정된 화법 공식**이 있다. 이게 Type C 회의에서 네가 따라 배워야 할 "조율의 뼈대"다.

### 단계 1: 일정 개시 (Schedule Opening)

Trent는 회의 시작과 함께 "we will expect to start on Monday"로 일정을 명시한다. 제품이나 이슈가 아니라 **일정**으로 시작하는 것이 Type C의 첫 신호.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we will expect to start on X and we will coordinate with Y to figure out Z` | "we will expect to start on Monday and we will coordinate with Zest Pro to figure out which days we're going to be in which days we will be at SSSK hynix's" | 일정 명시 + 조율 대상 지정 |
| `I believe X but I need to confirm with Y` | "I believe Monday or Tuesday but I need to confirm with Zest Pro" | 견해 표시 + 확인 보류 - 일정에 대한 단정 금지 |

**Audrey 교훈**: Type C 회의는 "일정"으로 시작한다. "we will expect to start on X" - "expect to"가 핵심. 고정이 아니라 예상이라는 뉘앙스. 그리고 "I believe X but I need to confirm with Y" - 자신이 확신하지 않을 때 "I believe"로 표시하고 "need to confirm with Z"로 책임을 분산. 한국어 "아마 월요일이나 화요일인데 확인해 봐야겠습니다"의 영어 버전.

### 단계 2: 요청 (Ask)

일정 명시 후, 즉시 상대에게 필요한 것을 요청한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `One thing I will ask is if you can share X so that we can Y` | "One thing I will ask is if you can share the address office location so that we can look at booking the travel" | 정중한 요청 - "I will ask" + "so that we can" |
| `That would be very helpful.` | "That would be very helpful." | 요청 후 감사 표현 - 짧지만 의무적 |

**Audrey 교훈**: "I need X"가 아니라 "One thing I will ask is if you can share X" - 요청을 "ask"로 포장. 그리고 "so that we can Y"로 이유 부여. 마지막으로 "That would be very helpful"로 마무리. 이 3단 요청 공식을 외워. 한국어 "주소 공유 부탁드립니다"의 영어 버전이지만 훨씬 구조적.

### 단계 3: 작업 항목 나열 (Work Item Enumeration)

Trent는 on-site에서 할 일을 "and then in addition to that we will..."로 나열한다. 각 항목마다 동사가 명확.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `and then in addition to that we will go on site, install, set up X, verify Y` | "and then in addition to that we will go on site, install, set up the remaining three servers and all the additional items, verify that all five servers are up and running" | 작업 항목 나열 - 동사 연쇄 (install, set up, verify) |
| `The X that we also installed Y and tested with Z so we know that they're working` | "The three additional servers that we also installed the custom BIOS and tested with the CXL solution at Liquid so we know that they're working" | 사전 검증 강조 - "so we know that" |

**Audrey 교훈**: 영어 회의에서 작업 항목은 동사로 나열한다. "install, set up, verify" - 이렇게 동사 3개를 쓰면 작업 범위가 명확해진다. 한국어로는 "설치하고 세팅하고 확인합니다"인데, 영어는 동사 사이에 쉼표만. 그리고 "so we know that they're working" - 사전 검증을 강조할 때 "so we know that"을 써서 신뢰를 준다.

### 단계 4: 이슈 진단 보고 (Issue Status Report)

이슈가 있을 때, Trent와 Vincent는 "we did receive X" → "we believe Y" → "we feel that we should be able to Z"의 공식을 쓴다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we did receive from X received Y for Z that will help with W` | "we did receive from our chassis manufacturer received a new firmware for the retimers in the chassis that will help with some of the linked issues" | 이슈 + 조치 보고 - "did receive"로 강조 |
| `We also think just with X on the site he can verify Y` | "We also think just with Stainless on the site he can verify all the settings" | 현장 검증 가능성 표시 |
| `we feel that we should be able to resolve it when we go on site` | "we feel that we should be able to resolve it when we go on site" | "we feel that we should be able to" - 자신감 표현 공식 |

**Audrey 교훈**: 이슈 보고는 3단이다. ① "we did receive X" (조치 받음) ② "we also think with Y on site he can verify Z" (현장 검증 가능) ③ "we feel that we should be able to resolve it" (해결 자신감). "we feel that we should be able to" - "we can"이 아니라 "we feel that we should be able to"가 훨씬 정중하고 신뢰감 있다. "should be able to"가 핵심.

### 단계 5: 액션 아이템 정리 (Action Item Wrap-up)

회의 마무리에 Trent는 "one action item for me was to confirm X"로 자신의 액션을 명시한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `one action item for me was to confirm X` | "one action item for me was to confirm the the the ocp networking device for out of bad management for the super micro server" | 자신의 액션 아이템 명시 |
| `me and Vincent will discuss with X and confirm after we discuss with them` | "me and Vincent will discuss with super micro and confirm after we discuss with them" | 협업 대상 + 시퀀스 명시 |
| `I will be sending you some emails offline regarding some of the action items we discussed` | "I will be sending you some emails offline regarding some of the action items we discussed" | 오프라인 후속 명시 |

**Audrey 교훈**: 회의 마무리에 자신의 액션을 "one action item for me was to..."로 명시한다. "I'll check"가 아니라 "action item for me was to" - 이게 책임을 명시하는 공식. 그리고 "I will be sending you some emails offline regarding X" - 회의에서 끝내지 못한 것은 "offline"로 이월. "offline"은 회의 후 이메일/개별 논의를 뜻하는 핵심 단어다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

Type C 회의에서의 회피는 "안 됩니다"가 아니라 "일정은 조정 가능", "펌웨어는 테스트 중", "샘플은 고가라 조심" 등이다.

### 전략 1: 일정 여유 확보 (Schedule Cushion)

확정 일정을 피하고 "we are expecting" + "should be more than enough"으로 여유를 만든다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 체류 일수 | "We are expecting to stay a total of five days but we plan to spend two days at SK Hanex." | "총 5일 체류 예정이지만 SK Hynix에서는 2일 예정입니다" |
| 일정 충분성 | "we scheduled two days should be more than enough but for sure we won't leave the country until everything is up and running so don't worry" | "2일 예정했고 충분할 것이지만, 모든 게 가동될 때까지 귀국 안 하니 걱정 마세요" |

**패턴 공식**: `We are expecting to stay X days but we plan to spend Y days at Z. We scheduled Y should be more than enough but for sure we won't leave the country until everything is up and running.`

**Audrey 교훈**: "should be more than enough" - 충분하다는 표현. 그리고 "for sure we won't leave the country until everything is up and running" - "for sure"로 확신, "won't leave until"로 조건부 완료 약속. 한국어 "다 될 때까지 안 갑니다"의 영어 버전이지만 "for sure" + "until"이 핵심. 이게 신뢰를 준다.

### 전략 2: 펌웨어 공개 지연 (Firmware Release Deferral)

펌웨어를 바로 공유할 수 없을 때, "testing 중" + "as soon as available"로 미룬다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 펌웨어 공유 시점 | "the firmware is currently being evaluated by our engineering team at the moment so we possibly could share it before Daniel comes on site but we wouldn't want to share it until they're testing us" | "펌웨어는 현재 엔지니어링팀 평가 중이라 현장 방문 전엔 공유 가능할 수도 있지만, 테스트 전엔 공유하고 싶지 않습니다" |
| 후속 약속 | "as soon as it's available we will ask them to release it to share it with you once they're done testing" | "테스트 완료되는 대로 릴리스해서 공유하겠습니다" |

**패턴 공식**: `X is currently being evaluated by Y so we possibly could share it before Z but we wouldn't want to share it until testing. As soon as it's available we will ask them to release it.`

**Audrey 교훈**: "we wouldn't want to share it until" - "until"로 조건을 건다. "공유하고 싶지 않다"고 직접 말하지만 "until testing"으로 이유를 댄다. 그리고 "as soon as it's available" - "가능한 한 빨리"의 정중 버전. "we will ask them to release it" - 자기가 결정하는 게 아니라 "ask them"으로 엔지니어링팀에 책임을 둔다. 이게 부서 간 책임 분산 화법이다.

### 전략 3: 샘플 고가 경고 (Sample Value Hedging)

샘플(production carriers)이 고가라 파손 우려를 표현할 때, "each one of them is very costly" + "I'm concerned about"로 경고.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 샘플 고가 | "we don't have a sample carriers as submit mentioned these are actual production carriers and each one of them this this were designed by liquid so each one of them is very costly" | "샘플 캐리어가 없고, 실제 양산 캐리어라 하나하나 매우 고가입니다" |
| 파손 우려 | "I'm concerned about you know ESD or somebody grabbing the the cards and then they are they may be they may become damaged" | "ESD나 누가 카드를 만져서 손상될까 우려됩니다" |
| 해결 약속 | "but let me talk with my team and figure out how we do that" | "팀과 이야기해서 어떻게 할지 알아보겠습니다" |

**패턴 공식**: `We don't have sample X. These are actual production Y. Each one of them is very costly. I'm concerned about Z. But let me talk with my team and figure out how we do that.`

**Audrey 교훈**: 샘플이 고가일 때 "costly"라는 단어를 쓴다. "expensive"보다 "costly"가 더 전문적. 그리고 "I'm concerned about X" - 우려를 명시하되 "but let me talk with my team and figure out how"로 해결 의지를 표시. "figure out how we do that" - "how"를 문장 끝에 두는 회화체.

### 전략 4: 혼동 정정 (Misunderstanding Correction)

상대와 Supermicro 사이의 혼동을 정정할 때, "there was some confusion because"로 부드럽게 출발.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| OCP 카드 혼동 | "Okay so there was some confusion because I had asked Supermicro that the customer reported that they don't have a networking card so they said please provide the OCP networking device and they said no there was a networking device already inside the server" | "혼동이 있었습니다. Supermicro에 물어보니 고객이 네트워크 카드가 없다고 해서 OCP를 제공하라고 했는데, 서버 안에 이미 네트워크 카드가 있다고 하더군요" |
| 정정 | "so it was a misunderstanding you need you need you need the networking device for out of band management" | "오해였습니다. out of band management용 네트워크 장치가 필요한 거였습니다" |

**패턴 공식**: `There was some confusion because X. So it was a misunderstanding. You need Y for Z.`

**Audrey 교훈**: 혼동을 정정할 때 "you misunderstood"가 아니라 "there was some confusion" - 주어를 "you"에서 "confusion"으로 빼서 비난감 제거. 그리고 "it was a misunderstanding" - "misunderstanding"은 누구의 잘못도 아닌 중성적 표현. 이게 정정 화법의 핵심이다.

### 전략 5: 책임 분산 (Responsibility Distribution)

자기가 결정하지 못하는 것은 "let me take that action item offline" + "discuss with my team"으로 분산.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 액션 수령 | "Steve let me take that action item offline and I will discuss with my team and see how we can get those carriers" | "Steve, 그 액션은 제가 오프라인으로 받고 팀과 논의해서 캐리어를 어떻게 보낼지 보겠습니다" |
| 내부 처리 | "Steve I'll work with you on that one but we will I will take care of this internally uh on the liquid side" | "Steve, 그건 같이 작업하되 Liqid 내부는 제가 처리하겠습니다" |

**패턴 공식**: `Let me take that action item offline and I will discuss with my team and see how we can X. I'll work with you on that one but I will take care of this internally.`

**Audrey 교훈**: "let me take that action item offline" - 액션을 "offline"으로 받는다. 회의에서 해결하지 않겠다는 뜻. 그리고 "I will take care of this internally" - "internally"로 내부 처리를 명시. 외부 파트너에게 책임을 넘기지 않겠다는 의지. "take care of"는 "처리하다"의 가장 자연스러운 영어 표현이다.

---

## 3. 정중한 도전 화법 (SK 측 질문자)

SK 측이 이슈 진단·일정·샘플을 정중하게 묻는 패턴. **네가 직접 써야 할 화법**이다.

### 질문 유형 1: 이슈 근원 질문 (Root Cause Inquiry)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we have shared our status with X and there is some issue with Y so we want to know that what is the issue or what is the root cause to solve this issue in our site before traveling` | "we have shared our status set up status with the two host server and there is there is some issue with connecting to host to the CXS chassis so so we want to know that what is the issue or what is the root cause to solve this issue in our site before traveling to our site" | 상태 공유 + 이슈 명시 + 근원 질문 - "before traveling"으로 시급성 표시 |

**Audrey 교훈**: 이 질문은 3단 구조다. ① "we have shared our status with X" (상태 공유) ② "there is some issue with Y" (이슈 명시) ③ "we want to know what is the issue or what is the root cause to solve this issue before traveling" (근원 질문 + 시급성). "before traveling"이 핵심 - 현장 방문 전에 해결하고 싶다는 의지. 이게 정중하면서도 시급성을 전달하는 화법이다.

### 질문 유형 2: 펌웨어 수급 확인 (Firmware Availability Check)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `can we receive the X in this week?` | "this is Seonjun so can we receive the firmware in this week?" | 짧고 직접적인 수급 질문 - "this is X"로 자기 소개 후 질문 |
| `we want to know that what is the current details status in getting the chassis` | "we want to know that what is the current details status in getting the chassis" | 상세 상태 요청 - "current details status" |

**Audrey 교훈**: "can we receive the X in this week?" - 가장 직접적인 수급 질문. "is it possible"로 시작하지 않고 "can we receive"로 바로 묻는다. 긴급할 때는 이렇게 직접 묻는 게 효과적. 그리고 자기 소개 "this is Seonjun"을 먼저 하고 질문 - 전화 회의에서 누군지 명시하는 의무적 화법.

### 질문 유형 3: 일정 충분성 확인 (Schedule Adequacy Check)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `And how many days are you expecting to stay in Korea?` | "And how many days are you expecting to stay in Korea?" | 체류 일수 질문 - "expecting to" |
| `We expected the setup is working good and I think yes today's is okay` | "We expected the setup is working good and I think yes today's is okay" | 일정 충분성 의견 - "I think yes X is okay" |

**Audrey 교훈**: "how many days are you expecting to stay" - "expecting to"가 핵심. "staying"이 아니라 "expecting to stay" - 상대의 예정을 존중하는 화법. 그리고 "I think yes today's is okay" - 자기 의견을 "I think yes"로 표시. 한국어 "2일이면 충분할 것 같습니다"의 영어 버전.

### 질문 유형 4: 샘플 호환성 질문 (Sample Compatibility Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we don't know the what type of X is can compatible to our Y so I want to just know what is the X model numbers okay that are compatible to our Y` | "we don't know the what type of OCP is can compatible to our SMC server so I want to just know what is the OCP model numbers okay that are compatible to our SMC server" | 호환성 질문 - "compatible to" + "model numbers" |
| `and do you expect it when when it's arrived this server they just sent it` | "do you expect it when when it's arrived this server they just sent it" | 도착 예정 질문 - "do you expect it when" |

**Audrey 교훈**: "compatible to our X" - 호환성을 물을 때 "compatible to"를 쓴다. 그리고 "model numbers" - 구체 모델 번호를 요구. 모호한 "어떤 거 쓸 수 있나요?"가 아니라 "OCP model numbers that are compatible to our SMC server"로 정확히. 이게 엔지니어의 질문 방식이다.

### 질문 유형 5: 입장 절차 안내 (Entry Procedure Guidance)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I think and entry procedure for SK Hanix I think Zespro can handle it so since visitor and vehicle registrations are required so please first provide Zespro with the details` | "I think entry procedure for SK Hanix I think Zespro can handle it so since visitor and vehicle registrations are required so please first provide Zespro with the details of the liquid personal busy information" | 입장 절차 안내 - "visitor and vehicle registrations are required" + "please provide X with the details" |

**Audrey 교훈**: SK 측이 Liqid에게 입장 절차를 안내할 때. "visitor and vehicle registrations are required" - "required"로 의무성을 명시. 그리고 "please first provide Zespro with the details" - ZesPro(로컬 파트너)를 통하도록 안내. 한국어 "방문자·차량 등록 필요하니 ZesPro에 정보 제공해 주세요"의 영어 버전. "please provide X with Y"가 정중한 안내 공식.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

Type C 회의의 핵심. 일정 협상, 샘플 수량 조율, 액션 아이템 정리의 언어.

### 일정 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 일정 명시 | Trent | "we will expect to start on Monday and we will coordinate with Zest Pro to figure out which days" | "expect to start" + "coordinate with X to figure out Y" |
| 체류 일수 | Trent | "We are expecting to stay a total of five days but we plan to spend two days at SK Hanex" | "expecting to stay X but plan to spend Y at Z" |
| 완료 보증 | Trent | "for sure we won't leave the country until everything is up and running so don't worry" | "for sure we won't leave until X" - 완료 조건부 체류 |
| 일정 확인 | SK | "I think the traveling schedule will be fine to us" | "will be fine to us" - 일정 수락 |
| 일정 조정 의향 | Trent | "Jungmin if we have to stay longer we will" | "if we have to X we will" - 조건부 확장 |

**Audrey 교훈**:
- "for sure we won't leave until everything is up and running" - Type C 회의에서 가장 강력한 신뢰 표현. "for sure"로 확신, "until X"로 조건, "don't worry"로 안심. 이 3단을 외워.
- "if we have to stay longer we will" - 조건부 확장 의향. "if we have to X we will" - 한국어 "필요하면 더 있겠습니다"의 영어 버전.

### 샘플 수량 조율 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 수량 명시 | Steve | "we are also bringing our 26 modules to install in ricketts chassis and showcase them" | "bringing X to install in Y and showcase Z" |
| 수량 확인 | Trent | "you will bring the 20 devices correct" | "you will bring X correct" - 확인 질문 |
| 캐리어 수 | Trent | "we'll get you the the 10 carrier so you can fully populate 20 devices in the box" | "get you X so you can fully populate Y" - 수량 채움 |
| 데모 유형 | Steve | "we we show the in the HPED we will show the cold demo or the live demo" | "cold demo or live demo" - 데모 유형 구분 |
| 데모 확인 | Trent | "just cold demo" + "it should it should be a very nice cold demo" | "just cold demo" - 데모 유형 확정 |

**Audrey 교훈**:
- "cold demo" vs "live demo" - 전시회 데모의 핵심 구분. "cold demo"는 전원 안 넣는 전시용, "live demo"는 실제 가동. 이 단어를 모르면 전시회 협상이 안 된다.
- "you will bring X correct" - 확인 질문. "correct"를 끝에 붙여서 "그렇죠?"의 의미. "you will bring 20 devices correct" - "20개 가져오시죠?"
- "fully populate X devices in the box" - "populate"가 핵심. "채우다"의 전문 용어. 서버 슬롯에 장치를 꽂는 것을 "populate"라 한다.

### 액션 아이템 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 자기 액션 명시 | Trent | "one action item for me was to confirm the the the ocp networking device for out of bad management" | "one action item for me was to X" - 자기 액션 |
| 액션 수령 | Trent | "Steve let me take that action item offline" | "let me take that action item offline" - 오프라인 액션 수령 |
| 내부 처리 | Trent | "I will take care of this internally uh on the liquid side" | "take care of this internally" - 내부 처리 명시 |
| 후속 이메일 | Trent | "I will be sending you some emails offline regarding some of the action items we discussed" | "emails offline regarding X" - 오프라인 후속 |
| 오프라인 협업 | Trent | "Steve I'll work with you on that one" | "I'll work with you on that one" - 협업 의지 |

**Audrey 교훈**:
- "one action item for me was to X" - 자기 액션을 명시하는 공식. "for me"가 핵심. 자기 책임이라는 표시.
- "let me take that action item offline" - 회의에서 해결 못 할 때 "offline"로 이월. "take"로 액션을 "받는다". 이게 책임 수령의 공식.
- "I will take care of this internally" - "internally"가 핵심. 외부에 넘기지 않고 내부에서 처리하겠다는 의지. "take care of"는 "처리하다"의 가장 자연스러운 영어.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 on-site install / CXL / 전시회 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **on site install** | 현장 설치 | "we will go on site, install, set up the remaining three servers" - "on site" + 동사 나열 |
| **drop-ship** | 중간 창고 안 거치고 직접 배송 | "the two servers that drop-ship directly from Supermicro" - "drop-ship from X" |
| **custom BIOS** | 맞춤 BIOS | "we install the custom BIOS and then we link it and connect it to the Liquid CXL before we ship" - 사전 설치 순서 |
| **retimer** | 신호 재생 칩 | "a new firmware for the retimers in the chassis that will help with some of the linked issues" - 펌웨어 업데이트 대상 |
| **chassis** | 서버/스토리지 프레임 | "there is some issue with connecting to host to the CXS chassis" - CXL 섀시 연결 이슈 |
| **host server** | 호스트 서버 | "we can install the two GPUs through the one host server" - GPU 설치 단위 |
| **GPU power cable** | GPU 전원 케이블 | "those three additional servers will include the GPU power cables for the H100s" - H100 전원 케이블 |
| **out of band management** | 대역 외 관리 (전용 네트워크) | "you need the networking device for out of band management" - OOB 관리용 NIC |
| **OCP card** | Open Compute Project 규격 카드 | "we want the NS card on OCP type" - OCP 타입 네트워크 카드 |
| **cold demo** | 전원 안 넣는 전시용 데모 | "we will show the cold demo or the live demo it's just cold demo" - HPE Discover 데모 유형 |
| **live demo** | 실제 가동 데모 | "that makes us feel a little better about having the live demo live boards on the show floor" - "live boards on the show floor" |
| **production carrier** | 양산용 캐리어 (샘플 아님) | "these are actual production carriers and each one of them is very costly" - 고가 양산품 |
| **E1.S drive** | E1.S 규격 SSD | "they're going to bring 20 of the e1s drives" - 전시용 드라이브 |
| **populate** | 슬롯에 장치 꽂기 | "you can fully populate 20 devices in the box" - "fully populate X in Y" |
| **ESD** | 정전기 방전 | "I'm concerned about you know ESD or somebody grabbing the the cards" - 정전기 우려 |
| **plastic cover** | 전시용 덮개 | "we already prepared the plastic cover" - 전시회 보호용 |
| **show floor** | 전시장 바닥 | "having the live demo live boards on the show floor" - "on the show floor" |
| **hand carry** | 기내 휴대 | "maybe Dave needs to hand carry them to the show" - 샘플 기내 반입 |
| **bring up** | 하드웨어 초기 구동 | "verify that all five servers are up and running" - "up and running" |
| **dial in** | 원격 접속 | "they will also need to dial in to theiRDIM back at HQ" - HQ 원격 접속 |
| **tracking number** | 운송장 번호 | "Zespro will be sharing the tracking number with the servers" - 출하 추적 |
| **business days** | 영업일 | "the package arrives between three to four business days" - 영업일 기준 |
| **visitor registration** | 방문자 등록 | "visitor and vehicle registrations are required" - SK Hynix 입장 절차 |
| **action item** | 회의 후 할 일 | "one action item for me was to confirm the OCP networking device" - 책임 항목 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 48개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 일정 조율 (Schedule Coordination) ──
- id: m08-001
  expression: "we will expect to start on X and we will coordinate with Y to figure out Z"
  category: schedule_opening
  function: schedule_stating
  speaker_role: coordinator
  difficulty: 4
  context: "we will expect to start on Monday and we will coordinate with Zest Pro to figure out which days we're going to be in which days we will be at SSSK hynix's"
  note: Type C 회의 시작 공식 - "expect to start" + "coordinate with X to figure out Y"

- id: m08-002
  expression: "I believe X but I need to confirm with Y"
  category: schedule_hedging
  function: tentative_stating
  speaker_role: coordinator
  difficulty: 4
  context: "I believe Monday or Tuesday but I need to confirm with Zest Pro"
  note: "I believe X but I need to confirm with Y" - 단정 피하는 화법

- id: m08-003
  expression: "One thing I will ask is if you can share X so that we can Y"
  category: request_polite
  function: ask_with_reason
  speaker_role: coordinator
  difficulty: 4
  context: "One thing I will ask is if you can share the address office location so that we can look at booking the travel"
  note: 정중한 요청 공식 - "I will ask" + "so that we can"

- id: m08-004
  expression: "That would be very helpful."
  category: gratitude_short
  function: thanks_after_request
  speaker_role: coordinator
  difficulty: 2
  context: "That would be very helpful."

- id: m08-005
  expression: "We are expecting to stay a total of X days but we plan to spend Y days at Z"
  category: schedule_stating
  function: duration_split
  speaker_role: coordinator
  difficulty: 4
  context: "We are expecting to stay a total of five days but we plan to spend two days at SK Hanex"
  note: 체류 일수 분할 - "expecting to stay X but plan to spend Y at Z"

- id: m08-006
  expression: "we scheduled X should be more than enough but for sure we won't leave the country until everything is up and running"
  category: schedule_guarantee
  function: completion_commitment
  speaker_role: coordinator
  difficulty: 5
  context: "we scheduled two days should be more than enough but for sure we won't leave the country until everything is up and running so don't worry"
  note: Type C 핵심 신뢰 표현 - "for sure" + "until X" + "don't worry"

- id: m08-007
  expression: "if we have to stay longer we will"
  category: conditional_extension
  function: extension_willingness
  speaker_role: coordinator
  difficulty: 3
  context: "Jungmin if we have to stay longer we will"

- id: m08-008
  expression: "I think the traveling schedule will be fine to us"
  category: schedule_acceptance
  function: agreement
  speaker_role: questioner
  difficulty: 3
  context: "I think the traveling schedule will be fine to us"
  note: "will be fine to us" - 일정 수락 표현

# ── 작업 항목 나열 (Work Item Enumeration) ──
- id: m08-009
  expression: "and then in addition to that we will go on site, install, set up X, verify Y"
  category: work_enumeration
  function: task_listing
  speaker_role: coordinator
  difficulty: 4
  context: "and then in addition to that we will go on site, install, set up the remaining three servers and all the additional items, verify that all five servers are up and running"
  note: 동사 연쇄 - install, set up, verify

- id: m08-010
  expression: "The X that we also installed Y and tested with Z so we know that they're working"
  category: pre_verification
  function: prior_test_stating
  speaker_role: coordinator
  difficulty: 4
  context: "The three additional servers that we also installed the custom BIOS and tested with the CXL solution at Liquid so we know that they're working"
  note: "so we know that they're working" - 사전 검증 강조

- id: m08-011
  expression: "those should be very easy when we when we arrive on site"
  category: ease_projection
  function: difficulty_downplay
  speaker_role: coordinator
  difficulty: 3
  context: "those should be very easy when we when we arrive on site"

- id: m08-012
  expression: "we will make sure that all five servers are attached to the Liquid CXL chassis and working"
  category: completion_promise
  function: full_verification
  speaker_role: coordinator
  difficulty: 4
  context: "when we go on site we will make sure that all five servers are attached to to the Liquid CXL chassis and working with the GPUs installed and everything should be working"

# ── 이슈 진단 (Issue Diagnosis) ──
- id: m08-013
  expression: "we have shared our status with X and there is some issue with Y so we want to know that what is the issue or what is the root cause to solve this issue"
  category: issue_report
  function: root_cause_inquiry
  speaker_role: questioner
  difficulty: 5
  context: "we have shared our status set up status with the two host server and there is there is some issue with connecting to host to the CXS chassis so so we want to know that what is the issue or what is the root cause to solve this issue in our site before traveling to our site"
  note: SK 측 이슈 보고 3단 - 상태 공유 + 이슈 명시 + 근원 질문

- id: m08-014
  expression: "has X responded to the email regarding the current status?"
  category: status_check
  function: follow_up_inquiry
  speaker_role: coordinator
  difficulty: 3
  context: "has Richmond responded to the email to your email regarding the the current status?"

- id: m08-015
  expression: "we did receive from X received Y for Z that will help with some of the linked issues"
  category: action_received
  function: receipt_stating
  speaker_role: technical
  difficulty: 4
  context: "we did receive from our chassis manufacturer received a new firmware for the retimers in the chassis that will help with some of the linked issues that we did receive there we believe"
  note: "did receive"로 수신 강조

- id: m08-016
  expression: "We also think just with X on the site he can verify Y"
  category: onsite_verification
  function: site_check_option
  speaker_role: technical
  difficulty: 4
  context: "We also think just with Stainless on the site he can verify all the settings that were applied during the initial setup he may be able to resolve it without any additional firmware changes"

- id: m08-017
  expression: "we feel that we should be able to resolve it when we go on site"
  category: confidence_expression
  function: resolution_confidence
  speaker_role: coordinator
  difficulty: 4
  context: "we feel that we should be able to resolve it when we go on site"
  note: "we feel that we should be able to" - "we can"보다 정중하고 신뢰감

- id: m08-018
  expression: "we've gotten this functioning with many other servers just like this so it should be a problem"
  category: precedent_citing
  function: similar_success
  speaker_role: technical
  difficulty: 3
  context: "we've gotten this functioning with many other servers just like this so it should be a problem"

- id: m08-019
  expression: "we have many many CXL boxes installed in Korea and in the US and they are running with no issues"
  category: track_record
  function: reliability_evidence
  speaker_role: coordinator
  difficulty: 3
  context: "we have many many CXL boxes installed in Korea and in the US and they are running with no issues"

- id: m08-020
  expression: "But we will be bringing some updated firmware just in case"
  category: contingency
  function: backup_plan
  speaker_role: technical
  difficulty: 3
  context: "But we will be bringing some updated firmware just in case"
  note: "just in case" - 만일을 위한 백업 표현

# ── 펌웨어 공개 지연 (Firmware Deferral) ──
- id: m08-021
  expression: "the firmware is currently being evaluated by our engineering team at the moment"
  category: status_in_progress
  function: testing_stating
  speaker_role: technical
  difficulty: 4
  context: "the firmware is currently being evaluated by our engineering team at the moment"
  note: "currently being evaluated by X" - 진행 중 상태 표현

- id: m08-022
  expression: "we possibly could share it before X but we wouldn't want to share it until Y"
  category: conditional_deferral
  function: release_delay
  speaker_role: technical
  difficulty: 5
  context: "we possibly could share it before Daniel comes on site but we wouldn't want to share it until they're testing us"
  note: "we wouldn't want to share it until" - 조건부 지연

- id: m08-023
  expression: "as soon as it's available we will ask them to release it to share it with you once they're done testing"
  category: release_promise
  function: post_test_release
  speaker_role: coordinator
  difficulty: 4
  context: "as soon as it's available we will ask them to release it to share it with you once they're done testing"
  note: "as soon as X available we will ask them to release" - 부서 간 책임 분산

# ── 혼동 정정 (Misunderstanding Correction) ──
- id: m08-024
  expression: "there was some confusion because X"
  category: confusion_stating
  function: blame_neutralizing
  speaker_role: coordinator
  difficulty: 4
  context: "there was some confusion because I had asked Supermicro that the customer reported that they don't have a networking card"
  note: "you misunderstood" 대신 "there was some confusion" - 비난감 제거

- id: m08-025
  expression: "so it was a misunderstanding you need the networking device for out of band management"
  category: correction_stating
  function: neutral_correction
  speaker_role: coordinator
  difficulty: 3
  context: "so it was a misunderstanding you need you need you need the networking device for out of band management"
  note: "misunderstanding" - 중성적 정정 표현

- id: m08-026
  expression: "Okay we will discuss offline with X and find you and try to obtain the right device"
  category: offline_resolution
  function: offline_promise
  speaker_role: questioner
  difficulty: 4
  context: "Okay we will discuss offline with Supermicro and find you and try to obtain the the the right device"

# ── 샘플 조율 (Sample Coordination) ──
- id: m08-027
  expression: "we are also bringing our X modules to install in Y chassis and showcase them"
  category: sample_stating
  function: sample_quantity
  speaker_role: partner
  difficulty: 3
  context: "we are also bringing our 26 modules to install in ricketts chassis and showcase them"

- id: m08-028
  expression: "you will bring the X devices correct"
  category: quantity_confirm
  function: verify_count
  speaker_role: coordinator
  difficulty: 3
  context: "you will bring the 20 devices correct"

- id: m08-029
  expression: "we'll get you the X carrier so you can fully populate Y devices in the box"
  category: populate_stating
  function: full_fill
  speaker_role: coordinator
  difficulty: 4
  context: "we'll get you the the 10 carrier so you can fully populate 20 devices in the box"
  note: "populate X devices in the box" - 슬롯 채우기

- id: m08-030
  expression: "we don't have a sample carriers. These are actual production carriers and each one of them is very costly"
  category: sample_value
  function: costly_warning
  speaker_role: coordinator
  difficulty: 4
  context: "we don't have a sample carriers as submit mentioned these are actual production carriers and each one of them this this were designed by liquid so each one of them is very costly"

- id: m08-031
  expression: "I'm concerned about ESD or somebody grabbing the cards and then they may become damaged"
  category: damage_concern
  function: risk_stating
  speaker_role: coordinator
  difficulty: 4
  context: "I'm concerned about you know ESD or somebody grabbing the the cards and then they are they may be they may become damaged"

- id: m08-032
  expression: "but let me talk with my team and figure out how we do that"
  category: team_consultation
  function: internal_escalation
  speaker_role: coordinator
  difficulty: 3
  context: "but let me talk with my team and figure out how we do that"

- id: m08-033
  expression: "maybe Dave needs to hand carry them to the show"
  category: transport_method
  function: hand_carry_option
  speaker_role: coordinator
  difficulty: 3
  context: "maybe Dave needs to hand carry them to the show"
  note: "hand carry" - 기내 휴대 전문 용어

- id: m08-034
  expression: "we want to make sure this is our first show together we want to make sure SKHannis is successful"
  category: partnership_stating
  function: shared_success
  speaker_role: coordinator
  difficulty: 4
  context: "we want to make sure this is our first show together we want to make sure uh SKHannis is successful"
  note: 파트너십 강조 - "first show together" + "make sure X is successful"

- id: m08-035
  expression: "we want to be best foot forward in the show so this is this is a must do"
  category: priority_stating
  function: mandatory_emphasis
  speaker_role: coordinator
  difficulty: 4
  context: "we want to be best foot forward in the in the show so this is this is a must do"
  note: "best foot forward" + "must do" - 우선순위 최고 표현

- id: m08-036
  expression: "we will show the cold demo or the live demo"
  category: demo_type
  function: demo_inquiry
  speaker_role: partner
  difficulty: 3
  context: "we we show the in the HPED we will show the cold demo or the live demo"
  note: "cold demo" vs "live demo" - 전시회 데모 핵심 구분

- id: m08-037
  expression: "that makes us feel a little better about having the live demo live boards on the show floor"
  category: reassurance
  function: concern_relief
  speaker_role: coordinator
  difficulty: 4
  context: "that makes us feel a little better about having the live demo live uh boards on the show floor"
  note: "makes us feel a little better about X" - 우려 완화

# ── 액션 아이템 (Action Items) ──
- id: m08-038
  expression: "one action item for me was to confirm X"
  category: self_action
  function: own_responsibility
  speaker_role: coordinator
  difficulty: 3
  context: "one action item for me was to confirm the the the ocp networking device for out of bad management for the super micro server"
  note: "one action item for me was to" - 자기 액션 명시 공식

- id: m08-039
  expression: "let me take that action item offline and I will discuss with my team and see how we can X"
  category: action_take
  function: offline_ownership
  speaker_role: coordinator
  difficulty: 5
  context: "Steve let me take that action item offline and I will discuss with my team and see how we can get those carriers"

- id: m08-040
  expression: "I'll work with you on that one but I will take care of this internally"
  category: internal_handling
  function: responsibility_scope
  speaker_role: coordinator
  difficulty: 4
  context: "Steve I'll work with you I'll work with you on that one but we will I will take care of this internally uh on the liquid side"
  note: "take care of this internally" - 내부 처리 명시

- id: m08-041
  expression: "I will be sending you some emails offline regarding some of the action items we discussed"
  category: offline_followup
  function: email_commitment
  speaker_role: coordinator
  difficulty: 3
  context: "I will be sending you some emails offline regarding some of the action items we discussed"

- id: m08-042
  expression: "if there's anything else we can discuss otherwise I will be sending you some emails"
  category: meeting_close
  function: wrap_up
  speaker_role: coordinator
  difficulty: 3
  context: "Steve if there's anything else we can discuss otherwise I will be sending you some emails offline regarding some of the action items we discussed"

# ── 입장 절차·지원 (Entry Procedure & Support) ──
- id: m08-043
  expression: "visitor and vehicle registrations are required so please first provide X with the details"
  category: entry_procedure
  function: requirement_stating
  speaker_role: questioner
  difficulty: 4
  context: "since visitor and vehicle registrations are required so please first provide Zespro with the details of the liquid personal busy information"

- id: m08-044
  expression: "we kindly ask if you could support Wi-Fi during their visit"
  category: support_request
  function: polite_facility_ask
  speaker_role: coordinator
  difficulty: 4
  context: "they will also need to dial in to theiRDIM back at HQ so we kindly ask if you could support Wi-Fi during their visit"
  note: "we kindly ask if you could support X" - 시설 지원 요청

- id: m08-045
  expression: "Just in case."
  category: contingency_short
  function: backup_note
  speaker_role: coordinator
  difficulty: 1
  context: "Just in case."

# ── 출하 추적 (Shipment Tracking) ──
- id: m08-046
  expression: "normally when we ship to Korea the package arrives between three to four business days"
  category: shipping_estimate
  function: delivery_estimate
  speaker_role: coordinator
  difficulty: 3
  context: "normally when we ship when we ship to Korea the package arrives between three to four business days"
  note: "business days" - 영업일 기준

- id: m08-047
  expression: "we expect it to be there by Friday timeframe and then Zespro will verify the shipment"
  category: arrival_estimate
  function: delivery_chain
  speaker_role: coordinator
  difficulty: 3
  context: "we expect it to be there by Friday timeframe and then Zespro will verify the shipment and make sure that the servers arrive at SK Hanix before we go on site on Monday morning"

- id: m08-048
  expression: "we really appreciate your patience and we're looking forward to arriving next week"
  category: closing_gratitude
  function: thanks_and_anticipation
  speaker_role: coordinator
  difficulty: 3
  context: "but we really appreciate your your your patience and we're looking forward to to arriving next week"
  note: "appreciate your patience" + "looking forward to arriving" - 마무리 감사
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-06-10 09 03 06_EN_Liqid-extracted.wav` (총 ~28분, 3,544단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 1-8) | Trent 일정 개시 + Jungmin 주소 공유 약속 + "we will go on site, install, set up, verify" | Type C 회의 시작 화법 + 동사 연쇄 | ★★☆ |
| 2 | 이슈 진단 (line 14-28) | Jungmin "we want to know the root cause" + Vincent "we did receive new firmware" + "we feel we should be able to resolve it" | 이슈 보고 + 자신감 표현 | ★★★ |
| 3 | 혼동 정정 (line 40-58) | OCP 카드 혼동 + "there was some confusion" + "it was a misunderstanding" + "we will discuss offline" | 혼동 정정 화법 | ★★★ |
| 4 | HPE Discover 샘플 조율 (line 89-101) | "20 of the e1s drives" + "production carriers very costly" + "best foot forward" + "must do" | 샘플 수량·고가 경고 + 우선순위 | ★★★★ |
| 5 | 마무리 액션 (line 107-117) | "one action item for me was to" + "let me take that action item offline" + "I will take care of this internally" + "looking forward to arriving" | 액션 아이템 정리 + 마무리 | ★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 4, 5가 가장 가치 높음 - 샘플 조율·액션 아이템 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **execution coordination** register다. 제품을 설명하는 게 아니라 "누가 언제 어디서 무엇을 할지"를 맞추는 화체. Type C의 핵심:
- **조율자 역할 (Trent)**: 일정 명시, 작업 항목 나열, 액션 아이템 정리 - 네가 설치 일정을 조율할 때
- **질문자 역할 (SK)**: 이슈 진단, 일정 확인, 샘플 호환성 질문 - 네가 파트너 방문을 받을 때
- **기술자 역할 (Vincent)**: 펌웨어 상태, 검증 가능성 표시 - 네가 기술 이슈를 보고할 때

### Pragmatics (화용론) 핵심
1. **"for sure we won't leave until X"**: Type C 회의에서 가장 강력한 신뢰 표현. "for sure"로 확신, "until X"로 조건. "다 될 때까지 안 갑니다"의 영어 버전. 한국어 "걱정 마세요"보다 훨씬 구체적.
2. **"there was some confusion because X"**: 혼동 정정 시 "you misunderstood" 절대 금지. "there was some confusion" - 주어를 "you"에서 "confusion"으로 빼서 비난감 제거. "misunderstanding"도 중성적.
3. **"let me take that action item offline"**: 회의에서 해결 못 할 때 "offline"로 이월. "take"로 액션을 "받는다". "I'll check"가 아니라 "take that action item"이 책임 수령의 공식.
4. **"each one of them is very costly"**: 샘플이 고가일 때 "costly" 사용. "expensive"보다 전문적. 그리고 "I'm concerned about X"로 우려를 명시하되 "let me figure out how"로 해결 의지.
5. **"best foot forward" + "must do"**: 우선순위 최고 표현. "best foot forward"는 "최선의 모습 보여주기"의 관용구. "must do"는 "필수"의 짧은 표현.

### 네가 당장 써야 할 Top 5
1. **"we will expect to start on X and we will coordinate with Y to figure out Z"** - Type C 회의 시작 공식
2. **"for sure we won't leave the country until everything is up and running"** - 완료 조건부 체류 약속
3. **"there was some confusion because X. It was a misunderstanding."** - 혼동 정정
4. **"let me take that action item offline and I will discuss with my team"** - 액션 수령 + 내부 논의
5. **"we want to be best foot forward in the show so this is a must do"** - 우선순위 최고 표현

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "월요일에 시작할 예정입니다" | "we will expect to start on Monday" | "expect to" - 예정의 정중 표현 |
| "다 될 때까지 안 갑니다" | "for sure we won't leave until everything is up and running" | "for sure" + "until" - 확신+조건 |
| "오해가 있었습니다" | "there was some confusion. It was a misunderstanding." | 주어 "you" → "confusion" |
| "내가 확인하겠습니다" | "let me take that action item offline" | "check" → "take action item" |
| "이건 필수입니다" | "this is a must do" | "must do" - 짧고 강한 필수 표현 |
| "샘플이 비쌉니다" | "each one of them is very costly" | "costly"가 "expensive"보다 전문적 |
| "팀과 논의하겠습니다" | "let me talk with my team and figure out how we do that" | "figure out how" - 회화체 |
| "감사합니다 기다려주셔서" | "we appreciate your patience and we're looking forward to arriving" | "appreciate your patience" - 감사의 공식 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 48개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 4절 협상 화법·2절 회피 화법을 중심으로 dump 작성
4. **비교 학습**: 9절 한국어-영어 비교표로 화법 차이 체득
5. **Type C 시뮬레이션**: 다음 파트너 방문·샘플 조율 회의 전, 4절 협상 화법을 소리 내 연습

---

*Textbook 08 - Liqid On-site Install & HPE Discover Coordination (2026-06-10). 회의 유형 C (sample/schedule coordination). 표현 DB 48개. 5개 발췌 구간. 작성: 2026-09-02.*
