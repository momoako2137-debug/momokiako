# Resume helper (ASCII only). Shows memo + line to paste into Claude Code.
# Run: .\続き.ps1   or double-click 続き.bat

$ErrorActionPreference = "Stop"
try {
    [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
} catch { }
Set-Location $PSScriptRoot

# Prefer 00_ももさん用 for Claude*.txt / 07_ fallback (not 00_入口)
$momDir = Join-Path $PSScriptRoot "00_ももさん用"
if (Test-Path -LiteralPath $momDir) {
    $base = Get-Item -LiteralPath $momDir
} else {
    $base = Get-ChildItem -LiteralPath $PSScriptRoot -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -like "00_*" -and $_.Name -ne "00_入口" } |
        Select-Object -First 1
}
if (-not $base) {
    Write-Host "ERROR: 00_ももさん用 not found and no other 00_* folder."
    exit 1
}

$memoRoot = Join-Path $PSScriptRoot "hikitsugi.txt"
$memoFile = $null
if (Test-Path -LiteralPath $memoRoot) {
    $memoFile = Get-Item -LiteralPath $memoRoot
} else {
    $memoFile = Get-ChildItem -LiteralPath $base.FullName -Filter "07_*.txt" | Select-Object -First 1
}
$pasteFile = Get-ChildItem -LiteralPath $base.FullName -Filter "Claude*.txt" | Select-Object -First 1

Write-Host ""
Write-Host "======== memo (next tasks) ========" -ForegroundColor Cyan
if ($memoFile) {
    Get-Content -LiteralPath $memoFile.FullName -Encoding UTF8 | Write-Host
} else {
    Write-Host "(hikitsugi.txt not found)"
}
Write-Host ""
Write-Host "======== Claude Code ========" -ForegroundColor Cyan
Write-Host "1. cd to folder:"
Write-Host "   $PSScriptRoot"
Write-Host "2. run: claude"
Write-Host "3. paste this line:" -ForegroundColor Yellow
Write-Host ""
if ($pasteFile) {
    $line = (Get-Content -LiteralPath $pasteFile.FullName -Raw -Encoding UTF8).Trim()
    Write-Host $line -ForegroundColor Yellow
    try {
        Set-Clipboard -Value $line
        Write-Host ""
        Write-Host ">>> Copied to clipboard. In Claude Code press Ctrl+V to paste." -ForegroundColor Green
    } catch {
        Write-Host "(Clipboard copy failed - open Claude再開_コピペ一行.txt manually)"
    }
} else {
    Write-Host "(Claude*.txt not found - open Claude再開_コピペ一行.txt)"
}
Write-Host ""
