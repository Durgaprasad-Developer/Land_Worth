import { useState } from "react";
import { predictPrice } from "../../services/api";

export default function PredictionPanel({ location }) {
  const [classification, setClassification] = useState("Residential");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    if (!location) return alert("Select location on map");

    setLoading(true);
    setResult(null);

    try {
      const response = await predictPrice({
        latitude: location.lat,
        longitude: location.lng,
        classification
      });

      setResult(response);
    } catch (err) {
      alert("Prediction failed");
    }

    setLoading(false);
  };

  return (
    <div>
      <h2>Land Valuation</h2>

      {location ? (
        <div>
          <p><strong>Latitude:</strong> {location.lat.toFixed(6)}</p>
          <p><strong>Longitude:</strong> {location.lng.toFixed(6)}</p>
        </div>
      ) : (
        <p>Click on map to select location</p>
      )}

      <label>Classification:</label>
      <select
        value={classification}
        onChange={(e) => setClassification(e.target.value)}
      >
        <option value="Residential">Residential</option>
        <option value="Commercial">Commercial</option>
      </select>

      <br /><br />

      <button onClick={handlePredict} disabled={loading}>
        {loading ? "Predicting..." : "Predict Price"}
      </button>

      {loading && <p>⏳ Calculating valuation...</p>}

      {result && (
        <div className="result-card">
          <h3>Estimated Price</h3>
          <h1>₹ {result.predicted_price_per_sq_yard}</h1>
        </div>
      )}
    </div>
  );
}
