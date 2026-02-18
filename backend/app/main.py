from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, threads, jobs

app = FastAPI(title="ThreadOS API", version="1.0.0")

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

app.include_router(auth.router)
app.include_router(threads.router)
app.include_router(jobs.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "env": settings.APP_ENV}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
