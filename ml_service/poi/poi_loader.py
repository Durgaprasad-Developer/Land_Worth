# ml_service/poi/poi_loader.py
import osmnx as ox

def load_pois(place_name="Vijayawada, Andhra Pradesh, India"):
    """
    Load POIs (Points of Interest) from OpenStreetMap
    using OSMnx 2.x API
    """

    tags = {
        "amenity": True,
        "shop": True,
        "office": True,
        "public_transport": True
    }

    # OSMnx 2.x uses features_from_place
    gdf = ox.features_from_place(place_name, tags)

    # Keep only point geometries
    gdf = gdf[gdf.geometry.type == "Point"]

    # Ensure CRS
    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4326)

    return gdf
