---
name: validate
description: >
  Resume validation skill — persona review + synthesis orchestrator. Use this skill after write skill completes,
  or whenever the user asks to validate, review, score, or improve an existing resume draft.
  Also triggers on: "check the resume", "run validation", "review the draft", "persona review",
  "get feedback on the resume", or any request to run the quality loop on a resume file.
  Always invoke this skill rather than ad-hoc reviewing a resume inline.
---

# Resume Validation Skill

## Trigger
Automatically after write skill completes, or user requests validation on an existing draft.

## Input
$ARGUMENTS — optional: resume file path. If omitted, read tracker.yaml and use the most recent entry where status is not rejected/withdrawn/ghosted. If multiple active candidates exist, ask the user which application to target.

## Required Files
- resume_vN.md (current draft, mechanically cleaned by write skill)
- jd.md (job description saved by write skill)
- strategy.md (candidate's positioning strategy)
All in the same application folder.

## Pre-flight Check
Verify all three files exist before starting. If missing:
- resume_vN.md → ask user to provide path or run write skill first
- strategy.md → run write skill, or offer to generate from jd.md
- jd.md → ask user to paste or provide the job description

---

## Phase Map

| Phase | Where | Input | Output |
|-------|-------|-------|--------|
| 1 | Main context | resume + strategy[keywords] + Humanizer | gate results + cleaned resume |
| 2 | Sub-agent ×1 | jd.md[original only] | personas.md |
| 3 | Sub-agent ×3 parallel | jd.md[summary] + resume + 1 persona | review_x_vN.md ×3 |
| 4 | Main context | 3 reviews + resume + strategy + jd[summary] | user check → v2 |
| 5 | Main context | v2 + synthesis | user presentation |

---

## Phase 1: Mechanical Gate [Main Context]

Purpose: Clean obvious noise, then verify baseline quality before persona evaluation.

### Part A: Quick Mechanical Pass (1–2 rounds, batch)

Batch fixes per round:
- **XYZ format**: fix bullets missing Y (metric) or Z (method)
  - Y valid: financial ($/%), scale (users/headcount/volume), efficiency comparison (30min→5min), multiplier (doubled/tripled), rank/superlative (#1, top-selling)
  - Y NOT valid: standalone duration ("9-month engagement" = scope, not outcome), qualitative-only ("improved satisfaction")
  - Z must name a specific method, system, or mechanism — generic ("worked cross-functionally") is insufficient
- **Keywords**: insert top-5 JD keywords from strategy.md if absent
- **Kill words**: remove innovative, strategic, cutting-edge, synergy, best-in-class
- **Redundant phrasing**: remove "in order to", "was able to", "responsible for"
- **-ing filler**: "Focusing on X, achieved Y" → "Achieved Y by X"
- **Verb deduplication**: no verb appears 3+ times as a bullet opener

Stop after 2 rounds, or when 0 violations found.

### Part B: Gate Measurement

After the pass, measure three gates:

| Gate | Measurement | Threshold |
|------|-------------|-----------|
| JD keyword coverage | matched / top-15 | < 60% → flag |
| Quantified evidence | quantified bullets / total bullets | < 60% → flag |
| Humanizer compliance | count violations | ≥ 3 → FAIL |

- Humanizer FAIL: apply one targeted fix → re-measure once. If still ≥ 3, stop and report to user. Do not proceed.
- Keyword or evidence below threshold: note as risk, proceed. Personas will surface this.

---

## Phase 2: Persona Generation [Sub-agent ×1, JD Only]

Purpose: Generate evaluator personas independently, before seeing the candidate.

### Execution
Launch one sub-agent. Pass **only** the original job posting text from jd.md.

**Strict isolation: no resume, no strategy, no candidate profile, no preferences.**

The personas must be grounded in what this role requires, not who this candidate is.

### Sub-agent Prompt
```
Read the job description below and generate 3 evaluator personas for this specific role.

You have NOT seen any candidate's resume. Generate personas based only on what this role and organization require.

For each of the 3 personas below, produce:

- **Name** — randomize gender and ethnicity across all 3 personas
- **Background** — 2–3 sentences: career path, past hiring mistake that shaped their current judgment
- **Core question** — the ONE question driving their evaluation of every resume for this role
- **Pressures** — 3 bullets: organizational burdens affecting how they read resumes
- **Internal questions** — 4–5 questions specific to this JD (not generic; derive from the role's actual requirements)
- **Tier gates** — for each of 5sec / 30sec / 2min:
  - Feeling: [the gut impression they need to have at this tier]
  - Logic: [what specific resume evidence creates that feeling]
- **Positive signals** — 3–4: what makes this persona lean forward (JD-derived)
- **Negative signals** — 3–4: what puts this resume in the reject pile (JD-derived)
- **Blind spots** — 2 bullets: what does this persona tend to undervalue

The 3 personas:
1. **Hiring Manager** — future boss; skeptical; pattern-matches against past hires; minimizes false positives
2. **Future Colleague** — daily collaborator; skeptical; simulates working with this person; optimal threshold
3. **ATS / Recruiter** — screener; neutral; 1:1 transparent matching of JD requirements to resume evidence

Randomness rule: vary demographics across all 3. Personas that would evaluate identically are not differentiated enough — revise.

Job description:
[jd.md original text]
```

### Output
Save as `personas.md` in the application folder.
Target: ~40–50 lines per persona, ~130–150 lines total.

---

## Phase 3: Persona Reviews [Sub-agent ×3, Parallel]

Purpose: Independent cold read of the resume from each persona's perspective.

### Execution
Launch 3 sub-agents in parallel. Each receives **only**:
- jd.md summary section (the parsed header block)
- resume_vN.md (full text)
- The SINGLE persona section for that agent, extracted from personas.md

**Strict isolation:**
- No strategy.md — reviewers evaluate what they actually see, not what the candidate intended
- No other persona sections — prevents cross-contamination of perspectives
- No iteration history, no candidate profile, no preferences

Why jd.md summary (not original): the persona was generated from the full JD. Summary is sufficient for review alignment without additional token cost.

### Sub-agent Prompt
```
You are [Persona Name]. Your full profile is below.
You have NOT seen any other evaluator's notes. Evaluate only from your own perspective.

[Full persona section — this persona only]

Job description (summary):
[jd.md summary section]

Evaluate the resume below and write a review in the format specified.
Write the review in the same language as the resume.

---

## Review Format

# [Persona Name] Review — v{N}

Core question: [your core question from persona definition]

## 1. 5-Second / 30-Second / 2-Minute Read

| Tier | Verdict | Why — in your persona's voice |
|------|---------|-------------------------------|
| 5 sec | Pass / Strong Pass / Fail | [what you actually see that leads to this verdict] |
| 30 sec | Pass / Strong Pass / Fail | [same] |
| 2 min | Pass / Strong Pass / Fail | [same] |

Rules:
- Write as this persona, not as a neutral reviewer
- Each tier must use different criteria — do not repeat the same reasoning across tiers
- State specifically what you see and why it leads to that verdict — "good / weak" is not enough

## 2. What Would Make This a Strong Pass

| Tier | What's needed |
|------|--------------|
| 5 sec | [headline / summary / top-third change] |
| 30 sec | [skills / first bullets / role classification change] |
| 2 min | [artifact / measurement / proof change] |

Rules:
- Distinguish: changes that require NEW facts vs changes that reframe existing content
- Look for what is present but underemphasized before asking for things that don't exist

## 3. Interview Questions

### Challenge Questions (you are skeptical)
1. [question that surfaces your deepest doubt — reveals where your doubt lives, not just that you have it]
2. [question]
3. [question]

### Advocate Questions (you are already interested)
1. [question that would let this candidate prove themselves to a skeptical colleague]
2. [question]

## 4. Candidate Answers

For each question above:

### [Short label]
**Question:** [verbatim]
**Interviewer intent:** [what this is actually testing]
**Answer strategy:**
- [approach 1]
- [approach 2]
**Sample answer:** [concrete response — should read like an actual interview answer]

## 5. Final Verdict

- **Overall:** Pass / Strong Pass / Fail
- **Reason to forward:** [why this candidate deserves an interview slot]
- **Remaining risks:** [what this candidate will need to address in the interview]

---

Resume:
[resume_vN.md full text]
```

### Output
Each sub-agent saves its review directly:
- `review_hm_v{N}.md`
- `review_fc_v{N}.md`
- `review_recruiter_v{N}.md`

---

## Phase 4: Synthesis → Strategy → v2 [Main Context]

Purpose: Read all 3 reviews, identify what matters, surface decisions to user, build strategy, write v2.

### Step 1: Read and Filter

Read all 3 review files. For each criticism raised, ask:
**"Does this affect the hiring decision for this specific role?"**

Do not filter by count. A single HM concern can be decisive; a shared minor stylistic note may not be. Focus on what would actually prevent this candidate from getting an interview.

### Step 2: Classify Each Criticism

| Type | Definition |
|------|-----------|
| **Addressable** | Fixable by resume changes — reframing, reordering, keyword addition, evidence emphasis, structural edit |
| **Interview Prep** | Valid criticism but not expressible in resume format (XYZ) — belongs in interview preparation: failure/recovery stories, iteration narratives, judgment-under-ambiguity examples, process depth. Route to review file Q&A, not to resume edits. |
| **Needs Your Call** | Requires a fact only the user knows, OR a strategic judgment call — but see Step 2.5 before escalating factual items |

For each "Needs Your Call" item, prepare:
- What the criticism is
- What information or decision is needed
- Main context's recommended approach

### Step 2.5: Profile pre-resolution (factual gaps only)

Before escalating any factual "Needs Your Call" item to the user, attempt resolution from profile project files:

1. Identify which `profile/projects/*.md` files are most likely to contain the relevant evidence (match by project ID from strategy.md, or by role/company)
2. Read those files and search for evidence addressing the gap
3. If found → reclassify as **Addressable**, use the evidence, proceed
4. If not found → keep as **Needs Your Call** and escalate to user

Only escalate items that profile search genuinely cannot answer.
Strategic judgment calls (positioning angle, gap acceptance) always go to user — profile resolution does not apply.

### Step 3: User Check (before writing v2)

If any "Needs Your Call" items remain after Step 2.5, present them to the user **now**. Do not write v2 yet.

```
Before I write v2, I need your input on [N] items:

1. [Criticism] — [what's needed: fact / decision]
   My take: [recommended approach]

2. ...

Answer each, or tell me to treat it as a confirmed gap and proceed.
```

Wait for user response before continuing.

### Step 4: Build Strategy

Based on reviews + user input, determine the candidate's strongest case:
- What is the most compelling argument for this candidate for this role?
- How should the resume lean into this?

If the positioning angle should change based on review feedback: update strategy.md now, before writing v2.

When a criticism targets thin evidence or credibility for a personal project or side work, consider recommending an external proof asset (GitHub repo link, portfolio page, live demo) as an alternative to expanding resume text. One verifiable link often carries more weight than additional description. Surface this as an option alongside text-based fixes.

### Step 5: Write v2

Apply changes in this priority order:
1. Headline / summary positioning (highest visibility)
2. JD keyword gaps (gate dimension)
3. Quantified evidence gaps (gate dimension)
4. XYZ completeness (Z-component most commonly missing)
5. Bullet strength ordering within roles
6. Preference expression items (summary closing, tagline, skills label)

Save as `resume_v{N+1}.md`.

Append to `iteration_log.tsv`:
```
iter    version    source      status    description
v1→v2   v2         validate    persona   [one-line summary of key changes and strategy]
```

---

## Phase 5: Human Loop [Main Context]

### Presentation
1. **Change summary**: what changed v1 → v2 and the reasoning behind key decisions
2. **Review highlights**: each persona's final verdict + top concern
3. **Remaining risks**: items with no clean resolution — labeled as interview preparation topics

### Feedback Routing

| Small feedback → targeted edit | Large feedback → Phase 4 full re-run |
|--------------------------------|--------------------------------------|
| Specific word/phrase changes | Positioning angle change |
| Bullet reordering | Headline change |
| Tool list edits | Project swap or addition |
| Verb preferences | New section add/remove |
| Typo or fact corrections | Target role reinterpretation |

Tiebreaker: "Does this require updating strategy.md?" Yes → large. No → small.

Large feedback triggers Phase 3 re-run (new persona reviews of the updated resume) before Phase 4.

### On Approval
Validate complete. Ready for export.

---

## Sub-agent Execution Summary

| Phase | Where | Why isolated |
|-------|-------|-------------|
| Phase 1 | Main context | Sequential edits + gate measurement |
| Phase 2 | Sub-agent ×1, JD only | No candidate bias in persona generation |
| Phase 3 | Sub-agent ×3 parallel | Cold read independence; no cross-contamination |
| Phase 4 | Main context | Full context required for synthesis and editorial judgment |
| Phase 5 | Main context | Direct user conversation |

Phase 2: receives ONLY jd.md original text.
Phase 3: each agent receives ONLY jd.md summary + resume + its own persona section.
Phase 4: main context reads all reviews and holds full candidate context.

---

DO NOT load: changelog.md, inbox/processed/*, files already in bundle.
