@echo off
cd /d "%~dp0"
python --version >nul 2>nul
if not errorlevel 1 (
  python serve.py
  goto :eof
)
py -3 --version >nul 2>nul
if not errorlevel 1 (
  py -3 serve.py
  goto :eof
)
powershell -NoProfile -ExecutionPolicy Bypass -File "serve.ps1"
