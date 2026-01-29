@echo off
setlocal EnableDelayedExpansion

cd /d "%~dp0"

set "PRIVATE_URL=https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework-dev.git"
set "PUBLIC_URL=https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework.git"

echo.
echo [INFO] Dev HQ launcher

call :DetectGit
if "%HAS_GIT%"=="0" (
  echo [ERROR] Git es obligatorio para el entorno Dev HQ.
  exit /b 1
)

set "ORIGIN_URL="
for /f "delims=" %%U in ('git remote get-url origin 2^>nul') do set "ORIGIN_URL=%%U"
if not defined ORIGIN_URL (
  echo [ERROR] Remote origin no configurado.
  exit /b 1
)
if /I not "%ORIGIN_URL%"=="%PRIVATE_URL%" (
  echo [ERROR] origin no apunta al repo privado esperado.
  echo [INFO] Esperado: %PRIVATE_URL%
  echo [INFO] Actual:   %ORIGIN_URL%
  exit /b 1
)

set "UPSTREAM_URL="
for /f "delims=" %%U in ('git remote get-url upstream 2^>nul') do set "UPSTREAM_URL=%%U"
if not defined UPSTREAM_URL (
  echo [ERROR] Remote upstream no configurado.
  exit /b 1
)
if /I not "%UPSTREAM_URL%"=="%PUBLIC_URL%" (
  echo [ERROR] upstream no apunta al repo publico esperado.
  echo [INFO] Esperado: %PUBLIC_URL%
  echo [INFO] Actual:   %UPSTREAM_URL%
  exit /b 1
)

set "CURRENT_BRANCH="
for /f "delims=" %%B in ('git rev-parse --abbrev-ref HEAD 2^>nul') do set "CURRENT_BRANCH=%%B"
if "%CURRENT_BRANCH%"=="public-release" (
  echo [ERROR] No ejecutes Dev HQ en public-release.
  echo [INFO] Cambia a la rama privada (main).
  exit /b 1
)

call pa.bat --feature %*
exit /b %errorlevel%

:DetectGit
set "HAS_GIT=0"
git --version >nul 2>nul
if %errorlevel%==0 set "HAS_GIT=1"
exit /b 0
