import pandas as pd
import numpy as np

class Metrics:

    def __init__(self):
        pass

    def RMSE(self, y_true: pd.DataFrame, y_pred: pd.DataFrame):
        RMSE = np.sqrt(np.mean((y_true - y_pred) ** 2))

        return RMSE

