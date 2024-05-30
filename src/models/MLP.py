import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


import pandas as pd
from tensorflow.keras.layers import Dense, Input # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore



class MLP:
    def __init__(self, epochs: int = 10, batch_size: int = 256):
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = Sequential()

        self.model.add(Input(shape=(4,)))
        self.model.add(Dense(512, activation="elu"))
        self.model.add(Dense(512, activation="elu"))
        self.model.add(Dense(32, activation="elu"))
        self.model.add(Dense(10))

        self.model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mean_squared_error"])

    def fit(self, X_train: pd.DataFrame, y_train: pd.DataFrame):
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
