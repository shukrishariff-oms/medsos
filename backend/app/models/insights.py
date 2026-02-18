from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class InsightsSnapshot(Base):
    __tablename__ = "insights_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    threads_media_id = Column(String, index=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    replies = Column(Integer, default=0)
    reposts = Column(Integer, default=0)
    quotes = Column(Integer, default=0)
    captured_at = Column(DateTime(timezone=True), server_default=func.now())
