@echo off
setlocal

cd /d "%~dp0"

set "PY_CMD="
where python >nul 2>nul
if %errorlevel%==0 set "PY_CMD=python"
if not defined PY_CMD (
  where py >nul 2>nul
  if %errorlevel%==0 set "PY_CMD=py -3"
)

if not defined PY_CMD (
  echo [ERROR] Python no encontrado. Instala Python 3.11+.
  exit /b 1
)

if not exist ".context\profile.md" (
  echo [INFO] Primera ejecucion detectada. Iniciando instalador...
  %PY_CMD% scripts\install.py
  if %errorlevel% neq 0 exit /b %errorlevel%
)

%PY_CMD% scripts\pa.py %*
exit /b %errorlevel%
