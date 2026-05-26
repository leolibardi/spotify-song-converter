import os
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
from downloader import SpotifyDownloader

load_dotenv()

API_TOKEN = os.getenv("API_SECRET_TOKEN", "senha")

api = FastAPI(title="Spotify Downloader API")
bot = SpotifyDownloader()

security = HTTPBearer()

class DownloadRequest(BaseModel):
    url: str

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token. Access Denied."
        )
    return credentials.credentials


@api.get("/")
def read_root():
    return{"message":"API Online!"}

@api.post("/api/download", dependencies=[Depends(verify_token)])
async def start_download(request: DownloadRequest, background_tasks: BackgroundTasks):
    if "spotify.com" not in request.url:
        raise HTTPException(status_code=400, detail="Invalid URL. Use an official Spotify link.")
    
    background_tasks.add_task(bot.download_track, request.url)

    return {
        "status":"success",
        "message":"Download queued! Follow the progress in the console.",
        "received_url":request.url
    }