import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import osmnx as ox

# ======================================
# CONFIG
# ======================================

INPUT_FILE = "data/processed/vijayawada_street_geocoded_hybrid.csv"
OUTPUT_FILE = "data/processed/vijayawada_with_road_features.csv"
PLACE_NAME = "Vijayawada, Andhra Pradesh, India"

# ======================================
# ROAD CLASSIFIER
# ======================================

def classify_road(highway_tag):
    if isinstance(highway_tag, list):
        highway_tag = highway_tag[0]

    if highway_tag in ["motorway", "trunk", "primary"]:
        return "highway"
    elif highway_tag in ["secondary", "tertiary"]:
        return "main_road"
    else:
        return "inner_road"

# ======================================
# LOAD DATA
# ======================================

print("Loading hybrid dataset...")
df = pd.read_csv(INPUT_FILE)
df = df.dropna(subset=["latitude", "longitude"]).reset_index(drop=True)

# ======================================
# LOAD ROAD NETWORK
# ======================================

print("Downloading road network...")
G = ox.graph_from_place(PLACE_NAME, network_type="drive")
roads = ox.graph_to_gdfs(G, nodes=False)

roads = roads.dropna(subset=["geometry", "highway"]).copy()

if roads.crs is None:
    roads = roads.set_crs(epsg=4326)

# Project once to meters
roads = roads.to_crs(epsg=3857)

roads["road_class"] = roads["highway"].apply(classify_road)

# Build spatial index once
roads_sindex = roads.sindex

# ======================================
# PREPARE PARCEL GEO
# ======================================

parcel_gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(xy) for xy in zip(df["longitude"], df["latitude"])],
    crs="EPSG:4326"
).to_crs(epsg=3857)

# ======================================
# COMPUTE DISTANCES
# ======================================

print("Computing road class distances...")

distance_highway = []
distance_main = []
distance_inner = []

for i, row in parcel_gdf.iterrows():

    if i % 200 == 0:
        print(f"Processed {i}/{len(parcel_gdf)}")

    point_geom = row.geometry

    # 🔥 Use buffer search instead of nearest()
    search_radius = 500  # meters
    buffer = point_geom.buffer(search_radius)

    candidate_idx = list(roads_sindex.intersection(buffer.bounds))
    candidate_roads = roads.iloc[candidate_idx]

    # Expand search if nothing found
    if len(candidate_roads) == 0:
        buffer = point_geom.buffer(2000)
        candidate_idx = list(roads_sindex.intersection(buffer.bounds))
        candidate_roads = roads.iloc[candidate_idx]

    results = {
        "highway": None,
        "main_road": None,
        "inner_road": None
    }

    for road_class in ["highway", "main_road", "inner_road"]:
        subset = candidate_roads[candidate_roads["road_class"] == road_class]

        if len(subset) > 0:
            distances = subset.geometry.distance(point_geom)
            results[road_class] = float(distances.min())

    distance_highway.append(results["highway"])
    distance_main.append(results["main_road"])
    distance_inner.append(results["inner_road"])

# ======================================
# SAVE RESULTS
# ======================================

parcel_gdf["distance_to_highway"] = distance_highway
parcel_gdf["distance_to_main_road"] = distance_main
parcel_gdf["distance_to_inner_road"] = distance_inner

parcel_gdf = parcel_gdf.drop(columns=["geometry"])

parcel_gdf.to_csv(OUTPUT_FILE, index=False)

print("ROAD FEATURES ADDED SUCCESSFULLY ✅")
