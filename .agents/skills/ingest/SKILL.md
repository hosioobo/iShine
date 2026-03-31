---
name: ingest
description: >
  Inbox Processing Skill for iShine. Use this skill when the user shares new career info,
  project updates, corrections to their profile, or application outcome results — whether
  via a file path, pasted text, or casual message. Do NOT trigger for JD input (triggers
  write skill) or for questions about past ingest results.
---

# Inbox Processing Skill

## Input
$ARGUMENTS — file path(s) in inbox/ to process, OR inline text with career/project/outcome data

## Inbox Folder Structure
- `inbox/` — profile data (career info, project updates, corrections)
- `inbox/jd/` — reserved for JD files; ingest does NOT process these. JDs trigger the write skill.

## Step 0: Classify Input
Before executing any steps, classify the input into one or more of:
- **[profile]** — new career data, project updates, corrections, tool/system changes
- **[outcome]** — application status update (screen, interview, offer, rejected, withdrawn, ghosted)
- **[both]** — input contains both types

Execute only the paths that match. Do not skip steps within a matched path.

## Path A: Profile Data Ingestion

**Required for all [profile] inputs.**

1. Read source (inbox file or inline text). Extract: new data, new proper nouns, corrections.
2. Conflict check: compare dates/roles against index.yaml. Flag mismatches to user before continuing.
3. Update project file in `profile/projects/`:
   - Add/update metrics with concrete numbers or milestones
   - Add new story entries (id, title, tags, SAR body) if the input describes a new outcome or method
   - Update existing story Results if previously "in progress"
   - Append raw input verbatim to `## Raw Notes` section with date header — NEVER skip this step
   - Update `last_updated` and `source` fields
4. New proper nouns → `locale/glossary.yaml`.
5. Update `index.yaml`: add/edit project entry (id, metric, tags).
6. Append to `log/changelog.md`.

**Completion check:** Confirm all 6 steps executed. If any step was skipped, execute it now.

## Path B: Outcome Data Ingestion

**Required for all [outcome] inputs.**

7. Update `tracker.yaml`: set application status + date.
8. Append to `meta/outcome_log.yaml`:
   - status, date, resume_version used, quality_score (if available from iteration_log.tsv)
9. Pattern extraction: scan outcome_log.yaml for recurring patterns.
    - If 3+ outcomes share a trait → append pattern to `meta/outcome_summary.yaml`
    - Patterns include: score thresholds, keyword coverage, role_family trends, positioning angles

## DO NOT load
glossary.yaml (unless generating output), changelog.md, identity.md
