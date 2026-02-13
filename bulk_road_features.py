import osmnx as ox
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.strtree import STRtree
import time

# =============================
# CONFIG
# =============================
INPUT_CSV = "data/processed/vijayawada_street_geocoded_hybrid.csv"
OUTPUT_CSV = "data/processed/vijayawada_street_geocoded_hybrid_with_road_features.csv"

LAT_COL = "latitude"
LON_COL = "longitude"

LOG_EVERY = 50  # progress interval

# =============================
# STEP 1: LOAD CSV
# =============================
print("[1/6] Loading CSV...")
df = pd.read_csv(INPUT_CSV)
total = len(df)
print(f"      Loaded {total} rows")

# =============================
# STEP 2: DOWNLOAD ROADS (FAST PLACE QUERY)
# =============================
print("[2/6] Downloading OSM roads (place-based)...")
start = time.time()

G = ox.graph_from_place(
    "Vijayawada, Andhra Pradesh, India",
    network_type="drive"
)

print(f"      Roads downloaded in {round(time.time() - start, 2)} sec")

# =============================
# STEP 3: PROJECT GRAPH TO METERS
# =============================
print("[3/6] Projecting graph to meter-based CRS...")
G_proj = ox.project_graph(G)
edges = ox.graph_to_gdfs(G_proj, nodes=False, edges=True)

# =============================
# STEP 4: CLASSIFY ROADS
# =============================
print("[4/6] Classifying road types...")

HIGHWAY = {"motorway", "trunk"}
MAIN = {"primary", "secondary", "tertiary"}
INNER = {"residential", "service", "living_street", "unclassified"}

highway_geoms = []
main_geoms = []
inner_geoms = []

for _, r in edges.iterrows():
    t = r.get("highway")
    if isinstance(t, list):
        t = t[0]

    if t in HIGHWAY:
        highway_geoms.append(r.geometry)
    elif t in MAIN:
        main_geoms.append(r.geometry)
    elif t in INNER:
        inner_geoms.append(r.geometry)

print(f"      highways={len(highway_geoms)}, main={len(main_geoms)}, inner={len(inner_geoms)}")

# =============================
# STEP 5: BUILD SPATIAL INDEX
# =============================
print("[5/6] Building spatial index...")
highway_tree = STRtree(highway_geoms)
main_tree = STRtree(main_geoms)
inner_tree = STRtree(inner_geoms)

# =============================
# PROJECT POINTS TO SAME CRS
# =============================
points = gpd.GeoSeries(
    [Point(xy) for xy in zip(df[LON_COL], df[LAT_COL])],
    crs="EPSG:4326"
).to_crs(edges.crs)

# =============================
# FIXED HELPER (Shapely 2.x safe)
# =============================
def nearest(tree, geoms, pt):
    if not geoms:
        return None
    idx = tree.nearest(pt)  # returns index in Shapely 2.x
    nearest_geom = geoms[idx]
    return pt.distance(nearest_geom)

WEIGHTS = {
    "highway": 5,
    "main": 3,
    "inner": 1
}

# =============================
# STEP 6: FEATURE EXTRACTION
# =============================
print("[6/6] Computing road features...")
results = []

for i, pt in enumerate(points, start=1):

    d_h = nearest(highway_tree, highway_geoms, pt)
    d_m = nearest(main_tree, main_geoms, pt)
    d_i = nearest(inner_tree, inner_geoms, pt)

    road_score = 0
    if d_h is not None:
        road_score += WEIGHTS["highway"] / (d_h + 1)
    if d_m is not None:
        road_score += WEIGHTS["main"] / (d_m + 1)
    if d_i is not None:
        road_score += WEIGHTS["inner"] / (d_i + 1)

    results.append({
        "dist_highway_m": round(d_h, 2) if d_h is not None else None,
        "dist_main_road_m": round(d_m, 2) if d_m is not None else None,
        "dist_inner_road_m": round(d_i, 2) if d_i is not None else None,
        "road_score": round(road_score, 4),
        "main_road_under_50m": int(d_m is not None and d_m <= 50),
        "highway_under_500m": int(d_h is not None and d_h <= 500)
    })

    # Progress logging
    if i % LOG_EVERY == 0 or i == total:
        print(f"      processed {i}/{total}")

# =============================
# SAVE OUTPUT (HYBRID + ROAD)
# =============================
features_df = pd.DataFrame(results)
final_df = pd.concat([df.reset_index(drop=True), features_df], axis=1)

final_df.to_csv(OUTPUT_CSV, index=False)

print("✅ DONE. Output saved to:", OUTPUT_CSV)
