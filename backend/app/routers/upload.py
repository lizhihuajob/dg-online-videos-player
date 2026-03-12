from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
import uuid
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user
from app.config import UPLOAD_DIR, ALLOWED_VIDEO_EXTENSIONS, MAX_FILE_SIZE

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/video", response_model=schemas.UploadedVideoResponse)
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
        play_url = f"/api/videos/{db_video.id}"

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


@router.get("/videos", response_model=List[schemas.UploadedVideoResponse])
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
            play_url=f"/api/videos/{video.id}",
            created_at=video.created_at.isoformat() if video.created_at else ""
        ))
    return response


@router.delete("/videos/{video_id}")
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
