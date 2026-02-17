import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from ml_service.models.utils import load_data, split_data

CSV_PATH = "data/processed/vijayawada_street_with_all_features_Model.csv"

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "price_model.pkl")


def main():
    print("Loading data...")
    X, y = load_data(CSV_PATH)

    print("Splitting data...")
    X_train, X_test, y_train, y_test = split_data(X, y)

    print("Training final RandomForest model...")
    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    print("Saving model...")
    joblib.dump(model, MODEL_PATH)

    print(f"Model saved at {MODEL_PATH}")


if __name__ == "__main__":
    main()
