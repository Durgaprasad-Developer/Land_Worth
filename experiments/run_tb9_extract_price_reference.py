import pandas as pd
import os

INPUT_FILE = "data/processed/vijayawada_street_geocoded_hybrid.csv"
OUTPUT_FILE = "data/processed/land_price_reference.csv"

print("[1/4] Loading dataset...")
df = pd.read_csv(INPUT_FILE)

print("Total rows:", len(df))

print("[2/4] Selecting required columns...")

price_df = df[[
    "base_value",
    "latitude",
    "longitude"
]].copy()

print("[3/4] Dropping missing values...")

price_df = price_df.dropna(subset=["base_value", "latitude", "longitude"])

print("Rows after cleaning:", len(price_df))

print("[4/4] Saving price reference dataset...")

os.makedirs("data/processed", exist_ok=True)
price_df.to_csv(OUTPUT_FILE, index=False)

print("DONE.")
print("Saved at:", OUTPUT_FILE)
