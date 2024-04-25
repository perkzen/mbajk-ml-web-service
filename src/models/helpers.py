import os

import pandas as pd


def load_bike_station_dataset(station_number: str, file: str) -> pd.DataFrame:
    dataset = pd.read_csv(f"data/processed/{station_number}/{file}.csv")
    return dataset


def write_metrics_to_file(file_path: str, model_name: str, mse: float, mae: float, evs: float) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
        file.write(f"Model: {model_name}\n")
        file.write(f"MSE: {mse}\n")
        file.write(f"MAE: {mae}\n")
        file.write(f"EVS: {evs}\n")
