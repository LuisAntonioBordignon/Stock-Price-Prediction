from pathlib import Path

import pandas as pd

from src.models import *
from src.lib.metrics import Metrics


TRAINING_DAYS = 4
tickers = list(Path("data/tickers/").glob("**/"))[1:]

for ticker in tickers:
    model = LSTM(17, 5, 256)
    name = ticker.name
    histories = []
    datasets = ticker.glob(f"*-normalized.parquet")

    print(f"Estamos no ticker {name}!")

    for day, filename in enumerate(datasets, 1):
        print(f"Filename: {filename}")

        df = pd.read_parquet(filename)
        y = df["mid_price"]
        X = df.drop(columns=["mid_price"], level="features")

        if day > TRAINING_DAYS:
            break
        else:
            history = model.fit(X, y)
            histories.append(history)

    y_hat = model.predict(X)
    histories = pd.concat([pd.DataFrame(history.history) for history in histories])
    model_name = type(model).__name__

    histories.to_parquet(
        f"data/histories/{model_name}-{name}.parquet"
    )
    model.model.save(f"data/models/{model_name}-{name}.keras")
    y_hat.to_parquet(Path("data/predictions") / f"{model_name}-{name}.parquet")

    RMSPE_Open = Metrics.RMSPE(y["Open"], y_hat["Open"])
    RMSPE_High = Metrics.RMSPE(y["High"], y_hat["High"])
    RMSPE_Low = Metrics.RMSPE(y["Low"], y_hat["Low"])
    RMSPE_Close = Metrics.RMSPE(y["Close"], y_hat["Close"])

    RMSE = pd.DataFrame.from_dict({
        "Open": [RMSPE_Open],
        "High": [RMSPE_High],
        "Low":[RMSPE_Low],
        "Close": [RMSPE_Close],
    })

    RMSE.to_parquet(Path("data/RMSPE") / f"{model_name}-{name}.parquet")

    del model # Ensure the model is reset for the next ticker
