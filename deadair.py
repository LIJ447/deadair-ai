from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware to allow all origins (for local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for serving CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set the templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/narrate")
async def narrate(text: str = Form(...), voice_style: str = Form(...)):
    # Simulate TTS processing
    print(f"Text received: {text}")
    print(f"Voice style selected: {voice_style}")
    return JSONResponse(content={"message": f"Narration (simulated) for voice style: {voice_style}"})
