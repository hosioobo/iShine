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

    def stash(match: re.Match[str]) -> str:
        token = f"__URL_{len(placeholders)}__"
        url = match.group(0)
        href = url if "://" in url else f"https://{url}"
        placeholders[token] = (
            f'<a href="{html.escape(href, quote=True)}">{html.escape(url)}</a>'
        )
        return token

    url_pattern = re.compile(r"(https?://[^\s]+|linkedin\.com/[^\s]+)")
    text = url_pattern.sub(stash, text)
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
    core_skills = [
        " ".join(chunk.strip() for chunk in paragraph if chunk.strip())
        for paragraph in split_blocks(sections.get("CORE SKILLS", []))
        if any(chunk.strip() for chunk in paragraph)
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
            current = ExperienceEntry(
                role=stripped[4:].strip(),
                company="",
                context="",
                dates="",
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
                f"{html.escape(item)}</a>"
            )
        rendered.append(f'<li class="contact-item">{safe}</li>')
    return "\n".join(rendered)


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


def render_html(data: ResumeData) -> str:
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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --ink: #0a0a0a;
      --muted: #4a4a4a;
      --rule: #bdbdbd;
      --paper: #ffffff;
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
      font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 10pt;
      line-height: 1.4;
      text-rendering: geometricPrecision;
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
      font-size: 22pt;
      font-weight: 600;
      letter-spacing: -0.03em;
      line-height: 1.02;
      text-transform: uppercase;
      margin-bottom: 0.06in;
    }}

    .tagline {{
      font-size: 10pt;
      font-weight: 300;
      letter-spacing: 0.01em;
      line-height: 1.25;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 0.14in;
    }}

    .header-summary {{
      font-size: 10pt;
      line-height: 1.42;
      text-wrap: pretty;
    }}

    .contact-bar {{
      margin-top: 0.12in;
      margin-bottom: 0.22in;
      padding: 0.1in 0;
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
    }}

    section {{
      margin-top: 0.28in;
    }}

    section:first-of-type {{
      margin-top: 0;
    }}

    .section-header {{
      display: block;
      border-top: 1px solid var(--rule);
      padding-top: 0.18in;
      margin-bottom: 0.1in;
      break-after: avoid;
    }}

    section:first-of-type .section-header {{
      border-top: none;
      padding-top: 0;
    }}

    .section-label {{
      display: block;
      font-size: 12pt;
      font-weight: 500;
      letter-spacing: 0.01em;
      text-transform: uppercase;
      line-height: 1.2;
      color: var(--muted);
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
      break-inside: avoid;
    }}

    .experience-item + .experience-item {{
      margin-top: 0.18in;
    }}

    .role {{
      display: block;
      font-size: 11pt;
      font-weight: 700;
      letter-spacing: 0;
      line-height: 1.2;
      margin-bottom: 0.02in;
    }}

    .meta-row {{
      font-size: 9pt;
      color: var(--muted);
      margin-bottom: 0.04in;
      line-height: 1.3;
      text-wrap: pretty;
    }}

    .company {{
      font-style: italic;
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
      line-height: 1.28;
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
      font-style: italic;
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
      {section_heading("Core Skills")}
      {skills_html}
    </section>

    <section>
      {section_heading("Professional Experience")}
      {experience_html}
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
    if entry.context:
        meta_bits.append(
            f'<span class="context">({inline_html(entry.context)})</span>'
        )
    if entry.dates:
        meta_bits.append(f'<span class="context">· {html.escape(entry.dates)}</span>')
    meta_html = " ".join(meta_bits)
    return f"""
      <article class="experience-item">
        <h3 class="role">{html.escape(entry.role)}</h3>
        <div class="meta-row">{meta_html}</div>
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
    args = parser.parse_args()

    input_md = Path(args.input_md).expanduser()
    output_html = Path(args.output_html).expanduser()
    output_html.parent.mkdir(parents=True, exist_ok=True)

    try:
        data = parse_resume(input_md)
        output_html.write_text(render_html(data), encoding="utf-8")
        if args.output_pdf:
            chrome_path = find_chrome(args.chrome_path)
            export_pdf(output_html, Path(args.output_pdf).expanduser(), chrome_path)
    except Exception as exc:  # pragma: no cover - CLI surface
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
