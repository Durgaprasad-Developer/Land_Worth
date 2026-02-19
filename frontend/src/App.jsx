import { useState } from "react";
import MapView from "./components/Map/MapView";
import PredictionPanel from "./components/Prediction/PredictionPanel";
import "./index.css";

function App() {
  const [selectedLocation, setSelectedLocation] = useState(null);

  return (
    <div className="app-container">
      <div className="map-section">
        <MapView onLocationSelect={setSelectedLocation} />
      </div>

      <div className="panel-section">
        <PredictionPanel location={selectedLocation} />
      </div>
    </div>
  );
}

export default App;
