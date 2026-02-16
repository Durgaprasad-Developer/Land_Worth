import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

LAND_FILE = "data/processed/vijayawada_street_with_road_distances.csv"
INFRA_FILE = "data/processed/vijayawada_all_infra.csv"
OUTPUT_FILE = "data/processed/vijayawada_street_with_all_features.csv"

EARTH_RADIUS = 6371000  # meters

print("[1/8] Loading datasets...")
land_df = pd.read_csv(LAND_FILE)
infra_df = pd.read_csv(INFRA_FILE)

print("Land rows:", len(land_df))
print("Infra rows:", len(infra_df))

if len(infra_df) == 0:
    raise ValueError("Infra dataset is empty. Cannot proceed.")

print("[2/8] Preparing coordinates (convert to radians)...")

land_coords = np.radians(
    land_df[["latitude", "longitude"]].values
)

infra_coords = np.radians(
    infra_df[["latitude", "longitude"]].values
)

print("[3/8] Building BallTree (Haversine)...")

tree = BallTree(infra_coords, metric="haversine")

# ---------------------------------------------------
# 1️⃣ Nearest Infra Distance
# ---------------------------------------------------

print("[4/8] Computing nearest infra distance...")

distances, indices = tree.query(land_coords, k=1)

dist_meters = distances.flatten() * EARTH_RADIUS
land_df["dist_nearest_infra_m"] = np.round(dist_meters, 2)

# ---------------------------------------------------
# 2️⃣ Density within 1000m
# ---------------------------------------------------

print("[5/8] Computing infra density within 1000m...")

radius_1000_rad = 1000 / EARTH_RADIUS

counts_1000 = tree.query_radius(
    land_coords,
    r=radius_1000_rad,
    count_only=True
)

land_df["infra_count_1000m"] = counts_1000

# ---------------------------------------------------
# 3️⃣ Density within 3000m
# ---------------------------------------------------

print("[6/8] Computing infra density within 3000m...")

radius_3000_rad = 3000 / EARTH_RADIUS

counts_3000 = tree.query_radius(
    land_coords,
    r=radius_3000_rad,
    count_only=True
)

land_df["infra_count_3000m"] = counts_3000

# ---------------------------------------------------
# Sanity Check
# ---------------------------------------------------

print("[7/8] Sanity check statistics...")

print("\nNearest infra distance stats:")
print(land_df["dist_nearest_infra_m"].describe())

print("\nInfra count within 1000m stats:")
print(land_df["infra_count_1000m"].describe())

print("\nInfra count within 3000m stats:")
print(land_df["infra_count_3000m"].describe())

# ---------------------------------------------------
# Save
# ---------------------------------------------------

print("[8/8] Saving final dataset...")

land_df.to_csv(OUTPUT_FILE, index=False)

print("DONE.")
print("Saved at:", OUTPUT_FILE)

# ---------------------------------------------------
# Optional single-point test
# ---------------------------------------------------

print("\n--- Manual Test Point ---")

test_point = np.radians([[16.520856, 80.691696]])

dist_test, _ = tree.query(test_point, k=1)
print("Test nearest meters:", round(dist_test[0][0] * EARTH_RADIUS, 2))

count_test_1000 = tree.query_radius(test_point, r=radius_1000_rad, count_only=True)
print("Test density 1000m:", count_test_1000[0])

count_test_3000 = tree.query_radius(test_point, r=radius_3000_rad, count_only=True)
print("Test density 3000m:", count_test_3000[0])
