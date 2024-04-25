import os
import numpy as np
import pandas as pd
from multiprocessing import Pool
from typing import Tuple
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from src.data.data_manager import DataManager
from src.utils.decorators import execution_timer


def get_station_data(df: pd.DataFrame, station_number: int) -> pd.DataFrame:
    return df[df["number"] == station_number]


def save_station_data(data: Tuple[int, pd.DataFrame, DataManager]):
    number, current_data, manager = data

    station_data = get_station_data(current_data, number)

    manager.save(f"processed/{number}", f"mbajk_station_{number}", station_data, override=True)


def fill_missing_values_with_predictions(df: pd.DataFrame, cols_to_fill: list[str]) -> pd.DataFrame:
    filled_df = df.copy()

    pipeline = Pipeline(steps=[
        ("scaler", MinMaxScaler()),
        ("model", RandomForestRegressor())
    ])

    for col in cols_to_fill:
        incomplete_rows = filled_df[filled_df[col].isna()]
        complete_rows = filled_df[~filled_df[col].isna()]

        features = [c for c in filled_df.columns if c != col]
        target = col

        X_train = complete_rows[features]
        y_train = complete_rows[target]

        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(incomplete_rows[features])

        predictions_rounded = np.round(predictions, 1)

        filled_df.loc[filled_df[col].isna(), col] = predictions_rounded

    return filled_df


def process_all_data(weather_data: pd.DataFrame, stations_data: pd.DataFrame) -> pd.DataFrame:
    current_data = stations_data.merge(weather_data, on="date", how="left")
    current_data = current_data.drop_duplicates(subset=["date", "number"])

    current_data["date"] = pd.to_datetime(current_data["date"])
    current_data.sort_values(by="date", inplace=True)

    features = ["available_bike_stands",
                "temperature",
                "surface_pressure",
                "apparent_temperature",
                "dew_point",
                "number"
                ]

    data_to_fill = current_data[features]

    cols_to_fill = data_to_fill.columns[data_to_fill.isna().sum() > 0]

    filled_current_data = fill_missing_values_with_predictions(data_to_fill, cols_to_fill)

    filled_current_data["date"] = current_data["date"]

    return filled_current_data


@execution_timer("Process Data")
def main() -> None:
    manager = DataManager(data_path="data")

    df_weather = manager.get_dataframe("raw", "weather")
    df_weather = df_weather.drop_duplicates(subset=["date"])

    df_stations = manager.get_dataframe("raw", "mbajk_stations")

    current_data = process_all_data(df_weather, df_stations)

    unique_station_numbers = df_stations['number'].unique()
    data = [(number, current_data, manager) for number in unique_station_numbers]

    try:
        with Pool(processes=os.cpu_count()) as pool:
            pool.map(save_station_data, data)
    except FileNotFoundError:
        print("[Process Data] - No data to process")

    # Date col is required for mbajk_station_{station_number} dataset
    current_data = current_data.drop("date", axis=1)
    manager.save("processed", "current_data", current_data, override=True)


if __name__ == '__main__':
    main()
