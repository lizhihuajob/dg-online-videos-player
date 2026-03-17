from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    avatar_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    play_history = relationship("PlayHistory", back_populates="user", cascade="all, delete-orphan")
    local_play_history = relationship("LocalPlayHistory", back_populates="user", cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="user", cascade="all, delete-orphan")
    groups = relationship("Group", back_populates="user", cascade="all, delete-orphan")


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
    file_info = Column(Text)  # JSON string storing file info (name, size, type, lastModified)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="local_play_history")


class Group(Base):
    """分组/合集模型"""
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)  # 分组名称
    description = Column(Text, nullable=True)  # 分组描述
    group_type = Column(String(20), nullable=False, default="video")  # 分组类型: video, music
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="groups")
    videos = relationship("Video", back_populates="group")


class Video(Base):
    """用户上传的视频/音乐模型"""
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)  # 所属分组
    filename = Column(String(255), nullable=False)  # 存储的文件名
    original_name = Column(String(255), nullable=False)  # 原始文件名
    url = Column(String(255), nullable=False)  # 访问URL
    format = Column(String(10), nullable=False)  # 文件格式
    size = Column(BigInteger, default=0)  # 文件大小（字节）
    file_type = Column(String(20), nullable=False, default="video")  # 文件类型: video, music
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="videos")
    group = relationship("Group", back_populates="videos")
