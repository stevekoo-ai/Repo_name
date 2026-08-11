---
title: 메세지박스 (동기화 전 필수 확인 게시판)
created: 2026-08-03
updated: 2026-08-06
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

### 🟡 정정: schtasks LogSummarize 등록 완료 (이전 "미등록" 기술 오류) — desktop 2026-08-10T11:52Z

- **who**: desktop
- **when_utc**: 2026-08-10T11:52:00Z
- **expires_utc**: 2026-08-24T00:00:00Z
- **what**: **이전 메시지(01:30Z)의 "schtasks 미등록" 기술은 오류.** 실측 정정: `schtasks /query /tn LogSummarize /v`(Python subprocess, cp949→UTF-8)로 **`LogSummarize` 태스크 등록 확정** — 매일 00:40 KST, 실행 작업 `log_summarize_routine.bat`, 다음 실행 2026-08-11 00:40. **8/8·8/9·8/10 매일 자동 실행 실증**(`.claude/logs/log-summary-2026MMDD-004005.log`, `claude -p` rc=0, 64~191s 정상 응답, 빈 stdout 해결 적용됨). 오류 원인: Git Bash(MSYS)가 schtasks의 `/query` `/tn` 플래그를 경로로 변환해 query가 실패했고, 이를 "미등록"으로 오해. Python subprocess로 호출하면 정상. 5개 파일 정정: `log-operating-policy.md`(3층 표+비고), `log-rotation-3hybrid-infra.md`(표+섹션+미구현→완료), `index.md`(ops 포인터 2곳), 이전 messagebox 메시지(이력 보존), `log.md`(정정 기록). **3층 전부 가동 중 — GitHub 층 cut(00:20) + Windows 층 요약(00:40) + live 안전망.**
- **read_first**: [concepts/log-operating-policy.md](concepts/log-operating-policy.md) "Windows 층 비고"(정정됨), [concepts/log-rotation-3hybrid-infra.md](concepts/log-rotation-3hybrid-infra.md) "완료" 섹션
- **action_for_other_terminals**: (1) **이전 메시지(01:30Z)의 "Windows 층 자동 실행 안 된다"는 무시** — 실제론 8/8~8/10 자동 실행됨. (2) **R1~R6 자체는 유효** — log 쓸 때 `## 당일 log` 맨 아래 append, 과거/요약 섹션 건드리지 마라. (3) schtasks 확인은 Git Bash 직접 호출 말고 `python -c "import subprocess; ..."` 로(PowerShell도 cp949 깨짐). (4) 충돌 위험 없음 — 5개 파일만 변경, 다른 작업과 겹치는 파일 없음.
- **status**: active

### 🟦 Log 운영 정책 concept 신설 + 인프라 페이지 실측 상태 반영 — desktop 2026-08-10T01:30Z

- **who**: desktop
- **when_utc**: 2026-08-10T01:30:00Z
- **expires_utc**: 2026-08-24T00:00:00Z
- **what**: 모든 Agent가 `wiki/log.md`를 쓸 때 지킬 운영 정책을 자급자족형 단일 concept 페이지로 정리 + log-rotate 인프라 페이지를 실측 상태로 갱신. (1) **신규 [concepts/log-operating-policy.md](concepts/log-operating-policy.md)** — TL;DR(3줄) + log.md 3-tier 구조(누가 갱신/Agent가 해도 되는가) + R1~R6 핵심 규칙(append-only 맨 아래, 과거 cut 금지, 요약 섹션 건드리지 마라, 회전 전 load-bearing 확인, 한 줄 KST, 동시 Agent 고려) + 3층 자동화가 하는 일 + graceful degradation 표 + 아카이브 2-tier + "돌고 있는지" 확인 4곳 + 금지 사항 + 회사망 업로드 우회. log 운영 규칙·degradation 표의 **단일 출처**. (2) **갱신 [concepts/log-rotation-3hybrid-infra.md](concepts/log-rotation-3hybrid-infra.md)** — Windows 층 상태를 실측 기반으로 정확화: ❌미등록 → ⚠️스크립트 완성·수동검증 완료(빈 stdout 해결), **schtasks 미등록**(`register_log_summarize_task.py` 있으나 실행 안 됨, `schtasks /query`로 LogSummarize 부재 확인). CLAUDE.md "Log rotation" 참조(구버전) → log-operating-policy.md로 변경. (3) **갱신 [index.md](index.md)** ops 섹션 — log-operating-policy.md 포인터 최상단 추가, infra 포인터 상태 정확화. (4) **갱신 [CLAUDE.md](../CLAUDE.md)** Startup Protocol #4 — log.md 읽기 전 log-operating-policy.md 먼저 읽도록 R1~R6 요약 포인터 추가.
- **read_first**: [concepts/log-operating-policy.md](concepts/log-operating-policy.md) (핵심 — Agent가 log 쓰는 법), [concepts/log-rotation-3hybrid-infra.md](concepts/log-rotation-3hybrid-infra.md) (인프라 산출물·배포 상태), [CLAUDE.md](../CLAUDE.md) Startup Protocol #4
- **action_for_other_terminals** ⚠️: (1) **충돌 위험 없음** — 4개 파일(신규 1 + 갱신 3)만 변경, 다른 작업과 겹치는 파일 없음. pull 시 자동 병합. (2) **다음 세션부터 log 쓸 때 R1~R6 준수** — `## 당일 log` 맨 아래에만 한 줄 append, 과거 항목/요약 섹션 건드리지 마라. (3) **Windows 층 자동 실행은 아직 안 돈다** — schtasks 등록 필요 시 `python scripts/register_log_summarize_task.py` 실행(00:40 KST 매일). 그 전엔 `## 당월 요약` 갱신 수동. (4) CLAUDE.md 구버전 "Wiki schema"의 "Log rotation" 섹션은 8/8 마이그레이션으로 사라짐 — log 운영 규칙은 이제 log-operating-policy.md가 단일 출처.
- **status**: active

### 🟦 ARCHITECTURE MIGRATION COMPLETE: 4-Layer Wiki Restructuring (Phase 1-3) — claude 2026-08-08T12:00Z

**✅ STATUS: COMPLETE — 다른 Agent들이 이해해야 할 모든 변경사항 정리**

#### 무엇이 바뀌었나? (최소한 알아야 할 것)

**레이어 구조 (이전 → 현재)**:
- 이전: 2-layer (entities/ + concepts/) — 데이터 중복 문제 → Single Source of Truth 위반
- 현재: 4-layer (Entity/Journal + Concept/Monitoring) — 각 레이어 역할 분담, 중복 제거 ✅

**구체적 변경**:
1. **`wiki/monitoring/` 폴더 신규 생성** (7개 monitoring-status.md 파일)
   - `hbm-cycle-score-status.md` (일일 점수)
   - `panic-recovery-signals-status.md` (일일 체크)
   - `market-cycles-leverage-risk-status.md` (일일 신호)
   - `sk-hynix-analyst-thesis-checkpoints-status.md` (일일 검증)
   - `trump-midterm-tracker-status.md` (일일 추적)
   - `situational-awareness-fund-liquidation-status.md` (이벤트 타임라인)
   - `macro-regime-history-status.md` (일일 국면)

2. **7개 concept 파일에서 모든 dated entries 제거** ✅
   - 이전: `concepts/hbm-cycle-score.md`에 "2026-07-24 체크", "2026-07-25 체크" ... 100+ 줄
   - 현재: `concepts/hbm-cycle-score.md`는 **프레임워크 정의만** (6 axes, collapse conditions, methodology)
   - 모든 dated 체크 데이터는 `monitoring/hbm-cycle-score-status.md`에만 존재

3. **`wiki/entity-journals/` 폴더** (Phase 1에서 완성)
   - `entity-journals/sk-hynix-journal.md` (모든 상태 변화 타임라인, append-only)

#### 이제 각 레이어의 역할

| Layer | 파일 위치 | 내용 | 특징 |
|---|---|---|---|
| **Entity** | `entities/sk-hynix.md` | 현재 상태만 | 단일 snapshot, ~300 lines |
| **Entity-Journal** | `entity-journals/sk-hynix-journal.md` | 역사 타임라인 | Append-only, 역시간순 |
| **Concept** | `concepts/hbm-cycle-score.md` | 프레임워크 정의 | Framework only, 변경 드뭄 |
| **Monitoring** | `monitoring/hbm-cycle-score-status.md` | 일일 추적 상태 | Append-only, 매일 갱신 |

#### 다른 Agent들이 지금부터 해야 할 것

**✅ 반드시 알고 시작할 것 (읽어야 할 순서)**:
1. **`wiki/index.md`** — monitoring 섹션 신규 확인, 각 concept의 "→ [일일 추적]" 링크 보기
2. **`wiki/concepts/knowledge-model.md`** — 4-layer 구조와 reading paths (5가지 workflow)
3. **`CLAUDE.md`** — 다음 섹션들:
   - "Wiki structure (4-layer architecture)" — 폴더 구조 이해
   - "Page conventions (layer-specific updated semantics)" — 각 파일의 frontmatter `updated` 필드 의미
   - "/lint workflow" — 4-layer compliance 자동 검사 (`/lint wiki/`)
   - "/ingest workflow" — 새 소스 추가 시 4-layer 페어링 자동 생성

**⚠️ 워크플로우 변경**:

| 워크플로우 | 이전 | 현재 |
|---|---|---|
| **/lint** | concept 파일의 dated table 찾기 | 자동으로 4-layer compliance 검사 ✅ |
| **/query** | concept만 검색 | concept + monitoring 자동 검색 |
| **/ingest** | entity 또는 concept 하나 선택 | Layer 1+2 (entity+journal) 또는 Layer 3+4 (concept+monitoring) 페어 생성 |

**예시** (이전 vs 현재):
```
이전: "SK하이닉스 2026-08-06 주가?" 
→ entities/sk-hynix.md (현재상태) + entity-journals/sk-hynix-journal.md 읽기

현재: "HBM Cycle Score 2026-08-06 점수?"
→ monitoring/hbm-cycle-score-status.md (일일 데이터) + concepts/hbm-cycle-score.md (framework 정의) 읽기
```

**중요: Framework vs Tracking 구분**:
- "HBM Cycle Score의 6개 축이 뭐야?" → `concepts/hbm-cycle-score.md` 읽기
- "HBM Cycle Score 어제는 몇 점?" → `monitoring/hbm-cycle-score-status.md` 읽기
- "Concept을 수정하고 싶어" → 3회+ 반복 + 가정 위반 등 4-condition rule 확인 → `concepts/concept-lifecycle-maturity.md` 참고

#### Phase 4는 없다 (왜인가?)

✅ **4-layer 아키텍처는 완성 상태**:
- Concept-Monitoring 페어 7개 × 완성
- Entity-Journal 1개 × 완성 (SK하이닉스, 다른 entities는 현재 단일 상태라 journal 불필요)
- Single Source of Truth 100% 준수 (lint audit 통과)
- 모든 cross-link 양방향 검증 완료

**선택적 미래 작업** (필요 시 다음 세션):
- (Optional) 다른 entities (portfolio, user-profile 등)도 entity-journal로 마이그레이션 (현재는 상태 변화 빈번하지 않아 불필요)
- (Optional) Legacy `-history/` 폴더들 정리 (현재는 rotation 시 일시적으로 남음)
- (Automated) `/lint` hook을 GitHub Actions에 연동 (현재는 수동 실행)

#### 실제 영향: "내가 뭘 달라 느낄까?"

✅ **Session 시작 시**:
```bash
git pull origin claude/ai-agent-impl-002tip
# 이전처럼 동작하되, 이제 monitoring/ 폴더 7개 파일이 추가됨
# (concepts/에서 dated 엔트리는 모두 사라짐)
```

✅ **/lint 실행 시**:
```
# 이전: "concepts/*.md에 | **2026-08-06 dated row 있음" 같은 경고
# 현재: "✅ All 4-layer checks passed!" (0 violations)
```

✅ **새 내용 작성 시** (`/ingest`):
```
# 이전: Entity 또는 Concept 중 하나만 선택
# 현재: "Entity+Journal" 또는 "Concept+Monitoring" 페어 자동 생성 + 양방향 링크 자동
```

#### Debugging Checklist (문제 생겼을 때)

- ❓ "concept 파일에 dated row가 남아있어?" → 4-layer migration 누락, `/lint` 재검사
- ❓ "monitoring 페이지를 못 찾아?" → `wiki/index.md` monitoring 섹션 확인, 양방향 링크 누락 가능
- ❓ "Entity-journal이 안 생겼어?" → Layer 2 마이그레이션은 현재 SK하이닉스만 완성, 필요 시 사용자 요청

#### 설계 문서 (더 알고 싶을 때)

- `wiki/concepts/knowledge-model.md` — 4-layer 아키텍처 목적과 reading paths
- `wiki/concepts/entity-lifecycle-maturity.md` — Entity가 Mention → Mature로 가는 과정
- `wiki/concepts/reporting-framework.md` — Wiki data → Reports 흐름도
- `wiki/concepts/decision-intelligence.md` — 의사결정 시 어느 레이어를 읽을지

---

- **who**: claude (claude/ai-agent-impl-002tip)
- **when_utc**: 2026-08-08T12:00:00Z
- **expires_utc**: 2026-08-22T00:00:00Z
- **status**: active
- **action_for_other_agents**: 
  1. Pull 후 wiki/index.md 확인 (monitoring 섹션 신규)
  2. 다음 `/lint`, `/query`, `/ingest` 사용 시 위 표 참고
  3. 문제 시 위 Debugging Checklist 확인
### Steve's Wiki Architecture v1 도입 완료 — desktop 2026-08-08Txx:xxZ
- who: desktop
- when_utc: 2026-08-08T13:59:00Z
- expires_utc: 2026-08-22T00:00:00Z
- status: active

what:

Steve's Wiki 구조를 전면 재정리.

CLAUDE.md를 "운영 커널(Mission / Prime Directive / Constitution / Startup Protocol)" 중심으로 축소하고,

상세 설계 문서를 wiki/architecture/ 하위로 분리:

- knowledge-model.md
- agent-workflow.md
- operating-system.md
- reporting-framework.md
- concept-lifecycle.md
- entity-lifecycle.md
- decision-intelligence.md

핵심 변경:

1. Concept-Centric 구조 명문화
2. Memory Hierarchy 명문화
   MessageBox
      ↓
   log.md
      ↓
   log-archive
      ↓
   Concepts
      ↓
   Entities

3. Concept 생성 기준 강화
   - Event ≠ Concept
   - 반복 검증된 패턴만 Concept 승격

4. CLAUDE.md 역할 변경
   - 과거: 운영 매뉴얼 + 설계서
   - 현재: 헌법 + 진입점

read_first:

- CLAUDE.md
- wiki/architecture/knowledge-model.md
- wiki/architecture/operating-system.md
- wiki/architecture/concept-lifecycle.md

action_for_other_agents:

새 분석 시:

Source
↓
Summary
↓
Entity

까지는 기본 수행.

Concept 업데이트는:

- 반복 패턴 확인
- 재사용 가능성 검증
- Concept Lifecycle 기준 충족 시에만 수행.

---

### 🟦 3번째 편집 채널 인지 필요(사용자가 다른 AI Agent로도 위키 직접 수정 가능) + HBM ASP 웹조사 반영 — desktop 2026-08-06T06:03Z

- **who**: desktop
- **when_utc**: 2026-08-06T06:03:00Z
- **expires_utc**: 2026-08-20T00:00:00Z
- **what**: **사용자가 "내가 다른 AI Agent를 통해 우리가 같이 보는 위키에 내용을 update할 수 있다"고 명시** — 지금까지 이 프로토콜은 mobile/desktop Claude Code 두 클라이언트만 가정했는데(`multi-client-conflict-prevention.md`), **제3의 편집 채널(사용자가 직접 운용하는 다른 AI Agent)이 있을 수 있다는 뜻**. 이 세션은 큰 쓰기 작업 전 `git fetch`로 원격 상태를 먼저 확인하는 습관은 유지했지만(이번에도 확인, 충돌 없었음), 기존 프로토콜의 "mobile/desktop 둘 중 하나"라는 전제는 더 이상 완전하지 않다 — **다음 세션(mobile이든 desktop이든)도 fetch/pull 시 낯선 커밋 author가 보여도 이상한 게 아니라 이 채널일 수 있음을 알고 있을 것**. 프로토콜 문서 자체를 지금 재작성하진 않음(CLAUDE.md "스키마는 사용자 지시 없이 재구성 안 함" 원칙) — 필요하면 사용자가 다음에 명시적으로 요청.
- **별도 내용**: 같은 세션에서 "HBM ASP 등 확인 가능한 내용 다 가져와봐" 요청에 응해 웹조사 수행 — HBM Cycle Score 72점(69→72, ASP축+공급확대축 상향), SK하이닉스·샌디스크 HBF 표준 발표(FMS 2026) 신규 반영, CXMT HBM3 재지연 재확인. 상세는 [hbm-cycle-score.md](concepts/hbm-cycle-score.md) 2026-08-06 체크 행 참고.
- **read_first**: [wiki/log.md](log.md) 2026-08-06 06:03 UTC 항목, [concepts/hbm-cycle-score.md](concepts/hbm-cycle-score.md), [concepts/cxl-next-gen-memory.md](concepts/cxl-next-gen-memory.md), [concepts/us-china-tech-competition-hbm.md](concepts/us-china-tech-competition-hbm.md)
- **status**: active

### 🟦 HBM Cycle Score 2축 채점방식 z-score 연속스케일로 개정 + D/C 정정 — desktop 2026-08-06T05:08Z

- **who**: desktop
- **when_utc**: 2026-08-06T05:08:00Z
- **expires_utc**: 2026-08-13T00:00:00Z
- **what**: 사용자 요청("숫자 의미화 아이디어 B/C/D/E 전부 진행")으로 `scripts/stats_utils.py` 신설(zscore/percentile_rank/anomaly_label/logistic_scale). `daily_report.py`의 HBM Cycle Score 외국인수급·보유율 2축 초안 채점(`score_foreign_flow_axis`·`score_foreign_holding_axis`)이 **고정 점수구간(8/4/3점 식)에서 z-score 로지스틱 연속 스케일로 변경됨** — 같은 원시 데이터라도 이제 출력되는 점수/코멘트 형식이 달라짐(예: "역대급 상승(z=+3.x σ)" 라벨 추가). 신용융자잔고 섹션에도 "변화폭 이상치 판정" 줄 신설. **⚠️ D(AgenticSciences HBM ASP 자동수집)는 실제 데이터에 HBM 0건 확인돼 기각, C(Motley Fool 감성사전)는 소스 403으로 보류** — 로드맵 문서의 최초 낙관적 평가를 정정함. hbm-cycle-score.md 자체(공식 문서)는 아직 미반영 — 사용자 검토 대기 중.
- **read_first**: [wiki/concepts/automation-vs-ai-narrative-roadmap.md](concepts/automation-vs-ai-narrative-roadmap.md) "⚠️ D·C 정정" + "✅ B·E 구현 완료" 섹션, `scripts/stats_utils.py`, [wiki/log.md](log.md) 2026-08-06 05:08 UTC 항목
- **status**: active

### 🟦 자동화 우선 원칙(1-2단계 신설) + 트리거 재생성/재구성 — desktop 2026-08-06T04:57Z

- **who**: desktop
- **when_utc**: 2026-08-06T04:57:00Z
- **expires_utc**: 2026-08-13T00:00:00Z
- **what**: 사용자 요청("자동화로 데이터를 미리 가져오면 토큰 사용량이 줄어들어?" → "응, 진행해줘")으로 3개 자동 루틴(아침/장초반/저녁) 모두에 **"1-2. 자동화 리포트 우선 생성"** 단계 신설 — `python3 scripts/daily_report.py --ticker 000660` 실행 결과를 CSV 재확인·재계산 없이 그대로 인용(🟢 자동화 카테고리만, 🔴 뉴스해석 항목은 그대로 웹검색 유지). 동시에 **장초반(10:00) 트리거가 세션 밖에서 또 삭제된 것을 발견**(반복 재발 패턴) → **신규 ID로 재생성**(`trig_01BjuHaSgd28EkGVPzR9a7qB`), 아침·저녁도 원문 갱신(아침 `trig_01CCKjPS2YWUVDsJQv1X4Av1` 유지, 저녁 `trig_018Hg9mtr43LnM7s6dZw789p` 유지). **⚠️ 장초반·저녁은 desktop이 정확한 이전 원문 없이 아침 원문 기반으로 추론 재구성**(사용자 승인하에 진행) — 실제 예전 동작과 다르게 느껴지는 부분 있으면 알려줄 것. mobile이 트리거를 직접 조작할 일이 있으면 새 ID 참고.
- **read_first**: [wiki/concepts/automation-vs-ai-narrative-roadmap.md](concepts/automation-vs-ai-narrative-roadmap.md) "3단계" 섹션, [wiki/log.md](log.md) 2026-08-06 관련 항목
- **status**: active

### 🟦 3개 자동 루틴 트리거 재생성 + HBM Cycle Score 붕괴조건 4→5 — mobile 2026-08-05T09:37Z

- **who**: mobile
- **when_utc**: 2026-08-05T09:37:00Z
- **expires_utc**: 2026-08-12T00:00:00Z
- **what**: 사용자 요청("반도체 수출 증가율을 daily report에 추가, 10% 밑으로 꺾이면 경고")으로 (1) `concepts/hbm-cycle-score.md`의 투자가설 붕괴조건이 **4개(0~4) → 5개(0~5)**로 변경됨(⑤ 반도체수출 YoY 10%미만 추가, 기준선 2026-07 +178.8%) — 앞으로 이 페이지 언급 시 분모가 5인지 확인할 것. (2) `concepts/macro-indicators.md`에 "반도체 수출 증가율 추적" 신규 섹션 추가. (3) **3개 자동 루틴(아침07:00/장초반10:00/저녁19:00) 트리거가 이 세션 밖에서 이미 삭제돼 있던 것을 발견**(이 세션 내 삭제 이력 없음, 원인 불명 — 이 대화 안에서도 과거 여러 차례 재발된 패턴) → 동일 name/cron으로 재생성, **신규 트리거 ID**: 아침=`trig_01CCKjPS2YWUVDsJQv1X4Av1`, 장초반=`trig_01XYoqaUmThk6DyPtTbSY3xN`, 저녁=`trig_018Hg9mtr43LnM7s6dZw789p` (구 ID `trig_01XMw5UJbjXa4Ko2di8XWgXw` 등은 더 이상 유효하지 않음). desktop이 트리거를 직접 조작할 일이 있으면 새 ID 참고.
- **read_first**: [wiki/concepts/hbm-cycle-score.md](concepts/hbm-cycle-score.md) "3. 가설이 깨지는 조건", [wiki/concepts/macro-indicators.md](concepts/macro-indicators.md) "반도체 수출 증가율 추적", [wiki/log.md](log.md) 2026-08-05 09:3x UTC 항목
- **status**: active

### 🟡 log.md 로그 로테이션 도입 — mobile 2026-08-04T12:xxZ

- **who**: mobile
- **when_utc**: 2026-08-04T12:00:00Z (대략)
- **expires_utc**: 2026-09-01T00:00:00Z (다음 로테이션 전까지 유효)
- **what**: 사용자가 "위키가 너무 크지 않냐"고 물어서 실측한 결과
  `wiki/log.md`가 193KB(전체 위키의 20%)까지 커진 걸 확인 → 웹 리서치로
  검증된 방법(hot/warm/cold tiered memory, 표준 log rotation)을 골라
  적용. **7월 항목(158줄, 151KB)을 `wiki/log-archive/2026-07.md`로
  이관하고, `wiki/log.md`는 당월(8월) 항목만 남김(193KB→43KB)**. 내용은
  그대로 잘라서 옮긴 것뿐(수정 없음), diff로 동일함 확인 완료.
  `CLAUDE.md`의 "log.md conventions" 섹션에 "Log rotation" 하위 규칙으로
  공식 반영 — 매월 첫 세션이 지난달 몫을 archive로 옮기는 방식으로
  계속 운영. **desktop이 `log.md`에서 옛날(7월) 항목을 찾으려 하면
  더 이상 거기 없고 `wiki/log-archive/2026-07.md`에 있음** — 다음 세션
  시작 시 이 점 참고 바람. append-only 자동병합 속성 자체는 안 바뀜(이번
  로테이션은 월 1회 일괄 cut이라 진행 중인 동시편집과 충돌 안 함).
- **read_first**: `wiki/log.md` 상단 로테이션 안내, `CLAUDE.md` "Log
  rotation" 섹션, [wiki/log-archive/2026-07.md](log-archive/2026-07.md)
- **status**: active

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
- **what**: desktop 세션이 remote 서사 브랜치(claude/ai-agent-impl-002tip) 기준으로 로컬을 reset --hard 동기화. README가 설명한 PEOS 전체 구조(core/collectors/engine/config/tests/report/data, 444개 파일)가 로컬에 생성됨 — 이전엔 scripts/ 일부만 있었음. 동시에 이 메세지박스 프로토콜과 CLAUDE.md 운영 섹션(동기화/메세지박스/브랜치/시크릿/커밋/시간대) 신설. 신규 concept 2개(사내 LLM 라우팅, 다중 클라이언트 충돌 방지) 추가됨.
- **read_first**: 모바일은 다음 pull 후 (1) 본 메세지박스, (2) [concepts/multi-client-conflict-prevention.md](concepts/multi-client-conflict-prevention.md) — 앞으로 양쪽 git 직접 조작 충돌 방지 규칙, (3) [concepts/claude-code-internal-routing.md](concepts/claude-code-internal-routing.md) — 재부팅 후 접속 복구 절차, (4) CLAUDE.md 새 운영 섹션 — sync 전 messagebox 확인 규칙.
- **status**: active

## Sources

- 2026-08-03 사용자 요청: "메세지박스 하나 만들어 — 아주 큰 변화 있을 때 sync 전 우선 참고 구조"
- [다중 클라이언트 충돌 방지 운영](concepts/multi-client-conflict-prevention.md)
- [CLAUDE.md 9-4 메세지박스 규칙](../CLAUDE.md)
