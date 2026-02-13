import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# =====================================
# CONFIG
# =====================================

PARCEL_FILE = "data/processed/vijayawada_street_geocoded_hybrid.csv"
ROADS_FILE = "data/processed/vijayawada_roads.geojson"
OUTPUT_FILE = "data/processed/vijayawada_with_road_features.csv"

# =====================================
# ROAD CLASSIFIER
# =====================================

def classify_road(highway_tag):
    if isinstance(highway_tag, list):
        highway_tag = highway_tag[0]

    if highway_tag in ["motorway", "trunk", "primary"]:
        return "highway"
    elif highway_tag in ["secondary", "tertiary"]:
        return "main_road"
    else:
        return "inner_road"

# =====================================
# LOAD ROADS
# =====================================

print("Loading road geojson...")
roads = gpd.read_file(ROADS_FILE)

roads = roads.dropna(subset=["geometry", "highway"]).copy()

roads["road_class"] = roads["highway"].apply(classify_road)

# CRS84 = same as EPSG:4326
roads = roads.set_crs(epsg=4326)

# Project once to meters
roads = roads.to_crs(epsg=3857)

# Split by road class
roads_highway = roads[roads["road_class"] == "highway"]
roads_main = roads[roads["road_class"] == "main_road"]
roads_inner = roads[roads["road_class"] == "inner_road"]

print("Road class counts:")
print("Highway:", len(roads_highway))
print("Main:", len(roads_main))
print("Inner:", len(roads_inner))

# =====================================
# LOAD PARCELS
# =====================================

print("Loading parcel dataset...")
df = pd.read_csv(PARCEL_FILE)
df = df.dropna(subset=["latitude", "longitude"]).reset_index(drop=True)

parcel_gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(xy) for xy in zip(df["longitude"], df["latitude"])],
    crs="EPSG:4326"
).to_crs(epsg=3857)

# =====================================
# COMPUTE DISTANCES (ACCURATE)
# =====================================

print("Computing road distances...")

dist_highway = []
dist_main = []
dist_inner = []

for i, row in parcel_gdf.iterrows():

    if i % 200 == 0:
        print(f"Processed {i}/{len(parcel_gdf)}")

    point = row.geometry

    # Exact geometric distance
    d_highway = roads_highway.geometry.distance(point).min() if len(roads_highway) > 0 else None
    d_main = roads_main.geometry.distance(point).min() if len(roads_main) > 0 else None
    d_inner = roads_inner.geometry.distance(point).min() if len(roads_inner) > 0 else None

    dist_highway.append(float(d_highway) if d_highway is not None else None)
    dist_main.append(float(d_main) if d_main is not None else None)
    dist_inner.append(float(d_inner) if d_inner is not None else None)

# =====================================
# SAVE
# =====================================

parcel_gdf["distance_to_highway"] = dist_highway
parcel_gdf["distance_to_main_road"] = dist_main
parcel_gdf["distance_to_inner_road"] = dist_inner

parcel_gdf = parcel_gdf.drop(columns=["geometry"])

parcel_gdf.to_csv(OUTPUT_FILE, index=False)

print("ROAD FEATURES BUILT SUCCESSFULLY ✅")
