# File: C:\_YHJ\fast\backend\app\core\config.py
# Purpose: [Describe the purpose of this file]

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    VERSION: str = "0.1.0"
    ALLOWED_ORIGINS: List[str] = []
    UPLOAD_DIR: str = "uploads"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    PYTHONPATH: str = ""
    ML_OUTPUT_DIR: str = "C:/_YHJ/fast/backend/ml/trained_models"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @classmethod
    def model_validate(cls, *args, **kwargs):
        instance = super().model_validate(*args, **kwargs)
        
        # ALLOWED_ORIGINS 처리
        allowed_origins = instance.ALLOWED_ORIGINS
        if isinstance(allowed_origins, str):
            try:
                instance.ALLOWED_ORIGINS = json.loads(allowed_origins)
            except json.JSONDecodeError:
                print(f"Warning: ALLOWED_ORIGINS is not a valid JSON. Value: {allowed_origins}")
                instance.ALLOWED_ORIGINS = []
        
        print(f"Loaded ALLOWED_ORIGINS: {instance.ALLOWED_ORIGINS}")
        return instance

settings = Settings()

# 설정 내용 출력 (디버깅 목적)
print(f"ALLOWED_ORIGINS: {settings.ALLOWED_ORIGINS}")
print(f"HOST: {settings.HOST}")
print(f"PORT: {settings.PORT}")
print(f"PYTHONPATH: {settings.PYTHONPATH}")
print(f"ML_OUTPUT_DIR: {settings.ML_OUTPUT_DIR}")