import geopandas as gpd
from ml_service.poi.poi_loader import load_pois

print("Loading POIs from OSM...")
pois = load_pois()

pois.to_file(
    "data/processed/vijayawada_pois.geojson",
    driver="GeoJSON"
)

print("POI CACHE SUCCESS ✅")
print("Total POIs:", len(pois))
