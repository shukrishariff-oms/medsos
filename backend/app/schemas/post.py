from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    text: str
    error_message: str | None = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    threads_media_id: Optional[str] = None
    status: str
    error_message: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
