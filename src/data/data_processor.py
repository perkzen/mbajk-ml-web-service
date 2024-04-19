import pandas as pd
from typing import List
from sklearn.feature_selection import mutual_info_regression


class DataProcessor:

    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        df["date"] = pd.to_datetime(df["date"])
        df.sort_values(by="date", inplace=True)

        # df = self.add_new_features(df=df)

        df.drop(columns=["name", "address", "date", "number", "bike_stands", "available_bikes", "lat", "lon",
                         "last_updated"],
                inplace=True)

        target = "available_bike_stands"

        # top_features = self.__get_top_features(df=df, target_feature=target, num_of_features=settings.top_features)

        top_features = ["temperature", "surface_pressure", "apparent_temperature", "dew_point"]

        return df[[target] + top_features]

    @staticmethod
    def __get_top_features(df: pd.DataFrame, target_feature: str, num_of_features: int) -> List[str]:
        input_cols = df.columns.tolist()
        input_cols.remove(target_feature)

        information_gain = mutual_info_regression(df[input_cols], df[target_feature])

        feature_importance = pd.Series(information_gain, index=input_cols)
        feature_importance.sort_values(ascending=False, inplace=True)

        return feature_importance.head(num_of_features).index.tolist()

    @staticmethod
    def add_new_features(df: pd.DataFrame) -> pd.DataFrame:
        df["weekend"] = df["date"].apply(lambda x: 1 if x.weekday() in [5, 6] else 0)
        df["is_day"] = df["date"].apply(lambda x: 1 if 6 <= x.hour <= 18 else 0)
        df["season"] = df["date"].apply(lambda x: (x.month % 12 + 3) // 3)
        df["hour"] = df["date"].dt.hour
        df["day_of_week"] = df["date"].dt.weekday

        return df
