#!/usr/bin/env python3
"""Extract per-page text from a PDF into work/, with OCR fallback for scanned pages.

Output layout (UTF-8, safe for Chinese paths):
  <out>/<stem>/p0001.txt ...   one file per page, first line is "=== PDF page N ==="
  <out>/<stem>/all.txt         all pages concatenated
  <out>/<stem>/png/p0001.png   page renders (only with --render, or when OCR runs)

OCR engines are optional and tried in order: rapidocr_onnxruntime, then pytesseract
(needs the Tesseract binary with chi_sim data). Pages whose text layer is shorter
than --min-chars are OCR'd when --ocr is given.

Examples:
  python extract_text.py "D:/课程/教材.pdf" --pages 1-20          # TOC area only
  python extract_text.py paper.pdf --ocr --dpi 200                 # scanned past paper
  python extract_text.py slides.pdf --render --pages 5,9-11        # screenshots to check formulas
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:  # pragma: no cover - dependency hint
    sys.exit("PyMuPDF is required: pip install -r requirements.txt")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def parse_pages(spec: str | None, n: int) -> list[int]:
    """'1-3,7' -> [0,1,2,6] (1-based input, 0-based output)."""
    if not spec:
        return list(range(n))
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            lo, hi = int(a or 1), int(b or n)
            pages.update(range(lo - 1, min(hi, n)))
        else:
            pages.add(int(part) - 1)
    return sorted(p for p in pages if 0 <= p < n)


class Ocr:
    def __init__(self, lang: str):
        self.name = None
        self.lang = lang
        try:
            from rapidocr_onnxruntime import RapidOCR

            self.engine = RapidOCR()
            self.name = "rapidocr"
            return
        except Exception:
            pass
        try:
            import pytesseract

            pytesseract.get_tesseract_version()
            self.engine = pytesseract
            self.name = "tesseract"
        except Exception:
            self.engine = None

    def __call__(self, png: Path) -> str:
        if self.name == "rapidocr":
            result, _ = self.engine(str(png))
            return "\n".join(item[1] for item in result or [])
        if self.name == "tesseract":
            from PIL import Image

            return self.engine.image_to_string(Image.open(png), lang=self.lang)
        return ""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--out", default="work/text", help="output root (default work/text)")
    ap.add_argument("--pages", help="1-based page list, e.g. 1-20,35")
    ap.add_argument("--ocr", action="store_true", help="OCR pages with too little text")
    ap.add_argument("--min-chars", type=int, default=40, help="text-layer threshold for OCR (default 40)")
    ap.add_argument("--render", action="store_true", help="save PNG renders of the selected pages")
    ap.add_argument("--dpi", type=int, default=170)
    ap.add_argument("--lang", default="chi_sim+eng", help="tesseract languages (default chi_sim+eng)")
    args = ap.parse_args()

    src = Path(args.pdf)
    doc = pymupdf.open(src)
    out = Path(args.out) / src.stem
    out.mkdir(parents=True, exist_ok=True)
    pages = parse_pages(args.pages, doc.page_count)

    ocr = Ocr(args.lang) if args.ocr else None
    if ocr and not ocr.name:
        print("Warning: no OCR engine found. Install one of:\n"
              "  pip install rapidocr_onnxruntime\n"
              "  pip install pytesseract pillow  (plus the Tesseract binary with chi_sim)")

    combined, ocr_pages, empty_pages = [], [], []
    for i in pages:
        page = doc[i]
        text = page.get_text().strip()
        png = out / "png" / f"p{i + 1:04d}.png"
        need_ocr = ocr and ocr.name and len(text) < args.min_chars
        if args.render or need_ocr:
            png.parent.mkdir(exist_ok=True)
            page.get_pixmap(dpi=args.dpi).save(png)
        if need_ocr:
            text = ocr(png).strip()
            ocr_pages.append(i + 1)
        if len(text) < args.min_chars:
            empty_pages.append(i + 1)
        block = f"=== PDF page {i + 1} ===\n{text}\n"
        (out / f"p{i + 1:04d}.txt").write_text(block, encoding="utf-8")
        combined.append(block)

    (out / "all.txt").write_text("\n".join(combined), encoding="utf-8")
    print(f"{src.name}: {len(pages)} pages -> {out}")
    if ocr_pages:
        print(f"OCR ({ocr.name}) used on {len(ocr_pages)} pages: {compact(ocr_pages)}")
    if empty_pages:
        hint = "" if args.ocr else " (rerun with --ocr if these are scanned)"
        print(f"Little or no text on {len(empty_pages)} pages: {compact(empty_pages)}{hint}")


def compact(nums: list[int]) -> str:
    """[1,2,3,7] -> '1-3,7'"""
    parts, start = [], None
    for a, b in zip(nums, nums[1:] + [None]):
        start = a if start is None else start
        if b != a + 1:
            parts.append(f"{start}-{a}" if start != a else str(a))
            start = None
    return ",".join(parts)


if __name__ == "__main__":
    main()
