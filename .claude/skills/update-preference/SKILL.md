---
name: update-preference
description: >
  Tune voice, tone, and style preferences for iShine. Invoke when the user
  says "/update-preference", "remember my style", "update my preferences",
  "save this tone choice", "tune my voice", or "remember this for my preferences".
  DO NOT auto-run — explicit invocation only. For engine changes (skill weights,
  workflow logic, new skills), use /update-engine (dev-only) instead.
---

# Update Preference Skill

## Purpose

Capture voice, tone, and style signals from the session and apply them to
`preferences.md`. Engine files are off-limits here.

## When to invoke

Explicit user command only: `/update-preference` or equivalent phrasing.
DO NOT auto-trigger.

---

## Step 1: Collect Preference Signals

Scan the session for voice and style signals only:

| Signal type | What to look for | Threshold |
|---|---|---|
| **Word substitutions** | User preferred a specific word/phrase over the generated one | Any |
| **Tone corrections** | User adjusted energy level, formality, or register | Any |
| **Bullet structure** | User rewrote a bullet revealing a structural style preference | Any |
| **Section framing** | User changed how a section opens or closes | Any |
| **Summary arc** | User adjusted the narrative flow of the summary | Any |
| **Kill word additions** | User flagged a word/phrase as off-brand | Any explicit |

If the session has no preference signals, say so: "No preference updates found this session." Do not fabricate signals.

---

## Step 2: Draft Each Change

For every signal, produce a change card:

```
[Preference Change Card]
Target:    preferences.md
Section:   <Phase 1 / Phase 3 / Content — Persona Judgment>
Current:   <exact current text, or "none" if adding new rule>
Proposed:  <replacement or new rule>
Rationale: <the session moment: "user changed X to Y in bullet N">
```

---

## Step 3: Present and Apply

Present all cards grouped by section. **Do NOT apply until user approves.**

On approval:
1. Edit ONLY the targeted section of `preferences.md`. Never rewrite the file.
2. Append to `log/changelog.md`:
   ```
   ## [date] /update-preference
   - preferences.md [section]: [one-line summary]
   Source: session style corrections
   ```

For partial approvals: acknowledge which cards were skipped.

---

## Scope

**Allowed:** `preferences.md` · `log/changelog.md`

**Hard off-limits — never touch regardless of user request:**
`CLAUDE.md` · `AGENTS.md` · `.claude/skills/*` · `.agents/skills/*` · `profile/*` · `index.yaml` · `meta/*`

For engine-level changes (skill weights, workflow logic, new skills, outcome graduation), the dev owner uses `/update-engine`.
