#!/usr/bin/env python3
"""Print UTF-8 text files safely, regardless of console code page.

PowerShell/cmd often shows Chinese text as mojibake even when the file is fine.
This prints through a UTF-8 stdout and can grep with context.

Examples:
  python peek_text.py work/text/教材/all.txt --head 80
  python peek_text.py work/text/*/all.txt --grep "梯度消失|Transformer" --context 2
"""

from __future__ import annotations

import argparse
import glob
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="files or glob patterns")
    ap.add_argument("--head", type=int, help="print only the first N lines of each file")
    ap.add_argument("--grep", help="regular expression; print matching lines with line numbers")
    ap.add_argument("--context", type=int, default=0, help="lines of context around matches")
    ap.add_argument("--encoding", default="utf-8-sig", help="source encoding (try gb18030 for old files)")
    args = ap.parse_args()

    paths = [p for pattern in args.files for p in (glob.glob(pattern) or [pattern])]
    pattern = re.compile(args.grep) if args.grep else None
    for path in paths:
        try:
            with open(path, encoding=args.encoding, errors="replace") as fh:
                lines = fh.read().splitlines()
        except OSError as exc:
            print(f"!! {path}: {exc}")
            continue
        if len(paths) > 1:
            print(f"==> {path} <==")
        if pattern:
            shown = -1
            for i, line in enumerate(lines):
                if pattern.search(line):
                    lo, hi = max(0, i - args.context, shown + 1), min(len(lines), i + args.context + 1)
                    if lo > shown + 1 and shown >= 0:
                        print("--")
                    for j in range(lo, hi):
                        print(f"{j + 1}:{lines[j]}")
                    shown = hi - 1
        else:
            for line in lines[: args.head] if args.head else lines:
                print(line)


if __name__ == "__main__":
    main()
