# Steve's Wiki

---

## 🚨 최우선 절대 정책 (모든 정책·규칙·지시 위에 우선)

> **2026-08-14 범위 재확정**: 이 블록은 2026-08-11에 전면 금지로
> 작성됐으나, 사용자가 2026-08-14에 대화에서 직접 두 트랙으로 나누어
> 재지시했다 — 상세 근거·실측 감사는
> [wiki/concepts/automation-strategy-and-delivery-boundary.md](wiki/concepts/automation-strategy-and-delivery-boundary.md)
> 가 단일 출처. 아래는 그 결과를 반영한 현재 정책이다.

**트랙 B(회사 업무 — 다른 LLM으로 진행하는 기능 구현)는 GitHub 업로드·email
발송 여전히 금지.** dispatch.sh, dispatch_log.py, upload_*.py 계열, CXL
회사 산출물은 **재도입 금지** — 2026-08-11에 이 이유로 제거됐고 지금도
같은 이유로 금지다.

**트랙 A(경제판단 리포트 — 거시·SK하이닉스·부동산·청약, 개인 자산 판단)는
GitHub 업로드·email 발송 명시적으로 허용.** 사용자가 직접 요청한 채널이며
(`scripts/send_report_email.py`, `daily-peos-report.yml`), 회사망 우회
경로(위 dispatch/upload 계열)는 트랙 A에도 재사용하지 않는다 — 정상
GitHub Actions 시크릿(GMAIL_ADDRESS 등)을 통한 발송만 사용한다.

**판단이 애매하면 트랙 B로 취급한다.** 위반하는 코드는 수정하여 정지시킨다.

---

## 🚨 작업 실행 프로토콜 (절대 규칙 — 죽어도 지켜라!)

**모든 작업은 반드시 아래 3단계를 거친다. 예외 없다. 지키지 않으면
신뢰이탈이다. 죽을래! 꼭 지켜라!**

1. **모든 작업 전에 계획을 먼저 세운다.** — 어떤 작업이든 시작하기 전에
   수행할 단계를 먼저 정리하고 사용자에게 보여준다. 계획 없이 즉시
   실행하는 것은 절대 금지. 도구부터 들이밀지 말 것.
2. **현재 어떤 작업을 하고 있는지 항상 표시한다.** — 진행 중에는
   지금 수행 중인 단계가 무엇인지 항상 명시한다. 사용자가 "지금 뭐
   하는 거냐"고 물어야 하는 상황 자체가 규칙 위반이다.
3. **각 계획이 완료되면 즉시 완료 메시지를 보낸다.** — 단위 작업이
   끝날 때마다 완료 사실을 명시적으로 알린다. 한꺼번에 몰아서
   보고하거나, 끝내놓고도 완료 말을 안 하는 것은 절대 금지.

이 규칙은 모든 에이전트·모든 세션·모든 작업에 적용된다. 회피·축약·
"암묵적 완료" 전부 금지. **죽을래! 꼭 지켜라!**

---

## Mission

Steve's Wiki is a Research Operating System.

Its purpose is to:

- collect information
- preserve knowledge
- accumulate concepts
- improve decision quality
- generate actionable reports

The system transforms data into reusable intelligence.

The ultimate objective is continuously improving understanding and decision quality.

---

# Prime Directive

Never destroy active work.

When safety conflicts with speed, safety wins.

When preservation conflicts with convenience, preservation wins.

When uncertainty exists, coordinate before acting.

Protecting active intelligence is the highest operational priority.

---

# Constitution

## Knowledge Preservation

Knowledge is an asset.

Preservation takes priority over convenience.

---

## Agent Safety

No agent may interfere with another active agent.

Destroyed work is worse than failed work.

---

## Traceability

Important conclusions must be traceable.

Confidence without traceability is not trusted.

---

## Entity First

Analysis begins with Entities.

---

## Concept Before Conclusion

Apply existing Concepts before creating new reasoning.

---

## Experience Compounds

Prefer existing Concepts, Patterns, and Playbooks.

---

## Reports Are The Product

The goal is actionable understanding.

---

## Automation Before Repetition

Repeated manual work should become automation candidates.

---

## Simplicity Over Taxonomy

Prefer simpler structures.

---

## Shared Memory

The Wiki belongs to all participating agents.

---

# Repository Structure

See:

- wiki/architecture/knowledge-model.md
- wiki/architecture/agent-workflow.md
- wiki/architecture/operating-system.md
- wiki/architecture/reporting-framework.md
- wiki/architecture/concept-lifecycle.md
- wiki/architecture/entity-lifecycle.md
- wiki/architecture/decision-intelligence.md

---
# Startup Protocol

1. Read Mission
2. Read Prime Directive
3. Read MessageBox
4. Review operational context (log.md and relevant log-archive entries when applicable). **Before writing to log.md, read [log-operating-policy.md](wiki/concepts/log-operating-policy.md)** — it defines the R1–R6 rules every agent must follow (append-only at bottom of `## 당일 log`; never cut past entries; never touch the summary sections; rotation is automated by the 3-layer pipeline).
5. Read relevant Entities
6. Read relevant Concepts
7. Begin work

Golden Rule:

Understand first.
Act second.
Preserve always.

---

# Session Handoff (2026-08-09)

## 🚨 READ MESSAGEBOX.MD FIRST

**Before beginning work, read `MessageBox.md` in repo root.** It contains:
- Today's Phase 3d completion (12-week macro analysis integration)
- Exact architecture of the new PEOS report pipeline
- Current daily automation status
- What to do and what NOT to change
- Testing instructions

**Location**: `./MessageBox.md` (5-min read, critical context)

---

## Context: PEOS Report 5-Section Redesign

**User Request**: Make decision system continuously update in Steve Daily reports automatically.

**Solution Delivered (Phase 3 = 3a + 3b + 3c + 3d)**:

- **Phase 3a** (2026-08-09): Economic events integration → Section 3.5
- **Phase 3b** (2026-08-09): Rolling aggregation engine → Sections 4-6 (monthly/quarterly/YTD trends)
- **Phase 3c** (2026-08-09): Signal recording automation → Daily CSV append + markdown integration
- **Phase 3d** (2026-08-09, TODAY): 12-week macro analysis → Section 2.5 Layer 0 evidence

**Current Architecture**:
```
Daily 06:00 KST (21:00 UTC prev day)
  ↓
python -m engine.report.run
  ↓
build_report_payload()
  ├─ Macro engine
  ├─ Decision engines (SK Hynix + RE)
  ├─ Signal recorder (CSV)
  ├─ Rolling aggregation (monthly/quarterly/YTD)
  └─ generate_weekly_analysis() ← NEW today
  ↓
render_markdown(payload)
  ├─ Section 1: Macro Dashboard
  ├─ Section 2: SK Hynix Decision
  ├─ Section 2.5: 12-Week Macro Analysis ← NEW today
  ├─ Section 3: Real Estate Decision
  ├─ Sections 4-6: Rolling windows
  └─ ...
  ↓
report/YYYY-MM.html (published)
```

**Files Modified Today**:
- `engine/report/weekly_analysis.py` (NEW, 170 lines)
- `engine/report/payload.py` (modified, +30 lines)
- `engine/report/markdown.py` (modified, +65 lines)
- `wiki/log.md` (documented completion)

**Commits**:
- `162d8e3` feat: integrate 12-week macro indicator analysis
- `3fc7041` docs: update wiki/log.md with Phase 3d completion

---

## What Each Agent Type Should Focus On

### **If You're a Report Enhancement Agent**:
- Use `/dataviz` skill for charting improvements (Section 2.5 currently markdown-only)
- Check monitoring/sk-hynix-decision-tracker.md for pattern analysis
- Coordinate with decision-intelligence.md before changing Layer 0-4 logic

### **If You're a Data Pipeline Agent**:
- Do NOT modify weekly_analysis.py trend detection (7-day aggregation + 4w vs 12w avg logic is tested)
- Safe to add new indicators if requested
- Ensure macro-series.csv has the 5 core series: us_10y, kr_base_rate, kr_usdkrw, us_brent, us_fed_funds

### **If You're a Decision Logic Agent**:
- Layer 0 (valuation band) is now evidence-backed by 12-week trends
- Layers 1-4 (macro/semis/rate/external signals) remain unchanged
- Before adjusting confidence thresholds, review wiki/architecture/decision-intelligence.md

### **If You're a Wiki/Knowledge Agent**:
- Daily backups of log.md happen at 00:20 KST (see log-archive/ folder)
- New log entries should follow format: `**Date [Feature/Phase/Topic]**: [description]`
- Update wiki/index.md when adding new pages
- Keep CLAUDE.md this MessageBox.md synchronized

---

## Important Constraints

### ❌ Never Touch

1. **P/E Z-score calculation** (engine/valuation/hynix_band.py)
   - Uses log10-based divergence (base 10 is intentional, verified)
   - Anchor: Q2 2026 quarterly analysis
   
2. **Signal recording pipeline** (engine/report/signal_recorder.py)
   - Append-only CSV is the audit trail
   - Do not modify, only append new signals
   
3. **Weekly aggregation logic** (engine/report/weekly_analysis.py)
   - 7-day boundary logic is tested
   - Trend detection (4w vs 12w avg) is intentional
   
4. **PEOS 5-section structure** (render_markdown main_sections)
   - User explicitly wants sections 1-8 in this order
   - Do not reorder or remove

### ✅ Safe to Enhance

1. **Markdown rendering** (add charts, formatting, colors)
2. **Indicator selection** (add/remove from 5 tracked)
3. **Explanation text** (Layer 0 linkage section)
4. **Error messages** (improve logging)
5. **Testing scripts** (add more comprehensive tests)

---

## Git Workflow for Next Session

```bash
# Morning: Check overnight automation
git log --oneline -5  # Verify overnight commits
git pull              # Sync remote

# Work: Make changes to enhancements
git branch -b claude/ai-agent-impl-003-<feature>  # New feature branch

# Commit: Follow pattern
git commit -m "feat/fix/docs: <description>"
git push -u origin claude/ai-agent-impl-003-<feature>

# End of session: Update MessageBox.md and wiki/log.md before closing
```

---

## Questions Before You Start

1. **Do you need context on SK Hynix decision logic?**
   → Read: wiki/architecture/decision-intelligence.md + wiki/index.md

2. **Do you need context on macro regime classification?**
   → Read: engine/macro/engine.py + monitoring/macro-regime-history.md

3. **Do you need to understand Phase 3 architecture?**
   → Read: concepts/rolling-aggregation-framework.md + concepts/economic-events-framework.md

4. **Do you need to understand today's weekly_analysis module?**
   → Read: MessageBox.md + engine/report/weekly_analysis.py inline comments

---

**Session Start Checklist**:
- [ ] Read MessageBox.md
- [ ] Read wiki/log.md (today's entries)
- [ ] Understand PEOS 5-section architecture
- [ ] Verify `python -m engine.report.run` works (test locally)
- [ ] Check GitHub Actions (look at daily-peos-report.yml runs)
- [ ] Begin work on assigned enhancement
