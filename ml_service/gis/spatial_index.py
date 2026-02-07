# ml_service/gis/spatial_index.py

from shapely.geometry import Point

def prepare_road_geometries(roads_gdf):
    """
    Clean and return road geometries
    """
    roads_gdf = roads_gdf.dropna(subset=["geometry"])
    return roads_gdf