# iShine v6.1

## Principles
- profile/ = facts. FRAMING at output time. Never fabricate.
- Each project file is self-contained (metrics, skills, stories, confidence).
- Generate NATIVELY in target language.

## Session Start
- Read index.yaml FIRST (projects, active apps, pending actions).

## Loading Rules
- Prefer .cache/common_context_en.md (or _i18n.md) over individual file reads.
- Prefer .cache/project_frontmatter.yaml for project selection; full-read only 2-3 key projects for story detail.
- .cache/ files are generated — never Edit/Write directly.
- Glossary: included in i18n bundle only. English output does not need glossary.
- NEVER load: log/changelog.md, inbox/processed/*
- Workflow details: see skills (write, validate, ingest, export). Treat casual requests like "export as PDF", "save as DOCX", and "print resume" as export workflow requests.

## Adapter Rules
- Claude remains canonical. `.claude/skills/` is the source of truth; `.agents/skills/` is the Codex adapter layer.
- `.agents/skills/*/SKILL.md` must keep valid YAML frontmatter so Codex can load the adapter skills.
- `.agents` skills may reference canonical `.claude` assets when those assets are mirrored as-is.
- If a workflow step calls for sub-agents, Codex defaults to main-context execution unless the user explicitly asks for delegation or parallel agent work.

## Master Workflow

```
JD input
  │
  ▼
[write] JD → strategy.md → resume_v1.md → mechanical pass
  │
  ▼
[validate]
  ├→ Phase 1: Mechanical gate (XYZ/keyword/Humanizer cleanup + gate measurement)
  ├→ Phase 2: Persona generation [Sub Agent ×1, JD only → personas.md]
  ├→ Phase 3: Persona reviews [Sub Agent ×3 parallel → review_x_vN.md ×3]
  ├→ Phase 4: Synthesis → strategy → v2 [main context: gap analysis → user check → write v2]
  └→ Phase 5: Human loop (versioned doc, feedback routing)
  │
  ▼
[export] → PDF/DOCX
```

### Skills (MECE)

| Skill | Responsibility |
|-------|---------------|
| **write** | JD → strategy + v1 draft + mechanical cleanup |
| **validate** | Persona generation + review orchestrator: gate → personas → cold read → synthesis → v2 |
| **ingest** | Profile data + outcome data management |
| **export** | PDF/DOCX rendering |
| **update-preference** | Voice/tone/style tuning → preferences.md (public) |
| **update-engine** *(dev-only)* | Engine tuning + outcome graduation → CLAUDE.md, skills (dev only) |

### Validate Phase Details
- **Phase 1 (gate):** Mechanical pass (XYZ, keywords, kill words, verb dedup) + gate measurement (keyword coverage, quantified evidence, Humanizer). Fix + 1 re-check if fails. No scoring loop.
- **Phase 2 (personas):** 1 sub agent, JD original text only. Generates 3 personas (HM, FC, ATS/Recruiter). No candidate info — strict isolation for objectivity.
- **Phase 3 (reviews):** 3 sub agents in parallel. Each sees jd.md summary + resume + single persona section only. Outputs narrative review (5-section format) saved as md per persona. Includes interview Q&A.
- **Phase 4 (synthesis):** Main context reads all 3 reviews. Classifies each criticism as Addressable or Needs Your Call. Presents Needs Your Call items to user before writing v2. Builds candidate strategy, updates strategy.md if needed, writes v2.
- **Phase 5 (human loop):** Small feedback → targeted edit. Large feedback (strategy change) → Phase 3 re-run on new version.

## Updates
- Edit ONLY changed keys/sections. Never rewrite a whole file.
- After profile update: (1) edit project file, (2) update index.yaml entry, (3) append changelog.
- Conflict detection: compare dates/roles against index.yaml before updating. Mismatch → ask user.
- Multi-point feedback: when user provides 4+ changes in one message, number each point in the plan and confirm full coverage before proceeding.

## Rule Placement
- preferences.md — voice, tone, subjective style choices (e.g., word preferences, coaching framing)
- .claude/skills/*/SKILL.md — canonical skill rules and shared references
- .agents/skills/*/SKILL.md — Codex adapter metadata plus adapter-specific execution notes
- templates/ — layout, section order, formatting conventions
- scripts/ + templates/docx_spec.md — rendering, appearance, export styling. AGENTS.md and content templates must not contain rendering rules.

## Compact Instructions
When compacting, preserve: selected project IDs, gap analysis, active application path, current draft version, positioning angle, and current validate phase.

## Outcome Tracking (application results → better resumes)
- After resume generation: append entry to meta/outcome_log.yaml.
- On status update: ingest skill extracts patterns into meta/outcome_summary.yaml.
- On new resume: check meta/outcome_summary.yaml for patterns from similar role families.
- Validated outcome patterns graduate to permanent rules via /update-yourself.
- /update-yourself can propose weight adjustments based on outcome correlations.

## Process Improvement (user opinions → better iShine)
- **Public users:** run /update-preference to save voice/tone/style choices → preferences.md only.
- **Dev owner:** run /update-engine to review session and propose engine updates.
- /update-engine input: user corrections, friction points, style preferences from conversation.
- /update-engine output: targeted edits to AGENTS.md, skills, or preferences.md (with user approval).
- Two categories: (A) skill-internal tuning (weights, thresholds), (B) skill-external improvements (new skills, workflow changes).

## Output Rules
- Versioning: copy vN → vN+1, edit. Never rewrite from scratch.
- Statuses: applied | screen | interview | offer | rejected | withdrawn | ghosted
- Resume bullets: XYZ format at output time. Profile stores raw facts.
- Interview prep (notes.md): STAR format for behavioral answers.

## Session End
- Update index.yaml: session date, summary, pending_actions, active_applications.
