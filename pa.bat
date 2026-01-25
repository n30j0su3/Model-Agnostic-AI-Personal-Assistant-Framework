@echo off
setlocal EnableDelayedExpansion

cd /d "%~dp0"

chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║   🚀 Personal Assistant Framework - Launcher         ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

set "PY_CMD="
where python >nul 2>nul
if %errorlevel%==0 set "PY_CMD=python"
if not defined PY_CMD (
  where py >nul 2>nul
  if %errorlevel%==0 set "PY_CMD=py -3"
)

if not defined PY_CMD (
  call :HandleMissingPython
  exit /b 1
)

set "HAS_GIT=0"
where git >nul 2>nul
if %errorlevel%==0 set "HAS_GIT=1"
if "%HAS_GIT%"=="0" (
  call :HandleMissingGit
)

if not exist ".context\profile.md" (
  echo [INFO] Primera ejecucion detectada. Iniciando instalador...
  %PY_CMD% scripts\install.py
  if %errorlevel% neq 0 exit /b %errorlevel%
)

%PY_CMD% scripts\pa.py %*
exit /b %errorlevel%

:CheckWinget
set "HAS_WINGET=0"
where winget >nul 2>nul
if %errorlevel%==0 set "HAS_WINGET=1"
exit /b 0

:HandleMissingPython
echo [ERROR] Python no encontrado. Es obligatorio para ejecutar el Framework.
echo [INFO] Dependencias minimas: Python 3.11+ (obligatorio). Git es opcional.
call :CheckWinget
if "%HAS_WINGET%"=="1" (
  echo.
  echo  1. Instalar Python automaticamente (recomendado)
  echo  2. Abrir pagina de descarga
  echo  3. Salir
  set /p PY_CHOICE=Selecciona [1-3]: 
  if "%PY_CHOICE%"=="1" (
    winget install -e --id Python.Python.3.12
    echo.
    echo [OK] Instalacion finalizada.
    echo [INFO] Cierra esta ventana y vuelve a ejecutar pa.bat.
    pause
    exit /b 1
  )
  if "%PY_CHOICE%"=="2" (
    start https://www.python.org/downloads/
  )
  echo.
  echo [ERROR] No se puede continuar sin Python.
  pause
  exit /b 1
)

echo [INFO] Winget no disponible. Abriendo pagina de descarga...
start https://www.python.org/downloads/
pause
exit /b 1

:HandleMissingGit
echo.
echo [WARN] Git no encontrado. Es recomendado para updates y sincronizacion.
echo [INFO] Sin Git, el Framework funcionara solo en modo local.
call :CheckWinget
if "%HAS_WINGET%"=="1" (
  set /p GIT_CHOICE=Deseas instalar Git ahora? [S/N]: 
  if /I "%GIT_CHOICE%"=="S" (
    winget install -e --id Git.Git
    echo.
    echo [OK] Instalacion finalizada.
    echo [INFO] Cierra esta ventana y vuelve a ejecutar pa.bat.
    pause
    exit /b 0
  )
) else (
  set /p GIT_CHOICE=Abrir pagina de descarga de Git? [S/N]: 
  if /I "%GIT_CHOICE%"=="S" (
    start https://git-scm.com/download/win
  )
)

echo [INFO] Continuando sin Git...
exit /b 0
