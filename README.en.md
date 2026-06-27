# Open Book Exam Pack Skill

[中文](README.md) | [English](README.en.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)
![Codex Skill](https://img.shields.io/badge/Codex-Skill-blue)
![Exam Prep](https://img.shields.io/badge/Exam-Prep-orange)
![PDF Workflow](https://img.shields.io/badge/PDF-Workflow-lightgrey)

A Codex Skill for turning course slides, past papers, textbooks, scanned PDFs, and formatting requirements into exam-ready open-book review PDFs.

This is not a generic summarization skill. It is designed for material you can actually use under exam pressure: chapter lookup, answer templates, subjective-answer structures, calculation walkthroughs, verified textbook page indexes, and print-friendly PDF layout.

## Quick Start

Paste this into Codex and replace the placeholders:

```text
Please use the open-book-exam-pack skill to create an open-book exam review PDF.

Course: <course name and exam scope>
Courseware path: <folder containing lecture PDFs/PPTs>
Past-paper path: <folder containing past exam PDFs, optional>
Textbook path: <textbook PDF, optional>

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
- Handles scanned PDFs, OCR noise, and non-ASCII file paths.
- Verifies textbook page numbers from the table of contents or body pages.
- Adjusts layout density, font size, whitespace, and page count based on user preference.
- Places calculation walkthroughs in a final standalone appendix.
- Removes PDF page numbers when the exam only allows printed textbooks.
- Saves final PDFs to `outputs/` and keeps intermediate files in `work/`.

## Workflow Modes

| Mode | Best for | Main output |
| --- | --- | --- |
| `pack` | Full pack from courseware, past papers, and textbooks | A structured review PDF |
| `page-index` | Textbook page lookup only | Topic-to-page lookup table |
| `past-paper` | Past-paper pattern mining | Frequent themes, question types, answer templates |
| `calculation` | Calculation-heavy exams | Step-by-step solution templates and pitfalls |
| `polish` | Existing material with poor layout | A cleaner, tighter, printable version |

You do not have to specify a mode. Codex can infer the right mode from your materials and request.

## What You Get

- A PDF suitable for printing or electronic open-book lookup.
- Chapter-ordered knowledge lookup.
- Directly writable short-answer and essay templates.
- High-frequency themes mined from past papers.
- A verified textbook page index.
- A standalone calculation appendix.
- Notes about missing sources, OCR uncertainty, and external supplementary material.

## Installation

Clone the repository, then run this from the repository root:

```powershell
.\scripts\install.ps1
```

Manual install:

```powershell
Copy-Item -Recurse .\skills\open-book-exam-pack "$env:USERPROFILE\.codex\skills\open-book-exam-pack" -Force
```

Restart or refresh Codex after installation.

## Validation

Run the basic validation:

```powershell
.\scripts\validate.ps1
```

If the local Codex skill validator and its dependencies are available, run full validation:

```powershell
.\scripts\validate.ps1 -Full
```

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
- User preferences for page count, font size, layout density, and whether electronic PDFs are allowed.
- The exam scope, if available.

## Recommended Output Structure

1. How to use the open-book pack.
2. Chapter quick lookup.
3. High-frequency short-answer templates.
4. Multiple-choice / true-false lookup.
5. Subjective-answer skeletons.
6. Textbook page index.
7. Calculation appendix.

## Repository Layout

```text
skills/
  open-book-exam-pack/
    SKILL.md
    agents/
      openai.yaml
scripts/
  install.ps1
  validate.ps1
references/
  examples.md
AGENTS.md
README.en.md
```

## File Guide

| File | Purpose |
| --- | --- |
| `skills/open-book-exam-pack/SKILL.md` | Main skill instructions: triggers, workflow modes, process, and quality constraints. |
| `skills/open-book-exam-pack/agents/openai.yaml` | OpenAI/Codex-facing display metadata and default prompt. |
| `scripts/install.ps1` | Installs the skill into the local Codex skills directory. |
| `scripts/validate.ps1` | Checks core files and optionally calls the local full validator. |
| `references/examples.md` | Copyable prompts and expected output shapes. |
| `AGENTS.md` | Quick orientation for coding agents using this repo. |
| `README.md` | Chinese project README. |
| `GITHUB_TEXT.md` | GitHub About, topics, release notes, and other public copy. |

## Design Principles

- Make answers easy to find during the exam.
- Prefer directly writable answers over keyword-only notes.
- Treat textbook page numbers as source-critical data.
- Keep calculation steps complete and verifiable.
- Preserve readability instead of blindly compressing page count.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| The skill does not auto-trigger | Explicitly write "use the open-book-exam-pack skill", rerun `.\scripts\install.ps1`, then restart Codex. |
| `validate.ps1 -Full` fails because of Python dependencies | Use `.\scripts\validate.ps1` for basic validation; full validation depends on the local Codex validator environment. |
| PDF text extraction is empty | The PDF is probably scanned; use the skill's OCR branch. |
| Textbook page numbers do not match PDF pages | Trust printed textbook pages first; only add PDF pages after confirming the offset. |
| The output is too dense or too small | Ask for `polish` mode and prioritize readability, even if it adds pages. |

## Related Projects

This repository borrows documentation ideas from several public study and agent-skill projects:

- [Pattyboi101/open-book-exam-prep](https://github.com/Pattyboi101/open-book-exam-prep): clear agent quick-start prompts and output descriptions.
- [planetis-m/study-assistant](https://github.com/planetis-m/study-assistant): mode-based study workflows.
- [deusyu/superforecasting-skill](https://github.com/deusyu/superforecasting-skill): file guide, agent notes, and troubleshooting structure.

## License

MIT License. See [LICENSE.md](LICENSE.md).
