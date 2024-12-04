# path : models/weather/app.py
# description : 날씨 예측 API 서버

"""
날씨 예측 API 서버

이 모듈은 학습된 LSTM 모델을 사용하여 날씨 예측을 제공하는 FastAPI 애플리케이션입니다.
건강 체크, 예측, 모델 학습을 위한 엔드포인트를 포함합니다.
"""

from datetime import datetime
import logging
from typing import Dict, List, Union

import uvicorn
from fastapi import FastAPI, HTTPException
import pandas as pd
from keras import callbacks

from config import Config
from predictor import ClimatePredictor

logger = logging.getLogger(__name__)

app = FastAPI(
    title="날씨 예측 API",
    description="LSTM 모델을 사용한 날씨 예측 API",
    version="1.0.0"
)

predictor = ClimatePredictor()


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    API 상태 확인을 위한 헬스 체크 엔드포인트

    Returns:
        API 상태를 포함하는 딕셔너리
    """
    return {"status": "healthy"}


@app.get("/predict")
async def predict_weather() -> Dict[str, Union[str, List[Dict]]]:
    """
    학습된 모델을 사용하여 날씨 예측을 생성합니다.

    Returns:
        예측 상태와 결과를 포함하는 딕셔너리

    Raises:
        HTTPException: 다양한 이유로 예측이 실패할 경우 발생
    """
    try:
        model, sequence, date = predictor.model_manager.load_model()

        if model is None:
            logger.info("새로운 모델 학습 시작...")

            logger.info("데이터 수집 중...")
            data_frame = predictor.data_collector.fetch_data()
            if data_frame.empty:
                raise ValueError("데이터 수집 실패")

            logger.info("데이터 전처리 중...")
            features, targets, date = predictor.model_manager.prepare_model_data(data_frame)
            if not features:
                raise ValueError("데이터 전처리 실패")

            logger.info("모델 학습 중...")
            model = predictor.build_model((features.shape[1], features.shape[2]))

            early_stopping = callbacks.EarlyStopping(
                monitor="val_loss",
                patience=Config.EARLY_STOPPING_PATIENCE,
                restore_best_weights=True
            )

            model.fit(
                features,
                targets,
                epochs=Config.EPOCHS,
                batch_size=Config.BATCH_SIZE,
                validation_split=Config.VALIDATION_SPLIT,
                callbacks=[early_stopping],
                verbose=1
            )

            sequence = features[-1]
            if not predictor.model_manager.save_model(model, sequence, date):
                raise ValueError("모델 저장 실패")
        else:
            logger.info("기존 모델 로드 완료. 마지막 학습 날짜: %s", date)

        if sequence is None:
            raise ValueError("예측을 위한 시퀀스 데이터 없음")

        predictions = predictor.predict_future(model, sequence)

        if predictions is None or date is None:
            raise ValueError("예측 생성 실패")

        last_date = datetime.strptime(date, "%Y-%m")
        features = Config.DATA_FEATURES

        prediction_results = [
            {
                "date": (last_date + pd.DateOffset(months=i)).strftime("%Y-%m"),
                **{feature: float(value) for feature, value in zip(features, pred)}
            }
            for i, pred in enumerate(predictions, 1)
        ]

        return {
            "status": "success",
            "predictions": prediction_results
        }

    except ValueError as exc:
        logger.error("값 오류: %s", str(exc))
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.error("예기치 않은 오류: %s", str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/train")
async def train_model() -> Dict[str, Union[str, Dict[str, List[float]]]]:
    """
    새로운 데이터로 모델을 재학습합니다.

    Returns:
        학습 상태와 히스토리를 포함하는 딕셔너리

    Raises:
        HTTPException: 학습이 실패할 경우 발생
    """
    try:
        logger.info("새로운 모델 학습 시작...")

        data_frame = predictor.data_collector.fetch_data()
        if data_frame.empty:
            raise ValueError("데이터 수집 실패")

        features, targets, date = predictor.model_manager.prepare_model_data(data_frame)
        if not features:
            raise ValueError("데이터 전처리 실패")

        model = predictor.build_model((features.shape[1], features.shape[2]))
        early_stopping = callbacks.EarlyStopping(
            monitor="val_loss",
            patience=Config.EARLY_STOPPING_PATIENCE,
            restore_best_weights=True
        )

        history = model.fit(
            features,
            targets,
            epochs=Config.EPOCHS,
            batch_size=Config.BATCH_SIZE,
            validation_split=Config.VALIDATION_SPLIT,
            callbacks=[early_stopping],
            verbose=1
        )

        sequence = features[-1]
        if not predictor.model_manager.save_model(model, sequence, date):
            raise ValueError("모델 저장 실패")

        return {
            "status": "success",
            "message": "모델 학습 완료",
            "last_date": date,
            "training_history": {
                "loss": [float(loss) for loss in history.history["loss"]],
                "val_loss": [float(loss) for loss in history.history["val_loss"]]
            }
        }

    except Exception as exc:
        logger.error("학습 오류: %s", str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)