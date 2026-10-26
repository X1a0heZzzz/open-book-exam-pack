# GitHub 文案

## Repository name

```text
open-book-exam-pack
```

## Short description

```text
Codex / Claude Code skill for building open-book exam review PDFs from courseware, past papers, and verified textbook page indexes.
```

## Website / social summary

```text
Turn courseware, past papers, scanned textbooks, and layout preferences into exam-ready open-book PDFs with answer templates, calculation walkthroughs, and verified textbook page lookup tables.
```

## About

```text
Reusable Codex / Claude Code workflow, with bundled Python tools, for turning course materials, scanned PDFs, past exam papers, and textbook tables of contents into structured open-book exam PDFs with answer templates, calculation tutorials, and accurate textbook page lookup tables.
```

## Topics

```text
codex-skill
claude-code
claude-skill
agent-skill
open-book-exam
study-notes
study-tools
study-guide
pdf
ocr
exam-prep
education
ai-agent
```

## Initial commit message

```text
Add open-book exam pack Codex skill
```

## Release title

```text
v1.1.0 - Bundled tools and Claude Code support
```

## Release notes

```markdown
Highlights:
- Bundled Python tools: material inventory, text extraction with OCR fallback, textbook page-offset measurement and spot checks, and a Markdown-to-PDF builder with CJK fonts.
- Course-agnostic SKILL.md with a past-paper analysis step; the AI-course checklist is now an example reference.
- Generic answer templates and the pack Markdown format as skill references.
- Install to Codex and/or Claude Code (`install.ps1 -Target`, new `install.sh` for macOS/Linux).
- CI validation on Ubuntu and Windows.

See CHANGELOG.md for details.
```

### v1.0.0

```markdown
Initial release of the Open Book Exam Pack Codex Skill.

Features:
- Classifies courseware, past papers, and textbooks into a reusable exam-pack workflow.
- Handles scanned PDFs and OCR fallback logic.
- Builds chapter-order open-book review structures.
- Generates textbook-only page lookup tables from confirmed textbook TOC entries.
- Standardizes answer templates for short-answer, subjective, and calculation questions.
- Preserves user preferences such as larger font, tighter layout, no blank pages, and calculation appendix placement.
- Adds install and validation scripts for local Codex skill setup.
- Adds public-facing quick-start prompts, workflow modes, agent orientation notes, and reusable examples.
- Adds an English README for international users.
```

## PR title

```text
[codex] Add open-book exam pack skill
```

## PR body

```markdown
## Summary

Adds a reusable Codex Skill for producing open-book exam review PDFs from course materials, past exam papers, scanned PDFs, and textbook page indexes.

## What changed

- Added `open-book-exam-pack` Skill.
- Documented the full workflow from material identification to final PDF layout.
- Included rules for OCR fallback, missing-source web lookup, textbook page indexing, answer-template construction, and calculation-question appendices.
- Captured user-driven layout preferences from the source workflow.

## Validation

- Ran Codex skill validation successfully.
```

