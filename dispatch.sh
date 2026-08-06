#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dispatch.sh — 헤드리스 Claude 자율 사이클의 발송 leg (B1).

로컬 HTML → gzip 압축 → base64 인코딩 → repository_dispatch POST
(client_payload.html_b64) 로 GitHub Actions를 트리거. Actions가
gunzip→이메일 발송.

이 스크립트는 Claude가 직접 curl을 조립하지 않도록 "Bash 도구 격리"
(사용자 가이드 주의점 1)를 위해 미리 작성된 것. Claude는
  bash dispatch.sh <html경로>
만 실행하면 됨.

73KB 우회 원리 (large-file-upload-bypass-ideas.md 안 1):
  - HTML은 마크업·CSS가 대부분 → gzip에 4~8배 축소
  - 원본 200KB → gzip ~40KB → base64 ~53KB → POST body < 64KB ✅
  - client_payload 한계 64KB (docs 검증: "less than 64KB", 10 properties, event_type 100자)

CLAUDE.md "진단형 테스트 스크립트" 프로토콜 준수 — 6단계:
  1. 환경 진단
  2. 파일/리소스 존재 확인
  3. 네트워크/연결성 (SSL fallback)
  4. 에러별 분기 (401/403/404/422/429)
  5. 대체 경로 폴백 (PAT 체인)
  6. 최종 요약 리포트

사용법:
  python dispatch.sh <html경로>                 # 기본
  python dispatch.sh <html경로> --event daily-brief
  python dispatch.sh <html경로> ghp_...          # PAT 직접 지정
  env GITHUB_PAT=ghp_... python dispatch.sh <html경로>

설정 (상단 CONFIG):
  REPO, EVENT_TYPE, BRANCH
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

# Windows 콘솔 cp949 인코딩이 em-dash 등을 못 그리므로 UTF-8 강제 (CLAUDE.md 코드 품질: 에러 원인 특정)
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
EVENT_TYPE = "send-brief"          # Actions on: repository_dispatch.types: [send-brief]
BRANCH = "claude/ai-agent-impl-002tip"  # 참조용 (dispatch 자체는 브랜치 무관, 워크플로우가 main에서 돎)
DISPATCH_URL = f"https://api.github.com/repos/{REPO}/dispatches"
WORKDIR = os.path.expanduser("~")

# client_payload 한계 (docs: "less than 64KB"). base64 인코딩 후 JSON 전체가 이 이하여야 함.
PAYLOAD_CAP = 63_000  # 안전 마진 (64KB 한계)

COMMITTER_NAME = "Daily Brief Bot"
COMMITTER_EMAIL = "noreply@anthropic.com"


# ---------------------------------------------------------------------------
# Step 5 (early): PAT 확보 — upload_brief.py와 동일한 폴백 체인 재사용
# ---------------------------------------------------------------------------
def get_pat(cli_arg):
    """우선순위: CLI 인자 → env var → git credential manager → clipboard → pat.txt → getpass."""
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

    print("  [1/6] PAT 확보 실패 — 어느 소스에서도 ghp_ 토큰을 찾지 못함")
    return None


# ---------------------------------------------------------------------------
# Step 1: 환경 진단
# ---------------------------------------------------------------------------
def diag_environment(html_path):
    print(f"  [2/6] 환경 진단")
    print(f"    OS: {platform.system()} {platform.release()}")
    print(f"    Python: {platform.python_version()}")
    print(f"    Repo: {REPO}")
    print(f"    Event type: {EVENT_TYPE}")
    print(f"    HTML: {html_path} ({os.path.getsize(html_path):,} bytes 원본)")
    print(f"    SSL unverified fallback available: {hasattr(ssl, '_create_unverified_context')}")


# ---------------------------------------------------------------------------
# Step 3: 네트워크 — SSL fallback request helper (upload_brief.py 재사용)
# ---------------------------------------------------------------------------
def make_request(url, pat, method="GET", body=None, ctx_pref=None):
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "dispatch-bot",
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
def encode_html(html_path):
    """HTML → gzip binary → base64 ASCII. 압축률과 크기 출력."""
    with open(html_path, "rb") as f:
        raw = f.read()
    gz = gzip.compress(raw, compresslevel=9)
    b64 = base64.b64encode(gz).decode("ascii")
    print(f"    원본 {len(raw):,} → gzip {len(gz):,} (×{len(raw)/max(len(gz),1):.1f}) → base64 {len(b64):,}")
    return b64, len(raw), len(gz)


# ---------------------------------------------------------------------------
# Step 2+4: dispatch POST (에러별 분기)
# ---------------------------------------------------------------------------
def send_dispatch(pat, html_b64, date_slug, ctx_pref):
    """repository_dispatch POST. client_payload.html_b64에 압축 HTML 탑재."""
    # payload 크기 사전 점검 (Step 2 리소스 확인의 일부)
    if len(html_b64) > PAYLOAD_CAP:
        return False, (
            f"압축+base64 후 {len(html_b64):,} bytes > client_payload 한계 {PAYLOAD_CAP:,}. "
            f"원본이 너무 큼 — 안 2(gzip+Git Data blob chunk) 폴백 필요."
        )

    payload = {
        "event_type": EVENT_TYPE,
        "client_payload": {
            "date": date_slug,
            "html_b64": html_b64,
            "encoding": "gzip+base64",  # Actions 복원 힌트
        },
    }
    body_size = len(json.dumps(payload).encode("utf-8"))
    print(f"    POST body 총 {body_size:,} bytes (한계 {PAYLOAD_CAP:,})")

    # Step 4: 에러별 분기
    for attempt in range(1, 4):
        status, body = make_request(DISPATCH_URL, pat, method="POST", body=payload, ctx_pref=ctx_pref)
        if status == 204:
            return True, "204 No Content — dispatch 수신됨"
        if status == 401:
            return False, f"401: PAT 무효/만료 — {str(body)[:150]}"
        if status == 403:
            if "POST Blocking" in str(body):
                return False, (
                    f"403 POST Blocking: 회사망 한계. 압축해도 {body_size:,} bytes로 막힘 — "
                    f"안 2(chunk) 폴백 또는 외부망 필요."
                )
            return False, f"403 권한 부족 — {str(body)[:150]}"
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
# Step 6: 최종 요약
# ---------------------------------------------------------------------------
def report(success, detail, next_action):
    print(f"  [6/6] 최종 요약")
    print(f"    결과: {'SUCCESS' if success else 'FAILURE'}")
    if detail:
        print(f"    상세: {detail}")
    if next_action:
        print(f"    다음: {next_action}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("  dispatch.sh — gzip+base64 → repository_dispatch")
    print("=" * 60)

    args = [a for a in sys.argv[1:] if a != "--event"]
    # --event <type> 처리
    event_override = None
    if "--event" in sys.argv:
        idx = sys.argv.index("--event")
        if idx + 1 < len(sys.argv):
            event_override = sys.argv[idx + 1]
    global EVENT_TYPE
    if event_override:
        EVENT_TYPE = event_override

    # 인자 파싱: html경로(필수), PAT(optional)
    pat_candidates = [a for a in args if a.startswith("ghp_")]
    html_candidates = [a for a in args if not a.startswith("ghp_") and a.endswith(".html")]
    if not html_candidates:
        report(False, None, "HTML 파일 경로 인자 필요", "python dispatch.sh <html경로>")
        sys.exit(1)
    html_path = os.path.abspath(html_candidates[0])
    if not os.path.isfile(html_path):
        report(False, None, f"파일 없음: {html_path}", "HTML 생성 후 재실행")
        sys.exit(1)

    pat_arg = pat_candidates[0] if pat_candidates else None
    pat = get_pat(pat_arg)
    if not pat:
        report(False, None, "PAT 확보 실패",
               "GITHUB_PAT env / pat.txt / 인자 ghp_... 확인")
        sys.exit(1)

    diag_environment(html_path)

    # Step 3: 연결성 (repo 정보 GET)
    print(f"  [3/6] 연결성 테스트 (SSL fallback)")
    status, body = make_request(f"https://api.github.com/repos/{REPO}", pat, method="GET")
    if status != 200:
        report(False, None, f"연결 실패 status={status}: {str(body)[:100]}",
               "네트워크/VPN/PAT repo scope 확인")
        sys.exit(1)
    print(f"    연결 OK — repo: {body.get('full_name', REPO)}")
    ctx_pref = ssl._create_unverified_context()  # 회사망이면 verified 실패하므로 unverified 고정

    # 핵심: gzip + base64 인코딩
    print(f"  [4/6] gzip 압축")
    html_b64, orig_size, gz_size = encode_html(html_path)

    # date_slug: 파일명에서 추출 (daily-brief-YYYY-MM-DD.html → YYYY-MM-DD), 없으면 오늘
    import datetime
    base = os.path.basename(html_path).replace(".html", "")
    date_slug = base.split("-")[-3:] if "daily-brief-" in base else datetime.date.today().isoformat()
    if isinstance(date_slug, list):
        date_slug = "-".join(date_slug)

    # Step 4: dispatch POST
    print(f"  [5/6] dispatch POST (event_type={EVENT_TYPE})")
    ok, detail = send_dispatch(pat, html_b64, date_slug, ctx_pref)
    if not ok:
        report(False, detail, "원인 참조 — 안 2(chunk) 폴백 또는 외부망")
        sys.exit(1)

    report(True, detail,
           f"GitHub Actions 탭에서 '{EVENT_TYPE}' 워크플로우 run 확인 / 이메일 수신 대기")


if __name__ == "__main__":
    main()
