@echo off
setlocal
set USE_VENV=1
set PYTHON_CMD=python

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 未安装或未加入 PATH
    pause
    exit /b 1
)

if not exist "venv" (
    echo 正在创建虚拟环境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo 虚拟环境创建失败，改用系统环境
        set USE_VENV=0
    )
)

if %USE_VENV%==1 (
    echo 正在激活虚拟环境...
    call venv\Scripts\activate
    if %errorlevel% neq 0 (
        echo 虚拟环境激活失败，改用系统环境
        set USE_VENV=0
    ) else (
        set PYTHON_CMD=venv\Scripts\python
    )
)

set REQ=requirements.txt
if not exist "%REQ%" set REQ=reference\requirements.txt
if not exist "%REQ%" (
    echo 未找到 requirements.txt 或 reference\requirements.txt
    pause
    exit /b 1
)

echo 正在安装依赖: %REQ%
%PYTHON_CMD% -m pip install -r "%REQ%"
if %errorlevel% neq 0 (
    echo 依赖安装失败，尝试按组件安装
    %PYTHON_CMD% -m pip install fastapi==0.109.0 uvicorn==0.27.0 python-dotenv==1.0.1 requests==2.31.0 pydantic==2.6.0 pydub==0.25.1
    if %errorlevel% neq 0 (
        echo 组件安装失败
        pause
        exit /b 1
    )
)

set PYTHONPATH=%CD%\huaweicloud-python-sdk-sis-1.8.5;%PYTHONPATH%

echo 正在启动服务...
%PYTHON_CMD% -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

pause
endlocal
