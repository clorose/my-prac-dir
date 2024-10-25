# File: C:\gaon\2024\weather\config.py
# Purpose: [Describe the purpose of this file]

import os
from dotenv import load_dotenv
from pathlib import Path
import logging
from datetime import datetime

# .env 파일 로드
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """환경 설정 클래스"""

    # API 설정
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    API_BASE_URL = "https://apihub.kma.go.kr"
    API_ENDPOINTS = {
        "monthly_summary": "/api/typ02/openApi/SfcMtlyInfoService/getMmSumry",
        "monthly_summary2": "/api/typ02/openApi/SfcMtlyInfoService/getMmSumry2",
    }
    API_RETRY_ATTEMPTS = int(os.getenv("API_RETRY_ATTEMPTS", 3))
    API_RETRY_DELAY = int(os.getenv("API_RETRY_DELAY", 2))
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))

    # 데이터 설정
    STATION_ID = os.getenv("STATION_ID", "108")  # 서울
    START_DATE = os.getenv("START_DATE", "201601")  # YYYYMM 형식
    END_DATE = datetime.now().strftime("%Y%m")
    MONTH_SEQUENCE_LENGTH = int(os.getenv("MONTH_SEQUENCE_LENGTH", 12))
    DATA_FEATURES = os.getenv("DATA_FEATURES", "avg_temp,max_temp,min_temp,humidity").split(",")

    # 모델 설정
    MODEL_PATH = os.getenv("MODEL_PATH", "climate_model")
    MODEL_NAME = os.getenv("MODEL_NAME", "climate_predictor_model.h5")
    SEQUENCE_DATA_NAME = os.getenv("SEQUENCE_DATA_NAME", "last_sequence.npy")
    LAST_DATE_NAME = os.getenv("LAST_DATE_NAME", "last_date.txt")
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
    EPOCHS = int(os.getenv("EPOCHS", 100))
    VALIDATION_SPLIT = float(os.getenv("VALIDATION_SPLIT", 0.2))
    EARLY_STOPPING_PATIENCE = int(os.getenv("EARLY_STOPPING_PATIENCE", 10))
    LEARNING_RATE = float(os.getenv("LEARNING_RATE", 0.001))
    LSTM_UNITS = int(os.getenv("LSTM_UNITS", 50))
    DROPOUT_RATE = float(os.getenv("DROPOUT_RATE", 0.2))

    # 로깅 설정
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "climate_prediction.log")

    # 예측 설정
    PREDICTION_MONTHS = int(os.getenv("PREDICTION_MONTHS", 12))

    @classmethod
    def setup_logging(cls):
        """로깅 설정"""
        numeric_level = getattr(logging, cls.LOG_LEVEL.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {cls.LOG_LEVEL}")

        logging.basicConfig(
            level=numeric_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(cls.LOG_FILE), logging.StreamHandler()],
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

        required_paths = [cls.MODEL_PATH]
        for path in required_paths:
            os.makedirs(path, exist_ok=True)

        if not cls.DATA_FEATURES:
            raise ValueError("DATA_FEATURES가 설정되지 않았습니다.")

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
            "API 설정": [
                "WEATHER_API_KEY",
                "API_BASE_URL",
                "API_ENDPOINTS",
                "API_RETRY_ATTEMPTS",
                "API_RETRY_DELAY",
                "API_TIMEOUT",
            ],
            "데이터 설정": ["STATION_ID", "START_DATE", "END_DATE", "MONTH_SEQUENCE_LENGTH", "DATA_FEATURES"],
            "모델 설정": [
                "MODEL_PATH",
                "MODEL_NAME",
                "SEQUENCE_DATA_NAME",
                "LAST_DATE_NAME",
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
