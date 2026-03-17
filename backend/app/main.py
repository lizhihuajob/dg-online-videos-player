from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.staticfiles import StaticFiles
import os
import shutil
import uuid
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text
from datetime import timedelta
from pydantic import BaseModel
from typing import List, Optional
from jose import JWTError, jwt
from . import models, database, auth

app = FastAPI(title="Video Player API")

UPLOAD_DIR = "/app/uploads"
VIDEOS_DIR = os.path.join(UPLOAD_DIR, "videos")
MUSIC_DIR = os.path.join(UPLOAD_DIR, "music")
IMAGES_DIR = os.path.join(UPLOAD_DIR, "images")

os.makedirs(UPLOAD_DIR, exist_ok=True)
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

# 初始化默认用户
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

def sync_database_schema():
    """同步数据库表结构，处理模型变化但表已存在的情况"""
    inspector = inspect(database.engine)
    
    for table_name, table in models.Base.metadata.tables.items():
        if not inspector.has_table(table_name):
            continue
        
        existing_columns = {col['name'] for col in inspector.get_columns(table_name)}
        model_columns = {col.name for col in table.columns}
        
        missing_columns = model_columns - existing_columns
        
        if missing_columns:
            with database.engine.connect() as conn:
                for col_name in missing_columns:
                    column = table.c[col_name]
                    column_type = column.type.compile(database.engine.dialect)
                    nullable = "NULL" if column.nullable else "NOT NULL"
                    default = ""
                    if column.server_default:
                        default = f" DEFAULT {column.server_default.arg.text}"
                    elif column.default:
                        default = f" DEFAULT {column.default.arg}"
                    sql = f"ALTER TABLE {table_name} ADD COLUMN {col_name} {column_type} {nullable}{default}"
                    conn.execute(text(sql))
                conn.commit()

@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=database.engine)
    sync_database_schema()
    db = database.SessionLocal()
    try:
        init_default_user(db)
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

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

class VideoResponse(BaseModel):
    id: int
    filename: str
    original_name: str
    url: str
    format: str
    size: int
    created_at: str
    group_id: Optional[int] = None

    class Config:
        from_attributes = True

class VideoUpdate(BaseModel):
    name: str

class GroupCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = None

class GroupResponse(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class MusicResponse(BaseModel):
    id: int
    filename: str
    original_name: str
    url: str
    format: str
    size: int
    created_at: str
    group_id: Optional[int] = None

    class Config:
        from_attributes = True

class MoveToGroupRequest(BaseModel):
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

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    """用户注册"""
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
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

@app.put("/users/me", response_model=UserResponse)
def update_user_me(
    user_update: UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if user_update.username is not None:
        existing_user = db.query(models.User).filter(
            models.User.username == user_update.username,
            models.User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")
        current_user.username = user_update.username
    
    if user_update.email is not None:
        existing_user = db.query(models.User).filter(
            models.User.email == user_update.email,
            models.User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = user_update.email
    
    db.commit()
    db.refresh(current_user)
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
    # Verify current password
    if not auth.verify_password(password_update.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
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
    
    # 更新用户头像URL
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


# Video Management APIs
@app.post("/videos", response_model=VideoResponse)
async def upload_video(
    file: UploadFile = File(...),
    group_id: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """上传视频文件"""
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video")
    if group_id is not None:
        group = db.query(models.Group).filter(
            models.Group.id == group_id,
            models.Group.user_id == current_user.id
        ).first()
        if not group:
            raise HTTPException(status_code=400, detail="Invalid group_id")
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".mp4"
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(VIDEOS_DIR, unique_filename)
    file_size = 0
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        file_size = os.path.getsize(file_path)
    new_video = models.Video(
        user_id=current_user.id,
        group_id=group_id,
        filename=unique_filename,
        original_name=file.filename or "unnamed",
        url=f"/uploads/videos/{unique_filename}",
        format=file_ext.lstrip("."),
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
        size=new_video.size,
        created_at=new_video.created_at.isoformat() if new_video.created_at else "",
        group_id=new_video.group_id
    )


@app.get("/videos", response_model=List[VideoResponse])
def get_videos(
    group_id: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """获取当前用户的所有视频"""
    query = db.query(models.Video).filter(models.Video.user_id == current_user.id)
    if group_id is not None:
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
            size=video.size,
            created_at=video.created_at.isoformat() if video.created_at else "",
            group_id=video.group_id
        ))
    return response


@app.put("/videos/{video_id}", response_model=VideoResponse)
def update_video(
    video_id: int,
    video_update: VideoUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """修改视频名称"""
    video = db.query(models.Video).filter(
        models.Video.id == video_id,
        models.Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    video.original_name = video_update.name
    db.commit()
    db.refresh(video)
    
    return VideoResponse(
        id=video.id,
        filename=video.filename,
        original_name=video.original_name,
        url=video.url,
        format=video.format,
        size=video.size,
        created_at=video.created_at.isoformat() if video.created_at else "",
        group_id=video.group_id
    )


@app.delete("/videos/{video_id}")
def delete_video(
    video_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """删除视频"""
    video = db.query(models.Video).filter(
        models.Video.id == video_id,
        models.Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # 删除物理文件
    file_path = os.path.join(VIDEOS_DIR, video.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.delete(video)
    db.commit()
    
    return {"message": "Video deleted successfully"}


@app.post("/groups", response_model=GroupResponse)
def create_group(
    group: GroupCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """创建分组"""
    new_group = models.Group(
        user_id=current_user.id,
        name=group.name,
        type=group.type,
        description=group.description
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return GroupResponse(
        id=new_group.id,
        name=new_group.name,
        type=new_group.type,
        description=new_group.description,
        created_at=new_group.created_at.isoformat() if new_group.created_at else ""
    )

@app.get("/groups", response_model=List[GroupResponse])
def get_groups(
    type: Optional[str] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """获取用户的所有分组"""
    query = db.query(models.Group).filter(models.Group.user_id == current_user.id)
    if type:
        query = query.filter(models.Group.type == type)
    groups = query.order_by(models.Group.created_at.desc()).all()
    response = []
    for group in groups:
        response.append(GroupResponse(
            id=group.id,
            name=group.name,
            type=group.type,
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
    """更新分组信息"""
    group = db.query(models.Group).filter(
        models.Group.id == group_id,
        models.Group.user_id == current_user.id
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
        type=group.type,
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
    group = db.query(models.Group).filter(
        models.Group.id == group_id,
        models.Group.user_id == current_user.id
    ).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    videos = db.query(models.Video).filter(models.Video.group_id == group_id).all()
    for video in videos:
        video.group_id = None
    musics = db.query(models.Music).filter(models.Music.group_id == group_id).all()
    for music in musics:
        music.group_id = None
    db.delete(group)
    db.commit()
    return {"message": "Group deleted successfully"}

@app.post("/musics", response_model=MusicResponse)
async def upload_music(
    file: UploadFile = File(...),
    group_id: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """上传音乐文件"""
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio")
    if group_id is not None:
        group = db.query(models.Group).filter(
            models.Group.id == group_id,
            models.Group.user_id == current_user.id
        ).first()
        if not group:
            raise HTTPException(status_code=400, detail="Invalid group_id")
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".mp3"
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(MUSIC_DIR, unique_filename)
    file_size = 0
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        file_size = os.path.getsize(file_path)
    new_music = models.Music(
        user_id=current_user.id,
        group_id=group_id,
        filename=unique_filename,
        original_name=file.filename or "unnamed",
        url=f"/uploads/music/{unique_filename}",
        format=file_ext.lstrip("."),
        size=file_size
    )
    db.add(new_music)
    db.commit()
    db.refresh(new_music)
    return MusicResponse(
        id=new_music.id,
        filename=new_music.filename,
        original_name=new_music.original_name,
        url=new_music.url,
        format=new_music.format,
        size=new_music.size,
        created_at=new_music.created_at.isoformat() if new_music.created_at else "",
        group_id=new_music.group_id
    )

@app.get("/musics", response_model=List[MusicResponse])
def get_musics(
    group_id: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """获取用户的所有音乐"""
    query = db.query(models.Music).filter(models.Music.user_id == current_user.id)
    if group_id is not None:
        query = query.filter(models.Music.group_id == group_id)
    musics = query.order_by(models.Music.created_at.desc()).all()
    response = []
    for music in musics:
        response.append(MusicResponse(
            id=music.id,
            filename=music.filename,
            original_name=music.original_name,
            url=music.url,
            format=music.format,
            size=music.size,
            created_at=music.created_at.isoformat() if music.created_at else "",
            group_id=music.group_id
        ))
    return response

@app.delete("/musics/{music_id}")
def delete_music(
    music_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """删除音乐"""
    music = db.query(models.Music).filter(
        models.Music.id == music_id,
        models.Music.user_id == current_user.id
    ).first()
    if not music:
        raise HTTPException(status_code=404, detail="Music not found")
    file_path = os.path.join(MUSIC_DIR, music.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete(music)
    db.commit()
    return {"message": "Music deleted successfully"}

@app.put("/videos/{video_id}/group")
def move_video_to_group(
    video_id: int,
    request: MoveToGroupRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """移动视频到指定分组"""
    video = db.query(models.Video).filter(
        models.Video.id == video_id,
        models.Video.user_id == current_user.id
    ).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if request.group_id is not None:
        group = db.query(models.Group).filter(
            models.Group.id == request.group_id,
            models.Group.user_id == current_user.id
        ).first()
        if not group:
            raise HTTPException(status_code=400, detail="Invalid group_id")
    video.group_id = request.group_id
    db.commit()
    return {"message": "Video moved successfully", "group_id": request.group_id}

@app.put("/musics/{music_id}/group")
def move_music_to_group(
    music_id: int,
    request: MoveToGroupRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """移动音乐到指定分组"""
    music = db.query(models.Music).filter(
        models.Music.id == music_id,
        models.Music.user_id == current_user.id
    ).first()
    if not music:
        raise HTTPException(status_code=404, detail="Music not found")
    if request.group_id is not None:
        group = db.query(models.Group).filter(
            models.Group.id == request.group_id,
            models.Group.user_id == current_user.id
        ).first()
        if not group:
            raise HTTPException(status_code=400, detail="Invalid group_id")
    music.group_id = request.group_id
    db.commit()
    return {"message": "Music moved successfully", "group_id": request.group_id}

@app.get("/")
def root():
    return {"message": "Video Player API is running"}
