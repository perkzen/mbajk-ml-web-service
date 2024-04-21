from typing import List

import pandas as pd


class DataService:

    def __init__(self):
        self.dataset_path = "data/processed/"

    def get_latest_data(self, station_number: int) -> List[dict]:
        data = self.__get_bike_station_data(station_number)
        return data

    def __get_bike_station_data(self, station_number: int) -> List[dict]:
        file_name = f"{station_number}/mbajk_station_{station_number}.csv"
        return pd.read_csv(self.dataset_path + file_name).to_dict(orient="records")
