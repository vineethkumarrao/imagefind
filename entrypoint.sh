#!/bin/bash
# Docker entrypoint script to run both services

echo "Starting ImageCheck Application..."
echo "=================================="

# Export environment variables
export PYTHONUNBUFFERED=1

# Start backend
echo "Starting Backend Server..."
python -m backend.backend_server &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend static server
echo "Starting Frontend Server..."
python -m http.server 5000 --directory frontend/dist &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

echo "Services stopped"
