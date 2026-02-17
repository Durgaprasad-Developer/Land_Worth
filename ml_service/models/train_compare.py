from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from utils import load_data, split_data, evaluate_model

CSV_PATH = "data/processed/vijayawada_street_with_all_features_Model.csv"


def train_and_evaluate(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    return evaluate_model(model, X_test, y_test)


def main():
    print("Loading data...")
    X, y = load_data(CSV_PATH)

    X_train, X_test, y_train, y_test = split_data(X, y)

    print("\nTraining RandomForest...")
    rf = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )
    rf_mae, rf_rmse, rf_r2 = train_and_evaluate(rf, X_train, y_train, X_test, y_test)

    print("\nTraining GradientBoosting...")
    gb = GradientBoostingRegressor(
        n_estimators=300,
        random_state=42
    )
    gb_mae, gb_rmse, gb_r2 = train_and_evaluate(gb, X_train, y_train, X_test, y_test)

    print("\n=== Model Comparison ===")
    print("\nRandomForest:")
    print(f"MAE  : {rf_mae:.2f}")
    print(f"RMSE : {rf_rmse:.2f}")
    print(f"R2   : {rf_r2:.4f}")

    print("\nGradientBoosting:")
    print(f"MAE  : {gb_mae:.2f}")
    print(f"RMSE : {gb_rmse:.2f}")
    print(f"R2   : {gb_r2:.4f}")


if __name__ == "__main__":
    main()
