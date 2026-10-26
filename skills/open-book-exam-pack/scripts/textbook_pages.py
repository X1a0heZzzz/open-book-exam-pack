#!/usr/bin/env python3
"""Textbook page helpers: find the TOC, measure the printed-page offset, verify pages.

  offset = PDF page - printed page      (so PDF page = printed page + offset)

If printed page 1 is PDF page N, offset = N - 1. Offsets can change inside a book
(colour plates, unnumbered chapter openers), so `offset` reports every segment.

Subcommands:
  toc     PDF bookmarks plus candidate TOC pages and "title ..... 123" entries
  offset  read printed page numbers from headers/footers and report the offset(s)
  check   open the PDF page for given printed page(s) and show what is there

Examples:
  python textbook_pages.py toc 教材.pdf --scan 25
  python textbook_pages.py offset 教材.pdf
  python textbook_pages.py check 教材.pdf --offset 12 --printed 37 105 --render
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import pymupdf
except ImportError:  # pragma: no cover - dependency hint
    sys.exit("PyMuPDF is required: pip install -r requirements.txt")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOC_WORDS = ("目录", "目  录", "目 录", "Contents", "CONTENTS", "Table of Contents")
TOC_ENTRY = re.compile(r"^(?P<title>.{2,80}?)[\s.·…．。\-_]{2,}(?P<page>\d{1,4})\s*$")
PAGE_NUM = re.compile(r"^[-–—\s]*(\d{1,4})[-–—\s]*$|^第\s*(\d{1,4})\s*页$")


def cmd_toc(doc, args) -> None:
    bookmarks = doc.get_toc()
    if bookmarks:
        print(f"Bookmarks ({len(bookmarks)}), PDF page numbers are 1-based:")
        for level, title, page in bookmarks[: args.limit]:
            print(f"{'  ' * (level - 1)}- {title}  -> PDF p{page}")
        if len(bookmarks) > args.limit:
            print(f"  ... {len(bookmarks) - args.limit} more")
        print("Bookmarks point to PDF pages, not printed pages; still confirm the offset.\n")
    else:
        print("No bookmarks.\n")

    found = False
    for i in range(min(doc.page_count, args.scan)):
        text = doc[i].get_text()
        entries = [m for m in (TOC_ENTRY.match(l.strip()) for l in text.splitlines()) if m]
        if any(w in text for w in TOC_WORDS) or len(entries) >= 5:
            found = True
            print(f"--- candidate TOC page: PDF p{i + 1} ({len(entries)} entries) ---")
            for m in entries:
                print(f"{m.group('title').strip()}  ->  printed p{m.group('page')}")
    if not found:
        print(f"No TOC text found in the first {args.scan} pages. If the book is scanned, run\n"
              f"  extract_text.py <pdf> --pages 1-{args.scan} --ocr\n"
              "and read the TOC from the OCR output or the PNG renders.")


def printed_number(page) -> int | None:
    """Standalone number in the top or bottom 9% of the page (header/footer)."""
    h = page.rect.height
    for x0, y0, x1, y1, text, *_ in page.get_text("blocks"):
        if y1 > h * 0.09 and y0 < h * 0.91:
            continue
        for line in text.splitlines():
            m = PAGE_NUM.match(line.strip())
            if m:
                return int(m.group(1) or m.group(2))
    return None


def cmd_offset(doc, args) -> None:
    samples = []
    for i in range(args.start - 1, doc.page_count):
        num = printed_number(doc[i])
        if num is not None and 0 < num <= doc.page_count + 50:
            samples.append((i + 1, num, i + 1 - num))
    if not samples:
        print("No printed page numbers detected (scanned book or unusual layout).\n"
              "Use `check --render` on a few pages and read the numbers from the images,\n"
              "or OCR a handful of body pages with extract_text.py --ocr.")
        return

    counts = Counter(off for *_, off in samples)
    best, hits = counts.most_common(1)[0]
    print(f"Detected printed numbers on {len(samples)} of {doc.page_count} pages.")
    print(f"Most common offset: {best} ({hits} pages)  =>  PDF page = printed page + {best}")

    # Collapse into runs of the same offset, ignoring isolated outliers.
    segments, cur = [], None
    for pdf, num, off in samples:
        if counts[off] < max(3, hits * 0.05):
            continue
        if cur and cur[2] == off:
            cur[1] = pdf
        else:
            cur = [pdf, pdf, off]
            segments.append(cur)
    if len(segments) > 1:
        print("\nOffset changes inside the book:")
        for a, b, off in segments:
            print(f"  PDF p{a}-p{b}: offset {off}  (printed p{a - off}-p{b - off})")
    print("\nVerify 2-3 pages with `check` before writing PDF page numbers into the pack.")


def cmd_check(doc, args) -> None:
    out = Path(args.out)
    for printed in args.printed:
        pdf = printed + args.offset
        if not 1 <= pdf <= doc.page_count:
            print(f"printed p{printed} -> PDF p{pdf}: outside the document (1-{doc.page_count})")
            continue
        page = doc[pdf - 1]
        detected = printed_number(page)
        status = ("OK" if detected == printed else
                  "number not detected" if detected is None else f"MISMATCH (page shows {detected})")
        snippet = " ".join(page.get_text().split())[: args.chars]
        print(f"printed p{printed} -> PDF p{pdf}: {status}\n  {snippet}\n")
        if args.render:
            out.mkdir(parents=True, exist_ok=True)
            png = out / f"printed_p{printed}_pdf_p{pdf}.png"
            page.get_pixmap(dpi=110).save(png)
            print(f"  render: {png}\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("toc", help="list bookmarks and candidate TOC entries")
    p.add_argument("pdf")
    p.add_argument("--scan", type=int, default=25, help="leading pages to scan (default 25)")
    p.add_argument("--limit", type=int, default=200, help="max bookmarks to print")

    p = sub.add_parser("offset", help="estimate printed-page offset(s)")
    p.add_argument("pdf")
    p.add_argument("--start", type=int, default=1, help="first PDF page to inspect")

    p = sub.add_parser("check", help="verify printed pages against the PDF")
    p.add_argument("pdf")
    p.add_argument("--offset", type=int, required=True, help="PDF page - printed page")
    p.add_argument("--printed", type=int, nargs="+", required=True)
    p.add_argument("--chars", type=int, default=240, help="snippet length")
    p.add_argument("--render", action="store_true", help="save PNGs for visual confirmation")
    p.add_argument("--out", default="work/page_check")

    args = ap.parse_args()
    doc = pymupdf.open(args.pdf)
    {"toc": cmd_toc, "offset": cmd_offset, "check": cmd_check}[args.cmd](doc, args)


if __name__ == "__main__":
    main()
