from pathlib import Path

import pandas as pd

from src.models import *


TRAINING_DAYS = 5
tickers = list(Path("data/tickers/").glob("**/"))[1:]
histories = {}

for ticker in tickers:
    model = MLP()
    name = ticker.name
    histories[name] = []

    datasets = ticker.glob(f"*.parquet") 

    print(f"Estamos no ticker {name}!")

    for day, ticker in enumerate(tickers, 1):

        print(f"Dia {day}...")

        if day > TRAINING_DAYS:
            print(f"BREAK!!!!!")
            break

        X_train = pd.read_parquet(ticker, columns=["best_bid_price", "best_ask_price", "best_bid_qty", "best_ask_qty"])
        y_train = pd.read_parquet(ticker, columns=["mid_price"])

        history = model.fit(X_train, y_train)
        history = pd.DataFrame(history.history)
        histories[name].append(history)

    for ticker, history_list in histories.items():

        print(len(history_list))
        print(len(history_list[0]))

        history_df = pd.concat(history_list)
        history_df.to_parquet(f"data/histories/{type(model).__name__}-{ticker}.parquet")

    model.model.save(f"data/models/{type(model).__name__}-{name}.keras")