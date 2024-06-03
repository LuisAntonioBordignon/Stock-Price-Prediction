import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import pandas as pd
from tensorflow.keras.layers import LSTM as LSTM_layer, Input, Dropout # type: ignore
from tensorflow.keras.models import Sequential # type: ignore


class LSTM:
    def __init__(self, n_features: int, epochs: int, batch_size: int):
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = Sequential()

        self.model.add(Input(shape=(1, n_features)))
        self.model.add(LSTM_layer(512, activation="elu", return_sequences=True))
        self.model.add(LSTM_layer(512, activation="elu", return_sequences=True))
        self.model.add(LSTM_layer(4, activation="elu"))
        self.model.compile(
            optimizer="adam",
            loss="mean_squared_error",
            metrics=["mean_squared_error"]
        )

    def fit(self, X: pd.DataFrame, y: pd.Series):
        X = X.values.reshape((X.shape[0], 1, X.shape[1]))

        return self.model.fit(
            X,
            y,
            epochs=self.epochs,
            batch_size=self.batch_size,
            verbose=0,
            validation_split=0.2, 
        )

    def predict(self, X: pd.DataFrame):
        index = X.index
        X = X.values.reshape((X.shape[0], 1, X.shape[1]))

        return pd.DataFrame.from_records(
            data=self.model.predict(X),
            index=index,
            columns=("Open", "High", "Low", "Close"),
        )
