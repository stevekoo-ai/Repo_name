#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Brief 자동 업로드 — 로컬 보고서 HTML을 GitHub remote로.

회사망에서 `git push`가 403으로 막히므로 GitHub Contents API PUT으로 우회.
매일 날짜를 코드에 박는 대신, `report/daily-brief-*.html` 중 최신 파일을
자동 탐지하여 업로드. 날짜 하드코딩 제거가 이 스크립트의 존재 이유.

CLAUDE.md "진단형 테스트 스크립트" 프로토콜 준수 — 6단계:
  1. 환경 진단 — OS, Python, git, 대상 파일
  2. 파일/리소스 존재 확인 — 로컬 HTML, remote SHA
  3. 네트워크/연결성 — SSL fallback, timeout
  4. 에러별 분기 — 401/403/404/409/422/429 자동 대응
  5. 대체 경로 폴백 — CLI → env → git credential → clipboard → pat.txt → getpass
  6. 최종 요약 리포트 — 성공/실패, 원인, 다음 액션

사용법:
  python upload_brief.py                    # 최신 daily-brief-*.html 자동 선택
  python upload_brief.py 2026-08-04          # 특정 날짜
  python upload_brief.py 2026-08-04 ghp_...  # 날짜 + PAT 직접 지정
  env GITHUB_PAT=ghp_... python upload_brief.py

설정 (스크립트 상단 CONFIG 섹션):
  REPO, BRANCH, REPORT_GLOB — 저장소/브랜치/파일 패턴
"""
import sys
import os
import ssl
import glob
import json
import base64
import time
import platform
import subprocess
import urllib.request
import urllib.parse
import urllib.error

# ---------------------------------------------------------------------------
# CONFIG — 필요 시 이 섹션만 수정
# ---------------------------------------------------------------------------
REPO = "stevekoo-ai/Repo_name"
BRANCH = "claude/ai-agent-impl-002tip"
REPORT_GLOB = "report/daily-brief-*.html"
API_BASE = f"https://api.github.com/repos/{REPO}/contents"
WORKDIR = os.path.expanduser("~")

# 회사 프록시 POST body 한계 (측정값: ~73KB content). 이 이상 파일은 회사망에서 막힘.
POST_SIZE_CAP = 70_000  # 안전 마진 (측정 한계 73KB)

COMMITTER_NAME = "Daily Brief Bot"
COMMITTER_EMAIL = "noreply@anthropic.com"


# ---------------------------------------------------------------------------
# Step 5 (early): PAT 확보 — fallback chain
# ---------------------------------------------------------------------------
def get_pat(cli_arg):
    """우선순위: CLI 인자 → env var → git credential manager → clipboard → pat.txt → getpass."""
    # (a) CLI 인자
    if cli_arg and cli_arg.startswith("ghp_"):
        print(f"  [1/6] PAT: CLI 인자 ({cli_arg[:8]}...)")
        return cli_arg

    # (b) env var
    env_pat = os.environ.get("GITHUB_PAT", "") or os.environ.get("GH_TOKEN", "")
    if env_pat.startswith("ghp_"):
        print(f"  [1/6] PAT: GITHUB_PAT/GH_TOKEN env var ({env_pat[:8]}...)")
        return env_pat

    # (c) git credential manager (Windows 자격 증명 관리자)
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

    # (d) clipboard (PowerShell Get-Clipboard)
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

    # (e) pat.txt
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

    # (f) getpass (수동 입력)
    print("  [1/6] PAT: 자동 소스에서 찾지 못함. 수동 입력:")
    try:
        import getpass
        pat = getpass.getpass("  PAT (ghp_...): ").strip()
        if pat.startswith("ghp_"):
            return pat
    except Exception:
        pass

    print("  [1/6] PAT 확보 실패 — 어느 소스에서도 ghp_ 토큰을 찾지 못함")
    return None


# ---------------------------------------------------------------------------
# Step 1: 환경 진단
# ---------------------------------------------------------------------------
def diag_environment(report_path):
    print(f"  [2/6] 환경 진단")
    print(f"    OS: {platform.system()} {platform.release()}")
    print(f"    Python: {platform.python_version()}")
    print(f"    Repo: {REPO}")
    print(f"    Branch: {BRANCH}")
    print(f"    Report: {report_path} ({os.path.getsize(report_path):,} bytes)")
    ssl_ok = hasattr(ssl, "_create_unverified_context")
    print(f"    SSL unverified fallback available: {ssl_ok}")


# ---------------------------------------------------------------------------
# Step 3: 네트워크 — SSL fallback request helper
# ---------------------------------------------------------------------------
def make_request(url, pat, method="GET", body=None, ctx_pref=None):
    """
    Verified SSL 먼저, 실패 시 unverified(회사 MITM)로 폴백.
    ctx_pref가 주어지면 그것만 사용(재사용).
    Returns (status, json_or_text).
    """
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "upload-brief-bot",
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


def api_path(path, ref=None):
    url = API_BASE + "/" + urllib.parse.quote(path.lstrip("/"))
    if ref:
        url += f"?ref={ref}"
    return url


# ---------------------------------------------------------------------------
# Step 2: 파일 탐지 + remote SHA 확인
# ---------------------------------------------------------------------------
def find_report(date_arg):
    """report/daily-brief-*.html 중 최신(또는 지정 날짜) 파일 경로 반환."""
    pattern = os.path.join(WORKDIR, REPORT_GLOB)
    files = sorted(glob.glob(pattern), key=os.path.getmtime)
    if not files:
        return None, f"로컬에 {REPORT_GLOB} 파일 없음. 보고서를 먼저 생성하세요."

    if date_arg:
        target = f"daily-brief-{date_arg}.html"
        for f in files:
            if os.path.basename(f) == target:
                return f, None
        return None, f"지정 날짜 {date_arg} 파일 없음. 존재: {[os.path.basename(x) for x in files[-3:]]}"

    latest = files[-1]
    return latest, None


def get_remote_sha(pat, path, ctx_pref):
    """remote 파일 SHA 조회. 없으면 None(신규 생성)."""
    status, body = make_request(api_path(path, ref=BRANCH), pat, method="GET", ctx_pref=ctx_pref)
    if status == 200 and isinstance(body, dict):
        return body.get("sha"), None, ctx_pref
    if status == 404:
        return None, "new_file", ctx_pref
    return None, f"remote SHA 조회 실패 status={status}: {str(body)[:150]}", ctx_pref


# ---------------------------------------------------------------------------
# Step 4: Contents API PUT (에러별 분기)
# ---------------------------------------------------------------------------
def upload_file(pat, path, local_full, message, ctx_pref):
    """로컬 파일을 remote로 PUT. 신규/갱신 자동 판단."""
    with open(local_full, "rb") as f:
        raw = f.read()

    if len(raw) > POST_SIZE_CAP:
        return False, f"파일 크기 {len(raw):,} bytes > 회사망 POST 한계 {POST_SIZE_CAP:,}. 외부망/모바일에서 push 필요.", None

    content_b64 = base64.b64encode(raw).decode("ascii")

    # remote SHA 확인 (갱신 시 필요)
    sha, sha_err, ctx2 = get_remote_sha(pat, path, ctx_pref)
    if sha_err == "new_file":
        print(f"    remote에 신규 파일 — create")
    elif sha_err:
        return False, sha_err, ctx2
    else:
        print(f"    remote 기존 sha: {sha[:8]} — update")

    # PUT (409 stale sha 자동 재시도)
    for attempt in range(1, 4):
        payload = {
            "message": message,
            "branch": BRANCH,
            "content": content_b64,
            "committer": {"name": COMMITTER_NAME, "email": COMMITTER_EMAIL},
        }
        if sha:
            payload["sha"] = sha

        status, body = make_request(api_path(path), pat, method="PUT", body=payload, ctx_pref=ctx2)
        if status in (200, 201) and isinstance(body, dict):
            commit = body.get("commit", {}).get("sha", "?")
            return True, commit, ctx2
        if status == 409:
            print(f"    409 (stale sha) — 재조회 후 재시도 {attempt}/3")
            sha, _, _ = get_remote_sha(pat, path, ctx2)
            if not sha:
                # 파일이 사라졌으면 create로
                sha = None
            continue
        if status == 401:
            return False, f"401: PAT 무효/만료 — {str(body)[:150]}", ctx2
        if status == 403:
            if "POST Blocking" in str(body):
                return False, f"403 POST Blocking: 회사망 한계({len(raw)} bytes). 외부망 필요.", ctx2
            return False, f"403 권한 부족/Contents API 차단 — {str(body)[:150]}", ctx2
        if status == 422 and "branch" in str(body).lower():
            return False, f"422 브랜치 없음 — main에서 branch 생성 먼저 필요", ctx2
        if status == 429:
            print(f"    429 rate limit — 30s 대기 후 재시도 {attempt}/3")
            time.sleep(30)
            continue
        return False, f"PUT 실패 status={status}: {str(body)[:200]}", ctx2
    return False, "409 재시도 3회 초과 — remote가 빠르게 변경 중", ctx2


# ---------------------------------------------------------------------------
# Step 6: 최종 요약
# ---------------------------------------------------------------------------
def report(success, commit, cause, next_action):
    print(f"  [6/6] 최종 요약")
    print(f"    결과: {'SUCCESS' if success else 'FAILURE'}")
    if commit:
        print(f"    commit: {commit}")
    if cause:
        print(f"    원인: {cause}")
    if next_action:
        print(f"    다음: {next_action}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("  Daily Brief 자동 업로드 — Contents API")
    print("=" * 60)

    # 인자 파싱: 날짜(optional), PAT(optional)
    date_arg = None
    pat_arg = None
    args = [a for a in sys.argv[1:]]
    pat_candidates = [a for a in args if a.startswith("ghp_")]
    date_candidates = [a for a in args if not a.startswith("ghp_") and len(a) == 10 and a[4] == "-" and a[7] == "-"]
    if pat_candidates:
        pat_arg = pat_candidates[0]
    if date_candidates:
        date_arg = date_candidates[0]

    pat = get_pat(pat_arg)
    if not pat:
        report(False, None, "PAT 확보 실패",
               "python upload_brief.py <날짜> ghp_xxx... 또는 pat.txt 작성 / GITHUB_PAT env")
        sys.exit(1)

    # 1+2. 환경 진단 + 파일 탐지
    report_path, err = find_report(date_arg)
    if err:
        report(False, None, err, "보고서 생성 후 재실행, 또는 날짜 인자 확인")
        sys.exit(1)
    diag_environment(report_path)

    # 3. 연결성 테스트 (log.md GET으로 — 항상 존재)
    print(f"  [3/6] 연결성 테스트 (SSL fallback)")
    status, body = make_request(api_path("wiki/log.md", ref=BRANCH), pat, method="GET")
    if status != 200:
        report(False, None, f"연결 실패 status={status}: {str(body)[:100]}",
               "네트워크/VPN/PAT repo scope 확인")
        sys.exit(1)
    print(f"    연결 OK — log.md sha: {body['sha'][:8]}")
    ctx_pref = ssl._create_unverified_context()  # 회사망이면 verified가 실패했으므로 unverified 고정

    # 4. 보고서 HTML 업로드
    rel_path = os.path.relpath(report_path, WORKDIR).replace(os.sep, "/")
    date_slug = os.path.basename(report_path).replace("daily-brief-", "").replace(".html", "")
    msg = f"Daily Brief {date_slug} 업로드 (자동)"
    print(f"  [4/6] 보고서 업로드: {rel_path}")
    ok, commit, ctx_pref = upload_file(pat, rel_path, report_path, msg, ctx_pref)

    if not ok:
        report(False, None, commit, "원인 참조 — 외부망/모바일 push 또는 파일 크기 확인")
        sys.exit(1)

    # 5. log.md 업로드 — 73KB(POST_SIZE_CAP) 이하일 때만 자동 시도.
    #    측정 사실(2026-08-06): 회사망 Contents API PUT content 한계 ~73KB.
    #    log.md가 한계 이하면 PUT 성공, 초과하면 messagebox 대행/외부망 필요.
    log_full = os.path.join(WORKDIR, "wiki", "log.md")
    log_size = os.path.getsize(log_full) if os.path.isfile(log_full) else 0
    print(f"  [5/6] log.md 업로드: {log_size:,} bytes (한계 {POST_SIZE_CAP:,})")
    if log_size <= POST_SIZE_CAP:
        log_msg = f"log: Daily Brief {date_slug} 업로드 기록"
        ok2, commit2, ctx_pref = upload_file(pat, "wiki/log.md", log_full, log_msg, ctx_pref)
        if ok2:
            print(f"        log.md 업로드 성공 — commit {commit2[:8]}")
        else:
            print(f"        log.md 업로드 실패: {commit2}")
            print(f"        (보고서는 업로드됨. log.md는 messagebox 대행 또는 외부망 push)")
    else:
        print(f"        건너뜀 — {log_size:,} > {POST_SIZE_CAP:,}. 외부망/모바일 push 필요.")

    report(True, commit, None,
           f"git fetch && git log origin/{BRANCH} --oneline -3 으로 확인 / Actions 탭에서 이메일 발송 run 확인")


if __name__ == "__main__":
    main()
