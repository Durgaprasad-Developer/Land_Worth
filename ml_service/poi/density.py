# ml_service/poi/density.py

import geopandas as gpd
from shapely.geometry import Point

def computee_poi_density(lat, lng, pois_gdf, radius_m=1000):
    """
    Count POIs within radius (meters)
    """

    # Land point

    point_gdf = gpd.GeoDataFrame(
        geometry=[Point(lng, lat)],
        crs="EPSG:4326"
    )

    pois_proj = pois_gdf.to_crs(epsg=3857)
    point_proj = point_gdf.to_crs(epsg=3857)

    buffer = point_proj.geometry.iloc[0].buffer(radius_m)

    count = pois_proj[pois_proj.geometry.within(buffer)].shape[0]

    return int(count)