#!/usr/bin/env python3
"""Minimal markdown-to-PDF exporter for resumes.

Guardrail: prevents duplicate divider lines when both markdown '---'
and section-heading divider logic are present.
"""

from __future__ import annotations

import argparse
import textwrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def export(md_path: str, pdf_path: str) -> None:
    with open(md_path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]

    c = canvas.Canvas(pdf_path, pagesize=LETTER)
    width, height = LETTER
    margin_x = 0.7 * inch
    top = height - 0.7 * inch
    bottom = 0.65 * inch
    line_gap = 14

    x = margin_x
    y = top
    just_drew_rule = False

    def new_page() -> None:
        nonlocal y
        c.showPage()
        y = top

    def ensure_space(lines_needed: int = 1) -> None:
        nonlocal y
        if y - lines_needed * line_gap < bottom:
            new_page()

    def write_line(text: str, font: str = "Helvetica", size: float = 10.5, indent: int = 0) -> None:
        nonlocal y
        ensure_space(1)
        c.setFont(font, size)
        c.drawString(x + indent, y, text)
        y -= line_gap

    def write_wrapped(text: str, font: str = "Helvetica", size: float = 10.5, indent: int = 0, bullet: bool = False) -> None:
        max_chars = 105 if indent == 0 else 95
        wrapped = textwrap.wrap(text, width=max_chars)
        if not wrapped:
            return
        if bullet:
            wrapped[0] = "• " + wrapped[0]
        for i, seg in enumerate(wrapped):
            if bullet and i > 0:
                write_line(seg, font=font, size=size, indent=14)
            else:
                write_line(seg, font=font, size=size, indent=indent)

    def draw_divider(extra_before: int = 3, extra_after: int = 8) -> None:
        nonlocal y
        ensure_space(2)
        y -= extra_before
        c.setStrokeColor(colors.HexColor("#777777"))
        c.setLineWidth(0.6)
        c.line(x, y, width - margin_x, y)
        y -= extra_after

    for raw in lines:
        line = raw.strip()

        if line == "---":
            draw_divider(2, 8)
            just_drew_rule = True
            continue

        if line.startswith("# "):
            write_wrapped(line[2:].strip(), font="Helvetica-Bold", size=20)
            y -= 2
            just_drew_rule = False
            continue

        if line.startswith("## "):
            # Prevent double lines: if markdown already drew one via '---', skip extra divider.
            if not just_drew_rule:
                draw_divider(3, 8)
            write_wrapped(line[3:].strip(), font="Helvetica-Bold", size=13)
            y -= 1
            just_drew_rule = False
            continue

        if line.startswith("### "):
            write_wrapped(line[4:].strip(), font="Helvetica-Bold", size=11.5)
            just_drew_rule = False
            continue

        if not line:
            y -= 6
            continue

        if line.startswith("- "):
            write_wrapped(line[2:].strip(), bullet=True)
            just_drew_rule = False
            continue

        cleaned = line.replace("**", "").replace("*", "")
        write_wrapped(cleaned)
        just_drew_rule = False

    c.save()


def main() -> None:
    parser = argparse.ArgumentParser(description="Export resume markdown to PDF with divider de-duplication.")
    parser.add_argument("input_md", help="Path to input markdown resume")
    parser.add_argument("output_pdf", help="Path to output PDF")
    args = parser.parse_args()
    export(args.input_md, args.output_pdf)


if __name__ == "__main__":
    main()
