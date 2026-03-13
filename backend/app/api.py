from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
from jose import JWTError, jwt
import os
import shutil
import uuid

from . import models, database, auth, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

UPLOAD_DIR = "/app/uploads"
AVATAR_DIR = "/app/uploads/images/user"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AVATAR_DIR, exist_ok=True)

router = APIRouter()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
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

@router.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/users/me", response_model=schemas.UserResponse)
def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if user_update.username != current_user.username:
        existing_user = db.query(models.User).filter(
            models.User.username == user_update.username,
            models.User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    if user_update.email != current_user.email:
        existing_email = db.query(models.User).filter(
            models.User.email == user_update.email,
            models.User.id != current_user.id
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    current_user.username = user_update.username
    current_user.email = user_update.email
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/users/me/password")
def update_password(
    password_update: schemas.PasswordUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if not auth.verify_password(password_update.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    current_user.hashed_password = auth.get_password_hash(password_update.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@router.post("/upload-avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(AVATAR_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    avatar_url = f"/uploads/images/user/{unique_filename}"
    current_user.avatar = avatar_url
    db.commit()
    
    return {"avatar_url": avatar_url}

@router.post("/history", response_model=schemas.PlayHistoryResponse)
def add_play_history(
    history: schemas.PlayHistoryCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
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

@router.get("/history")
def get_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = None
):
    query = db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id
    )
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            models.PlayHistory.video_name.ilike(search_term) |
            models.PlayHistory.video_url.ilike(search_term)
        )
    
    total = query.count()
    history = query.order_by(models.PlayHistory.created_at.desc()) \
                  .offset((page - 1) * page_size) \
                  .limit(page_size) \
                  .all()
    
    items = []
    for item in history:
        items.append(schemas.PlayHistoryResponse(
            id=item.id,
            video_url=item.video_url,
            video_name=item.video_name,
            video_format=item.video_format,
            created_at=item.created_at.isoformat() if item.created_at else ""
        ))
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

@router.delete("/history/{history_id}")
def delete_play_history(
    history_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
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

@router.delete("/history")
def clear_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id
    ).delete()
    db.commit()
    return {"message": "All history cleared successfully"}

@router.post("/local-history", response_model=schemas.LocalPlayHistoryResponse)
def add_local_play_history(
    history: schemas.LocalPlayHistoryCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
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

@router.get("/local-history", response_model=List[schemas.LocalPlayHistoryResponse])
def get_local_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
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

@router.delete("/local-history/{history_id}")
def delete_local_play_history(
    history_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
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

@router.delete("/local-history")
def clear_local_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    db.query(models.LocalPlayHistory).filter(
        models.LocalPlayHistory.user_id == current_user.id
    ).delete()
    db.commit()
    return {"message": "All local history cleared successfully"}

@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user)
):
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video")
    
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".mp4"
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "filename": file.filename,
        "url": f"/uploads/{unique_filename}",
        "format": file_ext.lstrip(".")
    }
