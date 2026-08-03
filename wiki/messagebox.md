---
title: 메세지박스 (동기화 전 필수 확인 게시판)
created: 2026-08-03
updated: 2026-08-03
tags: [messagebox, sync, multi-client, ops, priority]
---

> ⚠️ **이 파일은 sync 직전 가장 먼저 읽어야 할 우선 게시판이다.**
> 양쪽 클라이언트(mobile/desktop) 모두 세션 시작 시, 그리고 GitHub
> 동기화(push/pull) 전에 반드시 이 파일을 가장 먼저 확인한다
> ([CLAUDE.md 9-4](../CLAUDE.md) 규칙). log.md와 다르게 **현재 유효한
> 공지만** 남긴다 — 해결/전달된 항목은 작성자가 clear 처리한다.

## 사용 규칙

- **누가 쓰나**: 큰 변화를 준 클라이언트가 다른 쪽에게 알리려고 게시.
- **언제 지우나**: 내용이 상대에게 전달되면 작성자가 다음 메시지로
  교체. log.md처럼 무한히 쌓지 않는다 — "지금 유효한 것"만 남긴다.
- **심각도 배지**: 🔴 HALT / 🟡 CAUTION / 🟦 INFO (아래 의미).
- **만료 시각**: 각 메시지는 `expires` 시각을 표기. 지난 메시지는
  죽은 것으로 간주해 무시 가능 (한쪽이 비정상 종료돼도 다른 쪽이
  멈추지 않는 안전장치).
- **잠금과의 관계**: 이 파일은 사람용 게시판. 기계용 잠금
  (`.wiki/active-session.json`)은 별개로 동작한다 — 큰 작업 전 잠금을
  걸고 여기에 게시까지 하는 식으로 조합해 쓴다.

## 심각도 배지 의미

| 배지 | 의미 | sync 동작 |
|---|---|---|
| 🔴 HALT | "이 영역, 당분간 건드리지 마" (rebase/기준선 재정렬 진행 중) | 활성 HALT가 있으면 sync 대기 |
| 🟡 CAUTION | "큰 변경 진행 중, 쓰기 전 반드시 pull 먼저" | pull 후 진행 |
| 🟦 INFO | "참고용, 방금 큰 커밋 하나 떨어졌어" | 그냥 읽고 진행 |

## 현재 메시지

<!-- 새 메시지는 아래 양식을 복사해 위에 추가. 가장 최근가 맨 위. -->
<!--
### [배지] 한 줄 제목 — <client> <UTC 시각>

- **who**: mobile / desktop
- **when_utc**: YYYY-MM-DDTHH:MM:SSZ
- **expires_utc**: YYYY-MM-DDTHH:MM:SSZ (일반적 24h)
- **what**: 무슨 큰 변화를 줬는지 서술
- **read_first**: 모바일이 다음 세션에서 가장 먼저 읽어야 할 파일/맥락
- **status**: active / acknowledged

-->
### 🟦 기준선 확립 + 메세지박스 프로토콜 신설 — desktop 2026-08-03T15:50Z

- **who**: desktop
- **when_utc**: 2026-08-03T15:50:00Z
- **expires_utc**: 2026-08-04T15:50:00Z
- **what**: desktop 세션이 remote 서사 브랜치(claude/ai-agent-impl-002tip, HEAD 2ff971e) 기준으로 로컬을 reset --hard 동기화. README가 설명한 PEOS 전체 구조(core/collectors/engine/config/tests/report/data, 444개 파일)가 로컬에 생성됨 — 이전엔 scripts/ 일부만 있었음. 동시에 이 메세지박스 프로토콜과 CLAUDE.md 9-4 규칙 신설. 신규 concept 2개(사내 LLM 라우팅, 다중 클라이언트 충돌 방지) 추가됨.
- **read_first**: 모바일은 다음 pull 후 (1) 본 메세지박스, (2) [concepts/multi-client-conflict-prevention.md](concepts/multi-client-conflict-prevention.md) — 앞으로 양쪽 git 직접 조작 충돌 방지 규칙, (3) [concepts/claude-code-internal-routing.md](concepts/claude-code-internal-routing.md) — 재부팅 후 접속 복구 절차, (4) [CLAUDE.md 9-4](../CLAUDE.md) — 새로 추가된 sync 전 messagebox 확인 규칙.
- **status**: active

## Sources

- 2026-08-03 사용자 요청: "메세지박스 하나 만들어 — 아주 큰 변화 있을 때 sync 전 우선 참고 구조"
- [다중 클라이언트 충돌 방지 운영](concepts/multi-client-conflict-prevention.md)
- [CLAUDE.md 9-4 메세지박스 규칙](../CLAUDE.md)
