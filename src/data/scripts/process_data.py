import pandas as pd
from src.data.data_manager import DataManager
from src.data.data_processor import DataProcessor

from src.utils.decorators import execution_timer


def get_station_data(df: pd.DataFrame, station_number: int) -> pd.DataFrame:
    return df[df["number"] == station_number]


@execution_timer("Process Data")
def main() -> None:
    manager = DataManager(data_path="data")
    processor = DataProcessor()

    try:
        df_weather = manager.get_dataframe("raw", "weather")
        df_stations = manager.get_dataframe("raw", "mbajk_stations")

        stations = df_stations.to_dict(orient="records")

        for station in stations:
            station_number = station["number"]
            df = pd.merge(df_weather, get_station_data(df_stations, station_number), on='date', how='inner')
            try:
                df = processor.clean(df)
                manager.save("processed", f"mbajk_station_{station_number}", df, override=True)
            except ValueError:
                # Information gain throws exception if there is not enough data to calculate mutual information
                print(f"[Process Data] - Not enough data to process for station {station_number}")

    except FileNotFoundError:
        print("[Process Data] - No data to process")


if __name__ == '__main__':
    main()
