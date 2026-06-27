param(
  [string]$CodexSkillsDir = "$env:USERPROFILE\.codex\skills"
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$source = Join-Path $repoRoot "skills\open-book-exam-pack"
$target = Join-Path $CodexSkillsDir "open-book-exam-pack"

if (-not (Test-Path $source)) {
  throw "Skill source not found: $source"
}

New-Item -ItemType Directory -Force -Path $CodexSkillsDir | Out-Null
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -Recurse -Force -Path (Join-Path $source "*") -Destination $target

Write-Host "Installed open-book-exam-pack to $target"
Write-Host "Restart or refresh Codex to load the skill."
