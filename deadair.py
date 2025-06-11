import cloudinary
import cloudinary.uploader
import os

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD"),
    api_key=os.getenv("CLOUDINARY_KEY"),
    api_secret=os.getenv("CLOUDINARY_SECRET")
)
from fastapi import Form
from fastapi.responses import JSONResponse
from TTS.api import TTS

# Load TTS model (do this once)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

@app.post("/narrate")
async def narrate(text: str = Form(...), voice_style: str = Form(...)):
    # Generate temp audio file
    temp_file = "temp.wav"
    tts.tts_to_file(text=text, file_path=temp_file)

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(temp_file, resource_type="video")
    audio_url = upload_result["secure_url"]

    return JSONResponse(content={"audio_url": audio_url})
