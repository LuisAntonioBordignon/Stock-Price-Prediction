import os
import timeit

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from tensorflow.keras.models import clone_model

from models.MLP import *
from models.LSTM import *


class Environment:

    min_scale = 0
    max_scale = 1

    def __init__(self, base_model: classmethod):

        self.base_model = base_model
        self.name = base_model.__class__.__name__

        self.start_timer = timeit.default_timer()

    def fitting(self):

        for ticker in os.listdir("data/tickers"):

            ticker_model = self.base_model

            for day in os.listdir(f"data/tickers/{ticker}"):

                self._load_data(ticker, day)


    def _load_data(self, ticker: str, day: int):

        day_count = 1
        for file in os.listdir(f"data/tickers/{ticker}"):

            if file.endswith(".csv"):

                if day_count == day:

                    data = pd.read_csv(f"data/tickers/{ticker}/{file}", usecols=)

                    X = data.drop(columns=["target"])
                    y = data["target"]



