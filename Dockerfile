# --- STAGE 1: Build Frontend ---
FROM node:18-alpine AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend ./
# Bake in the API URL for production
ENV VITE_API_BASE=/api
RUN npm run build

# --- STAGE 2: Build Backend & Serve ---
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (including curl for healthchecks)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./

# Copy built frontend assets from Stage 1 to backend static folder
# FastAPI will serve these from /app/app/static
COPY --from=frontend-build /frontend/dist /app/app/static

# Create storage directory with loose permissions to avoid permission issues
RUN mkdir -p /app/storage && chmod -R 777 /app/storage

# Set working directory to backend root for easier imports
WORKDIR /app

# Expose port 8000 (Standard)
EXPOSE 8000

# Simple entrypoint to migrate and run
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
