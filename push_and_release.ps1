# GaubenMaster - Push to GitHub & Create Release
# Führe dieses Skript AUS, NACHDEM du das Repository auf GitHub erstellt hast!

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  GaubenMaster - GitHub Push & Release" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Prüfen ob wir im richtigen Verzeichnis sind
$projectDir = "C:\Users\sonde\Desktop\Python Projekte\GaubenMaster\GaubenMaster"
if (-not (Test-Path "$projectDir\main.py")) {
    Write-Host "FEHLER: Projektverzeichnis nicht gefunden!" -ForegroundColor Red
    Read-Host "Drücke Enter zum Beenden"
    exit 1
}

Set-Location $projectDir
Write-Host "Arbeitsverzeichnis: $projectDir" -ForegroundColor Green
Write-Host ""

# 1. Push zu GitHub
Write-Host "[1/3] Push zu GitHub (master)..." -ForegroundColor Yellow
try {
    git push -u origin master
    Write-Host "  ✓ Push erfolgreich" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Push fehlgeschlagen!" -ForegroundColor Red
    Write-Host "  Hast du das Repository auf GitHub erstellt?" -ForegroundColor Yellow
    Write-Host "  URL: https://github.com/new" -ForegroundColor Yellow
    Read-Host "Drücke Enter zum Beenden"
    exit 1
}

# 2. Tag erstellen
Write-Host "[2/3] Release-Tag v1.0.0 erstellen..." -ForegroundColor Yellow
try {
    git tag v1.0.0
    git push origin v1.0.0
    Write-Host "  ✓ Tag v1.0.0 gepusht" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Tag fehlgeschlagen" -ForegroundColor Red
    Read-Host "Drücke Enter zum Beenden"
    exit 1
}

# 3. Fertig
Write-Host "[3/3] Fertig!" -ForegroundColor Green
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ERFOLGREICH!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Der Installer wird jetzt von GitHub Actions gebaut." -ForegroundColor White
Write-Host "In 2-3 Minuten verfügbar unter:" -ForegroundColor White
Write-Host ""
Write-Host "  https://github.com/soendi/GaubenMaster/releases/tag/v1.0.0" -ForegroundColor Cyan
Write-Host ""
Write-Host "Dort findest du:" -ForegroundColor White
Write-Host "  • GaubenMaster-Setup-1.0.0.exe  (Windows Installer)" -ForegroundColor White
Write-Host "  • GaubenMaster.exe               (Portable Version)" -ForegroundColor White
Write-Host ""
Write-Host "GitHub Actions Status:" -ForegroundColor White
Write-Host "  https://github.com/soendi/GaubenMaster/actions" -ForegroundColor Cyan
Write-Host ""
Read-Host "Drücke Enter zum Beenden"