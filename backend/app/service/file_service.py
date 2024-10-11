# File: C:\_YHJ\fast\backend\app\service\file_service.py
# Purpose: Handles file operations like listing and uploading files, as well as predictions

import os
import joblib
import pandas as pd
from fastapi import HTTPException, UploadFile
import logging
import shutil
from app.core.config import settings

logger = logging.getLogger(__name__)

def list_files(directory):
    """
    주어진 디렉토리에서 모든 .joblib 파일만 반환합니다.
    """
    files = []
    try:
        for root, _, filenames in os.walk(directory):
            for name in filenames:
                if name.endswith(".joblib"):  # .joblib 파일만 필터링
                    files.append(
                        {
                            "name": os.path.splitext(name)[0],  # 확장자 제거
                            "isDirectory": False,
                            "path": os.path.join(root, name),
                        }
                    )
    except Exception as e:
        logger.error(f"Error listing files in directory: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listing files in directory")
    return files

async def upload_file(file: UploadFile):
    """
    파일을 업로드하고 joblib 파일로 저장합니다.
    """
    try:
        logger.info(f"Received file upload request: {file.filename}")
        if not os.path.exists(settings.UPLOAD_DIR):
            os.makedirs(settings.UPLOAD_DIR)

        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"File uploaded successfully: {file.filename}")
        return {"filename": file.filename, "status": "File uploaded successfully"}
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error uploading file")

def predict_with_model(model_name, csv_file):
    """
    주어진 모델 이름과 CSV 파일을 사용하여 예측을 수행합니다.
    """
    try:
        # 모델 이름에서 확장자가 포함되어 있는지 확인하고, 없을 경우 추가
        if not model_name.endswith(".joblib"):
            model_name = f"{model_name}.joblib"
        
        # 모델 파일 경로 구성
        model_path = os.path.join(settings.ML_OUTPUT_DIR, model_name)
        
        # 모델 로드
        if not os.path.exists(model_path):
            logger.error(f"Model file not found: {model_path}")
            raise HTTPException(status_code=404, detail=f"Model file '{model_path}' not found in {settings.ML_OUTPUT_DIR}")

        model = joblib.load(model_path)

        # CSV 파일 읽기
        try:
            df = pd.read_csv(csv_file.file)
            logger.info(f"CSV file read successfully: {df.shape}")
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}", exc_info=True)
            raise HTTPException(status_code=400, detail="Invalid CSV file format")

        # 예측 수행
        try:
            logger.info(f"Predicting using model: {model_name}")
            predictions = model.predict(df)
            logger.info(f"Prediction completed successfully")
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error during model prediction")

        # CSV 데이터를 리스트로 변환하여 프론트엔드에 전송
        csv_data = [df.columns.tolist()] + df.values.tolist()

        return {"predictions": predictions.tolist(), "csvData": csv_data}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unhandled error during prediction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Unhandled error during prediction")
