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
set "STRICT_MODE=0"

echo [INFO] Verificando dependencias basicas...
call :DetectPython
if not defined PY_CMD goto :NoPython

call :DetectGit
if "%HAS_GIT%"=="0" (
  call :HandleMissingGit
  if "%STOP_LAUNCH%"=="1" exit /b 0
)

if not exist ".context\profile.md" set "STRICT_MODE=1"
if not exist ".git" set "STRICT_MODE=1"
if "%HAS_GIT%"=="0" set "STRICT_MODE=1"
if "%STRICT_MODE%"=="1" echo [INFO] Modo estricto activo: instalacion nueva o uso local sin Git. OpenCode es obligatorio.

if not exist ".context\profile.md" (
  echo [INFO] Primera ejecucion detectada. Iniciando instalador...
  %PY_CMD% scripts\install.py
  if !errorlevel! neq 0 (
    echo [ERROR] Instalacion incompleta.
    pause
    exit /b !errorlevel!
  )
)

echo [INFO] Verificando herramientas de IA...
call :EnsureOpenCode
if %errorlevel% neq 0 exit /b %errorlevel%

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

:DetectNode
set "HAS_NODE=0"
set "HAS_NPM=0"
node -v >nul 2>nul
if %errorlevel%==0 set "HAS_NODE=1"
npm -v >nul 2>nul
if %errorlevel%==0 set "HAS_NPM=1"
exit /b 0

:DetectOpenCode
set "HAS_OPENCODE=0"
opencode --version >nul 2>nul
if %errorlevel%==0 set "HAS_OPENCODE=1"
exit /b 0

:CheckWinget
set "HAS_WINGET=0"
winget --version >nul 2>nul
if %errorlevel%==0 set "HAS_WINGET=1"
exit /b 0

:EnsureNode
call :DetectNode
if "%HAS_NODE%"=="1" if "%HAS_NPM%"=="1" exit /b 0
echo [ERROR] Node.js/npm no detectado. Es obligatorio para instalar OpenCode.
call :CheckWinget
if "%HAS_WINGET%"=="1" goto :OfferWingetNode
goto :OfferNodeManual

:OfferWingetNode
echo.
echo  1. Instalar Node.js automaticamente (recomendado)
echo  2. Abrir pagina de descarga
echo  3. Salir
set /p NODE_CHOICE=Selecciona [1-3]: 
if "%NODE_CHOICE%"=="1" goto :InstallNode
if "%NODE_CHOICE%"=="2" goto :OfferNodeManual
echo.
echo [ERROR] No se puede continuar sin Node.js.
echo [INFO] Descarga directa: https://nodejs.org/en/download
pause
exit /b 1

:InstallNode
winget install -e --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
if %errorlevel% neq 0 goto :OfferNodeManual
call :DetectNode
if "%HAS_NODE%"=="1" if "%HAS_NPM%"=="1" (
  echo.
  echo [OK] Node.js instalado.
  exit /b 0
)
echo.
echo [INFO] Instalacion finalizada. Reinicia la terminal y vuelve a ejecutar pa.bat.
pause
exit /b 1

:OfferNodeManual
echo.
echo [INFO] Abriendo pagina de descarga...
echo [INFO] Descarga directa: https://nodejs.org/en/download
start https://nodejs.org/en/download
pause
exit /b 1

:EnsureOpenCode
call :DetectOpenCode
if "%HAS_OPENCODE%"=="1" exit /b 0
echo.
echo [WARN] OpenCode no detectado. Recomendado para usar el Framework.
if "%STRICT_MODE%"=="1" (
  echo [INFO] Modo estricto habilitado [nuevo/local]. OpenCode es obligatorio.
  echo [INFO] Este paso garantiza que la experiencia inicial sea estable y guiada.
  echo  1. Instalar OpenCode automaticamente (recomendado)
  echo  2. Ver instrucciones manuales
  echo  3. Salir
  set /p OC_CHOICE=Selecciona [1-3]: 
  if "!OC_CHOICE!"=="1" goto :InstallOpenCode
  if "!OC_CHOICE!"=="2" goto :OfferOpenCodeManualStrict
  echo.
  echo [ERROR] No se puede continuar sin OpenCode en modo estricto.
  pause
  exit /b 1
)
echo  1. Instalar OpenCode automaticamente (recomendado)
echo  2. Ver instrucciones manuales
echo  3. Continuar sin OpenCode
set /p OC_CHOICE=Selecciona [1-3]: 
if "%OC_CHOICE%"=="1" goto :InstallOpenCode
if "%OC_CHOICE%"=="2" goto :OfferOpenCodeManual
if "%OC_CHOICE%"=="3" goto :ContinueNoOpenCode
echo.
echo [WARN] Seleccion invalida. Continuando sin OpenCode.
goto :ContinueNoOpenCode

:InstallOpenCode
call :EnsureNode
if %errorlevel% neq 0 exit /b %errorlevel%
npm install -g opencode-ai
if %errorlevel% neq 0 goto :OfferOpenCodeManual
call :DetectOpenCode
if "%HAS_OPENCODE%"=="1" (
  echo.
  echo [OK] OpenCode instalado.
  exit /b 0
)
echo.
echo [INFO] Instalacion finalizada. Reinicia la terminal y vuelve a ejecutar pa.bat.
pause
exit /b 1

:OfferOpenCodeManual
echo.
echo [INFO] Instalacion manual:
echo [INFO] npm install -g opencode-ai
echo [INFO] Guia local: docs\quickstart.mdx
pause
exit /b 1

:OfferOpenCodeManualStrict
echo.
echo [INFO] Instalacion manual:
echo [INFO] npm install -g opencode-ai
echo [INFO] Guia local: docs\quickstart.mdx
echo.
echo [ERROR] OpenCode es obligatorio en modo estricto.
pause
exit /b 1

:ContinueNoOpenCode
echo [INFO] Continuando sin OpenCode...
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
