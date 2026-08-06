@echo off
REM ============================================================
REM  run_daily.bat - Headless Claude autonomous cycle wrapper (E1)
REM  Task Scheduler name: Steve_Daily_POET (user-set, 2026-08-06)
REM  Flow: git pull -> claude -p (headless, wiki context) -> dispatch
REM  Design: wiki/concepts/headless-claude-autonomous-cycle.md
REM  Prompt: prompts\daily-brief-headless.txt
REM  Task Scheduler: run only when user logged on (OAuth session),
REM                  execution account = current Claude-authed user.
REM
REM  Log: per-run file named Steve_Daily_POET-YYYYMMDD-HHMMSS.log
REM       (date+time 24h, so each run has its own file for error
REM        diagnosis). Plus a pointer file Steve_Daily_POET-latest.log
REM        symlink/copy to the most recent run for quick access.
REM ============================================================

setlocal enabledelayedexpansion

cd /d C:\Users\2053437

set PYTHONIOENCODING=utf-8
chcp 65001 >nul

REM === Build ISO-style timestamp YYYYMMDD-HHMMSS (24h) via PowerShell ===
REM   PowerShell Get-Date is fast and locale-independent. WMIC was too slow
REM   on this LTSC box (hung). Fallback to %date%/%time% if PowerShell missing.
for /f "delims=" %%t in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss" 2^>nul') do set STAMP=%%t
if not defined STAMP (
  set STAMP=%date:~0,4%%date:~5,2%%date:~8,2%-%time:~0,2%%time:~3,2%%time:~6,2%
  set STAMP=!STAMP: =0!
)

set LOG_DIR=C:\Users\2053437\.claude\logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%" >nul 2>&1
set RUN_LOG=%LOG_DIR%\Steve_Daily_POET-%STAMP%.log
set LATEST=%LOG_DIR%\Steve_Daily_POET-latest.log

echo [%STAMP%] === Steve_Daily_POET run start === > "%RUN_LOG%"

echo [%STAMP%] git pull start >> "%RUN_LOG%"
git fetch origin >> "%RUN_LOG%" 2>&1
git checkout claude/ai-agent-impl-002tip >> "%RUN_LOG%" 2>&1

REM === Robust clean-state sequence (root cause fix 2026-08-06) ===
REM Problem 1: "git stash push -u" FAILS on unmerged (conflict) index
REM   -> stash rejected -> pull blocked by "needs merge" -> deadlock (18:42 run).
REM Problem 2: repo root is user home (C:\Users\2053437) with thousands of
REM   untracked files (AppData/Desktop/etc); "stash -u" scans them all -> timeout.
REM Solution: operate ONLY on the two wiki files the headless cycle may touch,
REM   not the whole tree. The headless Claude does not edit wiki remotely
REM   (prompt forbids it), so normally nothing to stash.
REM   1) reset unmerged index for wiki files (keep working tree content)
REM   2) stash ONLY wiki/index.md and wiki/log.md if dirty (no -u, scoped)
REM   3) pull --rebase on a clean index
REM   4) pop the scoped stash back onto the updated branch
REM Force-clean any unmerged/conflict state in the wiki files (keep content).
git reset --mixed HEAD -- wiki/index.md wiki/log.md >> "%RUN_LOG%" 2>&1
REM Stash ONLY the two wiki files if they have changes (scoped, no -u, fast).
git stash push -m "headless-run wiki-stash" -- wiki/index.md wiki/log.md >> "%RUN_LOG%" 2>&1
REM pull --rebase on a clean index.
git pull --rebase origin claude/ai-agent-impl-002tip >> "%RUN_LOG%" 2>&1
if errorlevel 1 (
  echo [%STAMP%] git pull failed - rebase conflict possible >> "%RUN_LOG%"
  echo [%STAMP%] WARNING: headless will run on STALE wiki (recent INGESTs may be missed) >> "%RUN_LOG%"
) else (
  REM Restore stashed wiki edits on top of updated branch (if any were stashed).
  git stash pop >> "%RUN_LOG%" 2>&1
  echo [%STAMP%] git pull ok, stash popped >> "%RUN_LOG%"
)

echo [%STAMP%] claude -p start >> "%RUN_LOG%"
C:\Users\2053437\AppData\Roaming\npm\claude.cmd -p --dangerously-skip-permissions --allowedTools "Read Grep Glob Write Bash(python *) Bash(dispatch.sh)" --disallowedTools "Bash(git commit *) Bash(git push *) Bash(git rebase*) Bash(git reset*)" < prompts\daily-brief-headless.txt >> "%RUN_LOG%" 2>&1
set CLAUDE_EXIT=%errorlevel%
echo [%STAMP%] === Steve_Daily_POET run end (claude exitcode %CLAUDE_EXIT%) === >> "%RUN_LOG%"

REM === Update latest pointer (copy, not symlink — reliable on Windows) ===
copy /y "%RUN_LOG%" "%LATEST%" >nul 2>&1

REM === Retention: keep only the 30 most recent per-run logs ===
for /f "skip=30 eol=: delims=" %%f in ('dir /b /o-d /a-d "%LOG_DIR%\Steve_Daily_POET-*.log" 2^>nul') do del /q "%LOG_DIR%\%%f" 2>nul

endlocal
