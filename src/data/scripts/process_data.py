import pandas as pd
from src.data.data_manager import DataManager
from src.data.data_processor import DataProcessor

from src.utils.decorators import execution_timer


@execution_timer("Process Data")
def main() -> None:
    manager = DataManager(data_path="data")
    processor = DataProcessor()

    try:
        df_weather = manager.get_dataframe("raw", "weather")
        df_stations = manager.get_dataframe("raw", "mbajk_stations")

        stations = df_stations.to_dict(orient="records")

        # we need at least 4 rows to calculate mutual information
        if len(df_weather) < 3:
            return

        df_weather['merge_key'] = 1
        df_stations['merge_key'] = 1

        for station in stations:
            df = pd.merge(df_weather, df_stations[df_stations['number'] == station['number']], on='merge_key')
            df = processor.clean(df)
            manager.save("processed", f"mbajk_station_{station["number"]}", df, override=True)

    except FileNotFoundError:
        print("[Process Data] - No data to process")


if __name__ == '__main__':
    main()
