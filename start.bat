@echo off
title PCB Component & Circuit Copilot - Launcher
echo ========================================================
echo        PCB Component & Circuit Copilot Launcher
echo ========================================================

set "HF_HOME=E:\hf_cache"
set "OLLAMA_MODELS=E:\Ollama\models"
set "YOLO_CACHE=E:\yolo_cache"
set "PROJECT_DIR=%~dp0"
set "PYTHON_EXE=%PROJECT_DIR%..\cs2-tactical-copilot\.venv\Scripts\python.exe"

echo [1/3] Checking Ollama daemon...
start "Ollama Engine" /B "E:\Ollama\ollama.exe" serve

echo [2/3] Starting FastAPI Backend (Port 8000)...
start "FastAPI Backend" cmd /k "cd /d %PROJECT_DIR%backend && set PYTHONPATH=%PROJECT_DIR%backend && set HF_HOME=E:\hf_cache && %PROJECT_DIR%..\cs2-tactical-copilot\.venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo [3/3] Starting Streamlit Frontend (Port 8501)...
start "Streamlit Frontend" cmd /k "cd /d %PROJECT_DIR%frontend && %PROJECT_DIR%..\cs2-tactical-copilot\.venv\Scripts\streamlit.exe run app.py --server.port 8501"

echo.
echo All services launched!
echo - Backend API Docs: http://127.0.0.1:8000/docs
echo - Frontend HUD:     http://127.0.0.1:8501
echo ========================================================
