# 发布到 GitHub

这个仓库已经按公开 Agent Skill 项目整理，可直接推送到 GitHub。

## GitHub 仓库信息

- Repository name: `open-book-exam-pack`
- Description: `Codex / Claude Code skill for building open-book exam review PDFs from courseware, past papers, and verified textbook page indexes.`
- Topics: `codex-skill`, `claude-code`, `claude-skill`, `agent-skill`, `open-book-exam`, `study-notes`, `study-tools`, `study-guide`, `pdf`, `ocr`, `exam-prep`, `education`, `ai-agent`

更多文案见 `GITHUB_TEXT.md`，版本记录见 `CHANGELOG.md`。

README 语言入口：

- 中文：`README.md`
- English: `README.en.md`

## 发布前检查

```powershell
.\scripts\validate.ps1 -Full
```

推送到 `main` 后，GitHub Actions（`.github/workflows/validate.yml`）会在 Ubuntu 和 Windows 上重复这项检查。

## 命令行发布

如果本地已经有仓库权限：

```powershell
git add .
git commit -m "<变更说明>"
git push origin main
```

发布新版本时打标签，并用 `GITHUB_TEXT.md` 中的 Release notes 创建 Release：

```powershell
git tag v1.1.0
git push origin v1.1.0
```

如果是首次创建远程仓库：

```powershell
git init
git add .
git commit -m "Add open-book exam pack skill"
git branch -M main
git remote add origin https://github.com/<your-name>/open-book-exam-pack.git
git push -u origin main
```

把 `<your-name>` 换成 GitHub 用户名或组织名。

## 安装这个 Skill

从仓库下载后运行：

```powershell
.\scripts\install.ps1 -WithDeps            # Windows
```

```bash
sh scripts/install.sh --with-deps          # macOS / Linux
```

也可以手动把 `skills/open-book-exam-pack` 文件夹复制到 `~/.codex/skills/` 或 `~/.claude/skills/`，然后重启或刷新 Agent。
