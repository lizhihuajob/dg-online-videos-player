from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models, schemas
from app.security import get_current_active_user

router = APIRouter()


@router.get("/list", response_model=schemas.PlayHistoryList)
def get_history_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """获取当前用户的播放记录列表"""
    # 查询用户的播放记录，按更新时间倒序
    histories = db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id
    ).order_by(
        models.PlayHistory.updated_at.desc()
    ).offset(skip).limit(limit).all()
    
    # 获取总数
    total = db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id
    ).count()
    
    return {
        "items": histories,
        "total": total
    }


@router.post("/save", response_model=schemas.PlayHistoryResponse)
def save_history(
    history_data: schemas.PlayHistoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """保存或更新播放记录"""
    # 检查是否已存在相同的视频记录
    existing_history = db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id,
        models.PlayHistory.video_url == history_data.video_url
    ).first()
    
    if existing_history:
        # 更新现有记录
        existing_history.video_name = history_data.video_name
        existing_history.video_format = history_data.video_format
        existing_history.current_time = history_data.current_time
        existing_history.duration = history_data.duration
        existing_history.is_local = history_data.is_local
        db.commit()
        db.refresh(existing_history)
        return existing_history
    else:
        # 创建新记录
        new_history = models.PlayHistory(
            user_id=current_user.id,
            video_url=history_data.video_url,
            video_name=history_data.video_name,
            video_format=history_data.video_format,
            current_time=history_data.current_time,
            duration=history_data.duration,
            is_local=history_data.is_local
        )
        db.add(new_history)
        db.commit()
        db.refresh(new_history)
        return new_history


@router.put("/update/{history_id}", response_model=schemas.PlayHistoryResponse)
def update_history(
    history_id: int,
    history_data: schemas.PlayHistoryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """更新播放进度"""
    history = db.query(models.PlayHistory).filter(
        models.PlayHistory.id == history_id,
        models.PlayHistory.user_id == current_user.id
    ).first()
    
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="播放记录不存在"
        )
    
    history.current_time = history_data.current_time
    if history_data.duration is not None:
        history.duration = history_data.duration
    
    db.commit()
    db.refresh(history)
    return history


@router.delete("/delete/{history_id}")
def delete_history(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """删除单条播放记录"""
    history = db.query(models.PlayHistory).filter(
        models.PlayHistory.id == history_id,
        models.PlayHistory.user_id == current_user.id
    ).first()
    
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="播放记录不存在"
        )
    
    db.delete(history)
    db.commit()
    
    return {"message": "删除成功"}


@router.delete("/clear")
def clear_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """清空当前用户的所有播放记录"""
    db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id
    ).delete()
    db.commit()
    
    return {"message": "播放记录已清空"}


@router.get("/check", response_model=Optional[schemas.PlayHistoryResponse])
def check_history(
    video_url: str = Query(..., description="视频URL"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """检查某个视频是否有播放记录"""
    history = db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id,
        models.PlayHistory.video_url == video_url
    ).first()
    
    return history
