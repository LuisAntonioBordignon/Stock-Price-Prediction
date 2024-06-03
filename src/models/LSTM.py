import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow.keras.layers import LSTM as LSTM_layer, Dense, Input, Dropout # type: ignore
from tensorflow.keras.regularizers import L1L2 # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore
import pandas as pd


class LSTM:
    def __init__(self, epochs: int = 10, batch_size: int = 8):
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = Sequential()

        self.model.add(Input(shape=(1, 17)))
        self.model.add(LSTM_layer(units=4, activation="tanh", kernel_regularizer=L1L2(0.03, 0.03)))
        self.model.add(Dropout(0.5))
        self.model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mean_squared_error"])

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        # Reshape X_train to be 3D [samples, timesteps, features]
        X_train = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))

        return self.model.fit(
            X_train,
            y_train,
            epochs=self.epochs,
            batch_size=self.batch_size,
            verbose=1,
            validation_split=0.2, 
        )
    
        def predict(self, X):
            # Reshape X to be 3D [samples, timesteps, features]
            X = X.values.reshape((X.shape[0], 1, X.shape[1]))
            return self.model.predict(X)
