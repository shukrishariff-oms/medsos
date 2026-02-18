from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, threads, jobs

app = FastAPI(title="ThreadOS API", version="1.0.0")
print("🔥 FORCE REDEPLOY: BACKEND V3 STARTED 🔥")

# CORS Configuration
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://localhost:5177",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(threads.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "env": settings.APP_ENV}

# --- UNIFIED DEPLOYMENT: Serve React Static Files ---
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Path where the built frontend will be mounted in the Docker container
static_dir = os.path.join(os.path.dirname(__file__), "static")

# Only serve static files if the directory exists (Production mode)
if os.path.exists(static_dir):
    # Mount assets (JS, CSS, Images)
    # Vite builds to /assets by default
    assets_dir = os.path.join(static_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    # Catch-all route for SPA (React Router)
    # This must be LAST so it doesn't override API routes
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Allow API calls to pass through (returns 404 if not found above)
        if full_path.startswith("api"):
             return {"error": "API route not found"}
        
        # Check if a specific file exists (e.g., favicon.ico, logo.png)
        file_path = os.path.join(static_dir, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        
        # Otherwise, serve index.html for React Router handling
        return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
