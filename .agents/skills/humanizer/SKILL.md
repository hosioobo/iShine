# Humanizer

Remove AI writing patterns from documents and make them sound authentically human. This skill uses selective loading — it reads only the reference file relevant to the current document type, keeping its guidance focused and accurate.

---

## Step 1: Identify the Document Type

Ask the user what type of document they're working with. Present these options:

- **Resume** — work history, bullet points, professional experience
- **Cover letter** — job application letter, narrative self-introduction
- **Blog post** — informal long-form writing, personal or brand voice
- **News / editorial article** — journalistic writing, reporting, opinion pieces
- **Marketing copy** — ads, landing pages, emails, promotional content

If the user has already stated the document type in their request, skip this step.

---

## Step 2: Load Reference Materials

Load exactly two files — no more.

**Always load (universal patterns):**
```
.claude/skills/humanizer/references/base-patterns.md
```

**Then load ONE document-specific file:**

| Document type | File to load |
|---|---|
| Resume | `.claude/skills/humanizer/references/resume-cover-letter.md` |
| Cover letter | `.claude/skills/humanizer/references/resume-cover-letter.md` |
| Blog post | `.claude/skills/humanizer/references/blog.md` |
| News / editorial | `.claude/skills/humanizer/references/news-article.md` |
| Marketing copy | `.claude/skills/humanizer/references/marketing.md` |

Note: Reference files are stored in `.claude/skills/humanizer/references/` (canonical location, shared across adapters).

Do not load all reference files. Load only the one that matches the document type.

---

## Step 3: Humanize the Text

Apply both the base patterns and the document-specific patterns. Work in this order:

1. **Scan for AI patterns** — identify everything that needs fixing before rewriting anything
2. **Fix language patterns first** — vocabulary, grammar, sentence structure
3. **Fix style patterns** — em dashes, bold abuse, bullet formatting, title case
4. **Fix content patterns** — significance inflation, vague attributions, formulaic sections
5. **Add soul** — after removing bad patterns, inject personality and specificity (see below)

### Adding Soul — The Part Most Humanizers Skip

Removing AI patterns is only half the job. Sterile, voiceless writing is just as obvious as AI slop. Good writing has a human behind it.

**Signs of soulless writing (even if technically "clean"):**
- Every sentence is the same length and structure
- No opinions, just neutral reporting (unless writing news)
- No acknowledgment of uncertainty or complexity
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a press release or Wikipedia entry

**How to add voice:**
- Have opinions. Don't just report facts — react to them
- Vary rhythm: short punchy sentence. Then one that takes its time getting where it's going
- Acknowledge complexity: "This is impressive but also kind of unsettling" beats "This is impressive"
- Use "I" when it fits (not in resumes — see document-specific rules)
- Let some mess in: tangents, asides, and half-formed thoughts are human
- Be specific about feelings: not "this is concerning" but "there's something unsettling about..."

> Note: The degree of personality appropriate varies by document type. Blog posts welcome full voice. Resumes need confidence and specificity. News needs neutrality. See the document-specific reference for calibration.

---

## Step 4: Present Output

Provide:
1. The rewritten text
2. A brief summary of the main patterns fixed (3–6 bullet points is enough — don't list every single change)

Keep the summary practical. Name the patterns you removed and what you added instead.

---

## Key Principle

Specificity beats vagueness every time. The most common AI failure is making claims without evidence. The fix is almost always the same: cut the vague claim, keep the concrete detail, add the one that's missing.

Before: "Drove significant improvements to team performance."
After: "Cut sprint planning from 2 hours to 45 minutes by switching to async pre-reads."
