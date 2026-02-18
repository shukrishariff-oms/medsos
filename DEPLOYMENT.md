# ThreadOS Production Deployment Guide

## 1. Environment Setup

### Backend (.env)
Create `backend/.env` on the server with production values:
```ini
APP_ENV=production
FRONTEND_URL=https://tangger.ohmaishoot.com
THREADS_REDIRECT_URI=https://tangger.ohmaishoot.com/api/auth/threads/callback
THREADS_CLIENT_ID=your_prod_client_id
THREADS_CLIENT_SECRET=your_prod_client_secret
```

### Frontend (.env.production)
Ensure `frontend/.env.production` exists and contains:
```ini
VITE_API_BASE=/api
```

## 2. Build & Run

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --port 8001 --host 127.0.0.1
# Recommended: Use supervisor or systemd to keep it running
```

### Frontend
```bash
cd frontend
npm install
npm run build
# Dist files will be in frontend/dist
```

## 3. Nginx Configuration
1. Install Nginx: `sudo apt install nginx`
2. specific config: Copy `nginx.conf.example` content to `/etc/nginx/sites-available/tangger`.
3. Update SSL paths in the config.
4. Enable site: `sudo ln -s /etc/nginx/sites-available/tangger /etc/nginx/sites-enabled/`
5. Test & Reload: `sudo nginx -t && sudo systemctl reload nginx`

## 4. Verification
- Visit `https://tangger.ohmaishoot.com`
- Check API health: `https://tangger.ohmaishoot.com/api/docs`
- Test Login Flow.
