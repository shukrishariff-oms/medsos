from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    threads_media_id = Column(String, unique=True, index=True, nullable=True) # Nullable until published
    text = Column(String)
    status = Column(String, default="PUBLISHED") # PUBLISHED, FAILED, DRAFT, DELETED
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
