import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

# ---------------------------------------------------
# FILE PATHS
# ---------------------------------------------------

FEATURE_FILE = "data/processed/vijayawada_street_with_all_features.csv"
PRICE_REF_FILE = "data/processed/land_price_reference.csv"
OUTPUT_FILE = "data/processed/vijayawada_street_with_all_features_Model.csv"

EARTH_RADIUS = 6371000
K = 15

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

print("[1/6] Loading datasets...")

feature_df = pd.read_csv(FEATURE_FILE)
price_ref_df = pd.read_csv(PRICE_REF_FILE)

print("Feature rows:", len(feature_df))
print("Reference price rows:", len(price_ref_df))

# ---------------------------------------------------
# PREPARE COORDINATES
# ---------------------------------------------------

print("[2/6] Converting coordinates to radians...")

feature_coords = np.radians(
    feature_df[["latitude", "longitude"]].values
)

price_coords = np.radians(
    price_ref_df[["latitude", "longitude"]].values
)

# ---------------------------------------------------
# BUILD BALLTREE
# ---------------------------------------------------

print("[3/6] Building BallTree...")

tree = BallTree(price_coords, metric="haversine")

# ---------------------------------------------------
# QUERY K+1 (to exclude itself)
# ---------------------------------------------------

print("[4/6] Querying K nearest neighbors...")

distances, indices = tree.query(feature_coords, k=K+1)

neighbor_avgs = []

for i in range(len(feature_df)):

    neighbor_idxs = indices[i]

    # Remove itself (distance very close to zero)
    neighbor_idxs = neighbor_idxs[1:]

    neighbor_prices = price_ref_df.iloc[neighbor_idxs]["base_value"].values

    avg_price = np.mean(neighbor_prices)

    neighbor_avgs.append(round(avg_price, 2))

feature_df["avg_knn_base_value_15"] = neighbor_avgs

# ---------------------------------------------------
# SANITY CHECK
# ---------------------------------------------------

print("[5/6] Sanity check:")
print(feature_df["avg_knn_base_value_15"].describe())

# ---------------------------------------------------
# SAVE
# ---------------------------------------------------

print("[6/6] Saving file...")

feature_df.to_csv(OUTPUT_FILE, index=False)

print("DONE.")
print("Saved at:", OUTPUT_FILE)
