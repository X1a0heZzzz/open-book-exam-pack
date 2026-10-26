# Changelog

## v1.1.0 - 2026-10-26

### Added

- Bundled Python scripts in `skills/open-book-exam-pack/scripts/`:
  - `probe_pdfs.py`: material inventory with scanned-PDF detection and role guess.
  - `extract_text.py`: per-page text extraction, optional OCR (RapidOCR or Tesseract), page renders.
  - `textbook_pages.py`: TOC discovery, printed-page offset measurement (including offset changes inside a book), and page spot checks.
  - `peek_text.py`: UTF-8-safe viewing and grep, replacing the previously referenced but missing helper.
  - `build_pdf.py`: Markdown subset to A4 PDF with CJK font discovery, tables with repeated headers, highlights, columns, landscape, and appendix page breaks.
- Skill references: `pack-format.md`, `answer-templates.md`, and `example-ai-course.md`.
- `examples/sample-pack.md`, a renderable sample pack.
- Claude Code support: `install.ps1 -Target codex|claude|all|auto` and `-WithDeps`.
- `scripts/install.sh` for macOS/Linux.
- GitHub Actions workflow running full validation on Ubuntu and Windows.

### Changed

- `SKILL.md` is now course-agnostic: the AI-course topic checklist moved to `references/example-ai-course.md`, and a past-paper analysis step now produces the topic list for each course.
- The workflow now names the exact script for each step and adds a PDF build-and-preview step.
- `validate.ps1` checks the description length and that every file `SKILL.md` references exists; `-Full` compiles the scripts and renders the sample PDF.
- `install.ps1` replaces the previous installed copy instead of merging into it, so deleted files do not linger.

## v1.0.0

- Initial release of the Open Book Exam Pack Codex skill.
