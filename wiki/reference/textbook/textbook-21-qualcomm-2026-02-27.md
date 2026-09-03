---
textbook_id: 21
meeting: Qualcomm (Feb quarterly, roadmap/supply alignment)
date: 2026-02-27
type: B (roadmap/supply alignment)
partner: Qualcomm (AI Cloud / server CPU team, CXL memory solution architects)
sk_side: SK Hynix architecture, memory solution, CXL/HBF evaluation team
duration_words: 7246
audio: repo/webex-audio/2026-02-27 10 59 44_EN_Qualcomm-extracted.wav
transcript: repo/webex-audio/2026-02-27 10 59 44_EN_Qualcomm-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, qualcomm, cxl, hbf, high-bandwidth-flash, roadmap, supply-alignment, kv-cache, sample-schedule]
---

# Textbook 21 - Qualcomm HBF/CXL Roadmap Alignment (2026-02-27)

> **회의 유형**: B (roadmap/supply alignment) - 차세대 메모리 아키텍처(HBF) 및 CXL 로드맵 협의
> **학습 가치**: KPI 협상, 샘플 스케줄 조율, use case 탐색, 스펙 pushback, "aligned with X", "under consideration"
> **Audrey 관점**: 이 회의는 "roadmap 피칭 + 스펙 협상 + 샘플 요청"의 전형. Type B의 핵심인 Section 4(협상/액션) 언어가 밀집. 네가 파트너에게 로드맵을 맞출 때도, 요구사항을 밀어붙일 때도 배워야.

---

## 1. 발화 아키텍처 - Qualcomm 발표자의 로드맵 설계 (5단계)

Qualcomm 발표자는 로드맵 협의를 5단계 구조로 설계한다. 각 단계마다 **고정된 화법 공식**이 있다. 이게 네가 따라 배워야 할 "로드맵 협의의 뼈대"다.

### 단계 1: 포지셔닝 (Product Positioning)

발표자는 신제품을 소개하기 전에 **기존 제품 계층과의 비교**로 포지션을 잡는다. "우리 제품이 좋다"가 아니라 "이 계층 사이에 이 제품이 있다"로 시작.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `For a X, like the Y family, you have numerous Z` | "For our AI9 devices like AI9 family, you have numerous memory size... first call it AI NP, million IOPS, that's high performance SSD" | 제품 계층 구조로 문을 엶 |
| `Where in the middle, you can see it is we call X, which is like a very similar to Y, but based on Z` | "you can see it is we call you like AI9, high bandwidth flash that is the HBF, which is like a very similar to HBM, but based on the NAND flash" | 유사성 + 차이점으로 포지셔닝 |
| `This is just a positioning point of view` | "This is just a positioning point of view" | "positioning point of view" - 발표자가 맥락 한정을 명시 |

**Audrey 교훈**: 로드맵 발표는 "제품 스펙"으로 시작하지 않는다. **"계층 구조 속 위치"**로 시작한다. "X is like Y, but based on Z" - 이 공식을 외워. 이미 알고 있는 제품(HBM)에 연결해서 신제품(HBF)의 위치를 잡는다. 네가 신메모리 솔루션을 소개할 때, 먼저 기존 계층(HBM, SSD, CXL)을 나열하고 그 사이를 잡아라.

### 단계 2: KPI 테이블 제시 (KPI Specification)

포지셔닝 후, 수치 비교 테이블로 넘어간다. "If you take X as a baseline, then..."으로 비교 기준을 명시.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `If here is the comparison, like if you taking like X as a baseline, then Y is the Z` | "if you taking like HBM4 as a baseline, then 24 gigabit is the HBM4. Then you can see like in the AI9 is like that's in the middle for SSD baseline" | 비교 baseline 명시 |
| `We are promising at least NX like a Y for Z` | "we are promising at least 10X like a 240 gigabit die for HBEF" | "promising at least NX" - 수치 약속 |
| `Latency is like a X, which is like a Y times worse than Z` | "latency is like a five microsecond, which is like a 100 times worse than HBM" | 단점을 정직하게 수치화 - 신뢰構築 |
| `Endurance is we are targeting X, and data retention we are targeting like Y` | "Endurance is we are targeting 200K endurance, and data retention we are targeting like 24 to 48 hours" | "targeting"으로 KPI 명시 |

**Audrey 교훈**: "100 times worse than HBM" - 자기 제품 단점을 정직하게 수치화한다. 이게 로드맵 협의에서 신뢰를 만드는 화법이다. "우리 제품은 HBM보다 100배 느립니다" - 이 정도 정직함이 있어야 상대가 KPI를 믿고 협상할 수 있다. 한국어 발표에서는 단점을 숨기려 하지만, 영어 로드맵 협의에서는 단점을 수치로 드러내는 게 전문가 화법이다.

### 단계 3: use case 탐색 (Use Case Exploration)

KPI 테이블 후, "What is the right use case?"로 넘어간다. 여기가 이 회의의 핵심 - use case가 안 정해지면 KPI도 못 잡는다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `The first application we are thinking is like a X for Y` | "the first application we are thinking is like a CAS for KV cache" | "we are thinking" - use case 가설 제시 |
| `We have to find the right match` | "We have to find the right match" | "right match" - 워크로드-디바이스 매칭 강조 |
| `If workload is not matching with the device, the statistics, then it's not usable` | "If workload is not matching with the device, the statistics, then it's not usable" | 매칭 안 되면 사용 불가 - 전제 명시 |
| `There are two... One is X, we find the right match because Y. And then other one is can we do a Z` | "There are two... One is KV cache, we find the right match because you need a lot of bandwidth... And then other one is can we do a tier memory" | use case 이중 나열 |
| `We don't have answer of every question` | "For that one, we don't have answer of every question" | 모르는 것 인정 - 파트너십 요청 전제 |

**Audrey 교훈**: "We don't have answer of every question" - 모르는 것을 인정하는 게 로드맵 협의에서 파트너십의 시작이다. "We are thinking", "we don't have answer" - 이게 가설 단계의 정직한 화법. 한국어로는 "검토 중입니다"인데, 영어는 "we are thinking" + "we don't have answer"로 구체적으로 모르는 것을 드러낸다.

### 단계 4: 아키텍처 옵션 나열 (Architecture Options)

"Case one, case two, case three"로 아키텍처 옵션을 명시적으로 나열한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Case one where there's a hybrid? Today you have... Say for example, you have 8 HBM instead of that can be used like a 6 plus 2 or 7 plus 1` | "can we have a case one where there's a hybrid? Today you have... Say for example, you have 8 HBM instead of that can be used like a 6 plus 2 or 7 plus 1" | 구체 수치로 옵션 제시 |
| `Case two, is there any use case coming where... can we do like a replace HBM completely with HBF` | "Case two, is there any use case coming where the AI world is evolving so fast... can we do like a replace HBM completely with HBF" | 극단 옵션 제시 |
| `Third case is where you cannot replace the HBM, can you digitize?` | "Third case is where you cannot replace the HBM, can you digitize?" | 절충 옵션 |
| `And we don't know the answer. That's why we're saying like we are going to like trying to explore` | "And we don't know the answer. That's why we're saying like we are going to like trying to explore which would be right huge case" | 옵션 미확정 명시 |

**Audrey 교훈**: "Case one, case two, case three" - 옵션을 명시적으로 번호 붙여서 나열하는 게 영어 로드맵 협의의 구조다. 한국어로는 "경우가 몇 가지 있습니다"로 모호하게 넘기는데, 영어는 "Case one... Case two... Third case..."로 각 옵션을 독립된 단위로 제시한다. 그리고 각 옵션 뒤에 "we don't know the answer"로 미확정을 명시 - 이게 협상의 여지를 만든다.

### 단계 5: 다음 단계 요청 (Next Step Request)

발표 마지막에 KPI 보강 요청으로 연결. 여기가 협상이 시작된다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `We are seriously compare, compare the KPIs, X versus Y` | "we are seriously compare, compare the KPIs, HBM versus HBM, plus HBM you guys have" | "seriously compare" - 비교 의지 표시 |
| `So we do need some precise, more accurate numbers actually` | "So we do need some precise, more accurate numbers actually" | "do need" - 요구 강조 |
| `You can move me. So this time, if you can share the target KPI, okay? Then we can move forward` | "So this time, if you can share the target KPI, okay? Then we can move forward" | "Then we can move forward" - 다음 단계 조건 |
| `We have done some work... Now we are trying to quantitative` | "we have done qualitative... Now we are trying to quantitative" | 정성→정량 전환 명시 |

**Audrey 교훈**: "Then we can move forward" - 이게 로드맵 협의의 다음 단계 요청 공식이다. "If you can share X, then we can move forward" - 상대에게 책임을 전달하면서 다음 단계 조건을 명시. 한국어 "자료 주시면 검토하겠습니다"의 영어 버전이 "If you can share X, then we can move forward"다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. Qualcomm이 미확정 사항을 어떻게 정중하게 포장하는지. 로드맵 협의에서 "아직 모른다"를 어떻게 말하는지.

### 전략 1: "In flux" - 미확정 상태 정중 표현

가장 중요한 패턴. "모른다"가 아니라 "유동적이다"로 포장.

| 약점 | 원문 화법 | 번역 |
|:---|:---|:---|
| 타임라인 미확정 | "Yeah, this is because basically, yeah, introduction and open discussion. Right. Yeah, because this is like everything is in fluid" | "이건 기본적으로 소개와 공개 논의입니다. 모든 게 유동적이니까요" |
| KPI 미확정 | "You don't have a time, there is some timeframe, but this still is in flux, but at high level, KPI point of view" | "타임프레임은 있지만 여전히 유동적입니다. 다만 높은 수준의 KPI 관점에서는" |

**패턴 공식**: `This is like everything is in flux. There is some X, but this still is in flux, but at high level.`

**Audrey 교훈**: "In flux"는 로드맵 협의에서 가장 유용한 회피 단어다. "We don't know"가 아니라 "in flux" - "유동적이다"로 포장하면, 모르는 게 아니라 "아직 결정 중이다"가 된다. 한국어 "아직 논의 중입니다"의 영어 버전이 "this is in flux"다. 그리고 "but at high level"로 대략값을 주면 더 정중해진다.

### 전략 2: "We don't have answer of every question" - 모르는 것 인정 + 파트너십 요청

모르는 것을 인정하되, "그래서 파트너를 찾는다"로 전환.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| tiering 아키텍처 미정 | "For that one, we don't have answer of every question. We think one workload is very suitable, but... That's why we are looking for partner. Like a who's like... Because there's a lot of changes would be required from the host side, both in terms of hardware for the interface and the software" | "그건 모든 질문에 답이 없습니다. 하나의 워크로드는 적합하다고 생각하지만... 그래서 파트너를 찾고 있습니다. 호스트 측, 하드웨어와 소프트웨어 모두 많은 변경이 필요하니까요" |

**패턴 공식**: `We don't have answer of every question. That's why we are looking for partner. There's a lot of changes required from X side, both in terms of Y and Z.`

**Audrey 교훈**: "We don't have answer of every question" - 모르는 것을 인정하되, "That's why we are looking for partner"로 파트너십 요청으로 전환. 이게 정중한 "모름 + 도움 요청" 공식이다. 한국어 "관계자와 논의가 필요합니다"의 영어 버전이 "we don't have answer, that's why we are looking for partner"다.

### 전략 3: "Under works" - 진행 중 표현

아직 완료 안 된 것을 "진행 중"으로 포장.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 전력 수치 미완 | "Yeah, that is still under works right now" | "그건 여전히 작업 중입니다" |

**패턴 공식**: `That is still under works right now.`

**Audrey 교훈**: "Under works"는 "in progress"보다 더 회피적인 표현이다. "진행 중"이지만 언제 끝날지 모른다는 뉘앙스. 한국어 "작업 중입니다"의 영어 버전.

### 전략 4: "We don't know the answer. That's why we're saying we are going to try to explore" - 모름 + 탐색 전환

옵션 미확정을 "탐색 중"으로 포장.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| use case 미정 | "And we don't know the answer. That's why we're saying like we are going to like trying to explore which would be right huge case and then with the right combination" | "답을 모릅니다. 그래서 우리가 말하는 건, 어떤 게 올바른 use case일지 탐색하려고 한다는 겁니다" |

**패턴 공식**: `We don't know the answer. That's why we're saying we are going to try to explore which would be right X.`

### 전략 5: "Chicken and egg" - 순환 의존성 정중 표현

먼저 결정해야 할 것과 나중에 결정해야 할 것이 서로 물려 있을 때, 비유로 포장.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| KPI와 use case 순환 의존 | "This is a chicken and chicken. You still have chicken and chicken." | "이건 닭과 닭이에요. 여전히 닭과 닭이에요" |

**Audrey 교훈**: "Chicken and egg"의 변형 - 발표자가 "chicken and chicken"이라고 말하며 두 가지가 서로 물려 있음을 비유. 로드맵 협의에서 순환 의존성을 설명할 때 쓰는 화법. "어떤 걸 먼저 정해야 할지 모르는 상황"을 한 단어로 포장.

### 전략 6: "Still we have able to identify that any other use case it is very hard to compliment HBM" - 한계 인정 + HBM 보완 강조

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| use case 한계 | "so far we have able to identify that any other use case it is very hard to compliment HBM" | "지금까지 식별할 수 있는 건, 다른 use case는 HBM을 보완하기 매우 어렵다는 겁니다" |

---

## 3. 정중한 도전 화법 (SK 측 질문자)

SK 측이 로드맵·스펙·스케줄에 도전하면서도 정중하게 질문하는 패턴. **네가 직접 써야 할 화법**이다.

### 질문 유형 1: 타임라인 정밀 질문 (Timeline Precision Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Which time frame?` | "Which time frame?" | 짧고 직접 - 타임라인 확인 |
| `So when you are X available please consider the providing some a couple samples to us` | "when you are yes is available please consider the providing some a couple samples to us" | "please consider" - 정중한 샘플 요청 |
| `Then will you be also interested in early early early yes` | "Then will you be also interested in early early early yes" | "early early early" - 반복으로 강조 |
| `What is the difference between early yes and CS?` | "What is the difference between early yes and CS?" | 샘플 단계 차이 질문 |

**Audrey 교훈**: "Which time frame?" - 두 단어로 타임라인을 묻는 전문가 화법. "When?"보다 "Which time frame?"이 더 정중하고 구체적이다. 그리고 샘플 요청은 "please consider providing some a couple samples to us" - "give us"가 아니라 "please consider providing"으로 정중하게.

### 질문 유형 2: 스펙 pushback (Spec Pushback)

SK 측이 Qualcomm 스펙을 직접 도전하는 패턴. Type B의 핵심.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Is it including the software latency? The formula latency?` | "Is it including the software latency? The formula latency? Yeah. Is it?" | 스펙에 소프트웨어 지연 포함 여부 - 스펙 비교 기준 도전 |
| `And the pitch means you have to have the KPI numbers. Right?` | "And the pitch means you have to have the KPI numbers. Right?" | "Right?"로 압박 - KPI 수치화 요구 |
| `But we are seriously, again, we are seriously compare Apple to Apple, the target 29 or 20, 30 time. So I need you guys put the more target KPI` | "But we are seriously, again, we are seriously compare Apple to Apple, the target 29 or 20, 30 time. So I need you guys put the more target KPI" | "Apple to Apple" + "I need you guys put" - 강한 요구 |
| `But this table is good for the publications. But we are seriously compare Apple to Apple` | "But this table is good for the publications. But we are seriously compare Apple to Apple" | "for the publications" - 발표용 vs 실비교 구분 |

**Audrey 교훈**: "Apple to Apple" - 같은 조건 비교를 요구하는 전문가 화법. "이 테이블은 발표용이지만, 우리는 Apple to Apple로 비교해야 합니다" - 발표자료와 실제 협상용 수치를 구분. 그리고 "I need you guys put the more target KPI" - "need you"로 강한 요구. 한국어 "수치를 더 주셔야 합니다"의 영어 버전이 "I need you guys put the more target KPI"다.

### 질문 유형 3: 아키텍처 의도 질문 (Architecture Intent Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Why use that connection? I don't understand.` | "Why use that connection? I don't understand." | 직접적 - "I don't understand"으로 명확히 모름 표시 |
| `Is there any possibility for that one?` | "Is there any possibility for that one?" | "possibility" 탐색 |
| `Can we have a case one where there's a hybrid?` | "can we have a case one where there's a hybrid?" | 옵션 제안 |
| `Is there any use case coming where... can we do like a replace HBM completely with HBF` | "is there any use case coming where... can we do like a replace HBM completely with HBF" | 극단 옵션 제안 |

### 질문 유형 4: 비교 기준 제안 (Comparison Baseline Suggestion)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Best candidate is to compare with HBM 5` | "Best candidate is to compare with HBM 5. If you based on the current and your progress. That is always the target" | 비교 대상 제안 - "best candidate" |
| `Then maybe if you twill it, you should compare with the Compare with HBM 6. Then your target The KPI target should be higher` | "Then maybe if you twill it you should compare with HBM 6. Then your target KPI target should be higher" | 비교 대상 상향 제안 - pushback |
| `I can confirm the HBM HBM is almost pre-claimed HBM 5` | "I can confirm the HBM HBM is almost pre-claimed HBM 5" | SK 측이 HBM5를 비교 기준으로 확정 |

**Audrey 교훈**: "Best candidate is to compare with X" - 비교 기준을 제안하는 전문가 화법. "비교해야 합니다"가 아니라 "best candidate is X"로 권하면서 밀어붙인다. 그리고 "KPI target should be higher" - "should be"로 상향을 요구. 한국어 "목표가 더 높아야 합니다"의 영어 버전이 "KPI target should be higher"다.

### 질문 유형 5: 샘플 요청 (Sample Request)

Type B의 핵심 화법.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Also I got another email from Valkom for violet technology asking for one samples asking like a pricing` | "Also I got another email from Valkom for violet technology asking for one samples asking like a pricing" | 샘플 + 가격 요청 |
| `please, spend more energy on this` | "please, spend more energy on this" | 우선순위 요청 - "spend more energy" |
| `So when you are yes is available please consider the providing some a couple samples to us` | "So when you are yes is available please consider the providing some a couple samples to us" | "please consider providing" - 정중 샘플 요청 |
| `Sure Then will you be also interested in early early early yes` | "Then will you be also interested in early early early yes" | "early early early" - 반복으로 강조 |

**Audrey 교훈**: "Please, spend more energy on this" - 우선순위를 요구하는 직접 화법. "Please consider"보다 강하다. 로드맵 협의에서 샘플이 늦어질 때 쓰는 화법. 그리고 샘플 요청은 항상 "please consider providing"로 정중하게 - "give us samples"가 아니라.

### 질문 유형 6: 도입 질문 (Opening Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I want to, I wonder, I want to the recent you all, the specific plan for the CXL, the CPU product` | "I wonder, I want to the recent you all, the specific plan for the CXL, the CPU product" | "I wonder" - 정중한 호기심 표시 |
| `Could you please explain about the you all kinds of experience of developing or the manufacturing of the software CPU?` | "Could you please explain about the you all kinds of experience of developing or the manufacturing of the software CPU?" | "Could you please explain" - 정중한 설명 요청 |
| `Unless you do all the table, you are considering the 2028 for CSR just to E3. E3 is tight. But as you know, there are two kinds of CSR types. Another type is AIC` | "you are considering the 2028 for CSR just to E3. E3 is tight. But as you know, there are two kinds of CSR types. Another type is AIC" | 폼팩터 도전 - "as you know"로 전문가 전제 |

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

이 회의의 **핵심 섹션**. Type B (roadmap/supply alignment)에서 가장 중요한 언어.

### 타임라인 타겟 화법 (Timeline Targets)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 타겟 명시 | Qualcomm | "We are targeting up to like a three terabytes per second kind of bandwidth for HBF" | "targeting up to" - 상향 타겟 |
| 타임프레임 질의 | SK | "Which time frame?" | 짧은 타임라인 확인 |
| 타임프레임 답변 | Qualcomm | "This is around 29, 30 times" | "around 29, 30 times" - 대략 타임프레임 |
| 비교 대상 타임라인 매칭 | SK | "So when you show this slide, put the timeline, target timeline, and then pick the right HBM product and the capacity" | "put the timeline, target timeline" - 타임라인 매칭 요구 |
| 타겟 비율 명시 | Qualcomm | "Our goal is to keep like 50 percent" | "Our goal is to keep like X" - 비율 타겟 |
| 비교 시점 동기화 | SK | "So it's computer Apple to Apple at the same time, at the HBF and HBF" | "Apple to Apple at the same time" - 동시점 비교 요구 |

**Audrey 교훈**: 
- "We are targeting up to X" - 타겟 명시 공식. "up to"가 상향을 시사.
- "Apple to Apple at the same time" - 같은 시점, 같은 조건 비교 요구. Type B의 핵심 화법. "Apple to Apple"은 발표자료에 자주 쓰이지만, 회의에서는 "at the same time"을 붙여서 시점 동기화까지 요구해야.
- "Our goal is to keep like X percent" - 목표 비율 명시. "goal"이 "target"보다 더 확정적.

### 볼륨/샘플 요청 화법 (Volume/Sample Requests)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 샘플 요청 | SK | "asking for one samples asking like a pricing" | 샘플 + 가격 요청 |
| 우선순위 요청 | SK | "please, spend more energy on this" | "spend more energy" - 강한 우선순위 요청 |
| 정중 샘플 요청 | SK | "please consider the providing some a couple samples to us" | "please consider providing" - 정중 |
| early sample 관심 | SK | "Then will you be also interested in early early early yes" | "early early early" - 반복 강조 |
| 샘플 단계 구분 질문 | SK | "What is the difference between early yes and CS?" | ES vs CS 단계 구분 |
| 샘플 수급 | Qualcomm | "Sure I will take the other samples and then the SDI subject event" | "I will take" - 수급 수락 |

### 스펙 pushback 화법 (Spec Pushback)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 비교 기준 요구 | SK | "we are seriously compare Apple to Apple, the target 29 or 20, 30 time. So I need you guys put the more target KPI" | "Apple to Apple" + "I need you guys put" |
| 발표용 vs 실용 구분 | SK | "this table is good for the publications. But we are seriously compare Apple to Apple" | "for the publications" - 발표용 비판 |
| 정확 수치 요구 | SK | "we do need some precise, more accurate numbers actually" | "do need precise" - 강조 |
| 비교 대상 상향 제안 | SK | "Best candidate is to compare with HBM 5... Then maybe you should compare with HBM 6. Then your target KPI target should be higher" | "best candidate" + "should be higher" |
| 스펙 포함 범위 도전 | SK | "Is it including the software latency? The formula latency?" | 스펙 비교 기준 도전 |

### 마일스톤 조정 화법 (Milestone Coordination)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| ES/CS 타임라인 | Qualcomm | "We have early E.S. in August timeframe the E.S. in December and C.S. will be in the next year February" | ES Aug → ES Dec → CS Feb - 3단계 마일스톤 |
| 샘플 양측 합의 | Qualcomm | "So when you are yes is available please consider the providing some a couple samples to us" - SK: "Sure" | 샘플 스케줄 양측 합의 |
| 제너레이션 전환 | Qualcomm | "Gen one is PCI Gen 4... Chen 2 and TDR 5... Gen 3 will be TDR 6 or Chen 5? It would be DDR 5" | 제너레이션별 스펙 명시 |
| 얼라인먼트 확인 | SK | "So the schedule is aligned to the other you are you are X. XL. Yeah. Gen to see" | "schedule is aligned" - 스케줄 얼라인먼트 |
| 후속 미팅 제안 | SK | "Maybe we can target follow-up meeting and we'll get more information on KPI" | "target follow-up meeting" - 후속 미팅 제안 |

**Audrey 교훈**: 
- "Early ES in August timeframe, the ES in December, and CS will be in the next year February" - 샘플 단계를 3개로 나눠 명시. Type B의 핵심 - "early ES → ES → CS" 3단계 스케줄. 각 단계마다 월을 명시.
- "Schedule is aligned to X" - 얼라인먼트 확인 공식. "맞춰졌습니까?"의 영어 버전이 "schedule is aligned to X"다.
- "Target follow-up meeting" - 후속 미팅을 "target" 동사로 제안. "let's meet again"보다 "target follow-up meeting"이 더 전문적.

### "Aligned with" / "Under consideration" 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 얼라인먼트 명시 | SK | "So the schedule is aligned to the other you are you are X. XL" | "aligned to" - 스케줄 얼라인먼트 |
| 검토 중 표현 | Qualcomm | "We are also evaluating other like Marvell and other controller vendor as well" | "evaluating" - 검토 중 |
| 파트너십 명시 | Qualcomm | "we are looking for partner" | "looking for partner" - 파트너십 요청 |
| 워크스페이스 검토 | Qualcomm | "we have done like some huge cases 3D as well. We can also go through that" | "we can also go through that" - 검토 가능 |

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| KPI 공유 약속 | Qualcomm | "We shall Me at the home for if you have any questions" | "We shall" - 약속 |
| 후속 미팅 약속 | SK | "Maybe we can target follow-up meeting and we'll get more information on KPI" | "target follow-up meeting" |
| 정기 미팅 제안 | Qualcomm | "we are doing a periodic, we have like a monthly, a bi-weekly meetings to explore" | "monthly, bi-weekly meetings" - 정기 미팅 |
| 추가 논의 제안 | Qualcomm | "Then we can also talk if you want like further" | "if you want like further" - 추가 논의 제안 |
| 준비 부족 인정 | Qualcomm | "I didn't prepare that detail because detail is like a lot more. It should bring the details. Details again" | "It should bring the details" - 다음에 준비 약속 |

**Audrey 교훈**: 
- "Target follow-up meeting" - 후속 미팅을 "target" 동사로 제안. 회의 끝에 "다음에 또 봅시다"를 "let's target a follow-up meeting"으로 표현.
- "Monthly, bi-weekly meetings" - 정기 미팅 주기를 명시. "let's meet regularly"보다 "monthly or bi-weekly"가 구체적.
- "It should bring the details" - 준비 부족을 인정하면서 다음에 준비하겠다고 약속. "I'll prepare more"보다 "It should bring the details"이 더 책임감 있게 들린다.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 HBF/CXL/메모리 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **HBF** (High Bandwidth Flash) | HBM과 SSD 사이 포지션의 고대역폭 플래시 | "we call you like AI9, high bandwidth flash that is the HBF, which is like a very similar to HBM, but based on the NAND flash" - "like X, but based on Y" |
| **AI9** | Qualcomm의 AI 제품군 명 | "For our 9 devices like AI9 family" - "AI9 family"로 제품군 표현 |
| **SFC** (Single-Level Cell Flash) | 단일 레벨 셀 플래시 | "This is SFC. SFC, right? SFC." - 약어 확인 패턴 |
| **UCI** (Universal Chiplet Interconnect) | 칩렛 범용 인터페이스 | "the interface is like we are targeting current target is UCI" - "targeting X"로 인터페이스 타겟 |
| **base die** | HBF 패키지의 베이스 다이 | "the base die will have some buffering and then ping pong kind of buffer" - "ping pong kind of buffer"로 버퍼 설명 |
| **KV cache** | LLM 키-밸류 캐시 | "the first application we are thinking is like a CAS for KV cache" - "CAS for KV cache" |
| **CAS** (Cache-Attached Storage) | 캐시 부착 스토리지 | "CAS for KV cache" - use case 명시 |
| **CXL 2.x / 3.x / 4.0** | CXL 프로토콜 버전 | "CXL 2.x, memory expansion... CXL 3.0 and switch... CXL 4.0 sample" - 버전별 아키텍처 |
| **E3.S2T** | CXL 메모리 모듈 폼팩터 | "256 gigabytes same form factor E3.S2T" - 폼팩터 명시 |
| **MRDIM** | 고용량 MR-DIMM | "reduce the TCO without using expensive MRDIM kind of high capacity per server" - 비교 대상 |
| **XConn** | CXL 스위치 벤더 (Marvell 인수) | "XConn acquired by model? Yes, yeah, just last month" - 인수 정보 |
| **PCIe Gen 5/6/7** | PCIe 세대 | "Gen 5 5 and the Chen 2 and TDR 5... Gen 6 Chen 3 will be TDR 6" - 세대별 매핑 |
| **DDR5 / DDR6** | DRAM 표준 세대 | "Chen 3 will be TDR 6 or Chen 5? It would be DDR 5" - DRAM 세대 |
| **montage controller** | CXL 메모리 컨트롤러 | "we are again using same montage controller for this product" - 컨트롤러 벤더 |
| **ES / CS** (Engineering Sample / Customer Sample) | 엔지니어링 샘플 / 고객 샘플 | "early E.S. in August timeframe the E.S. in December and C.S. will be in the next year February" - 3단계 샘플 |
| **TCO** (Total Cost of Ownership) | 총소유비용 | "reduce the TCO without using expensive MRDIM" - 비용 절감 명시 |
| **TDI** (Through-Die Interface) | 다이 관통 인터페이스 | "TDI interface, do you think? No. That's like, yeah, because you're dropping contact" - TDI 논의 |
| **daisy chain** | 데이지 체인 연결 | "the daisy chain... It's directly connected" - 연결 방식 |
| **OCP** (Open Compute Project) | 오픈 컴퓨트 프로젝트 | "we did kickoff OCP and we started officially" - OCP 멤버십 |
| **AIC** (Add-In Card) | 확장 카드 폼팩터 | "Another type is AIC. So as you know, in USA, the big tech company is the people, the AIC, then E3" - 폼팩터 옵션 |
| **HBM4 / HBM5 / HBM6** | HBM 세대 | "Best candidate is to compare with HBM 5... should compare with HBM 6" - 비교 대상 세대 |
| **monoditensity** (monolithic density) | 단일 다이 밀도 | "HBM five will move on the around 48 gigabit monoditensity and the 16 high-stat" - 밀도 명시 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m21-001
  expression: "For a X, like the Y family, you have numerous Z"
  category: presentation_positioning
  function: product_layering
  speaker_role: presenter
  difficulty: 4
  context: "For our AI9 devices like AI9 family, you have numerous memory size"
  note: 제품 계층 구조로 발표 시작 - 로드맵 발표의开场

- id: m21-002
  expression: "Where in the middle, you can see it is we call X, which is like a very similar to Y, but based on Z"
  category: presentation_positioning
  function: similarity_difference
  speaker_role: presenter
  difficulty: 4
  context: "you can see it is we call you like AI9, high bandwidth flash that is the HBF, which is like a very similar to HBM, but based on the NAND flash"
  note: "like X, but based on Y" - 유사성+차이점으로 포지셔닝

- id: m21-003
  expression: "This is just a positioning point of view"
  category: scope_limiter
  function: context_qualification
  speaker_role: presenter
  difficulty: 3
  context: "This is just a positioning point of view"
  note: "point of view" - 발표자가 맥락 한정 명시

- id: m21-004
  expression: "If here is the comparison, like if you taking like X as a baseline, then Y is the Z"
  category: kpi_baseline
  function: comparison_setup
  speaker_role: presenter
  difficulty: 4
  context: "if you taking like HBM4 as a baseline, then 24 gigabit is the HBM4"

- id: m21-005
  expression: "We are promising at least NX like a Y for Z"
  category: kpi_promise
  function: spec_commitment
  speaker_role: presenter
  difficulty: 4
  context: "we are promising at least 10X like a 240 gigabit die for HBEF"

- id: m21-006
  expression: "Latency is like a X, which is like a Y times worse than Z"
  category: weakness_disclosure
  function: honest_spec
  speaker_role: presenter
  difficulty: 5
  context: "latency is like a five microsecond, which is like a 100 times worse than HBM"
  note: 단점 정직 수치화 - 신뢰構築

- id: m21-007
  expression: "The first application we are thinking is like a X for Y"
  category: use_case_hypothesis
  function: application_proposal
  speaker_role: presenter
  difficulty: 4
  context: "the first application we are thinking is like a CAS for KV cache"
  note: "we are thinking" - 가설 제시

- id: m21-008
  expression: "We have to find the right match"
  category: use_case_matching
  function: workload_device_match
  speaker_role: presenter
  difficulty: 3
  context: "We have to find the right match"

- id: m21-009
  expression: "If workload is not matching with the device, the statistics, then it's not usable"
  category: precondition
  function: matching_prerequisite
  speaker_role: presenter
  difficulty: 4
  context: "If workload is not matching with the device, the statistics, then it's not usable"

- id: m21-010
  expression: "Case one where there's a hybrid? Today you have... Say for example, you have 8 HBM instead of that can be used like a 6 plus 2 or 7 plus 1"
  category: architecture_option
  function: option_enumeration
  speaker_role: presenter
  difficulty: 5
  context: "can we have a case one where there's a hybrid? Today you have... Say for example, you have 8 HBM instead of that can be used like a 6 plus 2 or 7 plus 1"
  note: 구체 수치로 옵션 제시 - Type B 핵심

- id: m21-011
  expression: "And we don't know the answer. That's why we're saying like we are going to like trying to explore"
  category: uncertainty_acknowledgment
  function: exploration_framing
  speaker_role: presenter
  difficulty: 4
  context: "And we don't know the answer. That's why we're saying like we are going to like trying to explore which would be right huge case"

# ── 회피·포장 (Hedging & Deflection) ──
- id: m21-012
  expression: "This is like everything is in flux"
  category: flux_framing
  function: uncertainty_polite
  speaker_role: presenter
  difficulty: 4
  context: "because this is like everything is in fluid"
  note: "in flux" - 로드맵 협의 핵심 회피 단어. "We don't know" 대신 사용

- id: m21-013
  expression: "There is some X, but this still is in flux, but at high level"
  category: flux_with_approximation
  function: qualified_uncertainty
  speaker_role: presenter
  difficulty: 5
  context: "there is some timeframe, but this still is in flux, but at high level, KPI point of view"

- id: m21-014
  expression: "We don't have answer of every question. That's why we are looking for partner"
  category: knowledge_gap_acknowledgment
  function: partnership_request
  speaker_role: presenter
  difficulty: 5
  context: "For that one, we don't have answer of every question... That's why we are looking for partner"
  note: 모르는 것 인정 + 파트너십 요청 전환

- id: m21-015
  expression: "That is still under works right now"
  category: in_progress
  function: ongoing_status
  speaker_role: presenter
  difficulty: 3
  context: "Yeah, that is still under works right now"

- id: m21-016
  expression: "This is a chicken and chicken. You still have chicken and chicken"
  category: circular_dependency
  function: dependency_metaphor
  speaker_role: presenter
  difficulty: 4
  context: "This is a chicken and chicken. You still have chicken and chicken"
  note: "chicken and egg" 변형 - 순환 의존성 비유

- id: m21-017
  expression: "So far we have able to identify that any other use case it is very hard to compliment HBM"
  category: limitation_acknowledgment
  function: scope_reality
  speaker_role: presenter
  difficulty: 4
  context: "so far we have able to identify that any other use case it is very hard to compliment HBM"

- id: m21-018
  expression: "This has to be not a cookie cutter. It has to be a little custom because otherwise you cannot make it"
  category: custom_requirement
  function: non_standard_framing
  speaker_role: presenter
  difficulty: 4
  context: "This has to be not a cookie cutter. It has to be a little custom because otherwise you cannot make it"
  note: "cookie cutter" - 표준품 부정 + 커스텀 필요성

# ── 정중한 도전 (Polite Challenge) ──
- id: m21-019
  expression: "Which time frame?"
  category: timeline_probe
  function: direct_timeline_check
  speaker_role: questioner
  difficulty: 2
  context: "Which time frame?"
  note: 두 단어 타임라인 확인 - 전문가 화법

- id: m21-020
  expression: "But this table is good for the publications. But we are seriously compare Apple to Apple"
  category: spec_pushback
  function: presentation_vs_real_comparison
  speaker_role: questioner
  difficulty: 5
  context: "But this table is good for the publications. But we are seriously compare Apple to Apple, the target 29 or 20, 30 time"
  note: "for the publications" - 발표용 비판. Type B 핵심

- id: m21-021
  expression: "We are seriously compare Apple to Apple, the target X time. So I need you guys put the more target KPI"
  category: kpi_demand
  function: strong_request
  speaker_role: questioner
  difficulty: 5
  context: "we are seriously compare Apple to Apple, the target 29 or 20, 30 time. So I need you guys put the more target KPI"

- id: m21-022
  expression: "We do need some precise, more accurate numbers actually"
  category: precision_demand
  function: exactness_request
  speaker_role: questioner
  difficulty: 4
  context: "we do need some precise, more accurate numbers actually"
  note: "do need" - 강조

- id: m21-023
  expression: "Is it including the software latency? The formula latency?"
  category: spec_scope_probe
  function: comparison_basis_check
  speaker_role: questioner
  difficulty: 4
  context: "Is it including the software latency? The formula latency? Yeah. Is it?"

- id: m21-024
  expression: "And the pitch means you have to have the KPI numbers. Right?"
  category: requirement_assertion
  function: kpi_prerequisite
  speaker_role: questioner
  difficulty: 4
  context: "And the pitch means you have to have the KPI numbers. Right?"
  note: "Right?"로 압박

- id: m21-025
  expression: "Best candidate is to compare with X"
  category: comparison_suggestion
  function: baseline_proposal
  speaker_role: questioner
  difficulty: 4
  context: "Best candidate is to compare with HBM 5. If you based on the current and your progress"

- id: m21-026
  expression: "Then maybe you should compare with X. Then your target KPI target should be higher"
  category: baseline_pushback
  function: upward_adjustment
  speaker_role: questioner
  difficulty: 5
  context: "Then maybe if you twill it you should compare with HBM 6. Then your target KPI target should be higher"

- id: m21-027
  expression: "Why use that connection? I don't understand"
  category: architecture_challenge
  function: direct_question
  speaker_role: questioner
  difficulty: 3
  context: "Why use that connection? I don't understand"

- id: m21-028
  expression: "Could you please explain about the X"
  category: polite_request
  function: explanation_ask
  speaker_role: questioner
  difficulty: 3
  context: "Could you please explain about the you all kinds of experience of developing or the manufacturing of the software CPU?"

- id: m21-029
  expression: "I wonder, I want to the recent you all, the specific plan for X"
  category: curiosity_expression
  function: plan_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "I wonder, I want to the recent you all, the specific plan for the CXL, the CPU product"

- id: m21-030
  expression: "As you know, there are two kinds of X types. Another type is Y"
  category: expert_preface
  function: knowledge_display
  speaker_role: questioner
  difficulty: 4
  context: "as you know, there are two kinds of CSR types. Another type is AIC"
  note: "as you know" - 전문가 전제

# ── 협상·액션 (Negotiation) ──
- id: m21-031
  expression: "We are targeting up to like a X for Y"
  category: target_stating
  function: timeline_target
  speaker_role: presenter
  difficulty: 3
  context: "We are targeting up to like a three terabytes per second kind of bandwidth for HBF"

- id: m21-032
  expression: "This is around X, Y times"
  category: timeframe_approximate
  function: timeline_estimate
  speaker_role: presenter
  difficulty: 3
  context: "This is around 29, 30 times"

- id: m21-033
  expression: "Our goal is to keep like X percent"
  category: ratio_target
  function: goal_ratio
  speaker_role: presenter
  difficulty: 3
  context: "Our goal is to keep like 50 percent"

- id: m21-034
  expression: "So it's computer Apple to Apple at the same time, at the X and Y"
  category: synchronized_comparison
  function: same_time_comparison
  speaker_role: questioner
  difficulty: 5
  context: "So it's computer Apple to Apple at the same time, at the HBF and HBF"
  note: "at the same time" - 동시점 비교 요구

- id: m21-035
  expression: "So when you show this slide, put the timeline, target timeline, and then pick the right X product and the capacity"
  category: timeline_matching_request
  function: timeline_alignment
  speaker_role: questioner
  difficulty: 4
  context: "So when you show this slide, put the timeline, target timeline, and then pick the right HBM product and the capacity"

- id: m21-036
  expression: "Please consider the providing some a couple samples to us"
  category: sample_request
  function: polite_sample_ask
  speaker_role: questioner
  difficulty: 4
  context: "So when you are yes is available please consider the providing some a couple samples to us"
  note: "please consider providing" - 정중 샘플 요청

- id: m21-037
  expression: "Please, spend more energy on this"
  category: priority_demand
  function: urgency_request
  speaker_role: questioner
  difficulty: 4
  context: "please, spend more energy on this"
  note: "spend more energy" - 강한 우선순위 요청

- id: m21-038
  expression: "Then will you be also interested in early early early yes"
  category: early_sample_interest
  function: early_access_request
  speaker_role: questioner
  difficulty: 3
  context: "Then will you be also interested in early early early yes"
  note: "early early early" - 반복 강조

- id: m21-039
  expression: "We have early E.S. in X timeframe the E.S. in Y and C.S. will be in the next year Z"
  category: sample_milestone
  function: three_stage_schedule
  speaker_role: presenter
  difficulty: 4
  context: "We have early E.S. in August timeframe the E.S. in December and C.S. will be in the next year February"
  note: ES→ES→CS 3단계 마일스톤. Type B 핵심

- id: m21-040
  expression: "So the schedule is aligned to the X"
  category: schedule_alignment
  function: alignment_confirmation
  speaker_role: questioner
  difficulty: 4
  context: "So the schedule is aligned to the other you are you are X. XL"
  note: "aligned to" - 스케줄 얼라인먼트

- id: m21-041
  expression: "Maybe we can target follow-up meeting and we'll get more information on KPI"
  category: follow_up_meeting
  function: next_meeting_proposal
  speaker_role: questioner
  difficulty: 3
  context: "Maybe we can target follow-up meeting and we'll get more information on KPI"
  note: "target follow-up meeting" - 후속 미팅 제안

- id: m21-042
  expression: "We are doing a periodic, we have like a monthly, a bi-weekly meetings to explore"
  category: regular_meeting
  function: cadence_proposal
  speaker_role: presenter
  difficulty: 3
  context: "we are doing a periodic, we have like a monthly, a bi-weekly meetings to explore"

- id: m21-043
  expression: "Then we can also talk if you want like further"
  category: further_discussion
  function: open_continuation
  speaker_role: presenter
  difficulty: 3
  context: "Then we can also talk if you want like further"

- id: m21-044
  expression: "We are also evaluating other like X and other Y vendor as well"
  category: vendor_evaluation
  function: consideration_stating
  speaker_role: presenter
  difficulty: 3
  context: "we are also evaluating other like Marvell and other controller vendor as well"

- id: m21-045
  expression: "It should bring the details. Details again"
  category: preparation_promise
  function: next_prep_commitment
  speaker_role: presenter
  difficulty: 3
  context: "I didn't prepare that detail because detail is like a lot more. It should bring the details. Details again"

# ── 발화 채움 표현 (Discourse Markers in Use) ──
- id: m21-046
  expression: "We can always entertain more"
  category: open_membership
  function: welcoming
  speaker_role: presenter
  difficulty: 3
  context: "we can, we can, we can always entertain more"
  note: 멤버십/참여 환영

- id: m21-047
  expression: "That's good feedback"
  category: feedback_acknowledgment
  function: acceptance
  speaker_role: presenter
  difficulty: 2
  context: "That's good feedback"

- id: m21-048
  expression: "Let's move on"
  category: transition
  function: topic_shift
  speaker_role: presenter
  difficulty: 2
  context: "Let's move on"

- id: m21-049
  expression: "Sorry for the delay"
  category: apology
  function: delay_acknowledgment
  speaker_role: presenter
  difficulty: 2
  context: "Sorry for the delay"

- id: m21-050
  expression: "Anything else? It's people"
  category: open_check
  function: question_invitation
  speaker_role: presenter
  difficulty: 2
  context: "Anything else? Anything else? It's people"

- id: m21-051
  expression: "I think the content is absolutely excellent"
  category: compliment
  function: positive_feedback
  speaker_role: questioner
  difficulty: 2
  context: "I think the content is absolutely excellent"

- id: m21-052
  expression: "Thank you to team Korea"
  category: closing
  function: meeting_close
  speaker_role: presenter
  difficulty: 2
  context: "Thank you to team Korea"
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-02-27 10 59 44_EN_Qualcomm-extracted.wav` (총 ~60분, 7,246단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입·포지셔닝 (line 118-131) | AI9 제품군 + HBF 포지셔닝 "like HBM, but based on NAND flash" | 제품 포지셔닝 공식 | ★★☆ |
| 2 | KPI 테이블 (line 156-167) | "promising at least 10X" + "100 times worse than HBM" + "targeting 200K endurance" | KPI 명시 + 단점 정직 수치화 | ★★★ |
| 3 | use case 탐색 (line 230-260) | "first application we are thinking is CAS for KV cache" + "find the right match" | use case 가설 + 매칭 강조 | ★★★ |
| 4 | 스펙 pushback (line 643-670) | "this table is good for the publications" + "Apple to Apple" + "I need you guys put the more target KPI" | 스펙 pushback + 비교 기준 도전 | ★★★★ |
| 5 | 샘플 스케줄 (line 628-660) | "early ES in August, ES in December, CS in February" + "please consider providing a couple samples" | 3단계 마일스톤 + 샘플 요청 | ★★★★ |

**사용법**: 
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 4, 5가 가장 가치 높음 - 스펙 pushback + 샘플 스케줄이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **roadmap pitch + spec negotiation + sample coordination** register다. 발표자가 로드맵을 피칭하고, 상대가 스펙을 도전하고, 샘플 스케줄을 조율하는 구조. Type B의 전형. 두 역할 모두 학습해야:
- **발표자 역할 (Qualcomm)**: 로드맵 포지셔닝, KPI 명시, 미확정 회피, use case 탐색 - 네가 로드맵을 맞출 때
- **질문자 역할 (SK)**: 타임라인 정밀, 스펙 pushback, 샘플 요청, 비교 기준 제안 - 네가 파트너 로드맵을 평가할 때

### Pragmatics (화용론) 핵심
1. **"In flux"의 회피**: 로드맵 협의에서 "모른다"를 "in flux"로 포장. "We don't know"가 아니라 "this is in flux" - "유동적이다"로 정중하게. 한국어 "아직 논의 중입니다"의 영어 버전. 그리고 "but at high level"로 대략값을 주면 더 정중.
2. **"Apple to Apple"의 비교 요구**: 스펙 pushback의 핵심. "이 테이블은 발표용이지만, 우리는 Apple to Apple로 비교해야 합니다" - 발표자료와 실제 협상용 수치를 구분. "at the same time"을 붙여서 동시점 비교까지 요구.
3. **"Chicken and egg"의 순환 의존성**: KPI와 use case가 서로 물려 있을 때, "chicken and egg"로 포장. "어떤 걸 먼저 정해야 할지 모른다"를 비유로.
4. **"Please consider providing"의 샘플 요청**: "give us samples"가 아니라 "please consider providing a couple samples to us" - 정중한 샘플 요청. Type B의 핵심 화법.
5. **"Target follow-up meeting"의 후속 제안**: 회의 끝에 "다음에 또 봅시다"를 "let's target a follow-up meeting"으로. "let's meet again"보다 "target" 동사가 더 전문적.

### 네가 당장 써야 할 Top 5
1. **"This is in flux, but at high level"** - 미확정 회피
2. **"We are seriously compare Apple to Apple. So I need you guys put the more target KPI"** - 스펙 pushback
3. **"Please consider providing some a couple samples to us"** - 정중 샘플 요청
4. **"We have early ES in X, ES in Y, and CS in Z"** - 3단계 마일스톤
5. **"Maybe we can target follow-up meeting"** - 후속 미팅 제안

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "아직 논의 중입니다" | "This is in flux, but at high level" | "in flux"로 유동성 표시 + 대략값 |
| "발표용이지 실제와 다릅니다" | "this table is good for the publications. But we are seriously compare Apple to Apple" | "for the publications" - 직접적 비판 |
| "수치를 더 주셔야 합니다" | "I need you guys put the more target KPI" | "I need you guys put" - 강한 요구 |
| "샘플 좀 주세요" | "please consider providing some a couple samples to us" | "please consider providing" - 정중 |
| "다음에 또 봅시다" | "Maybe we can target follow-up meeting" | "target follow-up meeting" - 전문적 |
| "검토 중입니다" | "We are also evaluating other like X" | "evaluating" - 검토 중 |
| "스케줄 맞춰주세요" | "So the schedule is aligned to the X" | "aligned to" - 얼라인먼트 |
| "비교 대상이 뭐가 됩니까" | "Best candidate is to compare with X" | "best candidate" - 제안형 |
| "순환 의존성이 있습니다" | "This is a chicken and chicken" | "chicken and egg" 비유 |
| "커스텀 필요합니다" | "This has to be not a cookie cutter. It has to be a little custom" | "cookie cutter" 부정 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 4절 협상 화법·2절 회피 화법을 중심으로 dump 작성
4. **비교 학습**: 9절 한국어-영어 비교표로 화법 차이 체득
5. **Type B 특화**: 이 회의는 roadmap/supply alignment의 교본 - 스펙 pushback, 샘플 요청, 마일스톤 조정, "aligned with" 언어를 집중 학습

---

*Textbook 21 - Qualcomm HBF/CXL Roadmap Alignment (2026-02-27). 회의 유형 B (roadmap/supply alignment). 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-01.*
