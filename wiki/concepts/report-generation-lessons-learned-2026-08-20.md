---
name: report-generation-lessons-learned-2026-08-20
description: 2026-08-20 보고서 생성 세션에서 발견한 문제·원인·해결책 총정리 — Git Bash 실행 불가, UTF-8 인코딩, CXL 언어 누락, 토큰/타임아웃 제한
---

# 보고서 생성 — Lessons Learned (2026-08-20)

## 문제 요약

2026-08-20 세션에서 POET·CXL 양일일 보고서 재생성 과정에서 5가지 핵심 문제가 발견됐다. 각각 환경 제약, 인코딩 버그, 프롬프트 누락, 토큰/타임아웃 부족이 원인이었다.

---

## P1: Git Bash에서 `claude -p` / `claude.cmd` 실행 불가

**현상**: Git Bash 쉘에서 `claude -p`, `claude.cmd`, `claude.exe`를 호출하면
- `claude.exe`: "No such file or directory" (Git Bash가 Windows `.exe`를 직접 실행하지 않음)
- `claude.cmd`: cmd.exe quoting hell으로 인해 argv 파싱 실패
- `.bat` 파일: `@echo`/`REM` 코맨드가 bash에서 파싱 에러 발생

**원인**: Git Bash는 POSIX sh 래퍼이며, Windows 네이티브 실행자(`.exe`, `.cmd`, `.bat`)를 직접 실행할 수 없다. Git Bash에서 실행하면 `which claude`가 npm wrapper 경로를 반환하지만 실제 실행은 실패한다.

**해결**:
- ✅ `run_daily.bat` → **CMD.exe** 또는 **Task Scheduler**에서 실행
- ✅ `run_cxl_daily.bat` → **CMD.exe** 또는 **Task Scheduler**에서 실행
- ✅ `run_cxl_claude_bounded.ps1` → **PowerShell**에서 실행
- ❌ Git Bash에서 `claude -p` 직접 호출 **금지**
- ❌ Git Bash에서 `.bat` 파일 실행 **금지**

**규칙**: Windows 환경에서 headless claude 실행은 **반드시 bat/ps1 wrapper를 통해** 실행. Git Bash는 파일 읽기/쓰기/git 명령만 사용.

---

## P2: UTF-8 인코딩 모자이크 문자 (Mojibake)

**현상**: HTML 보고서에서 `"해석"`, `"SK하이닉스"` 등의 한국어가 `"헁확핔"`, `"늴늴"` 등으로 깨져 표시됨

**원인**:
1. `file://` 프로토콜에서 브라우저는 `<meta charset="utf-8">` 메타 태그를 **무시하고 인코딩을 추론**하는 경우가 있다. 특히 Windows 로컬 파일 열 때.
2. Edit 도구가 파일을 저장할 때 인코딩을 왜곡할 수 있음
3. 실제 파일 인코딩은 UTF-8이지만 (`file -i` 확인 가능), 브라우저가 잘못 해석

**해결**:
```html
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta charset="utf-8">
```
- `<meta http-equiv="Content-Type">`을 `<meta charset>` **앞에** 배치
- HTTP-equivalent 헤더는 브라우저가 인코딩을 반드시 읽도록 강제
- `file://` 프로토콜에서도 동작

**검증**: `file -i <file>`로 파일 인코딩 확인 (text/html; charset=utf-8이어야 함)
**검증**: `grep "깨진글자" <file>`로 모자이크 문자 확인 (0이어야 함)

---

## P3: CXL 보고서 본문 영어 혼합 (Language Null)

**현상**: CXL Daily Update에서 `[변경]`, `[영향]`, `[액션]` 라벨만 한국어일 뿐, 본문 전체가 영어. 한국 사용자로서는 말도 안 되는 혼합 텍스트.

**원인**:
1. `prompts/cxl-daily-update-headless.txt` — 언어 지시 **전혀 없음**
2. `.claude/prompts/cxl-daily-update.md` (시스템 프롬프트) — 역할 섹션에 언어 지시 **없음**
3. 헤드리스 에이전트가 언어 컨텍스트를 추론하지 못하고 영어로 생성

**해결**: 두 프롬프트 모두에 한국어 출력 지시 추가.

**적용 파일**:
- `prompts/cxl-daily-update-headless.txt` — 첫 줄에 "**반드시 모든 본문 출력을 한국어로 작성할 것**"
- `.claude/prompts/cxl-daily-update.md` — 역할 섹션에 "**모든 본문 출력을 한국어로 작성할 것**"

**주의**: 프롬프트에 언어 지시가 없으면 헤드리스 에이전트는 **언어를 추론하지 않는다**. 명시적 지시가 필수.

---

## P4: 토큰 부족 (32K → 64K)

**현상**: 보고서가 피상적이고 분석이 얕음. POET은 위키 종합 + SVG 차트 + 8개 섹션, CXL은 12개 카테고리 WebFetch + DRAFT 리라이팅. 모두 32K로는 부족.

**원인**: `.claude/settings.json`의 `CLAUDE_CODE_MAX_OUTPUT_TOKENS: "32000"`이 전체 세션의 토큰 제한. 32K로는 긴 HTML 보고서 + 심층 분석을 동시에 생성하기 벅차다.

**해결**:
```json
{
  "env": {
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "64000"
  }
}
```

**규칙**: 보고서 생성 작업에는 최소 64K 토큰 필요. 단순 쿼리/체크에는 32K로도 충분.

---

## P5: CXL 타임아웃 부족 (25분 → 40분 → 90분)

**현상**: CXL 보고서가 12개 카테고리 WebFetch를 돌리다가 중간에 타임아웃으로 끊김. 25분은 턱없이 부족.

**변천사**:
| 버전 | 타임아웃 | 설명 |
|---|---|---|
| 최초 | 1,500,000ms (25분) | `run_cxl_claude_bounded.ps1` 기본값 |
| 1차 | 2,400,000ms (40분) | `run_cxl_daily.bat` 파라미터로 설정 |
| 2차 | 5,400,000ms (90분) | 12개 카테고리 WebFetch + DRAFT 리라이팅에 충분한 시간 |

**적용 파일**:
- `run_cxl_daily.bat`: `-TimeoutMs 5400000`
- `scripts/run_cxl_claude_bounded.ps1`: 주석 업데이트 + 기본값 유지 (bat에서 오버라이드)

**POET**: bounded wrapper가 없어서 타임아웃 제한 없음 (무한 대기)

---

## 수정 이력 (2026-08-20)

| 파일 | 변경 전 | 변경 후 | 내용 |
|---|---|---|---|
| `.claude/settings.json` | `32000` | `64000` | 토큰 제한 2배 |
| `run_cxl_daily.bat` | `TimeoutMs 2400000` | `TimeoutMs 5400000` | CXL 타임아웃 40→90분 |
| `prompts/cxl-daily-update-headless.txt` | 언어 지시 없음 | 한국어 출력 강제 | CXL 본문 한국어 |
| `.claude/prompts/cxl-daily-update.md` | 언어 지시 없음 | 한국어 출력 강제 | 시스템 프롬프트 한국어 |
| `report/daily-brief-*.html` | `<meta charset>` | `<meta http-equiv>` + `<meta charset>` | UTF-8 모자이크 해결 |
| `Results/poet-daily/daily-brief-*.html` | — | — | 인코딩 fix + x축 확대 + 해석 텍스트 갱신 |
| `Results/cxl-daily/cxl-daily-report-*.html` | `<meta charset>` | `<meta http-equiv>` + `<meta charset>` | UTF-8 모자이크 해결 |
| `Results/peos-daily/2026-*.html` | `<meta charset>` | `<meta http-equiv>` + `<meta charset>` | UTF-8 모자이크 해결 |

---

## 실행 환경 체크리스트 (매 세션)

새 세션에서 보고서를 생성할 때 아래 순서로 실행:

1. **실행 환경 확인**: Git Bash가 아니라 CMD.exe 또는 Task Scheduler에서 실행
2. **settings.json 확인**: `CLAUDE_CODE_MAX_OUTPUT_TOKENS`가 64000인가?
3. **인코딩 확인**: `<meta http-equiv="Content-Type">`가 `<head>` 최상단에 있는가?
4. **프롬프트 언어 확인**: CXL 프롬프트에 한국어 출력 지시가 있는가?
5. **타임아웃 확인**: CXL timeout 5,400,000ms (90분)인가?
6. **실행**: `run_daily.bat` (POET) → `run_cxl_daily.bat` (CXL)

---

## 구조적 교훈

1. **Git Bash는 Windows 네이티브 실행자 실행 불가** — bat/ps1은 cmd/PS에서, Git Bash는 git/파일 읽기만
2. **`file://` 프로토콜에서 브라우저 인코딩 추론은 신뢰 불가** — `http-equiv` 강제
3. **프롬프트에 명시적 언어 지시 없으면 에이전트는 언어를 추론하지 않음**
4. **보고서 생성에는 64K 토큰이 최소** — 32K는 쿼리/체크용
5. **12개 카테고리 WebFetch에는 90분이 최소** — 25분/40분은 턱없이 부족
