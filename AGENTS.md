# Agent Notes

This repository contains an agent skill (Codex and Claude Code) for creating open-book exam review PDFs.

Read this file when a user asks you to install, test, or use this repository with an agent such as Codex, Claude Code, Cursor, or another coding assistant.

## What This Repo Is

- `skills/open-book-exam-pack/SKILL.md` is the main skill instruction file. The whole `skills/open-book-exam-pack/` folder is what gets installed.
- `skills/open-book-exam-pack/scripts/` holds the Python helpers the skill calls (inventory, text/OCR, textbook page offsets, PDF build).
- `skills/open-book-exam-pack/references/` holds the pack Markdown syntax, generic answer templates, and one real-course example.
- `skills/open-book-exam-pack/agents/openai.yaml` contains the OpenAI agent-facing display metadata.
- `scripts/install.ps1` / `scripts/install.sh` install the skill into `~/.codex/skills` and/or `~/.claude/skills`.
- `scripts/validate.ps1` runs repository validation; `-Full` also smoke-tests the Python scripts.
- `examples/sample-pack.md` is a renderable sample used by CI.
- `references/examples.md` contains copyable prompts and expected output shapes.

## Typical Agent Workflow

1. Install dependencies once: `python -m pip install -r skills/open-book-exam-pack/scripts/requirements.txt`.
2. Inventory the user's files with `probe_pdfs.py` and classify them as courseware, past papers, textbook, or instructions.
3. Choose the workflow mode: `pack`, `page-index`, `past-paper`, `calculation`, or `polish`.
4. Extract text with `extract_text.py`; add `--ocr` only when PDFs are scanned or text is too sparse.
5. Treat textbook page numbers as high-stakes: take them from the TOC (`textbook_pages.py toc`), and if PDF pages are needed, measure and spot-check the offset (`offset`, `check`).
6. Write the pack as Markdown in `work/`, render it with `build_pdf.py` into `outputs/`, and preview the first pages before delivering.

## Guardrails

- Do not invent textbook page numbers.
- Do not replace local source material with web summaries.
- Do not reuse another course's topic checklist; mine topics from this course's papers and slides.
- Do not compress text until it becomes unreadable (body text stays at or above 6.3 pt).
- Do not remove old generated PDFs unless the user explicitly asks.
- If calculation problems include formulas, matrices, diagrams, or numbers, verify them against the source before finalizing.

## Editing This Repo

- Keep `SKILL.md` course-agnostic; course-specific material belongs in `references/example-*.md`.
- Any `scripts/...` or `references/...` path mentioned in `SKILL.md` must exist; `validate.ps1` checks this.
- Scripts must stay standalone (no shared module) because the skill folder is copied as-is.
- Record user-visible changes in `CHANGELOG.md`.

## Quick Local Commands

```powershell
.\scripts\validate.ps1
.\scripts\validate.ps1 -Full
.\scripts\install.ps1 -WithDeps
```
