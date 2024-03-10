import os
import pandas as pd

from .entities import BikeStationWithWeather


class DatasetManager:

    def __init__(self, data_path: str):
        self.data_path = data_path

    def save(self, station: BikeStationWithWeather):
        filename = f"{self.data_path}/mbajk_dataset_{station.name}.csv"

        if os.path.exists(filename):
            existing_df = pd.read_csv(filename)
            df = pd.DataFrame([station.dict()])
            df = pd.concat([existing_df, df], ignore_index=True)
            df.to_csv(filename, index=False)
        else:
            df = pd.DataFrame([station.dict()])
            df.to_csv(filename, index=False)
