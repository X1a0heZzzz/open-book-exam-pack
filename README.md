# Open Book Exam Pack Skill

一个用于生成“开卷考试资料包”的 Codex Skill。它把课程课件、往年试卷、教材 PDF 和用户排版要求整合为可打印、可翻查的复习资料，尤其适合需要：

- 按章节顺序速查知识点
- 根据往年试卷提炼高频题型
- 整理简答题、主观题和计算题模板
- 建立教材页码索引
- 输出开卷可用 PDF

## Skill 能做什么

- 识别课件、试卷、教材三类素材
- 处理扫描版 PDF 和 OCR 文本噪声
- 从教材目录确认页码，避免凭空推断
- 根据用户要求调整排版密度、字号、空白和页数
- 将计算题作为最后独立附录，写完整教程式解题步骤
- 在只允许携带实体教材时，自动删除 PDF 页码，只保留教材页码

## 安装

把 `skills/open-book-exam-pack` 复制到你的 Codex skills 目录：

```powershell
Copy-Item -Recurse .\skills\open-book-exam-pack "$env:USERPROFILE\.codex\skills\open-book-exam-pack" -Force
```

重启或刷新 Codex 后，遇到同类任务会自动触发。

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

- 课程课件 PDF/PPT
- 往年试卷 PDF
- 开卷教材 PDF
- 用户对页数、字号、排版密度、是否可携带电子版的说明

## 输出习惯

默认把最终 PDF 放到当前工作区的 `outputs/` 目录，中间 OCR、预览图和脚本放到 `work/`。

## 仓库结构

```text
skills/
  open-book-exam-pack/
    SKILL.md
    agents/
      openai.yaml
```

## 设计原则

这不是普通摘要技能，而是“考试可用资料包”技能。它优先考虑：

- 考场能不能快速翻到
- 答案能不能直接写
- 页码是否来自教材目录
- 计算题步骤是否完整
- 排版是否可读

