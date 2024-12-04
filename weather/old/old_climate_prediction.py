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
import os
from dotenv import load_dotenv
import logging
from pathlib import Path
from config import Config

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClimatePredictor:
    def __init__(self):
        self.base_url = Config.API_BASE_URL + Config.API_ENDPOINTS["monthly_summary"]
        self.scaler = MinMaxScaler()
        self.model = None
        self.model_path = Path(Config.MODEL_PATH)
        self.model_file = self.model_path / "model.keras"  # .h5 대신 .keras 사용
        self.sequence_file = self.model_path / Config.SEQUENCE_DATA_NAME
        self.last_date_file = self.model_path / Config.LAST_DATE_NAME
        self.scaler_file = self.model_path / "scaler.pkl"  # scaler 저장 파일 추가
        self.model_path.mkdir(parents=True, exist_ok=True)

        # aiohttp 세션 설정
        self.timeout = aiohttp.ClientTimeout(total=20)
        self.max_retries = 3
        self.retry_delay = 1
        self.semaphore = asyncio.Semaphore(10)

    async def _get_monthly_data_async(self, year, month, session):
        """특정 연월의 기후 데이터 비동기 조회"""
        params = {
            "pageNo": 1,
            "numOfRows": 999,
            "dataType": "XML",
            "year": str(year),
            "month": f"{month:02d}",
            "authKey": Config.WEATHER_API_KEY,
        }

        for retry in range(self.max_retries):
            try:
                async with self.semaphore:
                    async with session.get(self.base_url, params=params, timeout=self.timeout) as response:
                        if response.status == 200:
                            content = await response.text()
                            root = ET.fromstring(content)
                            data = self._parse_weather_data(root, year, month)
                            logger.info(f"Successfully fetched data for {year}-{month}")
                            return data
                        else:
                            logger.warning(f"Failed to fetch data for {year}-{month}: Status {response.status}")
            except Exception as e:
                if retry < self.max_retries - 1:
                    logger.warning(f"Retry {retry + 1} for {year}-{month}: {str(e)}")
                    await asyncio.sleep(self.retry_delay * (retry + 1))
                else:
                    logger.error(f"Failed after {self.max_retries} retries for {year}-{month}: {str(e)}")
        return None

    async def fetch_data_async(self, start_year=2016):
        """월별 기후 데이터 비동기 수집"""
        current_date = datetime.now()
        end_year = current_date.year
        end_month = current_date.month - 1

        if end_month == 0:
            end_month = 12
            end_year -= 1

        logger.info(f"데이터 수집 기간: {start_year}년 1월 ~ {end_year}년 {end_month}월")

        async with aiohttp.ClientSession() as session:
            tasks = []
            for year in range(start_year, end_year + 1):
                for month in range(1, 13):
                    if year == end_year and month > end_month:
                        break
                    tasks.append(self._get_monthly_data_async(year, month, session))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            all_data = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Error in batch {i}: {str(result)}")
                elif result is not None:
                    if isinstance(result, list):
                        all_data.extend(result)
                    else:
                        logger.error(f"Unexpected data type for {i}: {type(result)}")

        return pd.DataFrame(all_data)

    def fetch_data(self, start_year=2016):
        """동기 메서드로 비동기 함수 실행"""
        return asyncio.run(self.fetch_data_async(start_year))

    def _parse_weather_data(self, root, year, month):
        """XML 데이터 파싱"""
        data = []
        for info in root.findall(".//info"):
            try:

                def safe_float(value):
                    return float(value) if value and value != "null" else 0.0

                row = {
                    "date": f"{year}-{month:02d}",
                    "station": info.findtext("stnko", ""),
                    "avg_temp": safe_float(info.findtext("taavg")),
                    "max_temp": safe_float(info.findtext("tamax")),
                    "min_temp": safe_float(info.findtext("tamin")),
                    "humidity": safe_float(info.findtext("avghm")),
                }
                data.append(row)
            except (ValueError, TypeError) as e:
                logger.error(f"Error parsing data for {year}-{month}: {e}")
                continue
        return data

    def prepare_model_data(self, df, sequence_length=Config.MONTH_SEQUENCE_LENGTH):
        """모델 학습용 데이터 준비"""
        df_seoul = df[df["station"] == "서울"].sort_values("date")
        logger.info(f"서울 데이터 수: {len(df_seoul)} 개월")

        features = Config.DATA_FEATURES
        df_features = df_seoul[features]

        # 데이터 정규화
        scaled_data = self.scaler.fit_transform(df_features)

        # scaler 저장
        from joblib import dump

        dump(self.scaler, self.scaler_file)
        logger.info(f"Scaler saved to {self.scaler_file}")

        X, y = [], []
        for i in range(len(scaled_data) - sequence_length):
            X.append(scaled_data[i : (i + sequence_length)])
            y.append(scaled_data[i + sequence_length])

        return np.array(X), np.array(y), df_seoul["date"].iloc[-1]

    def build_model(self, input_shape):
        """LSTM 모델 구축"""
        sequence_length = input_shape[0]
        n_features = input_shape[1]

        model = Sequential(
            [
                LSTM(Config.LSTM_UNITS, return_sequences=True, input_shape=(sequence_length, n_features)),
                Dropout(Config.DROPOUT_RATE),
                LSTM(Config.LSTM_UNITS),
                Dropout(Config.DROPOUT_RATE),
                Dense(n_features),
            ]
        )

        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=Config.LEARNING_RATE), loss=keras.losses.MeanSquaredError()
        )
        return model

    def save_model(self, model, last_sequence, last_date):
        """모델과 관련 데이터 저장"""
        try:
            # 모델을 .keras 형식으로 저장
            model.save(self.model_file)

            # last_sequence가 유효한지 확인
            if last_sequence is not None:
                np.save(self.sequence_file, last_sequence)
            else:
                logger.error("저장할 시퀀스 데이터가 없습니다.")
                return False

            with open(self.last_date_file, "w") as f:
                f.write(last_date)

            logger.info(f"모델과 데이터가 저장되었습니다: {self.model_path}")
            return True
        except Exception as e:
            logger.error(f"모델 저장 중 오류 발생: {e}")
            return False

    def load_model(self):
        """저장된 모델과 데이터 로드"""
        try:
            required_files = [self.model_file, self.sequence_file, self.last_date_file, self.scaler_file]
            if not all(f.exists() for f in required_files):
                logger.warning("저장된 모델 또는 데이터가 없습니다.")
                return None, None, None

            # scaler 로드
            from joblib import load

            self.scaler = load(self.scaler_file)
            logger.info(f"Scaler loaded from {self.scaler_file}")

            # 커스텀 객체와 함께 모델 로드
            custom_objects = {"MeanSquaredError": keras.losses.MeanSquaredError}
            model = load_model(self.model_file, custom_objects=custom_objects)

            last_sequence = np.load(self.sequence_file)
            with open(self.last_date_file, "r") as f:
                last_date = f.read().strip()

            logger.info(f"모델과 데이터를 로드했습니다: {self.model_file}")
            return model, last_sequence, last_date
        except Exception as e:
            logger.error(f"모델 로드 중 오류 발생: {e}")
            return None, None, None

    def predict_future(self, model, last_sequence, steps=Config.PREDICTION_MONTHS):
        """미래 기후 예측"""
        if last_sequence is None:
            logger.error("예측을 위한 시퀀스 데이터가 없습니다.")
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
            logger.error(f"예측 중 오류 발생: {e}")
            return None


def main():
    predictor = ClimatePredictor()

    try:
        # 저장된 모델이 있는지 확인
        model, last_sequence, last_date = predictor.load_model()

        if model is None:
            # 새로운 모델 학습
            logger.info("새로운 모델을 학습합니다...")

            # 데이터 수집
            logger.info("데이터 수집 중...")
            df = predictor.fetch_data()

            if len(df) == 0:
                logger.error("데이터 수집 실패")
                return

            # 모델 데이터 준비
            logger.info("데이터 전처리 중...")
            X, y, last_date = predictor.prepare_model_data(df)

            if len(X) == 0:
                logger.error("데이터 전처리 실패")
                return

            # 모델 학습
            logger.info("모델 학습 중...")
            model = predictor.build_model((X.shape[1], X.shape[2]))

            # Early Stopping 콜백 추가
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

            # 마지막 시퀀스 저장
            last_sequence = X[-1]

            # 모델 저장
            if not predictor.save_model(model, last_sequence, last_date):
                logger.error("모델 저장 실패")
                return
        else:
            logger.info(f"저장된 모델을 불러왔습니다. 마지막 학습 데이터: {last_date}")

        # last_sequence 확인
        if last_sequence is None:
            logger.error("예측에 필요한 시퀀스 데이터가 없습니다.")
            return

        # 미래 예측
        logger.info(f"\n=== 향후 {Config.PREDICTION_MONTHS}개월 예측 결과 ===")
        predictions = predictor.predict_future(model, last_sequence)

        if predictions is None:
            logger.error("예측 실패")
            return

        if last_date is None:
            logger.error("날짜 정보를 가져올 수 없습니다.")
            return

        last_date = datetime.strptime(last_date, "%Y-%m")
        features = Config.DATA_FEATURES

        for i, pred in enumerate(predictions, 1):
            future_date = last_date + pd.DateOffset(months=i)
            pred_str = ", ".join([f"{feature}: {value:.1f}" for feature, value in zip(features, pred)])
            logger.info(f"{future_date.strftime('%Y-%m')}: {pred_str}")

    except Exception as e:
        logger.error(f"프로그램 실행 중 오류 발생: {e}")


if __name__ == "__main__":
    main()
