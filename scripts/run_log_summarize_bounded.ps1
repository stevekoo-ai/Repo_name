# run_log_summarize_bounded.ps1
# ============================================================
# Bounded-execution wrapper for headless `claude -p` — wiki/log.md
# 당월/직전월 요약 자동 갱신 (3인 하이브리드 Windows 층).
#
# run_cxl_claude_bounded.ps1의 CR1~CR11 검증 패턴을 그대로 차용:
#   CR6: claude.EXE 직접 호출 (claude.cmd shim 안 씀)
#   CR9: `&` call operator + 배열로 argv 전달 (재토큰화 방지)
#   CR10: Get-Content -Encoding UTF8 (한국어 프롬프트 mojibake 방지)
#   CR11: timeout 시 process sweep 안 함 (다른 Agent/live 세션 보호)
#
# 차이점 (CXL 성공 패턴 대비 — 2026-08-07 빈 stdout 원인 수정):
#   - --append-system-prompt-file 추가 (★ 최우선 원인). 성공 패턴 run_cxl은
#     .claude/prompts/cxl-daily-update.md를 system prompt로 주입하는데,
#     사내 GLM 라우팅 환경에서 system prompt 주입이 응답 생성의 실질적
#     트리거. 이 스크립트엔 빠져 있어 rc=0인데 stdout 완전히 비는 현상 발생.
#     → .claude/prompts/log-summarize.md 신규 생성 후 주입.
#   - allowedTools: Write WebFetch 추가 (성공 패턴과 동일화). 요약 섹션
#     신규 생성/갱신에 Write 필요. Edit만 있으면 도구 호출 포기하고 빈 응답.
#   - prompt: prompts/log-summarize-headless.txt (그대로)
#   - timeout: 10분 (요약은 12카테고리 웹스위프보다 훨씬 짧음)
#
# Params:
#   -LogPath     : per-run 로그 파일 [required]
#   -Stamp       : YYYYMMDD-HHMMSS [required]
#   -TimeoutMs   : hard cap [default 600000 = 10분]
# Exit: 0 clean / 1 실패 / 124 timeout / 3 launch 실패
# ============================================================

param(
    [Parameter(Mandatory=$true)] [string] $LogPath,
    [Parameter(Mandatory=$true)] [string] $Stamp,
    [int] $TimeoutMs = 600000
)

$ErrorActionPreference = "Continue"
$WorkDir = "C:\Users\2053437"
$Claude = "$WorkDir\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe"
$Prompt = "$WorkDir\prompts\log-summarize-headless.txt"
# 성공 패턴(run_cxl) 대비 누락된 system prompt — 2026-08-07 빈 stdout 원인 #1.
$SysPrompt = "$WorkDir\.claude\prompts\log-summarize.md"

$OutFile  = "$LogPath.claude.$Stamp.out"
$ErrFile  = "$LogPath.claude.$Stamp.err"

# CR9: 배열 요소 → `&` call이 하나의 argv 토큰으로 전달.
# 성공 패턴(run_cxl)과 동일화: --append-system-prompt-file + Write/WebFetch 추가.
# 요약 갱신: Read/Grep/Glob(아카이브·log.md 읽기) + Write/Edit(log.md 요약 섹션
# 갱신/신규 생성) + WebFetch(필요 시 웹 컨텍스트). git/빌드 명령은 금지.
# 다른 Agent node.exe/interactive 세션 보호(CR11 정신).
$ClaudeArgs = @(
    '-p',
    '--dangerously-skip-permissions',
    '--append-system-prompt-file', $SysPrompt,
    '--allowedTools', 'Read Grep Glob Write Edit WebFetch Bash(python *)',
    '--disallowedTools', 'Bash(git commit *) Bash(git push *) Bash(git rebase*) Bash(git reset*) Bash(git checkout*) Bash(git stash*) Bash(git pull*) Bash(git fetch*)'
)

Add-Content -Path $LogPath -Value "[$Stamp] claude -p (log-summarize) start (bounded, timeout ${TimeoutMs}ms)" -Encoding UTF8

$t0 = Get-Date

$job = Start-Job -ScriptBlock {
    param($Claude, $ClaudeArgs, $PromptPath, $OutFile, $ErrFile, $WorkDir)
    Set-Location $WorkDir
    # CR10: 한국어 프롬프트 UTF-8 강제 읽기 (CP949 mojibake 방지)
    Get-Content -Raw -Encoding UTF8 -Path $PromptPath | & $Claude @ClaudeArgs 2>$ErrFile 1>$OutFile
} -ArgumentList $Claude, $ClaudeArgs, $Prompt, $OutFile, $ErrFile, $WorkDir

if ($null -eq $job) {
    Add-Content -Path $LogPath -Value "[$Stamp] FATAL: Start-Job returned null — claude never started" -Encoding UTF8
    exit 3
}

$done = $job | Wait-Job -Timeout ([int]([math]::Floor($TimeoutMs / 1000)))
$elapsed = ((Get-Date) - $t0).TotalSeconds

function Fold-File($path, $header) {
    if (Test-Path $path) {
        Add-Content -Path $LogPath -Value "[$Stamp] --- $header ---" -Encoding UTF8
        Add-Content -Path $LogPath -Value (Get-Content -Path $path -Raw) -Encoding UTF8
        Remove-Item -Path $path -Force -ErrorAction SilentlyContinue
    }
}

if ($done) {
    $rc = if ($job.State -eq 'Completed') { 0 } else { 1 }
    Fold-File $OutFile "claude stdout"
    Fold-File $ErrFile "claude stderr"
    Add-Content -Path $LogPath -Value "[$Stamp] claude (log-summarize) job $($job.State) (rc=$rc) in $([math]::Round($elapsed,1))s (clean)" -Encoding UTF8
    $job | Remove-Job -Force
    exit $rc
} else {
    Add-Content -Path $LogPath -Value "[$Stamp] claude (log-summarize) TIMEOUT after $([math]::Round($elapsed,1))s — stopping job" -Encoding UTF8
    $job | Stop-Job
    $job | Remove-Job -Force
    # CR11: process sweep 금지. 다른 Agent/live 세션 보호. 고아 node.exe는 차라리 남김.
    Start-Sleep -Milliseconds 300
    Fold-File $OutFile "claude stdout (partial, pre-timeout)"
    Fold-File $ErrFile "claude stderr (partial, pre-timeout)"
    Add-Content -Path $LogPath -Value "[$Stamp] claude stopped; bat will continue (exit 124)" -Encoding UTF8
    exit 124
}
