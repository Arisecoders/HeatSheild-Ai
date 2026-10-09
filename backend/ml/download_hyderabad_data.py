import requests
import pandas as pd

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 17.398945,
    "longitude": 78.457085,
    "start_date": "2025-01-01",
    "end_date": "2026-10-04",
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "rain",
        "wind_speed_10m",
        "shortwave_radiation"
    ],
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params, timeout=60)
response.raise_for_status()

data = response.json()

df = pd.DataFrame(data["hourly"])

df["time"] = pd.to_datetime(df["time"])

output = "hyderabad_climate_data.csv"
df.to_csv(output, index=False)

print("Dataset downloaded successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"Saved as: {output}")
print()
print(df.head())
