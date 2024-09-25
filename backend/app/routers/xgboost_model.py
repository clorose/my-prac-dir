from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
from ..models.xg_model import xg_model

router = APIRouter()

class PredictionInput(BaseModel):
    temperature: float
    pressure: float
    speed: float
    tool_wear: float
    material_hardness: float
    vibration: float
    power_consumption: float

@router.post("/xgboost/predict")
async def predict(input: PredictionInput):
    input_data = np.array([[
        input.temperature, input.pressure, input.speed, input.tool_wear,
        input.material_hardness, input.vibration, input.power_consumption
    ]])
    prediction = xg_model.predict(input_data)
    return {"prediction": int(prediction[0])}

@router.get("/xgboost/model-performance")
async def model_performance():
    accuracy, report = xg_model.get_model_performance()
    return {
        "accuracy": accuracy,
        "classification_report": report
    }

@router.get("/xgboost/feature-importance")
async def feature_importance():
    return xg_model.get_feature_importance()

@router.get("/xgboost/scatter-data")
async def scatter_data():
    scatter_data, top_features = xg_model.get_scatter_data()
    return {
        "scatter_data": scatter_data,
        "top_features": top_features
    }