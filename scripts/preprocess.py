from pathlib import Path

import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler


def __main__():
    tickers = ("ADA", "AXS", "BTC", "DOGE", "NEAR")

    for ticker in tickers:
        execute(ticker)

def execute(ticker: str, basedir: Path = Path.cwd() / "data"):
    data_dir = basedir / "tickers" / ticker
    dataframes = _process_dataframes(data_dir)

    for index, df in enumerate(dataframes, 1):
        df.to_parquet(data_dir / f"{ticker}-day_{index}-raw.parquet", )

        df = _normalize_dataframe(df)

        df.to_parquet(data_dir / f"{ticker}-day_{index}-normalized.parquet")

def _process_dataframes(data_dir: Path):
    for df in _load_dataframes(data_dir):
        RESEMPLE_TIME = "10s"

        df["event_time"] = pd.to_datetime(df["event_time"], unit="ms")
        df["mid_price"] = (df["best_ask_price"] + df["best_bid_price"]) / 2
        df = df.set_index("event_time")

        columns = df.columns
        df = df.resample(RESEMPLE_TIME).agg("mean")
        df.columns = columns

        yield df

def _load_dataframes(data_dir: Path):
    for data_file in data_dir.glob("*.csv"):
        yield pd.read_csv(
            data_file,
            usecols=[
                "event_time",
                "best_ask_price",
                "best_ask_qty",
                "best_bid_price",
                "best_bid_qty",
            ],
        )

        # data_file.unlink()

def _normalize_dataframe(df: pd.DataFrame):
    scaler = StandardScaler()

    return pd.DataFrame.from_records(
        data=scaler.fit_transform(df.values),
        index=df.index,
        columns=df.columns
    )


if __name__ == "__main__":
    __main__()
