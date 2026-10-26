#!/usr/bin/env python3
"""Inventory course materials before building an exam pack.

For every PDF found under the given files/folders, report page count, size,
extracted text volume, whether it looks scanned (needs OCR), whether it has
bookmarks, and a guessed role (courseware / past paper / textbook).
Non-PDF files (PPT, DOCX, images) are listed so nothing is silently skipped.

Example:
  python probe_pdfs.py "D:/课程/课件" "D:/课程/试卷" "D:/课程/教材.pdf" --json work/inventory.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:  # pragma: no cover - dependency hint
    sys.exit("PyMuPDF is required: pip install -r requirements.txt")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OTHER_TYPES = {".ppt", ".pptx", ".doc", ".docx", ".png", ".jpg", ".jpeg", ".txt", ".md"}
ROLE_HINTS = {
    "past-paper": ("试卷", "真题", "期末", "期中", "考卷", "exam", "paper", "quiz", "test", "答案"),
    "textbook": ("教材", "课本", "教程", "textbook", "book", "出版社"),
    "courseware": ("课件", "讲义", "章", "lecture", "slides", "chapter", "week", "ppt"),
}


def guess_role(path: Path, first_text: str, pages: int) -> str:
    name = path.stem.lower()
    for role, words in ROLE_HINTS.items():
        if any(w in name for w in words):
            return role
    head = first_text[:600]
    if any(w in head for w in ("目录", "Contents", "CONTENTS", "ISBN", "出版社")) and pages > 80:
        return "textbook"
    if sum(w in head for w in ("试卷", "得分", "评卷人", "学号", "姓名", "考试时间")) >= 2:
        return "past-paper"
    return "textbook" if pages > 150 else "courseware"


def probe(path: Path, sample: int) -> dict:
    info = {"path": str(path), "size_mb": round(path.stat().st_size / 2**20, 2)}
    try:
        doc = pymupdf.open(path)
    except Exception as exc:
        info["error"] = f"cannot open: {exc}"
        return info
    if doc.needs_pass:
        info["error"] = "encrypted (password required)"
        return info
    n = doc.page_count
    idx = sorted(set(range(min(n, sample))) | set(range(max(0, n - 3), n)))
    chars = [len(doc[i].get_text().strip()) for i in idx]
    per_page = sum(chars) / max(len(chars), 1)
    empty = sum(1 for c in chars if c < 30)
    first_text = "".join(doc[i].get_text() for i in range(min(n, 3)))
    info.update(
        pages=n,
        chars_per_page=round(per_page),
        sampled_pages=len(idx),
        likely_scanned=per_page < 50 or empty / max(len(idx), 1) > 0.6,
        has_bookmarks=bool(doc.get_toc()),
        role_guess=guess_role(path, first_text, n),
    )
    return info


def collect(inputs: list[str]) -> tuple[list[Path], list[Path], list[str]]:
    pdfs, others, missing = [], [], []
    for raw in inputs:
        p = Path(raw)
        if not p.exists():
            missing.append(raw)
            continue
        files = [p] if p.is_file() else sorted(q for q in p.rglob("*") if q.is_file())
        for f in files:
            ext = f.suffix.lower()
            if ext == ".pdf":
                pdfs.append(f)
            elif ext in OTHER_TYPES:
                others.append(f)
    return pdfs, others, missing


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="files or folders")
    ap.add_argument("--sample", type=int, default=12, help="leading pages sampled per PDF (default 12)")
    ap.add_argument("--json", help="also write the inventory to this JSON file")
    args = ap.parse_args()

    pdfs, others, missing = collect(args.inputs)
    rows = [probe(p, args.sample) for p in pdfs]

    print("| File | Pages | MB | Chars/page | Scanned? | Bookmarks | Role guess |")
    print("| --- | ---: | ---: | ---: | --- | --- | --- |")
    for r in rows:
        name = os.path.basename(r["path"])
        if "error" in r:
            print(f"| {name} | - | {r['size_mb']} | - | - | - | ERROR: {r['error']} |")
            continue
        print(f"| {name} | {r['pages']} | {r['size_mb']} | {r['chars_per_page']} | "
              f"{'YES -> OCR' if r['likely_scanned'] else 'no'} | {'yes' if r['has_bookmarks'] else 'no'} | "
              f"{r['role_guess']} |")
    if others:
        print("\nNon-PDF files (convert or read separately):")
        for f in others:
            print(f" - {f}")
    if missing:
        print("\nMissing paths:")
        for m in missing:
            print(f" - {m}")
    if not pdfs:
        print("\nNo PDF files found.")

    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(
            json.dumps({"pdfs": rows, "other_files": [str(f) for f in others], "missing": missing},
                       ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\nInventory saved to {args.json}")


if __name__ == "__main__":
    main()
