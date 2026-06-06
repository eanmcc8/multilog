# Run a demo by number (non-interactive)
param(
    [Parameter(Mandatory = $true)]
    [string]$Demo,
    [switch]$List
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path $PSScriptRoot -Parent
Set-Location $RepoRoot

$demosDir = Join-Path $RepoRoot "demos"
$num = $Demo.PadLeft(2, "0")

if ($List) {
    Get-ChildItem $demosDir -Filter "${num}_*.py" | ForEach-Object { $_.Name }
    exit 0
}

$match = Get-ChildItem $demosDir -Filter "${num}_*.py" | Select-Object -First 1
if (-not $match) {
    Write-Error "Demo $num not found in demos/"
}

Write-Host "Running $($match.Name)..." -ForegroundColor Cyan
python $match.FullName
exit $LASTEXITCODE
