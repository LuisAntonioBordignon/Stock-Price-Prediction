import os

import pandas as pd


class Script:

    ticker: str
    data_dir: str

    def __init__(self, ticker):
        """Download data, preprocess and save it to a file."""
        self.ticker = ticker
        self.data_dir = f"data/{ticker}"

    def _DownloadData(self):
        """Download data from Binance API."""
        pass

    def GetData(self):
        list_of_dataframes = []

        for file in os.listdir(self.data_dir):
            if file.endswith(".csv"):

                dataframe = pd.read_csv(
                    f"{self.data_dir}/{file}",
                    usecols=[
                        "best_ask_price"
                        "best_ask_qty"
                        "best_bid_price"
                        "best_bid_qty"
                        "event_time"
                    ],
                )

                list_of_dataframes.append(dataframe)

        return list_of_dataframes

    def _Preprocess(self):
        self._DownloadData()

        list_of_dataframes = self.GetData()

        list_of_preprocessed_dataframes = [
            dataframe.assign(
                mid_price=(dataframe["best_ask_price"] + dataframe["best_bid_price"])
                / 2
            )
            for dataframe in list_of_dataframes
        ]

        return list_of_preprocessed_dataframes
    
    def SaveData(self):
        list_of_preprocessed_dataframes = self._Preprocess()

        for i, dataframe in enumerate(list_of_preprocessed_dataframes):
            dataframe.to_parquet(f"{self.data_dir}/{self.ticker}-day_{i}.parquet", index=False)

        return True
