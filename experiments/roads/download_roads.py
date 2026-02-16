import osmnx as ox
import pandas as pd
from roads.road_classifier import classify_road


def download_and_process_vijayawada_roads():

    print("[1/5] Downloading Vijayawada road network...")
    G = ox.graph_from_place(
        "Vijayawada, Andhra Pradesh, India",
        network_type="drive"
    )

    print("[2/5] Converting graph to GeoDataFrame...")
    nodes, edges = ox.graph_to_gdfs(G)

    print("[3/5] Cleaning edges...")
    edges = edges.reset_index()

    processed_rows = []

    print("[4/5] Classifying roads...")

    for index, row in edges.iterrows():

        highway = row.get("highway")
        name = row.get("name")
        length = row.get("length")
        geometry = row.get("geometry")

        category = classify_road(highway)

        if category is None:
            continue

        # Get centroid for lat/lon
        centroid = geometry.centroid

        processed_rows.append({
            "road_name": name,
            "road_type_raw": highway,
            "road_category": category,
            "road_length_meters": length,
            "latitude": centroid.y,
            "longitude": centroid.x
        })

        if index % 500 == 0:
            print(f"Processed {index}/{len(edges)}")

    print("[5/5] Creating DataFrame...")

    df = pd.DataFrame(processed_rows)

    return df
