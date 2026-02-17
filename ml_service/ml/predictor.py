import os
import joblib
import numpy as np
from .feature_config import FEATURE_ORDER


MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "price_model.pkl")

# Load model once
model = joblib.load(MODEL_PATH)


def encode_classification(value):
    value = value.strip()
    mapping = {
        "Residential": 0,
        "Commercial": 1
    }
    return mapping.get(value, 0)


def predict_price(input_data: dict):
    """
    input_data must contain:
    - classification
    - avg_local_ward_class_knn_10
    - dist_highway_m
    - dist_main_road_m
    - dist_inner_road_m
    - dist_nearest_infra_m
    - latitude
    - longitude
    """

    encoded_class = encode_classification(input_data["classification"])

    feature_vector = [
        encoded_class,
        input_data["avg_local_ward_class_knn_10"],
        input_data["dist_highway_m"],
        input_data["dist_main_road_m"],
        input_data["dist_inner_road_m"],
        input_data["dist_nearest_infra_m"],
        input_data["latitude"],
        input_data["longitude"]
    ]

    feature_array = np.array(feature_vector).reshape(1, -1)

    prediction = model.predict(feature_array)[0]

    return round(float(prediction), 2)
