# GitHub 文案

## Repository name

```text
open-book-exam-pack
```

## Short description

```text
Codex Skill for building open-book exam review PDFs from courseware, past papers, and textbook page indexes.
```

## About

```text
Reusable Codex workflow for turning course materials, scanned PDFs, past exam papers, and textbook tables of contents into structured open-book exam PDFs with answer templates, calculation tutorials, and accurate textbook page lookup tables.
```

## Topics

```text
codex-skill
open-book-exam
study-notes
pdf
ocr
exam-prep
education
```

## Initial commit message

```text
Add open-book exam pack Codex skill
```

## Release title

```text
v1.0.0 - Open Book Exam Pack Skill
```

## Release notes

```markdown
Initial release of the Open Book Exam Pack Codex Skill.

Features:
- Classifies courseware, past papers, and textbooks into a reusable exam-pack workflow.
- Handles scanned PDFs and OCR fallback logic.
- Builds chapter-order open-book review structures.
- Generates textbook-only page lookup tables from confirmed textbook TOC entries.
- Standardizes answer templates for short-answer, subjective, and calculation questions.
- Preserves user preferences such as larger font, tighter layout, no blank pages, and calculation appendix placement.
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

