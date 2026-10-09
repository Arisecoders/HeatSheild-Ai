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

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]
    confidence = max(probabilities) * 100

    risk_scores = {
        "Low": 25,
        "Moderate": 50,
        "High": 75,
        "Critical": 95
    }

    return {
        "risk": str(prediction),
        "risk_score": risk_scores[str(prediction)],
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