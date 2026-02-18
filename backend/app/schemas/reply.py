from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReplyBase(BaseModel):
    text: str
    parent_media_id: str
    author: Optional[str] = None

class ReplyCreate(ReplyBase):
    pass

class Reply(ReplyBase):
    id: int
    threads_reply_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
