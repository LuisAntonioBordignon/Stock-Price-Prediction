import os
import timeit
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from src.models.LSTM import *
from src.models.MLP import *


class Environment:
    min_scale = 0.0
    max_scale = 1.0

    def __init__(self, env: any):
        self.env = env
        self.name = env.__class__.__name__
        self.start_timer = timeit.default_timer()

    def fit(self, ticker: str, training_days: int, target: str = "mid_price", data_dir: Path = Path.cwd() / "data" / "tickers"):

        histories = []
        tickers = data_dir.glob(f"{ticker}/*.parquet") 

        for n, ticker in enumerate(tickers, 1):

            if n > training_days:

                print(f"BREAK!!!!!")
                break

            X_train = pd.read_parquet(ticker, columns=["best_bid_price", "best_bid_qty", "best_ask_price", "best_ask_qty"])
            y_train = pd.read_parquet(ticker, columns=[target])

            history = self.env.fit(X_train, y_train)
            print(f"History: {history.history}")
            histories.append(history)

        

        return histories

