# run_claude_bounded.ps1
# ============================================================
# Bounded-execution wrapper for headless `claude -p` in run_daily.bat
# (and any sibling .bat that runs headless claude — cxl_daily_routine.bat).
#
# Why this exists: `type prompt | claude.cmd -p ...` (and `< file`)
# in the bat hangs in practice — claude -p emits its final text but the
# node process does not exit, so the bat blocks at the pipe forever
# (verified: two real run logs 20260806-202040 / -210311 both end at the
# claude output line, the bat's "run end" marker never executes). Killing
# claude then takes the terminal with it (process-group propagation).
#
# Fix: launch claude with a hard timeout via Start-Process -PassThru +
# WaitForExit($ms). On timeout, tree-kill the whole claude.cmd -> node
# subtree. Control ALWAYS returns to the bat so its trailing lines
# (run-end marker, latest pointer, retention) run.
#
# stdin is fed from a FILE via -RedirectStandardInput (no pipe / `type`),
# which is the documented Start-Process mechanism and avoids the pipe
# that caused the original hang.
#
# === Code-review fixes (2026-08-06) ===
#  CR1 (FATAL) stdout+stderr pointed at the SAME file under Start-Process
#      -> one stream's open fails / output is dropped. Now stderr is
#      redirected to a SEPARATE .err file; both are folded into the run
#      log afterward by the caller (run_daily.bat) so nothing is lost.
#  CR2 (FATAL) the bat appended the PS wrapper's own stdout to RUN_LOG
#      with `>> %RUN_LOG%` WHILE this script wrote claude's stdout to the
#      same RUN_LOG via -RedirectStandardOutput -> two writers on one
#      file, interleaved/lost. Now -RedirectStandard* targets the
#      wrapper's OWN sidecar logs, and the wrapper's own progress lines
#      go through Add-Content. The caller must NOT `>> %RUN_LOG%` on the
#      powershell invocation line (see run_daily.bat comment).
#  CR3 (MAJOR) $proc.Id was cmd.exe (npm shim launches node in a fresh
#      process group), so `taskkill /T /PID cmd.exe` could miss node.
#      On timeout we now kill by IMAGE name across the whole subtree
#      (taskkill /T on the cmd.exe AND a sweep of orphaned node.exe that
#      were children), plus kill by command-line match as a belt-and-
#      suspenders so the actual claude node dies.
#
# Params:
#   -LogPath     : per-run log file (append progress lines here)        [required]
#   -Stamp       : YYYYMMDD-HHMMSS stamp for log lines                  [required]
#   -TimeoutMs   : hard cap in milliseconds                            [default 600000 = 10 min]
#
# Exit codes: claude's own rc on clean exit, 124 on timeout (convention).
# ============================================================

param(
    [Parameter(Mandatory=$true)] [string] $LogPath,
    [Parameter(Mandatory=$true)] [string] $Stamp,
    [int] $TimeoutMs = 600000
)

$ErrorActionPreference = "Continue"
$WorkDir = "C:\Users\2053437"
# CR6 (2026-08-07, FATAL): launch claude.EXE directly, not the claude.cmd shim.
#   The shim is `"%dp0%\...\claude.exe" %*` — going through cmd.exe /c + the
#   shim + nested quotes broke argument parsing on EVERY run (DIAGTEST2/3:
#   cmd saw `claude.cmd" -p ... --allowedTools "Read` as one broken token).
#   claude.exe is a real .exe, so Start-Process can launch it directly with
#   UseShellExecute=false (required by -RedirectStandard*), no cmd.exe layer,
#   no quoting hell. Verified path below.
$Claude = "$WorkDir\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe"
$Prompt = "$WorkDir\prompts\daily-brief-headless.txt"

# CR1/CR2: sidecar output files, NOT the shared run log. The caller
# folds these in. Use a stamp-qualified name so concurrent runs (two
# bat invocations) never collide.
$OutFile  = "$LogPath.claude.$Stamp.out"
$ErrFile  = "$LogPath.claude.$Stamp.err"

# claude flags — IDENTICAL to the old bat pipe line. Only the launch
# mechanism changed. Keep allowedTools/disallowedTools exactly as-is.
#
# CR5/CR7 (2026-08-07, FATAL): Start-Process -ArgumentList does NOT preserve
#   spaces inside array elements for a native .exe — it re-tokenizes on
#   whitespace, so `Bash(git commit *)` arrived at claude.exe as three
#   separate argv tokens `Bash(git` `commit` `*)` no matter whether we used
#   a single string, a comma-joined string, or repeated --disallowedTools
#   flags (DIAGTEST4/5/6 all reproduced the same "deny rule Bash(git
#   matches no known tool" stderr). The variadic <tools...> parser then
#   sees bogus split rules. cmd.exe /c re-quoting (CR8) didn't work either
#   because cmd does not understand `\"` escaping (DIAGTEST7).
#
# CR9 (2026-08-07, FIX): use the PowerShell `&` CALL OPERATOR with an
#   array (splatting) inside a Start-Job. The `&` operator hands each
#   array element to the native .exe as ONE argv token WITHOUT
#   re-tokenizing on whitespace — verified in call-probe: stderr had
#   ZERO rule-parse warnings (vs Start-Process's four). Start-Job wraps
#   the synchronous `&` call so we get Wait-Job -Timeout for the hard
#   cap, and stdin is piped from the prompt file inside the job's
#   scriptblock. Output redirected to sidecar files via PS redirection.
#   On timeout we Stop-Job AND sweep orphaned claude.exe/node.exe by
#   command-line match (the job's child processes are not killed by
#   Stop-Job alone — belt-and-suspenders, same idea as old CR3).
$ClaudeArgs = @(
    '-p',
    '--dangerously-skip-permissions',
    '--allowedTools', 'Read Grep Glob Write Bash(python *) Bash(dispatch.sh)',
    '--disallowedTools', 'Bash(git commit *) Bash(git push *) Bash(git rebase*) Bash(git reset*)'
)

Add-Content -Path $LogPath -Value "[$Stamp] claude -p start (bounded via & call + Start-Job, timeout ${TimeoutMs}ms)" -Encoding UTF8

$t0 = Get-Date

# CR9: run `& $Claude @ClaudeArgs` inside a job. Pass variables by -ArgumentList
# so the job scriptblock (isolated runspace) can see them. stdin comes from
# the prompt file; stdout/stderr go to the sidecar files via PS redirection.
$job = Start-Job -ScriptBlock {
    param($Claude, $ClaudeArgs, $PromptPath, $OutFile, $ErrFile, $WorkDir)
    Set-Location $WorkDir
    # Pipe prompt file content to claude's stdin; capture streams to files.
    # CR10 (2026-08-07, FATAL): -Encoding UTF8 required — without it
    # Get-Content read the BOMless UTF-8 Korean prompt as CP949 -> mojibake
    # -> claude saw "corrupted text" and refused to act (verified in probe).
    Get-Content -Raw -Encoding UTF8 -Path $PromptPath | & $Claude @ClaudeArgs 2>$ErrFile 1>$OutFile
} -ArgumentList $Claude, $ClaudeArgs, $Prompt, $OutFile, $ErrFile, $WorkDir

if ($null -eq $job) {
    Add-Content -Path $LogPath -Value "[$Stamp] FATAL: Start-Job returned null — claude never started" -Encoding UTF8
    exit 3
}

# Wait-Job -Timeout returns the job if it completed in time, $null otherwise.
$done = $job | Wait-Job -Timeout ([int]([math]::Floor($TimeoutMs / 1000)))
$elapsed = ((Get-Date) - $t0).TotalSeconds

# Fold the sidecar outputs into the run log regardless of outcome, so
# the caller doesn't need to. (CR1/CR2 — done here, not by the bat.)
function Fold-File($path, $header) {
    if (Test-Path $path) {
        Add-Content -Path $LogPath -Value "[$Stamp] --- $header ---" -Encoding UTF8
        Add-Content -Path $LogPath -Value (Get-Content -Path $path -Raw) -Encoding UTF8
        Remove-Item -Path $path -Force -ErrorAction SilentlyContinue
    }
}

if ($done) {
    # Job finished within the timeout. claude's own exit code is not directly
    # available from the job state; derive from the child process via the
    # sidecar output (the bat only checks for the "발송 완료" line anyway).
    # Treat Completed = success-ish (rc 0), Failed = error (rc 1).
    $rc = if ($job.State -eq 'Completed') { 0 } else { 1 }
    Fold-File $OutFile "claude stdout"
    Fold-File $ErrFile "claude stderr"
    Add-Content -Path $LogPath -Value "[$Stamp] claude job $($job.State) (rc=$rc) in $([math]::Round($elapsed,1))s (clean)" -Encoding UTF8
    $job | Remove-Job -Force
    exit $rc
} else {
    # Timeout — Stop-Job stops the PS job, but the child claude.exe/node.exe
    # it spawned may survive. Sweep by command-line match (CR3 idea).
    Add-Content -Path $LogPath -Value "[$Stamp] claude TIMEOUT after $([math]::Round($elapsed,1))s — stopping job" -Encoding UTF8
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
    Add-Content -Path $LogPath -Value "[$Stamp] claude stopped; bat will continue (exit 124)" -Encoding UTF8
    exit 124
}
