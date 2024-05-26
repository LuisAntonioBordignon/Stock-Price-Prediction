import os
import timeit

from models.MLP import *
from models.LSTM import *

class Environment:

    min_scale = 0
    max_scale = 1

    def __init__(self, model: classmethod):

        self.model = model
        self.name = model.__class__.__name__
        
        self.start_timer = timeit.default_timer()

    def fitting(self):

        for ticker in os.listdir("data/tickers"):
            for day in os.listdir(f"data/tickers/{ticker}"):

                print(day)

       




    # def _load_data(self, day: int):
        
        
