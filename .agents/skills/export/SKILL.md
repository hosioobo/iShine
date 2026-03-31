---
name: export
description: >
  Use this skill whenever the user asks to export, render, save, convert, or
  print a resume or cover letter as PDF, HTML, or DOCX. Trigger on any of:
  "export", "render", "save as PDF", "save as DOCX", "print resume",
  "convert to PDF", "convert to DOCX", "save as Word", "generate PDF", or any
  request to produce a file version of the current resume or cover letter.
  When in doubt, trigger — it is far better to run this skill unnecessarily
  than to miss it and leave the user without a file.
---

# Export Skill

## Input
$ARGUMENTS — format (pdf|docx|html), optional source path. Both are optional.
Default format: **PDF**.

## Steps

### Step 1 — Identify the source file
- If the user provided an explicit path, use it.
- Otherwise, read tracker.yaml and use the most recent entry where status is not rejected/withdrawn/ghosted. If multiple active candidates exist, ask the user which application to target.
- If the user said "cover letter", target `cover_letter_v*.md` instead.
- If no matching file is found, tell the user and stop.

### Step 2 — Determine the output filename
- Output to the **same folder** as the source file.
- Pattern: `{First}_{Last}_Resume_{Company}_{Role}_v{N}.{ext}`
- Derive the candidate name from the resume's `# ` heading (e.g., `# Jane Doe` → `Jane_Doe`).
- Derive Company and Role from the folder name (`YYYYMMDD_company_role`).
- Preserve the version number from the source filename.
- If an output file with the same name already exists, confirm with the user before overwriting.

### Step 3 — Run the export

**PDF (default):**
```
python3 scripts/export_resume_web_pdf.py <input.md> <output.html> --pdf <output.pdf>
```
Requires Google Chrome. Produces both HTML and PDF in one step.

Fallback (no Chrome):
```
python3 scripts/export_resume_pdf.py <input.md> <output.pdf>
```
Requires: `pip install reportlab`. Produces PDF only (no HTML). Lower visual fidelity — inform the user.

**HTML only:**
```
python3 scripts/export_resume_web_pdf.py <input.md> <output.html>
```
Omit the `--pdf` flag.

**DOCX:**
Build using `python-docx` following `templates/docx_spec.md` for all styling details.
Fallback: `/opt/homebrew/bin/pandoc <input.md> -o <output.docx>` — unstyled, warn the user.

### Step 4 — Verify and report
1. Confirm the output file exists. If not, show the full stderr output and stop.
2. Check file size: PDF < 5 KB or DOCX < 2 KB almost always means a rendering failure — flag it.
2.5. **Section check (PDF only):** Scan the source markdown for `## ` headings. Standard renderable sections: SUMMARY · CORE SKILLS · PROFESSIONAL EXPERIENCE · ADDITIONAL EXPERIENCE & LANGUAGES · EDUCATION. If any heading falls outside this list, warn before exporting: "Section [X] will be dropped from the PDF. Move its content to a standard section, or use DOCX/HTML instead."
3. Verify obvious output issues (missing nested bullets, missing pages).
4. Report the output path(s) to the user.

## Constraints
- **Never modify the source markdown.**
- If the export script exits with a non-zero code, show the full stderr before attempting any fallback.
