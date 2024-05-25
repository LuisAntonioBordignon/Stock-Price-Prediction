from pathlib import Path

import pandas as pd


class Script:
    ticker: str
    data_dir: Path

    def __init__(self, ticker: str, basedir: Path = Path.cwd() / "data"):
        """Download data, preprocess and save it to a file."""
        self.ticker = ticker
        self.data_dir = basedir / ticker
    
    def preprocess(self):
        preprocessed_dataframes = self._process_dataframes()

        for index, dataframe in enumerate(preprocessed_dataframes):
            filename = self.data_dir / f"{self.ticker}-day_{index}.parquet"

            dataframe.to_parquet(filename, index=False)

    def _process_dataframes(self):
        for dataframe in self._load_dataframes():
            mid_price = (dataframe["best_ask_price"] + dataframe["best_bid_price"]) / 2

            yield dataframe.assign(mid_price=mid_price)

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
