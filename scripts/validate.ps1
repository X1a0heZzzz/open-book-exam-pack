param(
  # Also compile the Python scripts, render examples/sample-pack.md, and run the Codex validator if present
  [switch]$Full
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$skillDir = Join-Path $repoRoot "skills/open-book-exam-pack"
$skillFile = Join-Path $skillDir "SKILL.md"
$agentFile = Join-Path $skillDir "agents/openai.yaml"
$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
$validator = Join-Path $homeDir ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
$failures = New-Object System.Collections.Generic.List[string]

function Fail([string]$message) { $failures.Add($message) }

foreach ($file in @($skillFile, $agentFile)) {
  if (-not (Test-Path $file)) { Fail "Missing $file" }
}
if ($failures.Count -gt 0) { throw ($failures -join "`n") }

# Front matter: name must match the folder, description must exist and stay within 1024 chars.
$lines = Get-Content -Encoding UTF8 -Path $skillFile
if ($lines[0] -ne "---") {
  Fail "SKILL.md must start with YAML front matter."
} else {
  $end = [Array]::IndexOf($lines, "---", 1)
  $front = $lines[1..($end - 1)]
  if (-not ($front -match "^name:\s+open-book-exam-pack$")) {
    Fail "SKILL.md front matter must include name: open-book-exam-pack"
  }
  $description = ($front | Where-Object { $_ -match "^description:" }) -replace "^description:\s*", ""
  if (-not $description) {
    Fail "SKILL.md front matter must include a description."
  } elseif ($description.Length -gt 1024) {
    Fail "SKILL.md description is $($description.Length) chars; keep it under 1024."
  }
}

if (-not (Select-String -Path $agentFile -Pattern "display_name:" -Quiet)) {
  Fail "OpenAI agent config must include interface.display_name."
}

# Every scripts/... or references/... path mentioned in SKILL.md must exist in the skill folder.
$text = Get-Content -Raw -Encoding UTF8 -Path $skillFile
$referenced = [regex]::Matches($text, '(?:scripts|references)/[A-Za-z0-9_.\-]+\.(?:py|md|txt)') |
  ForEach-Object { $_.Value } | Sort-Object -Unique
foreach ($rel in $referenced) {
  if (-not (Test-Path (Join-Path $skillDir $rel))) { Fail "SKILL.md references missing file: $rel" }
}

if ($failures.Count -gt 0) { throw ("Validation failed:`n - " + ($failures -join "`n - ")) }

Write-Host "Basic validation passed:"
Write-Host " - front matter OK"
Write-Host " - $($referenced.Count) bundled files referenced by SKILL.md exist"

if (-not $Full) {
  Write-Host "Run .\scripts\validate.ps1 -Full to also test the Python scripts."
  exit 0
}

$python = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }
$env:PYTHONUTF8 = "1"
$scriptDir = Join-Path $skillDir "scripts"
$pyFiles = @(Get-ChildItem -Path $scriptDir -Filter *.py | ForEach-Object { $_.FullName })

& $python -m py_compile @pyFiles
if ($LASTEXITCODE -ne 0) { throw "Python syntax check failed." }
Write-Host "Python syntax OK ($($pyFiles.Count) scripts)."

& $python -c "import pymupdf, reportlab" 2>$null
if ($LASTEXITCODE -ne 0) {
  Write-Host "pymupdf/reportlab not installed; skipped the PDF smoke test (pip install -r skills/open-book-exam-pack/scripts/requirements.txt)."
} else {
  $outDir = Join-Path $repoRoot "work/validate"
  New-Item -ItemType Directory -Force -Path $outDir | Out-Null
  $pdf = Join-Path $outDir "sample-pack.pdf"
  & $python (Join-Path $scriptDir "build_pdf.py") (Join-Path $repoRoot "examples/sample-pack.md") -o $pdf
  if ($LASTEXITCODE -ne 0) { throw "build_pdf.py failed on examples/sample-pack.md." }
  & $python (Join-Path $scriptDir "probe_pdfs.py") $pdf
  if ($LASTEXITCODE -ne 0) { throw "probe_pdfs.py failed." }
  & $python (Join-Path $scriptDir "extract_text.py") $pdf --out (Join-Path $outDir "text")
  if ($LASTEXITCODE -ne 0) { throw "extract_text.py failed." }
  & $python (Join-Path $scriptDir "textbook_pages.py") offset $pdf
  if ($LASTEXITCODE -ne 0) { throw "textbook_pages.py failed." }
  Write-Host "PDF smoke test passed ($pdf)."
}

if (Test-Path $validator) {
  & $python $validator $skillDir
  if ($LASTEXITCODE -ne 0) { throw "Codex skill validation failed." }
  Write-Host "Codex skill validation passed."
} else {
  Write-Host "Codex skill validator not found locally; skipped it."
}
