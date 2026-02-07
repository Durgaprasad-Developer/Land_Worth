# ml_service/daa_adapter/loader.py

import pandas as pd
from pathlib import Path

def load_dataset(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if path.suffix in [".xls", ".xlsx"]:
        return pd.read_excel(path)
    elif path.suffix == ".csv":
        return pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")