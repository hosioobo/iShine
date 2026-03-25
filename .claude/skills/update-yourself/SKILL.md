---
name: update-yourself
description: >
  Runs a structured self-improvement cycle for the iShine resume system. Explicit invocation only:
  user says "/update-yourself", "improve the system", "tune the skill", "update iShine", or
  "remember this for next time". DO NOT auto-run — never trigger from conversation patterns alone.
---

# Self-Update Skill

## Purpose

Translate user corrections, session friction, and outcome data into targeted, file-level edits.
The skill proposes; the user approves; only then are changes applied.

## When to invoke

Explicit user command only: `/update-yourself` or equivalent phrasing.
DO NOT auto-trigger — not from detected frustration, repeated corrections, outcome events, or ingest skill chains.

---

## Step 1: Collect Evidence

Two source types — check both before drafting proposals.

### A. Conversation signals
Scan the dialogue since session start (or last `/update-yourself` run):

| Signal type | What to look for | Threshold |
|---|---|---|
| **Repeated corrections** | User rewrote or rejected the same type of output | 2+ times |
| **Friction points** | Steps that required back-and-forth to clarify intent | Any |
| **Voice/style preferences** | Phrasing, word choices, formatting the user preferred | Any explicit |
| **Bullet rewrite patterns** | User edited a bullet and the edit reveals a structural preference | Any |
| **Scoring eval results** | Multi-version config comparison run in session; one config shows better discrimination | 3+ versions scored |

If the conversation is sparse (< 3 substantive exchanges), say so explicitly: "The session was short — I found [N] signals. Proceed or defer?" Do not fabricate signals.

### B. File-based signals
Read these files directly — do not rely on memory of their contents:

- **`meta/outcome_summary.yaml`** — graduation candidates:
  - Pattern must appear in 3+ outcomes across **different** `role_family` values
  - Pattern must be translatable into a concrete, testable rule
  - Patterns already in `system_updates` list are already graduated — skip them

---

## Step 2: Categorize Proposed Changes

Organize findings into two categories before drafting proposals.

### Category A — Skill-Internal Tuning

Changes to parameters or prompts *within* existing skills. Examples:

- **validate**: quality score weights, guard dimension thresholds, max iteration count, stop conditions, tier gate language in personas
- **write**: strategy.md schema fields, gap-fill question framing, mechanical pass checklist items
- **preferences.md**: voice rules, word substitutions, Phase 1/Phase 3 expression items
- Loop thresholds: plateau detection sensitivity, retry limits, sub-agent prompt phrasing

### Category B — Skill-External / System Improvements

Changes to the system's structure or wiring. Examples:

- New skill proposals (include: trigger, input, output, rationale, where it fits in master workflow)
- Skill execution order changes in CLAUDE.md
- Workflow branching logic (e.g., new condition in feedback routing table)
- New guard dimensions or composite score components
- Changes to index.yaml schema, tracker.yaml fields, or outcome_log.yaml structure

---

## Step 3: Draft Each Proposed Change

For every signal that warrants a change, produce a change card:

```
[Change Card]
Category:    A | B
Scope:       public | private
Target file: <exact path, e.g., .claude/skills/validate/SKILL.md>
Section:     <heading or line reference>
Current:     <exact current text, if editing an existing passage>
Proposed:    <replacement text>
Rationale:   <conversation moment ("user rewrote X three times") or outcome pattern ("r=0.7 interview correlation")>
Priority:    high | medium | low
```

**Scope guidance:**
- **public** — engine or adapter files that go to public mirror as-is. If the change touches engine content shared between CLAUDE.md and AGENTS.md (or .claude/skills/ and .agents/skills/), cross-sync to the counterpart.
- **private** — personal preference content (preferences.md). Mirrored as `.example` version only.

**Priority guidance:**
- **high** — corrects a behavior the user flagged as wrong or frustrating
- **medium** — improves coverage or precision of an existing rule
- **low** — nice-to-have, no current evidence of harm if skipped

Trivial changes (fixing a typo, updating a stale example) do not need a full card — group them as a "Minor fixes" batch at the end.

---

## Step 4: Data-Driven Additions (when outcome data exists)

If `meta/outcome_summary.yaml` has `by_role_family` entries with 3+ outcomes:

- Surface weight adjustment suggestions with correlation evidence:
  > "Interview rate correlates with keyword coverage (r=0.7) but not verb diversity (r=0.1). Suggest reweighting keyword coverage from 25 → 28 pts and verb diversity from 8 → 5 pts."
- Surface guard threshold tightening:
  > "Quantified evidence below 15/20 correlates with rejection in PM roles. Suggest tightening guard floor from implicit 0 to 14/20."
- Surface new tracking dimensions:
  > "Persona `strong_pass` rate correlates with interview invites (r=0.6). Suggest adding it as a reported meta-metric in Phase 5 presentation."

These go into Category A or B cards like any other proposal.

---

## Step 5: Present Proposals to User

Present all change cards **grouped by category**, high-priority first within each group. Format:

```
## Category A — Skill-Internal Tuning (N proposals)

### [1] High — preferences.md: verb substitution rule
...card...

### [2] Medium — validate/SKILL.md: plateau detection
...card...

## Category B — Skill-External Improvements (N proposals)

### [3] High — CLAUDE.md: feedback routing table
...card...

## Minor Fixes (N items)
- ...
```

**Do NOT apply any change until the user approves.**

If there are no signals to act on, say: "No system updates proposed — the session didn't surface recurring corrections or outcome patterns. Run again after more sessions or an outcome status update."

---

## Step 6: Apply Approved Changes

On user approval (full or partial):

1. Apply only the approved change cards, in order of priority.
2. Edit ONLY the targeted section of the targeted file. Never rewrite a whole file.
3. **Cross-adapter sync (scope: public, engine content only):**
   - If `.claude/skills/*` was modified → sync the corresponding `.agents/skills/*` file
   - If `CLAUDE.md` engine section was modified → sync the corresponding section in `AGENTS.md`
   - If `AGENTS.md` engine section was modified → sync the corresponding section in `CLAUDE.md`
   - Adapter-only files (`.claude/hooks/*`, `.claude/settings.json`) do not need cross-sync.
4. For graduated outcome patterns: remove the pattern from `meta/outcome_summary.yaml` `global_lessons` or `by_role_family` and add it to the permanent rule in its target file.
5. Append an entry to `log/changelog.md`:
   ```
   ## [date] /update-yourself
   - [Category A|B] [file]: [one-line summary of change]
   - [Category A|B] [file]: [one-line summary of change]
   Source: session corrections | outcome graduation | both
   ```

For partial approvals: acknowledge which cards were skipped and why (user declined, deferred, etc.).

---

## Scope

**Hard off-limits — never modify regardless of user request:**
`profile/*` · `index.yaml` · `tracker.yaml`

**Propose → user approves → apply (all changes go through this gate):**
`CLAUDE.md` · `AGENTS.md` · `preferences.md` · `.claude/skills/*.md` · `.agents/skills/*.md` · `templates/*` · `log/changelog.md` · new file creation (e.g., new skill SKILL.md)

**Special constraint:**
`meta/outcome_summary.yaml` — graduation removal only. New entries are written by ingest skill, not here.

---

## Guardrails

- Never fabricate signals. If the conversation was brief, say so.
- Never apply changes without explicit user approval on this run.
- Never rewrite a whole file when a section edit will do.
- Never touch profile data — profile stores facts; framing lives in skills and preferences.
- If a proposed change conflicts with an existing rule in CLAUDE.md, flag the conflict in the change card rather than silently overriding.
