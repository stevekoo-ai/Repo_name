---
title: Claude Code 사내 LLM 라우팅 & 재부팅 후 접속 복구
created: 2026-08-03
updated: 2026-08-03
tags: [claude-code, internal-llm, routing, recovery, ops]
---

이 저장소의 Claude Code는 Anthropic 공용 API가 아니라 **SK하이닉스 사내
LLM 게이트웨이**(`http://common.llm.skhynix.com`)로 라우팅된다. "JSON
고치니 API가 된다"는 현상의 실체, 그리고 재부팅/재시작 후 접속이
깨질 수 있는 시나리오와 복구 절차를 정리한 운용 페이지. 사용자가
회사 노트북(Windows 10 LTSC, 사내망)에서 Claude Code를 쓰는 환경이
전제다.

## 라우팅 설정의 실제 위치 (가장 중요)

| 파일 | 경로 | 역할 | 접속에 영향? |
|---|---|---|---|
| `.claude/settings.json` | 프로젝트 루트 | ⭐ **실제 라우팅 설정** — `env` 블록에 `ANTHROPIC_BASE_URL`, 모델 매핑, `ANTHROPIC_AUTH_TOKEN` | **YES (깨지면 접속 끊김)** |
| `.claude.json` | 홈 전역 (`C:\Users\2053437\`) | Claude Code 상태/통계 (numStartups, userID 등). **env 블록 없음** | NO |
| `.claude/settings.local.json` | 프로젝트 루트 | 권한 허용 목록 (Bash 허용 패턴) | NO (권한만 영향) |

**핵심 오해 정정**: "`.claude.json`을 고쳤다"고 인식했을 수 있으나, 실제
라우팅을 좌우하는 건 **`.claude/settings.json`의 `env` 블록**이다.
`.claude.json`을 아무리 고쳐도 env가 없으므로 접속에 무관하고, 반대로
이 파일을 고쳐선 안 된다.

### `.claude/settings.json`의 env 블록 구조 (2026-08-03 기준)

```json
"env": {
  "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "32000",
  "DISABLE_TELEMETRY": "1",
  "DISABLE_ERROR_REPORTING": "1",
  "DISABLE_FEEDBACK_COMMAND": "1",
  "CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY": "1",
  "ANTHROPIC_BASE_URL": "http://common.llm.skhynix.com",
  "ANTHROPIC_AUTH_TOKEN": "<본인 토큰 — 절대 위키/채팅에 노출 금지>",
  "ANTHROPIC_DEFAULT_OPUS_MODEL": "GLM-5.2[1m]",
  "ANTHROPIC_DEFAULT_SONNET_MODEL": "gemma-4-31B-it",
  "ANTHROPIC_DEFAULT_HAIKU_MODEL": "Qwen3.6-35B-A3B",
  "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000"
}
```

- `ANTHROPIC_BASE_URL`이 사내 게이트웨이를 가리킨다. 이 한 줄이 없으면
  Anthropic 공용 API로 연결을 시도해 사내망에선 실패한다.
- `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL`이 Claude의 3개 슬롯을
  사내 배포 모델로 매핑한다. 현재 이 세션의 런타임 모델은 `GLM-5.2[1m]`
  (Opus 슬롯)이다.
- 토큰은 절대 위키/채팅/코드에 노출하지 않는다 ([CLAUDE.md 9-2](../CLAUDE.md)
  시크릿 규칙 준수).

## 재부팅 후 접속 장애 시나리오 4가지

### ① 사내 게이트웨이 자체 장애 (가장 유력)
`http://common.llm.skhynix.com`은 사내망 HTTP 엔드포인트다. 재부팅 직후
가장 자주 걸리는 원인:
- VPN / 사내망 연결이 안 된 상태 (재부팅 직후 VPN 미연결)
- 게이트웨이 서버 점검 / 다운
- 방화벽 / 프록시 차단

**특징**: `settings.json`은 멀쩡한데 접속만 안 된다. "JSON을 고쳐도"
안 되는 패턴이면 십중팔구 이쪽이다.

### ② Claude Code 버전업 → 재온보딩 → settings.json 초기화
`.claude.json`에 `lastOnboardingVersion: 2.1.76`으로 기록된 반면,
현재 런타임 버전은 `2.1.220`이다. **버전이 다르면 재온보딩이
트리거되어 `settings.json`의 env 블록이 초기화될 위험이 있다.**
버전업 후 갑자기 접속이 안 되면 이 시나리오를 의심한다.

### ③ ANTHROPIC_AUTH_TOKEN 만료 / 교체
토큰이 사내 SSO 등에 연동되어 있다면 주기적 만료 가능. 설정은
살아있는데 401 반환. 이전에 "JSON을 고쳤다"는 게 실제로는 **토큰
재발급**이었을 가능성이 높다.

### ④ 사내 모델 식별자 변경
`GLM-5.2[1m]` / `gemma-4-31B-it` / `Qwen3.6-35B-A3B`는 사내에서
배포한 모델 식별자다. 사내에서 모델 버전 업데이트로 이 이름이
바뀌면 "model not found" 에러 발생. 게이트웨이는 응답하는데 모델만
못 찾는 패턴이면 이쪽.

## 재부팅 후 안 될 때 진단 순서

```bash
# 1단계: 설정 파일이 살아있는지
cat .claude/settings.json | grep ANTHROPIC_BASE_URL
# → http://common.llm.skhynix.com 이 없으면 시나리오 ② (초기화됨)

# 2단계: 게이트웨이가 응답하는지
curl -s -o /dev/null -w "%{http_code}" http://common.llm.skhynix.com
# → 응답 없으면 시나리오 ① (게이트웨이/망 문제)

# 3단계: 환경변수가 Claude Code에 반영됐는지
env | grep ANTHROPIC
# → ANTHROPIC_BASE_URL 이 없으면 settings.json 반영 실패

# 4단계: 에러 코드로 원인 분리
#   401 → 시나리오 ③ (토큰 만료) → 토큰 재발급 후 settings.json 갱신
#   "model not found" → 시나리오 ④ → 사내 모델명 최신값으로 갱신
#   연결 자체 실패 → 시나리오 ① → VPN/망 확인
#   settings.json 비었음 → 시나리오 ② → 백업에서 복구
```

## 예방 / 복구 자산

- **백업**: `.claude/settings.json`을
  `.claude/backups/settings.json.backup.1785731773`로 최초 백업
  (2026-08-03 생성). 기존엔 `.claude.json` 백업만 있었고 정작 중요한
  `settings.json` 백업은 없었음. env 블록이 날아가면 이 백업에서 복구:
  ```bash
  cp .claude/backups/settings.json.backup.1785731773 .claude/settings.json
  ```
  (단 토큰은 만료/교체될 수 있으니 복구 후 토큰만 최신값으로 갱신)
- **재온보딩 대비**: Claude Code 버전업 직후 한 번은
  `cat .claude/settings.json | grep BASE_URL`로 env 블록이 살아있는지
  확인하는 습관. 날아가 있으면 백업에서 복구.
## 관련 파일

- `.claude.json` — 홈 전역 상태 파일 (env 없음, 접속 무관)
- `.claude/settings.json` — ⭐ 라우팅 실체 (백업 필수)
- `.claude/settings.local.json` — 권한 허용 목록

## Sources

- 2026-08-03 사용자 요청: "재부팅 후 접속 안 될 수 있는지 자체 조사"
- `.claude/settings.json`, `.claude.json`, `.claude/settings.local.json`
  실제 검증 (2026-08-03)
- [CLAUDE.md 시크릿 관리 규칙](../CLAUDE.md)
