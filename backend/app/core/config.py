import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str = "local"
    DATABASE_URL: str = "sqlite:////app/storage/app.db"
    
    # Threads API
    THREADS_GRAPH_BASE: str = "https://graph.threads.net"
    THREADS_CLIENT_ID: str = ""
    THREADS_CLIENT_SECRET: str = ""
    THREADS_REDIRECT_URI: str = "http://localhost:8000/auth/threads/callback"
    THREADS_SCOPES: str = "threads_basic,threads_content_publish,threads_delete,threads_read_replies,threads_manage_replies,threads_manage_insights"
    
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        env_file_encoding='utf-8',
        extra='ignore'
    )

    def __init__(self, **data):
        super().__init__(**data)
        # Fix for Coolify/Docker environment where DATABASE_URL might be set to the old relative path
        if self.DATABASE_URL == "sqlite:///../storage/app.db" and os.path.exists("/app/storage"):
            # Force absolute path in Docker environment
            self.DATABASE_URL = "sqlite:////app/storage/app.db"

settings = Settings()
