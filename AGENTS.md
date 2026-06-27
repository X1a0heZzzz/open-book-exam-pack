# Agent Notes

This repository contains a Codex Skill for creating open-book exam review PDFs.

Read this file when a user asks you to install, test, or use this repository with an agent such as Codex, Claude Code, Cursor, or another coding assistant.

## What This Repo Is

- `skills/open-book-exam-pack/SKILL.md` is the main skill instruction file.
- `skills/open-book-exam-pack/agents/openai.yaml` contains the OpenAI agent-facing display metadata.
- `scripts/install.ps1` installs the skill into the local Codex skills directory.
- `scripts/validate.ps1` runs basic repository validation and can call the local Codex validator with `-Full`.
- `references/examples.md` contains copyable prompts and expected output shapes.

## Typical Agent Workflow

1. Inspect the user-provided course files and classify them as courseware, past papers, textbook, or instructions.
2. Choose the workflow mode:
   - `pack` for a full open-book PDF.
   - `page-index` for textbook page lookup.
   - `past-paper` for exam pattern mining.
   - `calculation` for worked calculation templates.
   - `polish` for layout improvement.
3. Extract text first; use OCR only when PDFs are scanned or text is too sparse.
4. Treat textbook page numbers as high-stakes: derive them from the table of contents or verified body pages.
5. Save final user-facing PDFs to `outputs/`; keep intermediate files in `work/`.

## Guardrails

- Do not invent textbook page numbers.
- Do not replace local source material with web summaries.
- Do not compress text until it becomes unreadable.
- Do not remove old generated PDFs unless the user explicitly asks.
- If calculation problems include formulas, matrices, diagrams, or numbers, verify them against the source before finalizing.

## Quick Local Commands

```powershell
.\scripts\validate.ps1
.\scripts\install.ps1
```

Use full validation only when the local Codex validator and dependencies are available:

```powershell
.\scripts\validate.ps1 -Full
```
