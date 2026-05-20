#!/usr/bin/env python3
"""Render a resume markdown file to refined HTML and optional PDF.

The markdown source stays canonical. This script parses the repo's resume
structure into a restrained HTML/CSS layout and can print it via headless
Chrome for higher-fidelity PDFs than the minimal ReportLab exporter.
"""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


CHROME_CANDIDATES = [
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
]

CONTACT_ICONS = {
    "github": (
        "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 "
        "11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-"
        "1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.087-.744.084-.729."
        "084-.729 1.205.084 1.84 1.236 1.84 1.236 1.07 1.835 2.809 1.305 "
        "3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 "
        "0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 "
        "1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 "
        "3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 "
        "3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 "
        "5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 "
        "0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-"
        "5.373-12-12-12"
    ),
    "linkedin": (
        "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-"
        "1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046"
        "c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 "
        "5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 "
        "0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 "
        "2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564"
        "v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 "
        "23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 "
        "22.271V1.729C24 .774 23.2 0 22.222 0h.003z"
    ),
}


@dataclass
class ExperienceEntry:
    role: str
    company: str
    context: str
    dates: str
    bullets: list["BulletItem"] = field(default_factory=list)


@dataclass
class BulletItem:
    text: str
    children: list["BulletItem"] = field(default_factory=list)


@dataclass
class ResumeData:
    name: str
    tagline: str
    contacts: list[str]
    summary: list[str]
    core_skills: list[str]
    experience: list[ExperienceEntry]
    education: list[list[str]]
    additional: list[list[str]]


def inline_html(text: str) -> str:
    placeholders: dict[str, str] = {}

    def stash_anchor(label: str, url: str) -> str:
        token = f"__URL_{len(placeholders)}__"
        href = url if "://" in url else f"https://{url}"
        placeholders[token] = (
            f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'
        )
        return token

    markdown_link_pattern = re.compile(
        r"\[([^\]]+)\]\((https?://[^\s)]+|(?:linkedin|github)\.com/[^\s)]+)\)"
    )
    text = markdown_link_pattern.sub(
        lambda match: stash_anchor(match.group(1), match.group(2)), text
    )

    url_pattern = re.compile(r"(https?://[^\s]+|linkedin\.com/[^\s]+|github\.com/[^\s]+)")
    text = url_pattern.sub(lambda match: stash_anchor(match.group(0), match.group(0)), text)
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", escaped)
    for token, replacement in placeholders.items():
        escaped = escaped.replace(html.escape(token), replacement)
    return escaped


def parse_bold_prefix(text: str) -> tuple[str, str]:
    match = re.match(r"^\*\*(.+?)\*\*(.*)$", text)
    if not match:
        return "", text
    return match.group(1).strip(), match.group(2).strip()


def clean_lines(md_path: Path) -> list[str]:
    return [line.rstrip("\n") for line in md_path.read_text(encoding="utf-8").splitlines()]


def skip_front_matter(lines: list[str], idx: int) -> int:
    if idx >= len(lines) or lines[idx].strip() != "---":
        return idx

    idx += 1
    while idx < len(lines) and lines[idx].strip() != "---":
        idx += 1

    if idx < len(lines) and lines[idx].strip() == "---":
        idx += 1
    return idx


def parse_company_line(line: str) -> tuple[str, str, str]:
    company, tail = parse_bold_prefix(line)
    tail = tail.lstrip()
    if tail.startswith("("):
        context, sep, rest = tail.partition(")")
        context = context.lstrip("(").strip()
        rest = rest.strip()
    else:
        context = ""
        sep = ""
        rest = tail

    if sep:
        remainder = rest
    else:
        remainder = tail

    if remainder.startswith("·"):
        remainder = remainder[1:].strip()
    return company, context, remainder


def parse_experience_heading(heading: str) -> tuple[str, str, str, str]:
    """Parse headings that inline role, bold company, and dates.

    Standard entries keep company/dates on the following line, but compact
    entries sometimes use: `Role · **Company** · Dates`.
    """
    match = re.match(
        r"^(?P<role>.+?)\s+·\s+\*\*(?P<company>.+?)\*\*\s+·\s+(?P<dates>.+)$",
        heading,
    )
    if not match:
        return heading, "", "", ""
    return (
        match.group("role").strip(),
        match.group("company").strip(),
        "",
        match.group("dates").strip(),
    )


def parse_resume(md_path: Path) -> ResumeData:
    lines = clean_lines(md_path)
    idx = 0

    def skip_blank(pointer: int) -> int:
        while pointer < len(lines) and not lines[pointer].strip():
            pointer += 1
        return pointer

    idx = skip_blank(idx)
    idx = skip_front_matter(lines, idx)
    idx = skip_blank(idx)
    if idx >= len(lines) or not lines[idx].startswith("# "):
        raise ValueError(f"Expected resume name heading in {md_path}")
    name = lines[idx][2:].strip()
    idx += 1

    idx = skip_blank(idx)
    tagline = lines[idx].strip().strip("*") if idx < len(lines) else ""
    idx += 1

    idx = skip_blank(idx)
    contacts = []
    if idx < len(lines) and lines[idx].strip() != "---":
        contacts = [part.strip() for part in lines[idx].split("·")]
        idx += 1

    while idx < len(lines) and lines[idx].strip() != "---":
        idx += 1
    if idx < len(lines) and lines[idx].strip() == "---":
        idx += 1

    sections: dict[str, list[str]] = {}
    current = ""
    buffer: list[str] = []
    while idx < len(lines):
        raw = lines[idx]
        stripped = raw.strip()
        if stripped == "---":
            idx += 1
            continue
        if stripped.startswith("## "):
            if current:
                sections[current] = buffer[:]
            current = stripped[3:].strip().upper()
            buffer = []
        else:
            buffer.append(raw)
        idx += 1
    if current:
        sections[current] = buffer

    summary = [
        " ".join(chunk.strip() for chunk in paragraph if chunk.strip())
        for paragraph in split_blocks(sections.get("SUMMARY", []))
        if any(chunk.strip() for chunk in paragraph)
    ]
    # Core skill rows are visually meaningful in the source markdown.
    # Preserve each non-empty line instead of paragraph-joining the section.
    core_skills = [
        line.strip()
        for line in sections.get("CORE SKILLS", [])
        if line.strip()
    ]
    experience = parse_experience(sections.get("PROFESSIONAL EXPERIENCE", []))
    education = split_blocks(sections.get("EDUCATION", []))
    additional = split_blocks(
        sections.get("ADDITIONAL EXPERIENCE & LANGUAGES", [])
        or sections.get("ADDITIONAL", [])
    )

    return ResumeData(
        name=name,
        tagline=tagline,
        contacts=contacts,
        summary=summary,
        core_skills=core_skills,
        experience=experience,
        education=education,
        additional=additional,
    )


def split_blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for raw in lines:
        if raw.strip():
            current.append(raw.strip())
            continue
        if current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def parse_experience(lines: list[str]) -> list[ExperienceEntry]:
    entries: list[ExperienceEntry] = []
    current: ExperienceEntry | None = None
    bullet_stack: list[tuple[int, BulletItem]] = []
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            bullet_stack = []
            continue
        if stripped.startswith("### "):
            if current:
                entries.append(current)
            role, company, context, dates = parse_experience_heading(stripped[4:].strip())
            current = ExperienceEntry(
                role=role,
                company=company,
                context=context,
                dates=dates,
            )
            bullet_stack = []
            continue
        if current is None:
            continue
        if stripped.startswith("**") and not current.company:
            current.company, current.context, current.dates = parse_company_line(stripped)
            bullet_stack = []
            continue
        bullet_match = re.match(r"^(\s*)- (.+)$", raw)
        if bullet_match:
            indent = len(bullet_match.group(1).replace("\t", "    "))
            item = BulletItem(text=bullet_match.group(2).strip())
            while bullet_stack and bullet_stack[-1][0] >= indent:
                bullet_stack.pop()
            if bullet_stack:
                bullet_stack[-1][1].children.append(item)
            else:
                current.bullets.append(item)
            bullet_stack.append((indent, item))
            continue
        if bullet_stack:
            bullet_stack[-1][1].text = f"{bullet_stack[-1][1].text} {stripped}".strip()
        elif current.context:
            current.context = f"{current.context} {stripped}".strip()
        else:
            current.context = stripped
    if current:
        entries.append(current)
    return entries


def section_heading(title: str) -> str:
    safe = html.escape(title)
    return (
        '<div class="section-header">'
        f'<span class="section-label">{safe}</span>'
        '<span class="section-rule" aria-hidden="true"></span>'
        "</div>"
    )


def render_contacts(contacts: list[str]) -> str:
    def priority(item: str) -> tuple[int, str]:
        lowered = item.lower()
        if "@" in item:
            return (0, lowered)
        if item.startswith("+") or re.match(r"^\(?\d", item):
            return (1, lowered)
        if "linkedin.com/" in lowered:
            return (3, lowered)
        if "github.com/" in lowered:
            return (4, lowered)
        return (2, lowered)

    rendered = []
    for item in sorted(contacts, key=priority):
        safe = inline_html(item)
        if "@" in item:
            href = f'mailto:{html.escape(item, quote=True)}'
            safe = f'<a href="{href}">{html.escape(item)}</a>'
        elif item.startswith("linkedin.com/"):
            safe = (
                f'<a href="https://{html.escape(item, quote=True)}">'
                f'{render_contact_handle("linkedin", item.rsplit("/", 1)[-1])}</a>'
            )
        elif item.startswith("github.com/"):
            safe = (
                f'<a href="https://{html.escape(item, quote=True)}">'
                f'{render_contact_handle("github", item.rsplit("/", 1)[-1])}</a>'
            )
        rendered.append(f'<li class="contact-item">{safe}</li>')
    return "\n".join(rendered)


def render_contact_handle(icon: str, handle: str) -> str:
    path = CONTACT_ICONS[icon]
    return (
        '<svg class="contact-icon" role="img" aria-hidden="true" '
        'viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
        f'<path d="{html.escape(path, quote=True)}"></path></svg>'
        f'<span>{html.escape(handle)}</span>'
    )


def render_labeled_blocks(blocks: list[list[str]]) -> str:
    rendered = []
    for block in blocks:
        lead = block[0].strip()
        details = [line.strip() for line in block[1:] if line.strip()]
        label, rest = parse_bold_prefix(lead)
        if label:
            separator = " — "
            label = label.rstrip(":").strip()
            if rest.startswith(":"):
                separator = ": "
                rest = rest[1:].strip()
            elif rest.startswith("—"):
                rest = rest[1:].strip()
            rendered.append(
                '<div class="support-item">'
                f'<p class="support-line"><strong>{html.escape(label)}</strong>'
                f"{separator}{inline_html(rest)}</p>"
                + "".join(
                    f'<p class="support-note">{inline_html(detail)}</p>'
                    for detail in details
                )
                + "</div>"
            )
        else:
            rendered.append(
                '<div class="support-item">'
                f'<p class="support-line">{inline_html(lead)}</p>'
                + "".join(
                    f'<p class="support-note">{inline_html(detail)}</p>'
                    for detail in details
                )
                + "</div>"
            )
    return "\n".join(rendered)


def render_html(data: ResumeData, theme: str = "#8c1515") -> str:
    header_summary_html = "\n".join(
        f'<p class="header-summary">{inline_html(paragraph)}</p>' for paragraph in data.summary
    )
    skills_html = "\n".join(
        f'<p class="skill-line">{inline_html(line)}</p>' for line in data.core_skills
    )
    experience_html = "\n".join(render_experience(entry) for entry in data.experience)
    education_html = render_labeled_blocks(data.education)
    additional_html = render_labeled_blocks(data.additional)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(data.name)} Resume</title>
  <style>
    :root {{
      --ink: #0a0a0a;
      --muted: #4a4a4a;
      --rule: #bdbdbd;
      --paper: #ffffff;
      --theme: {theme};
    }}

    @page {{
      size: Letter;
      margin: 0.67in 0.72in 0.67in 0.72in;
    }}

    * {{
      box-sizing: border-box;
    }}

    html {{
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    body {{
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
      font-size: 10pt;
      line-height: 1.4;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }}

    main {{
      width: 100%;
    }}

    h1, h2, h3, p, ul {{
      margin: 0;
    }}

    .resume {{
      width: 100%;
    }}

    .masthead {{
      padding: 0;
    }}

    .name {{
      font-size: 24pt;
      font-weight: 600;
      letter-spacing: 0;
      line-height: 1.02;
      color: var(--theme);
      margin-bottom: 0.06in;
    }}

    .tagline {{
      font-size: 12pt;
      letter-spacing: 0;
      line-height: 1.25;
      color: var(--muted);
      margin-bottom: 0.1in;
    }}

    .header-summary {{
      font-size: 10pt;
      line-height: 1.42;
      text-wrap: pretty;
    }}

    .contact-bar {{
      margin-top: 0.1in;
      margin-bottom: 0.17in;
      padding: 0.08in 0;
      border-top: 1px solid var(--rule);
      border-bottom: 1px solid var(--rule);
    }}

    .contacts {{
      list-style: none;
      display: flex;
      justify-content: space-evenly;
      flex-wrap: nowrap;
      gap: 0.12in;
      padding: 0;
      color: var(--muted);
      font-size: 9pt;
      line-height: 1.3;
      text-align: center;
    }}

    .contact-item {{
      display: inline-flex;
      align-items: center;
      white-space: nowrap;
    }}

    .contact-item a {{
      color: inherit;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
    }}

    .contact-icon {{
      width: 0.13in;
      height: 0.13in;
      margin-right: 0.035in;
      fill: currentColor;
      flex: 0 0 auto;
      display: block;
    }}

    section {{
      margin-top: 0.24in;
    }}

    section:first-of-type {{
      margin-top: 0;
    }}

    .section-header {{
      display: block;
      border-top: 1px solid var(--rule);
      padding-top: 0.1in;
      margin-bottom: 0.2in;
      break-after: avoid;
    }}

    section:first-of-type .section-header {{
      border-top: none;
      padding-top: 0;
    }}

    .section-label {{
      display: block;
      font-size: 12pt;
      font-weight: 600;
      letter-spacing: 0;
      text-transform: uppercase;
      line-height: 1.2;
      color: var(--theme);
    }}

    .section-rule {{
      display: none;
    }}

    .skill-line {{
      font-size: 10pt;
      line-height: 1.4;
    }}

    .skill-line strong {{
      font-size: 10pt;
      font-weight: 600;
      letter-spacing: 0;
    }}

    .skill-line + .skill-line {{
      margin-top: 0.03in;
    }}

    .experience-item {{
      break-inside: auto;
    }}

    .experience-heading {{
      break-inside: avoid;
      break-after: avoid;
    }}

    .experience-heading + .bullets {{
      break-before: avoid;
    }}

    .experience-item + .experience-item {{
      margin-top: 0.18in;
    }}

    .experience-item.compact {{
      break-inside: avoid;
    }}

    .experience-item.compact .experience-heading {{
      display: flex;
      align-items: baseline;
      gap: 0.08in;
    }}

    .experience-item.compact + .experience-item.compact {{
      margin-top: 0.08in;
    }}

    .role {{
      display: block;
      font-size: 12pt;
      font-weight: 700;
      letter-spacing: 0;
      line-height: 1.2;
      margin-bottom: 0.02in;
    }}

    .experience-item.compact .role {{
      flex: 0 0 auto;
      font-size: 10pt;
      margin-bottom: 0;
    }}

    .meta-row {{
      font-size: 10pt;
      color: var(--muted);
      margin-bottom: 0.04in;
      line-height: 1.3;
      text-wrap: pretty;
    }}

    .experience-item.compact .meta-row {{
      margin-bottom: 0;
    }}

    .company {{
      font-style: normal;
    }}

    .context {{
      font-style: normal;
    }}

    ul.bullets {{
      list-style: disc;
      padding-left: 0.18in;
      margin: 0;
    }}

    .bullets li {{
      line-height: 1.5;
      text-wrap: pretty;
    }}

    .compact-body {{
      font-size: 10pt;
      line-height: 1.5;
      margin: 0.05in 0 0;
      text-wrap: pretty;
    }}

    ul.sub-bullets {{
      list-style: circle;
      padding-left: 0.18in;
      margin-top: 0.04in;
      margin-bottom: 0;
    }}

    .sub-bullets li {{
      line-height: 1.26;
      text-wrap: pretty;
    }}

    .bullets li::marker {{
      font-size: 8pt;
      color: var(--ink);
    }}

    .sub-bullets li::marker {{
      font-size: 7pt;
      color: var(--ink);
    }}

    .bullets li + li {{
      margin-top: 0.03in;
    }}

    .sub-bullets li + li {{
      margin-top: 0.02in;
    }}

    .support-item + .support-item {{
      margin-top: 0.06in;
    }}

    .support-line {{
      font-size: 10pt;
      line-height: 1.4;
      text-wrap: pretty;
    }}

    .support-line strong {{
      font-size: 10pt;
      font-weight: 700;
      letter-spacing: 0;
    }}

    .support-note {{
      margin-top: 0.015in;
      color: var(--muted);
      font-size: 9pt;
      line-height: 1.3;
      text-wrap: pretty;
    }}

    em {{
      font-style: normal;
    }}

    a {{
      color: inherit;
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <main class="resume">
    <header class="masthead">
      <div class="name">{html.escape(data.name)}</div>
      <div class="tagline">{inline_html(data.tagline)}</div>
      {header_summary_html}
    </header>

    <div class="contact-bar">
      <ul class="contacts">
        {render_contacts(data.contacts)}
      </ul>
    </div>

    <section>
      {section_heading("Professional Experience")}
      {experience_html}
    </section>

    <section>
      {section_heading("Core Skills")}
      {skills_html}
    </section>

    <section>
      {section_heading("Education")}
      {education_html}
    </section>

    <section>
      {section_heading("Additional Experience & Languages")}
      {additional_html}
    </section>

  </main>
</body>
</html>
"""


def render_experience(entry: ExperienceEntry) -> str:
    meta_bits = [f'<span class="company">{inline_html(entry.company)}</span>']
    inline_context = entry.context if entry.context and len(entry.context) <= 80 else None
    block_context = entry.context if entry.context and len(entry.context) > 80 else None
    if inline_context:
        meta_bits.append(
            f'<span class="context">({inline_html(inline_context)})</span>'
        )
    if entry.dates:
        meta_bits.append(f'<span class="context">· {html.escape(entry.dates)}</span>')
    meta_html = " ".join(meta_bits)

    if not entry.bullets:
        body_html = f'<p class="compact-body">{inline_html(block_context)}</p>' if block_context else ""
        return f"""
      <article class="experience-item compact">
        <div class="experience-heading">
          <h3 class="role">{html.escape(entry.role)}</h3>
          <div class="meta-row">{meta_html}</div>
        </div>
        {body_html}
      </article>
    """

    return f"""
      <article class="experience-item">
        <div class="experience-heading">
          <h3 class="role">{html.escape(entry.role)}</h3>
          <div class="meta-row">{meta_html}</div>
        </div>
        {render_bullets(entry.bullets)}
      </article>
    """


def render_bullets(bullets: list[BulletItem], depth: int = 0) -> str:
    class_name = "bullets" if depth == 0 else "sub-bullets"
    items = []
    for bullet in bullets:
        children_html = render_bullets(bullet.children, depth + 1) if bullet.children else ""
        items.append(f"<li>{inline_html(bullet.text)}{children_html}</li>")
    return f'<ul class="{class_name}">\n' + "\n".join(items) + "\n</ul>"


def find_chrome(user_supplied: str | None) -> Path:
    if user_supplied:
        chrome_path = Path(user_supplied).expanduser()
        if chrome_path.exists():
            return chrome_path
        raise FileNotFoundError(f"Chrome binary not found: {chrome_path}")
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No supported Chrome binary found")


def export_pdf(html_path: Path, pdf_path: Path, chrome_path: Path) -> None:
    html_uri = html_path.resolve().as_uri()
    subprocess.run(
        [
            str(chrome_path),
            "--headless=new",
            "--disable-gpu",
            "--allow-file-access-from-files",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_uri,
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Export resume markdown to HTML and optional PDF.")
    parser.add_argument("input_md", help="Path to input markdown resume")
    parser.add_argument("output_html", help="Path to output HTML")
    parser.add_argument("--pdf", dest="output_pdf", help="Optional PDF output path")
    parser.add_argument("--chrome", dest="chrome_path", help="Optional path to Chrome binary")
    parser.add_argument("--theme", dest="theme_color", default="#8c1515", help="CSS accent color (hex)")
    args = parser.parse_args()

    input_md = Path(args.input_md).expanduser()
    output_html = Path(args.output_html).expanduser()
    output_html.parent.mkdir(parents=True, exist_ok=True)

    try:
        data = parse_resume(input_md)
        output_html.write_text(render_html(data, theme=args.theme_color), encoding="utf-8")
        if args.output_pdf:
            chrome_path = find_chrome(args.chrome_path)
            export_pdf(output_html, Path(args.output_pdf).expanduser(), chrome_path)
    except Exception as exc:  # pragma: no cover - CLI surface
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
