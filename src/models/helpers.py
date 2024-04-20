import os

import pandas as pd


def load_dataset() -> pd.DataFrame:
    dataset = pd.read_csv("data/processed/mbajk_processed.csv")
    dataset.drop(columns=["date"], inplace=True)
    return dataset


def load_bike_station_dataset(station_number) -> pd.DataFrame:
    dataset = pd.read_csv(f"data/processed/{station_number}/mbajk_station_{station_number}.csv")
    return dataset


def write_metrics_to_file(file_path: str, model_name: str, mse: float, mae: float, evs: float) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
        file.write(f"Model: {model_name}\n")
        file.write(f"MSE: {mse}\n")
        file.write(f"MAE: {mae}\n")
        file.write(f"EVS: {evs}\n")
