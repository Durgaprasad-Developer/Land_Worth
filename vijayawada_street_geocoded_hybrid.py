import pandas as pd
import os
import time
import json
import re
import random
import google.generativeai as genai
from dotenv import load_dotenv
import osmnx as ox

# ===================================
# CONFIG
# ===================================

INPUT = "data/processed/vijayawada_street_level.csv"
OUTPUT = "data/processed/vijayawada_street_geocoded_hybrid.csv"

random.seed(42)

# ===================================
# GEMINI SETUP
# ===================================

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ===================================
# LOAD DATA
# ===================================

df = pd.read_csv(INPUT)
df["latitude"] = None
df["longitude"] = None

# ===================================
# CLEAN STREET
# ===================================

def clean_street(text):
    text = re.sub(r"\[.*?\]", "", str(text))  # remove ward blocks
    return text.strip()

# ===================================
# GEMINI GEOCODE
# ===================================

def gemini_geocode(address):

    prompt = f"""
    You are a geocoding system.
    Return ONLY valid JSON.
    No explanation.

    Format:
    {{
        "latitude": float,
        "longitude": float
    }}

    Location:
    {address}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]

        data = json.loads(json_text)

        return float(data["latitude"]), float(data["longitude"])

    except:
        return None, None

# ===================================
# OSM FALLBACK (SRNAME LEVEL)
# ===================================

def osm_fallback(srname):
    try:
        lat, lon = ox.geocode(f"{srname}, Vijayawada, Andhra Pradesh, India")
        return lat, lon
    except:
        return None, None

# ===================================
# SMALL JITTER (avoid identical coords)
# ===================================

def jitter(lat, lon, meters=120):
    delta = meters / 111000
    return (
        lat + random.uniform(-delta, delta),
        lon + random.uniform(-delta, delta)
    )

# ===================================
# MAIN LOOP
# ===================================

print("Starting HYBRID Geocoding...")

for i, row in df.iterrows():

    street = clean_street(row["LOCALITY_STREET"])
    address = f"{street}, {row['SRNAME']}, Vijayawada, Andhra Pradesh, India"

    # 1️⃣ Try Gemini
    lat, lon = gemini_geocode(address)

    # 2️⃣ Fallback to SRNAME if Gemini fails
    if lat is None or lon is None:
        lat, lon = osm_fallback(row["SRNAME"])

    # 3️⃣ Add slight jitter if we got something
    if lat is not None and lon is not None:
        lat, lon = jitter(lat, lon)

    df.at[i, "latitude"] = lat
    df.at[i, "longitude"] = lon

    if i % 20 == 0:
        print(f"Processed {i}/{len(df)}")
        df.to_csv(OUTPUT, index=False)

    time.sleep(1.2)  # stable speed

df.to_csv(OUTPUT, index=False)

print("HYBRID GEOCODING COMPLETE ✅")
print("Missing:", df["latitude"].isna().sum())
