from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    threads_user_id = Column(String, unique=True, index=True)
    username = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tokens = relationship("Token", back_populates="account")

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    access_token = Column(String)
    scopes = Column(String)
    expires_at = Column(DateTime(timezone=True), nullable=True) # Long-lived tokens might expire
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("Account", back_populates="tokens")
