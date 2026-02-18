from sqlalchemy.orm import Session
from app.models.post import Post
from typing import List, Optional
from datetime import datetime

class PostService:
    def __init__(self, db: Session):
        self.db = db

    def list_posts(self, limit: int = 10) -> List[Post]:
        return self.db.query(Post).order_by(Post.created_at.desc()).limit(limit).all()

    def create_post_record(self, text: str, status: str = "PENDING") -> Post:
        db_post = Post(text=text, status=status)
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post

    def mark_published(self, id: int, media_id: str) -> Post:
        post = self.db.query(Post).filter(Post.id == id).first()
        if post:
            post.status = "PUBLISHED"
            post.threads_media_id = media_id
            self.db.commit()
            self.db.refresh(post)
        return post

    def mark_failed(self, id: int, message: str) -> Post:
        post = self.db.query(Post).filter(Post.id == id).first()
        if post:
            post.status = "FAILED"
            post.error_message = message
            self.db.commit()
            self.db.refresh(post)
        return post

    def mark_deleted_by_media_id(self, media_id: str) -> Optional[Post]:
        post = self.db.query(Post).filter(Post.threads_media_id == media_id).first()
        if post:
            post.status = "DELETED"
            self.db.commit()
            self.db.refresh(post)
        return post
