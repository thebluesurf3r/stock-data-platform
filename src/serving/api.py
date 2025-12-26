from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from src.serving.model_loader import ModelLoader


app = FastAPI(title="Stock Direction Prediction API")

MODEL_VERSION = "v1"
MODEL_BASE_PATH = "models/stock_direction"

model_loader = ModelLoader(MODEL_BASE_PATH)
model, metadata = model_loader.load(MODEL_VERSION)


class PredictionRequest(BaseModel):
    daily_return: float
    ma_7: float
    ma_14: float
    ma_30: float
    volatility_14: float


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_version": MODEL_VERSION
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    features = np.array([[
        req.daily_return,
        req.ma_7,
        req.ma_14,
        req.ma_30,
        req.volatility_14
    ]])

    prob = model.predict_proba(features)[0][1]
    pred = int(prob >= 0.5)

    return PredictionResponse(
        prediction=pred,
        probability=prob,
        model_version=MODEL_VERSION
    )
