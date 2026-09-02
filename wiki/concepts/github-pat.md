---
name: github-pat
description: GitHub Personal Access Token 참조 — PAT 값은 코드/위키에 평문으로 적지 마라
metadata:
  type: reference
---

# GitHub PAT 참조

> **⚠️ 보안 규칙**: PAT 값(`ghp_...`)은 이 파일이나 코드/위키/커밋에 **절대
> 평문으로 적지 마라**. GitHub Secret scanning이 감지해 push를 차단한다.
> PAT는 아래 경로 중 하나로만 보관하고, 사용 시 환경변수로만 주입한다.

## PAT 보관 위치 (단일 출처)

- **PAT_90days.txt** (루트, `.gitignore`에 등록됨 — 절대 push 금지)
- 또는 git credential manager (Windows 자격 증명 관리자)
- 또는 `GITHUB_PAT` 환경변수

## 사용법 (값 노출 없이)

```bash
# 환경변수로 주입 — 명령행/로그에 PAT 값 안 나옴
GITHUB_PAT="$(cat PAT_90days.txt | tr -d '[:space:]')" python scripts/github_push.py --api-only --files <파일>
```

```python
# 스크립트 내 — get_pat() 6단계 폴백체인이 자동 추출 (env → credential manager → ...)
from github_push import get_pat
pat = get_pat()  # 값을 출력/로그에 적지 말 것
```

## Scope

- `repo`, `actions:secrets` (Classic PAT)

## 관련

- `scripts/github_push.py` — 순수 push 도구 (PAT 폴백체인 내장)
- `wiki/reference/github-connection-guide.md` — GitHub 접속 길라잡이 SSOT
- `github_config.py` — GitHub Secrets 읽기 헬퍼 (PAT는 이 파일에도 평문 금지)

## 이력

- 2026-09-02: 이전 버전에 PAT 평문이 적혀 있어 GitHub Secret scanning이
  push 차단 → PAT 값 제거, 보관 위치/사용법만 남김.
