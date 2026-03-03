@echo off
REM Upload vidtogif to PyPI
REM Prerequisites: pip install build twine

echo === Cleaning old build artifacts ===
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist vidtogif.egg-info rmdir /s /q vidtogif.egg-info

echo === Building package ===
python -m build
if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo === Uploading to PyPI ===
python -m twine upload dist/*
if %errorlevel% neq 0 (
    echo Upload failed!
    pause
    exit /b 1
)

echo === Done! Package uploaded to PyPI ===
pause
