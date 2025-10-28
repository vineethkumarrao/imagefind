@echo off
echo ================================
echo Quantum Image Retrieval - Setup
echo ================================
echo.

echo Step 1: Checking dependencies...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python first.
    pause
    exit /b 1
)

echo Step 2: Installing backend dependencies...
pip install -r requirements.txt

echo.
echo Step 3: Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo NEXT STEPS:
echo.
echo 1. Get your Cloudinary API Secret from:
echo    https://console.cloudinary.com/settings/security
echo.
echo 2. Update .env file with your API secret
echo.
echo 3. Run: python setup_cloudinary_pinecone.py
echo.
echo 4. Run: python test_upload.py (optional test)
echo.
echo 5. Start backend: python backend_server.py
echo.
echo 6. Start frontend: cd frontend ^&^& npm run dev
echo.
echo See SETUP_INSTRUCTIONS.md for detailed guide
echo.
pause
