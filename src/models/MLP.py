import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Sequential
import pandas as pd

class MLP:

    def __init__(self):
        
        self.model = Sequential()
        self.model.add(Input(shape=(4,)))
        self.model.add(Dense(8, activation="relu"))
        self.model.add(Dense(8, activation="relu"))
        self.model.add(Dense(3, activation="softmax"))
        self.model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    def fitting(self, X_train: pd.DataFrame, y_train: pd.DataFrame) :
        
        # return self.model.fit(
        #     X_train, 
        #     y_train, 
        #     epochs=100, 
        #     batch_size=32, 
        #     verbose=0
        # )

        return print(f"Fitting (AAAAA)")

    