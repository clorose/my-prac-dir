# path : models/weather/model_manager.py
# description : 날씨 예측을 위한 모델 관리 모듈

"""
기후 예측을 위한 모델 관리 모듈.

이 모듈은 학습된 모델, 시퀀스, 스케일러의 저장 및 로딩을 포함한
모델 지속성, 데이터 준비, 모델 수명주기 관리를 처리합니다.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple

import keras
import numpy as np
import pandas as pd
from keras.models import Sequential, load_model
from joblib import dump, load
from sklearn.preprocessing import MinMaxScaler

from config import Config

logger = logging.getLogger(__name__)


class ModelManager:
    """
    Manages model lifecycle including data preparation, persistence, and loading.

    This class handles:
    - Data preparation and scaling for model training
    - Model and associated data persistence
    - Loading saved models and their associated data
    """

    def __init__(self):
        """Initialize model manager with required paths and scaler."""
        self._initialize_paths()
        self.scaler = MinMaxScaler()

    def _initialize_paths(self) -> None:
        """Set up directories and file paths for model persistence."""
        self.model_path = Path(Config.CLIMATE_MODEL_DIR)
        self.model_file = Config.MODEL_FILE
        self.sequence_file = Config.SEQUENCE_FILE
        self.last_date_file = Config.LAST_DATE_FILE
        self.scaler_file = Config.SCALER_FILE
        self.model_path.mkdir(parents=True, exist_ok=True)

    def prepare_model_data(
        self,
        df: pd.DataFrame,
        sequence_length: int = Config.MONTH_SEQUENCE_LENGTH
    ) -> Tuple[np.ndarray, np.ndarray, str]:
        """
        Prepare and scale data for model training.

        Args:
            df: Input DataFrame containing weather data
            sequence_length: Length of input sequences for LSTM

        Returns:
            Tuple containing:
            - Input sequences array
            - Target values array
            - Last date in the dataset
            
        Raises:
            ValueError: If DataFrame is empty or has insufficient data
        """
        if df.empty:
            raise ValueError("Empty DataFrame provided")

        df_seoul = df[df["station"] == "서울"].sort_values("date")
        if df_seoul.empty:
            raise ValueError("No data found for Seoul station")

        logger.info("서울 데이터 수: %d 개월", len(df_seoul))

        features = Config.DATA_FEATURES
        df_features = df_seoul[features]

        scaled_data = self.scaler.fit_transform(df_features)
        dump(self.scaler, self.scaler_file)
        logger.info("Scaler saved to %s", self.scaler_file)

        if len(scaled_data) <= sequence_length:
            raise ValueError(
                f"Not enough data points. Need > {sequence_length}, "
                f"got {len(scaled_data)}"
            )

        input_sequences = np.array([
            scaled_data[i : i + sequence_length]
            for i in range(len(scaled_data) - sequence_length)
        ])
        target_values = np.array([
            scaled_data[i]
            for i in range(sequence_length, len(scaled_data))
        ])

        return input_sequences, target_values, df_seoul["date"].iloc[-1]

    def save_model(
        self,
        model: Sequential,
        last_sequence: np.ndarray,
        last_date: str
    ) -> bool:
        """
        Save model and associated data to disk.

        Args:
            model: Trained Keras Sequential model
            last_sequence: Last input sequence for predictions
            last_date: Last date in the training dataset

        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            if last_sequence is None:
                raise ValueError("No sequence data to save")

            model.save(self.model_file)
            np.save(self.sequence_file, last_sequence)

            with open(self.last_date_file, "w", encoding="utf-8") as f:
                f.write(last_date)

            logger.info("Model and data saved to: %s", self.model_path)
            return True
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Error saving model: %s", str(exc))
            return False

    def load_model(
        self
    ) -> Tuple[Optional[Sequential], Optional[np.ndarray], Optional[str]]:
        """
        Load saved model and associated data.

        Returns:
            Tuple containing:
            - Loaded Keras model or None
            - Last sequence data or None
            - Last training date or None
        """
        try:
            required_files = [
                self.model_file,
                self.sequence_file,
                self.last_date_file,
                self.scaler_file
            ]
            if not all(f.exists() for f in required_files):
                logger.warning("Some model files are missing")
                return None, None, None

            self.scaler = load(self.scaler_file)
            custom_objects = {"MeanSquaredError": keras.losses.MeanSquaredError}
            model = load_model(self.model_file, custom_objects=custom_objects)

            last_sequence = np.load(self.sequence_file)
            with open(self.last_date_file, "r", encoding="utf-8") as f:
                last_date = f.read().strip()

            logger.info("Model loaded from: %s", self.model_file)
            return model, last_sequence, last_date
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Error loading model: %s", str(exc))
            return None, None, None