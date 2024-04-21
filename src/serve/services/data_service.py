from typing import List

import pandas as pd


class DataService:

    def __init__(self):
        self.dataset_path = "data/processed"

    def get_latest_data(self, station_number: int) -> List[dict]:
        data = self.__get_bike_station_data(station_number)

        return data

    @staticmethod
    def __get_bike_station_data(station_number: int) -> List[dict]:
        url = f"https://dagshub.com/perkzen/mbajk-ml-web-service/raw/main/data/processed/{station_number}/mbajk_station_{station_number}.csv"
        df = pd.read_csv(url)
        df = df.drop(columns=["date"])
        return df.to_dict(orient="records")
