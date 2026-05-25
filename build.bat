@echo off
chcp 65001 >nul
title 秒速画像変換 Builder
echo ========================================================
echo   秒速画像変換 (Byousoku Image Converter) Build System
echo ========================================================
echo.

echo [1/3] Installing packaging dependencies...
pip install pyinstaller pillow-heif customtkinter tkinterdnd2 pillow
echo.

echo [2/3] Packaging application with PyInstaller...
echo [NOTE] Building with icon and proper naming...
echo.

pyinstaller --noconfirm --onedir --windowed --clean ^
    --name "秒速画像変換" ^
    --icon "assets/icon.ico" ^
    --add-data "locales;locales" ^
    --add-data "assets;assets" ^
    main.py

echo.
echo ========================================================
echo   PyInstaller build complete!
echo   Output: dist\秒速画像変換\
echo ========================================================
echo.

echo [3/3] Checking for Inno Setup...
where iscc >nul 2>&1
if %errorlevel%==0 (
    echo Inno Setup found! Building installer...
    iscc installer.iss
    echo.
    echo ========================================================
    echo   Installer created in: installer_output\
    echo ========================================================
) else (
    echo Inno Setup not found in PATH.
    echo To create the installer:
    echo   1. Download Inno Setup 6 from https://jrsoftware.org/isinfo.php
    echo   2. Install it (default location: C:\Program Files (x86)\Inno Setup 6)
    echo   3. Open installer.iss and click Build ^> Compile
    echo   4. Or run: "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
    echo.
    echo The portable app is ready at: dist\秒速画像変換\
)

echo.
pause
