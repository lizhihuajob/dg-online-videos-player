from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware

from . import models, database
from .api import router as api_router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Video Player API")

# Create directories
UPLOAD_DIR = "/app/uploads"
IMAGES_DIR = "/app/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Video Player API is running"}
