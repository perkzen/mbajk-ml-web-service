import os
import pandas as pd
from multiprocessing import Pool
from src.data.data_manager import DataManager
from src.data.data_processor import DataProcessor
from src.utils.decorators import execution_timer


def get_station_data(df: pd.DataFrame, station_number: int) -> pd.DataFrame:
    return df[df["number"] == station_number]


def process_station(station_data):
    station_number, df_weather, df_stations, processor, manager = station_data

    station = get_station_data(df_stations, station_number)
    df = station.merge(df_weather, on="date", how="left")
    df = df.dropna()
    df = df.drop_duplicates(subset=["date"])

    try:
        df = processor.clean(df)
        manager.save(f"processed/{station_number}", f"mbajk_station_{station_number}", df, override=True)
    except ValueError as e:
        print(e)
        print(f"[Process Data] - Not enough data to process for station {station_number}")


@execution_timer("Process Data")
def main() -> None:
    manager = DataManager(data_path="data")
    processor = DataProcessor()

    try:
        df_weather = manager.get_dataframe("raw", "weather")
        df_stations = manager.get_dataframe("raw", "mbajk_stations")
        df_weather = df_weather.drop_duplicates(subset=["date"])

        stations = df_stations.to_dict(orient="records")
        station_data = [(station["number"], df_weather, df_stations, processor, manager) for station in stations]

        with Pool(processes=os.cpu_count()) as pool:
            pool.map(process_station, station_data)

    except FileNotFoundError:
        print("[Process Data] - No data to process")

    finally:
        df_weather = manager.get_dataframe("raw", "weather")
        df_stations = manager.get_dataframe("raw", "mbajk_stations")

        df_weather = df_weather.drop_duplicates(subset=["date"])

        current_data = df_stations.merge(df_weather, on="date", how="left")
        current_data = current_data.dropna()

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

        current_data = current_data[features]
        manager.save("processed", "current_data", current_data, override=True)


if __name__ == '__main__':
    main()
