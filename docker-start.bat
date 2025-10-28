@echo off
REM Docker Quick Start Script for ImageCheck
REM This script builds and runs the Docker container with a single command

echo.
echo ========================================
echo ImageCheck Docker Startup Script
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [*] Docker found
echo.

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose is not installed
    echo Please install Docker Desktop which includes Docker Compose
    pause
    exit /b 1
)

echo [*] Docker Compose found
echo.

REM Ask user what to do
echo Select an option:
echo 1 - Start with docker-compose up
echo 2 - Rebuild and start (docker-compose up --build)
echo 3 - Stop all containers (docker-compose down)
echo 4 - View logs (docker-compose logs -f)
echo 5 - Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo [*] Starting Docker containers...
    docker-compose up
) else if "%choice%"=="2" (
    echo.
    echo [*] Rebuilding and starting Docker containers...
    docker-compose up --build
) else if "%choice%"=="3" (
    echo.
    echo [*] Stopping all containers...
    docker-compose down
    echo [+] Containers stopped
) else if "%choice%"=="4" (
    echo.
    echo [*] Showing logs (Ctrl+C to exit)...
    docker-compose logs -f
) else if "%choice%"=="5" (
    echo [*] Exiting...
    exit /b 0
) else (
    echo ERROR: Invalid choice
    pause
    exit /b 1
)

pause
