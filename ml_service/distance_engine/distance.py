import geopandas as gpd
from shapely.geometry import Point
from ml_service.gis.road_classifier import classify_road


def compute_nearest_road_features(lat, lng, roads_gdf):
    """
    Compute distance to nearest road using proper projected CRS (meters)
    """

    # 1️⃣ Create GeoDataFrame for land point
    point_gdf = gpd.GeoDataFrame(
        geometry=[Point(lng, lat)],
        crs="EPSG:4326"
    )

    # 2️⃣ Ensure roads CRS
    if roads_gdf.crs is None:
        roads_gdf = roads_gdf.set_crs(epsg=4326)

    # 3️⃣ Project both to meter-based CRS
    roads_projected = roads_gdf.to_crs(epsg=3857)
    point_projected = point_gdf.to_crs(epsg=3857)

    # 4️⃣ Compute distances in meters
    roads_projected["distance_m"] = roads_projected.geometry.distance(
        point_projected.geometry.iloc[0]
    )

    nearest = roads_projected.loc[roads_projected["distance_m"].idxmin()]

    road_type = classify_road(nearest["highway"])

    return float(nearest["distance_m"]), road_type
