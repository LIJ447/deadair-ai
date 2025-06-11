import os
import cloudinary
import cloudinary.uploader
import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Load Cloudinary credentials
cloud_name = os.getenv("CLOUDINARY_CLOUD")
api_key = os.getenv("CLOUDINARY_KEY")
api_secret = os.getenv("CLOUDINARY_SECRET")

if not all([cloud_name, api_key, api_secret]):
    raise ValueError("Missing Cloudinary configuration environment variables")

# Configure Cloudinary once
cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ElevenLabs API Key
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Default voice
