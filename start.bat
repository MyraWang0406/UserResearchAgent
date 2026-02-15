@echo off
setlocal enabledelayedexpansion

echo ===============================
echo User Research Agent - One Click Runner (Windows BAT)
echo ===============================

REM 0) Locate project root by walking up until backend\ frontend\ requirements.txt exist
set "dir=%cd%"

:findroot
if exist "%dir%\backend" if exist "%dir%\frontend" if exist "%dir%\requirements.txt" goto found
for %%I in ("%dir%\..") do set "parent=%%~fI"
if "%parent%"=="%dir%" (
  echo [ERROR] 未找到包含 backend、frontend、requirements.txt 的项目根目录。
  echo         请把 start.bat 放在项目根目录，或在项目根目录下运行。
  pause
  exit /b 1
)
set "dir=%parent%"
goto findroot

:found
cd /d "%dir%"
echo [OK] 项目根目录: %dir%

REM 1) Create venv if missing
if not exist ".venv" (
  echo [INFO] 创建虚拟环境 .venv ...
  py -m venv .venv
) else (
  echo [INFO] 已存在 .venv，跳过创建
)

REM 2) Install deps
echo [INFO] 安装依赖 ...
call ".venv\Scripts\python.exe" -m pip install -r requirements.txt

REM 3) Start backend (new window)
echo [INFO] 启动后端 http://127.0.0.1:8000 ...
start "backend" cmd /k ""%cd%\.venv\Scripts\python.exe" -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000"

REM 4) Start frontend (new window)
echo [INFO] 启动前端 http://127.0.0.1:5173/index.html ...
start "frontend" cmd /k "py -m http.server 5173 --directory frontend"

REM 5) Open URLs
start "" "http://127.0.0.1:8000/health"
start "" "http://127.0.0.1:8000/docs"
start "" "http://127.0.0.1:5173/index.html"

echo [DONE] 已尝试启动后端(8000) + 前端(5173)。如有报错，把新窗口里的红字复制给我。
pause
