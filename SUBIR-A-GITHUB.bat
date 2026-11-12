@echo off
chcp 65001 > nul
title Alpha Tech — Subir a GitHub
cd /d "%~dp0"

echo.
echo ════════════════════════════════════════════════════════════
echo   ALPHA TECH — Subir web v3 a GitHub
echo   Repo: alphatechnologique/alphatech-web
echo ════════════════════════════════════════════════════════════
echo Carpeta: %CD%
echo.

REM ============================================================
REM  Buscar git.exe en ubicaciones conocidas
REM ============================================================
set "GIT="

if exist "C:\Program Files\Git\bin\git.exe" set "GIT=C:\Program Files\Git\bin\git.exe"
if exist "C:\Program Files\Git\cmd\git.exe" set "GIT=C:\Program Files\Git\cmd\git.exe"
if exist "C:\Program Files (x86)\Git\bin\git.exe" set "GIT=C:\Program Files (x86)\Git\bin\git.exe"
if exist "C:\Program Files (x86)\Git\cmd\git.exe" set "GIT=C:\Program Files (x86)\Git\cmd\git.exe"

REM Si no lo encontró en rutas, probar PATH
if not defined GIT (
    for /f "delims=" %%G in ('where git 2^>nul') do set "GIT=%%G"
)

if not defined GIT (
    echo [ERROR] git.exe no encontrado.
    echo.
    echo Buscado en:
    echo   - C:\Program Files\Git\bin\git.exe
    echo   - C:\Program Files\Git\cmd\git.exe
    echo   - C:\Program Files ^(x86^)\Git\bin\git.exe
    echo   - PATH del sistema
    echo.
    echo Solución: instalar Git for Windows desde https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Git encontrado: "%GIT%"
echo.

REM ============================================================
REM  Configurar safe directory (por si la carpeta está en OneDrive/red)
REM ============================================================
"%GIT%" config --global --add safe.directory "%CD%" 2>nul

REM ============================================================
REM  Crear .gitignore si no existe
REM ============================================================
if not exist ".gitignore" (
    echo [1/7] Creando .gitignore...
    (
        echo # Sistema
        echo .DS_Store
        echo Thumbs.db
        echo desktop.ini
        echo.
        echo # Editor
        echo .vscode/
        echo .idea/
        echo *.swp
        echo.
        echo # Logs
        echo *.log
        echo upload.log
        echo.
        echo # Backups
        echo *-backup.*
        echo *-old.*
    ) > .gitignore
) else (
    echo [1/7] .gitignore ya existe...
)

REM ============================================================
REM  Inicializar git si no estaba
REM ============================================================
if not exist ".git" (
    echo [2/7] Inicializando repositorio git...
    "%GIT%" init
) else (
    echo [2/7] Repositorio git ya inicializado, continuando...
)

REM ============================================================
REM  Configurar remote
REM ============================================================
echo [3/7] Configurando remote origin...
"%GIT%" remote remove origin 2>nul
"%GIT%" remote add origin https://github.com/alphatechnologique/alphatech-web.git

REM ============================================================
REM  Configurar branch main
REM ============================================================
echo [4/7] Configurando branch main...
"%GIT%" branch -M main

REM ============================================================
REM  Add + commit
REM ============================================================
echo [5/7] Agregando archivos al staging...
"%GIT%" add .

echo [6/7] Creando commit...
"%GIT%" commit -m "Alpha Tech Web v3 — lanzamiento inicial (catalogo completo, carrito, checkout placeholder, paginas legales, casos Performance/Engineering)"

REM ============================================================
REM  Push
REM ============================================================
echo [7/7] Subiendo a GitHub...
echo.
echo Si es la primera vez, va a pedir login. Usar Personal Access Token,
echo NO la contraseña. Generalo en: https://github.com/settings/tokens
echo.
"%GIT%" push -u origin main

set RESULT=%errorlevel%

echo.
echo ════════════════════════════════════════════════════════════
if "%RESULT%"=="0" (
    echo   ✓ LISTO. El repo está actualizado en:
    echo     https://github.com/alphatechnologique/alphatech-web
    echo.
    echo   Para próximos cambios: edita los HTML, después doble-click
    echo   a este mismo .bat. Va a crear un nuevo commit y subirlo.
) else (
    echo   [ERROR] Falló el push (código %RESULT%^).
    echo.
    echo   Causas comunes:
    echo     - Credenciales: usar Personal Access Token, no password
    echo     - Repo ya tiene contenido: hacer git pull primero
    echo     - Sin conexión: chequear internet
    echo.
    echo   Volvé a correr este .bat después de resolver.
)
echo ════════════════════════════════════════════════════════════
echo.
echo Presioná cualquier tecla para cerrar esta ventana...
pause > nul
