# iShine

Paste a job description, get a tailored resume. iShine analyzes the JD, selects your best-fit experience, validates through simulated hiring reviews, and exports a polished PDF or DOCX.

Powered by [Claude Code](https://claude.ai/claude-code). Also compatible with [Codex](https://github.com/openai/codex).

<!-- TODO: demo GIF here -->

## Why iShine?

Rewriting your resume for every application is slow, repetitive, and error-prone. Most people either submit a generic resume or spend hours tailoring by hand.

iShine automates the hard parts:

1. **Analyzes the JD** — extracts key requirements, keywords, and signals
2. **Builds a positioning strategy** — selects the most relevant projects and metrics from your profile
3. **Drafts a tailored resume** — XYZ-format bullets, JD-aligned skills section
4. **Validates with 3 simulated personas** — hiring manager, functional colleague, and recruiter each review your draft cold
5. **Exports** to PDF or DOCX

Your career data stays local — nothing is sent to external servers beyond the AI model API.

## Skills

```
JD input → [write] strategy + draft → [validate] persona reviews → [export] PDF/DOCX

Utilities:  [ingest] profile data    [humanizer] AI tone fix    [update-yourself] system tuning
```

| Skill | What it does |
|-------|-------------|
| **write** | JD analysis → positioning strategy → tailored resume draft |
| **validate** | Mechanical gate + 3-persona cold review → synthesis → refined v2 |
| **export** | Renders resume or cover letter as PDF / DOCX |
| **ingest** | Adds career data, project updates, or application outcomes to your profile |
| **humanizer** | Detects and removes AI writing patterns from any text |
| **update-yourself** | Tunes the system based on your feedback and session history |

### Outcome tracking

Track which resumes led to interviews. iShine logs application results and uses outcome patterns to improve future drafts — prioritizing strategies that have worked for similar roles.

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI (or [Codex](https://github.com/openai/codex))
- Python 3.9+
- Playwright for PDF export:
  ```bash
  pip install playwright && playwright install chromium
  ```

## Setup

1. Clone this repo
2. Copy example files to create your profile:
   ```bash
   cp index.example.yaml index.yaml
   mkdir -p profile/projects
   cp profile/identity.example.md profile/identity.md
   cp profile/projects/example_project.md profile/projects/my_project.md
   cp preferences.example.md preferences.md
   ```
3. Fill in your data:
   - `profile/identity.md` — name, contact info, career summary, education
   - `profile/projects/*.md` — one file per role or project (metrics, skills, stories in SAR format)
   - `preferences.md` — tone, verb choices, formatting preferences
4. Open the repo in Claude Code and paste a job description to get started

## Agent Compatibility

| Agent | How it works |
|-------|-------------|
| **Claude Code** (primary) | Skills in `.claude/skills/`, orchestrated by `CLAUDE.md` |
| **Codex** | Skills in `.agents/skills/`, orchestrated by `AGENTS.md` |

Both agents read from the same core — templates, scripts, and profile data are shared. The `.claude/` and `.agents/` directories contain agent-specific skill definitions only.

## File Structure

```
├── CLAUDE.md                # Claude Code orchestrator
├── AGENTS.md                # Codex orchestrator
├── .claude/skills/          # Claude Code skills (canonical)
├── .agents/skills/          # Codex adapter skills
├── templates/               # Resume & cover letter templates (en + ko)
├── scripts/                 # Export rendering scripts
├── preferences.example.md   # Style & tone preferences (template)
├── index.example.yaml       # Runtime state (template)
└── profile/                 # Your career data (gitignored)
```

## FAQ

**Do I need to be a developer to use this?**
No. If you can install Claude Code and run terminal commands, you can use iShine. The setup takes about 15 minutes.

**Does it support languages other than English?**
Yes. iShine generates resumes natively in the target language. English and Korean templates are included.

**Where is my data stored?**
All career data stays in `profile/` on your local machine. It is gitignored by default — nothing is committed or uploaded unless you choose to.

**How much does it cost?**
iShine itself is free and open-source. You need a Claude Code subscription (or Codex) for the AI model, and usage is billed by token through your provider.

## License

MIT
