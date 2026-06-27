param(
  [switch]$Full
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$skillDir = Join-Path $repoRoot "skills\open-book-exam-pack"
$skillFile = Join-Path $skillDir "SKILL.md"
$agentFile = Join-Path $skillDir "agents\openai.yaml"
$validator = Join-Path $env:USERPROFILE ".codex\skills\.system\skill-creator\scripts\quick_validate.py"

if (-not (Test-Path $skillFile)) {
  throw "Missing SKILL.md at $skillFile"
}

if (-not (Test-Path $agentFile)) {
  throw "Missing OpenAI agent config at $agentFile"
}

Write-Host "Core files found:"
Write-Host " - $skillFile"
Write-Host " - $agentFile"

$frontMatter = Get-Content -Encoding UTF8 -Path $skillFile -TotalCount 5
if ($frontMatter[0] -ne "---") {
  throw "SKILL.md must start with YAML front matter."
}

if (-not ($frontMatter -match "^name:\s+open-book-exam-pack$")) {
  throw "SKILL.md front matter must include name: open-book-exam-pack"
}

if (-not (Select-String -Path $agentFile -Pattern "display_name:" -Quiet)) {
  throw "OpenAI agent config must include interface.display_name."
}

if ($Full -and (Test-Path $validator)) {
  $env:PYTHONUTF8 = "1"
  python $validator $skillDir
  if ($LASTEXITCODE -ne 0) {
    throw "Full Codex skill validation failed."
  }
  Write-Host "Full Codex skill validation passed."
} elseif ($Full) {
  Write-Host "Codex skill validator not found locally; skipped full validation."
} else {
  Write-Host "Basic validation passed. Run .\scripts\validate.ps1 -Full to use the local Codex validator when available."
}
