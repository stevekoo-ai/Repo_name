# 웹 검색 우회 가이드 (사내 vLLM `web_search` 도구 오류 대응)

> **발생 원인**: Claude Code가 `web_search` 도구를 호출할 때 `tool_choice: 'auto'`를 보냈으나 `tools` 배열은 보내지 않음.
> 사내 vLLM/Qwen 서버가 이 파라미터 불일치로 **400 Bad Request**를 반환.
>
> **영향**: Claude Code 세션에서 웹 검색이 아예 작동하지 않음.
>
> **해결**: 로컬 DuckDuckGo 검색 스크립트(`search.py`)를 사용. 사내 서버 의존도 0.
> 보고서·기사 분석에는 **`cxl_fetch_urls.py` 파이프라인**을 사용해 실제 기사 본문까지 확보.

---

## 빠른 시작 (가장 추천 ⭐)

### 일반 검색 — snippet만 필요할 때

```bash
python search.py "검색어"
```

Claude Code에게 검색 요청할 때:

> "로컬의 `python search.py '검색어'`를 실행하고 결과를 바탕으로 답변해줘"

결과가 5개까지 제목·링크·요약으로 반환됩니다.

### 기사 본문 분석 — 보고서·날짜 검증 필요할 때

```bash
python scripts/cxl_fetch_urls.py sources/cxl-daily-raw-YYYY-MM-DD.md
```

이 스크립트는 내부적으로 `search.py` 12개 카테고리 검색 → 각 URL HTML 본문 fetch → MD 변환까지 자동 수행.
`sources/cxl-daily-raw-YYYY-MM-DD.md`에 다음 형식으로 저장:

```
# CXL Daily Raw Data
Generated: 2026-08-21 06:35:00

## Category: cxl-specs
Query: CXL Consortium specification 2026

### [1] Article Title
**URL**: https://...
**Date**: 2026-08-21

# Article Title
Full article body content here...
```

Claude가 실제 기사 본문을 읽고 날짜 검증 → 현재 기사만 사용.

---

## 상세 설명

### 1. `search.py` — DuckDuckGo 검색 스크립트 (기본)

**위치**: `C:\Users\2053437\search.py`

**작동 원리**: DuckDuckGo 직접 검색 — 사내 서버 거치지 않음

**장점**:
- ⚡ 빠름 (2~3초)
- 🔒 외부 의존 없음 (사내 서버 느려도 영향 없음)
- ⚙️ 설정 불필요 (설치 한 번, 그 끝)

**단점**:
- title·URL·snippet(50자)만 반환 → 기사 본문 X
- Claude가 날짜 검증 못 함 → 낡은 기사를 오늘의 뉴스라고 보고할 수 있음
- 단독 사용은 일반 검색에만 적합

**설치**:
```bash
pip install duckduckgo_search
```

### 2. `scripts/cxl_fetch_urls.py` — 검색 + 본문 fetch + MD 변환 (보고서용)

**위치**: `scripts/cxl_fetch_urls.py`

**작동 원리**: DuckDuckGo search → 각 URL HTML fetch → 본문 추출(BeautifulSoup) → MD 변환

**기능**:
- 12개 카테고리 자동 검색 (내부에서 search.py 호출)
- User-Agent spoofing으로 anti-bot 우회
- meta tag에서 기사 **발표일** 자동 추출 (`og:published_time`, `datePublished` 등)
- nav/sidebar/script 제거 → 본문만 추출
- MD 포맷으로 `sources/cxl-daily-raw-YYYY-MM-DD.md`에 저장

**사용법**:
```bash
python scripts/cxl_fetch_urls.py sources/cxl-daily-raw-YYYY-MM-DD.md
python scripts/cxl_fetch_urls.py sources/cxl-daily-raw-YYYY-MM-DD.md "cxl-specs|cxl-devices" "CXL Consortium 2026|CXL memory 2026"
```

**설치**:
```bash
pip install duckduckgo_search requests beautifulsoup4
```

### 3. `scripts/cxl_news_search.py` — 구조화된 DuckDuckGo JSON

**위치**: `scripts/cxl_news_search.py`

**작동 원리**: `search.py`의 wrapper. JSON 출력으로 `cxl_fetch_urls.py`에서 파싱 가능.

**사용법**:
```bash
python scripts/cxl_news_search.py "cxl-specs" "CXL Consortium specification 2026"
```

**출력 형식**:
```json
{"results": [{"title": "...", "url": "https://...", "snippet": "..."}]}
```

### 4. `proxy.py` — 로컬 프록시 서버 (옵션)

**위치**: `C:\Users\2053437\proxy.py`

**작동 원리**: Claude Code ↔ 사내 서버 사이에 끼어 `tool_choice` 파라미터 자동 교정

**장점**:
- Claude Code의 `web_search` 도구 완전 우회 (자동 교정)
- 매번 명령어 없이 web_search가 정상 작동

**단점**:
- ⚠️ 사내 서버 응답이 느리면 타임아웃
- 설정 2단계 필요 (proxy 실행 + envvar 변경)
- 항상 백그라운드에서 실행 중이어야 함

**실행**:
```bash
python proxy.py
set ANTHROPIC_BASE_URL=http://127.0.0.1:8000
claude
```

**언제 사용?**: 사내 서버 응답이 빠를 때만. 보통은 `search.py`가 더 빠르고 안정적.

### 5. `--disallowedTools` CLI 옵션

```bash
claude --disallowedTools web_search,web_fetch "질문"
```

web_search 도구를 아예 차단 — 도구 호출 자체를 하지 못하게 함.
에러 메시지를 줄일 수 있으나 검색 기능 자체도 사라짐.

---

## CLAUDE.md 자동 로드 (자동 적용)

`CLAUDE.md`에 검색 우회 규칙이 이미 추가되어 있습니다.
모든 Claude Code 세션은 세션 시작 시 `CLAUDE.md`를 자동 로드하므로,
**Agent가 web_search를 호출하지 않도록 이미 규칙이 주입되어 있습니다.**

### 새로고침 방법

새로운 세션에서 이 규칙을 즉시 적용하려면:
```bash
claude --append-system-prompt "web_search를 절대 사용하지 마. python search.py '검색어'를 대신 사용해."
```

또는 세션 시작 시 첫 메시지로:
> "CLAUDE.md의 검색 우회 규칙을 따르고, 검색이 필요하면 python search.py를 사용해."

---

## 비교 표

| 방법 | 속도 | 설정 비용 | 자동성 | 안정성 | 권장도 |
|---|---|---|---|---|---|
| `cxl_fetch_urls.py` | ⏱️ 5~10분 | 없음 | ⭐ 자동 | 높음 | ⭐⭐⭐ (보고서) |
| `search.py` | ⚡ 빠름 | 없음 | ⚠️ 수동 | 높음 | ⭐⭐⭐ (일반) |
| `cxl_news_search.py` | ⚡ 빠름 | 없음 | ⚠️ 수동 | 높음 | ⭐⭐ (개발용) |
| `proxy.py` | ⚠️ 사내서버 의존 | 높음 | ⭐ 자동 | 중간 | ⭐⭐ |
| `--disallowedTools` | N/A | 낮음 | ⭐ 차단 | 높음 | ⭐ |

---

## FAQ

**Q: web_search를 계속 쓸 수 있는 방법은 없나요?**
A: 사내 vLLM 서버 측에서 `tool_choice`/`tools` 파라미터 불일치를 수정해야 합니다.
로컬에서는 `proxy.py`로 완전히 우회 가능하나 사내 서버 응답 속도에 의존합니다.

**Q: search.py가 실행되지 않는데?**
A: `pip install duckduckgo_search`를 먼저 실행하세요.

**Q: 검색 결과가 영어만 나와요.**
A: 검색어를 한국어로 입력하세요. DuckDuckGo는 언어를 감지합니다.

---

**생성일**: 2026-08-21
**검증**: search.py 테스트 완료 (DuckDuckGo 정상 응답), proxy.py 테스트 완료 (Health check OK, 사내서버 응답 느림)
