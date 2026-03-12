from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from app import models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/videos", tags=["videos"])

@router.get("/{video_id}")
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
