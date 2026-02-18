FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Set API base URL for production build
ENV VITE_API_BASE=/api

RUN npm run build

# Stage 2: Minimal image to just verify or hold assets (optional, usually we just copy from builder in compose)
# But for this compose setup, we will use a scratch container or busybox to hold the volume
# Actually, we can just use this builder image in docker-compose to copy files to volume
CMD ["echo", "Frontend build complete"]
