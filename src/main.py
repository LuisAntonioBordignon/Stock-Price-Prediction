from pathlib import Path

import pandas as pd

from src.models import *


TRAINING_DAYS = 4
tickers = list(Path("data/tickers/").glob("**/"))[1:]
# tickers = [Path("data/tickers/BTC") ]

for ticker in tickers:
    model = MLP()
    name = ticker.name
    histories = []
    datasets = ticker.glob(f"*-raw.parquet")
    y_pred = None

    print(f"Estamos no ticker {name}!")

    for day, filename in enumerate(datasets, 1):
        print(f"Filename: {filename}")

        df = pd.read_parquet(filename)
        y_train = df["mid_price"]
        X_train = df.drop(columns=["mid_price"], level="features")

        if day > TRAINING_DAYS:
            y_pred = data=model.predict(X_train)
            break
        else:
            history = model.fit(X_train, y_train)
            histories.append(history)

    histories = pd.concat([pd.DataFrame(history.history) for history in histories])
    model_name = type(model).__name__

    histories.to_parquet(
        f"data/histories/{model_name}-{name}.parquet"
    )
    model.model.save(f"data/models/{model_name}-{name}.keras")
    pd.DataFrame(y_pred).to_parquet(Path("data/predictions") / f"{model_name}-{name}.parquet")

    del model # Ensure the model is reset for the next ticker
