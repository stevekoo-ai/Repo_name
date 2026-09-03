# Knowledge Model

## Purpose

Steve's Wiki stores information in progressively higher levels of understanding.

---

# Repository Structure

sources/
    Raw evidence

summaries/
    Events, observations, investigations

entities/
    Long-lived tracked subjects

concepts/
    Reusable cognitive assets

reports/
    Generated outputs

---

# Knowledge Flow

Sources
    ↓
Summaries
    ↓
Entities
    ↓
Concepts
    ↓
Reports

---

# Sources

Immutable evidence.

Ground truth.

Examples:

- API responses
- News
- PDFs
- Reports

---

# Summaries

Events, observations, investigations, case studies.

Examples:

- SK Hynix ADR breakout
- Buffett AI interview review

---

# Entities

Long-lived tracked subjects.

Examples:

- SK Hynix
- Portfolio
- User Profile
- Automation Infrastructure

---

# Concepts

Reusable cognitive assets.

Examples:

- Frameworks
- Patterns
- Playbooks
- Lessons Learned
- Monitoring Systems

Concepts are the highest value assets in Steve's Wiki.

---

# Reports

Actionable understanding generated from Sources, Summaries, Entities, and Concepts.

---

# 분류 정책 (단일 출처 — 다른 이름의 폴더 생성 금지)

위 5계층 폴더만 허용한다. **`reference/`, `monitoring/`, `daily-updates/` 등 비공식 폴더는 2026-09-02 마이그레이션으로 제거됐으며 재생성 금지.**

새 파일 저장 시 반드시 아래 기준으로 분류:

| 폴더 | 저장 대상 | 금지 |
|---|---|---|
| `sources/` | 공식 스펙시트, API 원응답, raw evidence | 분석이나 해석은 넣지 않음 |
| `summaries/` | 일일 update, 사건 관찰, 조사 기록 | "참고 자료"라는 이유로 reference/ 생성 금지 |
| `entities/` | 장기 추적 대상 (SK하이닉스, Portfolio 등) | |
| `concepts/` | 재사용 컨셉트, 프레임워크, 분석, 계산 엔진, tracker/monitoring, 가이드 | tracker/monitoring을 별도 폴더로 분리 금지 — concepts/ 안에 둠 |
| `reports/` | 생성된 산출물 (HTML, PNG 등) | |

**판단이 애매하면 `concepts/`에 둔다** (재사용 가능성이 가장 넓음).

### 이전 관행 (더 이상 사용 금지)

- `reference/` → 분석 자료, 가이드, 계산 엔진은 `concepts/`로, 공식 스펙은 `sources/`로, 산출물 HTML은 `reports/`로 이동 완료 (2026-09-02)
- `monitoring/` → `concepts/`로 이동 완료 (tracker는 컨셉트의 일종)
- `daily-updates/` → `summaries/`로 이동 완료 (일일 update는 summary의 일종)
