@echo off
cls
echo ==========================================
echo   INVIO AGGIORNAMENTI A GITHUB E RENDER
echo ==========================================

echo.
echo [1/4] Aggiorno la lista delle librerie (requirements.txt)...
:: Questo comando PowerShell assicura che il file sia leggibile da Render
powershell -Command "pip freeze | Out-File -Encoding UTF8 requirements.txt"

echo [2/4] Preparo i file per il caricamento...
git add .

echo.
set /p msg="Cosa hai modificato? (scrivi e premi Invio): "

echo.
echo [3/4] Salvo le modifiche...
git commit -m "%msg%"

echo [4/4] Spedisco i file su GitHub...
git push origin main

echo.
echo ==========================================
echo   FATTO! Render si aggiornera' a breve.
echo ==========================================
pause