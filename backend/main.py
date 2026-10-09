from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "ml" / "heatshield_model.pkl"
CLIMATE_DATA_PATH = BASE_DIR / "hyderabad_climate_data.csv"

app = FastAPI(title="HeatShield AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load(MODEL_PATH)


class ClimateData(BaseModel):
    temperature: float
    humidity: float
    rain: float
    wind_speed: float
    solar_radiation: float
    hour: int
    month: int
    day_of_year: int
    is_daytime: int


@app.get("/")
def home():
    return {
        "message": "HeatShield AI API is running",
        "model": "Random Forest"
    }


@app.post("/predict")
def predict(data: ClimateData):

    input_data = pd.DataFrame([{
        "temperature_2m": data.temperature,
        "relative_humidity_2m": data.humidity,
        "rain": data.rain,
        "wind_speed_10m": data.wind_speed,
        "shortwave_radiation": data.solar_radiation,
        "hour": data.hour,
        "month": data.month,
        "day_of_year": data.day_of_year,
        "is_daytime": data.is_daytime
    }])

    probabilities = model.predict_proba(input_data)[0]
    prediction = str(model.predict(input_data)[0])
    confidence = max(probabilities) * 100

    risk_levels = {
        "Low": 0,
        "Moderate": 100 / 3,
        "High": 200 / 3,
        "Critical": 100,
    }
    risk_score = sum(
        probability * risk_levels[str(risk)]
        for risk, probability in zip(model.classes_, probabilities)
    )

    if data.temperature > 50:
        prediction = "High"
        risk_score = max(risk_score, risk_levels["High"])

    return {
        "risk": prediction,
        "risk_score": round(risk_score, 2),
        "confidence": round(confidence, 2)
    }


@app.get("/current-climate")
def current_climate():

    df = pd.read_csv(CLIMATE_DATA_PATH)

    latest = df.iloc[-1]

    time = pd.to_datetime(latest["time"])

    return {
        "time": str(time),
        "temperature": float(latest["temperature_2m"]),
        "humidity": float(latest["relative_humidity_2m"]),
        "rain": float(latest["rain"]),
        "wind_speed": float(latest["wind_speed_10m"]),
        "solar_radiation": float(latest["shortwave_radiation"]),
        "hour": int(time.hour),
        "month": int(time.month),
        "day_of_year": int(time.dayofyear),
        "is_daytime": 1 if 6 <= time.hour <= 18 else 0
    }