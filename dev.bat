@echo off
setlocal

cd /d "%~dp0"

set "PRIVATE_URL=https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework-dev.git"
set "PUBLIC_URL=https://github.com/n30j0su3/Model-Agnostic-AI-Personal-Assistant-Framework.git"

echo [INFO] Dev HQ launcher

:: Check Git - allow local mode without Git
git --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARN] Git no encontrado. Funcionando en modo local sin sincronizacion.
    echo [INFO] Para sincronizar cambios con GitHub, instala Git y clona el repo.
    echo.
    goto :Launch
)

:: Check Origin
set "ORIGIN_URL="
for /f "usebackq delims=" %%U in (`git remote get-url origin 2^>nul`) do set "ORIGIN_URL=%%U"

if not defined ORIGIN_URL (
    echo [WARN] Remote 'origin' no configurado.
    echo [INFO] Esto es normal si descargaste el proyecto como ZIP.
    echo [INFO] Para sincronizar cambios, clona el repo con: git clone %PRIVATE_URL%
    echo.
    goto :Launch
)

echo [INFO] Origin: %ORIGIN_URL%

:: Normalize URLs by removing .git suffix for comparison
set "ORIGIN_URL_NORM=%ORIGIN_URL:.git=%"
set "PRIVATE_URL_NORM=%PRIVATE_URL:.git=%"

if /I not "%ORIGIN_URL_NORM%"=="%PRIVATE_URL_NORM%" (
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
    echo [WARN] Remote 'upstream' no configurado.
    echo [INFO] Se recomienda agregar el upstream publico para recibir actualizaciones.
    echo [INFO] Ejecuta: git remote add upstream %PUBLIC_URL%
    echo.
) else (
    echo [INFO] Upstream: %UPSTREAM_URL%
    
    :: Normalize upstream URL for comparison
    set "UPSTREAM_URL_NORM=%UPSTREAM_URL:.git=%"
    set "PUBLIC_URL_NORM=%PUBLIC_URL:.git=%"
    
    if /I not "%UPSTREAM_URL_NORM%"=="%PUBLIC_URL_NORM%" (
        echo [ERROR] 'upstream' debe apuntar al repo publico.
        echo [INFO] Esperado: %PUBLIC_URL%
        echo [INFO] Actual:   %UPSTREAM_URL%
        pause
        exit /b 1
    )
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
:Launch
echo [INFO] Iniciando sesion de features...
call pa.bat --feature %*
if %errorlevel% neq 0 pause
exit /b %errorlevel%
