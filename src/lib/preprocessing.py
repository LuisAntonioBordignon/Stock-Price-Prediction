import os

import pandas as pd


class Preprocessing:
    def __init__(self):
        self.cripto_coins = os.listdir(f"data")
        self.cripto_coin_1_name = self.cripto_coins[0]
        self.cripto_coin_2_name = self.cripto_coins[1]
        self.cripto_coin_3_name = self.cripto_coins[2]
        self.cripto_coin_4_name = self.cripto_coins[3]
        self.cripto_coin_5_name = self.cripto_coins[4]

    @staticmethod
    def get_raw_data(raw_data_dir: str):
        cripto_data = []

        for cripto in os.listdir(raw_data_dir):
            cripto_dict = {}
            day_count = 1

            for day_folder in os.listdir(f"{raw_data_dir}/{cripto}"):
                for day_data in os.listdir(f"{raw_data_dir}/{cripto}/{day_folder}"):
                    day_data = pd.read_csv(f"{raw_data_dir}/{cripto}/{day_folder}/{day_data}")
                    cripto_dict[f"day_{day_count}"] = day_data
                    day_count += 1

            cripto_data.append(cripto_dict)

        return cripto_data
    
    # def concatenate_days(dict: dict):
        


    def remove_columns(self, dataframe, columns):
        dataframe = dataframe.drop(columns, axis=1)
        
        return dataframe