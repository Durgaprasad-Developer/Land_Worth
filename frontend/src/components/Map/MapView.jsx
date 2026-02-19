import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import { useState } from "react";
import "leaflet/dist/leaflet.css";

function ClickHandler({ onSelect, setMarker }) {
  useMapEvents({
    click(e) {
      onSelect(e.latlng);
      setMarker(e.latlng);
    }
  });
  return null;
}

export default function MapView({ onLocationSelect }) {
  const [markerPosition, setMarkerPosition] = useState(null);

  const vijayawadaBounds = [
    [16.44, 80.55],
    [16.60, 80.75]
  ];

  return (
    <MapContainer
      center={[16.5062, 80.6480]}
      zoom={13}
      style={{ height: "100%" }}
      maxBounds={vijayawadaBounds}
    >
      <TileLayer
        attribution='© OpenStreetMap'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <ClickHandler
        onSelect={onLocationSelect}
        setMarker={setMarkerPosition}
      />

      {markerPosition && <Marker position={markerPosition} />}
    </MapContainer>
  );
}
