# 发布到 GitHub

## 方法一：网页上传

1. 打开 GitHub，创建新仓库。
2. 仓库名建议：`open-book-exam-pack`。
3. 描述使用 `GITHUB_TEXT.md` 里的 Short description。
4. 上传本目录下所有文件：
   - `README.md`
   - `GITHUB_TEXT.md`
   - `PUBLISHING.md`
   - `LICENSE.md`
   - `.gitignore`
   - `skills/open-book-exam-pack/SKILL.md`
   - `skills/open-book-exam-pack/agents/openai.yaml`
5. 提交信息使用：

```text
Add open-book exam pack Codex skill
```

## 方法二：命令行上传

在本目录运行：

```powershell
git init
git add .
git commit -m "Add open-book exam pack Codex skill"
git branch -M main
git remote add origin https://github.com/<your-name>/open-book-exam-pack.git
git push -u origin main
```

把 `<your-name>` 换成你的 GitHub 用户名或组织名。

## 安装这个 Skill

从仓库下载后，把 Skill 目录复制到 Codex skills 目录：

```powershell
Copy-Item -Recurse .\skills\open-book-exam-pack "$env:USERPROFILE\.codex\skills\open-book-exam-pack" -Force
```

然后重启或刷新 Codex。

## 验证

如果你本机有 Codex skill-creator 的校验脚本，可运行：

```powershell
$env:PYTHONUTF8='1'
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "$env:USERPROFILE\.codex\skills\open-book-exam-pack"
```

看到 `Skill is valid!` 即可。

