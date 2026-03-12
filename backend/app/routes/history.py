from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.models import User, PlayHistory
from ..schemas.schemas import PlayHistoryCreate, PlayHistoryResponse, MessageResponse
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/history", tags=["播放记录"])


@router.get("/", response_model=List[PlayHistoryResponse])
def get_play_history(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(PlayHistory).filter(
        PlayHistory.user_id == current_user.id
    ).order_by(PlayHistory.created_at.desc()).limit(limit).all()
    
    return history


@router.post("/", response_model=PlayHistoryResponse, status_code=status.HTTP_201_CREATED)
def add_play_history(
    history_data: PlayHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(PlayHistory).filter(
        PlayHistory.user_id == current_user.id,
        PlayHistory.video_url == history_data.video_url
    ).first()
    
    if existing:
        db.delete(existing)
    
    new_history = PlayHistory(
        user_id=current_user.id,
        video_url=history_data.video_url,
        video_name=history_data.video_name,
        video_format=history_data.video_format,
        is_local=history_data.is_local
    )
    
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    
    return new_history


@router.delete("/{history_id}", response_model=MessageResponse)
def delete_play_history(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history_item = db.query(PlayHistory).filter(
        PlayHistory.id == history_id,
        PlayHistory.user_id == current_user.id
    ).first()
    
    if not history_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="播放记录不存在"
        )
    
    db.delete(history_item)
    db.commit()
    
    return {"message": "删除成功"}


@router.delete("/", response_model=MessageResponse)
def clear_play_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(PlayHistory).filter(PlayHistory.user_id == current_user.id).delete()
    db.commit()
    
    return {"message": "已清除所有播放记录"}
