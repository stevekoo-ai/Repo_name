# 용인 플랫폼시티 청약 시스템 (Yongin Platform City Subscription System)

## 📋 개요

개인 경제 의사결정 시스템(PEOS)의 일부로, 용인 플랫폼시티 관련 청약 공고를 자동으로 감지하고 사용자에게 알림을 제공하는 통합 시스템입니다.

---

## 🔑 핵심 발견사항

### 주택 유형 분류의 중요성

**역사적 데이터 분석 결과:**
- 청약Home에서 "플랫폼시티"로 검색되는 모든 프로젝트는 **민영(Private) 주택**으로 분류됨
- 예: 라온프라이빗 아르디에 (2026-03-13), e편한세� 용인역 플랫폼시티 (2023-04-20)
- 현재 시스템은 국민주택(Public Housing) 만 추적 → **범위 확대 필요**

**시스템 영향:**
```
현재 상태: 국민주택(공공) 공고만 감지 ❌
실제 필요: 국민주택 + 민영 공고 모두 감지 ✅
```

---

## 🏗️ 아키텍처

### 1. 데이터 모델 (Data Schema)

#### 청약 공고 구조 (`data/manual_inputs/subscription_notices.yaml`)

```yaml
notices:
  - name: "프로젝트명"
    agency: "발행 기관 (LH/플랫폼시티운영사 등)"
    region: "지역"
    is_platform_city: true/false      # 플랫폼시티 여부
    housing_type: "국민주택|민영"     # ⚠️ 필수 필드
    supply_type: "일반공급"
    size: "84㎡ 이상"
    household_count: 1500
    announce_date: "2026-09-01"
    application_start: "2026-09-15"
    application_end: "2026-09-20"
    expected_price_krw: 850000000
    expected_competition_ratio: 15.2   # 또는 null (미확정)
    source: "청약홈 (수동 입력)"
```

**필드 설명:**
| 필드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| `name` | str | 프로젝트 공식명 | "세종 5-1생활권 공공분양" |
| `agency` | str | 시행기관 | "LH" / "플랫폼시티" |
| `region` | str | 공급 위치 | "용인 기흥구" |
| `is_platform_city` | bool | 플랫폼시티 프로젝트 여부 | true |
| `housing_type` | str | **국민주택 또는 민영** | "민영" |
| `expected_price_krw` | int | 예상 가격 (원) | 850000000 |
| `expected_competition_ratio` | float/null | 예상 경쟁률 | 12.5 또는 null |

---

### 2. API 통합 (청약Home - data.go.kr)

#### 쿼리 엔드포인트

```
GET https://api.odcloud.kr/api/ApplyhomeInfoDetailSvc/v1/getAPTLttotPblancDetail
Header: Authorization: Infuser <SERVICE_KEY>
```

#### 주요 쿼리 조건

| 조건 | 필드 | 용도 |
|------|------|------|
| 직접 검색 | `cond[HOUSE_NM::LIKE]` | "플랫폼시티" 정확 매칭 |
| 시도 검색 | `cond[HSSPLY_ADRES::LIKE]` | "용인" (광범위) |
| 구 검색 | `cond[HSSPLY_ADRES::LIKE]` | "기흥구" (정확 위치) |

#### 응답 필드

```json
{
  "data": [
    {
      "HOUSE_NM": "라온프라이빗 아르디에",
      "HOUSE_DTL_SECD_NM": "민영아파트",
      "HSSPLY_ADRES": "경기도 용인시 기흥구...",
      "RCRIT_PBLANC_DE": "2026-03-13",
      "SUBSCRPT_AREA_CODE_NM": "...",
      ...
    }
  ],
  "totalCount": 42,
  "matchCount": 10
}
```

**핵심 필드:**
- `HOUSE_DTL_SECD_NM`: 주택 유형 코드 (국민주택/민영/임대 등) → 자동 분류
- `HOUSE_NM`: 프로젝트 명칭
- `RCRIT_PBLANC_DE`: 공고 일시
- `HSSPLY_ADRES`: 공급 위치

---

## 🔧 구현 (Implementation)

### 1. 검증 스크립트

**파일:** `scripts/verify_platform_city_listings.py`

**기능:**
```
1. 플랫폼시티 이름 검색
   ↓
2. 용인시 주소 검색
   ↓
3. 기흥구 주소 검색
   ↓
4. 결과를 주택 유형별로 분류
   ↓
5. 시스템 범위 권고 생성
```

**실행:**
```bash
export DATA_GO_KR_KEY="<service_key>"
python3 scripts/verify_platform_city_listings.py "$DATA_GO_KR_KEY"
```

**출력 예시:**
```
1️⃣ Search: 플랫폼시티 (exact house name match)
────────────────────────────────────────────────
📊 Total matches: 2 (displayed: 2)

  🏢 라온프라이빗 아르디에
     Type: 민영 (Private)
     Address: 경기도 용인시 기흥구...
     Announce: 2026-03-13

📈 Summary by Housing Type:
  • 민영 (Private): 2 listings
  • 국민주택 (Public): 0 listings

💡 NOTIFICATION SYSTEM SCOPE:
   ⚠️  Yongin Platform City historical data shows PRIVATE (민영) housing.
   ✅ RECOMMENDATION: Expand scope to include BOTH 국민주택 & 민영 types
```

### 2. 자동화 워크플로우

**파일:** `.github/workflows/verify-platform-city.yml`

**트리거:**
- 스크립트 수정 후 푸시
- 수동 트리거

```bash
gh workflow run verify-platform-city.yml
```

### 3. 주택 유형 분류 로직

**구현:** `scripts/verify_platform_city_listings.py` → `categorize_housing_type()`

```python
def categorize_housing_type(row: dict) -> str:
    """HOUSE_DTL_SECD_NM에서 주택 유형 추론"""
    house_type_code = row.get("HOUSE_DTL_SECD_NM", "").upper()
    
    if any(x in house_type_code for x in ["국민", "공공", "임대"]):
        return "국민주택 (Public)"
    elif any(x in house_type_code for x in ["민영", "Private", "분양"]):
        return "민영 (Private)"
    else:
        return f"Unknown ({house_type_code})"
```

---

## 📊 점수 계산 (Housing Readiness Scoring)

**파일:** `engine/personal/housing.py`

### 계산 공식

```
Housing Readiness Score = 
    0.30 × eligibility_fit           # 계좌 활성화 기간
  + 0.25 × funding_readiness          # 자금 준비도
  + 0.20 × region_type_match          # 지역/형식 부합도
  + 0.15 × timing_readiness           # 신청 시간까지 여유
  + 0.10 × competition_adjustment     # 경쟁률 역조정
```

### 점수 요소 설명

| 요소 | 가중치 | 설명 | 범위 |
|------|--------|------|------|
| eligibility_fit | 30% | 청약통장 보유 기간 (10년 만기) | 0-100 |
| funding_readiness | 25% | 자금 준비 정도 (예상가 20% 목표) | 0-100 |
| region_type_match | 20% | 우선지역 + 선호 크기 부합 | 25-100 |
| timing_readiness | 15% | 신청까지 남은 일수 | 40-100 |
| competition_adjustment_inverse | 10% | 경쟁률 낮을수록 높음 | 0-100 |

### 플랫폼시티 전용 분석 (`platform_city_analysis`)

신청 공고가 `is_platform_city: true`이면 추가 분석 생성:

```json
{
  "platform_city_analysis": {
    "location": "용인 기흥구",
    "supply_scale_households": 1500,
    "expected_schedule": {
      "announce_date": "2026-09-01",
      "application_start": "2026-09-15",
      "application_end": "2026-09-20"
    },
    "expected_price_krw": 850000000,
    "funding_gap_krw": 20000000,
    "expected_competition_ratio": null,
    "user_fit_score": 72.5,
    "risk_notes": [
      "예상 경쟁률 미확정 — 청약홈 공고 확정 후 재평가 필요",
      "자금조달 갭 발생 시 채권/현금 배분 조정 필요"
    ]
  }
}
```

---

## 📝 데이터 흐름

### 1. 수동 입력 워크플로우

```
User 발견         청약Home 공고에서 플랫폼시티 프로젝트 발견
    ↓
검증 실행         python3 scripts/verify_platform_city_listings.py
    ↓
데이터 입력       data/manual_inputs/subscription_notices.yaml에 추가
    ↓
점수 계산         engine/personal/housing.py → compute_housing_readiness()
    ↓
리포트 생성       engine/report/run.py → 월간 리포트에 포함
    ↓
알림 발송         src/clock/notify.py → 이메일/Slack 알림
```

### 2. 자동 검증 워크플로우

```
코드 푸시                    
    ↓
verify-platform-city.yml 트리거
    ↓
GitHub Actions 환경에서 스크립트 실행
    ↓
청약Home API 쿼리
    ↓
결과 분류 및 권고 생성
    ↓
워크플로우 로그에 출력
```

---

## 🔌 설정 (Configuration)

### 환경 변수

**`.env.example`에 추가:**
```bash
# 청약Home API 키 (data.go.kr)
DATA_GO_KR_KEY="<your_service_key>"
```

**GitHub Actions Secrets:**
- `DATA_GO_KR_KEY` 설정 필수 (워크플로우 자동 실행 위함)

### 규칙 설정

**파일:** `config/rules.yaml`

```yaml
housing:
  eligibility_fit: 0.30
  funding_readiness: 0.25
  region_type_match: 0.20
  timing_readiness: 0.15
  competition_adjustment_inverse: 0.10
```

---

## 🧪 테스트

**모든 테스트 통과:**
```bash
python -m pytest tests/test_housing.py -v
# ✅ test_housing_warning_when_deadline_imminent_and_funding_short PASSED
# ✅ test_no_notices_is_pending_not_a_guess PASSED
```

---

## 📂 파일 구조

```
Repo_name/
├── data/
│   └── manual_inputs/
│       └── subscription_notices.yaml          # 청약 공고 입력 (housing_type 필드 포함)
├── scripts/
│   ├── verify_platform_city_listings.py       # 검증 스크립트
│   └── README.md                               # 스크립트 문서
├── .github/workflows/
│   ├── subscription-schema-probe.yml          # 기존: 스키마 검증
│   ├── network-diagnostic.yml                 # 기존: 네트워크 검사
│   └── verify-platform-city.yml               # 신규: 플랫폼시티 검증
├── engine/personal/
│   ├── housing.py                             # 점수 계산 엔진 (housing_type 필드 지원)
│   └── portfolio_impact.py                    # 개인화 매핑
├── collectors/
│   └── manual.py                              # 수동 입력 로더
├── config/
│   ├── api.yaml                               # API 설정
│   ├── rules.yaml                             # 규칙/가중치
│   ├── user.yaml                              # 사용자 프로필
│   └── portfolio.yaml                         # 자산 포트폴리오
└── docs/
    └── SUBSCRIPTION_SYSTEM.md                 # 본 문서
```

---

## 🚀 사용 시나리오

### Scenario 1: 플랫폼시티 공고 발견

```
1. 청약Home에서 "용인 플랫폼시티" 공고 발견
2. 스크립트 실행: python3 scripts/verify_platform_city_listings.py
3. 결과 검증: 민영(Private) 주택으로 분류 확인
4. YAML 입력: data/manual_inputs/subscription_notices.yaml에 추가
   - housing_type: "민영"
   - is_platform_city: true
5. 점수 계산: engine/personal/housing.py 자동 실행
6. 리포트 생성 및 알림 발송
```

### Scenario 2: 자동 검증 (GitHub Actions)

```
1. scripts/verify_platform_city_listings.py 수정 후 푸시
   또는 verify-platform-city.yml 수동 트리거
2. GitHub Actions 워크플로우 실행
3. 청약Home API 자동 쿼리
4. 워크플로우 로그에 결과 출력
5. 개발자 검토
```

---

## ⚠️ 주의사항

### 1. housing_type 필드는 필수

```yaml
# ❌ 틀림
- name: "플랫폼시티 공고"
  is_platform_city: true
  supply_type: "일반공급"
  # housing_type 누락!

# ✅ 맞음
- name: "플랫폼시티 공고"
  is_platform_city: true
  housing_type: "민영"  # 필수
  supply_type: "일반공급"
```

### 2. 주택 유형 분류는 API 응답 기반

- `HOUSE_DTL_SECD_NM` 필드에서 자동 추론
- 애매한 경우 스크립트 출력으로 검증 후 수동 입력

### 3. 경쟁률이 null인 경우

공고 초기에는 경쟁률이 미정(`null`)일 수 있음:
- 리포트에 "예상 경쟁률 미확정 — 청약홈 공고 확정 후 재평가 필요" 경고 표시
- 공고 마감 후 실제 경쟁률로 업데이트

---

## 🔄 향후 확장 (Future Roadmap)

- [ ] 청약Home API 자동화 (수동 입력 → 실시간 API)
- [ ] 여러 플랫폼 통합 (LH, GH, SH 등)
- [ ] 머신러닝 기반 경쟁률 예측
- [ ] 개인화된 알림 (지역/가격대 필터)
- [ ] 모바일 앱 연동

---

## 📞 문의 및 피드백

주요 구현 파일:
- 검증: `scripts/verify_platform_city_listings.py`
- 점수: `engine/personal/housing.py`
- 자동화: `.github/workflows/verify-platform-city.yml`
- 데이터: `data/manual_inputs/subscription_notices.yaml`

각 파일 내 주석 및 `scripts/README.md` 참고
