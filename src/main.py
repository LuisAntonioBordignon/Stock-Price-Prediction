from pathlib import Path

import pandas as pd

from src.models import *


TRAINING_DAYS = 5
tickers = list(Path("data/tickers/").glob("**/"))[1:]
histories = {}

for ticker in tickers:
    name = ticker.name
    histories[name] = []
    model = MLP(batch_size=2)
    datasets = ticker.glob(f"*.parquet") 

    for day, ticker in enumerate(tickers, 1):
        if day > TRAINING_DAYS:
            print(f"BREAK!!!!!")
            break

        X_train = pd.read_parquet(ticker)
        y_train = X_train["mid_price"]

        X_train.drop(columns=["mid_price"], inplace=True)

        history = model.fit(X_train, y_train)

        histories[name].append(history)

print(f"histories: {histories}")
