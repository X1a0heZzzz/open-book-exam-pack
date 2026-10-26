# Open Book Exam Pack Skill

[中文](README.md) | [English](README.en.md)

[![validate](https://github.com/X1a0heZzzz/open-book-exam-pack/actions/workflows/validate.yml/badge.svg)](https://github.com/X1a0heZzzz/open-book-exam-pack/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)
![Codex Skill](https://img.shields.io/badge/Codex-Skill-blue)
![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-d97757)
![Exam Prep](https://img.shields.io/badge/Exam-Prep-orange)

一个用于生成“开卷考试资料包”的 Agent Skill（支持 Codex 和 Claude Code）。它把课程课件、往年试卷、教材 PDF 和排版要求整合成可打印、可翻查、能在考试中快速定位答案的复习 PDF。

这个技能的重点不是普通摘要，而是把资料整理成“考场可用”的结构：章节速查、高频答题模板、主观题骨架、计算题步骤、教材页码索引和最终 PDF 排版。技能自带 Python 工具脚本，负责素材盘点、扫描件 OCR、教材页码偏移核验和中文 PDF 生成。

## Quick Start

1. 安装（见下方“安装”）。
2. 把下面这段发给 Codex 或 Claude Code，并替换课程信息和文件路径：

```text
请使用 open-book-exam-pack skill，帮我把课程资料整理成开卷考试 PDF。

课程：<课程名称和考试范围>
课件路径：<课件 PDF/PPT 文件夹>
往年试卷路径：<试卷 PDF 文件夹，可选>
教材路径：<教材 PDF，可选>
考场规则：<只能带实体教材 / 可以带打印资料 / 可以用电子 PDF>

要求：
- 按章节做速查。
- 提炼高频简答题和主观题模板。
- 如果有教材目录，请加入教材页码速查。
- 计算题步骤详细，单独放在最后。
- 排版紧凑但保持可读，最终 PDF 放到 outputs/。
```

## 适合什么场景

- 需要把课件、教材、旧卷整理成一份开卷考试资料。
- 需要按章节顺序快速查知识点。
- 需要根据往年试卷提炼高频题型和答题套路。
- 需要整理简答题、主观题和计算题模板。
- 需要建立教材页码索引，尤其是只能携带实体教材时。
- 需要输出紧凑但可读的考试用 PDF。

## Skill 能做什么

- 识别课件、试卷、教材三类素材，并按用途分工。
- 处理扫描版 PDF、OCR 噪声和中文路径读写问题。
- 从教材目录或正文页码确认页码，自动测出“印刷页 ↔ PDF 页”偏移并抽查，避免凭空推断。
- 根据用户要求调整排版密度、字号、空白、分栏和页数。
- 将计算题作为最后独立附录，写完整教程式解题步骤。
- 在只允许携带实体教材时，删除 PDF 页码，只保留教材印刷页码。
- 将最终 PDF 默认保存到 `outputs/`，把中间文本、OCR、预览图和 Markdown 源稿放到 `work/`。

## 工作模式

| 模式 | 适合场景 | 主要输出 |
| --- | --- | --- |
| `pack` | 从课件、旧卷和教材生成完整开卷资料包 | 一份结构化 PDF |
| `page-index` | 只想做教材页码速查 | 知识点到教材页码的表格 |
| `past-paper` | 重点分析往年试卷 | 高频题型、考点频率、答题模板 |
| `calculation` | 计算题是主要风险点 | 步骤化解题模板和易错点 |
| `polish` | 已有资料但排版不好 | 更清晰、紧凑、可打印的版本 |

不用显式写模式也可以；Agent 会根据你的材料和要求自动选择。

## 内置工具脚本

位于 `skills/open-book-exam-pack/scripts/`，Agent 会按 SKILL.md 的流程自动调用，也可以手动使用：

| 脚本 | 作用 | 示例 |
| --- | --- | --- |
| `probe_pdfs.py` | 盘点素材：页数、文字量、是否扫描件、角色猜测 | `python probe_pdfs.py 课件/ 试卷/ 教材.pdf` |
| `extract_text.py` | 逐页抽文本，扫描页 OCR，渲染截图 | `python extract_text.py 试卷.pdf --ocr` |
| `textbook_pages.py` | 找目录、测页码偏移、核对页码 | `python textbook_pages.py offset 教材.pdf` |
| `peek_text.py` | UTF-8 安全查看/检索文本 | `python peek_text.py work/text/*/all.txt --grep 梯度` |
| `build_pdf.py` | Markdown → A4 中文 PDF（表格、高亮、分栏） | `python build_pdf.py work/pack.md --columns 2` |

依赖：Python 3.9+、`pymupdf`、`reportlab`；扫描件 OCR 可选装 `rapidocr_onnxruntime`。源稿语法见 [pack-format.md](skills/open-book-exam-pack/references/pack-format.md)，样例见 [examples/sample-pack.md](examples/sample-pack.md)。

## 你会得到什么

- 一个适合打印或电子开卷翻查的 PDF。
- 按章节组织的知识点速查。
- 能直接落笔的简答题和主观题模板。
- 从旧卷提炼的高频题型和可能借鉴题型。
- 经过核验的教材页码表。
- 独立的计算题附录。
- 对缺失材料、OCR 不确定点和外部补充来源的说明。
- 可再次修改的 Markdown 源稿（`work/` 下）。

## 安装

克隆仓库后，在仓库根目录运行。

Windows（PowerShell）：

```powershell
.\scripts\install.ps1 -WithDeps
```

macOS / Linux：

```bash
sh scripts/install.sh --with-deps
```

默认 `auto`：本机有 `~/.codex` 就装到 Codex，有 `~/.claude` 就装到 Claude Code，两者都有则都装。也可以指定：

```powershell
.\scripts\install.ps1 -Target claude     # codex | claude | all
.\scripts\install.ps1 -SkillsDir D:\my-skills
```

手动安装：把 `skills/open-book-exam-pack` 整个文件夹复制到 `~/.codex/skills/` 或 `~/.claude/skills/`（项目级可放到项目的 `.claude/skills/`），再执行 `pip install -r skills/open-book-exam-pack/scripts/requirements.txt`。

重启或刷新 Agent 后，遇到同类任务会自动触发。

## 验证

```powershell
.\scripts\validate.ps1        # 基础检查：front matter、SKILL.md 引用的文件是否都存在
.\scripts\validate.ps1 -Full  # 另外编译脚本、用样例生成 PDF，并在本机有 Codex 校验器时调用
```

仓库的 GitHub Actions 会在 Ubuntu 和 Windows 上跑 `-Full` 校验，并把样例 PDF 作为构建产物上传。

## 典型触发请求

```text
根据这些课件、试卷和教材，给我做一份开卷考试 PDF。
```

```text
结合教材页码做速查表，只能带实体教材，不要 PDF 页码。
```

```text
计算题步骤要详细，单独放在最后。
```

```text
字太小，排版清楚一点，但不要大片空白。
```

更多例子见 [references/examples.md](references/examples.md)。

## 推荐输入

- 课程课件 PDF/PPT。
- 往年试卷 PDF。
- 开卷教材 PDF。
- 考场规则：能带实体教材、打印资料还是电子 PDF。
- 用户对页数、字号、排版密度的说明。
- 如果有明确考试范围，也一并提供。

## 推荐输出结构

1. 开卷使用法。
2. 章节速查。
3. 高频简答模板。
4. 选择/判断速查。
5. 主观题万能骨架。
6. 旧卷可能借鉴题型。
7. 万能句子库。
8. 教材页码速查。
9. 计算题专题教程（最后独立附录）。

## 仓库结构

```text
skills/
  open-book-exam-pack/        # 安装时复制的就是这个文件夹
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
README.en.md
```

## 文件用途

| 文件 | 用途 |
| --- | --- |
| `skills/open-book-exam-pack/SKILL.md` | Skill 主说明，定义触发场景、工作模式、处理流程和质量约束。 |
| `skills/open-book-exam-pack/agents/openai.yaml` | OpenAI/Codex 侧展示信息和默认提示词。 |
| `skills/open-book-exam-pack/scripts/` | 素材盘点、文本/OCR、页码核验、PDF 生成脚本。 |
| `skills/open-book-exam-pack/references/` | 源稿语法、通用答题模板、真实课程示例。 |
| `examples/sample-pack.md` | 可直接渲染的样例源稿，也用于 CI 冒烟测试。 |
| `scripts/install.ps1` / `install.sh` | 安装到 Codex / Claude Code 的 skills 目录。 |
| `scripts/validate.ps1` | 检查核心文件和引用，`-Full` 时测试脚本。 |
| `references/examples.md` | 可复制的使用示例和预期输出形态。 |
| `AGENTS.md` | 给 coding agent 的快速接手说明。 |
| `CHANGELOG.md` | 版本变更记录。 |
| `GITHUB_TEXT.md` | GitHub About、topics、release notes 等公开展示文案。 |

## 设计原则

- 考场能不能快速翻到。
- 答案能不能直接写。
- 页码是否来自教材目录或正文确认。
- 计算题步骤是否完整。
- 排版是否可读，而不是一味压缩页数。
- 考点从本课程素材提炼，不套用其他课程的清单。

## Troubleshooting

| 问题 | 处理方式 |
| --- | --- |
| Skill 没有自动触发 | 显式在提示词里写“请使用 open-book-exam-pack skill”，或重新运行安装脚本后重启 Agent。 |
| 脚本报 `PyMuPDF is required` / `reportlab is required` | 运行 `pip install -r skills/open-book-exam-pack/scripts/requirements.txt`，或安装时加 `-WithDeps`。 |
| PDF 文字抽不出来 | 很可能是扫描件：`pip install rapidocr_onnxruntime` 后用 `extract_text.py --ocr`。 |
| 教材页码和 PDF 页码对不上 | 以印刷页码为准；用 `textbook_pages.py offset` 测偏移，再用 `check --render` 抽查。 |
| 生成的 PDF 中文是方块 | 用 `--font` 指定一个 TrueType 中文字体（.ttf/.ttc）；CFF 格式的 .otf 不支持。 |
| 无法覆盖旧 PDF | 旧文件正被阅读器打开，用 `-o` 另存新文件名。 |
| 输出太密或字太小 | 要求 `polish` 模式，或调大 `--body-size`，优先可读性，允许增加页数。 |

## 参考项目

这个仓库借鉴了几个公开学习/考试类 agent 项目的展示方式：

- [Pattyboi101/open-book-exam-prep](https://github.com/Pattyboi101/open-book-exam-prep)：把“复制给 agent 的快速开始”和最终产物写得很清楚。
- [planetis-m/study-assistant](https://github.com/planetis-m/study-assistant)：用模式区分转写、笔记、测验、作文等学习任务。
- [deusyu/superforecasting-skill](https://github.com/deusyu/superforecasting-skill)：用文件用途表和故障排查说明帮助别人快速接手。

## License

MIT License. See [LICENSE.md](LICENSE.md).
