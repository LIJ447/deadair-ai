
import os
import uuid

def generate_tts(text, voice):
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join("static", filename)
    # Placeholder: Replace with real Coqui TTS call
    with open(filepath, "wb") as f:
        f.write(b"FAKE_AUDIO")
    return {"url": f"/static/{filename}"}
    