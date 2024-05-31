from pathlib import Path

import pandas as pd

from src.models import *


TRAINING_DAYS = 5
tickers = list(Path("data/tickers/").glob("**/"))[1:]

for ticker in tickers:
    model = MLP()
    name = ticker.name
    histories = []

    datasets = ticker.glob(f"*.parquet")

    print(f"Estamos no ticker {name}!")

    for day in range(1, TRAINING_DAYS + 1):

        print(f"Dia {day} no ticker {name}!")

        X_train = pd.read_parquet(
            ticker,
            columns=[
                "best_bid_price",
                "best_ask_price",
                "best_bid_qty",
                "best_ask_qty",
            ],
        )
        y_train = pd.read_parquet(ticker, columns=["mid_price"])

        X_train = X_train.iloc[:100, :]
        y_train = y_train.iloc[:100, :]

        history = model.fit(X_train, y_train)
        histories.append(history)

    histories = pd.concat([pd.DataFrame(history.history) for history in histories])

    histories.to_parquet(
        f"data/histories/{type(model).__name__}-{name}.parquet"
    )
    model.model.save(f"data/models/{type(model).__name__}-{name}.keras")
