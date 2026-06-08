# One-click environment setup (Windows)
param(
    [switch]$SkipPlaywright
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path $PSScriptRoot -Parent
Set-Location $RepoRoot

Write-Host "=== Multilogin X Auto Setup ===" -ForegroundColor Cyan

function Find-Python {
    $candidates = @(
        "python", "py",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe",
        "$env:ProgramFiles\Python311\python.exe",
        "$env:ProgramFiles\Python312\python.exe"
    )
    foreach ($c in $candidates) {
        try {
            if ($c -match "\\") {
                if (Test-Path $c) { return $c }
            } else {
                $v = & $c -c "import sys; print(sys.executable)" 2>$null
                if ($v) { return $c }
            }
        } catch {}
    }
    throw "Python not found. Install Python 3.10+ first."
}

$py = Find-Python
Write-Host "Python: $py"

Write-Host "`n>> pip install -e .[dev]" -ForegroundColor Blue
& $py -m pip install -e ".[dev]"

if (-not $SkipPlaywright) {
    Write-Host "`n>> playwright install chromium" -ForegroundColor Blue
    & $py -m playwright install chromium
}

$examples = @(
    @(".env.example", ".env"),
    @("profiles.csv.example", "profiles.csv"),
    @("proxies.txt.example", "proxies.txt"),
    @("keywords.txt.example", "keywords.txt"),
    @("live_comments.txt.example", "live_comments.txt")
)

Write-Host "`n>> Copy example files" -ForegroundColor Blue
foreach ($pair in $examples) {
    $src, $dst = $pair
    if ((Test-Path $src) -and -not (Test-Path $dst)) {
        Copy-Item $src $dst
        Write-Host "  Created $dst"
    }
}

$dirs = @("output", "cookies", "migration/adblogin", "migration/adspower", "migration/dolphin", "migration/incogniton")
foreach ($d in $dirs) {
    $p = Join-Path $RepoRoot $d
    if (-not (Test-Path $p)) {
        New-Item -ItemType Directory -Path $p -Force | Out-Null
        New-Item -ItemType File -Path (Join-Path $p ".gitkeep") -Force | Out-Null
        Write-Host "  Created $d/"
    }
}

Write-Host "`n>> Compile check" -ForegroundColor Blue
& $py -m compileall mlx demos tests -q

Write-Host "`n>> Tests" -ForegroundColor Blue
& $py -m pytest tests -q

Write-Host "`n=== SETUP DONE ===" -ForegroundColor Green
Write-Host "Next:"
Write-Host "  1. Edit .env (MLX_EMAIL, MLX_PASSWORD, MLX_FOLDER_ID)"
Write-Host "  2. AUTO-PIPELINE.bat  — API health check"
Write-Host "  3. RUN-DEMOS.bat      — interactive menu (120 tools)"
