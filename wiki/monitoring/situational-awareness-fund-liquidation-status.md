---
title: Situational Awareness LP 강제청산 — 사건 진행 기록
created: 2026-08-02
updated: 2026-08-02
tags: [hedge-fund, leverage, margin-call, citadel, sk-hynix, daily-tracking, monitoring, append-only]
---

# Event Timeline & Resolution

**Resolution Status**: ✅ **COMPLETE (2026-07-30)** — Citadel acquired entire public portfolio ($16B block deal), overhang eliminated, portfolio consolidation ongoing.

---

## Event Sequence (Chronological)

| 시점 | 사건 | 영향·규모 | 해석 |
| --- | --- | --- | --- |
| **2024-09** | SA 설립 (Leopold Aschenbrenner, 前OpenAI) | 초기자본 약 $225M | AI 전문 헤지펀드 창립 |
| **~2026-06월말** | AUM $45B, 누적수익률 +439%(수수료 후) | 약 4배 레버리지 구조 | "AI Midas" 평가, 고수익·고위험 포지션 구축 |
| **2026-07(한달간)** | SA 집중 보유종목 **35~47% 하락** (SK하이닉스·CoreWeave·Nebius·Micron·Bloom Energy) | 레버리지 담보가치 붕괴 | 4배 구조에서 최소 손절매 위기 도래 |
| **2026-07-29(수, 촉발)** | **SK하이닉스 2분기 실적 컨센서스 미달** + 나스닥 -1.7~2.1% | SK하이닉스가 직접 촉발 역할 | SA가 보유한 종목 중 하나의 악재가 전체 포트폴리오 붕괴의 첫 도미노 |
| **2026-07-29~30** | **3개 프라임브로커 동시 마진콜** (골드만삭스·JP모건·BofA) | 담보 추가 요구 불가능 | 긴급 24시간 협상 |
| **2026-07-30(화, 핵심)** | **Citadel이 SA의 전체 공개주식 포트폴리오 인수** | **$16B 블록딜** (월가 역사상 최대) | SK하이닉스·CoreWeave·Nebius 등 전부 시타델로 이전, SA는 비상장(Anthropic 지분 $5B) 등만 남겨 소형 사모펀드로 축소(AUM $45B→약 $10B) |
| **2026-07-31(수, 반응)** | **"매물 공포(overhang)" 해소** → 급반등 | SOX +8.19%, 코스피 +17.91%, 삼성전자 +27%, SK하이닉스 +29.95%(상한가) | SA 보유 종목들이 정확히 이 방향으로 가장 강하게 반등 — 강제매도 공포 제거의 심리적 효과 |

---

## SK하이닉스 직결도 분석

### 포지션 규모 (2026-08-02 밤 검증)

**Input**: SK하이닉스 시총 $865.5B, SA 전체 블록딜 $16B

| 가정 비중 | SK하이닉스 특정 규모 | 시총 대비 |
| --- | --- | --- |
| 15% | $2.40B | **0.28%** |
| 20% | $3.20B | **0.37%** |
| 30%(최대 후하) | $4.80B | **0.56%** |

**Cornerstone 투자 수치로 재검증**: SA가 SK하이닉스 ADR 상장($28B, 2026-07)의 **최대 cornerstone investor**로 최대 $7B 참여 의사 → 3사(SA·Baillie Gifford·Coatue) 합산 약 $5B 배정 → SA 개별 최대치 추정 $1.7B = SK하이닉스 시총 **0.19~0.81%** (같은 자릿수로 재확인)

### 결론

1. **코스피·삼성전자 전체 랠리 설명력**: **규모상 성립하지 않음** — $2.4~4.8B는 수조 달러 규모의 코스피 시총 대비 반올림 오차 수준
2. **SK하이닉스 개별 종목 변동성 설명력**: **제한적으로 가능** — 일평균 거래대금(수천억~1조원대, 정밀 미확인) 대비로는 $2.4~4.8B(약 3.5~7조원) 규모가 정상 거래대금의 여러 배이므로, **단기 가격 변동(7/29~31)에는 유의미하게 기여했을 가능성** 남음 (다만 정밀 검증 없이는 **가설**임)
3. **7/31 급등의 진짜 동인**: 
   - **펀더멘털 호재** (아마존·MS CapEx 확정, 삼성 "2028년까지 공급부족" 가이던스) = **지속 가능한 재평가**
   - **Overhang 해소** (시타델 급인수로 강제매도 공포 제거) = **일회성 안도 랠리**, 수요 증가 아니라 비정상적 매도 압력 제거
   - 7/31은 이 둘이 **같은 날 겹쳐서 증폭**, 어느 쪽이 얼마나 기여했는지 정량적으로 분리 어려움

---

## Wiki 기존 프레임에 주는 함의

### 급락(7/28~30) 원인 보완
- 기존: CXMT IPO + 실적 미달 + 중국 노광장비 공포
- **추가 축**: SK하이닉스 개별 악재 → SA 담보 붕괴 → 다른 종목(CoreWeave·Nebius) 강제매도 까지 한 묶음으로 얽혀 **증폭**

### 급반등(7/31) 원인 재해석 (가장 중요)
- 기존: 아마존·MS CapEx + 삼성 공급부족 가이던스 ✅
- **추가 축**: Overhang 해소의 심리적 전염 → "AI 테마 전반" 안도 랠리 (가설, 정성적, 미검증)

### 관련 기존 페이지의 신중론 강화
- [찐반등 신호③(외국인 수급)](market-cycles-leverage-risk.md): 7/31 외국인 +3조 5,883억원 중 일부는 시타델 리밸런싱·차익거래일 가능성 → 기존 "20일 지속 기준 판정" 신중론 재확인
- [패닉 회복 신호 "회복 초입"](panic-recovery-signals.md): 7/31 가격 반응의 상당 부분이 일회성 overhang 해소일 수 있음 → Tier1 확인 사항 유효하나 신중론 추가

### 월요일(8/3) 이후 전망
- **긍정**: SA overhang 완전히 해소 → 이 요인 더 이상 매도 압력 아님
- **주의**: 시타델이 인수한 $16B 포지션을 자체 리스크 관리로 점진적 재조정 가능 → 간헐적 매물 출회 가능성 배제 불가
- **기본**: SK하이닉스 펀더멘털(HBM 수요·CapEx·CXMT) 이 사건과 무관하게 그대로 유효

---

## Sources

- [CNBC — Situational Awareness Fund Unwinding](https://www.cnbc.com/2026/07/30/)
- [Bloomberg — Aschenbrenner Hedge Fund Citadel Deal](https://www.bloomberg.com/news/articles/2026-07-30/)
- [TechTimes — Citadel Buys Situational Awareness](https://www.techtimes.com/articles/322285/20260730/)
- [SpotGamma — Margin Call Anatomy](https://spotgamma.com/situational-awareness-unwind-margin-call-ai/)
- [Hedgeweek — SA Cornerstone Investor for SK Hynix ADR](https://www.hedgeweek.com/situational-awareness-backs-sk-hynixs-28bn-us-listing/)
- [Seoul Economic Daily — SK Hynix ADR Cornerstone Backing](https://en.sedaily.com/finance/2026/07/08/sk-hynix-lands-record-cornerstone-backing-for-adr-draws-ai)
- [SK하이닉스 목표주가 근거 체크리스트](../concepts/sk-hynix-analyst-thesis-checkpoints.md) (framework 참고, Layer 3)
