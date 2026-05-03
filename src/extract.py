import pandas as pd


def load_csv(path: str) -> pd.DataFrame:

    df = pd.read_csv(path)
    df = df.dropna(subset=["artists", "track_name"])
    df["duration_ms"] = (df["duration_ms"] / 1000).astype(int)

    return df
