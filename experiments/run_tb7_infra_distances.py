import os
from infra.download_infra import download_vijayawada_infra

OUTPUT = "data/processed/vijayawada_all_infra.csv"

print("Starting infra extraction...")

infra_df = download_vijayawada_infra()

os.makedirs("data/processed", exist_ok=True)

print("Saving CSV...")
infra_df.to_csv(OUTPUT, index=False)

print("DONE. Saved at:", OUTPUT)
