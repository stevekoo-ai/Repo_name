---
title: Economic Calendar Framework
created: 2026-08-09
updated: 2026-08-09
tags: [macro, concept, framework, decision-events]
---

# Economic Calendar Framework

This concept defines how macroeconomic events integrate into personal investment decisions
for SK Hynix and Real Estate market entry timing.

**Purpose**: Transform economic calendar from isolated data → actionable decision triggers
by mapping event outcomes to signal changes in real-time.

---

## 1. Decision Impact Mapping

### 1.1 CPI / PPI Events (Inflation Tracking)

**SK Hynix Signal Impact**:
- **CPI Upside (>3.0%)**: 긴축 우려 심화 → HOLD 신뢰도 ↓10%p → SELL 검토 신호
- **CPI Base (2.7-3.0%)**: 예상 부합 → HOLD 유지 → 신뢰도 무변
- **CPI Downside (<2.5%)**: 물가 안정화 → 경기 둔화 신호 → SELL ↑ (수요 약화 우려)

**Real Estate Signal Impact**:
- **CPI 강세 (>3.0%)**: 실질금리 압박 → 명목금리 인상 우려 → WAIT ↑
- **CPI 정상 (2-3%)**: 금리 기조 유지 → 현재 신호 유지
- **CPI 약세 (<2.0%)**: 명목금리 인하 가능성 ↑ → ENTER 전환 검토

**Measurement**:
- Source: 한국은행 ECOS (한국 CPI), FRED (미국 CPI)
- Consensus vs Actual: 차이 > 0.5%p 시 신호 재평가
- Prior Month 추이: 가속/안정/감속 패턴 분석

---

### 1.2 기준금리 / 정책금리 Events (Monetary Policy)

**SK Hynix Signal Impact**:
- **인하 신호**: 달러약세 + 유동성 확대 → BUY 신호 전환 (신뢰도 +15%p)
- **동결**: 현상 유지 → HOLD (기대치 부합)
- **인상**: 고금리 장기화 → SELL 검토 (수요 악화)

**Real Estate Signal Impact**:
- **인하 신호**: 월상여금 부담 ↓ → ENTER 신호 전환 가능 (신뢰도 +20%p)
- **동결**: WAIT 유지 → 플랫폼시티 이벤트만 모니터
- **인상**: 명목금리 상승 → WAIT 강화 (신뢰도 +10%p)

**Measurement**:
- 한국은행 금융통화위원회 (매월 14일경)
- 연방기금금리 FOMC 회의 (분기별)
- Market 선행 지표: 3M 금리 스왑, 선물 시장 기대치

---

### 1.3 고용 / 실업률 Events (Labor Market)

**SK Hynix Signal Impact**:
- **고용 강세 (Upside)**: 경기 견조 신호 → HOLD 신뢰도 +5%p
- **고용 약세 (Downside)**: 경기 둔화 신호 → SELL 관심 ↑ (수요 약화)

**Real Estate Signal Impact**:
- **고용 강세**: 소비심리 개선 → 건설 경기 우호 → ENTER 신호 약보강
- **고용 약세**: 구직활동 감소 → 경기 둔화 신호 → WAIT 강화

---

## 2. Event Importance Classification

| 등급 | 신호 변경 가능성 | 신뢰도 변동 | 예시 |
|------|----------|---------|------|
| 🔴 Critical | 높음 (신호 전환 가능) | ±10-20%p | 미국 CPI, 기준금리 결정 |
| 🟡 High | 중간 (신뢰도 변동) | ±5-10%p | 미국 고용, 한국 CPI |
| 🟢 Medium | 낮음 (모니터 수준) | ±0-5%p | 제조업 PMI, 소비자신심 |

---

## 3. Scenario Planning Template

**각 Critical 이벤트마다 D-3일 전 수립**:

### Example: 미국 CPI (월 12일)

| 시나리오 | 예상치 | 가능성 | SK Signal | RE Signal | Action |
|--------|--------|--------|----------|----------|--------|
| **Downside** | <2.5% | 20% | SELL 고려 | WAIT 강화 | 약달러 but 경기 약세 우려 |
| **Base** | 2.8% | 60% | HOLD 유지 | WAIT 유지 | 예상 부합 → 신호 무변 |
| **Upside** | >3.2% | 20% | HOLD↓신뢰도 | WAIT↑신뢰도 | 긴축 우려 심화 |

---

## 4. Post-Event Analysis Framework

### 4.1 Immediate (발표 후 2시간)

1. **Event vs Consensus Gap**
   - Difference > 0.5%p → 신호 재평가 필요 판정
   - Signal change threshold 계산

2. **Market Reaction**
   - USD/KRW 즉시 반응 추적
   - 선물 시장 변화 (S&P 500, Kospi)
   - 금리 스왑 변화

3. **Decision Impact**
   - "현재 HOLD 신호는 유효한가?"
   - "Real Estate WAIT는 지속되는가?"

### 4.2 Follow-up (발표 후 1주)

- Market repricing 완료 여부 확인
- 신호 변경의 지속성 판단
- 다음 critical event까지의 holding period 판정

---

## 5. Data Sources & Automation

### Primary Sources (자동화 가능)

- **한국은행 ECOS API**: CPI, 기준금리, 고용
- **FRED API**: 미국 CPI, 실업률, FOMC 결정
- **Trading Economics API**: 컨센서스, 예상치
- **웹 스크래핑 (Selenium)**: investing.com (캘린더), tradingeconomics.com

### Fallback (수동)

- 사용자 캡처 (이메일 또는 웹 조회)
- 뉴스 검색 ("미국 CPI 발표 결과")

---

## 6. Integration with Decision Engines

### SK Hynix Decision Engine

```python
def apply_economic_event_impact(signal, confidence, event_name, actual_vs_consensus):
    """
    이벤트 결과에 따른 신호/신뢰도 조정
    """
    if event_name == "미국 CPI":
        if actual_vs_consensus > 0.5:  # Upside
            return signal, confidence - 10  # 신뢰도 감소 (긴축 우려)
        elif actual_vs_consensus < -0.5:  # Downside
            return signal, confidence - 10  # 신뢰도 감소 (경기 둔화)
    return signal, confidence
```

### Real Estate Decision Engine

```python
def apply_economic_event_impact_realestate(signal, confidence, event_name, actual_vs_consensus):
    """
    Real Estate 신호 조정
    """
    if event_name == "기준금리 결정":
        if "인하" in result:
            return "ENTER", confidence + 20
        elif "인상" in result:
            return "WAIT", confidence + 10
    return signal, confidence
```

---

## 7. Monitoring & Alerts

**매일 체크 (아침 07:00 KST)**:
1. 다음 Critical 이벤트는 언제인가? (D-days)
2. 발표 전 컨센서스는? (시나리오 준비)
3. 어제 이벤트 결과는? (사후 분석)

**신호 변경 조건**:
- Event Consensus vs Actual 차이 > 1.0%p
- 또는 명시적 Policy Signal 변화 (인하/인상)

---

## References

- 한국은행 정책금리: [base.kbstat.com](https://base.kbstat.com)
- FRED API: [fred.stlouisfed.org](https://fred.stlouisfed.org)
- Trading Economics: [tradingeconomics.com](https://tradingeconomics.com)
- investing.com Calendar: [investing.com/economic-calendar](https://investing.com/economic-calendar)

---

## Maintenance

- **Last Updated**: 2026-08-09 (Framework definition only)
- **Daily Tracking**: See `monitoring/economic-events-status.md`
- **Issue Reports**: Log decision signal changes caused by economic events in monitoring page
