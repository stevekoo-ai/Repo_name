#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
push_log_rotate_to_main.py — log-rotate 자동화 2개 파일을 main에 Contents API PUT.

목적:
  log-rotate.yml / log_rotate.py 가 한 번도 commit/push 되지 않아 GitHub Actions
  schedule.cron이 발화하지 않음. schedule은 default branch(main)에 파일이
  있어야만 도므로, 이 2개 파일을 main에 올려야 자정 자동 로테이션이 작동.
  (사용자 결정: 이번만 예외로 main 직접 push — CLAUDE.md "main 직접 커밋 금지"
   예외 승인. 규칙 위반이므로 messagebox 사전 게시 완료상태에서 진행.)

3가지 함정 적용 (CLAUDE.md corp-github-api-push-gotchas.md 필수):
  함정 1: git credential fill 대화형 팝업 무한대기 → PAT를 CLI 인자로 직접 전달해
          get_pat (a) 분기에서 즉시 리턴, (c) credential 단계 자체 우회.
  함정 2: repo endpoint trailing slash → 404 → 본 스크립트는 Contents API
          (contents/{path}?ref=) 만 쓰고 루트 endpoint(path="") 안 써 자연 회피.
  함정 3: SSL 폴백 루프가 MITM 앱층 404에 무력 → 처음부터 unverified 단일 ctx 고정.

검증된 패턴 재사용: upload_log_summary.py / upload_brief.py 와 동일한
Contents API PUT 시퀀스(remote SHA 조회 → 갱신, 409 stale SHA 재시도,
HTTP status별 분기). 단 BRANCH="main" 으로 고정(서사 브랜치 아님).

Usage:
  python push_log_rotate_to_main.py            # PAT를 pat.txt에서 자동 읽어 CLI 인자로 전달
  python push_log_rotate_to_main.py "<PAT>"    # PAT 직접 전달
"""
import os
import sys
import ssl
import json
import time
import base64
import platform
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO = "stevekoo-ai/Repo_name"
BRANCH = "main"  # ★ main 고정 — schedule.cron 발화 조건
FILES = [
    ".github/workflows/log-rotate.yml",
    "scripts/log_rotate.py",
]

# 함정 3: 처음부터 unverified 단일 ctx 고정 (verified→unverified 폴백 안 함)
_CTX = ssl._create_unverified_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------------------
# Step 1: 환경 진단
# ---------------------------------------------------------------------------
def diag_environment():
    print("[1/6] 환경 진단")
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Python: {platform.python_version()}")
    print(f"  Repo: {REPO}")
    print(f"  Target branch: {BRANCH} (★ schedule 발화 조건)")
    print(f"  Files to upload: {len(FILES)}")
    for p in FILES:
        exists = os.path.isfile(p)
        size = os.path.getsize(p) if exists else 0
        flag = "OK" if exists else "MISSING"
        print(f"    [{flag}] {p} ({size} bytes)")
        if size > 73_000:
            print(f"    WARNING: {size} bytes > 73KB 사내망 한계 — PUT 실패 가능")
    print(f"  SSL: unverified 단일 ctx 고정 (함정 3 회피)")


# ---------------------------------------------------------------------------
# Step 2: PAT 확보 — 함정 1 회피: CLI 인자 최우선, pat.txt 다음, credential 금지
# ---------------------------------------------------------------------------
def get_pat(cli_arg):
    print("[2/6] PAT 확보 (함정 1 회피: CLI 인자 → pat.txt → 끝, credential 우회)")
    # (a) CLI 인자 — 가장 우선, credential 단계 완전 우회
    if cli_arg:
        print("  source: CLI 인자 (credential fill 단계 우회 확정)")
        return cli_arg, "cli arg"
    # (e) pat.txt — 환경변수 없으면 파일에서
    env_pat = os.environ.get("GITHUB_PAT", "") or os.environ.get("GH_TOKEN", "")
    if env_pat:
        print("  source: GITHUB_PAT/GH_TOKEN env var")
        return env_pat, "env var"
    for cand in [
        os.path.join(os.getcwd(), "PAT.txt"),
        os.path.join(os.getcwd(), "pat.txt"),
        os.path.join(os.path.expanduser("~"), "PAT.txt"),
        os.path.join(os.path.expanduser("~"), "pat.txt"),
    ]:
        if os.path.isfile(cand):
            try:
                with open(cand, "r", encoding="utf-8") as f:
                    val = f.read().strip()
                if val:
                    print(f"  source: pat.txt at {cand}")
                    return val, f"pat.txt ({cand})"
            except Exception:
                pass
    # (c) git credential fill — ★ 의도적으로 시도 안 함 (함정 1: 무한대기 위험)
    print("  PAT 확보 실패 — CLI 인자/pat.txt/env 모두 없음")
    print("  (git credential fill은 함정 1 무한대기 위험으로 시도 안 함)")
    return None, None


# ---------------------------------------------------------------------------
# Step 3: 네트워크 — 함정 3: unverified 단일 ctx (폴백 루프 없음)
# ---------------------------------------------------------------------------
def make_request(url, pat, method="GET", data=None):
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "log-rotate-main-push",
    }
    if data is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, context=_CTX, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            try:
                return resp.status, json.loads(body)
            except json.JSONDecodeError:
                return resp.status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            body_json = json.loads(body)
        except json.JSONDecodeError:
            body_json = body
        return e.code, body_json
    except urllib.error.URLError as e:
        return -1, f"URLError: {e.reason}"
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"


def get_remote_sha(path, pat):
    # Contents API GET — path 가 항상 비어있지 않으므로 함정 2(trailing slash) 해당 없음
    api = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={BRANCH}"
    status, body = make_request(api, pat, method="GET")
    if status == 200 and isinstance(body, dict):
        return body.get("sha", "")
    if status == 404:
        return None  # 신규 파일
    print(f"  remote SHA 조회 status {status}: {str(body)[:150]}")
    return "ERROR"


# ---------------------------------------------------------------------------
# Step 4: Contents API PUT (409 stale SHA 재시도)
# ---------------------------------------------------------------------------
def upload_file(path, pat):
    print(f"[4/6] Contents API PUT — {path} → {BRANCH}")
    if not os.path.isfile(path):
        print(f"  로컬 파일 없음 — skip")
        return None
    size = os.path.getsize(path)
    if size > 100_000:
        print(f"  WARNING: {size} bytes — Contents API 크기 한계 주의")

    print(f"  remote SHA 조회...")
    sha = get_remote_sha(path, pat)
    if sha == "ERROR":
        return None
    if sha is None:
        print(f"  신규 파일 (remote에 없음) — create")
    else:
        print(f"  기존 파일 (sha={sha[:8]}...) — update")

    with open(path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode("ascii")

    url = f"https://api.github.com/repos/{REPO}/contents/{path}"

    for attempt in range(1, 4):
        payload = {
            "message": f"ci: add {path} (log-rotate 자동화 main 배포 — schedule 발화 조건)\n\nCo-Authored-By: Claude <noreply@anthropic.com>",
            "content": content_b64,
            "branch": BRANCH,
        }
        if sha:
            payload["sha"] = sha

        status, body = make_request(url, pat, method="PUT", data=json.dumps(payload).encode("utf-8"))
        if status in (200, 201):
            csha = body.get("commit", {}).get("sha", "?") if isinstance(body, dict) else "?"
            print(f"  PUT success ({status}) — commit {csha}")
            return csha
        elif status == 409:
            print(f"  409 (stale SHA) — re-fetch, retry {attempt}/3")
            new_sha = get_remote_sha(path, pat)
            if new_sha in (None, "ERROR"):
                return None
            sha = new_sha
            time.sleep(2)
            continue
        elif status == 401:
            print(f"  401: PAT invalid/expired")
            return None
        elif status == 403:
            print(f"  403: forbidden/rate-limit. body: {str(body)[:200]}")
            return None
        elif status == 404:
            print(f"  404 on PUT — retry as create (no sha)")
            sha = None
            continue
        elif status == 422:
            print(f"  422: validation failed. body: {str(body)[:200]}")
            return None
        elif status == 429:
            print(f"  429: rate limited — backoff 30s")
            time.sleep(30)
            continue
        else:
            print(f"  unexpected status {status}: {str(body)[:200]}")
            return None
    print(f"  exhausted 409 retries")
    return None


# ---------------------------------------------------------------------------
# Step 5: 에러별 분기 (make_request/upload_file 내 status 분기로 통합)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Step 6: 최종 요약 리포트
# ---------------------------------------------------------------------------
def report(results, pat_source):
    print("[6/6] 최종 요약 리포트")
    ok = sum(1 for r in results if r[1])
    fail = len(results) - ok
    print(f"  작업: log-rotate 자동화 2개 파일 main 배포")
    print(f"  결과: {ok} 성공 / {fail} 실패 (전체 {len(results)})")
    for path, csha in results:
        mark = "OK " if csha else "FAIL"
        print(f"    [{mark}] {path} → {csha or '실패'}")
    print(f"  PAT source: {pat_source}")
    if ok == len(results):
        print(f"  다음 액션: main에 파일 반영 완료. GitHub Actions schedule(15:20 UTC=00:20 KST)가")
        print(f"            다음 자정부터 log_rotate.py 실행 → log.md 일자별 자동 아카이브 시작.")
        print(f"            (선택) Actions 탭에서 'Log Rotate' workflow 수동 run으로 즉시 검증 가능.")
    else:
        print(f"  다음 액션: 실패 파일 로그 확인 후 PAT/네트워크 점검. 부분 성공 시 이미 올라간 파일은 남음.")


def main():
    cli_pat = sys.argv[1] if len(sys.argv) > 1 else None
    diag_environment()

    # 파일 존재 사전 확인
    missing = [p for p in FILES if not os.path.isfile(p)]
    if missing:
        print(f"FATAL: 로컬 파일 없음: {missing}")
        sys.exit(1)

    pat, pat_source = get_pat(cli_pat)
    if not pat:
        print("FATAL: PAT 확보 실패 — pat.txt 또는 CLI 인자로 전달 필요")
        print("  사용법: python push_log_rotate_to_main.py \"<PAT>\"")
        report([], "none")
        sys.exit(1)

    results = []
    for path in FILES:
        csha = upload_file(path, pat)
        results.append((path, csha))

    report(results, pat_source)
    sys.exit(0 if all(r[1] for r in results) else 1)


if __name__ == "__main__":
    main()
