@echo off
setlocal

cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
  python scripts\pa.py %*
  exit /b %errorlevel%
)

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 scripts\pa.py %*
  exit /b %errorlevel%
)

echo [ERROR] Python no encontrado. Instala Python 3.11+.
exit /b 1
