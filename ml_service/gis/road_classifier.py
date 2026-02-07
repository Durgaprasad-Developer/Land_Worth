# ml_service/gis/road_classifier.py

def classify_road(highway_tag):
    """
    Convert OSM highway tags into simple classes
    """
    if highway_tag in ["motorway", "trunk", "primary"]:
        return "highway"
    elif highway_tag in ["secondary", "tertiary"]:
        return "main_road"
    else:
        return "inner_road"