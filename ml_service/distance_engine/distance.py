# Land_Worth/ml_service/distance_engine/distance.py

import geopandas as gpd
from shapely.geometry import Point
from ml_service.gis.road_classifier import classify_road


def prepare_roads_for_distance(roads_gdf):
    """
    Prepare roads once:
    - Drop null geometry/highway
    - Project to meter CRS (EPSG:3857)
    - Add simplified road_class
    - Build spatial index
    """

    roads = roads_gdf.dropna(subset=["geometry", "highway"]).copy()

    if roads.crs is None:
        roads = roads.set_crs(epsg=4326)

    # Project once
    roads = roads.to_crs(epsg=3857)

    # Normalize highway tag
    def normalize_highway(tag):
        if isinstance(tag, list):
            tag = tag[0]
        return classify_road(tag)

    roads["road_class"] = roads["highway"].apply(normalize_highway)

    # Build spatial index
    roads_sindex = roads.sindex

    return roads, roads_sindex


def compute_road_class_distances(lat, lng, roads_projected, roads_sindex):
    """
    Compute accurate distance to:
    - highway
    - main_road
    - inner_road

    Uses spatial index with radius-based filtering (Shapely 2.x safe)
    """

    # Create projected point
    point = gpd.GeoDataFrame(
        geometry=[Point(lng, lat)],
        crs="EPSG:4326"
    ).to_crs(epsg=3857)

    point_geom = point.geometry.iloc[0]

    results = {
        "distance_to_highway": None,
        "distance_to_main_road": None,
        "distance_to_inner_road": None
    }

    # Step 1️⃣ initial search radius (500 meters)
    search_radius = 500
    buffer = point_geom.buffer(search_radius)

    possible_index = list(roads_sindex.intersection(buffer.bounds))
    candidate_roads = roads_projected.iloc[possible_index]

    # Step 2️⃣ expand search if nothing found
    if len(candidate_roads) == 0:
        buffer = point_geom.buffer(2000)
        possible_index = list(roads_sindex.intersection(buffer.bounds))
        candidate_roads = roads_projected.iloc[possible_index]

    # Step 3️⃣ compute distance per road class
    for road_class in ["highway", "main_road", "inner_road"]:

        subset = candidate_roads[
            candidate_roads["road_class"] == road_class
        ]

        if len(subset) > 0:
            distances = subset.geometry.distance(point_geom)
            results[f"distance_to_{road_class}"] = float(distances.min())

    return results
