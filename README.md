# iShine

AI-powered resume engine that turns your career profile into tailored, role-specific resumes.

## How It Works

```
JD input → [write] strategy + draft → [validate] persona reviews → [export] PDF/DOCX
```

| Skill | What it does |
|-------|-------------|
| **write** | Analyzes JD → builds strategy → generates tailored resume draft |
| **validate** | Mechanical gate + 3-persona cold review → synthesis → refined v2 |
| **export** | Renders resume/cover letter as PDF or DOCX |
| **ingest** | Manages your career profile data and application outcomes |
| **humanizer** | Removes AI writing patterns from any text |
| **update-yourself** | Self-improvement cycle for the system |

## Setup

1. Clone this repo
2. Copy example files to create your profile:
   ```
   cp index.example.yaml index.yaml
   cp profile/identity.example.md profile/identity.md
   cp profile/projects/example_project.md profile/projects/your_project.md
   cp preferences.example.md preferences.md
   ```
3. Fill in your real data in each file
4. Run with [Claude Code](https://claude.com/claude-code) — paste a job description to get started

## Requirements

- [Claude Code](https://claude.com/claude-code) CLI
- Python 3.9+ (for PDF/DOCX export)

## File Structure

```
├── CLAUDE.md / AGENTS.md    # Orchestrator instructions
├── .claude/skills/          # Claude Code skills
├── .agents/skills/          # Codex-compatible adapter
├── templates/               # Resume & cover letter templates
├── scripts/                 # Export rendering scripts
├── profile/                 # Your career data (gitignored)
├── outputs/                 # Generated resumes (gitignored)
└── preferences.md           # Your style preferences
```

## License

MIT
