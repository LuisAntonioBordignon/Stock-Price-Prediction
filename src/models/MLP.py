import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import pandas as pd
from tensorflow.keras.layers import Dense, Input  # type: ignore
from tensorflow.keras.models import Sequential  # type: ignore


class MLP:
    def __init__(self, n_features: int, epochs: int, batch_size: int):
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = Sequential()

        self.model.add(Input(shape=(n_features, )))
        self.model.add(Dense(512, activation="elu"))
        self.model.add(Dense(512, activation="elu"))
        self.model.add(Dense(32, activation="elu"))
        self.model.add(Dense(4))
        self.model.compile(
            optimizer="adam",
            loss="mean_squared_error",
            metrics=["mean_squared_error"],
        )

    def fit(self, X: pd.DataFrame, y: pd.DataFrame):
        return self.model.fit(
            X,
            y,
            epochs=self.epochs,
            batch_size=self.batch_size,
            verbose=0,
            validation_split=0.2,
        )

    def predict(self, X: pd.DataFrame):
        return pd.DataFrame.from_records(
            data=self.model.predict(X),
            index=X.index,
            columns=("Open", "High", "Low", "Close"),
        )
