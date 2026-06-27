# Open Book Exam Pack Skill

一个用于生成“开卷考试资料包”的 Codex Skill。它把课程课件、往年试卷、教材 PDF 和排版要求整合成可打印、可翻查、能在考试中快速定位答案的复习 PDF。

这个技能的重点不是普通摘要，而是把资料整理成“考场可用”的结构：章节速查、 高频答题模板、主观题骨架、计算题步骤、教材页码索引和最终 PDF 排版。

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
```

## 设计原则

- 考场能不能快速翻到。
- 答案能不能直接写。
- 页码是否来自教材目录或正文确认。
- 计算题步骤是否完整。
- 排版是否可读，而不是一味压缩页数。

## License

MIT License. See [LICENSE.md](LICENSE.md).
