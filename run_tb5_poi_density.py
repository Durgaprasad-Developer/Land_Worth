import pandas as pd
import geopandas as gpd
from ml_service.poi.density import computee_poi_density

LAND_FILE = "data/processed/canonical_with_road_features.csv"
POI_FILE = "data/processed/vijayawada_pois.geojson"
OUTPUT_FILE = "data/processed/canonical_with_poi_features.csv"

print("Loading land data")
df = pd.read_csv(LAND_FILE)

print("Loading cached data...")
pois = gpd.read_file(POI_FILE)

poi_density = []

for i, row in df.iterrows():
    if i % 100 == 0:
        print(f"Processed {i} parcels...")

    count = computee_poi_density(
        lat=row["latitude"],
        lng=row["longitude"],
        pois_gdf=pois,
        radius_m=1000
    )
    poi_density.append(count)

df["po_density_1km"] = poi_density

df.to_csv(OUTPUT_FILE, index=False)

print("TB-5.1 SUCCESS")
print(df[["parcel_id", "poi_density_1km"]].head())