import osmnx as ox
import pandas as pd


def download_vijayawada_infra():

    print("[1/6] Downloading ALL infrastructure from OSM...")

    tags = {
        "amenity": True,
        "shop": True,
        "railway": True,
        "aeroway": True,
        "public_transport": True
    }

    gdf = ox.features_from_place(
        "Vijayawada, Andhra Pradesh, India",
        tags
    )

    print("[2/6] Resetting index...")
    gdf = gdf.reset_index()

    infra_rows = []

    print("[3/6] Extracting valid infra entries...")

    for idx, row in gdf.iterrows():

        geometry = row.get("geometry")
        if geometry is None:
            continue

        # Extract infra type (first non-null valid tag)
        infra_type = (
            row.get("amenity")
            or row.get("shop")
            or row.get("railway")
            or row.get("aeroway")
            or row.get("public_transport")
        )

        if not infra_type:
            continue

        # Extract coordinates
        try:
            if geometry.geom_type == "Point":
                lat = geometry.y
                lon = geometry.x
            else:
                centroid = geometry.centroid
                lat = centroid.y
                lon = centroid.x
        except Exception:
            continue

        # Skip invalid coordinates
        if pd.isna(lat) or pd.isna(lon):
            continue

        infra_rows.append({
            "infra_type_raw": infra_type,
            "latitude": float(lat),
            "longitude": float(lon)
        })

        if idx % 500 == 0:
            print(f"Processed {idx}/{len(gdf)}")

    print("[4/6] Creating DataFrame...")
    infra_df = pd.DataFrame(infra_rows)

    print("[5/6] Cleaning dataset...")

    # Remove blank types
    infra_df = infra_df[infra_df["infra_type_raw"].notna()]

    # Remove duplicates by coordinates
    infra_df = infra_df.drop_duplicates(subset=["latitude", "longitude"])

    # Reset index
    infra_df = infra_df.reset_index(drop=True)

    print("[6/6] Final infra count:", len(infra_df))

    return infra_df
