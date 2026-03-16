from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.staticfiles import StaticFiles
import os
import shutil
import uuid
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel
from typing import List, Optional
from jose import JWTError, jwt
from . import models, database, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Video Player API")

UPLOAD_DIR = "/app/uploads"
AVATAR_DIR = "/app/uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AVATAR_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_default_admin():
    db = database.SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            hashed_password = auth.get_password_hash("123456")
            admin = models.User(
                username="admin",
                email="admin@example.com",
                hashed_password=hashed_password
            )
            db.add(admin)
            db.commit()
            print("Default admin user created: admin / 123456")
    finally:
        db.close()


create_default_admin()

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class PlayHistoryCreate(BaseModel):
    video_url: str
    video_name: str
    video_format: str

class PlayHistoryResponse(BaseModel):
    id: int
    video_url: str
    video_name: str
    video_format: str
    created_at: str

    class Config:
        from_attributes = True

class LocalPlayHistoryCreate(BaseModel):
    video_name: str
    video_format: str
    file_info: str  # JSON string

class LocalPlayHistoryResponse(BaseModel):
    id: int
    video_name: str
    video_format: str
    file_info: str
    created_at: str

    class Config:
        from_attributes = True

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


@app.post("/token", response_model=Token)
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
            "email": user.email,
            "avatar": user.avatar
        }
    }

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


class UserUpdate(BaseModel):
    email: str


class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str


@app.put("/users/me", response_model=UserResponse)
def update_user(
    user_update: UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if user_update.email != current_user.email:
        existing_email = db.query(models.User).filter(
            models.User.email == user_update.email,
            models.User.id != current_user.id
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    current_user.email = user_update.email
    db.commit()
    db.refresh(current_user)
    return current_user


@app.post("/users/me/avatar")
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
    
    if current_user.avatar:
        old_avatar_path = os.path.join(UPLOAD_DIR, current_user.avatar.lstrip("/uploads/"))
        if os.path.exists(old_avatar_path):
            os.remove(old_avatar_path)
    
    current_user.avatar = f"/uploads/avatars/{unique_filename}"
    db.commit()
    db.refresh(current_user)
    
    return {"avatar": current_user.avatar}


@app.put("/users/me/password")
def update_password(
    password_update: PasswordUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    # Verify current password
    if not auth.verify_password(password_update.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    current_user.hashed_password = auth.get_password_hash(password_update.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@app.post("/history", response_model=PlayHistoryResponse)
def add_play_history(
    history: PlayHistoryCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
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
    
    response = PlayHistoryResponse(
        id=new_history.id,
        video_url=new_history.video_url,
        video_name=new_history.video_name,
        video_format=new_history.video_format,
        created_at=new_history.created_at.isoformat() if new_history.created_at else ""
    )
    return response

@app.get("/history", response_model=List[PlayHistoryResponse])
def get_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    history = db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id
    ).order_by(models.PlayHistory.created_at.desc()).limit(10).all()
    
    response = []
    for item in history:
        response.append(PlayHistoryResponse(
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

@app.delete("/history")
def clear_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == current_user.id
    ).delete()
    db.commit()
    return {"message": "All history cleared successfully"}


# Local Play History APIs
@app.post("/local-history", response_model=LocalPlayHistoryResponse)
def add_local_play_history(
    history: LocalPlayHistoryCreate,
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

    response = LocalPlayHistoryResponse(
        id=new_history.id,
        video_name=new_history.video_name,
        video_format=new_history.video_format,
        file_info=new_history.file_info,
        created_at=new_history.created_at.isoformat() if new_history.created_at else ""
    )
    return response


@app.get("/local-history", response_model=List[LocalPlayHistoryResponse])
def get_local_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    history = db.query(models.LocalPlayHistory).filter(
        models.LocalPlayHistory.user_id == current_user.id
    ).order_by(models.LocalPlayHistory.created_at.desc()).limit(10).all()

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


@app.delete("/local-history/{history_id}")
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


@app.delete("/local-history")
def clear_local_play_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    db.query(models.LocalPlayHistory).filter(
        models.LocalPlayHistory.user_id == current_user.id
    ).delete()
    db.commit()
    return {"message": "All local history cleared successfully"}


@app.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video")
    
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".mp4"
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_size = os.path.getsize(file_path)
    
    video = models.Video(
        user_id=current_user.id,
        name=file.filename or "未命名视频",
        filename=unique_filename,
        url=f"/uploads/{unique_filename}",
        format=file_ext.lstrip("."),
        size=file_size
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    
    return {
        "id": video.id,
        "name": video.name,
        "filename": video.filename,
        "url": video.url,
        "format": video.format,
        "size": video.size,
        "created_at": video.created_at.isoformat() if video.created_at else ""
    }


class VideoResponse(BaseModel):
    id: int
    name: str
    filename: str
    url: str
    format: str
    size: Optional[int] = None
    created_at: str

    class Config:
        from_attributes = True


class VideoUpdate(BaseModel):
    name: str


@app.get("/videos", response_model=List[VideoResponse])
def get_videos(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    videos = db.query(models.Video).filter(
        models.Video.user_id == current_user.id
    ).order_by(models.Video.created_at.desc()).all()
    
    response = []
    for video in videos:
        response.append(VideoResponse(
            id=video.id,
            name=video.name,
            filename=video.filename,
            url=video.url,
            format=video.format,
            size=video.size,
            created_at=video.created_at.isoformat() if video.created_at else ""
        ))
    return response


@app.put("/videos/{video_id}", response_model=VideoResponse)
def update_video(
    video_id: int,
    video_update: VideoUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    video = db.query(models.Video).filter(
        models.Video.id == video_id,
        models.Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    video.name = video_update.name
    db.commit()
    db.refresh(video)
    
    return VideoResponse(
        id=video.id,
        name=video.name,
        filename=video.filename,
        url=video.url,
        format=video.format,
        size=video.size,
        created_at=video.created_at.isoformat() if video.created_at else ""
    )


@app.delete("/videos/{video_id}")
def delete_video(
    video_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    video = db.query(models.Video).filter(
        models.Video.id == video_id,
        models.Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    file_path = os.path.join(UPLOAD_DIR, video.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.delete(video)
    db.commit()
    
    return {"message": "Video deleted successfully"}

@app.get("/")
def root():
    return {"message": "Video Player API is running"}
