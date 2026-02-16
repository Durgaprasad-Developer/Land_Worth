import osmnx as ox
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import time

# =============================
# CONFIG
# =============================
INPUT_CSV = "data/processed/vijayawada_street_geocoded_hybrid.csv"
OUTPUT_CSV = "data/processed/vijayawada_street_geocoded_hybrid_with_road_features_v2.csv"

LAT_COL = "latitude"
LON_COL = "longitude"

LOG_EVERY = 50

# =============================
# STEP 1: LOAD CSV
# =============================
print("[1/6] Loading CSV...")
df = pd.read_csv(INPUT_CSV)
total = len(df)
print(f"      Loaded {total} rows")

# =============================
# STEP 2: DOWNLOAD ROAD NETWORK
# =============================
print("[2/6] Downloading road network (place-based)...")
start = time.time()

G = ox.graph_from_place(
    "Vijayawada, Andhra Pradesh, India",
    network_type="drive"
)

print(f"      Downloaded in {round(time.time() - start, 2)} sec")

# =============================
# STEP 3: PROJECT GRAPH (METERS)
# =============================
print("[3/6] Projecting graph to meters...")
G_proj = ox.project_graph(G)

# =============================
# STEP 4: CLASSIFICATION SETS
# =============================
HIGHWAY = {"motorway", "trunk"}
MAIN = {"primary", "secondary", "tertiary"}
INNER = {"residential", "service", "living_street", "unclassified"}

WEIGHTS = {
    "highway": 5,
    "main": 3,
    "inner": 1
}

# =============================
# STEP 5: PROCESS POINTS
# =============================
print("[4/6] Computing road features (accurate edge-based)...")

results = []

for i, row in df.iterrows():
    lat = row[LAT_COL]
    lon = row[LON_COL]

    # Get nearest edge + distance (in meters)
    u, v, key, dist = ox.distance.nearest_edges(
        G_proj,
        X=lon,
        Y=lat,
        return_dist=True
    )

    edge_data = G_proj[u][v][key]
    road_type = edge_data.get("highway")

    # highway tag can be list
    if isinstance(road_type, list):
        road_type = road_type[0]

    # Initialize distances
    d_highway = None
    d_main = None
    d_inner = None

    # Assign distance to correct category
    if road_type in HIGHWAY:
        d_highway = dist
    elif road_type in MAIN:
        d_main = dist
    elif road_type in INNER:
        d_inner = dist

    # Road score
    road_score = 0
    if d_highway is not None:
        road_score += WEIGHTS["highway"] / (d_highway + 1)
    if d_main is not None:
        road_score += WEIGHTS["main"] / (d_main + 1)
    if d_inner is not None:
        road_score += WEIGHTS["inner"] / (d_inner + 1)

    results.append({
        "dist_highway_m": round(d_highway, 2) if d_highway else None,
        "dist_main_road_m": round(d_main, 2) if d_main else None,
        "dist_inner_road_m": round(d_inner, 2) if d_inner else None,
        "road_score": round(road_score, 4),
        "main_road_under_50m": int(d_main is not None and d_main <= 50),
        "highway_under_500m": int(d_highway is not None and d_highway <= 500)
    })

    if (i + 1) % LOG_EVERY == 0 or (i + 1) == total:
        print(f"      processed {i+1}/{total}")

# =============================
# STEP 6: SAVE NEW CSV
# =============================
features_df = pd.DataFrame(results)
final_df = pd.concat([df.reset_index(drop=True), features_df], axis=1)

final_df.to_csv(OUTPUT_CSV, index=False)

print("✅ DONE. Saved to:", OUTPUT_CSV)
