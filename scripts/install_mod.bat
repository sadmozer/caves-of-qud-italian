@echo off
setlocal

set "SOURCE=%~dp0..\ItalianLanguage"
set "DEST=%USERPROFILE%\AppData\LocalLow\Freehold Games\CavesOfQud\Mods\ItalianLanguage"

echo Source:      %SOURCE%
echo Destination: %DEST%
echo.

if not exist "%SOURCE%" (
    echo ERRORE: cartella sorgente non trovata: %SOURCE%
    pause
    exit /b 1
)

robocopy "%SOURCE%" "%DEST%" /E /PURGE /NFL /NDL /NJH /NJS

if %ERRORLEVEL% GEQ 8 (
    echo ERRORE: robocopy ha fallito con codice %ERRORLEVEL%
    pause
    exit /b 1
)

echo Installazione completata!
pause
