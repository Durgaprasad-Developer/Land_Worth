import pandas as pd
import re

# ---------------- INPUT FILES ----------------
CANONICAL = "data/processed/canonical_clean.csv"
ZONES = "data/processed/zone_geocoded.csv"
OUTPUT = "data/processed/zone_with_base_value.csv"

# ---------------- LOAD ----------------
df = pd.read_csv(CANONICAL)
zones = pd.read_csv(ZONES)

# ---------------- EXTRACT ZONE FIELDS ----------------
def extract_srname(meta):
    m = re.search(r"'SRNAME':\s*'([^']+)'", str(meta))
    return m.group(1) if m else None

def extract_sro(meta):
    m = re.search(r"'SRO_CODE':\s*(\d+)", str(meta))
    return m.group(1) if m else None

def extract_ward(meta):
    m = re.search(r"'WARD_BLOCK':\s*\"*'([^']+)'\"*", str(meta))
    return m.group(1) if m else None

df["SRNAME"] = df["metadata"].apply(extract_srname)
df["SRO_CODE"] = df["metadata"].apply(extract_sro)
df["WARD_BLOCK"] = df["metadata"].apply(extract_ward)

# ---------------- ZONE ID ----------------
df["ZONE_ID"] = (
    df["SRO_CODE"].astype(str)
    + "__"
    + df["SRNAME"].astype(str)
    + "__"
    + df["WARD_BLOCK"].astype(str)
)

# ---------------- AGGREGATE BASE VALUE (MEDIAN) ----------------
zone_price = (
    df.groupby("ZONE_ID")["base_value"]
      .median()
      .reset_index()
      .rename(columns={"base_value": "zone_base_value"})
)

# ---------------- MERGE WITH ZONES ----------------
final = zones.merge(zone_price, on="ZONE_ID", how="left")

final.to_csv(OUTPUT, index=False)

print("ZONE BASE VALUE ATTACHED ✅")
print("Rows:", len(final))
print(final.head())
print("Null base values:", final['zone_base_value'].isna().sum())
