from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountBase(BaseModel):
    threads_user_id: str
    username: str

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenBase(BaseModel):
    access_token: str
    scopes: str
    expires_at: Optional[datetime] = None

class TokenCreate(TokenBase):
    account_id: int

class Token(TokenBase):
    id: int
    account_id: int
    created_at: datetime

    class Config:
        from_attributes = True
