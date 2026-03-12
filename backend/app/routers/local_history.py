from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from jose import JWTError, jwt
from ..database import get_db
from ..models import User, LocalPlayHistory
from ..auth import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/local-history", tags=["local-history"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LocalPlayHistoryCreate(BaseModel):
    video_name: str
    video_format: str
    file_info: str

class LocalPlayHistoryResponse(BaseModel):
    id: int
    video_name: str
    video_format: str
    file_info: str
    created_at: str

    class Config:
        from_attributes = True

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("", response_model=LocalPlayHistoryResponse)
def add_local_play_history(
    history: LocalPlayHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(LocalPlayHistory).filter(
        LocalPlayHistory.user_id == current_user.id,
        LocalPlayHistory.video_name == history.video_name
    ).first()

    if existing:
        db.delete(existing)
        db.commit()

    new_history = LocalPlayHistory(
        user_id=current_user.id,
        video_name=history.video_name,
        video_format=history.video_format,
        file_info=history.file_info
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)

    response = LocalPlayHistoryResponse(
        id=new_history.id,
        video_name=new_history.video_name,
        video_format=new_history.video_format,
        file_info=new_history.file_info,
        created_at=new_history.created_at.isoformat() if new_history.created_at else ""
    )
    return response

@router.get("", response_model=List[LocalPlayHistoryResponse])
def get_local_play_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(LocalPlayHistory).filter(
        LocalPlayHistory.user_id == current_user.id
    ).order_by(LocalPlayHistory.created_at.desc()).limit(10).all()

    response = []
    for item in history:
        response.append(LocalPlayHistoryResponse(
            id=item.id,
            video_name=item.video_name,
            video_format=item.video_format,
            file_info=item.file_info,
            created_at=item.created_at.isoformat() if item.created_at else ""
        ))
    return response

@router.delete("/{history_id}")
def delete_local_play_history(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(LocalPlayHistory).filter(
        LocalPlayHistory.id == history_id,
        LocalPlayHistory.user_id == current_user.id
    ).first()

    if not history:
        raise HTTPException(status_code=404, detail="History item not found")

    db.delete(history)
    db.commit()
    return {"message": "Local history item deleted successfully"}

@router.delete("")
def clear_local_play_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(LocalPlayHistory).filter(
        LocalPlayHistory.user_id == current_user.id
    ).delete()
    db.commit()
    return {"message": "All local history cleared successfully"}
