@echo off
REM Quick start backend server with new structure
echo Starting Quantum Image Retrieval Backend...
echo.
echo Server will run on: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
cd /d %~dp0
python main.py
pause
