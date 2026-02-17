from sklearn.ensemble import RandomForestRegressor
from utils import load_data, split_data, evaluate_model
import numpy as np

CSV_PATH = "data/processed/vijayawada_street_with_all_features_Model.csv"


def main():
    print("Loading data...")
    X, y = load_data(CSV_PATH)

    # 🔥 Add this
    mean_price = np.mean(y)
    print(f"\nMean Base Value: {mean_price:.2f}")

    print("Splitting data...")
    X_train, X_test, y_train, y_test = split_data(X, y)

    print("Training RandomForest...")
    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    print("Evaluating model...")
    mae, rmse, r2 = evaluate_model(model, X_test, y_test)

    print("\n=== RandomForest Results ===")
    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R2   : {r2:.4f}")

    print("\nFeature Importances:")
    for feature, importance in zip(X.columns, model.feature_importances_):
        print(f"{feature}: {importance:.4f}")


if __name__ == "__main__":
    main()
