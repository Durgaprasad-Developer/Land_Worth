function isInsideVijayawada(lat, lon) {
  const minLat = 16.44;
  const maxLat = 16.60;
  const minLon = 80.55;
  const maxLon = 80.75;

  return (
    lat >= minLat &&
    lat <= maxLat &&
    lon >= minLon &&
    lon <= maxLon
  );
}

module.exports = { isInsideVijayawada };
