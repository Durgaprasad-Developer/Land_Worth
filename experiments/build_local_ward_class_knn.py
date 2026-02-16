import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

# ---------------------------------------------------
# FILES
# ---------------------------------------------------

INPUT_FILE = "data/processed/vijayawada_street_with_all_features.csv"
OUTPUT_FILE = "data/processed/vijayawada_street_with_all_features_Model.csv"

EARTH_RADIUS = 6371000
K = 10

print("[1/6] Loading dataset...")
df = pd.read_csv(INPUT_FILE)

print("Total rows:", len(df))

# Precompute radians
df["lat_rad"] = np.radians(df["latitude"])
df["lon_rad"] = np.radians(df["longitude"])

# Global BallTree for fallback
global_coords = df[["lat_rad", "lon_rad"]].values
global_tree = BallTree(global_coords, metric="haversine")

results = []

print("[2/6] Computing ward+class KNN feature...")

for idx, row in df.iterrows():

    ward = row["WARD_BLOCK"]
    classification = row["CLASSIFICATION"]

    # Step 1: Ward + Class filter
    subset = df[
        (df["WARD_BLOCK"] == ward) &
        (df["CLASSIFICATION"] == classification)
    ]

    # If enough data
    if len(subset) > K:

        coords = subset[["lat_rad", "lon_rad"]].values
        tree = BallTree(coords, metric="haversine")

        point = np.array([[row["lat_rad"], row["lon_rad"]]])

        distances, indices = tree.query(point, k=K+1)

        # Drop itself
        neighbor_idxs = indices.flatten()[1:]

        avg_price = subset.iloc[neighbor_idxs]["base_value"].mean()

    # Fallback 1: Same classification only
    elif len(df[df["CLASSIFICATION"] == classification]) > K:

        subset = df[df["CLASSIFICATION"] == classification]

        coords = subset[["lat_rad", "lon_rad"]].values
        tree = BallTree(coords, metric="haversine")

        point = np.array([[row["lat_rad"], row["lon_rad"]]])

        distances, indices = tree.query(point, k=K+1)

        neighbor_idxs = indices.flatten()[1:]

        avg_price = subset.iloc[neighbor_idxs]["base_value"].mean()

    # Fallback 2: Global
    else:

        point = np.array([[row["lat_rad"], row["lon_rad"]]])

        distances, indices = global_tree.query(point, k=K+1)

        neighbor_idxs = indices.flatten()[1:]

        avg_price = df.iloc[neighbor_idxs]["base_value"].mean()

    results.append(round(avg_price, 2))

    if idx % 300 == 0:
        print(f"Processed {idx}/{len(df)}")

df["avg_local_ward_class_knn_10"] = results

# Drop temp rad columns
df = df.drop(columns=["lat_rad", "lon_rad"])

print("[3/6] Sanity check:")
print(df["avg_local_ward_class_knn_10"].describe())

print("[4/6] Saving file...")
df.to_csv(OUTPUT_FILE, index=False)

print("[5/6] DONE.")
print("Saved at:", OUTPUT_FILE)
