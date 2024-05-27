from pathlib import Path

import pandas as pd


def __main__():
    tickers = ("ADA", "AXS", "BTC", "DOGE", "NEAR")

    for ticker in tickers:
        execute(ticker)

def execute(ticker: str, basedir: Path = Path.cwd() / "data"):
    data_dir = basedir / "tickers" / ticker
    dataframes = _process_dataframes(data_dir)

    for index, df in enumerate(dataframes, 1):
        filename = data_dir / f"{ticker}-day_{index}.parquet"

        df.to_parquet(filename)

def _process_dataframes(data_dir: Path):
    for df in _load_dataframes(data_dir):
        df["event_time"] = pd.to_datetime(df["event_time"], unit="ms")
        df["mid_price"] = (df["best_ask_price"] + df["best_bid_price"]) / 2

        yield df.set_index("event_time") 

def _load_dataframes(data_dir: Path):
    for data_file in data_dir.glob("*.csv"):
        yield pd.read_csv(
            data_file,
            usecols=[
                "best_ask_price",
                "best_ask_qty",
                "best_bid_price",
                "best_bid_qty",
                "event_time",
            ],
        )

        data_file.unlink()


if __name__ == "__main__":
    __main__()
