@echo off
title PCB Component and Circuit Copilot - Launcher
echo ========================================================
echo        PCB Component and Circuit Copilot Launcher
echo ========================================================

set "PROJECT_DIR=%~dp0"

:: 1. Detect Python / Virtual Environment
set "VENV_BIN="
if exist "%PROJECT_DIR%.venv\Scripts\python.exe" (
    set "VENV_BIN=%PROJECT_DIR%.venv\Scripts"
    echo [*] Detected local project virtual environment: .venv
) else if exist "%PROJECT_DIR%..\cs2-tactical-copilot\.venv\Scripts\python.exe" (
    set "VENV_BIN=%PROJECT_DIR%..\cs2-tactical-copilot\.venv\Scripts"
    echo [*] Detected workspace virtual environment: cs2-tactical-copilot\.venv
) else (
    echo [*] Using system PATH Python environment
)

if defined VENV_BIN (
    set "UVICORN_EXE=%VENV_BIN%\uvicorn.exe"
    set "STREAMLIT_EXE=%VENV_BIN%\streamlit.exe"
    set "PYTHON_EXE=%VENV_BIN%\python.exe"
) else (
    set "UVICORN_EXE=uvicorn"
    set "STREAMLIT_EXE=streamlit"
    set "PYTHON_EXE=python"
)

:: 2. Optional Drive E: Cache Configuration
if exist "E:\hf_cache" (
    set "HF_HOME=E:\hf_cache"
)
if exist "E:\Ollama\models" (
    set "OLLAMA_MODELS=E:\Ollama\models"
)
if exist "E:\yolo_cache" (
    set "YOLO_CACHE=E:\yolo_cache"
)

:: 3. Start Ollama Engine
echo [1/3] Starting Ollama Engine...
if exist "E:\Ollama\ollama.exe" (
    start "Ollama Engine" /B "E:\Ollama\ollama.exe" serve
) else (
    start "Ollama Engine" /B ollama serve
)

ping 127.0.0.1 -n 2 >nul

:: 4. Start FastAPI Backend (Port 8000)
echo [2/3] Starting FastAPI Backend (Port 8000)...
pushd "%PROJECT_DIR%backend"
set "PYTHONPATH=%CD%"
start "FastAPI Backend" cmd /k ""%UVICORN_EXE%" app.main:app --host 127.0.0.1 --port 8000 --reload"
popd

echo [*] Waiting for FastAPI to pre-warm vector store and become ready...
"%PYTHON_EXE%" -c "import urllib.request, time; [print('[*] FastAPI Backend is ready!') or exit(0) for _ in range(30) if (time.sleep(1) or True) and (lambda: (urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=1).status == 200 if True else False))()]" 2>nul

:: 5. Start Streamlit Frontend (Port 8501)
echo [3/3] Starting Streamlit Frontend (Port 8501)...
pushd "%PROJECT_DIR%frontend"
start "Streamlit Frontend" cmd /k ""%STREAMLIT_EXE%" run app.py --server.port 8501"
popd

ping 127.0.0.1 -n 3 >nul

echo.
echo Launching Web Browser at http://localhost:8501 ...
start http://localhost:8501

echo.
echo ========================================================
echo All services launched!
echo - Backend API Docs: http://127.0.0.1:8000/docs
echo - Frontend HUD:     http://localhost:8501
echo ========================================================
