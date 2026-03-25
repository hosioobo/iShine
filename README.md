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

## Getting Started

### 1. Install

Open [Claude Code](https://claude.ai/claude-code) (or [Codex](https://github.com/openai/codex)) and say:

> "Clone https://github.com/hosioobo/iShine and set it up for me."

That's it. The agent handles the rest — cloning, copying example files, and creating the folder structure.

### 2. Build your profile

Drop your career info into the conversation — a resume PDF, a LinkedIn export, bullet points, anything:

> "Here's my background. Organize this into my profile."

iShine will parse it and structure everything into the right files. You can add more anytime:

> "I just finished a project where I migrated 3 services to Kubernetes and cut deploy time by 40%. Add this."

### 3. Generate a resume

Paste a job description URL or text:

> "Write a resume for this: https://example.com/jobs/12345"

iShine analyzes the JD, picks the best-fit experience from your profile, and drafts a tailored resume. Then run validation:

> "Validate the draft."

Three simulated reviewers (hiring manager, recruiter, functional peer) will critique it. iShine synthesizes their feedback and produces a refined v2.

### 4. Export

> "Export as PDF."

### Requirements

- [Claude Code](https://claude.ai/claude-code) or [Codex](https://github.com/openai/codex)
- Python 3.9+ with Playwright (for PDF/DOCX export — the agent will install it if needed)

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
No. Everything is done through natural language. If you can install Claude Code, you can use iShine.

**Does it support languages other than English?**
Yes. iShine generates resumes natively in the target language. English and Korean templates are included.

**Where is my data stored?**
All career data stays in `profile/` on your local machine. It is gitignored by default — nothing is committed or uploaded unless you choose to.

**How much does it cost?**
iShine itself is free and open-source. You need a Claude Code subscription (or Codex) for the AI model, and usage is billed by token through your provider.

## License

MIT
