---
name: recommend-jobs
description: >
  Job recommendation skill for iShine. Use this skill whenever the user asks to find jobs,
  recommend opportunities, scan the market, show what roles fit them, or says things like
  "find jobs for me", "recommend jobs", "what should I apply to", "scan jobs", or
  "show me good openings". The skill refreshes live ATS-backed recommendations, summarizes
  the shortlist, and leaves promotion into a real application as an explicit next step.
---

# Job Recommendation Skill

## Input

$ARGUMENTS — optional narrowing instructions for what to emphasize or deprioritize.

## Steps

### 1. Refresh live recommendations

Choose the mode based on what the user asked for:

- **Default** — broad scan, all relevant roles: `python3 -m ops.scripts.refresh_recommendations`
- **Winnable** — core-strength roles only, no stretch titles: `python3 -m ops.scripts.refresh_recommendations --mode winnable`

Use winnable mode when the user says "winnable", "strong fit only", "best chances", "most likely to land", or similar.

This refresh must:
- fetch live ATS-backed jobs
- scan them into the queue
- triage them against the current master resume
- render review artifacts

Do not ask the user to run raw commands manually.

### 2. Read the latest recommendation artifacts

Inspect the most recent:

- `ops/reports/recommendations/*/top-recommendations.json`
- `ops/reports/recommendations/*/summary.md`

If the shortlist is empty, report that honestly and say why if the artifacts make the reason visible.

### 3. Summarize the shortlist

Present the top recommendations in priority order.

For each role, include:
- company
- title
- location
- score
- why it surfaced (reason codes + brief plain-language explanation)

Default to the top 10 unless the shortlist is smaller.

### 4. Handoff

If the user selects a role, hand off to the `start-application` flow instead of exposing queue internals.
