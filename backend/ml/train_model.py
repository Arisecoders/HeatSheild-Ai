from pathlib import Path

import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "heatshield_training_data.csv"
MODEL_PATH = BASE_DIR / "heatshield_model.pkl"

df = pd.read_csv(DATA_PATH)

features = [
    "temperature_2m",
    "relative_humidity_2m",
    "rain",
    "wind_speed_10m",
    "shortwave_radiation",
    "hour",
    "month",
    "day_of_year",
    "is_daytime"
]

X = df[features]
y = df["heat_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("HeatShield AI Model Training Complete!")
print()
print(f"Accuracy: {accuracy:.2%}")
print()
print("Classification Report:")
print(classification_report(y_test, predictions))

joblib.dump(model, MODEL_PATH)

print(f"Model saved as: {MODEL_PATH.name}")