import { useState, useEffect } from "react";
import { predictPrice } from "../../services/api";

export default function PredictionPanel({ location, onManualLocation }) {
  const [classification, setClassification] = useState("Residential");
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Sync when map is clicked
  useEffect(() => {
    if (location) {
      setLatitude(location.lat.toFixed(6));
      setLongitude(location.lng.toFixed(6));
    }
  }, [location]);

  const handlePredict = async () => {
    if (!latitude || !longitude) {
      setError("Please provide valid latitude and longitude.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await predictPrice({
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
        classification
      });

      setResult(response);
    } catch (err) {
      setError(
        err.response?.data?.message ||
        "Prediction failed. Location may be outside Vijayawada."
      );
    }

    setLoading(false);
  };

  return (
    <div>
      <h2>Land Valuation</h2>

      <label>Latitude</label>
      <input
        type="number"
        value={latitude}
        onChange={(e) => setLatitude(e.target.value)}
        placeholder="Enter latitude"
      />

      <label>Longitude</label>
      <input
        type="number"
        value={longitude}
        onChange={(e) => setLongitude(e.target.value)}
        placeholder="Enter longitude"
      />

      <label>Classification</label>
      <select
        value={classification}
        onChange={(e) => setClassification(e.target.value)}
      >
        <option value="Residential">Residential</option>
        <option value="Commercial">Commercial</option>
      </select>

      <button onClick={handlePredict} disabled={loading}>
        {loading ? "Predicting..." : "Predict Price"}
      </button>

      {loading && <p className="loading">⏳ Calculating valuation...</p>}

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}

      {result && (
        <div className="result-card">
          <h3>Estimated Price (per sq yard)</h3>
          <h1>₹ {result.predicted_price_per_sq_yard}/sq. yd</h1>
        </div>
      )}
    </div>
  );
}
