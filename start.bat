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

:: 2. Start Ollama Engine
echo [1/3] Starting Ollama Engine...
if exist "E:\Ollama\ollama.exe" (
    start "Ollama Engine" /B "E:\Ollama\ollama.exe" serve
) else (
    start "Ollama Engine" /B ollama serve
)

ping 127.0.0.1 -n 2 >nul

:: 3. Start FastAPI Backend (Port 8000)
echo [2/3] Starting FastAPI Backend (Port 8000)...
:: Free ports if left open from previous sessions
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1

pushd "%PROJECT_DIR%backend"
set "PYTHONPATH=%CD%"
start "FastAPI Backend" cmd /k ""%UVICORN_EXE%" app.main:app --host 127.0.0.1 --port 8000"
popd

:: Wait for FastAPI to finish pre-warming ChromaDB before launching the UI
"%PYTHON_EXE%" "%PROJECT_DIR%backend\wait_for_backend.py"

:: 4. Start Streamlit Frontend (Port 8501)
echo [3/3] Starting Streamlit Frontend (Port 8501)...
pushd "%PROJECT_DIR%frontend"
start "Streamlit Frontend" cmd /k ""%STREAMLIT_EXE%" run app.py --server.port 8501"
popd

ping 127.0.0.1 -n 2 >nul

echo.
echo Launching Web Browser at http://localhost:8501 ...
start http://localhost:8501

echo.
echo ========================================================
echo All services launched!
echo - Backend API Docs: http://127.0.0.1:8000/docs
echo - Frontend HUD:     http://localhost:8501
echo ========================================================
