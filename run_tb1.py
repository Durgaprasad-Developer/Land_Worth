from ml_service.data_adapter.loader import load_dataset
from ml_service.data_adapter.adapter import (
    govt_to_canonical,
    canonical_to_dataframe
)

# change this to test both files
INPUT_FILE = "data/raw/Vijayawada_Land_Worth_1.xls"

df = load_dataset(INPUT_FILE)

records = govt_to_canonical(df)
final_df = canonical_to_dataframe(records)

final_df.to_csv("data/processed/canonical_vijayawada.csv", index=False)

print("TB-1 SUCCESS ✅")
print(final_df.head())
print("Total rows:", len(final_df))

# /home/durga-prasad/Downloads/Land_Worth/data/raw/Vijayawada_Land_Worth_2.xlsx
# /home/durga-prasad/Downloads/Land_Worth/data/raw/Vijayawada_Land_Worth_1.xls
