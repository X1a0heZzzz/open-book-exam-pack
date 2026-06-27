# Open Book Exam Pack Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)
![Codex Skill](https://img.shields.io/badge/Codex-Skill-blue)
![Exam Prep](https://img.shields.io/badge/Exam-Prep-orange)
![PDF Workflow](https://img.shields.io/badge/PDF-Workflow-lightgrey)

一个用于生成“开卷考试资料包”的 Codex Skill。它把课程课件、往年试卷、教材 PDF 和排版要求整合成可打印、可翻查、能在考试中快速定位答案的复习 PDF。

这个技能的重点不是普通摘要，而是把资料整理成“考场可用”的结构：章节速查、高频答题模板、主观题骨架、计算题步骤、教材页码索引和最终 PDF 排版。

## Quick Start

把下面这段直接发给 Codex，并替换课程信息和文件路径：

```text
请使用 open-book-exam-pack skill，帮我把课程资料整理成开卷考试 PDF。

课程：<课程名称和考试范围>
课件路径：<课件 PDF/PPT 文件夹>
往年试卷路径：<试卷 PDF 文件夹，可选>
教材路径：<教材 PDF，可选>

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
- 从教材目录或正文页码确认页码，避免凭空推断。
- 根据用户要求调整排版密度、字号、空白和页数。
- 将计算题作为最后独立附录，写完整教程式解题步骤。
- 在只允许携带实体教材时，删除 PDF 页码，只保留教材印刷页码。
- 将最终 PDF 默认保存到 `outputs/`，把中间 OCR、预览图和脚本放到 `work/`。

## 工作模式

| 模式 | 适合场景 | 主要输出 |
| --- | --- | --- |
| `pack` | 从课件、旧卷和教材生成完整开卷资料包 | 一份结构化 PDF |
| `page-index` | 只想做教材页码速查 | 知识点到教材页码的表格 |
| `past-paper` | 重点分析往年试卷 | 高频题型、考点频率、答题模板 |
| `calculation` | 计算题是主要风险点 | 步骤化解题模板和易错点 |
| `polish` | 已有资料但排版不好 | 更清晰、紧凑、可打印的版本 |

不用显式写模式也可以；Codex 会根据你的材料和要求自动选择。

## 你会得到什么

- 一个适合打印或电子开卷翻查的 PDF。
- 按章节组织的知识点速查。
- 能直接落笔的简答题和主观题模板。
- 从旧卷提炼的高频题型和可能借鉴题型。
- 经过核验的教材页码表。
- 独立的计算题附录。
- 对缺失材料、OCR 不确定点和外部补充来源的说明。

## 安装

克隆仓库后，在仓库根目录运行：

```powershell
.\scripts\install.ps1
```

也可以手动复制：

```powershell
Copy-Item -Recurse .\skills\open-book-exam-pack "$env:USERPROFILE\.codex\skills\open-book-exam-pack" -Force
```

重启或刷新 Codex 后，遇到同类任务会自动触发。

## 验证

安装后可以运行：

```powershell
.\scripts\validate.ps1
```

如果本机存在 Codex skill 校验脚本，会执行结构校验；否则脚本会检查关键文件是否存在。

需要调用本机 Codex 完整校验器时运行：

```powershell
.\scripts\validate.ps1 -Full
```

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

## 推荐输入

- 课程课件 PDF/PPT。
- 往年试卷 PDF。
- 开卷教材 PDF。
- 用户对页数、字号、排版密度、是否可携带电子版的说明。
- 如果有明确考试范围，也一并提供。

## 推荐输出结构

1. 开卷使用法。
2. 章节速查。
3. 高频简答模板。
4. 选择/判断速查。
5. 主观题万能骨架。
6. 教材页码速查。
7. 计算题专题教程。

## 仓库结构

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
```

## 文件用途

| 文件 | 用途 |
| --- | --- |
| `skills/open-book-exam-pack/SKILL.md` | Skill 主说明，定义触发场景、工作模式、处理流程和质量约束。 |
| `skills/open-book-exam-pack/agents/openai.yaml` | OpenAI/Codex 侧展示信息和默认提示词。 |
| `scripts/install.ps1` | 将 skill 安装到本机 Codex skills 目录。 |
| `scripts/validate.ps1` | 检查核心文件是否完整，可选调用本机完整校验器。 |
| `references/examples.md` | 可复制的使用示例和预期输出形态。 |
| `AGENTS.md` | 给 coding agent 的快速接手说明。 |
| `GITHUB_TEXT.md` | GitHub About、topics、release notes 等公开展示文案。 |

## 设计原则

- 考场能不能快速翻到。
- 答案能不能直接写。
- 页码是否来自教材目录或正文确认。
- 计算题步骤是否完整。
- 排版是否可读，而不是一味压缩页数。

## Troubleshooting

| 问题 | 处理方式 |
| --- | --- |
| Skill 没有自动触发 | 显式在提示词里写“请使用 open-book-exam-pack skill”，或重新运行 `.\scripts\install.ps1` 后重启 Codex。 |
| `validate.ps1 -Full` 报缺少 Python 依赖 | 先用默认 `.\scripts\validate.ps1` 做基础检查；完整校验依赖本机 Codex validator 的运行环境。 |
| PDF 文字抽不出来 | 很可能是扫描件，按 skill 流程走页面渲染和 OCR。 |
| 教材页码和 PDF 页码对不上 | 以教材目录或正文印刷页码为准；电子 PDF 页码必须先确认偏移量。 |
| 输出太密或字太小 | 要求 `polish` 模式，优先可读性，允许增加页数。 |

## 参考项目

这个仓库借鉴了几个公开学习/考试类 agent 项目的展示方式：

- [Pattyboi101/open-book-exam-prep](https://github.com/Pattyboi101/open-book-exam-prep)：把“复制给 agent 的快速开始”和最终产物写得很清楚。
- [planetis-m/study-assistant](https://github.com/planetis-m/study-assistant)：用模式区分转写、笔记、测验、作文等学习任务。
- [deusyu/superforecasting-skill](https://github.com/deusyu/superforecasting-skill)：用文件用途表和故障排查说明帮助别人快速接手。

## License

MIT License. See [LICENSE.md](LICENSE.md).
