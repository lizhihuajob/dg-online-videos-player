from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ==================== 用户相关Schema ====================

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(UserBase):
    password: str = Field(..., min_length=1)


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Token相关Schema ====================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenPayload(BaseModel):
    sub: Optional[int] = None


# ==================== 播放记录相关Schema ====================

class PlayHistoryBase(BaseModel):
    video_url: str = Field(..., max_length=500)
    video_name: Optional[str] = Field(None, max_length=200)
    video_format: str = Field(default="mp4", max_length=20)
    current_time: float = Field(default=0, ge=0)
    duration: float = Field(default=0, ge=0)
    is_local: int = Field(default=0, ge=0, le=1)


class PlayHistoryCreate(PlayHistoryBase):
    pass


class PlayHistoryUpdate(BaseModel):
    current_time: float = Field(..., ge=0)
    duration: Optional[float] = Field(None, ge=0)


class PlayHistoryResponse(PlayHistoryBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PlayHistoryList(BaseModel):
    items: List[PlayHistoryResponse]
    total: int
