# Highway categories mapping

HIGHWAY_TYPES = [
    "motorway", "motorway_link",
    "trunk", "trunk_link"
]

MAIN_ROAD_TYPES = [
    "primary", "primary_link",
    "secondary", "secondary_link",
    "tertiary", "tertiary_link"
]

INNER_ROAD_TYPES = [
    "residential",
    "service",
    "unclassified",
    "living_street",
    "road"
]


def classify_road(highway_value):

    # Sometimes highway comes as list
    if isinstance(highway_value, list):
        highway_value = highway_value[0]

    if highway_value in HIGHWAY_TYPES:
        return "Highway"

    elif highway_value in MAIN_ROAD_TYPES:
        return "Main Road"

    elif highway_value in INNER_ROAD_TYPES:
        return "Inner Road"

    else:
        return None  # Ignore unwanted types
