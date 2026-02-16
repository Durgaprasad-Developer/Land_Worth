import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

# ---------------------------------------------------
# FILE
# ---------------------------------------------------

FILE = "data/processed/land_price_reference.csv"
EARTH_RADIUS = 6371000

# 🔴 NEW ANCHOR POINT (AS RAJU ROAD)
anchor_lat = 16.519099963348015
anchor_lon = 80.65786169622751

print("[1/5] Loading dataset...")
df = pd.read_csv(FILE)

print("Total rows:", len(df))

# ---------------------------------------------------
# Convert to radians
# ---------------------------------------------------

coords = np.radians(df[["latitude", "longitude"]].values)
anchor_point = np.radians([[anchor_lat, anchor_lon]])

# ---------------------------------------------------
# Build BallTree
# ---------------------------------------------------

print("[2/5] Building BallTree...")
tree = BallTree(coords, metric="haversine")

# ---------------------------------------------------
# Compute distance to ALL points
# ---------------------------------------------------

print("[3/5] Computing distances to all points...")
distances, _ = tree.query(anchor_point, k=len(df))

distances_m = distances.flatten() * EARTH_RADIUS

# Remove itself (0 distance)
distances_m = distances_m[1:]

# ---------------------------------------------------
# Stats
# ---------------------------------------------------

print("\n[4/5] Distance statistics (meters):")
print(pd.Series(distances_m).describe())

print("\nFirst 20 nearest distances:")
print(np.round(distances_m[:20], 2))

print("\nAverage distance to ALL lands:")
print(round(np.mean(distances_m), 2), "meters")

print("\nAverage distance of first 15 neighbors:")
print(round(np.mean(distances_m[:15]), 2), "meters")

print("\nAverage distance of first 30 neighbors:")
print(round(np.mean(distances_m[:30]), 2), "meters")

print("\nAverage distance of first 50 neighbors:")
print(round(np.mean(distances_m[:50]), 2), "meters")

print("[5/5] Done.")
