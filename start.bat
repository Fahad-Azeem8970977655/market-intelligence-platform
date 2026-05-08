@echo off
title Market Intelligence Platform

echo ================================================
echo   Real-Time Market Intelligence Platform
echo ================================================

:: Copy env if missing
if not exist .env (
    copy .env.example .env
    echo Created .env - please add your API keys
)

:: Create venv if missing
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

:: Start Flask API
echo Starting Flask API on http://localhost:5000 ...
start "MarketIntel API" python backend/app.py
timeout /t 3 /nobreak >nul

:: Start Streamlit
echo Starting Streamlit on http://localhost:8501 ...
echo.
echo ================================================
echo   Dashboard: http://localhost:8501
echo   API:       http://localhost:5000/api/health
echo ================================================
echo.
streamlit run frontend/streamlit_app.py --server.port 8501

pause
