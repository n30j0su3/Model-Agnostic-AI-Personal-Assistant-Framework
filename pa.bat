@echo off
setlocal EnableDelayedExpansion

cd /d "%~dp0"

chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║   🚀 Personal Assistant Framework - Launcher         ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

set "STOP_LAUNCH=0"

call :DetectPython
if not defined PY_CMD goto :NoPython

call :DetectGit
if "%HAS_GIT%"=="0" (
  call :HandleMissingGit
  if "%STOP_LAUNCH%"=="1" exit /b 0
)

if not exist ".context\profile.md" (
  echo [INFO] Primera ejecucion detectada. Iniciando instalador...
  %PY_CMD% scripts\install.py
  if %errorlevel% neq 0 (
    echo [ERROR] Instalacion incompleta.
    pause
    exit /b %errorlevel%
  )
)

%PY_CMD% scripts\pa.py %*
exit /b %errorlevel%

:DetectPython
set "PY_CMD="
python -V >nul 2>nul
if %errorlevel%==0 set "PY_CMD=python"
if not defined PY_CMD (
  py -3 -V >nul 2>nul
  if %errorlevel%==0 set "PY_CMD=py -3"
)
exit /b 0

:DetectGit
set "HAS_GIT=0"
git --version >nul 2>nul
if %errorlevel%==0 set "HAS_GIT=1"
exit /b 0

:CheckWinget
set "HAS_WINGET=0"
winget --version >nul 2>nul
if %errorlevel%==0 set "HAS_WINGET=1"
exit /b 0

:NoPython
echo [ERROR] Python no encontrado. Es obligatorio para ejecutar el Framework.
echo [INFO] Dependencias minimas: Python 3.11+ (obligatorio). Git es opcional.
call :CheckWinget
if "%HAS_WINGET%"=="1" goto :OfferWingetPython
goto :OfferPythonManual

:OfferWingetPython
echo.
echo  1. Instalar Python automaticamente (recomendado)
echo  2. Abrir pagina de descarga
echo  3. Salir
set /p PY_CHOICE=Selecciona [1-3]: 
if "%PY_CHOICE%"=="1" goto :InstallPython
if "%PY_CHOICE%"=="2" goto :OfferPythonManual
echo.
echo [ERROR] No se puede continuar sin Python.
echo [INFO] Descarga directa: https://www.python.org/downloads/
pause
exit /b 1

:InstallPython
winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
if %errorlevel% neq 0 goto :OfferPythonManual
echo.
echo [OK] Instalacion finalizada.
echo [INFO] Cierra esta ventana y vuelve a ejecutar pa.bat.
pause
exit /b 1

:OfferPythonManual
echo.
echo [INFO] Abriendo pagina de descarga...
echo [INFO] Descarga directa: https://www.python.org/downloads/
start https://www.python.org/downloads/
pause
exit /b 1

:HandleMissingGit
echo.
echo [WARN] Git no encontrado. Es recomendado para updates y sincronizacion.
echo [INFO] Sin Git, el Framework funcionara solo en modo local.
call :CheckWinget
if "%HAS_WINGET%"=="1" goto :OfferWingetGit
goto :OfferGitManual

:OfferWingetGit
set /p GIT_CHOICE=Deseas instalar Git ahora? [S/N]: 
if /I "%GIT_CHOICE%"=="S" goto :InstallGit
goto :ContinueNoGit

:InstallGit
winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements
if %errorlevel% neq 0 goto :OfferGitManual
echo.
echo [OK] Instalacion finalizada.
echo [INFO] Cierra esta ventana y vuelve a ejecutar pa.bat.
pause
set "STOP_LAUNCH=1"
exit /b 0

:OfferGitManual
set /p GIT_CHOICE=Abrir pagina de descarga de Git? [S/N]: 
if /I "%GIT_CHOICE%"=="S" (
  echo [INFO] Descarga directa: https://git-scm.com/download/win
  start https://git-scm.com/download/win
  pause
  set "STOP_LAUNCH=1"
  exit /b 0
)
goto :ContinueNoGit

:ContinueNoGit
echo [INFO] Continuando sin Git...
exit /b 0
