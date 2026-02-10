import pandas as pd
import geopandas as gpd

from ml_service.distance_engine.distance import compute_nearest_road_features

# =========================
# FILE PATHS
# =========================
LAND_INPUT = "data/processed/canonical_with_location.csv"
ROADS_INPUT = "data/processed/vijayawada_roads.geojson"
OUTPUT_FILE = "data/processed/canonical_with_road_features.csv"

# =========================
# LOAD DATA
# =========================
print("Loading land data...")
land_df = pd.read_csv(LAND_INPUT)

print("Loading cached road network...")
roads = gpd.read_file(ROADS_INPUT)

# =========================
# COMPUTE ROAD FEATURES
# =========================
distance_to_road = []
nearest_road_type = []

for _, row in land_df.iterrows():
    d, rtype = compute_nearest_road_features(
        lat=row["latitude"],
        lng=row["longitude"],
        roads_gdf=roads
    )
    distance_to_road.append(d)
    nearest_road_type.append(rtype)

# =========================
# ATTACH FEATURES
# =========================
land_df["distance_to_road_m"] = distance_to_road
land_df["nearest_road_type"] = nearest_road_type

# =========================
# SAVE OUTPUT
# =========================
land_df.to_csv(OUTPUT_FILE, index=False)

print("TB-4 SUCCESS ✅")
print(
    land_df[
        ["parcel_id", "distance_to_road_m", "nearest_road_type"]
    ].head()
)
