import pandas as pd

df = pd.read_csv("data/processed/vijayawada_street_geocoded_hybrid.csv")

print(df.columns)
print(df["CLASSIFICATION"].value_counts())
