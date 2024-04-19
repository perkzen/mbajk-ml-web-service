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
    df = pd.merge(df_weather, get_station_data(df_stations, station_number), on='date', how='inner')

    try:
        df = processor.clean(df)
        manager.save("processed", f"mbajk_station_{station_number}", df, override=True)
    except ValueError as e:
        print(e)
        print(f"[Process Data] - Not enough data to process for station {station_number}")


def concat_all_stations_data():
    concatenated_df = pd.DataFrame()
    directory = "data/processed"
    for filename in os.listdir(directory):
        # Check if the file is a CSV file
        if filename.endswith(".csv") and filename.startswith("mbajk_station_"):
            # Read the CSV file
            df = pd.read_csv(os.path.join(directory, filename))
            # Add a new column for the file name
            df['station_number'] = filename.split('_')[2].split('.')[0]
            # Concatenate the DataFrame to the main DataFrame
            concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)

    concatenated_df.sort_values(by="station_number", inplace=True)
    concatenated_df.to_csv("data/processed/current_data.csv", index=False)


@execution_timer("Process Data")
def main() -> None:
    manager = DataManager(data_path="data")
    processor = DataProcessor()

    try:
        df_weather = manager.get_dataframe("raw", "weather")
        df_stations = manager.get_dataframe("raw", "mbajk_stations")

        stations = df_stations.to_dict(orient="records")
        station_data = [(station["number"], df_weather, df_stations, processor, manager) for station in stations]

        with Pool(processes=os.cpu_count()) as pool:
            pool.map(process_station, station_data)

    except FileNotFoundError:
        print("[Process Data] - No data to process")

    finally:
        concat_all_stations_data()


if __name__ == '__main__':
    main()
