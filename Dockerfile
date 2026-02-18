# ==========================================
# STAGE 1: Build Frontend (Node.js)
# ==========================================
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
# Production build
# Ensure API calls go to relative path /api (proxied by FastAPI or Nginx if strictly needed, 
# but here FastAPI serves /api directly).
# In Unified mode, the same domain serves both, so relative path is fine.
ENV VITE_API_BASE=/api
RUN npm run build

# ==========================================
# STAGE 2: Build Backend & Serve (Python)
# ==========================================
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend Code
COPY backend/ .

# Copy Frontend Build Artifacts to Backend Static Folder
# We place them in app/static so uvicorn can serve them
COPY --from=frontend-builder /app/frontend/dist /app/app/static

# Ensure storage directory exists and has write permissions
RUN mkdir -p /app/storage/backups && chmod -R 777 /app/storage

EXPOSE 8000

# Entrypoint script
COPY <<EOF /app/entrypoint.sh
#!/bin/bash
set -e

# Robustness: ensure permissions at runtime
echo "Ensuring storage permissions..."
mkdir -p /app/storage/backups
touch /app/storage/app.db
chmod -R 777 /app/storage

echo "Running database migrations..."
alembic upgrade head

echo "Starting Unified Server (FastAPI + React)..."
# Host 0.0.0.0 is crucial for Docker
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
EOF

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
