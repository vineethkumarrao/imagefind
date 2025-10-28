# Quick start guide for running ImageCheck with Docker

## Prerequisites
- Docker installed and running
- Docker Compose installed (comes with Docker Desktop)

## Quick Start - Single Command

### Option 1: Using Docker Compose (Recommended)
```bash
docker-compose up
```

This will:
1. Build the Docker image (first time only)
2. Start the backend on `http://localhost:8000`
3. Start the frontend on `http://localhost:5000`
4. Mount the uploads directory for persistence

### Option 2: Using Docker CLI
```bash
docker build -t imagecheck:latest .
docker run -p 8000:8000 -p 5000:5000 \
  -e CLOUDINARY_CLOUD_NAME=ddyytqwbq \
  -e CLOUDINARY_API_KEY=315439667751671 \
  -e CLOUDINARY_API_SECRET=J9F8TguFx9Xw9TgCyLAamS2jGF0 \
  -e PINECONE_API_KEY=pcsk_6ymDQY_CpQG5yUj1BpjFYuD1g9KyuMFzebjbP1zvYXZ1v2jM7JLnevcgeLRbJTUGZxQqAM \
  -e PINECONE_ENVIRONMENT=us-east-1 \
  -e PINECONE_INDEX_NAME=quantum-images-prod \
  imagecheck:latest
```

## Access Points

- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Useful Commands

### Stop the application
```bash
docker-compose down
```

### Rebuild the image
```bash
docker-compose up --build
```

### View logs
```bash
docker-compose logs -f
```

### Run with specific environment file
```bash
docker-compose --env-file .env.production up
```

### Scale services (development)
```bash
docker-compose up --scale backend=2
```

## Environment Variables

All environment variables are pre-configured in `docker-compose.yml`:
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`
- `PINECONE_API_KEY`
- `PINECONE_ENVIRONMENT`
- `PINECONE_INDEX_NAME`

To use different values, create a `.env` file or modify `docker-compose.yml`.

## Troubleshooting

### Port already in use
```bash
# Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>

# For Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Build issues
```bash
docker-compose down --rmi all
docker-compose up --build
```

### View real-time logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Directory Structure Inside Container

```
/app
├── backend/
│   └── backend_server.py
├── frontend/
│   └── dist/              (built frontend files)
├── services/
├── ml/
├── config.py
└── requirements.txt
```

## Performance Notes

- First build takes 3-5 minutes (installing dependencies)
- Subsequent builds are much faster (cached layers)
- Container uses ~2GB RAM when running with ML models
- Frontend is served as static files (built with Vite)

## Production Deployment

For production, consider:
1. Using separate containers for frontend (nginx) and backend
2. Adding a reverse proxy (nginx/traefik)
3. Using environment-specific configs
4. Implementing proper logging and monitoring
5. Using Docker secrets for sensitive data
