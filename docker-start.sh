#!/bin/bash
# Docker Quick Start Script for ImageCheck
# This script builds and runs the Docker container with a single command

echo ""
echo "========================================"
echo "ImageCheck Docker Startup Script"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    echo "Please install Docker from https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "[*] Docker found"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "ERROR: Docker Compose is not installed"
    echo "Please install Docker Desktop which includes Docker Compose"
    exit 1
fi

echo "[*] Docker Compose found"
echo ""

# Display menu
echo "Select an option:"
echo "1 - Start with docker-compose up"
echo "2 - Rebuild and start (docker-compose up --build)"
echo "3 - Stop all containers (docker-compose down)"
echo "4 - View logs (docker-compose logs -f)"
echo "5 - Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "[*] Starting Docker containers..."
        docker-compose up
        ;;
    2)
        echo ""
        echo "[*] Rebuilding and starting Docker containers..."
        docker-compose up --build
        ;;
    3)
        echo ""
        echo "[*] Stopping all containers..."
        docker-compose down
        echo "[+] Containers stopped"
        ;;
    4)
        echo ""
        echo "[*] Showing logs (Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
    5)
        echo "[*] Exiting..."
        exit 0
        ;;
    *)
        echo "ERROR: Invalid choice"
        exit 1
        ;;
esac
