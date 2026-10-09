import { useState } from "react";
import "./App.css";

function App() {
  const [temperature, setTemperature] = useState(38);
  const [humidity, setHumidity] = useState(65);
  const [rain, setRain] = useState(0);
  const [windSpeed, setWindSpeed] = useState(4);
  const [solarRadiation, setSolarRadiation] = useState(800);

  const [climateTime, setClimateTime] = useState("Updated just now");
  const [prediction, setPrediction] = useState(null);
  const [loadingClimate, setLoadingClimate] = useState(false);
  const [loadingPrediction, setLoadingPrediction] = useState(false);
  const [error, setError] = useState("");

  const riskTrend = [
    { label: "06h", value: 28 },
    { label: "09h", value: 42 },
    { label: "12h", value: 58 },
    { label: "15h", value: 70 },
    { label: "18h", value: 64 },
    { label: "21h", value: 46 },
  ];

  const cityBlocks = [
    "hot",
    "warm",
    "cool",
    "warm",
    "hot",
    "hot",
    "cool",
    "warm",
    "hot",
  ];

  const loadClimate = async () => {
    setLoadingClimate(true);
    setError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/current-climate"
      );

      if (!response.ok) {
        throw new Error("Unable to load climate data");
      }

      const data = await response.json();

      setTemperature(data.temperature);
      setHumidity(data.humidity);
      setRain(data.rain);
      setWindSpeed(data.wind_speed);
      setSolarRadiation(data.solar_radiation);
      setClimateTime(data.time);
    } catch (err) {
      console.error("Unable to load climate data", err);
      setError(
        "Unable to connect to HeatShield AI backend. Make sure FastAPI is running."
      );
    } finally {
      setLoadingClimate(false);
    }
  };

  const predictHeatRisk = async () => {
    setLoadingPrediction(true);
    setError("");

    try {
      const climateResponse = await fetch(
        "http://127.0.0.1:8000/current-climate"
      );

      if (!climateResponse.ok) {
        throw new Error("Unable to load climate data");
      }

      const climate = await climateResponse.json();

      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            temperature: climate.temperature,
            humidity: climate.humidity,
            rain: climate.rain,
            wind_speed: climate.wind_speed,
            solar_radiation: climate.solar_radiation,
            hour: climate.hour,
            month: climate.month,
            day_of_year: climate.day_of_year,
            is_daytime: climate.is_daytime,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Prediction failed");
      }

      const result = await response.json();

      setTemperature(climate.temperature);
      setHumidity(climate.humidity);
      setRain(climate.rain);
      setWindSpeed(climate.wind_speed);
      setSolarRadiation(climate.solar_radiation);
      setClimateTime(climate.time);
      setPrediction(result);
    } catch (err) {
      console.error("Prediction request failed", err);
      setError(
        "Unable to connect to HeatShield AI backend. Make sure FastAPI is running."
      );
    } finally {
      setLoadingPrediction(false);
    }
  };

  const getRiskClass = (risk) => {
    if (risk === "Critical") return "critical";
    if (risk === "High") return "high";
    if (risk === "Moderate") return "moderate";
    return "low";
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>🔥 HeatShield AI</h1>
          <p>
            AI-Powered Urban Heat Risk & Climate Action Platform
          </p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          AI Model Online
        </div>
      </header>

      <main className="dashboard">
        <section className="hero">
          <div className="hero-copy">
            <h2>Hyderabad Heat Risk Analysis</h2>
            <p>
              Analyze real Hyderabad climate data using our trained
              Random Forest AI model.
            </p>
          </div>

          <div className="hero-visual" aria-hidden="true">
            <div className="sun-orb"></div>
            <div className="sun-rays">
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div className="shield-glow"></div>
            <div className="shield">
              <div className="shield-inner"></div>
            </div>
          </div>

          {prediction ? (
            <div
              className={`risk-badge ${getRiskClass(
                prediction.risk
              )}`}
            >
              {prediction.risk}
            </div>
          ) : (
            <div className="risk-badge low">Stable</div>
          )}
        </section>

        <section className="insights-panel">
          <div className="insight-card main-insight">
            <span className="eyebrow">Live status</span>
            <h3>{prediction ? prediction.risk : "Monitoring"}</h3>
            <p>
              AI is tracking the city’s temperature, humidity,
              and exposure conditions to estimate urban heat stress.
            </p>
          </div>

          <div className="mini-metrics">
            <div className="mini-metric">
              <span>Heat Index</span>
              <strong>
                {temperature
                  ? `${Math.round(Number(temperature) + Number(humidity) / 5)}°C`
                  : "--"}
              </strong>
            </div>
            <div className="mini-metric">
              <span>Wind</span>
              <strong>{windSpeed ? `${windSpeed} km/h` : "--"}</strong>
            </div>
            <div className="mini-metric">
              <span>Solar</span>
              <strong>
                {solarRadiation ? `${solarRadiation} W/m²` : "--"}
              </strong>
            </div>
          </div>
        </section>

        <section className="overview-grid">
          <div className="panel city-map-panel">
            <div className="panel-header">
              <span>Urban heat map</span>
              <span className="chip">Hyderabad</span>
            </div>

            <div className="city-grid">
              {cityBlocks.map((type, index) => (
                <span
                  key={`${type}-${index}`}
                  className={`city-cell ${type}`}
                />
              ))}
            </div>
          </div>

          <div className="panel trend-panel">
            <div className="panel-header">
              <span>Risk trend</span>
              <span className="chip subtle">Today</span>
            </div>

            <div className="bar-chart" aria-label="Heat risk trend chart">
              {riskTrend.map((item) => (
                <div key={item.label} className="bar-column">
                  <span
                    className="bar"
                    style={{ height: `${item.value}%` }}
                  ></span>
                  <small>{item.label}</small>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="control-card">
          <h2>🌡️ Climate Conditions</h2>

          {climateTime && (
            <p>
              Data time: <strong>{climateTime}</strong>
            </p>
          )}

          <div className="input-grid">
            <label>
              Temperature (°C)
              <input
                type="number"
                value={temperature}
                readOnly
              />
            </label>

            <label>
              Humidity (%)
              <input
                type="number"
                value={humidity}
                readOnly
              />
            </label>

            <label>
              Rain (mm)
              <input
                type="number"
                value={rain}
                readOnly
              />
            </label>

            <label>
              Wind Speed (km/h)
              <input
                type="number"
                value={windSpeed}
                readOnly
              />
            </label>

            <label>
              Solar Radiation
              <input
                type="number"
                value={solarRadiation}
                readOnly
              />
            </label>
          </div>

          <div className="button-row">
            <button onClick={loadClimate} disabled={loadingClimate}>
              {loadingClimate
                ? "Loading..."
                : "🌤️ Load Hyderabad Climate"}
            </button>

            <button
              onClick={predictHeatRisk}
              disabled={loadingPrediction}
            >
              {loadingPrediction
                ? "Analyzing..."
                : "🤖 Analyze Heat Risk"}
            </button>
          </div>

          {error && <p className="error">{error}</p>}
        </section>

        {prediction && (
          <section className="results">
            <div
              className={`result-card ${getRiskClass(
                prediction.risk
              )}`}
            >
              <span>Heat Risk</span>
              <strong>{prediction.risk}</strong>
            </div>

            <div className="result-card">
              <span>Risk Score</span>
              <strong>{prediction.risk_score}/100</strong>
            </div>

            <div className="result-card">
              <span>AI Confidence</span>
              <strong>{prediction.confidence}%</strong>
            </div>
          </section>
        )}

        {prediction && (
          <section className="analysis-card">
            <h2>🤖 AI Analysis</h2>

            <p>
              The HeatShield AI model classified the current
              Hyderabad climate conditions as{" "}
              <strong>{prediction.risk}</strong> heat risk with{" "}
              <strong>{prediction.confidence}%</strong> model
              confidence.
            </p>

            <h3>Recommended Actions</h3>

            <ul>
              <li>
                Increase tree and vegetation coverage.
              </li>
              <li>
                Promote cool roofs and reflective surfaces.
              </li>
              <li>
                Provide shaded areas in high-footfall locations.
              </li>
              <li>
                Monitor vulnerable populations during extreme
                heat.
              </li>
            </ul>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;