import pandas as pd
from typing import List
from sklearn.feature_selection import mutual_info_regression
from src.config import TOP_FEATURES_NUMBER


class DataProcessor:

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df["date"] = pd.to_datetime(df["date"])
        df.sort_values(by="date", inplace=True)

        df.drop(columns=["name", "address", "date", "number", "bike_stands", "available_bikes", "lat", "lon",
                         "last_updated"],
                inplace=True)

        target = "available_bike_stands"

        top_features = self.__get_top_features(df, target, TOP_FEATURES_NUMBER)

        return df[[target] + top_features]

    @staticmethod
    def __get_top_features(df: pd.DataFrame, target_feature: str, num_of_features: int) -> List[str]:
        input_cols = df.columns.tolist()
        input_cols.remove(target_feature)

        information_gain = mutual_info_regression(df[input_cols], df[target_feature])

        feature_importance = pd.Series(information_gain, index=input_cols)
        feature_importance.sort_values(ascending=False, inplace=True)

        return feature_importance.head(num_of_features).index.tolist()
