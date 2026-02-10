import pandas as pd

def encode_road_type(df):
    mapping = {
        "highway":3,
        "main_road":2,
        "inner_road":1,
    }
    df["road_type_score"] = df["nearest_road_type"].map(mapping)
    return df


def compute_neighborhood_avg_price(df, radius_m=1000):
    df["neighborhood_avg_price"] = (
        df.groupby("nearest_road_type")["base_value"].transform("mean")
    )
    return df