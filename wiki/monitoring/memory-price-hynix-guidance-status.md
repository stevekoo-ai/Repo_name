---
title: 메모리 가격 × 하이닉스 가이던스 — 발표일 Status & Tracking
created: 2026-10-21
updated: 2026-10-26
tags: [memory, dram, nand, hbm, sk-hynix, guidance, monitoring, append-only]
---

## 왜 이 페이지가 있나

반도체 수출 숫자([수출 정점-회복 관찰](semiconductor-export-peak-recovery-status.md))는
9월에 사상 최대를 찍었지만, 하이닉스 주가는 10/20 1,216,000원으로 고점 대비 약 −59%다.
시장이 묻는 것은 "지금 숫자"가 아니라 **"가격이 언제 꺾이나, 회사가 다음 분기를 어떻게
말하나"**다. 이 페이지는 그 두 축을 한곳에서 발표일마다 기록한다.

- 축 ① **메모리 계약가 방향** — D램·NAND 분기 계약가(전망·확정)
- 축 ② **하이닉스 가이던스** — 출하량(B/G) 가이던스 대비 실적, 다음 분기 전망
- 축 ③ **동종사 가이던스** — 마이크론 다음 분기 매출 가이던스

판정은 근거이지 매매 지시가 아니다(R4). 숫자가 없으면 "판단 불가"이고 "안전"이 아니다(R3).

---

## Latest Status (2026-10-21)

| 축 | 최신 근거 | 판정 |
| --- | --- | --- |
| ① 계약가 | TrendForce(9/30): 4Q26 범용 D램 계약가 **+10~15% QoQ**, HBM 포함 +15~20%, NAND +15~20%. 상승 속도는 둔화. 10/20 보도(Commercial Times 인용)는 약 +20% — 범위 기준 미확인 | 🟢 **상승 지속, 속도 둔화** — 계약가 하락 신호 없음 |
| ② 하이닉스 | 3Q 추정(증권사 2곳): D램 B/G **+7.1%**(가이던스 약 10% 미달), D램 ASP **+17~20%**, NAND B/G +2.9%·ASP +7~19%. 영업이익 72.7~73.8조원(환율로 시장 예상 하회 전망) | 🟡 **가격 주도 성장** — 4Q 가이던스는 10/28 발표 전이라 **판단 불가** |
| ③ 마이크론 | 다음 분기 매출 가이던스 **$61.5B**(직전 분기 $54.2B 대비 +13%), FY27 매 분기 증가 제시. 증설 발표(10/1) | 🟢 **업황 정점론 반박** |

**한 줄 요약**: 가격·동종사 가이던스는 아직 꺾이지 않았다. 남은 시험대는 **10/28 하이닉스
3Q 실적의 4Q 가이던스** — q/q 감소를 말하면 피크아웃론(이주환 10/2)이 맞고, 증가면 틀린다.
환율(원/달러 1,332, 1년 최저)은 원화 이익을 깎는 별도 역풍이다.

### 다음 체크

1. **2026-10-28** 하이닉스 3Q 실적 — 4Q 출하·가격 가이던스, HBM 매출 비중(2Q 기준 D램의 약 20%), 커스텀 HBM 언급
2. **2026-10월 말** D램 10월 고정거래가(월간) — 4Q 전망 +10~15% 경로 확인
3. **2026-11-01** 10월 수출입동향 — [수출 관찰](semiconductor-export-peak-recovery-status.md)과 교차 확인

---

## Check History — 역시간순 (최신부터)

| 날짜 & 이벤트 | ① 계약가 | ② 하이닉스 | ③ 마이크론 | 판정 | 비고 |
| --- | --- | --- | --- | --- | --- |
| **2026-10-21 (신설)** | 4Q 범용 D램 +10~15%, NAND +15~20% (TrendForce 9/30) | 3Q D램 B/G +7.1% < 가이던스 약 10%, ASP +17~20% (증권사 추정) | 다음 분기 $61.5B (+13%) | 🟡 가격 주도 성장 지속, 4Q 가이던스 판단 불가 | 9월 반도체 수출 603.0억 달러(+262.8%, 신정점)와 같은 방향. 약세론(이주환 10/2)·커스텀 HBM론(안유화 10/20)의 공통 시험대가 10/28 실적 |

---

## 채찍 효과(Bullwhip) 점검 — 가수요가 섞였는가 (2026-10-26 INGEST, 황승진 교수)

원문: `sources/bullwhip-effect-hwang-seungjin-2026-10-26.md`. 채찍 효과는 최종 수요의 작은 변동이 공급망 상류(부품·장비)로 갈수록
**증폭**되는 현상이다(불확실성 속 이중 주문·유령 주문). 메모리는 공급망 상류라 이 효과의 **가장 큰 수혜자이자 가장 큰 피해자**다.
교수의 경고("AI 가수요가 꺼지면 반도체·장비가 먼저 맞는다")를 이 페이지의 세 축에 대입한다.

| 채찍 효과의 흔적 | 지금 측정값 | 판정 |
| --- | --- | --- |
| 상류 주문 증가율 ≫ 최종 수요 증가율 | 하이퍼스케일러 CapEx QoQ(SEC EDGAR): GOOGL +125.9%·META +158.5%(2026-06-30). 최종 AI 매출(사용량) 증가율은 저장소에 없음 | **판단 불가** — 증폭 비율을 잴 분모(최종 수요)가 없다 |
| 가격이 물량보다 빠르게 오름(부족 공포) | 하이닉스 3Q D램 출하 +7.1% vs ASP +17~20%(증권사 추정), 4Q 계약가 +10~15% 전망 | **흔적 있음** — 가격 주도 상승은 이중 주문 국면과 모양이 같다(원인 단정은 못 함) |
| 장기계약(LTA)·선불로 주문 선점 | 구글·MS·아마존 3~5년 선불·가격밴드 계약, OpenAI·Anthropic 직접 LTA | **양면** — 선점 경쟁은 가수요 신호이면서, 동시에 주문 취소를 어렵게 해 붕괴 속도를 늦춘다 |
| 하류 재고 쌓임 | 고객 재고 축(HBM Cycle Score)은 정성 판단, 서버 고객 재고 수치 없음 | **판단 불가** — 수집 갭 |
| 신용 경로로 꺾임 시작 | 코어위브 채권 수익률 15%(10/14) — 차입으로 GPU를 산 네오클라우드부터 압박 | **첫 균열 후보**, 주문 축소는 아직 관측 안 됨 |

**10/28 가이던스에서 볼 것(채찍 효과 관점)**: ①4Q **출하(B/G) 가이던스**가 가격보다 약한지 — 물량이 안 늘고 가격만 오르면 가수요 쪽 신호 ②고객 재고 언급 ③주문 변경·연기 언급. 교수의 "가수요" 주장은 **방향 경고로 채택**하되, 측정 근거가 생길 때까지 판정은 보류한다(R1·R3).

## 연결

- [반도체수출 정점-회복 관찰](semiconductor-export-peak-recovery-status.md) — 체크리스트 4번(고정가)의 근거를 이 페이지에서 가져간다
- [HBM Cycle Score](hbm-cycle-score-status.md) — 붕괴조건①(ASP 3주 연속 하락) 판정 근거
- [하이닉스 목표주가 근거 추적](sk-hynix-analyst-thesis-checkpoints-status.md) — 약세론·강세론 주장별 대조
- [SK하이닉스 판단 트래커](sk-hynix-decision-tracker.md) — 매매 판단의 단일 출처(이 페이지는 근거만 제공)

## Sources

- 산업통상부, 「2026년 9월 수출입 동향」(2026-10-01) — https://www.motir.go.kr/kor/article/ATCL3f49a5a8c/172254/view
- TrendForce, "AI Server Demand Sustains Memory Contract Price Increases in 4Q26"(2026-09-30) — https://www.trendforce.com/presscenter/news/20260930-13258.html
- TrendForce News(2026-10-20) — https://www.trendforce.com/news/2026/10/20/news-dram-prices-seen-rising-20-qoq-in-4q26-despite-slower-gains-ai-demand-tight-supply-support-outlook/
- `sources/sk-hynix-broker-report-2026-09-30-tp3400000.md`, `sources/sk-hynix-broker-report-2026-09-30-b-lta-openai.md`
- `sources/memory-bear-case-lee-juhwan-2026-10-02.md`, `sources/memory-as-infrastructure-ahn-yoohwa-2026-10-20.md`
- [sk-hynix-analyst-thesis-checkpoints-status.md](sk-hynix-analyst-thesis-checkpoints-status.md) (마이크론 가이던스 기록, 10/2)
