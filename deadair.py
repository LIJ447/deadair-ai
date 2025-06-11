import os
import cloudinary
import cloudinary.uploader
import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Load env vars
cloud_name = os.getenv("CLOUDINARY_CLOUD")
api_key = os.getenv("CLOUDINARY_KEY")
api_secret = os.getenv("CLOUDINARY_SECRET")
eleven_api_key = os.getenv("ELEVEN_API_KEY")
voice_id = "EXAVITQu4vr4xnSDxMaL"

if not all([cloud_name, api_key, api_secret, eleven_api_key]):
    raise ValueError("Missing one or more required API environment variables.")

# Configure Cloudinary
cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)

# FastAPI setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Home route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Narration route
@app.post("/narrate")
async def narrate(text: str = Form(...), voice_style: str = Form(...)):
    try:
        headers = {
            "xi-api-key": eleven_api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.75
            }
        }

        tts_response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers=headers,
            json=payload
        )

        if tts_response.status_code != 200:
            return JSONResponse(
                status_code=500,
                content={"error": "TTS API failed", "details": tts_response.text}
            )

        with open("temp.mp3", "wb") as f:
            f.write(tts_response.content)

        upload_result = cloudinary.uploader.upload("temp.mp3", resource_type="video")
        audio_url = upload_result["secure_url"]

        return JSONResponse(content={"audio_url": audio_url})

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Narration failed", "details": str(e)}
        )
