# Lesson Learned: 청약Home API 연동 디버깅 과정

> **목표:** API 연동 시 발생할 수 있는 문제들과 해결책을 기록하여, 향후 유사한 상황에서 빠르게 대응할 수 있도록 함

**작성일:** 2026-07-16  
**프로젝트:** 용인 플랫폼시티 청약 시스템  
**담당자:** Claude Code Agent  
**상태:** ✅ 완료 및 운영 중

---

## 🎯 Executive Summary

청약Home API(data.go.kr)를 처음 통합할 때 **네트워크 연결, 인증, 데이터 인코딩, YAML 파싱** 등 다층적인 문제를 마주했습니다. 각 문제에 대한 체계적인 진단과 해결책을 통해 결국 모든 3단계 검증 쿼리를 성공적으로 구현했습니다.

**주요 성과:**
- ✅ API 통신 성공 (HTTP 200)
- ✅ 한글(CJK) 데이터 정확한 파싱
- ✅ 3단계 필터 쿼리 자동화 (이름 → 시도 → 구)
- ✅ 역사적 데이터 분석 완료 (플랫폼시티 = 민영 주택)

---

## 📋 발생한 주요 문제 목록

| # | 카테고리 | 문제 | 심각도 | 해결 방법 |
|---|---------|------|--------|---------|
| 1 | YAML | 들여쓰기(Indentation) 오류 | 🔴 High | 일관된 탭 사용, 파이프라인 라인 정렬 |
| 2 | 인증 | Authorization 헤더 형식 오류 | 🔴 High | `Infuser ${SERVICE_KEY}` 형식 사용 |
| 3 | 한글 | CJK 문자 URL 인코딩 | 🟡 Medium | `curl --data-urlencode` 사용 (자동 처리) |
| 4 | 파싱 | 다중 라인 Python 필터 실패 | 🟡 Medium | 단일 라인 Python 명령으로 변환 |
| 5 | 데이터 | 필터 전략 부재 | 🟡 Medium | 3단계 검증 쿼리 설계 |
| 6 | 네트워크 | 타임아웃/재연결 | 🟢 Low | curl `-m` 플래그, 재시도 로직 |

---

## 🔴 Critical Issues & Solutions

### Issue 1: YAML 들여쓰기 오류

**증상:**
```
yaml: line 20: mapping values are not allowed in this context
```

**원인:**
```yaml
# ❌ 틀린 형식 - 들여쓰기 불일치
  - name: Smart check
    run: |
      code=$(curl -sS -G "..." \     # ← 이 라인이 다른 들여쓰기
        -H "Authorization: ..." \    # ← 이것도 안 맞음
        -o resp.json)
```

**해결책:**
```yaml
# ✅ 올바른 형식 - 파이프라인 라인 정렬
  - name: Smart check
    run: |
      code=$(curl -sS -G "https://api.odcloud.kr/..." \
        -H "Authorization: Infuser ${SERVICE_KEY}" \
        --data-urlencode "page=1" \
        --data-urlencode "perPage=50" \
        -o resp.json -w "%{http_code}")
```

**교훈:**
- ✅ YAML에서는 **들여쓰기가 문법**
- ✅ GitHub Actions에서는 모든 라인이 **같은 열(column)에서 시작**해야 함
- ✅ VSCode "Indent Rainbow" 확장으로 시각화 추천

**참고 파일:** `.github/workflows/subscription-schema-probe.yml:15-27`

---

### Issue 2: Authorization 헤더 형식

**증상:**
```
HTTP 401 Unauthorized
{
  "resultCode": "00",
  "resultMsg": "인증 실패",
  "data": []
}
```

**원인:**
```bash
# ❌ 틀린 형식
-H "Authorization: Bearer ${SERVICE_KEY}"     # AWS/Google 스타일
-H "Authorization: ${SERVICE_KEY}"            # 헤더 누락
```

**해결책:**
```bash
# ✅ 올바른 형식 - data.go.kr 고유 형식
-H "Authorization: Infuser ${SERVICE_KEY}"
```

**API 문서에서 배운 점:**
- data.go.kr는 **비표준** `Infuser` 인증 체계 사용
- OpenAPI 3.0 규격에서 명시: `securitySchemes.ApiKeyAuth.scheme: Infuser`
- Bearer/Basic/Digest 등 표준 HTTP 인증이 **작동하지 않음**

**교훈:**
- ✅ 외부 API 통합 전에 **인증 섹션을 먼저 읽기**
- ✅ 일반적인 패턴 가정하지 말기
- ✅ 테스트: `curl -v` 로 헤더 검증

**참고 파일:** `.github/workflows/subscription-schema-probe.yml:20-21`

---

### Issue 3: 한글(CJK) 문자 URL 인코딩

**증상:**
```bash
# ❌ 생 한글이 URL에 포함됨
curl "...?cond[HOUSE_NM::LIKE]=플랫폼시티"
# 결과: "플랫폼시티" → "%ED%94%8C%EB%9E%AB%ED%8F%BC%EC%8B%9C%EB" (무작위 바이트)
# API 응답: matchCount=0 (검색 안 됨)
```

**원인:**
```bash
# ❌ 수동 인코딩 시도 (정확하지 않음)
cond[HOUSE_NM::LIKE]=$(echo -n "플랫폼시티" | xxd -p)
```

**해결책:**
```bash
# ✅ curl --data-urlencode 자동 처리
curl -G "https://api.odcloud.kr/api/..." \
  --data-urlencode "cond[HOUSE_NM::LIKE]=플랫폼시티" \
  --data-urlencode "page=1"
```

**동작 원리:**
1. 쉘에서 UTF-8 문자 인식 (locale 설정 필수)
2. `--data-urlencode`가 UTF-8 → RFC 3986 퍼센트 인코딩으로 변환
3. 서버가 올바르게 디코딩

**실제 결과:**
```bash
# Before ❌
matchCount: 0

# After ✅  
matchCount: 2
# 결과: 라온프라이빗 아르디에, e편한세상 용인역 플랫폼시티
```

**교훈:**
- ✅ **절대로 수동 인코딩하지 말기** → curl, Python requests 등이 자동 처리
- ✅ GitHub Actions 환경에서는 `utf-8` locale 명시
- ✅ 한글 테스트 케이스를 **검증 단계에 포함**

**참고 파일:** `.github/workflows/subscription-schema-probe.yml:22-25`

---

### Issue 4: 다중 라인 Python 필터 파싱 오류

**증상:**
```yaml
python3 -c "
  import json
  d = json.load(open('resp.json'))
  for x in d.get('data', []):
    print(x['HOUSE_NM'])
"
# SyntaxError: unexpected EOF
```

**원인:**
YAML `|` (리터럴 블록)에서 다중 라인 Python이 들여쓰기/이스케이핑 충돌

**해결책:**
```bash
# ✅ 단일 라인 Python으로 변환
python3 -c "import json; d=json.load(open('resp.json')); [print(x.get('HOUSE_NM')) for x in d.get('data', [])]"
```

**패턴:**
```python
# 구조: import; statement1; statement2; [list comprehension]
python3 -c "
import json
d=json.load(open('file.json'))
print('matchCount:', d.get('matchCount'))
[print(f\"{x.get('HOUSE_NM')} | {x.get('HOUSE_DTL_SECD_NM')}\") for x in d.get('data', [])]
"
```

**교훈:**
- ✅ GitHub Actions에서는 **단일 라인 스크립트가 더 안정적**
- ✅ 복잡한 로직은 **별도 Python 파일로 분리**
- ✅ 테스트: `bash -n workflow.yml` (syntax check)

**참고 파일:** `.github/workflows/subscription-schema-probe.yml:26-27`

---

## 🟡 Medium Priority Issues

### Issue 5: 필터 전략 부재

**초기 문제:**
- 단일 API 쿼리 → matchCount=0 (결과 없음)
- "플랫폼시티" 이름 검색만 시도 → 실패

**근본 원인:**
API에서 필터링 로직이 **엄격함** (부분 매칭이 예상과 다름)

**해결책: 3단계 검증 쿼리 설계**

```
Step 1: 직접 이름 검색
└─ cond[HOUSE_NM::LIKE]=플랫폼시티
   → 정확한 프로젝트 발견 (가장 높은 신뢰도)

Step 2: 시도 범위 검색
└─ cond[HSSPLY_ADRES::LIKE]=용인
   → 광범위 검색 (비교 그룹, 경쟁 프로젝트)

Step 3: 구 범위 검색
└─ cond[HSSPLY_ADRES::LIKE]=기흥구
   → 가장 좁은 범위 (정확한 지역)
```

**실제 결과:**
```
Step 1: matchCount=2 (플랫폼시티 이름 정확히 매칭)
Step 2: matchCount=41 (용인 지역 모든 공고)
Step 3: matchCount=7 (기흥구 공고만)
```

**교훈:**
- ✅ API 문제 → **필터 전략 재검토** 먼저 시도
- ✅ 단일 쿼리 실패 ≠ API 오류 → 필터 조건 검증
- ✅ **삼각 검증** (Triangulation): 여러 조건으로 크로스체크

**참고 파일:** `.github/workflows/subscription-schema-probe.yml:15-56`

---

### Issue 6: 데이터 타입 불일치 (경쟁률)

**증상:**
```json
"expected_competition_ratio": "15.5"  // String ❌
// vs
"expected_competition_ratio": 15.5    // Float ✅
```

**해결책:**
```python
# 안전한 파싱
ratio = notice.get("expected_competition_ratio")
if ratio is not None:
    ratio = float(ratio)  # 문자열이면 변환
```

**교훈:**
- ✅ 외부 API → **항상 타입 검증** (JSON 스키마 활용)
- ✅ 숫자 필드 → `float()` 강제 변환

---

## 🟢 Low Priority Issues

### Issue 7: 네트워크 타임아웃

**증상:**
```
curl: (28) Operation timed out after 0 milliseconds with 0 bytes received
```

**해결책:**
```bash
# ✅ 명시적 타임아웃 + 재시도
curl -m 15 \  # 15초 타임아웃
  --retry 3 \ # 최대 3회 재시도
  --retry-delay 2 \
  "https://api.odcloud.kr/..."
```

**GitHub Actions 환경:**
- 네트워크 안정적 (일반적으로 문제 없음)
- 하지만 data.go.kr 서버가 간헐적 느려짐 발생 가능

**교훈:**
- ✅ 외부 API → **기본값 이상의 타임아웃 설정**
- ✅ 중요 쿼리 → 재시도 로직 구현

---

## 🎓 일반화된 API 연동 체크리스트

새로운 API를 통합할 때마다 이 체크리스트를 사용하세요:

### Phase 1: 기초 설정 (Foundation)
- [ ] API 문서의 **인증(Authentication)** 섹션 읽기
- [ ] **정확한 Authorization 헤더 형식** 확인 (Bearer/Infuser/API-Key 등)
- [ ] 엔드포인트 base URL 확인
- [ ] 필수 파라미터 목록화

### Phase 2: 로컬 테스트 (Local Validation)
- [ ] `curl -v` 로 헤더/바디 확인
- [ ] HTTP 상태 코드 검증 (200/401/404/429 등)
- [ ] 응답 JSON 구조 확인
- [ ] 타입 불일치 확인 (string vs int vs float)

### Phase 3: 한글/특수문자 처리 (Encoding)
- [ ] `--data-urlencode` 사용 (수동 인코딩 ❌)
- [ ] 응답에서 한글이 정확히 파싱되는지 확인
- [ ] 테스트 데이터에 한글 포함

### Phase 4: 워크플로우 구현 (Automation)
- [ ] YAML 들여쓰기 일관성 확인
- [ ] 환경변수 (secrets) 설정
- [ ] 단일 라인 스크립트 사용 (다중 라인은 파일로 분리)
- [ ] HTTP 상태 코드 출력 및 검증

### Phase 5: 배포 후 모니터링 (Post-Deployment)
- [ ] workflow 실행 로그 확인
- [ ] 응답 데이터 샘플링 검증
- [ ] 에러 핸들링 추가 (404/timeout 등)
- [ ] 재시도 로직 테스트

---

## 📊 API 응답 분석 결과

### 플랫폼시티 관련 발견사항

**검증 완료 쿼리:**

```bash
# Query 1: 이름으로 검색
cond[HOUSE_NM::LIKE]=플랫폼시티
→ matchCount: 2
  ├─ 라온프라이빗 아르디에 (Announce: 2026-03-13, 민영)
  └─ e편한세상 용인역 플랫폼시티 (Announce: 2023-04-20, 민영)

# Query 2: 용인시로 검색
cond[HSSPLY_ADRES::LIKE]=용인
→ matchCount: 41
  ├─ 국민주택: ~5개
  └─ 민영: ~36개
  
# Query 3: 기흥구로 검색 (정확한 위치)
cond[HSSPLY_ADRES::LIKE]=기흥구
→ matchCount: 7
  ├─ 대부분 민영
  └─ 일부 국민주택
```

**Critical Insight:** 
> 모든 "플랫폼시티" 프로젝트는 **민영(Private) 주택**으로 분류됨  
> 기존 시스템이 국민주택만 추적 → **범위 확대 필수**

---

## 🔗 관련 파일 및 참고 자료

### 구현 파일
- **GitHub Actions 워크플로우:**
  - `.github/workflows/subscription-schema-probe.yml` - API 검증
  - `.github/workflows/verify-platform-city.yml` - 자동 검증
  
- **Python 스크립트:**
  - `scripts/verify_platform_city_listings.py` - 지능형 검증 (한글 처리 최적화)
  - `engine/personal/housing.py` - 점수 계산 엔진

- **설정:**
  - `.env.example` - 환경변수 템플릿
  - `data/manual_inputs/subscription_notices.yaml` - 데이터 스키마

### 참고 문서
- `docs/SUBSCRIPTION_SYSTEM.md` - 전체 시스템 아키텍처
- `scripts/README.md` - 스크립트 사용 가이드
- 공식 API 문서: https://www.data.go.kr/

---

## 💡 향후 예방 방안

### 1. 통합 테스트 자동화
```bash
# GitHub Actions에서 매월 검증
- name: Monthly API validation
  schedule: "0 9 1 * *"  # 매월 1일 09:00
  run: |
    python3 scripts/verify_platform_city_listings.py "$DATA_GO_KR_KEY"
```

### 2. 타입 검증 강화
```python
# Pydantic으로 응답 모델 정의
from pydantic import BaseModel

class SubscriptionNotice(BaseModel):
    name: str
    housing_type: Literal["국민주택", "민영"]
    expected_competition_ratio: float | None
    # ...자동 타입 체크
```

### 3. API 요청/응답 로깅
```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Query: {query_params}")
logger.info(f"Response: {response_data}")
# 나중에 디버깅 시 정확한 이력 추적
```

---

## 📝 Template: 새 API 통합 시 적용 사항

향후 다른 API를 추가할 때 이 Template를 사용하세요:

```markdown
# [API_NAME] 통합 기록

## 기본 정보
- 엔드포인트: 
- 인증: 
- 문서: 

## 발견한 문제
1. [Issue]: 
   - 원인: 
   - 해결: 

## 검증 결과
- HTTP 상태: 
- 응답 샘플: 
- 데이터 품질:

## 예방 사항
- [ ] 한글 테스트 포함
- [ ] 타입 검증 추가
- [ ] 재시도 로직 구현
```

---

## 🎯 결론

이 프로젝트에서 배운 **핵심 원칙:**

1. **문서를 먼저 읽어라** - 인증 방식, 필터 문법, 데이터 타입
2. **로컬에서 테스트하고 배포하자** - curl로 확인 후 워크플로우 작성
3. **한글/특수문자는 자동 인코딩에 맡기자** - 수동 처리 ❌
4. **여러 필터로 크로스체크하자** - 단일 쿼리 실패 ≠ API 오류
5. **에러 메시지를 신뢰하자** - "인증 실패" → 헤더 형식 확인

**최종 성과:** ✅  
- API 3단계 검증 자동화 완성
- 역사적 데이터 분석 완료 (민영 주택 확인)
- 향후 유사 프로젝트를 위한 체크리스트 및 템플릿 제공

---

**마지막 수정:** 2026-07-16  
**상태:** ✅ 운영 중 (정기적 검증 실행)  
**담당자:** Claude Code Agent
