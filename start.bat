@echo off
title PCB Component and Circuit Copilot - Launcher
echo ========================================================
echo        PCB Component and Circuit Copilot Launcher
echo ========================================================

set "HF_HOME=E:\hf_cache"
set "OLLAMA_MODELS=E:\Ollama\models"
set "YOLO_CACHE=E:\yolo_cache"

set "PROJECT_DIR=%~dp0"
set "UVICORN_EXE=%PROJECT_DIR%..\cs2-tactical-copilot\.venv\Scripts\uvicorn.exe"
set "STREAMLIT_EXE=%PROJECT_DIR%..\cs2-tactical-copilot\.venv\Scripts\streamlit.exe"
set "OLLAMA_EXE=E:\Ollama\ollama.exe"

echo [1/3] Checking Ollama daemon...
if exist "%OLLAMA_EXE%" (
    start "Ollama Engine" /B "%OLLAMA_EXE%" serve
) else (
    echo Ollama binary not found at %OLLAMA_EXE%, trying system PATH...
    start "Ollama Engine" /B ollama serve
)

ping 127.0.0.1 -n 2 >nul

echo [2/3] Starting FastAPI Backend (Port 8000)...
pushd "%PROJECT_DIR%backend"
set "PYTHONPATH=%CD%"
start "FastAPI Backend" "%UVICORN_EXE%" app.main:app --host 127.0.0.1 --port 8000 --reload
popd

ping 127.0.0.1 -n 4 >nul

echo [3/3] Starting Streamlit Frontend (Port 8501)...
pushd "%PROJECT_DIR%frontend"
start "Streamlit Frontend" "%STREAMLIT_EXE%" run app.py --server.port 8501
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
