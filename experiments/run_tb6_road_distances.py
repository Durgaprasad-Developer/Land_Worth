import pandas as pd
import numpy as np
from scipy.spatial import KDTree
from geopy.distance import geodesic
import os

LAND_FILE = "data/processed/vijayawada_street_geocoded_hybrid.csv"
ROADS_FILE = "data/processed/vijayawada_all_roads.csv"
OUTPUT_FILE = "data/processed/vijayawada_street_with_road_distances.csv"

print("[1/6] Loading datasets...")
land_df = pd.read_csv(LAND_FILE)
roads_df = pd.read_csv(ROADS_FILE)

print("[2/6] Splitting road categories...")

highway_df = roads_df[roads_df["road_category"] == "Highway"]
main_df = roads_df[roads_df["road_category"] == "Main Road"]
inner_df = roads_df[roads_df["road_category"] == "Inner Road"]

print("Highway count:", len(highway_df))
print("Main Road count:", len(main_df))
print("Inner Road count:", len(inner_df))

print("[3/6] Building KD Trees...")

highway_tree = KDTree(highway_df[["latitude", "longitude"]].values)
main_tree = KDTree(main_df[["latitude", "longitude"]].values)
inner_tree = KDTree(inner_df[["latitude", "longitude"]].values)

def get_distance(tree, df_category, lat, lon):
    distance, index = tree.query([lat, lon])
    nearest_point = df_category.iloc[index]
    nearest_coords = (nearest_point["latitude"], nearest_point["longitude"])
    return geodesic((lat, lon), nearest_coords).meters

print("[4/6] Computing distances...")

dist_highway = []
dist_main = []
dist_inner = []

for i, row in land_df.iterrows():
    lat = row["latitude"]
    lon = row["longitude"]

    d1 = get_distance(highway_tree, highway_df, lat, lon)
    d2 = get_distance(main_tree, main_df, lat, lon)
    d3 = get_distance(inner_tree, inner_df, lat, lon)

    dist_highway.append(round(d1, 2))
    dist_main.append(round(d2, 2))
    dist_inner.append(round(d3, 2))

    if i % 100 == 0:
        print(f"Processed {i}/{len(land_df)}")

print("[5/6] Adding columns...")

land_df["dist_highway_m"] = dist_highway
land_df["dist_main_road_m"] = dist_main
land_df["dist_inner_road_m"] = dist_inner

print("[6/6] Saving final dataset...")

land_df.to_csv(OUTPUT_FILE, index=False)

print("DONE.")
print("Saved at:", OUTPUT_FILE)
