import pandas as pd

INPUT = "data/processed/canonical_vijayawada.csv"
OUTPUT = "data/processed/zone_table.csv"

df = pd.read_csv(INPUT)

# Create ZONE_ID
df["ZONE_ID"] = df["WARD_BLOCK"].astype(str) + "__" + df["LOCALITY_STREET"].astype(str)

# Pick ONE representative lat/lng per zone
zone_df = (
    df.groupby("ZONE_ID")
      .agg({
          "WARD_BLOCK": "first",
          "LOCALITY_STREET": "first",
          "latitude": "first",
          "longitude": "first",
          "base_value": "mean"   # zone avg base value
      })
      .reset_index()
)

zone_df.to_csv(OUTPUT, index=False)

print("ZONE TABLE CREATED ✅")
print("Total zones:", len(zone_df))
print(zone_df.head())
