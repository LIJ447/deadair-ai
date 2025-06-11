cloud_name = os.getenv("CLOUDINARY_CLOUD")
api_key = os.getenv("CLOUDINARY_KEY")
api_secret = os.getenv("CLOUDINARY_SECRET")

if not all([cloud_name, api_key, api_secret]):
    raise ValueError("Missing Cloudinary configuration environment variables")

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import cloudinary
import cloudinary.uploader
import os
import requests

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

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD"),
    api_key=os.getenv("CLOUDINARY_KEY"),
    api_secret=os.getenv("CLOUDINARY_SECRET")
)

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Default voice

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/narrate")
async def narrate(text: str = Form(...), voice_style: str = Form(...)):
    try:
        print(f"[CHAR COUNT] Narration request: {len(text)} characters")

        headers = {
            "xi-api-key": ELEVEN_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            headers=headers,
            json=payload
        )

        print("ElevenLabs Status:", response.status_code)
        print("ElevenLabs Response:", response.text)

        if response.status_code != 200:
            return JSONResponse(
                content={"error": "Narration failed", "details": response.text},
                status_code=500
            )

        with open("temp.mp3", "wb") as f:
            f.write(response.content)

        upload_result = cloudinary.uploader.upload("temp.mp3", resource_type="video")
        return JSONResponse(content={"audio_url": upload_result["secure_url"]})

    except Exception as e:
        print("Narration exception:", str(e))
        return JSONResponse(content={"error": "Unexpected error", "details": str(e)}, status_code=500)
