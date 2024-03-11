import os
import pandas as pd
from typing import List
from sklearn.feature_selection import mutual_info_regression

from .entities import BikeStationWithWeather
from ..config import TOP_FEATURES_NUMBER


class DatasetManager:

    def __init__(self, data_path: str):
        self.data_path = data_path

    def save(self, folder: str, station: BikeStationWithWeather) -> pd.DataFrame:
        file_path = f"{self.data_path}/{folder}/mbajk_dataset_{station.name}.csv"

        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path)
            df = pd.DataFrame([station.dict()])
            df = pd.concat([existing_df, df], ignore_index=True)
            df.to_csv(file_path, index=False)
            return df
        else:
            df = pd.DataFrame([station.dict()])
            df.to_csv(file_path, index=False)
            return df

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        # filename = f"{self.data_path}/{dataset_path}"
        #
        # if not os.path.exists(filename):
        #     raise FileNotFoundError(f"File {filename} not found")
        #
        # df = pd.read_csv(filename)

        df["date"] = pd.to_datetime(df["date"])
        df.sort_values(by="date", inplace=True)

        df.drop(columns=["name", "address", "date"], inplace=True)

        target = "available_bike_stands"

        top_features = self.__get_top_features(df, target, TOP_FEATURES_NUMBER)

        return df[[target] + top_features]

    def save_df(self, df: pd.DataFrame, folder: str, dataset_name: str) -> None:
        file_path = f"{self.data_path}/{folder}/mbajk_dataset_{dataset_name}.csv"
        df.to_csv(file_path, index=False)

    @staticmethod
    def __get_top_features(df: pd.DataFrame, target_feature: str, num_of_features: int) -> List[str]:
        input_cols = df.columns.tolist()
        input_cols.remove(target_feature)

        # runs only if rows are greater than 3
        information_gain = mutual_info_regression(df[input_cols], df[target_feature])

        feature_importance = pd.Series(information_gain, index=input_cols)
        feature_importance.name = "Information Gain Scores"
        feature_importance.sort_values(ascending=False, inplace=True)

        return feature_importance.head(num_of_features).index.tolist()
