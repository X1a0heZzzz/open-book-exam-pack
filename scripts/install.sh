#!/usr/bin/env sh
# Install the open-book-exam-pack skill on macOS/Linux.
#
#   ./scripts/install.sh                 # auto: every agent whose home folder exists (Codex if none)
#   ./scripts/install.sh claude          # codex | claude | all
#   ./scripts/install.sh --dir PATH      # custom skills directory
#   ./scripts/install.sh all --with-deps # also pip-install Python dependencies
set -eu

repo_root=$(cd "$(dirname "$0")/.." && pwd)
source_dir="$repo_root/skills/open-book-exam-pack"
target=auto
custom_dir=
with_deps=0

while [ $# -gt 0 ]; do
  case "$1" in
    codex|claude|all|auto) target=$1 ;;
    --dir) shift; custom_dir=${1:?--dir needs a path} ;;
    --with-deps) with_deps=1 ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
  shift
done

[ -d "$source_dir" ] || { echo "Skill source not found: $source_dir" >&2; exit 1; }

if [ -n "$custom_dir" ]; then
  dirs=$custom_dir
else
  case "$target" in
    codex) dirs="$HOME/.codex/skills" ;;
    claude) dirs="$HOME/.claude/skills" ;;
    all) dirs="$HOME/.codex/skills $HOME/.claude/skills" ;;
    auto)
      dirs=
      [ -d "$HOME/.codex" ] && dirs="$HOME/.codex/skills"
      [ -d "$HOME/.claude" ] && dirs="$dirs $HOME/.claude/skills"
      [ -n "$dirs" ] || dirs="$HOME/.codex/skills"
      ;;
  esac
fi

for dir in $dirs; do
  dest="$dir/open-book-exam-pack"
  mkdir -p "$dir"
  rm -rf "$dest"
  cp -R "$source_dir" "$dest"
  find "$dest" -name __pycache__ -type d -prune -exec rm -rf {} +
  echo "Installed open-book-exam-pack to $dest"
done

if [ "$with_deps" -eq 1 ]; then
  python3 -m pip install -r "$source_dir/scripts/requirements.txt"
fi

echo "Restart or refresh your agent (Codex / Claude Code) to load the skill."
