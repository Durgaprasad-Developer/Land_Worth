import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point

# =============================
# INPUT
# =============================
lat, lon = 16.512100, 80.615156
point = Point(lon, lat)

# =============================
# DOWNLOAD ROADS
# =============================
G = ox.graph_from_point(
    (lat, lon),
    dist=1000,
    network_type="drive"
)

# Project graph → meters (OLD OSMnx safe)
G_proj = ox.project_graph(G)

# Convert to edges
edges = ox.graph_to_gdfs(G_proj, nodes=False, edges=True)

# Project point to same CRS
point_proj = (
    gpd.GeoSeries([point], crs="EPSG:4326")
    .to_crs(edges.crs)
    .iloc[0]
)

# =============================
# ROAD GROUPS
# =============================
HIGHWAY = {"motorway", "trunk"}
MAIN_ROAD = {"primary", "secondary", "tertiary"}
INNER_ROAD = {"residential", "service", "living_street", "unclassified"}

# =============================
# DISTANCE STORAGE
# =============================
distances = {
    "highway": None,
    "main_road": None,
    "inner_road": None
}

def update_min(key, dist):
    if distances[key] is None or dist < distances[key]:
        distances[key] = dist

# =============================
# DISTANCE CALCULATION
# =============================
for _, row in edges.iterrows():
    road_type = row.get("highway")

    if isinstance(road_type, list):
        road_type = road_type[0]

    if road_type is None:
        continue

    dist = point_proj.distance(row.geometry)

    if road_type in HIGHWAY:
        update_min("highway", dist)
    elif road_type in MAIN_ROAD:
        update_min("main_road", dist)
    elif road_type in INNER_ROAD:
        update_min("inner_road", dist)

# Round distances
for k in distances:
    if distances[k] is not None:
        distances[k] = round(distances[k], 2)

# =============================
# ROAD WEIGHT SCORING
# =============================
WEIGHTS = {
    "highway": 5,
    "main_road": 3,
    "inner_road": 1
}

road_score = 0
for k, w in WEIGHTS.items():
    if distances[k] is not None:
        road_score += w / (distances[k] + 1)

road_score = round(road_score, 4)

# =============================
# FINAL ML FEATURES
# =============================
features = {
    "dist_highway_m": distances["highway"],
    "dist_main_road_m": distances["main_road"],
    "dist_inner_road_m": distances["inner_road"],

    "road_score": road_score,

    "main_road_under_50m": int(distances["main_road"] is not None and distances["main_road"] <= 50),
    "highway_under_500m": int(distances["highway"] is not None and distances["highway"] <= 500)
}

print(features)
