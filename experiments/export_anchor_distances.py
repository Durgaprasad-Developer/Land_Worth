import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

# ---------------------------------------------------
# FILES
# ---------------------------------------------------

INPUT_FILE = "data/processed/land_price_reference.csv"
OUTPUT_FILE = "data/processed/anchor_distance_analysis.csv"

EARTH_RADIUS = 6371000

# 🔴 Anchor: AS RAJU ROAD
anchor_lat = 16.519099963348015
anchor_lon = 80.65786169622751

print("[1/5] Loading dataset...")
df = pd.read_csv(INPUT_FILE)

print("Total rows:", len(df))

# ---------------------------------------------------
# Prepare coords
# ---------------------------------------------------

coords = np.radians(df[["latitude", "longitude"]].values)
anchor_point = np.radians([[anchor_lat, anchor_lon]])

print("[2/5] Building BallTree...")
tree = BallTree(coords, metric="haversine")

print("[3/5] Computing distances...")

distances, indices = tree.query(anchor_point, k=len(df))

distances_m = distances.flatten() * EARTH_RADIUS
indices = indices.flatten()

# Remove self (distance ≈ 0)
distances_m = distances_m[1:]
indices = indices[1:]

# ---------------------------------------------------
# Build output dataframe
# ---------------------------------------------------

output_df = df.iloc[indices].copy()
output_df["distance_from_anchor_m"] = distances_m

# Sort by distance
output_df = output_df.sort_values("distance_from_anchor_m")

print("[4/5] Saving distance file...")
output_df.to_csv(OUTPUT_FILE, index=False)

print("[5/5] DONE.")
print("Saved at:", OUTPUT_FILE)
