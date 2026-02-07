import pandas as pd
from ml_service.location_resolver.resolver import resolve_lat_lng_from_ward

INPUT_FILE = "data/processed/canonical_vijayawada.csv"
OUTPUT_FILE = "data/processed/canonical_with_location.csv"

df = pd.read_csv(INPUT_FILE)

latitudes = []
longitudes = []

for _, row in df.iterrows():
    # metadata is a STRING → we do NOT parse it
    # ward is also available directly inside metadata string,
    # but we already preserved WARD_BLOCK as a column in TB-1 output
    ward = None

    # Extract ward safely from metadata string
    if "WARD_BLOCK" in row["metadata"]:
        # very safe extraction
        try:
            ward = row["metadata"].split("WARD_BLOCK':")[1].split(",")[0].replace("'", "").strip()
        except Exception:
            ward = None

    lat, lng = resolve_lat_lng_from_ward(ward)
    latitudes.append(lat)
    longitudes.append(lng)

df["latitude"] = latitudes
df["longitude"] = longitudes

df.to_csv(OUTPUT_FILE, index=False)

print("TB-2 SUCCESS ✅")
print(df[["parcel_id", "latitude", "longitude"]].head())
