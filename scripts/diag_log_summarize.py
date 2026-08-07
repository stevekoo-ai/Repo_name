#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diag_log_summarize.py — run_log_summarize_bounded.ps1의 빈 stdout 원인 진단.

CLAUDE.md "진단형 테스트 스크립트" 프로토콜 준수 — 모든 케이스 cover, 한 번에 실행,
최종 결론 나야 종료. 부분 테스트→실패→수정 사이클 금지.

문제: run_log_summarize_bounded.ps1이 claude -p를 rc=0, 18.1s로 완료하나
stdout이 완전히 비어 있음 → log.md 요약 갱신 안 됨.

방법: 기존 성공 사례(run_cxl_claude_bounded.ps1)와의 3가지 구문 차이를
변수로 고립해, 어느 조합에서 응답이 나오는지 측정.
  변수 A: --append-system-prompt-file (있음/없음)
  변수 B: --allowedTools (현재 Edit만 / 성공패턴 Write+Edit)
  변수 C: 프롬프트 파일 (log-summarize / 최소 1줄)

각 테스트는 claude.exe 직접 subprocess 호출 + stdin 파이프(이슈3 해결책 준수) +
timeout 120s. stdout/stderr/exit code 전부 캡처. 사내 GLM 라우팅은 .claude/settings.json
자동 적용(claude.exe가 로드).

진단 6단계 (CLAUDE.md 진단형 프로토콜):
  1. 환경 진단 (claude.exe, settings.json, 프롬프트 파일, 인코딩/BOM)
  2. 파일/리소스 존재 확인
  3. 최소 동작 베이스라인 (1+1 → "2" 나오는지, GLM 라우팅 정상 확인)
  4. 변수 고립 테스트 (A/B/C 조합, 응답 길이 비교)
  5. 에러별 분기 (exit code별 원인)
  6. 최종 요약 리포트 (원인 + 수정 액션)

Usage:
  python scripts/diag_log_summarize.py
"""
import os
import sys
import json
import subprocess
import platform
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

WORK = Path(r"C:\Users\2053437")
CLAUDE = WORK / "AppData" / "Roaming" / "npm" / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
SETTINGS = WORK / ".claude" / "settings.json"
PROMPT_LS = WORK / "prompts" / "log-summarize-headless.txt"
PROMPT_CXL_SYS = WORK / ".claude" / "prompts" / "cxl-daily-update.md"  # 성공 패턴의 system prompt
TIMEOUT = 120  # claude -p 최대 120s (요약은 짧음)

# 허용/금지 도구 — 성공 패턴(run_cxl) 그대로 vs 현재(log-summarize)
ALLOW_CXL = "Read Grep Glob Write Edit WebFetch Bash(python *) Bash(dispatch.sh)"
ALLOW_LS = "Read Grep Glob Edit Bash(python *)"
DISALLOW = "Bash(git commit *) Bash(git push *) Bash(git rebase*) Bash(git reset*) Bash(git checkout*) Bash(git stash*) Bash(git pull*) Bash(git fetch*)"


def banner(n, title):
    print(f"\n{'='*70}\n[{n}] {title}\n{'='*70}")


def check_bom(p):
    """파일 BOM/인코딩 진단."""
    if not p.exists():
        return f"MISSING ({p})"
    data = p.read_bytes()
    bom = data[:3] == b"\xef\xbb\xbf"
    try:
        data.decode("utf-8")
        enc = "UTF-8 OK"
    except UnicodeDecodeError:
        enc = "UTF-8 DECODE FAIL"
    kr = sum(1 for c in data.decode("utf-8", errors="replace") if ord(c) > 0xAC00)
    return f"exists, {len(data)}B, BOM={bom}, {enc}, 한글라인~{kr}"


def run_claude(prompt_text, allow, sys_prompt=None, label=""):
    """claude -p 호출 — stdin으로 프롬프트 전달(이슈3 해결책), 결과 캡처."""
    args = [
        str(CLAUDE), "-p",
        "--dangerously-skip-permissions",
        "--allowedTools", allow,
        "--disallowedTools", DISALLOW,
    ]
    if sys_prompt and Path(sys_prompt).exists():
        args += ["--append-system-prompt-file", str(sys_prompt)]

    print(f"\n--- TEST [{label}] ---")
    print(f"  allow: {allow}")
    print(f"  sys_prompt: {Path(sys_prompt).name if sys_prompt else '(없음)'}")
    print(f"  prompt len: {len(prompt_text)} chars")

    try:
        proc = subprocess.run(
            args, input=prompt_text.encode("utf-8"),
            capture_output=True, timeout=TIMEOUT,
            cwd=str(WORK),
        )
        out = proc.stdout.decode("utf-8", errors="replace")
        err = proc.stderr.decode("utf-8", errors="replace")
        print(f"  exit: {proc.returncode}")
        print(f"  stdout: {len(out)} chars | {out[:200]!r}")
        if err:
            print(f"  stderr: {len(err)} chars | {err[:200]!r}")
        return {"label": label, "exit": proc.returncode, "out_len": len(out),
                "out": out, "err": err}
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT after {TIMEOUT}s")
        return {"label": label, "exit": -1, "out_len": -1, "out": "", "err": "timeout"}
    except Exception as e:
        print(f"  ERR: {type(e).__name__}: {e}")
        return {"label": label, "exit": -2, "out_len": -2, "out": "", "err": str(e)}


def main():
    results = []

    # ------------------------------------------------------------------
    # Step 1: 환경 진단
    # ------------------------------------------------------------------
    banner(1, "환경 진단")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print(f"Work: {WORK}")
    print(f"claude.exe: [{'OK' if CLAUDE.exists() else 'MISSING'}] {CLAUDE}")
    print(f"settings.json: [{'OK' if SETTINGS.exists() else 'MISSING'}] {SETTINGS}")

    # ------------------------------------------------------------------
    # Step 2: 파일/리소스 존재 확인 + 인코딩/BOM 진단
    # ------------------------------------------------------------------
    banner(2, "파일/리소스 존재 + 인코딩/BOM 진단")
    print(f"prompt (log-summarize): {check_bom(PROMPT_LS)}")
    print(f"sys_prompt (cxl): {check_bom(PROMPT_CXL_SYS)}")

    # settings.json GLM 라우팅 키 확인 (노출 금지 — 키 이름만)
    if SETTINGS.exists():
        try:
            sj = json.loads(SETTINGS.read_text(encoding="utf-8"))
            env = sj.get("env", {})
            print(f"settings.json env keys: {list(env.keys())}")
            # 모델 매핑/게이트웨이 키 존재만 확인 (값 노출 X)
            for k in env:
                if any(t in k.lower() for t in ("model", "base", "url", "gateway", "token", "api")):
                    print(f"  라우팅 관련 키 있음: {k}")
        except Exception as e:
            print(f"settings.json 파싱 실패: {e}")

    # ------------------------------------------------------------------
    # Step 3: 최소 동작 베이스라인 (GLM 라우팅 정상 확인)
    # ------------------------------------------------------------------
    banner(3, "최소 동작 베이스라인 — 1+1 (GLM 라우팅 정상 확인)")
    base = run_claude("1+1은? 숫자로만 답해.", ALLOW_LS, label="base 1+1")
    results.append(base)
    if base["out_len"] > 0 and "2" in base["out"]:
        print("  ✅ GLM 라우팅 정상 — 응답 생성됨")
    else:
        print("  ❌ 베이스라인 실패 — GLM 라우팅/claude 자체 문제. 아래 테스트 무의미.")
        report(results, "베이스라인 실패: GLM 라우팅 또는 claude 자체 문제")
        return

    # ------------------------------------------------------------------
    # Step 4: 변수 고립 테스트 (A/B/C 조합)
    # ------------------------------------------------------------------
    banner(4, "변수 고립 테스트 — 어느 조합에서 빈 stdout 나는지")
    prompt_ls = PROMPT_LS.read_text(encoding="utf-8") if PROMPT_LS.exists() else "log.md 요약 갱신"
    # 진단용 축소 프롬프트 (전체 프롬프트 대신 간단 작업 — 응답 생성 자체가 원인인지 확인)
    prompt_mini = "wiki/log.md의 ## 당월 요약 (2026-08) 섹션을 읽고, 그대로 출력해. (진단용: 수정 금지, 읽기만)"

    # Test A1: 현재 패턴 그대로 (allow=LS, sys_prompt 없음, 전체 프롬프트)
    results.append(run_claude(prompt_ls, ALLOW_LS, sys_prompt=None, label="A1: 현재패턴(allow=LS,sys=없음,전체프롬프트)"))

    # Test A2: 현재 패턴 + 축소 프롬프트 (프롬프트 길이/내용이 원인인지)
    results.append(run_claude(prompt_mini, ALLOW_LS, sys_prompt=None, label="A2: 현재패턴+축소프롬프트(읽기만)"))

    # Test B: 성공 패턴 allow (Write+WebFetch 추가) — allow 구문이 원인인지
    results.append(run_claude(prompt_mini, ALLOW_CXL, sys_prompt=None, label="B: 성공패턴allow(Write+WebFetch)"))

    # Test C: 성공 패턴 sys_prompt 추가 — sys_prompt 부재가 원인인지 (★ 최유력)
    results.append(run_claude(prompt_mini, ALLOW_LS, sys_prompt=str(PROMPT_CXL_SYS), label="C: sys_prompt추가(cxl)"))

    # Test D: 성공 패턴 전부 (allow=CXL + sys_prompt) — 이게 응답 나오면 성공 패턴 복제로 해결
    results.append(run_claude(prompt_mini, ALLOW_CXL, sys_prompt=str(PROMPT_CXL_SYS), label="D: 성공패턴전부(allow=CXL+sys)"))

    # ------------------------------------------------------------------
    # Step 5: 에러별 분기 (exit code별 원인)
    # ------------------------------------------------------------------
    banner(5, "에러별 분기 (exit code별 원인 요약)")
    for r in results:
        if r["exit"] == 0:
            verdict = "정상종료" + ("" if r["out_len"] > 0 else " ⚠ 빈 stdout")
        elif r["exit"] == -1:
            verdict = "TIMEOUT"
        elif r["exit"] == -2:
            verdict = f"EXCEPTION: {r['err'][:50]}"
        else:
            verdict = f"exit {r['exit']}"
        print(f"  [{r['label']}]: exit={r['exit']}, stdout={r['out_len']} chars → {verdict}")

    # ------------------------------------------------------------------
    # Step 6: 최종 요약 리포트
    # ------------------------------------------------------------------
    report(results, None)


def report(results, forced):
    banner(6, "최종 요약 리포트")
    if forced:
        print(f"  결론: {forced}")
        print(f"  다음 액션: settings.json GLM 라우팅 점검 + claude.exe 재실행")
        return

    # 빈 stdout이 아닌 첫 테스트 찾기 → 원인 고립
    base = results[0]
    if base["out_len"] <= 0 or "2" not in base["out"]:
        print(f"  결론: 베이스라인(1+1) 실패 → GLM 라우팅/claude 자체 문제. 스크립트 수정으로 안 됨.")
        return

    # A1(현재 패턴) 응답 여부
    a1 = next((r for r in results if r["label"].startswith("A1")), None)
    d = next((r for r in results if r["label"].startswith("D")), None)
    c = next((r for r in results if r["label"].startswith("C")), None)
    b = next((r for r in results if r["label"].startswith("B")), None)
    a2 = next((r for r in results if r["label"].startswith("A2")), None)

    def has_resp(r):
        return r and r["out_len"] > 5

    print(f"  베이스라인(1+1): {'응답' if has_resp(base) else '빈 응답'} ({base['out_len']} chars)")
    print(f"  A1 현재패턴(전체프롬프트): {'응답' if has_resp(a1) else '빈 응답'} ({a1['out_len'] if a1 else '?'} chars)")
    print(f"  A2 축소프롬프트(읽기만): {'응답' if has_resp(a2) else '빈 응답'} ({a2['out_len'] if a2 else '?'} chars)")
    print(f"  B  성공allow(Write+WebFetch): {'응답' if has_resp(b) else '빈 응답'} ({b['out_len'] if b else '?'} chars)")
    print(f"  C  sys_prompt추가: {'응답' if has_resp(c) else '빈 응답'} ({c['out_len'] if c else '?'} chars)")
    print(f"  D  성공패턴전부: {'응답' if has_resp(d) else '빈 응답'} ({d['out_len'] if d else '?'} chars)")
    print()

    # 원인 특정 로직
    if has_resp(a1):
        print("  결론: 현재 패턴(A1) 자체가 응답함 → 빈 stdout 원인은 '전체 프롬프트의 특정 지시'가")
        print("        도구를 트리거하지 못한 것. 프롬프트 내용/지시 점검 필요 (허용 도구 아님).")
    elif has_resp(a2) and not has_resp(a1):
        print("  결론: 축소 프롬프트(A2)는 응답, 전체 프롬프트(A1)는 빈 응답 →")
        print("        원인은 '전체 프롬프트 내용' (log-summarize-headless.txt의 특정 지시가")
        print("        claude를 멈추게 함 — 예: messagebox HALT 체크 지시가 중단시키거나,")
        print("        너무 긴 프롬프트). 프롬프트 파일 수정 필요.")
    elif has_resp(c) and not has_resp(a2):
        print("  결론: sys_prompt 추가(C)시에만 응답 → 원인 #1 확정:")
        print("        --append-system-prompt-file 부재. run_log_summarize_bounded.ps1에")
        print("        --append-system-prompt-file 추가 + system prompt 파일 생성으로 해결.")
    elif has_resp(b) and not has_resp(a2):
        print("  결론: 성공 allow(B)시에만 응답 → 원인 #2: --allowedTools에 Write/WebFetch 부재.")
        print("        run_log_summarize_bounded.ps1의 allow에 Write 추가로 해결.")
    elif has_resp(d) and not has_resp(a2) and not has_resp(c) and not has_resp(b):
        print("  결론: 성공 패턴 전부(D)시에만 응답 → allow + sys_prompt 조합 필요.")
        print("        두 차이 모두 메꿔야 (Write 추가 + sys_prompt 추가).")
    elif not has_resp(d):
        print("  결론: 성공 패턴 전부(D)여도 빈 응답 → 구문 차이가 아닌 런타임 문제.")
        print("        원인 후보: (1) settings.json GLM 라우팅이 요약 작업을 거부,")
        print("        (2) 프롬프트 파일 BOM/인코딩, (3) .claude/settings.json 모델 매핑.")
        print("        다음 액션: settings.json env 점검 + 프롬프트 파일 BOM 제거 재테스트.")
    else:
        print("  결론: 변수 고립 결과로 원인 명확히 특정 못함 — 위 결과표 참조해 수동 판정.")
    print()
    print("  다음 액션: 위 결론에 따라 run_log_summarize_bounded.ps1 또는 프롬프트 파일 수정.")


if __name__ == "__main__":
    main()
