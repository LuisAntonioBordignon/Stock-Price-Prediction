from pathlib import Path

import pandas as pd


class Script:
    ticker: str
    data_dir: Path

    def __init__(self, ticker: str, basedir: Path = Path.cwd() / "data"):
        """Download data, preprocess and save it to a file."""
        self.ticker = ticker
        self.data_dir = basedir / "tickers" / ticker

    def preprocess(self):
        for index, dataframe in enumerate(self._process_dataframes(), 1):
            filename = self.data_dir / f"{self.ticker}-day_{index}.parquet"

            dataframe.to_parquet(filename)

    def _process_dataframes(self):
        for df in self._load_dataframes():
            df["event_time"] = pd.to_datetime(df["event_time"], unit="ms")
            df["mid_price"] = (df["best_ask_price"] + df["best_bid_price"]) / 2

            yield df.set_index("event_time") 

    def _load_dataframes(self):
        for data_file in self.data_dir.glob("*.csv"):
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
    tickers = ["ADA", "AXS", "BTC", "DOGE", "NEAR"]

    for ticker in tickers:
        Script(ticker).preprocess()
