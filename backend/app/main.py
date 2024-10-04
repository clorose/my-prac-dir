# Absolute path: C:\_YHJ\fast\backend\app\main.py

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
import logging
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS 설정
def get_allowed_origins():
    origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
    origins = [origin.strip() for origin in origins if origin.strip()]
    logger.debug(f"Allowed origins: {origins}")
    return origins

allowed_origins = get_allowed_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"Incoming request: {request.method} {request.url}")
    logger.debug(f"Request headers: {request.headers}")
    response = await call_next(request)
    logger.debug(f"Outgoing response: Status {response.status_code}")
    logger.debug(f"Response headers: {response.headers}")
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI project!"}

@app.get("/api/data")
def get_data():
    return {"message": "This is data from the FastAPI backend"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Received file upload request: {file.filename}")
        upload_dir = os.getenv("UPLOAD_DIR", os.path.join(os.getcwd(), "uploads"))
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File uploaded successfully: {file.filename}")
        return JSONResponse(content={
            "filename": file.filename,
            "status": "File uploaded successfully",
            "file_path": file_path
        }, status_code=200)
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"Allowed origins: {allowed_origins}")
    uvicorn.run(app, host=host, port=port)