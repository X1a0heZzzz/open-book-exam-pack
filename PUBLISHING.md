# 发布到 GitHub

这个仓库已经按公开 Codex Skill 项目整理，可直接推送到 GitHub。

## GitHub 仓库信息

- Repository name: `open-book-exam-pack`
- Description: `Codex Skill for building open-book exam review PDFs from courseware, past papers, and textbook page indexes.`
- Topics: `codex-skill`, `open-book-exam`, `study-notes`, `pdf`, `ocr`, `exam-prep`, `education`

更多文案见 `GITHUB_TEXT.md`。

## 命令行发布

如果本地已经有仓库权限：

```powershell
git add .
git commit -m "Improve docs and skill install workflow"
git push origin main
```

如果是首次创建远程仓库：

```powershell
git init
git add .
git commit -m "Add open-book exam pack Codex skill"
git branch -M main
git remote add origin https://github.com/<your-name>/open-book-exam-pack.git
git push -u origin main
```

把 `<your-name>` 换成 GitHub 用户名或组织名。

## 网页发布

1. 在 GitHub 创建公开仓库 `open-book-exam-pack`。
2. 使用 `GITHUB_TEXT.md` 中的 Short description 和 Topics。
3. 上传仓库全部文件。
4. 提交信息使用 `Add open-book exam pack Codex skill`。

## 安装这个 Skill

从仓库下载后运行：

```powershell
.\scripts\install.ps1
```

也可以手动复制：

```powershell
Copy-Item -Recurse .\skills\open-book-exam-pack "$env:USERPROFILE\.codex\skills\open-book-exam-pack" -Force
```

然后重启或刷新 Codex。

## 验证

```powershell
.\scripts\validate.ps1
```

默认会执行基础文件检查。

完整校验可用：

```powershell
.\scripts\validate.ps1 -Full
```
