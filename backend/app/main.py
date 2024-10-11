from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.api import router as api_router
from app.middleware.logging import log_requests
from app.core.config import settings
import logging
import uvicorn

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION
    )

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 필요한 경우 특정 도메인으로 제한 가능
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 정적 파일 서빙 설정
    static_folder_path = settings.ML_OUTPUT_DIR
    app.mount("/static", StaticFiles(directory=static_folder_path), name="static")

    # 미들웨어 추가
    app.middleware("http")(log_requests)

    # 기본 엔드포인트 추가
    @app.get("/")
    async def root():
        return {"message": "Welcome to the FastAPI project!"}

    # 라우터 추가
    app.include_router(api_router)

    return app

app = create_app()

if __name__ == "__main__":
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
