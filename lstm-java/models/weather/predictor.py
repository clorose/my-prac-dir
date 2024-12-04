# path : models/weather/predictor.py
# description : 날씨 예측을 위한 예측 모듈

"""
기후 예측을 위한 모듈입니다.

이 모듈은 과거 데이터를 기반으로 미래 날씨 패턴을 예측하기 위한
LSTM 모델을 구축, 훈련 및 사용하는 기능을 제공합니다.
"""

import logging
from typing import Optional, Tuple

import numpy as np
from keras import optimizers, losses
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout

from config import Config
from data_collector import WeatherDataCollector
from model_manager import ModelManager

logger = logging.getLogger(__name__)


class ClimatePredictor:
    """
    Main predictor class for climate forecasting.

    Integrates data collection, model management, and prediction functionality
    to provide end-to-end climate prediction capabilities using LSTM models.
    """

    def __init__(self):
        """Initialize predictor with data collector and model manager."""
        self.data_collector = WeatherDataCollector()
        self.model_manager = ModelManager()

    def build_model(self, input_shape: Tuple[int, int]) -> Sequential:
        """
        Build and compile LSTM model for climate prediction.

        Args:
            input_shape: Shape of input data (sequence_length, features)

        Returns:
            Compiled Keras Sequential model
        """
        model = Sequential([
            LSTM(
                Config.LSTM_UNITS,
                return_sequences=True,
                input_shape=input_shape
            ),
            Dropout(Config.DROPOUT_RATE),
            LSTM(Config.LSTM_UNITS),
            Dropout(Config.DROPOUT_RATE),
            Dense(input_shape[1])
        ])

        model.compile(
            optimizer=optimizers.Adam(
                learning_rate=Config.LEARNING_RATE
            ),
            loss=losses.MeanSquaredError()
        )
        return model

    def predict_future(
        self,
        model: Sequential,
        last_sequence: np.ndarray,
        steps: int = Config.PREDICTION_MONTHS
    ) -> Optional[np.ndarray]:
        """
        Generate future climate predictions.

        Args:
            model: Trained LSTM model
            last_sequence: Last known sequence of climate data
            steps: Number of future steps to predict

        Returns:
            Numpy array of predictions or None if prediction fails
        """
        if last_sequence is None:
            logger.error("No sequence data for prediction")
            return None

        try:
            predictions = []
            current_sequence = last_sequence.copy()

            for _ in range(steps):
                next_pred = model.predict(
                    current_sequence.reshape(1, *current_sequence.shape),
                    verbose=0
                )
                predictions.append(next_pred[0])

                current_sequence = np.roll(current_sequence, -1, axis=0)
                current_sequence[-1] = next_pred[0]

            predictions = np.array(predictions)
            return self.model_manager.scaler.inverse_transform(predictions)
            
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Prediction error: %s", str(exc))
            return None