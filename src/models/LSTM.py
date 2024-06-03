import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow.keras.layers import LSTM as LSTM_layer, Dense, Input, Dropout # type: ignore
from tensorflow.keras.regularizers import L1L2 # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore
import pandas as pd


class LSTM:
    def __init__(self, n_features: int, epochs: int, batch_size: int):
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = Sequential()

        self.model.add(Input(shape=(1, n_features)))

        self.model.add(LSTM_layer(512, activation="elu", return_sequences=True))
        self.model.add(LSTM_layer(512, activation="elu", return_sequences=True))
        self.model.add(LSTM_layer(4, activation="elu"))

        self.model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mean_squared_error"])

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):

        X_train = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))
        
        return self.model.fit(
            X_train,
            y_train,
            epochs=self.epochs,
            batch_size=self.batch_size,
            verbose=0,
            validation_split=0.2, 
        )
    

    def predict(self, X_test: pd.DataFrame):

        X_test_index = X_test.index
        X_test = X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1]))

        return pd.DataFrame.from_records(
            data=self.model.predict(X_test),
            index=X_test_index,
            columns=("Open", "High", "Low", "Close")
        )