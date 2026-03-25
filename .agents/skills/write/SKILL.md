# Resume Generation Skill

## Input
$ARGUMENTS — JD URL, file path, or pasted JD text. Default language: English.

## Steps

### 1. Parse and save JD

Determine JD input type and extract content:
- URL → fetch page, strip nav/footer/boilerplate, extract job posting body only
- File path → read file
- Pasted text → use as-is

Save as `jd.md` with two labeled blocks:

```
## Summary
role · company · type (contract/FTE) · salary · location · work-auth
company 1-liner: stage/industry/product
must-have qualifications + hard requirements
priority keywords (top 7, ordered by emphasis in JD)
responsibilities (bullets)
nice-to-haves (if distinguishable from must-haves)

---

## Original
[verbatim posting — strip nav, footer, and application form only]
```

Create the application folder at this step if it doesn't exist yet:
`outputs/applications/{YYYYMMDD}_{company}_{role}/`

---

### 2. Load context (parallel)

Run 2a and 2b together — don't wait for one before starting the other.

**2a. Index scan:**
Read `index.yaml` → scan project `tags` against JD keywords → build candidate project list.

**2b. Load cache files:**
- If `.cache/project_frontmatter.yaml` is missing or older than any file in `profile/projects/`: run `.claude/hooks/build-bundle.sh` first.
  Then read `.cache/project_frontmatter.yaml`.
- If `.cache/common_context_en.md` is missing or older than `profile/identity.md` or `profile/preferences.md`: run `.claude/hooks/build-bundle.sh` first.
  Then read `.cache/common_context_en.md` (identity + preferences + template).
  For non-English output: read `.cache/common_context_i18n.md` instead.

---

### 3. Check outcome patterns

Read `meta/outcome_summary.yaml`. Find any entries matching this role's `role_family` and `seniority`.
If patterns exist, note which project types or framing approaches had higher success rates — use this to inform project selection and positioning in step 5.

---

### 4. Refine project selection

Using `project_frontmatter.yaml` (metrics + confidence scores), cross-reference with the candidate list from step 2a.
Narrow to final 5–7 projects. Selection criteria:
- Covers the most JD keywords with quantified evidence
- Confidence ≥ medium for primary bullets
- Recency and role-relevance match JD seniority level

Gap check: count top-7 JD keywords with no matched project coverage.
- Gap ≤ 3: ask gap-fill questions (max 2), then write strategy.md and proceed without confirmation
- Gap > 3: ask gap-fill questions (max 3–5), write strategy.md, confirm with user before proceeding

---

### 5. Strategy

**Gap-fill inquiry** — ask targeted questions before writing strategy.md.
- If selected projects lack quantified results for a JD-critical keyword: ask for the specific metric.
  "Do you have a specific number for [keyword] in [project]?"
- If a must-have requirement can't be covered by any project: ask for an alternative experience.
  "Is there an experience or example that demonstrates [requirement]?"
- If user says "none" → acknowledge the gap, proceed.
- User answers → update the relevant project file's Raw Notes section before continuing.

Write `strategy.md` in machine-readable YAML:
```yaml
priority_keywords: [top 5 JD keywords in order of importance]
gap_direction: [what to emphasize to close coverage gaps]
constraints: [must-have signals, positioning angle, red lines]
project_selection:
  - id: [project_id]
    reason: [why selected]
    primary_bullet_target: [which JD keyword this project addresses]
```

**Factual verification:** Each `reason` in project_selection must state only facts present in the profile project file. Do not extrapolate audience, market segment, or customer type beyond what the profile explicitly states. If the strategy requires a market-fit claim (e.g., "targets solopreneurs"), verify it against the project's actual customer/audience data before writing it.

If gap > 3: confirm strategy with user before proceeding to step 6.

---

### 6. Full-read key projects

Read the full content of 2–3 projects that require detailed story material for primary bullets.
Do not full-read projects used only for secondary or supporting bullets — frontmatter is sufficient.

---

### 7. Generate resume

Follow the template structure from `common_context_en.md`.

**Bullet format: result-first XYZ**
Lead every bullet with the outcome [X] and metric [Y], then the method [Z].

Good: "Reduced onboarding time from 14 days to 3 (200+ accounts) by rebuilding the welcome flow with automated check-ins"
Bad: "Leveraged automated check-ins to reduce onboarding time"

The reason this matters: recruiters and hiring managers scan for impact before method. Starting with the result signals that the candidate thinks in outcomes, not activity. Starting with the method reads as task-execution thinking.

Apply voice and style rules from `preferences.md`.

---

### 8. Mechanical pass (1–2 rounds, batch fixes)

Run all checks in a single pass per round. Do not fix one item at a time.

**XYZ structure:**
- Fix bullets missing Y (metric) or Z (method)
- Lead verbs that should be replaced: strengthened, enhanced, leveraged, utilized, facilitated, spearheaded

**Keyword coverage:**
- Insert top-5 JD keywords from `strategy.md` if absent from resume body

**Kill words and redundancy:**
- Remove: innovative, strategic, cutting-edge, synergy, best-in-class
- Remove: "in order to", "was able to", "responsible for"
- Fix -ing filler: "Focusing on X, achieved Y" → "Achieved Y by X"
- Fix double prepositions: "by through", "for across"

**Verb diversity:**
- Deduplicate verbs appearing 3+ times as bullet lead across all roles

**Preference expression (Phase 1 items from preferences.md):**
- Drop "I" pronouns from summary and bullets; use implied subject
- Summary: ≤60 words, 3–4 sentences
- Remove commodity tools from Tools line: Google Sheets, Looker Studio, Slack, Notion
- Word substitution: grow/grew → scale/scaled (team/org context); strengthen/strengthened → improve/improved
- Consulting prefix: `**Consulting (Client):**` for external client projects

**Structure:**
- Strongest JD-relevant bullet leads each role section. For PM roles: lead with analytical/product-building bullets (decision-making, system design, data product) over operational/scale/founder-context bullets — company description already establishes founder context, so role bullets should demonstrate PM capability.
- Tools line: ordered by role relevance, most distinctive first
- Summary closing: last sentence in candidate voice — state what you built/did, not how you match the company. See preferences.md.

Git: 1 commit per round (batch all fixes). Stop after 2 rounds or when 0 violations found.

---

### 9. Humanizer pass

Run the humanizer skill on the draft with resume type.

The humanizer applies two pattern sets:
- `base-patterns.md` — 24 universal AI writing tells (inflated significance, AI vocabulary, em dash overuse, etc.)
- `resume-cover-letter.md` — resume-specific patterns R1–R10 (inflated significance in bullets, filler -ing verbs, AI vocabulary in professional context, vague process/scope, etc.)

Scan for all violations first, then fix in a single batch. Do not fix one item at a time.

---

### 10. Save outputs

Save to `outputs/applications/{YYYYMMDD}_{company}_{role}/`:
- `jd.md` (already saved in step 1)
- `resume_v1.md` (mechanically cleaned draft)
- `strategy.md` (always save, even if gap ≤ 3 — validate skill requires it; write a minimal version if no gap analysis was needed)
- `notes.md` with sections: Research, Gaps, Interview Prep (STAR format), Follow-up

---

### 11. Update tracking

- Update `tracker.yaml` with new application entry
- Update `index.yaml` `active_apps`

---

### 12. Hand off

Call ingest skill to register the new application entry, then proceed to validate skill automatically.

---

## notes.md Interview Prep

Use STAR format:
- **Situation:** context and background
- **Task:** your specific responsibility
- **Action:** what you did (concrete steps, not vague effort)
- **Result:** measurable outcome

Populate 2–3 STAR stories using the primary projects selected in strategy.md, targeting the JD's top behavioral or scenario-based interview signals.

---

## DO NOT load
- `index.yaml` a second time
- `changelog.md`
- `inbox/processed/*`
- Any file already read as part of the cache bundle
