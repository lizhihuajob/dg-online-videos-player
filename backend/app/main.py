from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
from app import models, schemas
from app.database import engine, get_db
from app.auth import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.dependencies import get_current_user
from app.config import UPLOAD_DIR, ALLOWED_VIDEO_EXTENSIONS, MAX_FILE_SIZE
import os

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Video Player API")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 认证相关API ==========

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }


# ========== 在线视频历史记录API ==========

@app.post("/history", response_model=schemas.PlayHistoryResponse)
def add_play_history(
    history: schemas.PlayHistoryCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id,
        models.PlayHistory.video_url == history.video_url
    ).first()

    if existing:
        db.delete(existing)
        db.commit()

    new_history = models.PlayHistory(
        user_id=current_user.id,
        video_url=history.video_url,
        video_name=history.video_name,
        video_format=history.video_format
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)

    response = schemas.PlayHistoryResponse(
        id=new_history.id,
        video_url=new_history.video_url,
        video_name=new_history.video_name,
        video_format=new_history.video_format,
        created_at=new_history.created_at.isoformat() if new_history.created_at else ""
    )
    return response


@app.get("/history", response_model=List[schemas.PlayHistoryResponse])
def get_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id
    ).order_by(models.PlayHistory.created_at.desc()).limit(10).all()

    response = []
    for item in history:
        response.append(schemas.PlayHistoryResponse(
            id=item.id,
            video_url=item.video_url,
            video_name=item.video_name,
            video_format=item.video_format,
            created_at=item.created_at.isoformat() if item.created_at else ""
        ))
    return response


@app.delete("/history/{history_id}")
def delete_play_history(
    history_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(models.PlayHistory).filter(
        models.PlayHistory.id == history_id,
        models.PlayHistory.user_id == current_user.id
    ).first()

    if not history:
        raise HTTPException(status_code=404, detail="History item not found")

    db.delete(history)
    db.commit()
    return {"message": "History item deleted successfully"}


@app.delete("/history")
def clear_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id
    ).delete()
    db.commit()
    return {"message": "All history cleared successfully"}


# ========== 本地视频历史记录API ==========

@app.post("/local-history", response_model=schemas.LocalPlayHistoryResponse)
def add_local_play_history(
    history: schemas.LocalPlayHistoryCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(models.LocalPlayHistory).filter(
        models.LocalPlayHistory.user_id == current_user.id,
        models.LocalPlayHistory.video_name == history.video_name
    ).first()

    if existing:
        db.delete(existing)
        db.commit()

    new_history = models.LocalPlayHistory(
        user_id=current_user.id,
        video_name=history.video_name,
        video_format=history.video_format,
        file_info=history.file_info
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)

    response = schemas.LocalPlayHistoryResponse(
        id=new_history.id,
        video_name=new_history.video_name,
        video_format=new_history.video_format,
        file_info=new_history.file_info,
        created_at=new_history.created_at.isoformat() if new_history.created_at else ""
    )
    return response


@app.get("/local-history", response_model=List[schemas.LocalPlayHistoryResponse])
def get_local_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(models.LocalPlayHistory).filter(
        models.LocalPlayHistory.user_id == current_user.id
    ).order_by(models.LocalPlayHistory.created_at.desc()).limit(10).all()

    response = []
    for item in history:
        response.append(schemas.LocalPlayHistoryResponse(
            id=item.id,
            video_name=item.video_name,
            video_format=item.video_format,
            file_info=item.file_info,
            created_at=item.created_at.isoformat() if item.created_at else ""
        ))
    return response


@app.delete("/local-history/{history_id}")
def delete_local_play_history(
    history_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(models.LocalPlayHistory).filter(
        models.LocalPlayHistory.id == history_id,
        models.LocalPlayHistory.user_id == current_user.id
    ).first()

    if not history:
        raise HTTPException(status_code=404, detail="History item not found")

    db.delete(history)
    db.commit()
    return {"message": "Local history item deleted successfully"}


@app.delete("/local-history")
def clear_local_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(models.LocalPlayHistory).filter(
        models.LocalPlayHistory.user_id == current_user.id
    ).delete()
    db.commit()
    return {"message": "All local history cleared successfully"}


# ========== 视频上传API ==========

import shutil
import uuid
from fastapi.responses import FileResponse


@app.post("/upload/video", response_model=schemas.UploadedVideoResponse)
async def upload_video(
    video: UploadFile = File(...),
    video_name: str = Form(""),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传视频文件到服务器"""
    # 检查文件扩展名
    file_ext = os.path.splitext(video.filename)[1].lower()
    if file_ext not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式。支持的格式: {', '.join(ALLOWED_VIDEO_EXTENSIONS)}"
        )

    # 生成唯一文件名
    unique_id = str(uuid.uuid4())
    stored_filename = f"{unique_id}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, stored_filename)

    try:
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        # 获取文件大小
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="文件大小超过限制（最大500MB）")

        # 保存到数据库
        db_video = models.UploadedVideo(
            user_id=current_user.id,
            video_name=video_name or video.filename,
            video_format=file_ext[1:],  # 去掉点号
            file_path=file_path,
            file_size=file_size
        )
        db.add(db_video)
        db.commit()
        db.refresh(db_video)

        # 构建播放URL
        play_url = f"/videos/{db_video.id}"

        return schemas.UploadedVideoResponse(
            id=db_video.id,
            video_name=db_video.video_name,
            video_format=db_video.video_format,
            file_size=db_video.file_size,
            play_url=play_url,
            created_at=db_video.created_at.isoformat() if db_video.created_at else ""
        )

    except Exception as e:
        # 清理已保存的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


@app.get("/upload/videos", response_model=List[schemas.UploadedVideoResponse])
def get_uploaded_videos(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户上传的视频列表"""
    videos = db.query(models.UploadedVideo).filter(
        models.UploadedVideo.user_id == current_user.id
    ).order_by(models.UploadedVideo.created_at.desc()).all()

    response = []
    for video in videos:
        response.append(schemas.UploadedVideoResponse(
            id=video.id,
            video_name=video.video_name,
            video_format=video.video_format,
            file_size=video.file_size,
            play_url=f"/videos/{video.id}",
            created_at=video.created_at.isoformat() if video.created_at else ""
        ))
    return response


@app.delete("/upload/videos/{video_id}")
def delete_uploaded_video(
    video_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除上传的视频"""
    video = db.query(models.UploadedVideo).filter(
        models.UploadedVideo.id == video_id,
        models.UploadedVideo.user_id == current_user.id
    ).first()

    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")

    # 删除物理文件
    if os.path.exists(video.file_path):
        os.remove(video.file_path)

    # 删除数据库记录
    db.delete(video)
    db.commit()

    return {"message": "视频删除成功"}


# ========== 视频播放API ==========

@app.get("/videos/{video_id}")
def get_video(
    video_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取上传的视频文件"""
    video = db.query(models.UploadedVideo).filter(
        models.UploadedVideo.id == video_id,
        models.UploadedVideo.user_id == current_user.id
    ).first()

    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")

    if not os.path.exists(video.file_path):
        raise HTTPException(status_code=404, detail="视频文件不存在")

    # 根据文件扩展名设置正确的media type
    media_type_map = {
        'mp4': 'video/mp4',
        'webm': 'video/webm',
        'mov': 'video/quicktime',
        'avi': 'video/x-msvideo',
        'mkv': 'video/x-matroska',
        'flv': 'video/x-flv'
    }
    media_type = media_type_map.get(video.video_format, 'video/mp4')

    return FileResponse(
        video.file_path,
        media_type=media_type,
        filename=video.video_name
    )


@app.get("/")
def root():
    return {"message": "Video Player API is running"}
