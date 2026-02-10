import pandas as pd

df = pd.read_csv("data/processed/canonical_with_poi_features.csv")

df = df.rename(columns={
    "po_density_1km": "poi_density_1km"
})

df.to_csv("data/processed/canonical_with_poi_features.csv", index=False)

print("Column renamed successfully ✅")
print(df.columns)
