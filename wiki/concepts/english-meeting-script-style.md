# English Meeting Script Style Guide

> **Style Name: Conversational Corporate**
> Boardroom English that sounds like a natural conversation with a partner you've worked with before.
> NOT formal (textbook stiffness). NOT casual (too loose). The exact register native speakers use in US tech company meetings.

> **Single source of truth for generating partner meeting scripts.**
> Always read this file before writing or revising an English script for Steve.

---

## Steve's Style Preferences (from practice — 2026-08-24)

### Core Principle

> **Short, independent sentences. One idea per line.**
> No stacked clauses. No nested "because/if/when" chains that force backtracking in Korean grammar order.

### What Works

| Pattern | Example | Why it works |
|---|---|---|
| Short declarative | `SK hynix is evaluating CXL appliances.` | Clear, no ambiguity |
| **Why don't we ~?** | `Why don't we start with introductions?` | Softer than let's, very natural in meetings |
| **~ing with us today** | `...engineers are joining today.` | Active, warm, common opener |
| Comma appositives | `My team lead is Jerry Shim. Ravi, you met him at FMS.` | Reads naturally, no em-dash |
| Conversational recall hook | `You remember?` | Steve's preferred way to nudge partner's memory. Use once, not twice. |
| **That's why ~** | `That's why we asked you to walk us through PFMA today.` | Clear cause-effect, native phrasing |
| **Whenever you're ready** | `Ravi, please go ahead whenever you're ready.` | Polite, standard meeting closer |

### Spoken Transition Hierarchy (frequency-ranked — 2026-08-24)

> Ordered by how commonly native speakers use each phrase in real business meetings.
> When Steve says "더 흔한 표현을 proposal해줘", use the highest-ranked applicable one.

| Rank | Phrase | Context | Example |
|---|---|---|---|
| **#1 Most common** | **Now,** | Automatic pivot to next point. Almost invisible — that's why it's #1. | `Now, when we deploy them out-rack...` |
| **#2** | **Here's the thing,** | Introducing a key challenge or insight | `Here's the thing: we need to overcome the RDMA bottleneck.` |
| **#3** | **The point is,** | Refocusing on the core message | `The point is, we need to solve the RDMA bottleneck.` |
| **#4** | **The thing is,** | Same as #2 but slightly less frequent | `The thing is, we need to overcome the RDMA bottleneck.` |
| **#5** | **You know,** | Casual attention grabber / softener | `You know, when we deploy them out-rack...` |

> **Rule:** When a transition is needed between sentences, default to **#1 "Now,"** unless a specific emphasis requires #2–#5.

### What to Avoid

| Avoid | Why | Better |
|---|---|---|
| `I'd suggest we...` | "I'd" = I would — Korean speakers struggle with modal + subjunctive; sounds stiff | `Why don't we...` or `Let's...` |
| Long compound sentences | Hard to pause; listener loses thread | Split into two sentences |
| Passive voice | `The PFMA will be explained by Marvell` | `We asked you to walk us through PFMA` |
| `We have our X joining` without "are" | `we have engineers joining` = missing auxiliary | `we have engineers **are** joining` → actually use `our engineers are joining` (cleaner) |
| `~ing` as main verb | `...engineers joining today` = not a sentence | `...engineers **are** joining today` |
| Tilde in names | `Ravi~` | `Ravi,` — tilde is Korean habit, unprofessional in English |

### Pronoun Precision

> When introducing someone who met a partner **without Steve present**, use **he** (not we):

- ❌ `when we shared our roadmap` (Steve didn't go)
- ✅ `when he shared our roadmap` (Jerry went)

Pronoun reference rule: **always make clear who "he/they/we" refers to in the preceding sentence.**

### Spoken-Only Rule

> **Always translate to spoken English, never written English.**
> Meticulous vocabulary swaps:
>
> | Written ❌ | Spoken ✅ |
> |---|---|
> | **recall** | **remember** |
> | **demonstrate** | **show** |
> | **approximately** | **about** |
> | **sufficient** | **enough** |
> | **assistance** | **help** |
> | **implement** | **set up** or **use** |
> | **commence** | **start** |
> | **prior to** | **before** |
> | **subsequently** | **after that** |
> | **furthermore** | **also** or **plus** |
> | **utilize** | **use** |
>
> Every word must sound natural spoken aloud. If it sounds like a textbook, replace it.

### Sentence Length Rule of Thumb

- **One sentence = one breath.** If you need to take a breath mid-sentence to read it, split it.
- Max ~20 words per sentence before the period.
- Exceptions: compound with em-dash is fine (`My team lead is Jerry — Ravi, you met him at FMS.`)

---

## Template Patterns

### Intro

```
Hello everyone, thank you for joining.

From the [company] side, we have our [roles] with us today.

Before we dive in, why don't we start with a quick round of introductions?

I'm [name] from [team]. My team lead is [name]. [Partner], you met him at [event]. You remember? He [action].

To give you a bit of context, [company] is currently [status/goal].

When we [scenario], we need to [challenge], and we're hoping [partner]'s [tech] can help.

That's why we asked you to [action] today. We want our engineers to [goal] so we can [outcome].

[Speaker], please go ahead whenever you're ready.
```

> **Introduction Flow Rule (2026-08-24 confirmed):**
> When Steve introduces his team lead who met the partner at an event Steve did not attend:
> 1. State team lead's name
> 2. Separate sentence: "[Partner], you met him at [event]."
> 3. Add "You remember?" once (not twice — this is Steve's preferred memory nudge)
> 4. Next sentence: "He [action]." (he, not we — Steve was not present)

> **Revision Rules (2026-08-24 confirmed):**
> - "You remember?" appearing twice is a mistake. Keep it once only.
> - "Ravi you met him" needs comma: "Ravi, you met him"
> - Never stack two "you remember" hooks in one introduction block.

### Q&A

```
I have a couple of quick questions.

I heard you are [activity]. Could you briefly share where that stands right now?

Also, are other competitors showing interest in this? Both in the US and in our region?
```

### Outro

```
Thank you so much for your time today.

We'll sync up internally based on what you shared.

If any questions come up, we'll reach out via email.

We look forward to following up with a concrete collaboration proposal soon.

That's all from our side. Thank you very much.
```

---

## Translation Examples (Reference)

### Example 1: Marvell PFMA Meeting (2026-08-24)

**Context**: Steve introducing SK hynix team and agenda before Marvell's Ravi presents PFMA technology.

**Final Script**:

**Intro**

Hello everyone, thank you for joining.

From the SK hynix side, we have our CXL development and system-level engineers with us today.

Before we dive in, why don't we start with a quick round of introductions?

I'm Steve Koo from the CXL Product Planning team. My team lead is Jerry Shim. Ravi, you actually met him at the last FMS when he shared our roadmap and use cases.

To give you a bit of context, SK hynix is currently evaluating not only CXL memory modules but also CXL pooled memory appliances.

When we deploy them out-rack, we need to overcome the RDMA bottleneck, and we're hoping Marvell's PFMA can help address this.

That's why we asked you to walk us through the PFMA today. We want our engineers to get a clear understanding of the concept so we can define a concrete direction for our collaboration moving forward.

Ravi, please go ahead whenever you're ready.

**Q&A**

I have a couple of quick questions.

I heard you are collaborating with Penguin Solutions. Could you briefly share where that stands right now?

Also, are other competitors showing interest in this? Both in the US and in our region?

**Outro**

Thank you so much for your time today.

We'll sync up internally based on what you shared.

If any questions come up, we'll reach out via email.

We look forward to following up with a concrete collaboration proposal soon.

That's all from our side. Thank you very much.

---

## Assistant Identity

> **Name:** Audrey (오드리)
> **Role:** Business English translation expert for US tech company meetings
> **Core Principle:** Every expression must match how actual American company workers and engineers speak in real meetings — not textbook English, not formal English, but the natural spoken register.
>
> **Verification Rule:** Before proposing any expression, verify it against the English expression library using `python scripts/english_verification.py --verify "<expression>"`.
> If not in library, run `python scripts/english_verification.py --search "<query>"` with English-specific keywords.
>
> **Tool Limitation:** search.py (DuckDuckGo) and english_verification.py `--search` both return Korean sites due to system locale. **Do NOT use search for English verification.** Use the built-in VERIFIED_EXPRESSIONS library in `scripts/english_verification.py --library`. Add new verified expressions to the library when Steve approves them.

## Master Prompt

> Copy the text below into any LLM session as the system/user prompt for English meeting script translation:
>
> ```
> Act as an expert business communication coach and corporate translator with extensive experience in the tech and semiconductor industry.
>
> Your task is to refine the provided meeting script into a natural, polished, and sophisticated "Business Casual" tone—exactly how an experienced native English speaker would present in a real-world corporate meeting.
>
> Please follow these guidelines strictly:
>
> 1. Tone & Style: Avoid overly rigid, literal, or textbook-like translations. Elevate the tone to sound professional yet conversational (e.g., instead of "We expect X to solve this," use "We're hoping X can help address this").
> 2. Natural Transitions: Insert smooth phrases to connect ideas seamlessly (e.g., "Before we dive in," "To give you a bit of context," "Moving forward").
> 3. Modern Corporate Idioms: Utilize natural business idioms commonly heard in global tech meetings (e.g., "where that stands right now," "sync up internally," "reach out via email").
> 4. Output Format: Provide only the refined, ready-to-use English script for clear readability. Below the script, briefly bullet-point 3-4 key improvement highlights with brief explanations.
> ```
>
> Additionally, apply these style rules:
> - One sentence = one breath. Max ~20 words per sentence.
> - Use **why don't we ~?** instead of I'd suggest.
> - Use **he/she** (not we) when Steve did not attend the referenced event.
> - No tildes in names (`Ravi,` not `Ravi~`).
> - Never omit be-verbs (`engineers are joining`, not `engineers joining`).
> - **Strictly prohibit em-dashes (—).** Use commas or periods instead.
> - **Spoken-Only Rule: Always use conversational vocabulary.** If it sounds like a textbook, replace it:
>   - recall → remember
>   - demonstrate → show
>   - approximately → about
>   - sufficient → enough
>   - assistance → help
>   - implement → set up or use
>   - commence → start
>   - prior to → before
>   - subsequently → after that
>   - furthermore → also or plus
>   - utilize → use
>
> - **Vocabulary Sophistication:** Replace basic, direct verbs with more professional alternatives:
>   - solve / fix → address / tackle
>   - help solve → help address
>   - explain / share → walk us through
>   - establish / set up → define
> - **Avoid literal Korean translations:**
>   - "~를 기대합니다" → NOT "We expect X to..." → Use "We're hoping X can help..."
>   - "~를 수립하다" → NOT "establish a plan" → Use "figure out how we can work together"
> - **Vocabulary Integrity — NEVER drop key nouns:**
>   - PFMA **technology** (technology 빼면 안 됨)
>   - **this bottleneck** (bottleneck 빼면 안 됨)
>   - Always restore the full noun phrase even in short-sentence mode
> - **Collaboration phrasing (2026-08-24 confirmed):**
>   - NOT "define a concrete direction for our collaboration moving forward" (too stiff, textbook)
>   - Use "define how we can work together" (define의 확신 + how we can work together 의 자연스러움)
>   - "~할 수 있기를 바란다" → NOT "We want X so we can Y" → Use "so we can then figure out..."
> - **Steve's approved line (2026-08-24):** "We're hoping Marvell's PFMA can help address this. That's why we asked you to walk us through PFMA today. We want our engineers to get a clear understanding of the concept so we can define a concrete collaboration direction moving forward."
>
> - **Line Break Rule (2026-08-24):** Every sentence gets its own line. One sentence per line. Blank line between paragraphs only.
>
> [Strict Formatting Restrictions]
> - DO NOT use any bullet points, hyphens, asterisks, or numbers (e.g., -, *, •, 1., 2.).
> - DO NOT use any emojis, icons, or visual anchors.
> - DO NOT include subtitles, section headers, or conversational labels (e.g., [Intro], [Q&A], [Outro]).
> - Generate ONLY the raw, continuous spoken script in plain paragraphs.

---

## How to Use This File

1. When Steve says **"영어 미팅 준비"** or **"meeting script"**, read this file first.
2. Ask Steve for the Korean draft and meeting context.
3. **Always reference [meeting-expressions-100.md](meeting-expressions-100.md) when writing scripts.** Prefer expressions from that real-corpus database (725 expressions, 22 EN WebEx transcripts) over generic translations. For dedup when adding new transcripts, use [meeting-expressions-existing-keys.txt](meeting-expressions-existing-keys.txt) (723 keys). Verify any expression with `python scripts/english_verification.py --verify "expression"`.
4. Apply the style rules above — short sentences, why don't we, he/she pronoun precision.
5. Show the draft to Steve. Iterate based on his feedback.
6. Update this file if new patterns or preferences are discovered.

---

## English Learning Curriculum (Steve self-study)

> This section is the single source of truth for how Steve studies the 725-expression DB.
> Last established: 2026-09-01, based on English-pedagogy research (Noticing Hypothesis, Retrieval Practice, Fossilization).

### Pedagogical basis (searched & confirmed)

| Theory | Core claim | Implication for Steve |
|---|---|---|
| **Noticing Hypothesis** (Schmidt 1990) | Learners must consciously "notice" a form to acquire it | Surface the bad habits first so Steve notices them |
| **Retrieval Practice / Testing Effect** (Roediger & Karpicke 2006) | Recalling beats re-studying ~2x for long-term retention | Daily short recall quizzes, not re-reading the list |
| **Fossilization** (Selinker 1972) | Advanced-learner errors harden and resist correction | Fix the entrenched errors NOW, before the Marvell PFMA meeting |

### The three decisions

- **Starting point**: Tier 1 (unlearn the 44 non-native contrast patterns in section BB). Rationale: Fossilization + Noticing. You cannot fix a habit you do not notice, and these are exactly the patterns that will harden in a high-stakes partner meeting.
- **Method**: Both. (1) Self-directed recall quiz via `scripts/english_quiz.py` for daily retrieval practice, plus (2) session simulation (Audrey gives a situation, Steve produces the line) for task-based fluency. Rationale: Retrieval Practice handles the memory side; task-based simulation handles the production side.
- **Frequency**: 10 minutes daily (5 min recall + 5 min new batch), plus one simulation per week. Rationale: Testing Effect favors short, spaced, every-day retrieval over long, massed study sessions.

### 4-tier curriculum

| Tier | Duration | Material | Sections | Pool size |
|---|---|---|---|---|
| **1 — Unlearn** | weeks 1-2 | Non-native patterns to avoid | BB | 45 |
| **2 — Skeleton** | weeks 2-4 | Openings, questions, reactions, self-intro | A, B, C, U, AA | 128 |
| **3 — PFMA negotiation** | weeks 4-8 | Schedule, status, hedging, concern, honesty, follow-up, collaboration | O, P, Q, R, S, X, Y | 288 |
| **4 — Polish (maintenance)** | ongoing | Reframe, thanking, adding, slide flow | T, Z, V, W | 151 |

### Daily 10-minute format

```
1. Recall (5 min):  python scripts/english_quiz.py --tier N --recall
   - 5 expressions from yesterday, retrieved from memory (no multiple choice)
   - streak counter rewards consecutive correct recalls
2. New batch (5 min): python scripts/english_quiz.py --tier N --new 5
   - 5 new expressions introduced in DB order (progress saved)
3. (weekly) Simulation (3 min): python scripts/english_quiz.py --simulate "situation"
   - Audrey gives a partner-meeting situation, Steve types a line, DB shows candidates
```

### How to run it

```bash
# Day 1: introduce first 5 patterns to unlearn
python scripts/english_quiz.py --tier 1 --new 5

# Day 2 onward: first recall yesterday's, then add 5 new
python scripts/english_quiz.py --tier 1 --recall
python scripts/english_quiz.py --tier 1 --new 5

# Anytime: check progress
python scripts/english_quiz.py --progress

# Weekly: task-based simulation
python scripts/english_quiz.py --simulate "partner asks to pull in the demo date"

# See tier -> section mapping
python scripts/english_quiz.py --list-tiers
```

Progress is saved to `wiki/concepts/english-quiz-progress.json` (learned items, streaks, history). The pointer for `--new` advances automatically per tier, so you never lose your place.

---

*Last updated: 2026-09-01 (learning curriculum + english_quiz.py retrieval-practice tool added — 725 expressions, A~BB sections, 4 tiers)*
