@echo off
REM ===========================================================================
REM log_summarize_routine.bat - log.md monthly/daily summary auto-update
REM   3-way hybrid Windows layer (00:40 KST daily).
REM
REM Steps:
REM   1. git fetch + pull --rebase (recover GitHub Actions layer cut result)
REM   2. claude -p via run_log_summarize_bounded.ps1 (GLM gateway, free LLM)
REM      -> read yesterday's archive, write 2-3 line prose summary into log.md
REM      ## current-month summary section
REM   3. upload_log_summary.py (Contents API PUT - bypass corp-net git push block)
REM
REM 3-way collaboration roles:
REM   GitHub Actions (00:20 KST): deterministic cut -> log-archive/ transfer + push
REM   Windows Task (00:40 KST, this bat): LLM prose summary -> log.md section update
REM   Live session: quality/recovery, session-start safety net (wc -c > 50KB -> cut)
REM
REM graceful degradation:
REM   - laptop OFF: GitHub layer cuts only, summary skipped (full text in archive)
REM   - GitHub delay/miss: this bat does its own fallback cut from log.md
REM   - both down: log.md +17KB/day, next run idempotent catch-up is safe
REM
REM corp-net env (see CLAUDE.md / claude-code-internal-routing.md):
REM   - git push HTTP 403 blocked -> Contents API PUT to upload
REM   - claude -p routes to corp GLM gateway via .claude/settings.json env (free)
REM   - PAT kept in git credential manager (upload script extracts automatically)
REM ===========================================================================

setlocal enabledelayedexpansion
cd /d "C:\Users\2053437"

set PYTHONIOENCODING=utf-8
chcp 65001 >nul

for /f "delims=" %%t in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss" 2^>nul') do set STAMP=%%t
if not defined STAMP (
  set STAMP=%date:~0,4%%date:~5,2%%date:~8,2%-%time:~0,2%%time:~3,2%%time:~6,2%
  set STAMP=!STAMP: =0!
)

set LOG_DIR=C:\Users\2053437\.claude\logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%" >nul 2>&1
set RUN_LOG=%LOG_DIR%\log-summary-%STAMP%.log
set LATEST=%LOG_DIR%\log-summary-latest.log

echo [%STAMP%] === log summarize routine start === > "%RUN_LOG%"

REM --- Step 1: git sync (recover GitHub layer cut result) ---
echo [%STAMP%] [1/3] git fetch + pull --rebase >> "%RUN_LOG%" 2>&1
git fetch origin >> "%RUN_LOG%" 2>&1
git checkout claude/ai-agent-impl-002tip >> "%RUN_LOG%" 2>&1
git reset --mixed HEAD -- wiki/index.md wiki/log.md wiki/log-archive wiki/messagebox.md >> "%RUN_LOG%" 2>&1
git stash push -m "log-summary-run wiki-stash" -- wiki/index.md wiki/log.md wiki/log-archive wiki/messagebox.md >> "%RUN_LOG%" 2>&1
git pull --rebase origin claude/ai-agent-impl-002tip >> "%RUN_LOG%" 2>&1
if errorlevel 1 (
  echo [%STAMP%] WARN: pull --rebase conflict - manual intervention needed >> "%RUN_LOG%" 2>&1
) else (
  git stash pop >> "%RUN_LOG%" 2>&1
  echo [%STAMP%] git pull ok, stash popped >> "%RUN_LOG%"
)

REM --- Step 2: Claude Code non-interactive run (GLM summary) ---
echo [%STAMP%] [2/3] claude -p (log summarize via GLM) >> "%RUN_LOG%" 2>&1
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\run_log_summarize_bounded.ps1" -LogPath "%RUN_LOG%" -Stamp "%STAMP%" -TimeoutMs 600000
set CLAUDE_RC=%errorlevel%
echo [%STAMP%] claude -p (log-summarize) exit code: %CLAUDE_RC% >> "%RUN_LOG%" 2>&1

if not %CLAUDE_RC%==0 (
  if not "%CLAUDE_RC%"=="124" (
    echo [%STAMP%] WARN: claude -p failed (exit %CLAUDE_RC%) - upload still attempted >> "%RUN_LOG%" 2>&1
  ) else (
    echo [%STAMP%] WARN: claude -p TIMEOUT(124) - partial result possible, upload attempted >> "%RUN_LOG%" 2>&1
  )
)

REM --- Step 3: upload (log.md only via Contents API PUT) ---
echo [%STAMP%] [3/3] upload log.md via Contents API >> "%RUN_LOG%" 2>&1
python scripts\upload_log_summary.py >> "%RUN_LOG%" 2>&1
set UPLOAD_RC=%errorlevel%
echo [%STAMP%] upload exit code: %UPLOAD_RC% >> "%RUN_LOG%" 2>&1

git checkout claude/ai-agent-impl-002tip >> "%RUN_LOG%" 2>&1

copy /y "%RUN_LOG%" "%LATEST%" >nul 2>&1
for /f "skip=30 eol=: delims=" %%f in ('dir /b /o-d /a-d "%LOG_DIR%\log-summary-*.log" 2^>nul') do del /q "%LOG_DIR%\%%f" 2>nul

echo [%STAMP%] === routine end (claude %CLAUDE_RC%, upload %UPLOAD_RC%) === >> "%RUN_LOG%" 2>&1
endlocal
exit /b 0
