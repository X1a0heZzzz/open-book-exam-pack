# Open Book Exam Pack Skill

[中文](README.md) | [English](README.en.md)

[![validate](https://github.com/X1a0heZzzz/open-book-exam-pack/actions/workflows/validate.yml/badge.svg)](https://github.com/X1a0heZzzz/open-book-exam-pack/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)
![Codex Skill](https://img.shields.io/badge/Codex-Skill-blue)
![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-d97757)
![Exam Prep](https://img.shields.io/badge/Exam-Prep-orange)

An agent skill (Codex and Claude Code) for turning course slides, past papers, textbooks, scanned PDFs, and formatting requirements into exam-ready open-book review PDFs.

This is not a generic summarization skill. It is designed for material you can actually use under exam pressure: chapter lookup, answer templates, subjective-answer structures, calculation walkthroughs, verified textbook page indexes, and print-friendly PDF layout. The skill ships Python helpers for material inventory, OCR of scanned PDFs, textbook page-offset verification, and CJK-ready PDF generation.

## Quick Start

1. Install the skill (see [Installation](#installation)).
2. Paste this into Codex or Claude Code and replace the placeholders:

```text
Please use the open-book-exam-pack skill to create an open-book exam review PDF.

Course: <course name and exam scope>
Courseware path: <folder containing lecture PDFs/PPTs>
Past-paper path: <folder containing past exam PDFs, optional>
Textbook path: <textbook PDF, optional>
Exam rules: <printed textbook only / printed notes allowed / electronic PDF allowed>

Requirements:
- Build a chapter-by-chapter lookup.
- Extract high-frequency short-answer and essay-answer templates.
- If the textbook has a table of contents, add a verified textbook page index.
- Put detailed calculation walkthroughs at the end.
- Keep the layout compact but readable, and save the final PDF to outputs/.
```

## When To Use It

- You need one open-book exam pack from slides, textbooks, and past papers.
- You want fast chapter-by-chapter lookup during the exam.
- You want high-frequency question patterns mined from past papers.
- You need reusable short-answer, essay, and calculation templates.
- You need a textbook page index, especially when only printed textbooks are allowed.
- You want a compact but readable PDF for printing or electronic open-book use.

## What The Skill Does

- Classifies inputs as courseware, past papers, textbooks, or user instructions.
- Handles scanned PDFs, OCR noise, and non-ASCII (e.g. Chinese) file paths.
- Verifies textbook page numbers from the table of contents or body pages, and measures the printed-page ↔ PDF-page offset instead of guessing.
- Adjusts layout density, font size, columns, whitespace, and page count based on user preference.
- Places calculation walkthroughs in a final standalone appendix.
- Removes PDF page numbers when the exam only allows printed textbooks.
- Saves final PDFs to `outputs/` and keeps text dumps, OCR, previews, and the Markdown source in `work/`.

## Workflow Modes

| Mode | Best for | Main output |
| --- | --- | --- |
| `pack` | Full pack from courseware, past papers, and textbooks | A structured review PDF |
| `page-index` | Textbook page lookup only | Topic-to-page lookup table |
| `past-paper` | Past-paper pattern mining | Frequent themes, question types, answer templates |
| `calculation` | Calculation-heavy exams | Step-by-step solution templates and pitfalls |
| `polish` | Existing material with poor layout | A cleaner, tighter, printable version |

You do not have to specify a mode. The agent infers it from your materials and request.

## Bundled Scripts

In `skills/open-book-exam-pack/scripts/`. The agent calls them as part of the workflow; you can also run them yourself:

| Script | Purpose | Example |
| --- | --- | --- |
| `probe_pdfs.py` | Inventory: pages, text volume, scanned or not, role guess | `python probe_pdfs.py slides/ papers/ book.pdf` |
| `extract_text.py` | Per-page text, OCR fallback, page renders | `python extract_text.py paper.pdf --ocr` |
| `textbook_pages.py` | Find the TOC, measure page offset, check pages | `python textbook_pages.py offset book.pdf` |
| `peek_text.py` | Print/grep UTF-8 text regardless of console encoding | `python peek_text.py work/text/*/all.txt --grep softmax` |
| `build_pdf.py` | Markdown → A4 PDF with tables, highlights, columns | `python build_pdf.py work/pack.md --columns 2` |

Requirements: Python 3.9+, `pymupdf`, `reportlab`; optionally `rapidocr_onnxruntime` for OCR. Source syntax: [pack-format.md](skills/open-book-exam-pack/references/pack-format.md). Sample: [examples/sample-pack.md](examples/sample-pack.md).

## What You Get

- A PDF suitable for printing or electronic open-book lookup.
- Chapter-ordered knowledge lookup.
- Directly writable short-answer and essay templates.
- High-frequency themes mined from past papers.
- A verified textbook page index.
- A standalone calculation appendix.
- Notes about missing sources, OCR uncertainty, and external supplementary material.
- An editable Markdown source in `work/`.

## Installation

Clone the repository, then run from the repository root.

Windows (PowerShell):

```powershell
.\scripts\install.ps1 -WithDeps
```

macOS / Linux:

```bash
sh scripts/install.sh --with-deps
```

The default `auto` target installs into every agent whose home folder exists (`~/.codex`, `~/.claude`), falling back to Codex. You can choose explicitly:

```powershell
.\scripts\install.ps1 -Target claude     # codex | claude | all
.\scripts\install.ps1 -SkillsDir D:\my-skills
```

Manual install: copy the whole `skills/open-book-exam-pack` folder into `~/.codex/skills/` or `~/.claude/skills/` (or a project's `.claude/skills/`), then run `pip install -r skills/open-book-exam-pack/scripts/requirements.txt`.

Restart or refresh the agent after installation.

## Validation

```powershell
.\scripts\validate.ps1        # front matter and every file SKILL.md references
.\scripts\validate.ps1 -Full  # also compiles the scripts, renders the sample PDF, and runs the Codex validator if present
```

GitHub Actions runs `-Full` on Ubuntu and Windows and uploads the sample PDF as a build artifact.

## Example Prompts

```text
Use open-book-exam-pack to create an open-book exam PDF from these lecture slides, past papers, and the textbook.
```

```text
Create a textbook page lookup table. I can only bring the printed textbook, so do not include PDF page numbers.
```

```text
Make the calculation steps detailed and place them in a separate final appendix.
```

```text
The text is too small. Improve readability without leaving large blank spaces.
```

More examples are available in [references/examples.md](references/examples.md).

## Recommended Inputs

- Course slides or handouts in PDF/PPT format.
- Past exam papers in PDF format.
- The open-book textbook PDF.
- Exam rules: printed textbook only, printed notes, or electronic PDFs.
- Preferences for page count, font size, and layout density.
- The exam scope, if available.

## Recommended Output Structure

1. How to use the open-book pack.
2. Chapter quick lookup.
3. High-frequency short-answer templates.
4. Multiple-choice / true-false lookup.
5. Subjective-answer skeletons.
6. Past-paper questions likely to be reused.
7. Reusable sentence bank.
8. Textbook page index.
9. Calculation appendix (last, on its own pages).

## Repository Layout

```text
skills/
  open-book-exam-pack/        # this folder is what gets installed
    SKILL.md
    agents/
      openai.yaml
    scripts/
      probe_pdfs.py
      extract_text.py
      textbook_pages.py
      peek_text.py
      build_pdf.py
      requirements.txt
    references/
      pack-format.md
      answer-templates.md
      example-ai-course.md
examples/
  sample-pack.md
scripts/
  install.ps1
  install.sh
  validate.ps1
references/
  examples.md
.github/workflows/validate.yml
AGENTS.md
CHANGELOG.md
README.md
```

## File Guide

| File | Purpose |
| --- | --- |
| `skills/open-book-exam-pack/SKILL.md` | Main skill instructions: triggers, workflow modes, process, and quality constraints. |
| `skills/open-book-exam-pack/agents/openai.yaml` | OpenAI/Codex-facing display metadata and default prompt. |
| `skills/open-book-exam-pack/scripts/` | Inventory, text/OCR, page verification, and PDF build scripts. |
| `skills/open-book-exam-pack/references/` | Source syntax, generic answer templates, and a real-course example. |
| `examples/sample-pack.md` | Renderable sample source, also used by the CI smoke test. |
| `scripts/install.ps1` / `install.sh` | Install into the Codex / Claude Code skills directory. |
| `scripts/validate.ps1` | Checks core files and references; `-Full` tests the scripts. |
| `references/examples.md` | Copyable prompts and expected output shapes. |
| `AGENTS.md` | Quick orientation for coding agents using this repo. |
| `CHANGELOG.md` | Release history. |
| `GITHUB_TEXT.md` | GitHub About, topics, release notes, and other public copy. |

## Design Principles

- Make answers easy to find during the exam.
- Prefer directly writable answers over keyword-only notes.
- Treat textbook page numbers as source-critical data.
- Keep calculation steps complete and verifiable.
- Preserve readability instead of blindly compressing page count.
- Mine topics from this course's materials; never reuse another course's checklist.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| The skill does not auto-trigger | Explicitly write "use the open-book-exam-pack skill", rerun the install script, then restart the agent. |
| `PyMuPDF is required` / `reportlab is required` | `pip install -r skills/open-book-exam-pack/scripts/requirements.txt`, or install with `-WithDeps`. |
| PDF text extraction is empty | The PDF is probably scanned: `pip install rapidocr_onnxruntime`, then `extract_text.py --ocr`. |
| Textbook page numbers do not match PDF pages | Trust printed pages; measure with `textbook_pages.py offset`, then spot-check with `check --render`. |
| Chinese text renders as boxes | Pass a TrueType CJK font with `--font` (.ttf/.ttc); CFF-based .otf fonts are not supported. |
| Cannot overwrite the old PDF | It is open in a viewer; write a new file with `-o`. |
| The output is too dense or too small | Ask for `polish` mode or raise `--body-size`; readability wins over page count. |

## Related Projects

This repository borrows documentation ideas from several public study and agent-skill projects:

- [Pattyboi101/open-book-exam-prep](https://github.com/Pattyboi101/open-book-exam-prep): clear agent quick-start prompts and output descriptions.
- [planetis-m/study-assistant](https://github.com/planetis-m/study-assistant): mode-based study workflows.
- [deusyu/superforecasting-skill](https://github.com/deusyu/superforecasting-skill): file guide, agent notes, and troubleshooting structure.

## License

MIT License. See [LICENSE.md](LICENSE.md).
