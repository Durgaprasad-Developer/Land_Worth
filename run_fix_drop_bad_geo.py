import pandas as pd

INPUT = "data/processed/canonical_with_ml_features.csv"
OUTPUT = "data/processed/canonical_clean.csv"

df = pd.read_csv(INPUT)

# Drop all wrong / duplicate geo columns
cols_to_drop = [
    "latitude",
    "longtitude",   # typo column
    "longitude",    # duplicate
    "distance_to_road_m",
    "nearest_road_type",
    "poi_density_1km",
    "neighborhood_avg_price"
]

df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

df.to_csv(OUTPUT, index=False)

print("BAD GEO COLUMNS DROPPED ✅")
print(df.columns)
