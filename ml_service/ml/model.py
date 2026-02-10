from sklearn.ensemble import RandomForestRegressor

def build_model():
    return RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )