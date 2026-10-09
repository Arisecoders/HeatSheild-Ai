from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "hyderabad_climate_data.csv"
OUTPUT_PATH = BASE_DIR.parent / "heatshield_training_data.csv"

df = pd.read_csv(DATA_PATH)

df["time"] = pd.to_datetime(df["time"])

df["hour"] = df["time"].dt.hour
df["day"] = df["time"].dt.day
df["month"] = df["time"].dt.month
df["day_of_year"] = df["time"].dt.dayofyear

df["is_daytime"] = ((df["hour"] >= 6) & (df["hour"] <= 18)).astype(int)

df["heat_index_proxy"] = (
    0.45 * df["temperature_2m"]
    + 0.25 * (df["relative_humidity_2m"] / 100 * 40)
    + 0.20 * (df["shortwave_radiation"] / 1000 * 40)
    + 0.10 * df["wind_speed_10m"]
)

df["heat_risk"] = pd.cut(
    df["heat_index_proxy"],
    bins=[-float("inf"), 18, 22, 26, float("inf")],
    labels=["Low", "Moderate", "High", "Critical"]
)

df = df.dropna()

df.to_csv(OUTPUT_PATH, index=False)

print("HeatShield training dataset created!")
print(f"Rows: {len(df)}")
print()
print("Heat Risk Distribution:")
print(df["heat_risk"].value_counts())
print()
print(df.head())