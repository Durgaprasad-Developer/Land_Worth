import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree
from scipy.spatial import KDTree
from geopy.distance import geodesic
import os

EARTH_RADIUS = 6371000
K = 15  # must match training

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ROADS_FILE = os.path.join(BASE_DIR, "data/processed/vijayawada_all_roads.csv")
INFRA_FILE = os.path.join(BASE_DIR, "data/processed/vijayawada_all_infra.csv")
PRICE_REF_FILE = os.path.join(BASE_DIR, "data/processed/land_price_reference.csv")


class SpatialEngine:

    def __init__(self):
        print("Initializing Spatial Engine...")

        # -------------------------
        # Load Roads
        # -------------------------
        roads_df = pd.read_csv(ROADS_FILE)

        self.highway_df = roads_df[roads_df["road_category"] == "Highway"]
        self.main_df = roads_df[roads_df["road_category"] == "Main Road"]
        self.inner_df = roads_df[roads_df["road_category"] == "Inner Road"]

        self.highway_tree = KDTree(self.highway_df[["latitude", "longitude"]].values)
        self.main_tree = KDTree(self.main_df[["latitude", "longitude"]].values)
        self.inner_tree = KDTree(self.inner_df[["latitude", "longitude"]].values)

        # -------------------------
        # Load Infra
        # -------------------------
        infra_df = pd.read_csv(INFRA_FILE)

        self.infra_coords = np.radians(
            infra_df[["latitude", "longitude"]].values
        )

        self.infra_tree = BallTree(self.infra_coords, metric="haversine")

        # -------------------------
        # Load Price Reference (KNN)
        # -------------------------
        self.price_ref_df = pd.read_csv(PRICE_REF_FILE)

        self.price_coords = np.radians(
            self.price_ref_df[["latitude", "longitude"]].values
        )

        self.price_tree = BallTree(self.price_coords, metric="haversine")

        print("Spatial Engine Ready.")

    # -----------------------------------------------------
    # ROAD DISTANCE
    # -----------------------------------------------------
    def _get_road_distance(self, tree, df_category, lat, lon):
        _, index = tree.query([lat, lon])
        nearest_point = df_category.iloc[index]
        nearest_coords = (
            nearest_point["latitude"],
            nearest_point["longitude"]
        )
        return geodesic((lat, lon), nearest_coords).meters

    # -----------------------------------------------------
    # MAIN FEATURE GENERATOR
    # -----------------------------------------------------
    def compute_features(self, lat, lon):

        # Road distances
        dist_highway = self._get_road_distance(
            self.highway_tree, self.highway_df, lat, lon
        )

        dist_main = self._get_road_distance(
            self.main_tree, self.main_df, lat, lon
        )

        dist_inner = self._get_road_distance(
            self.inner_tree, self.inner_df, lat, lon
        )

        # Infra nearest
        test_point = np.radians([[lat, lon]])

        dist_rad, _ = self.infra_tree.query(test_point, k=1)
        dist_infra = dist_rad[0][0] * EARTH_RADIUS

        # KNN Avg Price
        distances, indices = self.price_tree.query(test_point, k=K)

        neighbor_prices = self.price_ref_df.iloc[
            indices.flatten()
        ]["base_value"].values

        avg_knn_price = np.mean(neighbor_prices)

        return {
            "dist_highway_m": round(dist_highway, 2),
            "dist_main_road_m": round(dist_main, 2),
            "dist_inner_road_m": round(dist_inner, 2),
            "dist_nearest_infra_m": round(dist_infra, 2),
            "avg_local_ward_class_knn_10": round(avg_knn_price, 2)
        }


# Initialize globally (only once)
spatial_engine = SpatialEngine()
