# Multi-stage build for frontend and backend
# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Build backend and runtime
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create necessary directories
RUN mkdir -p /app/data/uploads

# Expose ports
EXPOSE 8000 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start both services
CMD ["sh", "-c", "python -m backend.backend_server & python -m http.server 5000 --directory frontend/dist"]
