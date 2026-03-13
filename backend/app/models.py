from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    avatar = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    play_history = relationship("PlayHistory", back_populates="user", cascade="all, delete-orphan")
    local_play_history = relationship("LocalPlayHistory", back_populates="user", cascade="all, delete-orphan")
    play_logs = relationship("PlayLog", back_populates="user", cascade="all, delete-orphan")


class PlayHistory(Base):
    __tablename__ = "play_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_url = Column(Text)
    video_name = Column(String(255))
    video_format = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="play_history")


class LocalPlayHistory(Base):
    __tablename__ = "local_play_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_name = Column(String(255))
    video_format = Column(String(10))
    file_info = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="local_play_history")


class PlayLog(Base):
    __tablename__ = "play_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_name = Column(String(255))
    video_url = Column(Text, nullable=True)
    video_format = Column(String(10))
    play_time = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="play_logs")
