# Path: D:\git\weather\legacy\climate_prediction.py
# Purpose: [Describe the purpose of this file]

import numpy as np
import pandas as pd
import aiohttp
import asyncio
import xml.etree.ElementTree as ET
from datetime import datetime
import keras
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import sys
import logging
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # weather 디렉토리
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from config import Config

# 로깅 설정 개선
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(Config.LOG_FILE), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class ClimatePredictor:
    def __init__(self):
        """기후 예측 시스템 초기화"""
        self._initialize_paths()  # 경로 초기화
        self._initialize_api_settings()  # API 설정 초기화
        self.scaler = MinMaxScaler()  # 데이터 정규화를 위한 스케일러
        self.model = None  # 머신러닝 모델

    def _initialize_paths(self) -> None:
        """경로 설정 초기화"""
        self.model_path = Path(Config.CLIMATE_MODEL_DIR)
        self.model_file = Config.MODEL_FILE
        self.sequence_file = Config.SEQUENCE_FILE
        self.last_date_file = Config.LAST_DATE_FILE
        self.scaler_file = Config.SCALER_FILE
        self.model_path.mkdir(parents=True, exist_ok=True)

    def _initialize_api_settings(self) -> None:
        """API 설정 초기화"""
        self.base_url = Config.API_BASE_URL + Config.API_ENDPOINTS["monthly_summary"]
        self.timeout = aiohttp.ClientTimeout(total=Config.API_TIMEOUT)
        self.max_retries = Config.API_RETRY_ATTEMPTS
        self.retry_delay = Config.API_RETRY_DELAY
        self.semaphore = asyncio.Semaphore(10)

    async def _get_monthly_data_async(
        self, year: int, month: int, session: aiohttp.ClientSession
    ) -> Optional[List[Dict]]:
        """
        특정 연월의 기후 데이터를 비동기적으로 조회
        Args:
            year: 조회할 연도
            month: 조회할 월
            session: aiohttp 세션
        Returns:
            기후 데이터 리스트 또는 None
        """
        params = {
            "pageNo": "1",
            "numOfRows": "999",
            "dataType": "XML",
            "year": str(year),
            "month": f"{month:02d}",
            "authKey": Config.WEATHER_API_KEY,
        }

        for retry in range(self.max_retries):
            try:
                async with self.semaphore:
                    async with session.get(self.base_url, params=params, timeout=self.timeout) as response:
                        content = await response.text()

                        if response.status == 200:
                            try:
                                root = ET.fromstring(content)
                                result_code = root.findtext(".//resultCode")
                                result_msg = root.findtext(".//resultMsg")

                                if result_code != "00":
                                    logger.error(f"API Error for {year}-{month:02d}: {result_code} - {result_msg}")
                                    return None

                                data = self._parse_weather_data(root, year, month)
                                if data:
                                    logger.info(f"Successfully fetched {len(data)} records for {year}-{month:02d}")
                                    return data
                                logger.warning(f"No data found for {year}-{month:02d}")
                            except ET.ParseError as e:
                                logger.error(f"XML Parse Error for {year}-{month:02d}: {str(e)}")
                        else:
                            logger.error(f"HTTP {response.status} for {year}-{month:02d}")

            except asyncio.TimeoutError:
                logger.error(f"Timeout for {year}-{month:02d} (attempt {retry + 1})")
            except Exception as e:
                logger.error(f"Error for {year}-{month:02d} (attempt {retry + 1}): {str(e)}")

            if retry < self.max_retries - 1:
                await asyncio.sleep(self.retry_delay * (retry + 1))

        return None

    def _parse_weather_data(self, root: ET.Element, year: int, month: int) -> List[Dict[str, Any]]:
        """XML 데이터 파싱"""
        data = []
        for idx, info in enumerate(root.findall(".//info")):
            try:
                def safe_float(value: Optional[str], field_name: str) -> float:
                    if not value or value == "null":
                        return 0.0
                    try:
                        return float(value)
                    except ValueError:
                        logger.error(f"Invalid {field_name} value: {value} in {year}-{month}")
                        return 0.0

                row = {
                    "date": f"{year}-{month:02d}",
                    "station": info.findtext("stnko", ""),
                    "avg_temp": safe_float(info.findtext("taavg"), "avg_temp"),
                    "max_temp": safe_float(info.findtext("tamax"), "max_temp"),
                    "min_temp": safe_float(info.findtext("tamin"), "min_temp"),
                    "humidity": safe_float(info.findtext("avghm"), "humidity"),
                }

                if not row["station"]:
                    logger.warning(f"Empty station name in record {idx} for {year}-{month}")
                    continue

                data.append(row)

            except Exception as e:
                logger.error(f"Error parsing record {idx} for {year}-{month}: {str(e)}")
                continue

        return data

    async def fetch_data_async(self, start_year: int = 2016) -> pd.DataFrame:
        """월별 기후 데이터 비동기 수집"""
        current_date = datetime.now()
        end_year = current_date.year
        end_month = current_date.month - 1 if current_date.month > 1 else 12
        end_year = end_year if current_date.month > 1 else end_year - 1

        logger.info(f"데이터 수집 기간: {start_year}년 1월 ~ {end_year}년 {end_month}월")

        async with aiohttp.ClientSession() as session:
            tasks = [
                self._get_monthly_data_async(year, month, session)
                for year in range(start_year, end_year + 1)
                for month in range(1, 13)
                if not (year == end_year and month > end_month)
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            all_data = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Error in batch {i}: {str(result)}")
                elif isinstance(result, list):
                    all_data.extend(result)
                elif result is not None:
                    logger.error(f"Unexpected data type for batch {i}: {type(result)}")

        df = pd.DataFrame(all_data)
        if df.empty:
            logger.error("No data collected")
        return df

    def fetch_data(self, start_year: int = 2016) -> pd.DataFrame:
        """동기 메서드로 비동기 함수 실행"""
        return asyncio.run(self.fetch_data_async(start_year))

    def prepare_model_data(
        self, df: pd.DataFrame, sequence_length: int = Config.MONTH_SEQUENCE_LENGTH
    ) -> Tuple[np.ndarray, np.ndarray, str]:
        """
        모델 학습용 데이터 준비
        Args:
            df: 원본 데이터프레임
            sequence_length: 시퀀스 길이
        Returns:
            X: 입력 데이터
            y: 타겟 데이터
            last_date: 마지막 데이터 날짜
        """
        if df.empty:
            raise ValueError("Empty DataFrame provided")

        df_seoul = df[df["station"] == "서울"].sort_values("date")
        if df_seoul.empty:
            raise ValueError("No data found for Seoul station")

        logger.info(f"서울 데이터 수: {len(df_seoul)} 개월")

        features = Config.DATA_FEATURES
        df_features = df_seoul[features]

        # 데이터 정규화
        scaled_data = self.scaler.fit_transform(df_features)

        # scaler 저장
        from joblib import dump
        dump(self.scaler, self.scaler_file)
        logger.info(f"Scaler saved to {self.scaler_file}")

        if len(scaled_data) <= sequence_length:
            raise ValueError(f"Not enough data points. Need > {sequence_length}, got {len(scaled_data)}")

        X = np.array([scaled_data[i : i + sequence_length] for i in range(len(scaled_data) - sequence_length)])
        y = np.array([scaled_data[i] for i in range(sequence_length, len(scaled_data))])

        return X, y, df_seoul["date"].iloc[-1]

    def build_model(self, input_shape: Tuple[int, int]) -> Sequential:
        """
        LSTM 모델 구축
        Args:
            input_shape: 입력 데이터 형태
        Returns:
            구축된 LSTM 모델
        """
        model = Sequential(
            [
                LSTM(Config.LSTM_UNITS, return_sequences=True, input_shape=input_shape),
                Dropout(Config.DROPOUT_RATE),
                LSTM(Config.LSTM_UNITS),
                Dropout(Config.DROPOUT_RATE),
                Dense(input_shape[1]),
            ]
        )

        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=Config.LEARNING_RATE), loss=keras.losses.MeanSquaredError()
        )
        return model

    def save_model(self, model: Sequential, last_sequence: np.ndarray, last_date: str) -> bool:
        """모델과 관련 데이터 저장"""
        try:
            if last_sequence is None:
                raise ValueError("No sequence data to save")

            model.save(self.model_file)
            np.save(self.sequence_file, last_sequence)

            with open(self.last_date_file, "w") as f:
                f.write(last_date)

            logger.info(f"Model and data saved to: {self.model_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False

    def load_model(self) -> Tuple[Optional[Sequential], Optional[np.ndarray], Optional[str]]:
        """저장된 모델과 데이터 로드"""
        try:
            required_files = [self.model_file, self.sequence_file, self.last_date_file, self.scaler_file]
            if not all(f.exists() for f in required_files):
                logger.warning("Some model files are missing")
                return None, None, None

            from joblib import load
            self.scaler = load(self.scaler_file)
            # 커스텀 오브젝트
            custom_objects = {"MeanSquaredError": keras.losses.MeanSquaredError}
            model = load_model(self.model_file, custom_objects=custom_objects)

            last_sequence = np.load(self.sequence_file)
            with open(self.last_date_file, "r") as f:
                last_date = f.read().strip()

            logger.info(f"Model loaded from: {self.model_file}")
            return model, last_sequence, last_date
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return None, None, None

    def predict_future(
        self, model: Sequential, last_sequence: np.ndarray, steps: int = Config.PREDICTION_MONTHS
    ) -> Optional[np.ndarray]:
        """
        미래 기후 예측
        Args:
            model: 학습된 모델
            last_sequence: 마지막 시퀀스 데이터
            steps: 예측할 개월 수
        Returns:
            예측된 기후 데이터
        """
        if last_sequence is None:
            logger.error("No sequence data for prediction")
            return None

        try:
            predictions = []
            current_sequence = last_sequence.copy()

            for _ in range(steps):
                next_pred = model.predict(current_sequence.reshape(1, *current_sequence.shape), verbose=0)
                predictions.append(next_pred[0])

                current_sequence = np.roll(current_sequence, -1, axis=0)
                current_sequence[-1] = next_pred[0]

            predictions = np.array(predictions)
            return self.scaler.inverse_transform(predictions)
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return None


def main():
    """
    메인 실행 함수
    1. 모델 로드 또는 새로운 모델 학습
    2. 데이터 수집 및 전처리
    3. 모델 학습 (필요한 경우)
    4. 미래 기후 예측
    """
    predictor = ClimatePredictor()

    try:
        # 모델 로드 또는 새로 학습
        model, last_sequence, last_date = predictor.load_model()

        if model is None:
            logger.info("Starting new model training...")

            # 데이터 수집
            logger.info("Collecting data...")
            df = predictor.fetch_data()
            if df.empty:
                raise ValueError("Failed to collect data")

            # 데이터 전처리
            logger.info("Preprocessing data...")
            X, y, last_date = predictor.prepare_model_data(df)
            if len(X) == 0:
                raise ValueError("Failed to preprocess data")

            # 모델 학습
            logger.info("Training model...")
            model = predictor.build_model((X.shape[1], X.shape[2]))

            early_stopping = keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=Config.EARLY_STOPPING_PATIENCE, restore_best_weights=True
            )

            history = model.fit(
                X,
                y,
                epochs=Config.EPOCHS,
                batch_size=Config.BATCH_SIZE,
                validation_split=Config.VALIDATION_SPLIT,
                callbacks=[early_stopping],
                verbose=1,
            )

            last_sequence = X[-1]
            if not predictor.save_model(model, last_sequence, last_date):
                raise ValueError("Failed to save model")
        else:
            logger.info(f"Loaded existing model. Last training date: {last_date}")

        # 예측 실행
        if last_sequence is None:
            raise ValueError("No sequence data for prediction")

        logger.info(f"\n=== {Config.PREDICTION_MONTHS} Month Forecast ===")
        predictions = predictor.predict_future(model, last_sequence)

        if predictions is None:
            raise ValueError("Failed to generate predictions")

        if last_date is None:
            raise ValueError("No date information available")

        # 예측 결과 출력
        last_date = datetime.strptime(last_date, "%Y-%m")
        features = Config.DATA_FEATURES

        for i, pred in enumerate(predictions, 1):
            future_date = last_date + pd.DateOffset(months=i)
            pred_str = ", ".join(f"{feature}: {value:.1f}" for feature, value in zip(features, pred))
            logger.info(f"{future_date.strftime('%Y-%m')}: {pred_str}")

    except ValueError as e:
        logger.error(f"Value Error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
