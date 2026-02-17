import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np


FEATURE_COLUMNS = [
    "CLASSIFICATION",
    "avg_local_ward_class_knn_10",
    "dist_highway_m",
    "dist_main_road_m",
    "dist_inner_road_m",
    "dist_nearest_infra_m",
    "latitude",
    "longitude"
]

TARGET_COLUMN = "base_value"


def load_data(csv_path):
    df = pd.read_csv(csv_path)

    # Encode CLASSIFICATION
    df["CLASSIFICATION"] = df["CLASSIFICATION"].str.strip()
    df["CLASSIFICATION"] = df["CLASSIFICATION"].map({
        "Residential": 0,
        "Commercial": 1
    })

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    return X, y


def split_data(X, y, test_size=0.3):
    return train_test_split(
        X, y,
        test_size=test_size,
        random_state=42
    )


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    return mae, rmse, r2
