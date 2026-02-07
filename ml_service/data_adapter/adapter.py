# ml_service/data_adapter/adapter.py

import pandas as pd
from .schema import CanonicalParcel
from .mapping import RATE_COLUMNS

def get_base_value(row: pd.Series) -> float:
    for col in RATE_COLUMNS:
        if col in row and pd.notna(row[col]):
            return float(row[col])
    raise ValueError("No UNITRATE / UNIT_RATE column found")

def generate_parcel_id(row: pd.Series, index: int) -> str:
    sro = row.get("SRO_CODE", "SRO")
    ward = row.get("WARD_BLOCK", "WARD")
    return f"{sro}-{ward}-{index}"

def govt_to_canonical(df:pd.DataFrame) -> list[CanonicalParcel]:
    records = []

    for idx, row in df.iterrows():
        parcel = CanonicalParcel(
            parcel_id = generate_parcel_id(row, idx),
            latitude=None,
            longitude=None,
            base_value=get_base_value(row),
            metadata={
                **row.to_dict(),
                "unit": "INR_per_sq_yard"
            }
        )
        records.append(parcel)

    return records

def canonical_to_dataframe(records: list[CanonicalParcel]) -> pd.DataFrame:
    return pd.DataFrame([
        {
            "parcel_id": r.parcel_id,
            "latitude": r.latitude,
            "longtitude": r.longitude,
            "base_value": r.base_value,
            "metadata": r.metadata
        }
        for r in records
    ])