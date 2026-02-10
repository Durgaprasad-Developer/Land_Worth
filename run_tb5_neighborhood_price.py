import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

INPUT_FILE = "data/processed/canonical_with_poi_features.csv"
OUTPUT_FILE = "data/processed/canonical_with_ml_features.csv"

RADIUS_METERS = 1000  # 1 km

print("Loading dataset...")
df = pd.read_csv(INPUT_FILE)

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(xy) for xy in zip(df["longitude"], df["latitude"])],
    crs="EPSG:4326"
)

# Project to meters
gdf = gdf.to_crs(epsg=3857)

print("Computing radius-based neighborhood average price...")

neighborhood_prices = []

for i, row in gdf.iterrows():
    if i % 200 == 0:
        print(f"Processed {i} parcels...")

    buffer = row.geometry.buffer(RADIUS_METERS)

    neighbors = gdf[gdf.geometry.within(buffer)]

    if len(neighbors) > 0:
        neighborhood_prices.append(neighbors["base_value"].mean())
    else:
        neighborhood_prices.append(row["base_value"])  # fallback

gdf["neighborhood_avg_price"] = neighborhood_prices

# Drop geometry before saving
gdf = gdf.drop(columns=["geometry"])

gdf.to_csv(OUTPUT_FILE, index=False)

print("TB-5.2 (RADIUS) SUCCESS ✅")
print(
    gdf[
        ["parcel_id", "base_value", "neighborhood_avg_price"]
    ].head()
)
