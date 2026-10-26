#!/usr/bin/env python3
"""Render an open-book exam pack written in a small Markdown subset to an A4 PDF.

Supported syntax (one construct per block, blocks separated by blank lines):

  # Title / ## Section / ### Subsection
  Plain paragraphs (consecutive lines are joined)
  - bullet item            1. numbered item
  > note / callout box
  | pipe | table |          (second line must be |---|---| separator)
  **bold**  ==highlight==  `code`
  <!-- widths: 20,15,65 -->   column width percentages for the next table
  <!-- pagebreak -->          force a new page
  <!-- appendix -->           new page; use before the calculation appendix

Example:
  python build_pdf.py work/pack.md -o outputs/course_open_book.pdf --body-size 7.2
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (
        BaseDocTemplate,
        CondPageBreak,
        Frame,
        PageBreak,
        PageTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )
except ImportError:  # pragma: no cover - dependency hint
    sys.exit("reportlab is required: pip install -r requirements.txt")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HIGHLIGHT = "#FFF2A8"
NOTE_BG = "#EEF4FB"
HEADER_BG = "#DCE6F2"
GRID = "#9AA7B5"

# (regular, bold) candidates; .ttc entries use subfont index 0.
FONT_CANDIDATES = [
    ("C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/msyhbd.ttc"),
    ("C:/Windows/Fonts/simhei.ttf", None),
    ("C:/Windows/Fonts/simsun.ttc", None),
    ("/System/Library/Fonts/STHeiti Medium.ttc", None),
    ("/Library/Fonts/Arial Unicode.ttf", None),
    ("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", None),
    ("/usr/share/fonts/truetype/arphic/uming.ttc", None),
]


def _try_ttf(name: str, path: str) -> bool:
    try:
        pdfmetrics.registerFont(TTFont(name, path, subfontIndex=0))
        return True
    except Exception:
        return False


def register_fonts(font_path: str | None, bold_path: str | None) -> tuple[str, str, str]:
    """Register a CJK-capable font and return (regular, bold, description)."""
    candidates = [(font_path, bold_path)] if font_path else FONT_CANDIDATES
    for regular, bold in candidates:
        if not regular or not os.path.exists(regular):
            if font_path:
                sys.exit(f"Font not found: {regular}")
            continue
        if not _try_ttf("PackFont", regular):
            if font_path:
                sys.exit(f"Font could not be loaded (CFF/OTF fonts are unsupported): {regular}")
            continue
        bold_name = "PackFont"
        if bold and os.path.exists(bold) and _try_ttf("PackFont-Bold", bold):
            bold_name = "PackFont-Bold"
        pdfmetrics.registerFontFamily(
            "PackFont", normal="PackFont", bold=bold_name, italic="PackFont", boldItalic=bold_name
        )
        return "PackFont", bold_name, regular
    # Built-in CID font: no embedding, but renders Chinese in every PDF viewer.
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    return "STSong-Light", "STSong-Light", "STSong-Light (built-in CID fallback)"


INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*(.+?)\*\*")
MARK = re.compile(r"==(.+?)==")


def inline(text: str, bold_font: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Courier has no CJK glyphs, so only switch fonts for ASCII code spans.
    text = INLINE_CODE.sub(
        lambda m: f'<font face="Courier">{m.group(1)}</font>' if m.group(1).isascii() else m.group(1), text
    )
    text = BOLD.sub(rf'<font face="{bold_font}">\1</font>', text)
    text = MARK.sub(rf'<font backColor="{HIGHLIGHT}">\1</font>', text)
    return text


def make_styles(font: str, bold: str, args: argparse.Namespace) -> dict[str, ParagraphStyle]:
    body = args.body_size
    lead = body * args.leading

    def style(name, size, font_name=font, **kw):
        return ParagraphStyle(
            name, fontName=font_name, fontSize=size, leading=size * args.leading,
            alignment=TA_LEFT, wordWrap="CJK", **kw
        )

    return {
        "h1": style("h1", args.title_size, bold, spaceBefore=2, spaceAfter=lead * 0.6),
        "h2": style("h2", args.h2_size, bold, spaceBefore=lead * 0.7, spaceAfter=lead * 0.3,
                    textColor=colors.HexColor("#1F3A5F")),
        "h3": style("h3", max(body + 1, args.h2_size - 1.5), bold, spaceBefore=lead * 0.4,
                    spaceAfter=lead * 0.2),
        "body": style("body", body, spaceAfter=lead * 0.3),
        "cell": style("cell", body),
        "cell_head": style("cell_head", body, bold),
        "bullet": style("bullet", body, leftIndent=body * 1.6, bulletIndent=body * 0.3,
                        bulletFontName=font, bulletFontSize=body, spaceAfter=lead * 0.1),
        "note": style("note", body, backColor=colors.HexColor(NOTE_BG), borderPadding=(3, 4, 3, 4),
                      spaceBefore=lead * 0.3, spaceAfter=lead * 0.6),
    }


TABLE_SEP = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
WIDTHS = re.compile(r"<!--\s*widths:\s*([\d.,\s]+)-->", re.I)
DIRECTIVE = re.compile(r"<!--\s*(pagebreak|appendix)\s*-->", re.I)


def split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    cells = re.split(r"(?<!\\)\|", line)
    return [c.strip().replace("\\|", "|") for c in cells]


def auto_widths(rows: list[list[str]], total: float) -> list[float]:
    """Share width by content length, but never let a column get too narrow."""
    ncol = max(len(r) for r in rows)
    weights = []
    for c in range(ncol):
        lengths = sorted(len(r[c]) if c < len(r) else 0 for r in rows)
        typical = lengths[int(len(lengths) * 0.8)] if lengths else 1
        weights.append(max(typical, 4) ** 0.85)
    floor = total * min(0.12, 0.6 / ncol)
    raw = [total * w / sum(weights) for w in weights]
    short = sum(floor - w for w in raw if w < floor)
    big = [w for w in raw if w >= floor]
    scale = (sum(big) - short) / sum(big) if big else 1
    return [floor if w < floor else w * scale for w in raw]


def build_table(rows, widths_pct, avail, styles, font, bold):
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    if widths_pct and len(widths_pct) == ncol:
        widths = [avail * p / sum(widths_pct) for p in widths_pct]
    else:
        widths = auto_widths(rows, avail)
    data = []
    marks = []
    for ri, row in enumerate(rows):
        out = []
        for ci, cell in enumerate(row):
            st = styles["cell_head"] if ri == 0 else styles["cell"]
            if ri > 0 and cell.startswith("==") and cell.endswith("==") and len(cell) > 4:
                marks.append((ci, ri))
                cell = cell[2:-2]
            out.append(Paragraph(inline(cell, bold), st))
        data.append(out)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    cmds = [
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor(GRID)),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(HEADER_BG)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2.5),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
    ]
    cmds += [("BACKGROUND", pos, pos, colors.HexColor(HIGHLIGHT)) for pos in marks]
    t.setStyle(TableStyle(cmds))
    return t


def parse(md: str, styles, avail, font, bold):
    story = []
    lines = md.splitlines()
    i = 0
    pending_widths = None
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        m = DIRECTIVE.fullmatch(stripped)
        if m:
            story.append(PageBreak())
            i += 1
            continue
        m = WIDTHS.fullmatch(stripped)
        if m:
            pending_widths = [float(x) for x in m.group(1).split(",") if x.strip()]
            i += 1
            continue
        if stripped.startswith("<!--"):
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            i += 1
            continue
        heading = re.match(r"^(#{1,3})\s+(.*)$", stripped)
        if heading:
            level = len(heading.group(1))
            if level <= 2:
                story.append(CondPageBreak(styles["h2"].fontSize * 6))
            story.append(Paragraph(inline(heading.group(2), bold), styles[f"h{level}"]))
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1].strip()):
            rows = [split_row(stripped)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            story.append(build_table(rows, pending_widths, avail, styles, font, bold))
            story.append(Spacer(1, styles["body"].leading * 0.5))
            pending_widths = None
            continue
        if stripped.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            story.append(Paragraph("<br/>".join(inline(b, bold) for b in buf), styles["note"]))
            continue
        item = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if item:
            while i < len(lines):
                item = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", lines[i])
                if not item:
                    break
                depth = len(item.group(1).expandtabs(4)) // 2
                marker = item.group(2)
                bullet = "•" if marker in "-*+" else marker
                text = item.group(3)
                i += 1
                while (i < len(lines) and lines[i].strip() and lines[i].startswith("  ")
                       and not re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i])):
                    text += " " + lines[i].strip()
                    i += 1
                st = ParagraphStyle(f"b{depth}", parent=styles["bullet"],
                                    leftIndent=styles["bullet"].leftIndent * (1 + depth),
                                    bulletIndent=styles["bullet"].bulletIndent + styles["bullet"].leftIndent * depth)
                story.append(Paragraph(inline(text, bold), st, bulletText=bullet))
            story.append(Spacer(1, styles["body"].leading * 0.3))
            continue
        buf = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
            r"^\s*(#{1,3}\s|[-*+]\s|\d+[.)]\s|>|\||<!--)", lines[i]
        ):
            buf.append(lines[i].strip())
            i += 1
        sep = "" if all(ord(b[-1]) > 0x2E80 for b in buf[:-1] if b) else " "
        story.append(Paragraph(inline(sep.join(buf), bold), styles["body"]))
    return story


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="Markdown file (UTF-8)")
    ap.add_argument("-o", "--output", help="output PDF (default: outputs/<source stem>.pdf)")
    ap.add_argument("--body-size", type=float, default=7.2, help="body/table font size in pt (default 7.2)")
    ap.add_argument("--title-size", type=float, default=15)
    ap.add_argument("--h2-size", type=float, default=10.5)
    ap.add_argument("--leading", type=float, default=1.25, help="line height multiplier (default 1.25)")
    ap.add_argument("--margin-mm", type=float, default=10)
    ap.add_argument("--columns", type=int, choices=(1, 2, 3), default=1)
    ap.add_argument("--landscape", action="store_true")
    ap.add_argument("--no-page-numbers", action="store_true", help="omit footer page numbers")
    ap.add_argument("--font", help="path to a TrueType font (.ttf/.ttc) with CJK glyphs")
    ap.add_argument("--bold-font", help="optional bold variant of --font")
    ap.add_argument("--title", help="PDF metadata title (default: first # heading)")
    args = ap.parse_args()

    src = Path(args.source)
    md = src.read_text(encoding="utf-8-sig")
    out = Path(args.output) if args.output else Path("outputs") / f"{src.stem}.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)

    font, bold, font_desc = register_fonts(args.font, args.bold_font)
    styles = make_styles(font, bold, args)

    pagesize = landscape(A4) if args.landscape else A4
    margin = args.margin_mm * mm
    gap = 5 * mm
    width = pagesize[0] - 2 * margin
    col_w = (width - gap * (args.columns - 1)) / args.columns
    footer = 0 if args.no_page_numbers else 4 * mm
    height = pagesize[1] - 2 * margin - footer
    frames = [
        Frame(margin + c * (col_w + gap), margin + footer, col_w, height,
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id=f"c{c}")
        for c in range(args.columns)
    ]

    def on_page(canvas, doc):
        if args.no_page_numbers:
            return
        canvas.setFont(font, 7)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawCentredString(pagesize[0] / 2, margin * 0.6, str(doc.page))

    title_match = re.search(r"^#\s+(.+)$", md, re.M)
    title = args.title or (title_match.group(1).strip() if title_match else src.stem)
    doc = BaseDocTemplate(str(out), pagesize=pagesize, leftMargin=margin, rightMargin=margin,
                          topMargin=margin, bottomMargin=margin, title=title, author="open-book-exam-pack")
    doc.addPageTemplates([PageTemplate(id="main", frames=frames, onPage=on_page)])
    try:
        doc.build(parse(md, styles, col_w, font, bold))
    except PermissionError:
        sys.exit(f"Cannot write {out} - it is probably open in a PDF viewer. Save under a new name with -o.")

    print(f"Wrote {out} ({doc.page} pages, font: {font_desc}, body {args.body_size}pt)")
    if args.body_size < 6.3:
        print("Warning: body text below 6.3pt is hard to read when printed.")


if __name__ == "__main__":
    main()
