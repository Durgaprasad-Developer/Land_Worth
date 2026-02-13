import pandas as pd
import osmnx as ox
import re

INPUT = "data/processed/canonical_clean.csv"
OUTPUT = "data/processed/zone_geocoded.csv"

df = pd.read_csv(INPUT)

# -------- robust string extractors --------
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

# -------- ZONE ID --------
df["ZONE_ID"] = (
    df["SRO_CODE"].astype(str)
    + "__"
    + df["SRNAME"].astype(str)
    + "__"
    + df["WARD_BLOCK"].astype(str)
)

zones = df[["ZONE_ID", "SRNAME"]].drop_duplicates().reset_index(drop=True)

# -------- GEOCODE --------
lats, lngs = [], []

for i, row in zones.iterrows():
    place = f"{row['SRNAME']}, Vijayawada, Andhra Pradesh, India"
    try:
        lat, lng = ox.geocode(place)
    except Exception:
        lat, lng = None, None

    lats.append(lat)
    lngs.append(lng)

zones["latitude"] = lats
zones["longitude"] = lngs

zones.to_csv(OUTPUT, index=False)

print("ZONE GEOCODING DONE ✅")
print("Total zones:", len(zones))
print(zones.head())
