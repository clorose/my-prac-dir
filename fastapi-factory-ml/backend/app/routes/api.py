# File: C:\_YHJ\fast\backend\app\routes\api.py
# Purpose: API routes for interacting with the backend

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.service.file_service import upload_file, list_files, predict_with_model
from ml.main import run_model
from app.core.config import settings
import os

router = APIRouter()

@router.get("/")
async def root():
    """
    기본 엔드포인트 - API 상태를 확인하는 간단한 응답입니다.
    """
    return {"message": "Welcome to the FastAPI project!"}

@router.get("/api/files")
def get_files():
    """
    Returns all .joblib files in the output directory.
    """
    try:
        return list_files(settings.ML_OUTPUT_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload(file: UploadFile = File(...), target_column: str = Form(None)):
    try:
        upload_result = await upload_file(file)
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)

        # ML 모델 실행 (타겟 열 지정, 기본값은 None으로 'quality_label' 사용)
        ml_result = run_model(file_path, target_column)

        return {"upload_result": upload_result, "ml_result": ml_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/predict")
async def predict(file: UploadFile = File(...), selected_model: str = Form(...)):
    """
    선택된 모델과 업로드된 CSV 파일을 사용하여 예측을 수행합니다.
    """
    try:
        # predict_with_model 함수를 호출하여 예측을 수행
        result = predict_with_model(selected_model, file)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing prediction: {str(e)}")
