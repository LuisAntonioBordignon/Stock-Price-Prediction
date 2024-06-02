import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow.keras.layers import LSTM as LSTM_layer, Dense, Input # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore
import pandas as pd


class LSTM:
    def __init__(self, epochs: int = 1, batch_size: int = 256):
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = Sequential()

        self.model.add(Input(shape=(1, 4)))
        self.model.add(LSTM_layer(units=128, activation="tanh"))
        self.model.add(Dense(units=10))
        self.model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mean_squared_error"])

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        # Reshape X_train to be 3D [samples, timesteps, features]
        X_train = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))

        early_stopping = EarlyStopping(monitor="val_loss", patience=2)

        return self.model.fit(
            X_train,
            y_train,
            epochs=self.epochs,
            batch_size=self.batch_size,
            verbose=1,
            callbacks=[early_stopping],
            validation_split=0.2, 
        )
