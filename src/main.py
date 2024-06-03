from pathlib import Path

import pandas as pd

from src.models import *


TRAINING_DAYS = 4
tickers = list(Path("data/tickers/").glob("**/"))[1:]
# tickers = [Path("data/tickers/BTC") ]

for ticker in tickers:
    model = MLP(TRAINING_DAYS)
    name = ticker.name
    histories = []
    datasets = ticker.glob(f"*-raw.parquet")
    y_pred = None

    print(f"Estamos no ticker {name}!")

    for day, filename in enumerate(datasets, 1):
        print(f"Dia {day} no ticker {name}!")

        X_train = pd.read_parquet(
            filename,
            columns=[
                "best_bid_price",
                "best_ask_price",
                "best_bid_qty",
                "best_ask_qty",
            ],
        )

        X_train = X_train.iloc[::100, :]

        if day > TRAINING_DAYS: # If this, it's test day!
            y_pred = pd.DataFrame.from_records(
                data=model.model.predict(X_train),
                index=X_train.index,
            )
            break
        else:
            y_train = pd.read_parquet(filename, columns=["mid_price"])

            y_train = y_train.iloc[::100, :]

            history = model.fit(X_train, y_train)
            histories.append(history)

    histories = pd.concat([pd.DataFrame(history.history) for history in histories])
    model_name = type(model).__name__

    histories.to_parquet(
        f"data/histories/{model_name}-{name}.parquet"
    )
    model.model.save(f"data/models/{model_name}-{name}.keras")
    pd.DataFrame(y_pred).to_parquet(Path("data/predictions") / f"{model_name}-{name}.parquet")
