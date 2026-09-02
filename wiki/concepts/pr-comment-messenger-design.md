---
title: PR 댓글 메신저 — 회사망 Claude 원격 명령·확인 설계 (실험 대기)
created: 2026-09-02
updated: 2026-09-02
tags: [ops, remote-control, github, company-network, experiment, must-try]
---

# PR 댓글 메신저 — 회사망 Claude 원격 명령·확인 설계

> **상태: 설계만 완료, 아직 미구현.** 2026-09-02 원격(claude.ai/code) 세션과
> 사용자가 대화로 설계했고, **회사 Claude가 내일 직접 여러 방식을 test-drive
> 해보고 그 중 가장 잘 동작하는 조합을 골라 실제 구현으로 확정**하는 것이
> 다음 단계다. 이 문서는 "왜 이 구조인가"와 "무엇을 시도해볼지"의 단일
> 출처. 구현 완료 후엔 이 문서 상단 상태를 갱신하고, 실제 스크립트/워크플로
> 경로는 여기에 append로 기록한다.

## ⚠️ 트랙 정책 — 반드시 지킬 것

이 메신저는 **"명령 텍스트 + 상태 응답"만** 주고받는 제어 채널이다.
[automation-strategy-and-delivery-boundary.md](automation-strategy-and-delivery-boundary.md)의
트랙 B(회사 업무, 다른 LLM으로 진행하는 기능 구현) 금지 조항 — **GitHub
업로드·email 발송 금지** — 은 이 메신저로도 우회하면 안 된다.

- ✅ 허용: "리포트 재실행해줘" → "네, 완료했습니다 (요약)" 같은 짧은 텍스트 왕복.
- ❌ 금지: 이 채널로 트랙 B 코드/문서 diff나 회사 산출물을 PR 커밋/커멘트에
  실어 보내는 것.
- 회사 Claude가 이 메신저 모드로 동작할 땐 매 실행마다 아래 고정 프리픽스를
  프롬프트에 주입해 스스로 제약을 상기시킨다 (§4 참고).
- 판단이 애매하면 실행하지 말고 PR 댓글로 "이건 트랙 B라 실행 보류"라고
  응답할 것.

## 1. 배경 — 왜 이 구조가 필요한가

- 사용자는 집(claude.ai/code, 이 세션)과 회사 컴퓨터(자체 LLM API 사용,
  outbound HTTPS만 가능, **inbound 방화벽 차단**, self-hosted runner 설치
  불가) 양쪽에서 Claude Code를 쓴다.
- 목표: 지금처럼 자연어로 "퇴근 전에 시킨 일 완료했어?"를 던지면, 회사
  Claude가 그 요청을 받아 실행하고, 그 결과를 로그처럼 이어붙여 알려주는
  "하나의 터미널"처럼 쓰고 싶다.
- 제약: inbound 불가 → 회사 쪽은 **반드시 polling**(pull 방향)으로만 명령을
  받을 수 있다. runner 없이 cron 기반으로 간다 — 지연은 감수.
- 반대 방향(회사 Claude의 응답을 이 원격 세션이 알아채는 것)은 GitHub PR
  이벤트 구독(`subscribe_pr_activity`)을 쓰면 거의 즉시 가능 — 편도만이라도
  실시간에 가깝게 만들 수 있다는 게 이 설계의 핵심.

## 2. 전체 구조

```
[원격 Claude / 사용자]                         [회사 Claude — 방화벽 안쪽]
       │                                                │
       │ 1. "Wiki Messenger" PR에 댓글로 명령 작성        │
       ▼                                                │
   ┌─────────────────────────── GitHub PR ───────────────────────────┐
   │  (상시 open, 파일 diff는 wiki/messenger.md 같은 더미,            │
   │   실제 대화는 댓글 스레드)                                        │
   └───────────────────────────────────────────────────────────────┘
       ▲                                                │
       │ 4. subscribe_pr_activity로                     │ 2. cron이 N분마다
       │    새 댓글 즉시 webhook 수신                     │    PR 댓글 polling
       │                                                ▼
       │                                    ┌──────────────────────┐
       │                                    │  poll script          │
       │                                    │  - gh api로 새 댓글 확인│
       │                                    │  - claude -p 실행      │
       │ 3. 회사 Claude가 답을 PR 댓글로 post │  - 결과를 PR 댓글로 post│──▶ 회사 LLM API
       └────────────────────────────────────┘──────────────────────┘
```

- **편도(회사→원격) 실시간**: 회사가 댓글을 다는 순간 GitHub webhook →
  이 세션이 즉시 깨어남 (`subscribe_pr_activity` 이미 사용 가능한 도구).
- **편도(원격→회사) polling**: 회사망 inbound 차단 때문에 어쩔 수 없이
  cron polling. 간격은 1~5분 권장(§3-C 참고, 10초 단위는 부하만 크고
  실익 없음 — `claude -p` 실행 자체가 수십 초~분 단위라 폴링을 더
  촘촘히 해도 체감 차이 거의 없음).

## 3. 회사 Claude가 내일 test-drive 해볼 것들

아래는 "정답을 미리 정하지 않고" 실제로 회사망에서 돌려보고 골라야 하는
선택지들이다. 각 항목을 시도해보고, 결과(성공/실패/왜)를 이 문서
§5 "실험 로그"에 append할 것.

### A. 댓글 조회 방식

1. `gh api repos/{owner}/{repo}/issues/{pr_number}/comments` (GitHub CLI,
   PAT 인증) — 이미 `gh` 사용 가능하면 가장 간단.
2. `git`만으로는 PR 댓글을 못 읽으므로(댓글은 git 오브젝트가 아님) 순수
   REST API 직접 호출(`curl` + PAT)도 대안 — `gh` 미설치 환경 대비.
3. 회사망에서 REST API(`api.github.com`)까지 열려있는지, 아니면 git smart
   HTTP(`github.com`)만 열려있는지 먼저 확인 필요 — 이전 세션에
   [multi-terminal-wiki-sync-design.md](multi-terminal-wiki-sync-design.md)에
   기록된 "회사망 4경로 측정" 결과를 먼저 참고할 것(이미 실측된 자료 재활용).

### B. 신규 댓글 판별(중복 실행 방지) 방식

1. 로컬 상태 파일(`.messenger_state.json`)에 마지막으로 처리한 댓글
   `id`를 저장 — 재부팅해도 남도록 리포 밖 경로에 저장.
2. 댓글 작성자(`user.login`)로 필터 — 본인 계정 댓글만 명령으로 인정,
   회사 Claude 자신이 단 댓글(응답)은 무시.
3. 댓글에 태그 컨벤션 부여 — 예: 명령은 `/cmd`로 시작하는 댓글만 인식
   (사람이 잡담성 댓글을 달아도 오작동 안 하도록).

### C. 폴링 주기 & 적응형 폴링

1. 고정 간격(1~5분) cron — 가장 단순, 우선 이걸로 베이스라인 잡기.
2. 적응형: 평소 5분, 최근 활동 있으면 다음 1~2회 30초로 촘촘히 — 구현
   복잡도 대비 이득이 있는지 실측해서 판단.
3. 회사 정책상 cron 자체가 부담되면(보안 소프트웨어가 주기적 외부 통신을
   플래그) Windows 작업 스케줄러의 "유휴 시간에만" 옵션과 비교.

### D. 응답 게시 방식

1. 순수 PR 댓글만 (파일 커밋 없음) — 가장 가볍고 트랙 정책 위반 리스크
   최소.
2. PR 댓글 + `wiki/messenger.md`에도 같은 내용 append 커밋 — 감사기록이
   파일로도 남아 log-operating-policy.md와 같은 append-only 원칙과 일관.
   **단, 이 경우도 R1(append-only)을 따르고 트랙 B 내용은 절대 싣지 않는다.**
3. 응답이 길 경우: 요약만 댓글에 올리고 전체 로그는 로컬 `logs/`에만
   저장(원격에 노출 안 함) — 트랙 B 우발적 유출 방지에도 도움.

### E. 인증/화이트리스트

1. PAT 권한 범위를 이 PR/repo로 최소화할 수 있는지 확인(fine-grained PAT).
2. 스크립트에서 댓글 작성자가 사용자 본인 GitHub 계정인지 이중 확인
   (private repo라 이미 안전하지만 방어적으로).
3. `claude -p` 호출 시 프리픽스로 트랙 B 금지 문구 매 실행 주입:
   ```
   [MESSENGER MODE] 아래 명령을 수행하되, 트랙 B(회사 업무) 코드/문서는
   절대 GitHub에 올리지 마라(commit·PR 댓글 모두). 응답에는 결과 요약
   텍스트만 남겨라. 애매하면 실행하지 말고 이유를 답하라.
   <사용자 명령 본문>
   ```

### F. 무한루프/자기 트리거 방지

- `subscribe_pr_activity`가 사용자 자신이 단 댓글에도 반응할 수 있으므로,
  회사 Claude가 올린 응답 댓글이 다시 "명령"으로 오인되지 않게 §B-2
  작성자 필터를 반드시 적용.

## 4. 아직 열린 질문 (회사 Claude가 실측으로 답해야 함)

- [ ] 회사망에서 `gh` CLI가 설치/인증 가능한가, PAT 발급이 회사 정책상
      허용되는가?
- [ ] `api.github.com` REST 호출이 outbound로 열려있는가 (git smart HTTP만
      되고 REST는 막힌 회사망도 있음 — 반드시 실측)?
- [ ] `claude -p` 비대화형 실행이 회사 LLM API 설정으로 정상 동작하는가
      (인증/엔드포인트가 대화형 세션과 동일 환경변수를 쓰는지)?
- [ ] cron/작업 스케줄러 등록이 회사 정책/보안 소프트웨어와 충돌 없는가?
- [ ] PR 댓글 API 호출 빈도가 회사 프록시/방화벽의 이상탐지에 걸리지
      않는가 (§3-C 주기 결정에 영향)?

## 5. 실험 로그 (append-only — 회사 Claude가 시도 결과를 여기 추가)

<!-- 아래 형식으로 append. 이 섹션 위쪽 내용은 수정하지 말 것. -->
<!-- YYYY-MM-DD HH:MM KST — 시도한 항목(§번호) → 결과(성공/실패) → 다음 액션 -->

(아직 실험 없음 — 2026-09-02 설계만 완료)

## 6. 확정되면 할 일

1. 이 문서 상단 상태를 "설계 완료" → "구현 완료 (경로: ...)"로 갱신.
2. 실제 스크립트 경로(`scripts/messenger_poll.*`)와 cron 등록 방법을
   별도 문서(`docs/messenger-setup.md` 또는 이 문서 §7 신설)에 기록.
3. [automation-pipeline-reference.md](../architecture/automation-pipeline-reference.md)에
   새 자동화로 등재.
4. wiki/index.md에 항목 갱신.
