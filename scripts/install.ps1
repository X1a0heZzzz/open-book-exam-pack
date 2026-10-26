param(
  # codex, claude, all, or auto (every agent whose home folder exists; Codex if none do)
  [ValidateSet("auto", "codex", "claude", "all")]
  [string]$Target = "auto",
  # Install into this skills directory instead (overrides -Target)
  [Alias("CodexSkillsDir")]
  [string]$SkillsDir,
  # Also pip-install the Python dependencies used by the bundled scripts
  [switch]$WithDeps
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$source = Join-Path $repoRoot "skills/open-book-exam-pack"
$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
$agents = [ordered]@{
  codex  = Join-Path $homeDir ".codex"
  claude = Join-Path $homeDir ".claude"
}

if (-not (Test-Path $source)) {
  throw "Skill source not found: $source"
}

if ($SkillsDir) {
  $dirs = @($SkillsDir)
} else {
  $names = switch ($Target) {
    "all" { $agents.Keys }
    "auto" {
      $found = @($agents.Keys | Where-Object { Test-Path $agents[$_] })
      if ($found.Count -gt 0) { $found } else { @("codex") }
    }
    default { @($Target) }
  }
  $dirs = @($names | ForEach-Object { Join-Path $agents[$_] "skills" })
}

foreach ($dir in $dirs) {
  $dest = Join-Path $dir "open-book-exam-pack"
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  if (Test-Path $dest) {
    # Remove the old copy so renamed or deleted files do not linger.
    Remove-Item -Recurse -Force -Path $dest
  }
  Copy-Item -Recurse -Force -Path $source -Destination $dest
  Get-ChildItem -Path $dest -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
  Write-Host "Installed open-book-exam-pack to $dest"
}

if ($WithDeps) {
  $requirements = Join-Path $source "scripts/requirements.txt"
  $python = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }
  & $python -m pip install -r $requirements
  if ($LASTEXITCODE -ne 0) {
    throw "pip install failed. Install manually: $python -m pip install -r `"$requirements`""
  }
}

Write-Host "Restart or refresh your agent (Codex / Claude Code) to load the skill."
if (-not $WithDeps) {
  Write-Host "Bundled scripts need Python packages: rerun with -WithDeps or pip install -r skills/open-book-exam-pack/scripts/requirements.txt"
}
