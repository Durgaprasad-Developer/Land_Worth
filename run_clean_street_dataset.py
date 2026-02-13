import pandas as pd

INPUT = "data/raw/Vijayawada_Land_Worth_2.xlsx"
OUTPUT = "data/processed/vijayawada_street_level.csv"

# Load Excel
df = pd.read_excel(INPUT)

# Rename for clarity
df = df.rename(columns={
    "UNITRATE": "base_value",
    "GROUNDFLOOR": "ground_floor",
    "FIRSTFLOOR": "first_floor",
    "OTHERFLOOR": "other_floor"
})

# Keep only required columns
df = df[[
    "SRNAME",
    "SRO_CODE",
    "WARD_BLOCK",
    "LOCALITY_STREET",
    "base_value",
    "ground_floor",
    "first_floor",
    "other_floor",
    "CLASSIFICATION"
]]

# Remove rows with missing street names
df = df[df["LOCALITY_STREET"].notna()]

# Strip spaces
df["LOCALITY_STREET"] = df["LOCALITY_STREET"].str.strip()
df["SRNAME"] = df["SRNAME"].str.strip()

# Aggregate per STREET (median to be safe)
street_df = (
    df.groupby(["SRNAME", "SRO_CODE", "WARD_BLOCK", "LOCALITY_STREET", "CLASSIFICATION"])
      .median(numeric_only=True)
      .reset_index()
)

street_df.to_csv(OUTPUT, index=False)

print("STREET DATASET CREATED ✅")
print("Rows:", len(street_df))
print(street_df.head())
