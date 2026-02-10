@echo off
:: 强制使用 UTF-8 编码防止中文乱码
chcp 65001 > nul

echo [Research OS] 正在初始化环境...

:: 检查 Python 3.12 是否安装
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python 3.12，请先安装 Python 3.12。
    echo 访问 https://www.python.org/downloads/windows/ 下载。
    pause
    exit /b
)

:: 创建并激活虚拟环境
if not exist .venv (
    echo [Research OS] 正在创建虚拟环境 (Python 3.12)...
    py -3.12 -m venv .venv
)

echo [Research OS] 正在激活虚拟环境...
call .venv\Scripts\activate

:: 安装依赖
echo [Research OS] 正在检查依赖更新...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: 启动后端 (后台运行)
echo [Research OS] 正在启动后端服务 (Port 8000)...
start /b uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload

:: 启动前端 (使用 Python 内置服务器)
echo [Research OS] 正在启动前端界面 (Port 5173)...
echo 访问地址: http://localhost:5173
cd frontend && python -m http.server 5173
