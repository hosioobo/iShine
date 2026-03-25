# DOCX Template Spec

Use this spec whenever generating a `.docx` resume via `python-docx`.

## Content Order

The DOCX must follow the same rendering order as the HTML/PDF export:

1. **Masthead block (no heading):** Name → Tagline → Summary paragraph
2. **Contact bar** (horizontal rule above and below)
3. **Sections with headings:** Core Skills → Professional Experience → Education → Additional

The `## SUMMARY` heading from the markdown is **not rendered** — its content becomes the masthead paragraph.

## Page & Margins

- Page: US Letter 8.5×11, all margins 0.75in

## Font

- Primary: Inter (fallback: Arial, then system sans-serif)
- Install Inter if available; degrade gracefully to Arial

## Colors

- Ink (body text): `#0a0a0a`
- Muted (tagline, contacts, dates, section headings): `#4a4a4a`
- Rule (divider lines): `#bdbdbd`
- No blue anywhere

## Typography

- **Name:** 22pt, semibold (600 equivalent), uppercase, color ink
- **Tagline:** 10pt, light weight, uppercase, color muted
- **Summary:** 10pt, color ink, no section heading
- **Contact line:** 9pt, color muted, items joined with ` · `, horizontal rules above/below
- **Section headers:** 12pt, medium weight, uppercase, color muted, `space_before=8pt`, `space_after=3pt`, thin rule above
- **Role title:** 11pt, bold, color ink, `space_before=6pt`
- **Company + date line:** 9pt, color muted, company name italic, one line joined with ` · `
- **Body/bullets:** 10pt, color ink
- **Bullet indent:** left 0.375in, first line -0.1875in (hanging)
- **Bullet char:** `•  `
- **Skills labels:** semibold (600 equivalent) + normal content run, `space_after=2pt`

## Inline Formatting

- Inline bold from markdown `**text**` maps to bold run at same size
- No horizontal rules within body (only contact bar rules)

## Output Naming

- `{First}_{Last}_Resume_{Company}_{Role}.docx` in the job folder
- Derive name from the resume's `# ` heading; Company and Role from the folder name.

Style adjustments should be scripted with targeted edits; do not rewrite from scratch.
