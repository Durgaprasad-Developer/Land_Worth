# ml_service/location_resolver/resolver.py

from .reference_points import WARD_CENTROIDS, VIJAYAWADA_FALLBACK

def resolve_lat_lng_from_ward(ward):
    if ward is not None:
        ward = str(ward)
        if ward in WARD_CENTROIDS:
            return WARD_CENTROIDS[ward]

    return VIJAYAWADA_FALLBACK
