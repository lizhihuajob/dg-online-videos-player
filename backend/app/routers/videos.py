import os
import uuid
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from jose import JWTError, jwt
from ..database import get_db
from ..models import User
from ..auth import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/videos", tags=["videos"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

UPLOAD_DIR = "/app/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

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

class UploadResponse(BaseModel):
    video_url: str
    video_name: str
    video_format: str
    message: str

@router.post("/upload", response_model=UploadResponse)
async def upload_video(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    allowed_types = ["video/mp4", "video/webm", "video/ogg", "video/quicktime", "video/x-msvideo"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only video files are allowed.")
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if not file_ext:
        file_ext = ".mp4"
    
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    user_dir = os.path.join(UPLOAD_DIR, str(current_user.id))
    os.makedirs(user_dir, exist_ok=True)
    
    file_path = os.path.join(user_dir, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    video_url = f"/videos/stream/{current_user.id}/{unique_filename}"
    video_format = file_ext.lstrip('.')
    
    return UploadResponse(
        video_url=video_url,
        video_name=file.filename,
        video_format=video_format,
        message="Video uploaded successfully"
    )
