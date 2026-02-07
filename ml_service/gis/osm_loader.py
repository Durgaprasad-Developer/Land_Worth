# ml_service/gis/osm_loader.py

import osmnx as ox

def load_road_network(place_name="Vijayawada, Andhra Pradesh, India"):
    """
    Load road network from OpenStreetMap
    """
    G = ox.graph_from_place(place_name, network_type="drive")
    gdf_edges = ox.graph_to_gdfs(G, nodes=False)
    return gdf_edges

