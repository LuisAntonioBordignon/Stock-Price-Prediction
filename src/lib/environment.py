import os
import timeit
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from tensorflow.keras.models import clone_model

from models.LSTM import *
from models.MLP import *


class Environment:
    min_scale = 0.0
    max_scale = 1.0

    def __init__(self, env: any):
        self.env = env
        self.name = env.__class__.__name__
        self.start_timer = timeit.default_timer()

    def fit(self, ticker: str = "**", target: str = "mid_price", data_dir: Path = Path.cwd() / "data" / "tickers"):
        for filename in data_dir.glob(f"{ticker}/*.parquet"):
            name = filename.parent.name
            X_train = pd.read_parquet(filename)
            y_train = X_train.drop(columns=[target])

            self.env.fit(X_train, y_train)
