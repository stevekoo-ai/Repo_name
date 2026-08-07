# run_cxl_claude_bounded.ps1
# ============================================================
# Bounded-execution wrapper for headless `claude -p` in
# scripts/cxl_daily_routine.bat — CXL Daily Update 자동 생성용.
#
# Why this exists: the old `claude.cmd -p "inline string"` call hung
# (node doesn't exit -> bat blocks). Same root cause as the SK-hynix
# daily-brief wrapper (run_claude_bounded.ps1); same fix lineage.
#
# === 2026-08-07 fixes (CR4-CR9, ported from run_claude_bounded.ps1
#     where they were verified end-to-end) ===
#  CR4 (FATAL): -NoNewWindow + -WindowStyle CANNOT be combined —
#      Start-Process throws InvalidOperationException, $proc null,
#      WaitForExit throws "InvokeMethodOnNull", script falls through to
#      a bogus "TIMEOUT after 0.7s". This is why the CXL routine NEVER
#      ran successfully. Fix: -NoNewWindow only + null guard.
#  CR6 (FATAL): launch claude.EXE directly, not the claude.cmd shim.
#      The shim + cmd.exe /c + nested quotes broke argv parsing.
#  CR5/CR7 (FATAL): Start-Process -ArgumentList re-tokenizes array
#      elements on whitespace, so `Bash(git commit *)` arrived as three
#      argv tokens -> bogus "deny rule Bash(git matches no known tool".
#  CR9 (FIX): use the `&` CALL OPERATOR with an array inside Start-Job.
#      `&` hands each array element to the native .exe as ONE argv token
#      without re-tokenizing — verified: zero rule-parse warnings in the
#      SK-hynix probe. Start-Job gives Wait-Job -Timeout for the hard cap.
#      stdin piped from the prompt file inside the scriptblock; output
#      redirected to sidecar files via PS redirection. On timeout we
#      Stop-Job AND sweep orphaned claude.exe/node.exe by command-line
#      match (Stop-Job alone doesn't kill the spawned child).
#
# CXL-specific differences from run_claude_bounded.ps1:
#   - prompt file: prompts/cxl-daily-update-headless.txt
#   - system-prompt append: .claude/prompts/cxl-daily-update.md via
#     --append-system-prompt-file (CXL 12-category procedure)
#   - allowedTools: includes WebFetch (web research) + Edit (DRAFT
#     reflect) + Glob/Grep (wiki navigation)
#   - timeout: 25 min (CXL 12-category WebFetch sweep is much longer)
#
# Params:
#   -LogPath     : per-run log file (append progress lines here)  [required]
#   -Stamp       : YYYYMMDD-HHMMSS stamp for log lines            [required]
#   -TimeoutMs   : hard cap in milliseconds                       [default 1500000 = 25 min]
#
# Exit codes: 0 on clean completion, 1 on job failure, 124 on timeout (convention), 3 on launch failure.
# ============================================================

param(
    [Parameter(Mandatory=$true)] [string] $LogPath,
    [Parameter(Mandatory=$true)] [string] $Stamp,
    [int] $TimeoutMs = 1500000
)

$ErrorActionPreference = "Continue"
$WorkDir = "C:\Users\2053437"
# CR6: claude.exe directly, not the claude.cmd shim (avoids cmd quoting hell).
$Claude = "$WorkDir\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe"
$Prompt = "$WorkDir\prompts\cxl-daily-update-headless.txt"
$SysPrompt = "$WorkDir\.claude\prompts\cxl-daily-update.md"

# CR1/CR2 sidecar outputs (separate .out/.err, folded into LogPath here).
$OutFile  = "$LogPath.claude.$Stamp.out"
$ErrFile  = "$LogPath.claude.$Stamp.err"

# CR9: args as a STRING ARRAY. Each element -> one argv token via `&` call.
# No quoting needed; `&` does not re-tokenize array elements on whitespace.
# CXL needs WebFetch (12-category web research) + Edit (DRAFT reflect) +
# Glob/Grep (wiki navigation) + Read/Write/Bash. git commit/push/rebase/reset denied.
$ClaudeArgs = @(
    '-p',
    '--dangerously-skip-permissions',
    '--append-system-prompt-file', $SysPrompt,
    '--allowedTools', 'Read Grep Glob Write Edit WebFetch Bash(python *) Bash(dispatch.sh)',
    '--disallowedTools', 'Bash(git commit *) Bash(git push *) Bash(git rebase*) Bash(git reset*)'
)

Add-Content -Path $LogPath -Value "[$Stamp] claude -p (CXL) start (bounded via & call + Start-Job, timeout ${TimeoutMs}ms)" -Encoding UTF8

$t0 = Get-Date

# CR9: run `& $Claude @ClaudeArgs` inside a job. Pass variables by -ArgumentList
# so the isolated job runspace can see them. stdin piped from the prompt file;
# stdout/stderr go to sidecar files via PS redirection.
$job = Start-Job -ScriptBlock {
    param($Claude, $ClaudeArgs, $PromptPath, $OutFile, $ErrFile, $WorkDir)
    Set-Location $WorkDir
    # CR10 (2026-08-07, FATAL): Get-Content without -Encoding UTF8 read the
    # Korean prompt as the system code page (CP949) -> mojibake -> claude saw
    # "corrupted text" and refused to act (verified: SK-hynix probe stderr
    # showed claude complaining about garbled Korean). Prompt files are
    # BOMless UTF-8, so read them as UTF8 explicitly.
    Get-Content -Raw -Encoding UTF8 -Path $PromptPath | & $Claude @ClaudeArgs 2>$ErrFile 1>$OutFile
} -ArgumentList $Claude, $ClaudeArgs, $Prompt, $OutFile, $ErrFile, $WorkDir

if ($null -eq $job) {
    Add-Content -Path $LogPath -Value "[$Stamp] FATAL: Start-Job returned null — claude never started" -Encoding UTF8
    exit 3
}

# Wait-Job -Timeout returns the job if completed in time, $null otherwise.
$done = $job | Wait-Job -Timeout ([int]([math]::Floor($TimeoutMs / 1000)))
$elapsed = ((Get-Date) - $t0).TotalSeconds

# Fold the sidecar outputs into the run log regardless of outcome.
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
    Add-Content -Path $LogPath -Value "[$Stamp] claude (CXL) job $($job.State) (rc=$rc) in $([math]::Round($elapsed,1))s (clean)" -Encoding UTF8
    $job | Remove-Job -Force
    exit $rc
} else {
    # Timeout — Stop-Job stops the PS job, but the child claude.exe/node.exe
    # it spawned may survive. Sweep by command-line match (CR3 idea).
    Add-Content -Path $LogPath -Value "[$Stamp] claude (CXL) TIMEOUT after $([math]::Round($elapsed,1))s — stopping job" -Encoding UTF8
    $job | Stop-Job
    $job | Remove-Job -Force
    # CR11 (2026-08-07, FATAL): process sweep REMOVED. The old belt-and-suspenders
    # sweep matched any claude.exe/node.exe whose command line contained 'claude'
    # — that caught THIS user's live interactive claude Code session AND any other
    # agent's node.exe mid-work, taskkill /F'd them, and killed the whole window.
    # Verified root cause of "running this makes the claude window exit". Stop-Job
    # alone may leave an orphaned headless child claude.exe/node.exe, but that is
    # strictly safer than killing other work. Do NOT re-add a process sweep here.
    Start-Sleep -Milliseconds 300
    Fold-File $OutFile "claude stdout (partial, pre-timeout)"
    Fold-File $ErrFile "claude stderr (partial, pre-timeout)"
    Add-Content -Path $LogPath -Value "[$Stamp] claude (CXL) stopped; bat will continue (exit 124)" -Encoding UTF8
    exit 124
}
