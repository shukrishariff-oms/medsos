from pydantic import BaseModel
from datetime import datetime

class InsightsSnapshotBase(BaseModel):
    threads_media_id: str
    views: int = 0
    likes: int = 0
    replies: int = 0
    reposts: int = 0
    quotes: int = 0

class InsightsSnapshotCreate(InsightsSnapshotBase):
    pass

class InsightsSnapshot(InsightsSnapshotBase):
    id: int
    captured_at: datetime

    class Config:
        from_attributes = True
