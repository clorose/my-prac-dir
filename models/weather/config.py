# File: C:\gaon\2024\weather\config.py
# Purpose: [Describe the purpose of this file]
# 신버전

import os
from dotenv import load_dotenv
from pathlib import Path
import logging
from datetime import datetime

def find_project_root(current_path: Path = Path.cwd()) -> Path:
    if (current_path / '.project_root').exists():
        return current_path
    parent = current_path.parent
    if parent == current_path:
        raise FileNotFoundError("Project root not found. Are you sure '.project_root' file exists?")
    return find_project_root(parent)

# 프로젝트 루트 찾기
try:
    project_root = find_project_root()
    env_path = project_root / '.env'

    load_dotenv(dotenv_path=env_path)

    class Config:
        """환경 설정 클래스"""

        # 프로젝트 구조
        ROOT_DIR = project_root
        APP_DIR = ROOT_DIR / "app"
        DATA_DIR = ROOT_DIR / "data"
        TESTS_DIR = ROOT_DIR / "tests"
        LOGS_DIR = ROOT_DIR / "logs"

        # 애플리케이션 디렉토리
        API_DIR = APP_DIR / "api"
        CORE_DIR = APP_DIR / "core"
        MODELS_DIR = APP_DIR / "models"
        SERVICES_DIR = APP_DIR / "services"
        UTILS_DIR = APP_DIR / "utils"

        # 모델 저장 디렉토리
        CLIMATE_MODEL_DIR = DATA_DIR / "climate_model"

        # API 설정
        WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
        API_BASE_URL = "https://apihub.kma.go.kr"
        API_ENDPOINTS = {
            "monthly_summary": "/api/typ02/openApi/SfcMtlyInfoService/getMmSumry",
            "monthly_summary2": "/api/typ02/openApi/SfcMtlyInfoService/getMmSumry2",
        }
        API_RETRY_ATTEMPTS = 3
        API_RETRY_DELAY = 2
        API_TIMEOUT = 10

        # 데이터 설정
        STATION_ID = "108"  # 서울
        START_DATE = "201601"  # YYYYMM 형식
        END_DATE = datetime.now().strftime("%Y%m")
        MONTH_SEQUENCE_LENGTH = 12
        DATA_FEATURES = ["avg_temp", "max_temp", "min_temp", "humidity"]

        # 모델 파일명
        MODEL_NAME = "model.keras"
        SEQUENCE_DATA_NAME = "last_sequence.npy"
        LAST_DATE_NAME = "last_date.txt"
        SCALER_NAME = "scaler.pkl"

        # 모델 파일 경로
        MODEL_FILE = CLIMATE_MODEL_DIR / MODEL_NAME
        SCALER_FILE = CLIMATE_MODEL_DIR / SCALER_NAME
        SEQUENCE_FILE = CLIMATE_MODEL_DIR / SEQUENCE_DATA_NAME
        LAST_DATE_FILE = CLIMATE_MODEL_DIR / LAST_DATE_NAME

        # 모델 학습 설정
        BATCH_SIZE = 32
        EPOCHS = 100
        VALIDATION_SPLIT = 0.2
        EARLY_STOPPING_PATIENCE = 10
        LEARNING_RATE = 0.001
        LSTM_UNITS = 50
        DROPOUT_RATE = 0.2

        # 로깅 설정
        LOG_LEVEL = "INFO"
        LOG_FILE = LOGS_DIR / "climate_prediction.log"

        # 예측 설정
        PREDICTION_MONTHS = 12

        @classmethod
        def setup_logging(cls):
            """로깅 설정"""
            numeric_level = getattr(logging, cls.LOG_LEVEL.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError(f"Invalid log level: {cls.LOG_LEVEL}")

            cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)

            logging.basicConfig(
                level=numeric_level,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                handlers=[
                    logging.FileHandler(cls.LOG_FILE),
                    logging.StreamHandler()
                ],
            )

        @classmethod
        def validate_config(cls):
            """필수 설정 검증"""
            if not cls.WEATHER_API_KEY:
                raise ValueError("API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")

            try:
                datetime.strptime(cls.START_DATE, "%Y%m")
            except ValueError:
                raise ValueError("시작 날짜 형식이 잘못되었습니다. YYYYMM 형식이어야 합니다.")

            # 필요한 디렉토리 생성
            directories = [
                cls.APP_DIR,
                cls.DATA_DIR,
                cls.TESTS_DIR,
                cls.API_DIR,
                cls.CORE_DIR,
                cls.MODELS_DIR,
                cls.SERVICES_DIR,
                cls.UTILS_DIR,
                cls.CLIMATE_MODEL_DIR,
                cls.LOGS_DIR,
            ]

            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)

            if not cls.DATA_FEATURES:
                raise ValueError("DATA_FEATURES가 설정되지 않았습니다.")

            # 모델 파라미터 검증
            if cls.MONTH_SEQUENCE_LENGTH < 1:
                raise ValueError("MONTH_SEQUENCE_LENGTH는 1 이상이어야 합니다.")
            if cls.EPOCHS < 1:
                raise ValueError("EPOCHS는 1 이상이어야 합니다.")
            if not (0 < cls.VALIDATION_SPLIT < 1):
                raise ValueError("VALIDATION_SPLIT는 0과 1 사이여야 합니다.")
            if not (0 <= cls.DROPOUT_RATE < 1):
                raise ValueError("DROPOUT_RATE는 0과 1 사이여야 합니다.")
            if cls.LSTM_UNITS < 1:
                raise ValueError("LSTM_UNITS는 1 이상이어야 합니다.")
            if cls.PREDICTION_MONTHS < 1:
                raise ValueError("PREDICTION_MONTHS는 1 이상이어야 합니다.")

        @classmethod
        def print_config(cls):
            """현재 설정 출력"""
            logger = logging.getLogger(__name__)
            logger.info("=== 현재 설정 ===")

            # 보안이 필요한 속성들
            sensitive_patterns = ["API_KEY", "PASSWORD", "SECRET", "TOKEN", "CREDENTIAL"]

            # 설정을 카테고리별로 정렬하여 출력
            categories = {
                "프로젝트 구조": [
                    "ROOT_DIR",
                    "APP_DIR",
                    "DATA_DIR",
                    "TESTS_DIR",
                    "LOGS_DIR",
                    "API_DIR",
                    "CORE_DIR",
                    "MODELS_DIR",
                    "SERVICES_DIR",
                    "UTILS_DIR",
                    "CLIMATE_MODEL_DIR",
                ],
                "API 설정": [
                    "API_BASE_URL",
                    "API_ENDPOINTS",
                    "API_RETRY_ATTEMPTS",
                    "API_RETRY_DELAY",
                    "API_TIMEOUT",
                ],
                "데이터 설정": ["STATION_ID", "START_DATE", "END_DATE", "MONTH_SEQUENCE_LENGTH", "DATA_FEATURES"],
                "모델 파일": ["MODEL_FILE", "SCALER_FILE", "SEQUENCE_FILE", "LAST_DATE_FILE"],
                "모델 설정": [
                    "BATCH_SIZE",
                    "EPOCHS",
                    "VALIDATION_SPLIT",
                    "EARLY_STOPPING_PATIENCE",
                    "LEARNING_RATE",
                    "LSTM_UNITS",
                    "DROPOUT_RATE",
                ],
                "로깅 설정": ["LOG_LEVEL", "LOG_FILE"],
                "예측 설정": ["PREDICTION_MONTHS"],
            }

            for category, attributes in categories.items():
                logger.info(f"\n[{category}]")
                for attr in attributes:
                    if hasattr(cls, attr):
                        value = getattr(cls, attr)
                        # 민감한 정보인 경우 마스킹
                        if any(pattern in attr.upper() for pattern in sensitive_patterns):
                            masked_value = "****"
                        else:
                            masked_value = value
                        logger.info(f"{attr}: {masked_value}")

    Config.setup_logging()
    Config.validate_config()

except FileNotFoundError as e:
    print(f"Error: {e}")
