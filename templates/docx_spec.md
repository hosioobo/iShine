# DOCX Template Spec

Use this spec whenever generating a `.docx` resume via `python-docx`.

## Content Order

The DOCX must follow the same rendering order as the HTML/PDF export:

1. **Masthead block (no heading):** Name → Tagline → Summary paragraph
2. **Contact bar** (horizontal rule above and below)
3. **Sections with headings:** Professional Experience → Core Skills → Education → Additional

The `## SUMMARY` heading from the markdown is **not rendered** — its content becomes the masthead paragraph.

## Page & Margins

- Page: US Letter 8.5×11, all margins 0.75in

## Font

- Primary: Arial (fallback: Helvetica, then system sans-serif)
- Use a plain, accessible sans-serif. Do not require a web font to render correctly.

## Colors

- Theme (Stanford Cardinal Red): `#8c1515`
- Ink (body text): `#0a0a0a`
- Muted (tagline, contacts, dates, section headings): `#4a4a4a`
- Rule (divider lines): neutral rule color
- No blue anywhere

## Typography

- **Name:** 24pt, semibold (600 equivalent), title case, theme color, no letter spacing
- **Tagline:** 12pt, default weight, sentence/title case, color muted, no letter spacing. Usually role title only.
- **Summary:** 10pt, color ink, no section heading
- **Contact line:** 9pt, color muted, items joined with ` · `, horizontal rules above/below
- **LinkedIn/GitHub:** display SVG icon + handle (`coreshift`, `hosioobo`) while preserving live links; no `@`; icon color matches handle text and is vertically centered
- **Section headers:** 12pt, semibold (600 equivalent), uppercase, theme color label, `space_before=8pt`, `space_after=6pt`, thin neutral rule above
- **Role title:** 12pt, bold, color ink, `space_before=6pt`
- **Company + date line:** 10pt, color muted, company name not italic, one line joined with ` · `
- **Compact earlier roles:** role title + company/date on one line where possible, no bullets
- **Pagination:** experience entries may split across pages to avoid large blank gaps; keep the role title + company/date heading with the first bullet where possible
- **Body/bullets:** 10pt, color ink, bullet line-height equivalent 1.5
- **Bullet indent:** left 0.375in, first line -0.1875in (hanging)
- **Bullet char:** `•  `
- **Skills labels:** semibold (600 equivalent) + normal content run, `space_after=2pt`

## Inline Formatting

- Inline bold from markdown `**text**` maps to bold run at same size
- Inline italics from markdown `*text*` renders as normal text
- No horizontal rules within body (only contact bar rules)

## Output Naming

- `{First}_{Last}_Resume_{Company}_{Role}.docx` in the job folder
- Derive name from the resume's `# ` heading; Company and Role from the folder name.

Style adjustments should be scripted with targeted edits; do not rewrite from scratch.
