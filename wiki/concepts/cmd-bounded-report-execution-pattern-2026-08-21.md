---
name: cmd-bounded-report-execution-pattern-2026-08-21
description: bat/PS wrapper 기반 보고서 자동화 — CMD 실시간 출력, search.py 기반 검색, --model alias, bat/PS 인코딩 주의
---

# bat/PS wrapper 기반 보고서 자동화 패턴 (2026-08-21)

## 문제 요약

2026-08-21 세션에서 POET/CXL 보고서 자동화 파이프라인이 여러 이유로 연속 실패했다. bat/PS wrapper 기반 실행에서 9가지 핵심 문제를 발견·해결했다. 특히 **bat 실행 시 CMD 창이 공백 → 사용자 진행状況 확인 불가**가 가장 큰 UX 문제였다.

---

## P1: bat 파일 내 한글 → CMD 파싱 에러

**현상**: bat 파일에 한글이 있으면 CMD가 bat 구문을 잘못 파싱하여
`'은(는) 내부 또는 외부 명령...'` 에러 발생

**원인**: bat 파일 자체가 UTF-8로 저장되어 있어, CMD 파서가 bat 파싱 시 인코딩 충돌 발생. `chcp 65001` 설정이 있어도 bat 파일 내 모든 줄이 인코딩의 영향을 받음.

**해결**: bat 파일의 **모든 줄(주석 포함)을 ASCII 영문으로** 작성. 한국어는 PS wrapper의 `Write-Host`에서만 사용 (PS가 UTF-8을 직접 처리하므로 깨지지 않음).

**규칙**: bat 파일은 ASCII만. PS wrapper에서 `Write-Host`는 한글 지원됨.

---

## P2: bat 파일 `if ... else` 블록에서 nested 에러

**현상**: bat 파일에서 `if ... (if ... else ...)` 같은 중첩 `if/else`가 CMD 파싱 에러를 일으킴.

**원인**: CMD bat 파서는 중첩 `if/else`에서 `)` 매칭이 불명확해지거나, 특정 인코딩 조합에서 괄호를 인식하지 못함.

**해결**: `goto :LABEL` 패턴으로 flat 구조 사용.

```bat
if %RC% equ 0 goto :SUCCESS
if %RC% equ 124 goto :TIMEOUT
goto :FAIL

:SUCCESS
echo OK
goto :DONE

:TIMEOUT
echo TIMEOUT
goto :DONE

:FAIL
echo FAIL

:DONE
```

**규칙**: bat에서 `if/else`는 flat 구조. 중첩 금지.

---

## P3: bat 파일 실행 시 CMD 창 바로 닫힘

**현상**: Explorer에서 bat double-click 시 CMD 창이 떴다가 바로 사라짐. 실행 결과를 볼 수 없음.

**원인**: bat 실행이 끝나면 CMD 창이 자동으로 닫힘.

**해결**: bat 파일 마지막에 `pause` 추가.

```bat
endlocal
pause
exit /b 0
```

**주의**: `pause`는 Task Scheduler 실행 시 `pause`가 진행 대기하므로 Task Scheduler용 bat에는 `pause` 금지. **반드시 수동 실행용인지 자동 실행인지 구분**.

---

## P4: PS wrapper stdout이 CMD에 안 보임 (가장 중요한 UX 개선)

**현상**: `claude -p`가 실행 중이지만 CMD 창에 아무것도 안 보임. 완전히 멈춘 것 같음.

**원인**: 기존 구조에서 claude stdout을 **sidecar 파일에 저장**하고, job이 완료된 후에만 `Fold-File`로 log에 fold. 실행 중인 동안 CMD 창에 출력 없음.

**해결**: PS wrapper에서 sidecar 파일을 **5초마다 폴링**하여 새로운 내용을 CMD 창에 실시간 출력.

```powershell
$lastOutputLength = 0
while ($true) {
    # poll sidecar for new content
    if (Test-Path $OutFile) {
        $currentContent = Get-Content -Path $OutFile -Raw
        if ($currentContent.Length -gt $lastOutputLength) {
            Write-Output $currentContent.Substring($lastOutputLength)
            $lastOutputLength = $currentContent.Length
        }
    }
    # heartbeat: if no new output for 30s
    ...
    Start-Sleep -Seconds 5
}
```

**규칙**: 모든 bounded wrapper는 **stdout 실시간 CMD 출력** 필수. `Write-Output` 사용 (PS의 `Write-Host`는 CMD 인코딩과 호환 안 됨).

---

## P5: PS heartbeat 주기 단축

**현상**: heartbeat 주기가 120초로 너무 길어, 사용자가 실행 중인지 확인 불가.

**해결**: 30초로 단축. claude 출력이 있을 때는 heartbeat 타이머 리셋 → claude가 활동 중이면 heartbeat 없이 stdout만 표시.

```powershell
if (new output detected) {
    $lastHeartbeatTime = Get-Date  # reset
}
if ((Get-Date - $lastHeartbeatTime).TotalSeconds -ge 30) {
    Write-Output "[heartbeat] X min elapsed, still running..."
    $lastHeartbeatTime = Get-Date
}
```

**규칙**: heartbeat는 30초 간격. claude 활동 중에는 heartbeat 없이 stdout만 표시.

---

## P6: API 400 Bad Request — 모델명 불일치

**현상**: `claude -p` 실행 시 `API Error: 400: Invalid model name provided in model=Qwen3.6-35B-A3B`

**원인**: `claude -p`가 settings.json의 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 값(`Qwen3.6-35B-A3B`)을 **직접 모델명으로** API에 보냄. 사내 vLLM 서버는 이 문자열을 인식하지 못해 400 에러.

**해결**: `claude -p`에 `--model haiku` alias를 명시적으로 전달. 서버가 alias를 올바른 모델명으로 변환.

```powershell
$ClaudeArgs = @(
    '-p',
    '--model', 'haiku',  # alias 사용, 직접 모델명 아님
    ...
)
```

**규칙**: `claude -p` 실행 시 항상 `--model` alias 명시. 직접 모델명(`Qwen3.6-35B-A3B`) 금지.

---

## P7: WebFetch/WebSearch 작동 안 함 (사내 vLLM 제한)

**현상**: claude -p가 WebFetch 또는 WebSearch 도구를 호출하면 사내 vLLM 서버에서 400 에러 발생.

**원인**: 사내 vLLM의 `tool_choice` 파라미터 불일치. `claude -p`는 CLI 옵션으로 도구를 제한하지만, vLLM이 `tools`/`tool_choice` 배열을 일치시키지 못함.

**해결**: `python search.py`로 대체. DuckDuckGo 직접 검색, 사내 서버 의존도 0.

```powershell
# allowedTools에서 WebFetch/WebSearch 차단
'--allowedTools', 'Read Grep Glob Write Edit Bash(python search.py *)'
'--disallowedTools', 'WebSearch WebFetch Bash(dispatch.sh)'
```

**headless prompt**: "12개 카테고리 search.py 검색, 순차적 실행"으로 명시.

**규칙**: 사내 vLLM 환경에서는 WebSearch/WebFetch 금지. `python search.py`만 사용.

---

## P8: search.py 기반 검색 — 병렬 금지

**현상**: CXL 12개 카테고리 검색 시 12개 프로세스 동시 실행 → 메모리 과부하 → 메모리 부족 에러.

**원인**: `python search.py`가 DuckDuckGo API 호출로 외부 네트워크 접근. 병렬 실행 시 메모리 누수/과부하 발생.

**해결**: headless prompt에 **"모든 search.py 호출 순차적"** 명시. 각 카테고리별 3개 검색어 → 36회 순차 실행.

**규칙**: `python search.py`는 **순차적 실행**만 허용. 병렬 금지.

---

## P9: PS wrapper Write-Output UTF-8 모자이크 문자 (2026-08-21 추가)

**현상**: bat 실행 시 CMD 창에 `CXL Daily Update COMPLETED` 메시지 등에서 한글이 `???` 또는 깨진 문자로 표시됨.

**원인**: `Write-Output`이 시스템 기본 인코딩(cp949)으로 출력을 변환. PS에서 UTF-8 클린텍스트를 읽어서 cp949로 잘못 변환 → 모자이크.

**해결**: PS 스크립트 시작 시 **`[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`** 명시. CMD가 UTF-8로 해석하도록 강제.

```powershell
# Must be at the VERY TOP of the PS script, before any Write-Output
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

**규칙**: 모든 PS wrapper는 시작 라인에 `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` 필수. `Write-Output`이 깨지면 이 줄이 누락된 것임.

---

## 최종 실행 아키텍처 (2026-08-21 현재)

### CXL
```
run_cxl_daily.bat (CMD, ASCII만)
  ├── [1/2] git fetch + pull --rebase (wiki sync, stash-protected)
  └── [2/2] claude -p via run_cxl_claude_bounded.ps1 (PowerShell)
        ├── [Console]::OutputEncoding = UTF8 (P9 fix)
        ├── --model haiku (alias — API 400 방지)
        ├── allowedTools: Bash(python search.py *)  (WebFetch 차단)
        ├── stdout: sidecar 5초 폴링 → CMD 실시간 출력
        ├── heartbeat: 30초 주기 (activity 기반 리셋)
        └── 완료: CMD 창에 큰 박스 + 한글 메시지 (PS Write-Host)
```

### POET (4-phase split)
```
run_daily.bat (CMD, ASCII만)
  ├── [0/4] git fetch + pull --rebase
  ├── [1/4] python poet_phase1_extract.py → poet-macro.json
  ├── [2/4] python poet_phase2_extract.py → poet-hynix.json
  ├── [3/4] python poet_phase3_extract.py → poet-decisions.json
  └── [4/4] claude -p via run_poet_claude_bounded.ps1
        ├── [Console]::OutputEncoding = UTF8 (P9 fix)
        ├── --model haiku (alias — API 400 방지)
        ├── allowedTools: Read Grep Glob Write Edit Bash(python *)
        ├── stdout: sidecar 5초 폴링 → CMD 실시간 출력
        └── 완료: CMD 창에 큰 박스 메시지
```

## 수정 파일

| 파일 | 변경 |
|---|---|
| `.claude/prompts/cxl-daily-update.md` | WebFetch/WebSearch 금지, search.py 전환 |
| `prompts/cxl-daily-update-headless.txt` | 12개 카테고리 search.py 순차 실행 절차 |
| `scripts/run_cxl_claude_bounded.ps1` | 실시간 stdout 출력, `--model haiku`, search.py allowedTools, ASCII 영문화, [Console]::OutputEncoding UTF8 |
| `run_cxl_daily.bat` | ASCII 영문화, goto 라벨 flat 구조, pause 추가, 완료 메시지 |
| `scripts/run_poet_claude_bounded.ps1` | CXL wrapper clone, parameterized (prompt/sysprompt/allowedTools), [Console]::OutputEncoding UTF8 |
| `run_daily.bat` | ASCII 영문화, goto 라벨 flat 구조, pause 추가 |
| `prompts/poet-phase4-headless.txt` | docs/index.html Read 금지 지시 |

---

## 구조적 교훈

1. **bat 파일은 ASCII만** — 한글은 PS wrapper에서 처리
2. **bat `if/else`는 flat 구조** — 중첩 금지 (goto 라벨 패턴 사용)
3. **bat double-click 시 `pause` 추가** — CMD 창 유지
4. **claude stdout 실시간 CMD 출력 필수** — sidecar 5초 폴링
5. **heartbeat 30초 주기** — claude 활동 중에는 리셋
6. **`--model haiku` alias 명시** — 직접 모델명 금지 (400 에러)
7. **WebSearch/WebFetch 금지** — `python search.py`만 사용
8. **search.py 순차 실행** — 병렬 금지 (메모리 안전)
9. **PS wrapper 시작 라인에 `[Console]::OutputEncoding = UTF8` 필수** — Write-Output 모자이크 방지

---

## 관련 문서

- [report-generation-lessons-learned-2026-08-20](report-generation-lessons-learned-2026-08-20.md) — 이전 세션 (인코딩, 언어, 토큰/타임아웃)
- [web-search-workaround.md](../tools/web-search-workaround.md) — 사내 vLLM web_search 우회 가이드
- [automation-strategy-and-delivery-boundary.md](automation-strategy-and-delivery-boundary.md) — 트랙 A/B 경계
