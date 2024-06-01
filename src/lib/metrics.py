import pandas as pd
import numpy as np


class Metrics:
    """
    Performance Metrics in Machine Learning
    From: https://neptune.ai/blog/performance-metrics-in-machine-learning-complete-guide
    """

    @staticmethod
    def MSE(y_true: pd.DataFrame, y_pred: pd.DataFrame):
        """Mean Squared Error"""
        return np.mean(np.square(y_true - y_pred))

    @staticmethod
    def MAE(y_true: pd.DataFrame, y_pred: pd.DataFrame):
        """Mean Absolute Error"""
        return np.mean(np.abs(y_true - y_pred))

    @staticmethod
    def RMSE(y_true: pd.DataFrame, y_pred: pd.DataFrame):
        """Root Mean Squared Error"""
        return np.sqrt(Metrics.MSE(y_true, y_pred))
    
    @staticmethod
    def MAPE(y_true: pd.DataFrame, y_pred: pd.DataFrame):
        """Mean Absolute Percentage Error"""
        return np.mean(np.abs((y_true - y_pred) / y_true))

    @staticmethod
    def R2(y_true: pd.DataFrame, y_pred: pd.DataFrame):
        """R-squared"""
        SE_line = np.sum(np.square(y_true - y_pred))
        SE_mean = np.sum(np.square(y_true - np.mean(y_true)))

        return 1 - SE_line / SE_mean

    @staticmethod
    def ddjusted_R2(y_true: pd.DataFrame, y_pred: pd.DataFrame):
        """Adjusted R-squared"""
        n, k = y_true.shape

        return 1 - ((n - 1) / (n - k - 1)) * (1 - Metrics.R2(y_true, y_pred))
