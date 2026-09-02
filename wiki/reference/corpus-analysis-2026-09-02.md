# WebEx 회의 코퍼스 분석 — 영어 학습 커리큘럼 설계용

> 생성: 2026-09-02 17:18 | 분석 대상: EN 전사본 37개 (rag-corrected)
> 목적: 40회의 전사 코퍼스에서 대화 패턴을 추출해 학습 소재로 전환

---

## 1. 코퍼스 인구조사

전체 EN 회의: **37개**, 기간: 2025-05-12 ~ 2026-08-25

| # | 날짜 | 시간 | 파트너(제목) | 단어수 | 문장수 |
|:-:|:--|:--|:--|--:|--:|
| 1 | 2025-05-12 | 09:49 | AMD_Roadmap | 5,902 | 537 |
| 2 | 2025-06-10 | 08:36 | Google | 2,772 | 219 |
| 3 | 2025-07-16 | 08:21 | LenovoUSQTR | 2,830 | 334 |
| 4 | 2025-07-23 | 08:29 | AMDCXLsync | 3,712 | 304 |
| 5 | 2025-08-21 | 08:19 | Intel | 5,409 | 586 |
| 6 | 2025-09-04 | 08:32 | Intel | 3,355 | 376 |
| 7 | 2025-11-05 | 09:10 | AMD | 3,294 | 291 |
| 8 | 2025-12-05 | 09:18 | INTEL | 5,226 | 33 |
| 9 | 2026-01-07 | 09:04 | AMDbiweekly | 7,034 | 304 |
| 10 | 2026-01-22 | 09:02 | Intel | 3,101 | 372 |
| 11 | 2026-01-28 | 10:26 | Lenovo(CN)weekly | 2,807 | 465 |
| 12 | 2026-02-04 | 10:02 | Montage_switchless | 5,943 | 658 |
| 13 | 2026-02-06 | 07:59 | IBM meeting | 7,694 | 585 |
| 14 | 2026-02-10 | 09:04 | AWSF2FQTR_Q12026 | 14,924 | 1706 |
| 15 | 2026-02-10 | 09:09 | AWS | 7,425 | 177 |
| 16 | 2026-02-12 | 09:34 | HPE_QTR_Q1 | 10,300 | 931 |
| 17 | 2026-02-27 | 10:59 | Qualcomm | 7,109 | 828 |
| 18 | 2026-03-12 | 08:35 | MSFTQTR | 3,122 | 261 |
| 19 | 2026-03-12 | 09:07 | MSFT | 1,638 | 143 |
| 20 | 2026-04-22 | 08:06 | AMD | 3,632 | 410 |
| 21 | 2026-04-27 | 10:01 | Qualcomm_Morning1 | 4,236 | 334 |
| 22 | 2026-04-27 | 11:04 | Qualcomm_Morning2 | 10,844 | 1105 |
| 23 | 2026-04-27 | 13:51 | Qualcomm_1H | 2,470 | 209 |
| 24 | 2026-04-27 | 15:56 | Qualcomm_2H | 8,757 | 1017 |
| 25 | 2026-04-29 | 08:52 | Liqid_biweekly | 4,477 | 470 |
| 26 | 2026-05-13 | 08:57 | Liqid_biweekly | 4,693 | 489 |
| 27 | 2026-05-27 | 09:02 | Liqid | 2,531 | 2 |
| 28 | 2026-05-27 | 10:02 | DELL_TDF | 4,928 | 402 |
| 29 | 2026-06-09 | 09:13 | Penguin | 3,485 | 355 |
| 30 | 2026-06-10 | 09:03 | Liqid | 3,507 | 74 |
| 31 | 2026-07-09 | 09:02 | MSFT_CXLpoolingDiscussion | 10,759 | 2 |
| 32 | 2026-08-13 | 09:01 | NVIDIA_Morning | 9,462 | 1014 |
| 33 | 2026-08-13 | 11:03 | NVIDIA_1H | 4,614 | 403 |
| 34 | 2026-08-13 | 15:38 | NVIDIA_2H | 10,090 | 1048 |
| 35 | 2026-08-18 | 09:01 | Marvell | 3,083 | 249 |
| 36 | 2026-08-19 | 09:08 | Scaleflux | 4,365 | 476 |
| 37 | 2026-08-25 | 08:00 | Marvell | 6,844 | 597 |

**코퍼스 총 단어 수**: 206,374 (≈ 412 페이지 분량)

---

## 2. 언어특성

TTR(Type-Token Ratio) = 어휘 다양성 (높으면 다양한 어휘, 낮으면 반복 많음). avg_sent = 평균 문장 길이. discourse = 대화 표식(you know, let me 등) 빈도.

| 파트너 | 날짜 | 단어 | TTR | 고유어 | 평균문장길이 | 대화표식 |
|:--|:--|--:|:--:|--:|:--:|--:|
| AMD_Roadmap | 2025-05-12 | 5,902 | 0.156 | 921 | 11.0 | 69 |
| Google | 2025-06-10 | 2,772 | 0.214 | 594 | 12.7 | 24 |
| LenovoUSQTR | 2025-07-16 | 2,830 | 0.247 | 700 | 8.5 | 16 |
| AMDCXLsync | 2025-07-23 | 3,712 | 0.198 | 734 | 12.2 | 33 |
| Intel | 2025-08-21 | 5,409 | 0.155 | 837 | 9.2 | 80 |
| Intel | 2025-09-04 | 3,355 | 0.218 | 733 | 8.9 | 36 |
| AMD | 2025-11-05 | 3,294 | 0.211 | 696 | 11.3 | 35 |
| INTEL | 2025-12-05 | 5,226 | 0.15 | 785 | 158.4 | 67 |
| AMDbiweekly | 2026-01-07 | 7,034 | 0.142 | 1000 | 23.1 | 103 |
| Intel | 2026-01-22 | 3,101 | 0.204 | 633 | 8.3 | 48 |
| Lenovo(CN)weekly | 2026-01-28 | 2,807 | 0.186 | 523 | 6.0 | 16 |
| Montage_switchless | 2026-02-04 | 5,943 | 0.148 | 877 | 9.0 | 92 |
| IBM meeting | 2026-02-06 | 7,694 | 0.153 | 1176 | 13.2 | 105 |
| AWSF2FQTR_Q12026 | 2026-02-10 | 14,924 | 0.111 | 1657 | 8.7 | 138 |
| AWS | 2026-02-10 | 7,425 | 0.156 | 1161 | 41.9 | 110 |
| HPE_QTR_Q1 | 2026-02-12 | 10,300 | 0.142 | 1463 | 11.1 | 86 |
| Qualcomm | 2026-02-27 | 7,109 | 0.151 | 1074 | 8.6 | 50 |
| MSFTQTR | 2026-03-12 | 3,122 | 0.245 | 765 | 12.0 | 54 |
| MSFT | 2026-03-12 | 1,638 | 0.308 | 504 | 11.5 | 33 |
| AMD | 2026-04-22 | 3,632 | 0.188 | 684 | 8.9 | 70 |
| Qualcomm_Morning1 | 2026-04-27 | 4,236 | 0.216 | 916 | 12.7 | 31 |
| Qualcomm_Morning2 | 2026-04-27 | 10,844 | 0.131 | 1423 | 9.8 | 138 |
| Qualcomm_1H | 2026-04-27 | 2,470 | 0.231 | 570 | 11.8 | 55 |
| Qualcomm_2H | 2026-04-27 | 8,757 | 0.145 | 1274 | 8.6 | 132 |
| Liqid_biweekly | 2026-04-29 | 4,477 | 0.201 | 900 | 9.5 | 26 |
| Liqid_biweekly | 2026-05-13 | 4,693 | 0.184 | 865 | 9.6 | 28 |
| Liqid | 2026-05-27 | 2,531 | 0.188 | 477 | 1265.5 | 8 |
| DELL_TDF | 2026-05-27 | 4,928 | 0.194 | 954 | 12.3 | 44 |
| Penguin | 2026-06-09 | 3,485 | 0.203 | 706 | 9.8 | 48 |
| Liqid | 2026-06-10 | 3,507 | 0.188 | 659 | 47.4 | 20 |
| MSFT_CXLpoolingDiscussion | 2026-07-09 | 10,759 | 0.119 | 1280 | 5379.5 | 277 |
| NVIDIA_Morning | 2026-08-13 | 9,462 | 0.142 | 1340 | 9.3 | 91 |
| NVIDIA_1H | 2026-08-13 | 4,614 | 0.186 | 859 | 11.4 | 45 |
| NVIDIA_2H | 2026-08-13 | 10,090 | 0.165 | 1660 | 9.6 | 144 |
| Marvell | 2026-08-18 | 3,083 | 0.181 | 558 | 12.4 | 73 |
| Scaleflux | 2026-08-19 | 4,365 | 0.161 | 703 | 9.2 | 48 |
| Marvell | 2026-08-25 | 6,844 | 0.15 | 1027 | 11.5 | 38 |

**평균 TTR**: 0.180 | **평균 대화표식**: 67.9/회의

---

## 3. 회의 유형 클러스터링 (TF-IDF + k-means, k=4)

### 군집 1 (2개 회의)

- 2025-12-05 INTEL
- 2026-01-22 Intel

**특징적 3-gram (군집 평균 TF-IDF)**:

- `flat to a` (0.007)
- `the miss rate` (0.006)
- `the gpu card` (0.004)
- `the volume validation` (0.004)
- `miss rate is` (0.004)
- `the last deck` (0.004)
- `get you some` (0.004)
- `you some answers` (0.004)
- `power on window` (0.003)
- `what kind of` (0.003)
- `and i'd like` (0.003)
- `to a limb` (0.003)
- `the gpu team` (0.003)
- `i don't recall` (0.003)
- `in the last` (0.003)

### 군집 2 (3개 회의)

- 2025-05-12 AMD_Roadmap
- 2026-02-10 AWSF2FQTR_Q12026
- 2026-03-12 MSFT

**특징적 3-gram (군집 평균 TF-IDF)**:

- `you guys are` (0.007)
- `the ddr uea` (0.007)
- `haven't seen any` (0.006)
- `seen any cxl` (0.006)
- `i haven't seen` (0.006)
- `for you guys` (0.006)
- `all of our` (0.005)
- `cxl cmm bdr` (0.005)
- `quick question about` (0.005)
- `be going over` (0.005)
- `going over the` (0.005)
- `building block and` (0.005)
- `block and pi` (0.005)
- `you know ev` (0.005)
- `exit pv exit` (0.005)

### 군집 3 (5개 회의)

- 2026-01-28 Lenovo(CN)weekly
- 2026-04-27 Qualcomm_2H
- 2026-08-13 NVIDIA_Morning
- 2026-08-13 NVIDIA_1H
- 2026-08-13 NVIDIA_2H

**특징적 3-gram (군집 평균 TF-IDF)**:

- `yeah yeah yeah` (0.025)
- `okay okay okay` (0.014)
- `sorry sorry sorry` (0.010)
- `the revision bb` (0.007)
- `in the office` (0.007)
- `will talk with` (0.006)
- `we will define` (0.006)
- `we're going to` (0.006)
- `are going to` (0.005)
- `we are going` (0.005)
- `revision bb schedule` (0.005)
- `our revision bb` (0.005)
- `do it we're` (0.005)
- `it we're going` (0.005)
- `hours of time` (0.005)

### 군집 4 (27개 회의)

- 2025-06-10 Google
- 2025-07-16 LenovoUSQTR
- 2025-07-23 AMDCXLsync
- 2025-08-21 Intel
- 2025-09-04 Intel
- 2025-11-05 AMD
- 2026-01-07 AMDbiweekly
- 2026-02-04 Montage_switchless
- 2026-02-06 IBM meeting
- 2026-02-10 AWS
- 2026-02-12 HPE_QTR_Q1
- 2026-02-27 Qualcomm
- 2026-03-12 MSFTQTR
- 2026-04-22 AMD
- 2026-04-27 Qualcomm_Morning1
- 2026-04-27 Qualcomm_Morning2
- 2026-04-27 Qualcomm_1H
- 2026-04-29 Liqid_biweekly
- 2026-05-13 Liqid_biweekly
- 2026-05-27 Liqid
- 2026-05-27 DELL_TDF
- 2026-06-09 Penguin
- 2026-06-10 Liqid
- 2026-07-09 MSFT_CXLpoolingDiscussion
- 2026-08-18 Marvell
- 2026-08-19 Scaleflux
- 2026-08-25 Marvell

**특징적 3-gram (군집 평균 TF-IDF)**:

- `i think that` (0.026)
- `thank you thank` (0.018)
- `you thank you` (0.018)
- `yes yes yes` (0.013)
- `think that the` (0.012)
- `yeah yeah yeah` (0.012)
- `share the screen` (0.011)
- `the kv cache` (0.010)
- `that the i` (0.010)
- `the editing card` (0.010)
- `i mean we` (0.010)
- `as i mentioned` (0.009)
- `side by side` (0.009)
- `mean we can` (0.009)
- `share share share` (0.009)

### 코퍼스 전체 고빈도 3-gram (반복 뼈대 — 모든 회의에 등장)

- `i think that` (170)
- `we need to` (168)
- `yeah yeah yeah` (158)
- `going to be` (157)
- `so i think` (122)
- `we want to` (118)
- `a lot of` (110)
- `i think we` (105)
- `we have to` (103)
- `are going to` (100)
- `do you have` (98)
- `we have a` (95)
- `i don't know` (94)
- `yeah i think` (92)
- `a little bit` (89)
- `you have any` (89)
- `think that the` (85)
- `you thank you` (85)
- `be able to` (84)
- `and then we` (84)
- `we're going to` (84)
- `i mean we` (83)
- `thank you thank` (83)
- `this is the` (81)
- `that we can` (80)

---

## 4. 기능 패턴 추출 (회의별)

| 파트너 | 날짜 | question | hedging | signal_open | negotiation | clarify_correct | agree_acknowledge |
|:--|:--|--:|--:|--:|--:|--:|--:|
| AMD_Roadmap | 2025-05-12 | 7 | 7 | 4 | 4 | 3 | 7 |
| Google | 2025-06-10 | 5 | 9 | 5 | 5 | 2 | 7 |
| LenovoUSQTR | 2025-07-16 | 10 | 7 | 5 | 2 | 2 | 3 |
| AMDCXLsync | 2025-07-23 | 7 | 9 | 5 | 2 | 3 | 7 |
| Intel | 2025-08-21 | 8 | 9 | 7 | 4 | 2 | 6 |
| Intel | 2025-09-04 | 5 | 7 | 3 | 3 | 2 | 8 |
| AMD | 2025-11-05 | 9 | 7 | 5 | 3 | 3 | 7 |
| INTEL | 2025-12-05 | 7 | 10 | 7 | 5 | 3 | 8 |
| AMDbiweekly | 2026-01-07 | 9 | 10 | 7 | 5 | 4 | 10 |
| Intel | 2026-01-22 | 6 | 6 | 6 | 1 | 3 | 5 |
| Lenovo(CN)weekly | 2026-01-28 | 5 | 5 | 3 | 3 | 2 | 4 |
| Montage_switchless | 2026-02-04 | 8 | 7 | 4 | 3 | 3 | 3 |
| IBM meeting | 2026-02-06 | 8 | 11 | 6 | 4 | 3 | 9 |
| AWSF2FQTR_Q12026 | 2026-02-10 | 10 | 12 | 8 | 7 | 4 | 9 |
| AWS | 2026-02-10 | 8 | 7 | 6 | 6 | 3 | 6 |
| HPE_QTR_Q1 | 2026-02-12 | 8 | 12 | 7 | 7 | 3 | 9 |
| Qualcomm | 2026-02-27 | 10 | 8 | 5 | 5 | 3 | 6 |
| MSFTQTR | 2026-03-12 | 5 | 8 | 4 | 2 | 2 | 4 |
| MSFT | 2026-03-12 | 3 | 4 | 3 | 1 | 1 | 4 |
| AMD | 2026-04-22 | 10 | 8 | 4 | 4 | 3 | 6 |
| Qualcomm_Morning1 | 2026-04-27 | 6 | 8 | 5 | 2 | 3 | 4 |
| Qualcomm_Morning2 | 2026-04-27 | 10 | 10 | 6 | 4 | 3 | 7 |
| Qualcomm_1H | 2026-04-27 | 4 | 7 | 4 | 2 | 2 | 5 |
| Qualcomm_2H | 2026-04-27 | 9 | 9 | 5 | 6 | 3 | 6 |
| Liqid_biweekly | 2026-04-29 | 8 | 9 | 4 | 5 | 3 | 9 |
| Liqid_biweekly | 2026-05-13 | 7 | 7 | 5 | 3 | 3 | 9 |
| Liqid | 2026-05-27 | 7 | 7 | 3 | 1 | 3 | 5 |
| DELL_TDF | 2026-05-27 | 8 | 11 | 5 | 5 | 3 | 7 |
| Penguin | 2026-06-09 | 5 | 10 | 2 | 2 | 3 | 5 |
| Liqid | 2026-06-10 | 8 | 5 | 6 | 4 | 4 | 8 |
| MSFT_CXLpoolingDiscussion | 2026-07-09 | 8 | 9 | 7 | 5 | 3 | 6 |
| NVIDIA_Morning | 2026-08-13 | 9 | 11 | 7 | 7 | 3 | 6 |
| NVIDIA_1H | 2026-08-13 | 4 | 5 | 6 | 6 | 2 | 4 |
| NVIDIA_2H | 2026-08-13 | 7 | 11 | 7 | 5 | 3 | 6 |
| Marvell | 2026-08-18 | 3 | 4 | 3 | 5 | 4 | 7 |
| Scaleflux | 2026-08-19 | 7 | 8 | 6 | 4 | 3 | 7 |
| Marvell | 2026-08-25 | 6 | 8 | 4 | 2 | 3 | 6 |

### 기능 패턴 예시 (가장 많이 쓴 회의별)

**question** — 대표: 2025-07-16 LenovoUSQTR

> What about density and speed
> How does the application system when the curate is releasing the CS
> Can you do the short introduction over there and then we can start it

**hedging** — 대표: 2026-02-10 AWSF2FQTR_Q12026

> So yeah, I think maybe if there's not too much trouble for you, why do we start off over again
> So as HBM product is going to evolve to a new product and the portion of new product will increase as well, I believe overall bit penalty fo
> So you said most of them are HBM and server, but it probably depends on the year and scope, right

**signal_open** — 대표: 2026-02-10 AWSF2FQTR_Q12026

> Okay, let me add comment here
> Then let's start to the meeting
> So why don't we have a short intro or while he's coming down if that's okay with you

**negotiation** — 대표: 2026-02-10 AWSF2FQTR_Q12026

> We need to think about, Hanix needs to think about how they are planning to support AWS, right
> Can you send us the email through the Carlio or someone else that we can promote with it
> Is it a function of how many products are actually lined up internally

**clarify_correct** — 대표: 2026-01-07 AMDbiweekly

> We put extra fans just to make sure that they don't get hot
> Uh, so At our last meeting, uh, I understand understood why the rating the gpu server is difficult in internal in the internal so I want to 
> Actually, there is no there I take it back and so auto new ma plus tpp patch Okay, I see I see okay Yeah, I just I'm expected that amd has t

**agree_acknowledge** — 대표: 2026-01-07 AMDbiweekly

> Let's get that details to the validation team and then come back to you with the our response that does this make sense does this not make s
> Yeah, we are from the summeRDIM Because we already delivered the The plasm the simulation model Yeah of the 512 gigabyte the same memory mod
> Uh, if you have anything any feedback In recent times because I think the feedback that I shared with you last time was the tiering makes se

---

## 5. 커리큘럼 매핑 (LLM 해석 영역)

> 이 섹션은 analyze_corpus.py 출력 후, LLM이 위 1~4단계 집계 + 40개 회의록 Summary를 읽고 채움.
> 분석일: 2026-09-02

### 5.1 의미 기반 회의 유형 분류 (40개 회의록 직독, 자동 클러스터링 교정)

자동 클러스터링(TF-IDF n-gram)은 Whisper 잔재/우발 n-gram에 묶여 의미 유형을 잡지 못함(27/5/3/2 쏠림). 40개 회의록 Summary를 직독하여 의미 기반으로 재분류:

| 유형 | 핵심 정의 | 회의 수 | 해당 회의 |
|:---|:---|:---:|:---|
| **A. 기술 Deep-dive** | 제품/아키텍처 깊이 설명·검증, 한쪽 발표 + Q&A | 14 | Marvell PFMA(8/25), Google, AMDCXLsync, Intel 8/21, Intel 9/4, Montage, IBM, Marvell 8/18, Scaleflux, Penguin, SoLab, MSFT_CXLpooling, DELL_TDF, Qualcomm HBF |
| **B. Roadmap/Supply 정합** | 양사 로드맵·일정·용량·속도 타겟 negotiation | 14 | AWS F2F, HPE QTR, MSFT QTR, MSFT, Qualcomm M1/M2/1H/2H, AMD Roadmap, LenovoUSQTR, NVIDIA Morning, NVIDIA 2H, AMDbiweekly 1/7, AMD 11/5, AMD 4/22 |
| **C. 샘플/일정 조율** | ES/CS/MP 샘플 수량·시점·pull-in 협의 | 8 | NVIDIA 1H, INTEL 12/5, Intel 1/22, Lenovo CN, WG_Clock, Liqid 5/27, Liqid 6/10, Liqid biweekly ×2 |
| **D. 이슈/품질 디버깅** | 버그·성능저하·품질지표 원인 분석 | 5 | Intel 1/22, MSFT UEA, AMD 4/22, AMDbiweekly, WG_Clock (C/A와 겹침) |
| ❌ 제외 | 내부 세미나 (영어 학습 대상 아님) | 1 | 미래포럼 (KR anyway) |

### 5.2 대화 패턴 뼈대 — 코퍼스 고빈도 3-gram 10개 (학습 코어)

이 10개 뼈대가 회의 언어의 구조적 다수를 차지. 725 일반 표현 DB를 대체하는 학습 소재 코어:

| 뼈대 | 빈도 | 기능 | 학습 우선순위 |
|:---|--:|:---|:---:|
| `i think that` | 170 | 의견 표명 | ★★★ |
| `we need to` | 168 | 요구·협상 | ★★★ |
| `going to be` | 157 | 미래 예측 | ★★★ |
| `so i think` | 122 | 의견 전환 | ★★☆ |
| `we want to` | 118 | 의사 표명 | ★★★ |
| `do you have` | 98 | 질문 | ★★★ |
| `i don't know` | 94 | 인지 부인·정중 양보 | ★★☆ |
| `yeah i think` | 92 | 동의+의견 | ★★☆ |
| `be able to` | 84 | 가능성 표현 | ★★☆ |
| `i mean we` | 83 | 정정·재표현 | ★★☆ |

### 5.3 유형별 학습 목표 분화

| 유형 | dominant 기능 패턴 | 학습 목표 표현군 | 드릴 타겟 |
|:---|:---|:---|:---|
| A. 기술 Deep-dive | signal_open, hedging | 설명·발표·따라잡기 | "Let me walk you through", "consists of", "to put it in perspective" |
| B. Roadmap 정합 | negotiation, question | 요구·협상·일정 | "We're targeting", "Can you support X by Y", "aligned with" |
| C. 샘플/일정 조율 | negotiation + clarify | 수량·시점·정정 | "ES in Q4, CS in Q1", "pull-in by N months", "we'd like to request" |
| D. 이슈 디버깅 | question + clarify | 문제 진단·원인 | "We found that", "root cause", "what's the issue" |

### 5.4 주간 사이클 (4유형 순환, 일반화 목적)

```
Week 1: A. 기술 Deep-dive (14개 회의 중 1) — 설명 언어
Week 2: B. Roadmap/Supply 정합 (14개 중 1) — negotiation 언어
Week 3: C. 샘플/일정 조율 (8개 중 1) — 실행 언어
Week 4: D. 이슈/품질 디버깅 (5개 중 1) — 진단 언어
Week 5: 다음 4개 회의로 순환
```

한 화체 고착화 방지 (Sweller 요소 상호작용 관리). 4주마다 4유형을 한 번씩 순회.

### 5.5 일일 20분 루틴 (유형별 회의 + 5구간 순회)

"이 주의 회의"를 5등분하여 월~금 각 다른 구간:
- 월: 0:00~1:00 / 화: 1:00~2:00 / ... 금: 4:00~5:00
- 같은 화체 안에서 다른 발화 패턴 노출

루틴 구조(이전 설계 유지, 인지부하 단계화):
1. Phonological loop 4분 — 소리만, 전사본 안 봄
2. Comprehension 4분 — 의미만, 전사본 보며 듣기
3. Integration 4분 — 통합 shadowing
4. Contrastive noticing 3분 — 내 녹음 vs 원본
5. Pragmatic drill 3분 — 유형별 상황 카드, 입으로
6. 기록 2분 — 발췌 인덱스 + "어디서 막혔나"

### 5.6 학습 소재 우선순위 (725 DB vs 코퍼스)

- **메인(80%)**: 코퍼스에서 추출한 유형별 패턴 + 고빈도 10 뼈대 → 네 실제 회의 언어
- **보조(20%)**: english_quiz.py 725 DB → 일반 비즈니스 영어 pragmatic drill 보조

이유: 코퍼스가 네 수준의 정확한 i+1 (매일 듣는 말). 725 DB는 일반 비즈니스 영어라 너무 쉽거나 화체가 안 맞을 수 있음.

### 5.7 도구 요구사항 (analyze_corpus.py 산출물 기반)

| 도구 | 역할 | 입력 | 산출 |
|:---|:---|:---|:---|
| corpus_pattern.py | 유형별 패턴 추출 + 뼈대 사전 | analyze_corpus.py --json | 유형별 드릴 소재 |
| english_drill.py | 주간 세트 + ①②③ play + ④ compare | webex-audio/ 전사본+wav | 20분 루틴 실행 |
| english_quiz.py (축소) | ⑤ pragmatic drill | 725 DB + 코퍼스 패턴 | 상황 카드 발화 |

### 5.8 분석 한계 (솔직한 기록)

1. **Whisper 잔재 미완전 제거** — `yeah yeah yeah`(158) 등 반복 토큰이 정제 후에도 남음. 학습 소재 추출 시 추가 정제 필요.
2. **자동 클러스터링 실패** — TF-IDF n-gram 기반 k-means가 의미 유형 안 잡음. 의미 분류는 LLM 직독으로 대체 (5.1).
3. **전사 품질 편차** — INTEL 12/5(평균문장 159.7), Liqid 5/27(1269) 등 문장 분리 안 된 회의 존재. 발췌 시 해당 회의는 제외 또는 재처리 권장.
4. **D 유형 표본 부족 (5개)** — 이슈 디버깅 회의가 적어 4주 cycle에서 D 주간 자료 부족 가능. C와 통합 운영 검토.

---
