---
name: cxl-newsroom-search-methodology
description: CXL Newsroom 수집을 위한 검색 방법론 — Bing RSS가 유일한 신뢰할 수 있는 채널, 한국어 기업은 반드시 한글 쿼리 사용
metadata:
  type: reference
---

# CXL Newsroom 수집 방법론 — 검색 전략

## 검색 채널 계층 (위에서 아래로 신뢰도 순)

### Tier 1: Bing RSS (가장 신뢰성 높음)
```
https://www.bing.com/news/search?q=[기업명]&form=NWSCNW
```
- **장점:** bot 차단 우회, JavaScript 불필요, 로그인 불필요
- **단점:** WebSearch API는 고장 상태
- **핵심 규칙:** **한국 기업은 반드시 한글 쿼리**, 영어 기업은 영문 쿼리
  - `삼성전자 2026 반도체` → 12건 확보 (인덱스 완벽)
  - `Neosem semiconductor` → 0건 (인덱스 없음)
  - `네오셈 2026` → 7건 확보 (국내 언론 인덱스)
- **이중 검색:** 기업명 + 영어명 + 연도 조합으로 교차 검증

### Tier 2: IR 페이지 직접 접근 (WebFetch)
```
https://ir.[company].com/news-events/press-releases
https://newsroom.[company].com/news-releases
https://investors.[company].com/news-releases
```
- 성공 기업: Intel, Microchip, Marvell, Synopsys, Micron, Panmnesia, OpenEdge
- 실패 기업: AWS(403), Alibaba(403), Samsung(timeout), Micron(timeout), Penguin(403), Exicon(403)

### Tier 3: PR Newswire / Globenewswire
```
https://www.prnewswire.com/news-search/[기업명]
https://www.globenewswire.com/SearchResult?q=[기업명]
```
- 실패 다수: Globenewswire 404, PRNewswire 404
- 성공: NVIDIA 일부, Cadence 일부

## 접근 불가 기업과 대체채널 매핑

| 기업 | WebFetch 실패 | Bing RSS 결과 |
|---|---|---|
| AWS | 403 | 10건 확보 (Q2 2026 $42.2B) |
| Alibaba | 403 | 9건 확보 (AI DC 100일 구축) |
| Samsung | timeout | 12건 확보 (세이프포럼2026, FMS 2026) |
| Micron | timeout | 8건 확보 (HBM4 공급망, 메모리 공급부족) |
| Cadence | timeout | 9건 확보 (2026 forecast $6.34B, AuraStack) |
| Penguin | 403 | 7건 확보 (Q3 2026 실적, CXL 확장) |
| Exicon | 403 | 3건 확보 (삼성 498억 공급계약) |
| Neosem | 0건 | 7건 확보 (수주공시 66.7억) |

## 절대 실패하는 채널

- **Naver search:** `Claude Code is unable to fetch from search.naver.com` — 명시적 차단
- **Google search:** redirect만 하고 내용 없음, 일부는 검색 차단 메시지
- **Yahoo search:** Google으로 redirect, 내용 없음
- **DART API:** 한국 비상장 기업만 (DART_API_KEY 필요)

## 30개사 분류 (수집 성공률 기준)

### 완전 확보 (27개사 — Bing RSS로 headline 확보)
- Host: NVIDIA, AMD, Intel, Microsoft, Google, Meta, Qualcomm, AWS, Alibaba (9/9)
- Controller: Montage, Marvell, Panmnesia, Microchip, Astera, Primemas, XConn (7/7)
- IP/EDA: Synopsys, Cadence, Rambus, OpenEdge, Qualitas (5/5)
- Memory: Samsung, SK hynix, Micron, Penguin (4/4)
- SW: MemVerge, H3 Platform (2/2)
- PCB: Neosem, Exicon, TLB (3/3)

### 존재 자체 확인 불가 (3개사)
- FADU — 도메인 404
- EEUM — 도메인 미확정
- Qualitas — 검색 인덱스 없음

## 주요 실수 기록 (반복 금지)

1. **❌ English-only 검색:** "한국 기업은 검색 인덱스가 없어서 0건" — 이건 영어 쿼리만으로 검색했기 때문. 한글 쿼리하면 국내 언론 인덱스가 나옴.
2. **❌ "접근불가"로 조기 단정:** IR 페이지 403/timeout 뜨면 거기서 멈춤. Bing RSS는 완전히 다른 채널.
3. **❌ Bing RSS를 대체채널로 간주:** Bing RSS가 유일한 대체채널이자 가장 신뢰할 수 있는 채널.

## 다음 세션 시작 전 체크리스트

1. WebSearch API 상태 확인 (여전히 고장일 수 있음)
2. Bing RSS로 검색할 때:
   - 한국어 기업명 → 한글 쿼리
   - 영문 기업명 → 영문 쿼리
   - 연도("2026") 추가하여 최근 결과 제한
   - 0건 뜨면 키워드 변형 재시도 (예: `네오셈` → `네오셈 수주` → `네오셈 반도체`)
3. Tier 1(Bing RSS)으로 다 시도한 후 → Tier 2(IR 직접) → Tier 3(PR) 순서
