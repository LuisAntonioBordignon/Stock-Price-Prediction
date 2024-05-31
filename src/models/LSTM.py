import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import pandas as pd
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Sequential


class LSTM:
    def __init__(self, epochs: int = 10, batch_size: int = 32):
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        return None
