import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str = "local"
    DATABASE_URL: str = "sqlite:///../storage/app.db"
    
    # App URLs
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Threads API
    THREADS_GRAPH_BASE: str = "https://graph.threads.net"
    THREADS_CLIENT_ID: str = ""
    THREADS_CLIENT_SECRET: str = ""
    THREADS_REDIRECT_URI: str = "http://localhost:8001/auth/threads/callback"
    THREADS_SCOPES: str = "threads_basic,threads_content_publish,threads_delete,threads_read_replies,threads_manage_replies,threads_manage_insights"
    
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        env_file_encoding='utf-8',
        extra='ignore'
    )

    def get_scopes_list(self) -> List[str]:
        return [s.strip() for s in self.THREADS_SCOPES.split(",") if s.strip()]

settings = Settings()
