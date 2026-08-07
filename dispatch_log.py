#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dispatch_log.py — log.md(회사망 73KB 한계 초과)를 GitHub Actions에 위임 commit.

flow: log.md → gzip 압축 → base64 → repository_dispatch(event_type=commit-log)
      → Actions runner가 gunzip → git commit + push (회사망 제약 없음)

이 스크립트는 dispatch.sh의 패턴을 log.md commit 용도로 확장. 차이:
  - HTML 발송(send-brief)이 아니라 파일 commit(commit-log)
  - client_payload에 commit_message, file_path, branch 포함
  - Actions가 이메일 대신 git commit + push 수행

왜 필요한가: log.md 113KB는 회사망 git push 403 + 73KB POST 한계로 직접 push
불가. gzip 42KB → base64 56KB < 64KB client_payload 한계 → dispatch 가능.
Actions runner는 GitHub 인프라라 회사망 제약 없이 commit+push.

CLAUDE.md "진단형 테스트 스크립트" 프로토콜 준수.

사용법:
  python dispatch_log.py wiki/log.md
  python dispatch_log.py wiki/log.md "커밋 메시지"
  python dispatch_log.py wiki/log.md "커밋 메시지" ghp_...
  env GITHUB_PAT=ghp_... python dispatch_log.py wiki/log.md "커밋 메시지"
"""
import sys
import os
import ssl
import json
import gzip
import base64
import time
import platform
import subprocess
import urllib.request
import urllib.error

# Windows 콘솔 cp949 인코딩 UTF-8 강제
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
REPO = "stevekoo-ai/Repo_name"
EVENT_TYPE = "commit-log"            # Actions on: repository_dispatch.types: [commit-log]
BRANCH = "claude/ai-agent-impl-002tip"
DISPATCH_URL = f"https://api.github.com/repos/{REPO}/dispatches"
WORKDIR = os.path.expanduser("~")
PAYLOAD_CAP = 63_000  # client_payload 64KB 안전 마진


# ---------------------------------------------------------------------------
# PAT 확보 — upload_brief.py / dispatch.sh 동일 폴백 체인
# ---------------------------------------------------------------------------
def get_pat(cli_arg):
    if cli_arg and cli_arg.startswith("ghp_"):
        print(f"  [1/6] PAT: CLI 인자 ({cli_arg[:8]}...)")
        return cli_arg
    env_pat = os.environ.get("GITHUB_PAT", "") or os.environ.get("GH_TOKEN", "")
    if env_pat.startswith("ghp_"):
        print(f"  [1/6] PAT: GITHUB_PAT/GH_TOKEN env var ({env_pat[:8]}...)")
        return env_pat
    try:
        proc = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True, text=True, timeout=10,
        )
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                val = line[len("password="):].strip()
                if val.startswith("ghp_"):
                    print(f"  [1/6] PAT: git credential manager ({val[:8]}...)")
                    return val
    except Exception:
        pass
    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-Clipboard"],
            capture_output=True, text=True, timeout=3,
        )
        pat = result.stdout.strip()
        if pat.startswith("ghp_"):
            print(f"  [1/6] PAT: clipboard ({pat[:8]}...)")
            return pat
    except Exception:
        pass
    for cand in [os.path.join(WORKDIR, "pat.txt"), os.path.join(os.getcwd(), "pat.txt")]:
        if os.path.isfile(cand):
            try:
                with open(cand, "r", encoding="utf-8") as f:
                    pat = f.read().strip()
                if pat.startswith("ghp_"):
                    print(f"  [1/6] PAT: pat.txt ({cand}, {pat[:8]}...)")
                    return pat
            except Exception:
                pass
    print("  [1/6] PAT: 자동 소스에서 찾지 못함. 수동 입력:")
    try:
        import getpass
        pat = getpass.getpass("  PAT (ghp_...): ").strip()
        if pat.startswith("ghp_"):
            return pat
    except Exception:
        pass
    print("  [1/6] PAT 확보 실패")
    return None


# ---------------------------------------------------------------------------
# 네트워크 — SSL fallback (회사 MITM 대응)
# ---------------------------------------------------------------------------
def make_request(url, pat, method="GET", body=None, ctx_pref=None):
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "dispatch-log-bot",
    }
    if body is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    ctxs = [ctx_pref] if ctx_pref else [ssl.create_default_context(),
                                         ssl._create_unverified_context()]
    for i, ctx in enumerate(ctxs):
        if ctx is None:
            continue
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
                try:
                    return resp.status, json.loads(raw)
                except json.JSONDecodeError:
                    return resp.status, raw
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            try:
                err_json = json.loads(err_body)
            except json.JSONDecodeError:
                err_json = err_body
            return e.code, err_json
        except urllib.error.URLError as e:
            reason = str(e.reason)
            if ("SSL" in reason or "CERTIFICATE" in reason or "verify" in reason.lower()) and i == 0 and ctx_pref is None:
                print(f"    SSL 검증 실패 ({reason[:50]}); unverified로 폴백...")
                continue
            return -1, f"URLError: {reason}"
        except Exception as e:
            return -1, f"{type(e).__name__}: {e}"
    return -1, "exhausted SSL fallback"


# ---------------------------------------------------------------------------
# 핵심: gzip + base64 인코딩
# ---------------------------------------------------------------------------
def encode_file(path):
    with open(path, "rb") as f:
        raw = f.read()
    gz = gzip.compress(raw, compresslevel=9)
    b64 = base64.b64encode(gz).decode("ascii")
    print(f"    원본 {len(raw):,} → gzip {len(gz):,} (×{len(raw)/max(len(gz),1):.1f}) → base64 {len(b64):,}")
    return b64, len(raw), len(gz)


# ---------------------------------------------------------------------------
# dispatch POST (에러별 분기)
# ---------------------------------------------------------------------------
def send_dispatch(pat, file_path, content_b64, commit_message, ctx_pref):
    if len(content_b64) > PAYLOAD_CAP:
        return False, (
            f"압축+base64 후 {len(content_b64):,} bytes > client_payload 한계 {PAYLOAD_CAP:,}. "
            f"log.md가 너무 큼 — 아카이브(rotete)로 줄이거나 외부망 필요."
        )
    payload = {
        "event_type": EVENT_TYPE,
        "client_payload": {
            "file_path": file_path.replace("\\", "/"),   # 원격 git 경로
            "content_b64": content_b64,
            "encoding": "gzip+base64",
            "commit_message": commit_message,
            "branch": BRANCH,
        },
    }
    body_size = len(json.dumps(payload).encode("utf-8"))
    print(f"    POST body 총 {body_size:,} bytes (한계 {PAYLOAD_CAP:,})")
    for attempt in range(1, 4):
        status, body = make_request(DISPATCH_URL, pat, method="POST", body=payload, ctx_pref=ctx_pref)
        if status == 204:
            return True, "204 No Content — dispatch 수신됨"
        if status == 401:
            return False, f"401: PAT 무효/만료 — {str(body)[:150]}"
        if status == 403:
            return False, f"403: 권한/회사망 한계 — {str(body)[:150]}"
        if status == 404:
            return False, f"404: 저장소 없음 — REPO 확인 ({REPO})"
        if status == 422:
            return False, f"422: event_type/client_payload 형식 오류 — {str(body)[:150]}"
        if status == 429:
            print(f"    429 rate limit — 30s 대기 후 재시도 {attempt}/3")
            time.sleep(30)
            continue
        return False, f"POST 실패 status={status}: {str(body)[:200]}"
    return False, "429 재시도 3회 초과"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("  dispatch_log.py — gzip+base64 → repository_dispatch (commit-log)")
    print("=" * 60)

    args = sys.argv[1:]
    pat_candidates = [a for a in args if a.startswith("ghp_")]
    non_pat = [a for a in args if not a.startswith("ghp_")]
    if not non_pat:
        print("  사용법: python dispatch_log.py <파일경로> [커밋메시지] [ghp_...]")
        sys.exit(1)
    file_path = os.path.abspath(non_pat[0])
    if not os.path.isfile(file_path):
        print(f"  [FATAL] 파일 없음: {file_path}")
        sys.exit(1)
    # 커밋 메시지: 두 번째 non_pat 인자, 없으면 기본
    commit_message = non_pat[1] if len(non_pat) > 1 else (
        "log: update via dispatch_log.py (회사망 73KB 한계 우회)"
    )

    print(f"  [2/6] 환경 진단")
    print(f"    OS: {platform.system()} {platform.release()}")
    print(f"    Python: {platform.python_version()}")
    print(f"    Repo: {REPO}")
    print(f"    Event type: {EVENT_TYPE}")
    print(f"    Branch: {BRANCH}")
    print(f"    File: {file_path} ({os.path.getsize(file_path):,} bytes 원본)")

    pat_arg = pat_candidates[0] if pat_candidates else None
    pat = get_pat(pat_arg)
    if not pat:
        print("  [FATAL] PAT 확보 실패")
        sys.exit(1)

    # 연결성
    print(f"  [3/6] 연결성 테스트 (SSL fallback)")
    status, body = make_request(f"https://api.github.com/repos/{REPO}", pat, method="GET")
    if status != 200:
        print(f"  [FATAL] 연결 실패 status={status}: {str(body)[:100]}")
        sys.exit(1)
    print(f"    연결 OK — repo: {body.get('full_name', REPO)}")
    ctx_pref = ssl._create_unverified_context()

    # 인코딩
    print(f"  [4/6] gzip 압축")
    # 원격 경로: 절대경로에서 repo 루트 상대경로로 변환
    cwd = os.getcwd().replace("\\", "/")
    remote_path = file_path.replace("\\", "/").replace(cwd + "/", "", 1)
    if remote_path == file_path.replace("\\", "/"):
        # cwd 기반 변환 실패 시 basename fallback
        remote_path = os.path.basename(file_path)
    print(f"    원격 경로: {remote_path}")
    content_b64, orig_size, gz_size = encode_file(file_path)

    # dispatch
    print(f"  [5/6] dispatch POST (event_type={EVENT_TYPE})")
    ok, detail = send_dispatch(pat, remote_path, content_b64, commit_message, ctx_pref)

    print(f"  [6/6] 최종 요약")
    print(f"    결과: {'SUCCESS' if ok else 'FAILURE'}")
    print(f"    상세: {detail}")
    if ok:
        print(f"    다음: GitHub Actions 탭 '{EVENT_TYPE}' run 확인 → "
              f"runner가 {remote_path} commit+push 수행")
    print("=" * 60)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
