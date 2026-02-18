FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Ensure storage directory exists and has write permissions (Build time)
RUN mkdir -p /app/storage/backups && chmod -R 777 /app/storage

# Expose port (Standard FastAPI port)
EXPOSE 8000

# Entrypoint script to run migrations then start app
COPY <<EOF /app/entrypoint.sh
#!/bin/bash
set -e

# Runtime permission fix (Robustness)
echo "Ensuring storage permissions..."
mkdir -p /app/storage/backups
touch /app/storage/app.db
chmod -R 777 /app/storage

echo "Running database migrations..."
alembic upgrade head

echo "Starting backend on port 8000..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
EOF

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
