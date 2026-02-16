import os
from roads.download_roads import download_and_process_vijayawada_roads

OUTPUT = "data/processed/vijayawada_all_roads.csv"

print("Starting road extraction...")

df = download_and_process_vijayawada_roads()

os.makedirs("data/processed", exist_ok=True)

print("Saving CSV...")
df.to_csv(OUTPUT, index=False)

print("DONE. File saved at:", OUTPUT)
