import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from ml_service.ml.features import encode_road_type, compute_neighborhood_avg_price
from ml_service.ml.model import build_model

df = pd.read_csv("data/processed/canonical_with_road_features.csv")

df = encode_road_type(df)
df = compute_neighborhood_avg_price(df)

X = df[
    [
        "distance_to_road_m",
        "road_type_score",
        "neighborhood_avg_price"
    ]
]

y = df["base_value"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = build_model()
model.fit(X_train, y_train)

preds = model.predict(X_test)
print("R2 Score:", r2_score(y_test, preds))

for name, importance in zip(X.columns, model.feature_importance_):
    print(f"{name}: {importance:.3f}")