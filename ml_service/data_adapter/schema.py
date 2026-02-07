#ml_service/data_adapter/schema.py

from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class CanonicalParcel:
    parcel_id: str
    latitude: float | None
    longitude: float | None
    base_value: float
    metadata: Dict[str, Any]