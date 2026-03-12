from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联播放记录
    histories = relationship("PlayHistory", back_populates="user", cascade="all, delete-orphan")


class PlayHistory(Base):
    __tablename__ = "play_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    video_url = Column(String(500), nullable=False)
    video_name = Column(String(200), nullable=True)
    video_format = Column(String(20), default="mp4")
    current_time = Column(Float, default=0)  # 播放进度（秒）
    duration = Column(Float, default=0)  # 视频总时长（秒）
    is_local = Column(Integer, default=0)  # 0: 在线视频, 1: 本地视频
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联用户
    user = relationship("User", back_populates="histories")
    
    # 创建复合索引，用于查询用户的播放记录并去重
    __table_args__ = (
        Index('idx_user_video', 'user_id', 'video_url', unique=True),
    )
