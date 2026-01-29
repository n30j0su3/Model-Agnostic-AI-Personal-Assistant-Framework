@echo off
setlocal

cd /d "%~dp0"

set "PRIVATE_URL=https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework-dev.git"
set "PUBLIC_URL=https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework.git"

echo [INFO] Dev HQ launcher

:: Check Git
git --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Git no encontrado.
    pause
    exit /b 1
)

:: Check Origin
set "ORIGIN_URL="
for /f "usebackq delims=" %%U in (`git remote get-url origin 2^>nul`) do set "ORIGIN_URL=%%U"

if not defined ORIGIN_URL (
    echo [ERROR] Remote 'origin' no configurado.
    pause
    exit /b 1
)

echo [INFO] Origin: %ORIGIN_URL%

if /I not "%ORIGIN_URL%"=="%PRIVATE_URL%" (
    echo [ERROR] 'origin' debe apuntar al repo privado.
    echo [INFO] Esperado: %PRIVATE_URL%
    echo [INFO] Actual:   %ORIGIN_URL%
    pause
    exit /b 1
)

:: Check Upstream
set "UPSTREAM_URL="
for /f "usebackq delims=" %%U in (`git remote get-url upstream 2^>nul`) do set "UPSTREAM_URL=%%U"

if not defined UPSTREAM_URL (
    echo [ERROR] Remote 'upstream' no configurado.
    pause
    exit /b 1
)

echo [INFO] Upstream: %UPSTREAM_URL%

if /I not "%UPSTREAM_URL%"=="%PUBLIC_URL%" (
    echo [ERROR] 'upstream' debe apuntar al repo publico.
    echo [INFO] Esperado: %PUBLIC_URL%
    echo [INFO] Actual:   %UPSTREAM_URL%
    pause
    exit /b 1
)

:: Check Branch
set "CURRENT_BRANCH="
for /f "usebackq delims=" %%B in (`git rev-parse --abbrev-ref HEAD 2^>nul`) do set "CURRENT_BRANCH=%%B"

if "%CURRENT_BRANCH%"=="public-release" (
    echo [ERROR] No trabajes en la rama 'public-release'.
    echo [INFO] Cambia a 'main' con: git checkout main
    pause
    exit /b 1
)

:: Launch
echo [INFO] Iniciando sesion de features...
call pa.bat --feature %*
if %errorlevel% neq 0 pause
exit /b %errorlevel%
