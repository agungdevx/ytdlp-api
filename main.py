from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Req(BaseModel):
    url: str
    format: str = "video"

@app.post("/api/download")
def download(r: Req):
    opts = {
        "quiet": True,
        "skip_download": True,
        "format": "best[ext=mp4]/best" if r.format == "video" else "bestaudio[ext=m4a]/bestaudio",
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(r.url, download=False)
        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "url": info.get("url"),
            "ext": info.get("ext"),
        }
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/")
def root():
    return FileResponse("index.html")
