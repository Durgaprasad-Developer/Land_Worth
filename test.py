import pandas as pd
import requests
import time
import re

INPUT = "data/processed/vijayawada_street_level.csv"
OUTPUT = "data/processed/vijayawada_street_geocoded_osm.csv"

df = pd.read_csv(INPUT)

df["latitude"] = None
df["longitude"] = None

def clean_street(text):
    text = re.sub(r"\[.*?\]", "", str(text))
    return text.strip()

def geocode(address):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "landworth-hackathon-app"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return data["lat"], data["lon"]

    return None, None


print("Starting OSM Geocoding...")

for i, row in df.iterrows():

    street = clean_street(row["LOCALITY_STREET"])
    address = f"{street}, {row['SRNAME']}, Vijayawada, Andhra Pradesh, India"

    lat, lon = geocode(address)

    df.at[i, "latitude"] = lat
    df.at[i, "longitude"] = lon

    if i % 50 == 0:
        print(f"Processed {i}/{len(df)}")
        df.to_csv(OUTPUT, index=False)

    time.sleep(1)  # IMPORTANT (rate limit)

df.to_csv(OUTPUT, index=False)

print("OSM GEOCODING COMPLETE ✅")
