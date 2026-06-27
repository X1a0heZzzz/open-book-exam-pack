# Examples

Copy these prompts into Codex after installing the skill, then replace paths and course details.

## Full Open-Book Pack

```text
请使用 open-book-exam-pack skill，帮我做一份开卷考试资料包。

课程：人工智能导论，考试范围是第1-8章。
课件：C:\path\to\slides
往年试卷：C:\path\to\past-papers
教材：C:\path\to\textbook.pdf

要求：
- 按章节做速查。
- 结合旧卷提炼高频简答题和主观题模板。
- 教材页码必须来自目录或正文确认。
- 计算题放到最后，步骤写完整。
- PDF 放到 outputs\。
```

Expected output:

- `outputs/<course>_open_book_exam_pack.pdf`
- Chapter quick lookup
- Short-answer templates
- Subjective-answer skeletons
- Textbook page index
- Calculation appendix

## Textbook Page Index Only

```text
请使用 open-book-exam-pack skill，只做教材页码速查表。

教材：C:\path\to\textbook.pdf
知识点清单：C:\path\to\topics.txt

只能带实体教材，所以不要输出 PDF 页码，只保留教材印刷页码。
```

Expected output:

- Topic
- Textbook printed page
- Where to look / how to use it
- Notes for uncertain page ranges

## Past-Paper Pattern Mining

```text
请使用 open-book-exam-pack skill，分析这些往年试卷。

试卷路径：C:\path\to\past-papers

输出：
- 高频题型
- 常见题干表达
- 分值分布
- 可复用答题模板
- 可能借鉴题型
```

Expected output:

- Frequency-ranked exam themes
- Question-type table
- Reusable answer templates
- Risk notes for ambiguous OCR

## Polish Existing Material

```text
请使用 open-book-exam-pack skill，优化这份已有开卷资料。

现有资料：C:\path\to\draft.pdf

要求：
- 字不要太小。
- 不要大片空白。
- 表格列宽更合理。
- 保留旧版，输出新版 PDF。
```

Expected output:

- A revised PDF in `outputs/`
- Brief summary of layout changes
- Note if the source PDF could not be edited directly
