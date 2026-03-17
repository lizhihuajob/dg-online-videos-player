from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
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
VIDEOS_DIR = os.path.join(UPLOAD_DIR, "videos")
MUSIC_DIR = os.path.join(UPLOAD_DIR, "music")
IMAGES_DIR = os.path.join(UPLOAD_DIR, "images")

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def init_default_user(db: Session):
    """初始化默认用户 admin/123456"""
    default_user = db.query(models.User).filter(models.User.username == "admin").first()
    if not default_user:
        hashed_password = auth.get_password_hash("123456")
        new_user = models.User(
            username="admin",
            email="admin@example.com",
            hashed_password=hashed_password,
            avatar_url=None
        )
        db.add(new_user)
        db.commit()
        print("Default user 'admin' created with password '123456'")

@app.on_event("startup")
def startup_event():
    db = database.SessionLocal()
    try:
        init_default_user(db)
    finally:
        db.close()

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: Optional[str] = None

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
    file_info: str

class LocalPlayHistoryResponse(BaseModel):
    id: int
    video_name: str
    video_format: str
    file_info: str
    created_at: str

    class Config:
        from_attributes = True

class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class GroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True

class VideoResponse(BaseModel):
    id: int
    filename: str
    original_name: str
    url: str
    format: str
    media_type: str
    size: int
    group_id: Optional[int] = None
    group_name: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True

class VideoUpdate(BaseModel):
    name: Optional[str] = None
    group_id: Optional[int] = None

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
            "avatar_url": user.avatar_url
        }
    }

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str


@app.put("/users/me/password")
def update_password(
    password_update: PasswordUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if not auth.verify_password(password_update.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    current_user.hashed_password = auth.get_password_hash(password_update.new_password)
    db.commit()
    return {"message": "Password updated successfully"}


@app.post("/users/me/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """上传用户头像"""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    unique_filename = f"avatar_{current_user.id}_{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(IMAGES_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    current_user.avatar_url = f"/uploads/images/{unique_filename}"
    db.commit()
    
    return {
        "avatar_url": current_user.avatar_url,
        "message": "Avatar uploaded successfully"
    }


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


@app.post("/groups", response_model=GroupResponse)
def create_group(
    group: GroupCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """创建分组"""
    new_group = models.MediaGroup(
        user_id=current_user.id,
        name=group.name,
        description=group.description
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    
    return GroupResponse(
        id=new_group.id,
        name=new_group.name,
        description=new_group.description,
        created_at=new_group.created_at.isoformat() if new_group.created_at else ""
    )


@app.get("/groups", response_model=List[GroupResponse])
def get_groups(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """获取当前用户的所有分组"""
    groups = db.query(models.MediaGroup).filter(
        models.MediaGroup.user_id == current_user.id
    ).order_by(models.MediaGroup.created_at.desc()).all()
    
    response = []
    for group in groups:
        response.append(GroupResponse(
            id=group.id,
            name=group.name,
            description=group.description,
            created_at=group.created_at.isoformat() if group.created_at else ""
        ))
    return response


@app.put("/groups/{group_id}", response_model=GroupResponse)
def update_group(
    group_id: int,
    group_update: GroupUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """更新分组"""
    group = db.query(models.MediaGroup).filter(
        models.MediaGroup.id == group_id,
        models.MediaGroup.user_id == current_user.id
    ).first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if group_update.name is not None:
        group.name = group_update.name
    if group_update.description is not None:
        group.description = group_update.description
    
    db.commit()
    db.refresh(group)
    
    return GroupResponse(
        id=group.id,
        name=group.name,
        description=group.description,
        created_at=group.created_at.isoformat() if group.created_at else ""
    )


@app.delete("/groups/{group_id}")
def delete_group(
    group_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """删除分组"""
    group = db.query(models.MediaGroup).filter(
        models.MediaGroup.id == group_id,
        models.MediaGroup.user_id == current_user.id
    ).first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db.query(models.Video).filter(
        models.Video.group_id == group_id
    ).update({"group_id": None})
    
    db.delete(group)
    db.commit()
    
    return {"message": "Group deleted successfully"}


def get_media_type_from_content_type(content_type: str) -> str:
    """根据 content-type 判断媒体类型"""
    if content_type.startswith("video/"):
        return "video"
    elif content_type.startswith("audio/"):
        return "music"
    elif content_type.startswith("image/"):
        return "image"
    return "video"


def get_storage_dir(media_type: str) -> str:
    """根据媒体类型获取存储目录"""
    if media_type == "video":
        return VIDEOS_DIR
    elif media_type == "music":
        return MUSIC_DIR
    elif media_type == "image":
        return IMAGES_DIR
    return VIDEOS_DIR


@app.post("/videos", response_model=VideoResponse)
async def upload_video(
    file: UploadFile = File(...),
    group_id: Optional[int] = Form(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """上传媒体文件（视频/音乐）"""
    if not file.content_type:
        raise HTTPException(status_code=400, detail="Unknown file type")
    
    media_type = get_media_type_from_content_type(file.content_type)
    if media_type not in ["video", "music"]:
        raise HTTPException(status_code=400, detail="File must be a video or audio file")
    
    if group_id:
        group = db.query(models.MediaGroup).filter(
            models.MediaGroup.id == group_id,
            models.MediaGroup.user_id == current_user.id
        ).first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
    
    target_dir = get_storage_dir(media_type)
    file_ext = os.path.splitext(file.filename)[1] if file.filename else (".mp4" if media_type == "video" else ".mp3")
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(target_dir, unique_filename)
    
    file_size = 0
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        file_size = os.path.getsize(file_path)
    
    url_path = f"/uploads/{media_type}s/{unique_filename}" if media_type != "image" else f"/uploads/images/{unique_filename}"
    
    new_video = models.Video(
        user_id=current_user.id,
        group_id=group_id,
        filename=unique_filename,
        original_name=file.filename or "unnamed",
        url=url_path,
        format=file_ext.lstrip("."),
        media_type=media_type,
        size=file_size
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    
    return VideoResponse(
        id=new_video.id,
        filename=new_video.filename,
        original_name=new_video.original_name,
        url=new_video.url,
        format=new_video.format,
        media_type=new_video.media_type,
        size=new_video.size,
        group_id=new_video.group_id,
        group_name=new_video.group.name if new_video.group else None,
        created_at=new_video.created_at.isoformat() if new_video.created_at else ""
    )


@app.get("/videos", response_model=List[VideoResponse])
def get_videos(
    media_type: Optional[str] = None,
    group_id: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """获取当前用户的媒体文件"""
    query = db.query(models.Video).filter(
        models.Video.user_id == current_user.id
    )
    
    if media_type:
        query = query.filter(models.Video.media_type == media_type)
    
    if group_id:
        query = query.filter(models.Video.group_id == group_id)
    
    videos = query.order_by(models.Video.created_at.desc()).all()
    
    response = []
    for video in videos:
        response.append(VideoResponse(
            id=video.id,
            filename=video.filename,
            original_name=video.original_name,
            url=video.url,
            format=video.format,
            media_type=video.media_type,
            size=video.size,
            group_id=video.group_id,
            group_name=video.group.name if video.group else None,
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
    """修改媒体文件名称"""
    video = db.query(models.Video).filter(
        models.Video.id == video_id,
        models.Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if video_update.name is not None:
        video.original_name = video_update.name
    
    db.commit()
    db.refresh(video)
    
    return VideoResponse(
        id=video.id,
        filename=video.filename,
        original_name=video.original_name,
        url=video.url,
        format=video.format,
        media_type=video.media_type,
        size=video.size,
        group_id=video.group_id,
        group_name=video.group.name if video.group else None,
        created_at=video.created_at.isoformat() if video.created_at else ""
    )


@app.put("/videos/{video_id}/group")
def change_video_group(
    video_id: int,
    group_id: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """切换媒体文件的分组"""
    video = db.query(models.Video).filter(
        models.Video.id == video_id,
        models.Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if group_id:
        group = db.query(models.MediaGroup).filter(
            models.MediaGroup.id == group_id,
            models.MediaGroup.user_id == current_user.id
        ).first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        video.group_id = group_id
    else:
        video.group_id = None
    
    db.commit()
    db.refresh(video)
    
    return VideoResponse(
        id=video.id,
        filename=video.filename,
        original_name=video.original_name,
        url=video.url,
        format=video.format,
        media_type=video.media_type,
        size=video.size,
        group_id=video.group_id,
        group_name=video.group.name if video.group else None,
        created_at=video.created_at.isoformat() if video.created_at else ""
    )


@app.delete("/videos/{video_id}")
def delete_video(
    video_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """删除媒体文件"""
    video = db.query(models.Video).filter(
        models.Video.id == video_id,
        models.Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    target_dir = get_storage_dir(video.media_type)
    file_path = os.path.join(target_dir, video.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.delete(video)
    db.commit()
    
    return {"message": "Video deleted successfully"}


@app.get("/")
def root():
    return {"message": "Video Player API is running"}
