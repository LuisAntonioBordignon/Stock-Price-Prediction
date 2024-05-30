import pandas as pd
import numpy as np

"""
https://neptune.ai/blog/performance-metrics-in-machine-learning-complete-guide
"""

class Metrics:

    def __init__(self):
        pass

    def MSE(self, y_true: pd.DataFrame, y_pred: pd.DataFrame):
        """Mean Squared Error"""
        MSE = np.mean((y_true - y_pred) ** 2)

        return MSE
    
    def MAE(self, y_true: pd.DataFrame, y_pred: pd.DataFrame):
        """Mean Absolute Error"""
        MAE = np.mean(np.abs(y_true - y_pred))

        return MAE

    def RMSE(self, y_true: pd.DataFrame, y_pred: pd.DataFrame):
        """Root Mean Squared Error"""
        RMSE = np.sqrt(np.mean((y_true - y_pred) ** 2))

        return RMSE
    
    def MAPE(self, y_true: pd.DataFrame, y_pred: pd.DataFrame):
        """Mean Absolute Percentage Error"""
        MAPE = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

        return MAPE
    
    def R2(self, y_true: pd.DataFrame, y_pred: pd.DataFrame):
        """R-squared"""
        R2 = 1 - np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2)

        return R2

