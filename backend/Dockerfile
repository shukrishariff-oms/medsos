FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for building wheels)
# RUN apt-get update && apt-get install -y gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Ensure storage directory exists
# Ensure storage directory exists and has write permissions
RUN mkdir -p /app/storage/backups && chmod -R 777 /app/storage

# Expose port
EXPOSE 8001

# Entrypoint script to run migrations then start app
COPY <<EOF /app/entrypoint.sh
#!/bin/bash
set -e
echo "Running database migrations..."
alembic upgrade head
echo "Starting backend..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8001
EOF

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
