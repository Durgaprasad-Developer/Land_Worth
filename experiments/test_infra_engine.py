import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

INFRA_FILE = "data/processed/vijayawada_all_infra.csv"

EARTH_RADIUS = 6371000  # meters
RADIUS_METERS = 1000

print("[1/4] Loading infra dataset...")
infra_df = pd.read_csv(INFRA_FILE)

print("Infra rows:", len(infra_df))

if len(infra_df) == 0:
    raise ValueError("Infra dataset is empty.")

print("[2/4] Preparing BallTree...")

infra_coords = np.radians(
    infra_df[["latitude", "longitude"]].values
)

tree = BallTree(infra_coords, metric="haversine")

radius_rad = RADIUS_METERS / EARTH_RADIUS

print("Radius (radians):", radius_rad)

print("[3/4] Running manual tests...")

sample_points = [
    ("GUNADALA_1", 16.519099963348015, 80.65786169622751),
    ("NUNNA_1", 16.57951040173136, 80.68427196563029),
    ("PATAMATA_1", 16.49409749323684, 80.66316483364498),
    ("VIJAYAWADA_1", 16.512498294562313, 80.616184427539),
]

for name, lat, lon in sample_points:

    test_point = np.radians([[lat, lon]])

    # Nearest infra
    dist_rad, _ = tree.query(test_point, k=1)
    nearest_m = dist_rad[0][0] * EARTH_RADIUS

    # Density
    count = tree.query_radius(test_point, r=radius_rad, count_only=True)

    print("\n--------------------------------")
    print("Location:", name)
    print("Lat/Lon:", lat, lon)
    print("Nearest infra distance (m):", round(nearest_m, 2))
    print("Infra count within 1000m:", count[0])

print("\n[4/4] Test complete.")
