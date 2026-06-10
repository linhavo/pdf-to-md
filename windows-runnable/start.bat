@echo off
title PDF Konvertor
echo ============================
echo       PDF Konvertor
echo ============================
echo.

:: ── Prvni spusteni - instalace ───────────────────────────────────────────────

if not exist ".venv" (
    echo Prvni spusteni - probiha nastaveni...
    echo.

    java -version >nul 2>&1
    if errorlevel 1 (
        echo CHYBA: Java neni nainstalovana.
        echo Stahnte a nainstalujte OpenJDK z https://adoptium.net/
        echo Pak tento soubor spustte znovu.
        pause
        exit /b 1
    )

    echo Instaluji zavislosti ^(muze to chvili trvat^)...
    py -m venv .venv
    if errorlevel 1 (
        echo CHYBA: Nepodarilo se vytvorit virtualni prostredi. Je Python nainstalovan? (zkuste: py --version^)
        pause
        exit /b 1
    )
    .venv\Scripts\pip install -r requirements.txt
    if errorlevel 1 (
        echo CHYBA: Instalace zavislosti selhala.
        pause
        exit /b 1
    )
    echo.
    echo Nastaveni dokonceno!
    echo.
)

:: ── Zkratky na plose (nabidnuto jednou) ──────────────────────────────────────

if not exist ".shortcuts_created" (
    set /p CREATE_SHORTCUTS=Vytvorit zastupce na plose pro slozky vstup a vystup? [A/N]:
    if /i "%CREATE_SHORTCUTS%"=="A" (
        set DESKTOP=%USERPROFILE%\Desktop
        set HERE=%~dp0
        powershell -NoProfile -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP%\PDF Vstup.lnk');$s.TargetPath='%HERE%input';$s.Save()"
        powershell -NoProfile -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP%\PDF Vystup.lnk');$s.TargetPath='%HERE%output';$s.Save()"
        echo Zastupci byli vytvoreni na plose.
    )
    echo. > .shortcuts_created
    echo.
)

:: ── Spusteni sledovace ────────────────────────────────────────────────────────

.venv\Scripts\python watcher.py
echo.
echo Program byl ukoncen. Stisknete libovolnou klavesu pro zavreni okna...
pause > nul
