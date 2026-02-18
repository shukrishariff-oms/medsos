from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, index=True)
    threads_reply_id = Column(String, unique=True, index=True, nullable=True)
    parent_media_id = Column(String, index=True) # ID of the post/reply being replied to
    text = Column(String)
    author = Column(String, nullable=True) # Username of who we replied to (optional context)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
